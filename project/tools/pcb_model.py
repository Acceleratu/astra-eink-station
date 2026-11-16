"""Board placement and planar geometry. All lengths use mm, top view, counterclockwise."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import json
import hashlib
import math

from shapely import affinity
from shapely.geometry import Point, box

BASE = Path(__file__).resolve().parents[1]
LAYOUT = BASE / "layout"
BLOCKS = ("power", "radio", "display", "wake")
LAYERS = {1: "F.Cu", 16: "B.Cu"}


def rotate(x, y, angle):
    r = math.radians(float(angle))
    return (round(x*math.cos(r) - y*math.sin(r), 6),
            round(x*math.sin(r) + y*math.cos(r), 6))


def point(x, y, position):
    dx, dy = rotate(float(x), float(y), position.get("rot", 0))
    return (round(float(position["x"]) + dx, 6), round(float(position["y"]) + dy, 6))


def center_of(pinch, part):
    return point(pinch["x"], pinch["y"], part)


def rect_poly(cx, cy, w, h, angle=0, roundness=0):
    """EAGLE roundness is a percentage of the maximum pad corner radius."""
    w, h = float(w), float(h)
    r = min(w, h) * float(roundness or 0) / 200
    if r < 1e-6:
        polygon = box(-w / 2, -h / 2, w / 2, h / 2)
    elif abs(w-2*r) < 1e-8 and abs(h-2*r) < 1e-8:
        polygon = Point(0, 0).buffer(r, quad_segs=40)
    else:
        polygon = box(-w/2 + r, -h/2+r, w/2-r, h/2-r).buffer(r, quad_segs=32)
    polygon = affinity.rotate(polygon, angle, origin=(0, 0))
    return affinity.translate(polygon, cx, cy)


def pad_shape(pad, part):
    cx, cy = center_of(pad, part)
    return rect_poly(cx, cy, pad["w"], pad["h"],
                     float(part.get("rot",0)) + float(pad.get("rot",0)),
                     pad.get("roundness", 100 if pad.get("drill") else 0))


def body_shape(p, f):
    offset = f.get("body_center", (0, 0))
    x,y = point(*offset,p)
    return rect_poly(x,y,*f["body"][:2],p.get("rot",0))


def read(path):
    return json.loads(Path(path).read_text())


def write(path, obj):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")


def rect_transform(rect, tf):
    x1,y1,x2,y2 = rect
    pts = [point(x,y,tf) for x,y in [(x1,y1),(x1,y2),(x2,y1),(x2,y2)]]
    return (min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts))


@dataclass
class Design:
    parts: list
    footprints: dict
    config: dict
    pads: dict
    nets: dict
    rules: dict
    fixed_wires: list
    fixed_vias: list
    keepouts: list
    planes: list
    board_holes: list
    package_holes: list

    @property
    def size(self):
        return self.config["board_mm"]


def get_design():
    from ecad_common import load_design
    components, footprints = load_design()
    config = read(LAYOUT / "placement.json")
    parts, pads, nets = [], {}, defaultdict(list)
    extra_holes = []
    part_blocks = {}
    local_parts = {}
    for block in BLOCKS:
        path = BASE / "hardware" / (block+".json")
        if path.is_file():
            for p in read(path)["parts"]:
                part_blocks[p["ref"]] = block
                local_parts[p["ref"]] = p
    wires, vias, keepouts, planes = [], [], [], []
    for p in components:
        if p.get("board",True) is False or p.get("offboard"): continue
        source = local_parts.get(p["ref"],p)
        block = part_blocks[p["ref"]]
        tf = config["blocks"][block]
        x,y = point(source["x"],source["y"],tf)
        part = dict(source,x=x,y=y,rot=(float(source.get("rot",0))+tf.get("rot",0))%360,block=block)
        part.update(config.get("overrides",{}).get(p["ref"],{}))
        part["pins"] = {str(k):n for k,n in part.get("pins",{}).items() if n and str(n).upper() not in ("NC","N/C","DNC")}
        parts.append(part)
        fp = footprints[part["footprint"]]
        for pad in fp["pads"]:
            n = str(pad["n"])
            if (p["ref"],n) in pads:
                raise ValueError(f"duplicate physical pad {p['ref']}.{n}")
            cx,cy=center_of(pad,part)
            net = part["pins"].get(n)
            pads[(p["ref"],n)] = dict(geom=pad_shape(pad,part), center=(cx,cy), net=net, pad=pad, part=part, type="pth" if pad.get("drill") else "smd")
            if net: nets[net].append((p["ref"],n))
        for h in fp.get("holes",[]):
            hx,hy=point(h["x"],h["y"],part)
            extra_holes.append(dict(x=hx,y=hy,drill=h["drill"],owner=p["ref"]))
        undefined = set(part["pins"]) - {str(pad["n"]) for pad in fp["pads"]}
        if undefined: raise ValueError(f"undefined pads on {p['ref']}: {undefined}")
    for block in BLOCKS:
        guidance = BASE/"hardware"/(block+"-layout.json")
        if guidance.exists():
            tf=config["blocks"][block]
            g=read(guidance)
            for w in g.get("wires",[]):
                wires.append(dict(w,points=[point(x,y,tf) for x,y in w["points"]]))
            for via in g.get("vias",[]):
                x,y=point(via["x"],via["y"],tf)
                vias.append(dict(via,x=x,y=y))
            for source,dest in ((g.get("keepouts",[]),keepouts),(g.get("planes",[]),planes)):
                for region in source:
                    dest.append(dict(region,rect=rect_transform(region["rect"],tf)))
    for kind,dest in (("wires",wires),("vias",vias),("keepouts",keepouts),("planes",planes)):
        dest.extend(config.get(kind,[]))
    return Design(parts, footprints, config, pads, dict(nets), config["rules"], wires, vias, keepouts, planes, config["holes"],extra_holes)


def routing_fingerprint(design):
    """Hash connectivity and all geometry that the router consumed."""
    parts=[(p["ref"],p["footprint"],p["x"],p["y"],p["rot"],sorted(p["pins"].items())) for p in design.parts]
    pads=[(ref,n,tuple(item["center"]),tuple(round(a,6) for a in item["geom"].bounds),item["pad"])
          for (ref,n),item in design.pads.items()]
    snapshot=(parts,pads,design.config,design.fixed_wires,design.fixed_vias,design.package_holes,design.planes,design.keepouts)
    return hashlib.sha256(json.dumps(snapshot,sort_keys=True,separators=(",",":")).encode()).hexdigest()
