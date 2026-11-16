"""Shared Fusion/EAGLE XML and footprint geometry. Dimensions are in millimetres."""
import json
from pathlib import Path
from math import cos, radians, sin
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = "ASTRA"
BLOCKS = ("power", "radio", "display", "wake")


def num(v):
    return f"{float(v):.6f}".rstrip("0").rstrip(".") or "0"


def tag(parent, tag_name, **attrs):
    return ET.SubElement(parent, tag_name, {k: str(v) for k, v in attrs.items() if v is not None})


def load_design():
    parts, footprints = [], {}
    for path in sorted((ROOT / "hardware").glob("*-footprints.json")):
        data = json.loads(path.read_text())
        for name, geometry in data.items():
            if name in footprints and geometry != footprints[name]:
                raise ValueError(f"Conflicting footprint {name} in {path}")
            footprints[name] = geometry
    for block in BLOCKS:
        src = ROOT / "hardware" / f"{block}.json"
        if src.exists():
            for part in json.loads(src.read_text())["parts"]:
                part = dict(part, block=block)
                parts.append(part)
    return parts, footprints


def scaffold():
    root = ET.Element("eagle", {"version": "9.6.2"})
    drawing = tag(root, "drawing")
    settings = tag(drawing, "settings")
    tag(settings, "setting", alwaysvectorfont="no")
    tag(settings, "setting", verticaltext="up")
    tag(drawing, "grid", distance="0.1", unitdist="inch", unit="inch", style="lines",
        multiple="1", display="no", altdistance="0.01", altunitdist="inch", altunit="inch")
    layers = tag(drawing, "layers")
    names = {1: "Top", 16: "Bottom", 17: "Pads", 18: "Vias", 19: "Unrouted", 20: "Dimension",
             21: "tPlace", 22: "bPlace", 23: "tOrigins", 24: "bOrigins", 25: "tNames",
             26: "bNames", 27: "tValues", 28: "bValues", 29: "tStop", 30: "bStop",
             31: "tCream", 32: "bCream", 33: "tFinish", 34: "bFinish", 35: "tGlue",
             36: "bGlue", 37: "tTest", 38: "bTest", 39: "tKeepout", 40: "bKeepout",
             41: "tRestrict", 42: "bRestrict", 43: "vRestrict", 44: "Drills", 45: "Holes",
             46: "Milling", 47: "Measures", 48: "Document", 49: "Reference", 51: "tDocu",
             52: "bDocu", 91: "Nets", 92: "Busses", 93: "Pins", 94: "Symbols", 95: "Names",
             96: "Values", 97: "Info", 98: "Guide"}
    hidden = {23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
              41, 42, 43, 44, 45, 47, 48, 49, 51, 52, 93, 98}
    colors = {1: 4, 16: 1, 17: 2, 18: 2, 19: 6, 20: 15, 21: 7, 22: 7, 25: 7, 26: 7,
              29: 7, 30: 7, 31: 7, 32: 7, 41: 4, 42: 1, 43: 2, 91: 2, 92: 1, 93: 2,
              94: 4, 95: 7, 96: 7, 97: 7, 98: 6}
    for index, name in sorted(names.items()):
        tag(layers, "layer", number=index, name=name, color=colors.get(index, 7),
            fill=1, visible="no" if index in hidden else "yes", active="yes")
    return root, drawing


def line(parent, x1, y1, x2, y2, width, layer, **extras):
    return tag(parent, "wire", x1=num(x1), y1=num(y1), x2=num(x2), y2=num(y2),
               width=num(width), layer=layer, **extras)


def box(parent, cx, cy, w, h, width, layer):
    p = [(cx-w/2, cy-h/2), (cx+w/2, cy-h/2), (cx+w/2, cy+h/2), (cx-w/2, cy+h/2)]
    for start, end in zip(p, p[1:]+p[:1]):
        line(parent, *start, *end, width, layer)


def rotation(angle):
    if isinstance(angle, str) and ("R" in angle):
        return angle
    return "R" + num(angle)


def custom_aperture(pkg, p, kind, layer):
    """A dimensioned SMD-defined land or stencil aperture, independent of DRC swell."""
    w = p[kind + "_w"]
    h = p.get(kind + "_h", w)
    if w == 0 or h == 0:
        return
    x, y = p["x"], p["y"]
    circular = p.get("shape") in ("round", "circle") or p.get("roundness") == 100
    if circular and abs(w-h) < 1e-9:
        # A stroked circle with stroke=diameter/2 and radius=diameter/4 is a solid disc.
        tag(pkg, "circle", x=num(x), y=num(y), radius=num(w/4), width=num(w/2), layer=layer)
    else:
        degrees = float(str(p.get("rot", 0)).lstrip("R"))
        a = radians(degrees)
        polygon = tag(pkg, "polygon", width="0", layer=layer)
        for lx, ly in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]:
            tag(polygon, "vertex", x=num(x+lx*cos(a)-ly*sin(a)), y=num(y+lx*sin(a)+ly*cos(a)))


def add_packages(library, footprints):
    packages = tag(library, "packages")
    for name, geo in sorted(footprints.items()):
        pkg = tag(packages, "package", name=name)
        tag(pkg, "description").text = str(geo.get("source", name))
        for p in geo["pads"]:
            attrs = {"name": str(p["n"]), "x": num(p["x"]), "y": num(p["y"])}
            if p.get("rot"):
                attrs["rot"] = rotation(p["rot"])
            for flag in ("stop", "cream", "thermals"):
                if flag in p:
                    attrs[flag] = "yes" if p[flag] in (True, "yes") else "no"
            if p.get("drill"):
                attrs.pop("cream", None)
                attrs.update(drill=num(p["drill"]), diameter=num(p.get("diameter", min(p["w"], p["h"]))),
                             shape=p.get("shape", "round"))
                tag(pkg, "pad", **attrs)
            else:
                for kind, layer, flag in (("mask", 29, "stop"), ("paste", 31, "cream")):
                    if kind + "_w" in p:
                        attrs[flag] = "no"
                        custom_aperture(pkg, p, kind, layer)
                attrs.update(dx=num(p["w"]), dy=num(p["h"]), layer=p.get("layer", 1),
                             roundness=p.get("roundness", 100 if p.get("shape") in ("round","circle") else 0))
                tag(pkg, "smd", **attrs)
        for hole in geo.get("holes", []):
            tag(pkg, "hole", x=num(hole["x"]), y=num(hole["y"]), drill=num(hole["drill"]))
        if geo.get("body"):
            cx, cy = geo.get("body_center", [0, 0])
            box(pkg, cx, cy, *geo["body"], 0.08, 51)
        for rectangle in geo.get("rectangles", []):
            tag(pkg, "rectangle", **rectangle)
        for wire in geo.get("wires", []):
            tag(pkg, "wire", **wire)
        for circle in geo.get("circles", []):
            tag(pkg, "circle", **circle)
        for poly in geo.get("polygons", []):
            shape = tag(pkg, "polygon", layer=poly["layer"], width=num(poly.get("width", 0)))
            for vx, vy in poly["vertices"]:
                tag(shape, "vertex", x=num(vx), y=num(vy))
    return packages


def write_xml(root, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="  ")
    with path.open("wb") as out:
        out.write(b'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE eagle SYSTEM "eagle.dtd">\n')
        out.write(ET.tostring(root, encoding="utf-8"))
        out.write(b"\n")
