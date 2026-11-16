"""Build the PCB's indexed image from registered, lossless Fusion exports.

Pass a capture directory containing refs/<name>.webp (500 dpi), sets.json
(name to visible layer numbers), train.json (calibration names), and
fusion-layers.json (Fusion's layer catalog). Reference names 'none', 'all',
'layer-NN' and 'drop-NN' denote the empty, full, solo and all-but-one views.
All remaining exports outside the calibration set serve as validation images.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def read_json(path):
    return json.loads(path.read_text())


def compact(flags, mask):
    index = 0
    weight = 1
    while mask:
        bit = mask & -mask
        if flags & bit:
            index += weight
        weight *= 2
        mask ^= bit
    return index


def build(source, dest):
    def pixels(name):
        with Image.open(source / 'refs' / (name + '.webp')) as image:
            rgb = np.asarray(image.convert('RGB'), dtype=np.uint32)
        return rgb[:, :, 0] << 16 | rgb[:, :, 1] << 8 | rgb[:, :, 2]

    sets = read_json(source / 'sets.json')
    training = read_json(source / 'train.json')
    empty, full = pixels('none'), pixels('all')
    layers = []
    dependencies = np.zeros(empty.shape, dtype=np.uint32)
    for layer in sets['all']:
        affected = (pixels(f'layer-{layer:02}') != empty) | (pixels(f'drop-{layer:02}') != full)
        if affected.any():
            dependencies[affected] |= 1 << len(layers)
            layers.append(layer)

    def flags(name):
        return sum(1 << i for i, layer in enumerate(layers) if layer in sets[name])

    # Partition pixels by local layer membership and identical colour histories.
    classes = dependencies.ravel().astype(np.uint64)
    for name in training:
        history = classes << 24 | pixels(name).ravel()
        _, classes = np.unique(history, return_inverse=True)
        classes = classes.astype(np.uint64)
    _, representatives = np.unique(classes, return_index=True)
    masks = list(map(int, dependencies.ravel()[representatives]))
    if len(masks) > 256:
        raise ValueError('This revision exceeds the 8-bit indexed PNG palette')
    colors = [[None] * (1 << mask.bit_count()) for mask in masks]
    for name in training:
        values = pixels(name).ravel()[representatives]
        for mask, row, rgb in zip(masks, colors, values):
            index = compact(flags(name), mask)
            if row[index] not in (None, rgb):
                raise ValueError(f'Conflicting palette values for {name}')
            row[index] = int(rgb)
    if any(None in row for row in colors):
        raise ValueError('Capture more combinations to cover every layer intersection')
    indices = classes.reshape(empty.shape).astype(np.uint8)
    for name in sets.keys() - training.keys():
        selected = flags(name)
        palette = np.array([row[compact(selected, m)] for m, row in zip(masks, colors)], dtype=np.uint32)
        if not np.array_equal(palette[indices], pixels(name)):
            raise ValueError(f'Mismatch with independent Fusion export {name}')

    catalog = [{'id': l['id'], 'name': l['name'], 'color': '#' + l['color'][-6:]}
               for l in read_json(source / 'fusion-layers.json') if l['id'] in sets['all']]
    table = dict(layers=layers, masks=masks, colors=colors, catalog=catalog)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'pcb-layer-colors.json').write_text(json.dumps(table, separators=(',', ':')))
    image = Image.frombytes('P', (indices.shape[1], indices.shape[0]), indices.tobytes())
    image.putpalette(b''.join(row[0].to_bytes(3, 'big') for row in colors))
    image.save(dest / 'pcb-layer-index.png', bits=8, optimize=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('captures', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    build(args.captures, args.destination)
