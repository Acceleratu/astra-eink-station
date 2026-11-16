"""Register 555 dpi Fusion sheet exports and build lossless detail tiles and pick targets.

Usage: schematic_details.py CAPTURES, containing s1-555.png through s7-555.png.
Run against the same revision of the schematic and base explorer assets.
"""
import json
import math
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

EXPLORER = Path(__file__).resolve().parents[1]
TILE = 2048
# The drawing frame's corners in the PDF coordinates shared by both display modes.
LEFT, TOP, RIGHT, BOTTOM = 19.5, 32.22, 1171.38, 809.7
FRAME_W, FRAME_H = 406.4, 274.32


def sheet_point(x, y):
    return [round(LEFT + x * (RIGHT - LEFT) / FRAME_W, 3),
            round(BOTTOM - y * (BOTTOM - TOP) / FRAME_H, 3)]


def registered_box(image):
    gray = np.asarray(image.convert('L'))
    h, w = gray.shape

    def center(strip):
        inds = np.flatnonzero((strip < 220).mean(axis=0) > .98)
        if not len(inds):
            raise ValueError('Missing schematic frame')
        return inds.mean() + .5

    x0, x1 = center(gray[16:-16, :12]), w - 12 + center(gray[16:-16, -12:])
    y0, y1 = center(gray[:12, 16:-16].T), h - 12 + center(gray[-12:, 16:-16].T)
    dx, dy = (RIGHT - LEFT) / (x1 - x0), (BOTTOM - TOP) / (y1 - y0)
    return [LEFT - x0 * dx, TOP - y0 * dy, w * dx, h * dy]


def symbol_geometry(sheet, symbols, parts):
    boxes, pin_strokes = {}, {}
    lengths = {'point': 0, 'short': 2.54, 'middle': 5.08, 'long': 7.62}
    for instance in sheet.findall('instances/instance'):
        ref = instance.get('part')
        sym = symbols[parts[ref], instance.get('gate')]
        coords = []
        for wire in sym.findall('wire'):
            coords.extend((float(wire.get('x' + i)), float(wire.get('y' + i))) for i in ('1', '2'))
        for circle in sym.findall('circle'):
            x, y, r = (float(circle.get(k)) for k in ('x', 'y', 'radius'))
            coords.extend([(x-r, y-r), (x+r, y+r)])
        rotation = math.radians(float(instance.get('rot', 'R0')[1:]))
        co, si = math.cos(rotation), math.sin(rotation)
        x0, y0 = float(instance.get('x')), float(instance.get('y'))
        def at(x, y):
            return sheet_point(x0 + co*x - si*y, y0 + si*x + co*y)

        corners = [at(x, y) for x, y in coords]
        xs, ys = zip(*corners)
        boxes[ref] = [min(xs), min(ys), round(max(xs)-min(xs), 3), round(max(ys)-min(ys), 3)]
        for pin in sym.findall('pin'):
            length = lengths[pin.get('length', 'middle')]
            if length:
                x, y = float(pin.get('x')), float(pin.get('y'))
                angle = math.radians(float(pin.get('rot', 'R0')[1:]))
                end = at(x + length * math.cos(angle), y + length * math.sin(angle))
                pin_strokes[ref, pin.get('name')] = 'M{} {}L{} {}'.format(*at(x, y), *end)
    return boxes, pin_strokes


def interactive_geometry(sheet, design, symbols, parts):
    bodies, pin_strokes = symbol_geometry(sheet, symbols, parts)
    paths, junctions, pins, pin_paths = {}, {}, {}, {}
    for net in sheet.findall('nets/net'):
        name = net.get('name')
        path = []
        for wire in net.findall('segment/wire'):
            ends = [sheet_point(float(wire.get('x' + i)), float(wire.get('y' + i))) for i in ('1', '2')]
            path.append('M{} {}L{} {}'.format(*ends[0], *ends[1]))
        if path:
            paths[name] = ''.join(path)
        points = [sheet_point(float(j.get('x')), float(j.get('y'))) for j in net.findall('segment/junction')]
        if points:
            junctions[name] = points
        strokes = []
        for pin in net.findall('segment/pinref'):
            key = (pin.get('part'), pin.get('pin'))
            pins[key] = name
            if key in pin_strokes:
                strokes.append(pin_strokes[key])
        if strokes:
            pin_paths[name] = ''.join(strokes)

    # Pin legends can have the same spelling as a different board net (e.g.
    # SDA on the display connector). Resolve those clicks by their actual pinref.
    labels = []
    for word, x, y, w, h in design['netLabels']:
        key = word
        for ref, (left, top, width, height) in bodies.items():
            if left <= x+w/2 <= left+width and top <= y+h/2 <= top+height:
                key = pins.get((ref, word), word)
                break
        labels.append([key, x, y, w, h])
    return dict(bodies=bodies, paths=paths, junctions=junctions, netLabels=labels, pinPaths=pin_paths)


def build(captures):
    repo = EXPLORER.parent
    schematic = ET.parse(repo / 'project/schematic/astra.sch').find('.//schematic')
    parts = {p.get('name'): (p.get('library'), p.get('deviceset')) for p in schematic.findall('parts/part')}
    symbols = {}
    for lib in schematic.findall('libraries/library'):
        by_name = {s.get('name'): s for s in lib.findall('symbols/symbol')}
        for ds in lib.findall('devicesets/deviceset'):
            for gate in ds.findall('gates/gate'):
                symbols[(lib.get('name'), ds.get('name')), gate.get('name')] = by_name[gate.get('symbol')]
    design = json.loads((EXPLORER / 'data/design.json').read_text())
    dest = EXPLORER / 'native/schematic'
    dest.mkdir(exist_ok=True)
    records = []
    for i, sheet in enumerate(schematic.findall('sheets/sheet'), 1):
        with Image.open(captures / f's{i}-555.png') as image:
            record = interactive_geometry(sheet, design['sheets'][i-1], symbols, parts)
            with Image.open(EXPLORER / f'native/sheet-{i:02}.webp') as preview:
                record.update(size=list(image.size), box=registered_box(image), previewWidth=preview.width)
            for y in range(0, image.height, TILE):
                for x in range(0, image.width, TILE):
                    # Two pixels of overlap cover subpixel sampling at tile boundaries.
                    crop = (max(0, x-2), max(0, y-2), min(image.width, x+TILE+2), min(image.height, y+TILE+2))
                    tile = image.crop(crop).convert('RGB')
                    tile.save(dest / f'{i}-{x//TILE}-{y//TILE}.webp', lossless=True, method=4)
        records.append(record)
    (dest / 'sheets.json').write_text(json.dumps(dict(tileSize=TILE, sheets=records), separators=(',', ':')))


if __name__ == '__main__':
    build(Path(sys.argv[1]))
