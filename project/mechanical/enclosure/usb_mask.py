"""Black optical mask installed on the front of GCT USB4135, in board millimetres.

The continuous PSA ring seals the stamped stainless front. The separate folded
PET strap anchors the skirt to the top shell. Both leave with the serviced PCB.
"""

from math import pi, sqrt
from pathlib import Path

import cadquery as cq


PORT_Y, PORT_Z = 67.0, 1.725
LIP_X = -0.0025
FILM_THICKNESS = 0.125
PSA_THICKNESS = 0.050
STRAP_THICKNESS = 0.050
MASK_BACK_X = LIP_X - PSA_THICKNESS
MASK_FRONT_X = MASK_BACK_X - FILM_THICKNESS
SKIRT = (15.00, 7.40, 0.80)
OPENING = (8.68, 2.90, 1.08)
RING_OUTER = (11.20, 3.20, 1.25)
RING_INNER = (8.74, 2.96, 1.11)
GUARD_CLEARANCE = (9.24, 3.46, 1.40)
GUARD_THICKNESS = 0.050
SHELL_TOP_Z = 3.305
STRAP_WIDTH = 6.00
STRAP_OUTER_BEND_R = 0.380
STRAP_END_X = 2.50
STRAP_END_Z = 5.11
STRAP_CENTRE_X = MASK_BACK_X + STRAP_OUTER_BEND_R
STRAP_CENTRE_Z = SHELL_TOP_Z + STRAP_OUTER_BEND_R

COLORS = {
    'USB_black_PET_mask': (.025, .027, .029),
    'USB_black_PSA_lip_seal': (.038, .040, .042),
    'USB_black_PET_side_guards': (.029, .031, .033),
    'USB_black_PET_anchor': (.032, .034, .036),
    'USB_black_PSA_anchor': (.043, .046, .048),
}


def _rounded(width, height, radius):
    x, y = width / 2, height / 2
    wire = cq.Wire.makePolygon([(-x, -y, 0), (x, -y, 0),
                                (x, y, 0), (-x, y, 0)], close=True)
    return wire.fillet2D(radius, wire.Vertices())


def _to_board(body, axial_start):
    return body.rotate((0, 0, 0), (1, 1, 1), 120).translate((axial_start, PORT_Y, PORT_Z))


def _annulus(outer, inner, axial_start, thickness):
    body = cq.Solid.extrudeLinear(_rounded(*outer), [_rounded(*inner)],
                                 cq.Vector(0, 0, thickness))
    return _to_board(body, axial_start)


def _guard_outlines():
    broad_adhesive = cq.Face.makeFromWires(_rounded(*RING_OUTER))
    metal_relief = cq.Face.makeFromWires(_rounded(*GUARD_CLEARANCE))
    return [face.outerWire() for face in broad_adhesive.cut(metal_relief).Faces()]


def _side_guards():
    ears = [cq.Solid.extrudeLinear(wire, [], (0, 0, GUARD_THICKNESS))
            for wire in _guard_outlines()]
    return _to_board(cq.Compound.makeCompound(ears), LIP_X)


def _anchor_layer(outer_radius, inner_radius):
    """Developable quarter bend with two tangent adhesive lands in the XZ plane."""
    x, z = STRAP_CENTRE_X, STRAP_CENTRE_Z
    y = PORT_Y - STRAP_WIDTH / 2
    def point(ax, az):
        return cq.Vector(ax, y, az)
    def line(a, b):
        return cq.Edge.makeLine(point(*a), point(*b))
    def bend(radius, reverse=False):
        start, end = point(x-radius, z), point(x, z-radius)
        centre = point(x-radius/sqrt(2), z-radius/sqrt(2))
        if reverse:
            start, end = end, start
        return cq.Edge.makeThreePointArc(start, centre, end)

    ro, ri = outer_radius, inner_radius
    edges = [line((x-ro, STRAP_END_Z), (x-ro, z)), bend(ro),
             line((x, z-ro), (STRAP_END_X, z-ro)),
             line((STRAP_END_X, z-ro), (STRAP_END_X, z-ri)),
             line((STRAP_END_X, z-ri), (x, z-ri)), bend(ri, reverse=True),
             line((x-ri, z), (x-ri, STRAP_END_Z)),
             line((x-ri, STRAP_END_Z), (x-ro, STRAP_END_Z))]
    section = cq.Wire.assembleEdges(edges)
    return cq.Solid.extrudeLinear(section, [], cq.Vector(0, STRAP_WIDTH, 0))


def references():
    middle = STRAP_OUTER_BEND_R - PSA_THICKNESS
    return {
        'USB_black_PET_mask': _annulus(SKIRT, OPENING, MASK_FRONT_X, FILM_THICKNESS),
        'USB_black_PSA_lip_seal': _annulus(RING_OUTER, RING_INNER, MASK_BACK_X, PSA_THICKNESS),
        'USB_black_PET_side_guards': _side_guards(),
        'USB_black_PET_anchor': _anchor_layer(middle, middle - STRAP_THICKNESS),
        'USB_black_PSA_anchor': _anchor_layer(STRAP_OUTER_BEND_R, middle),
    }


def anchor_flat_length():
    """Developed length at the PET midplane, which controls the flat cut size."""
    neutral_radius = STRAP_OUTER_BEND_R - PSA_THICKNESS - STRAP_THICKNESS / 2
    return STRAP_END_Z - STRAP_CENTRE_Z + pi*neutral_radius/2 + STRAP_END_X - STRAP_CENTRE_X


def drawings(directory):
    """Write 1:1 planar DXFs in millimetres; the origin is the cut-part centre."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    width = STRAP_WIDTH / 2
    length = anchor_flat_length() / 2
    anchor = cq.Wire.makePolygon([(-width, -length, 0), (width, -length, 0),
                                  (width, length, 0), (-width, length, 0)], close=True)
    patterns = {
        'USB-mask-Toray-X30-125um.dxf': [_rounded(*SKIRT), _rounded(*OPENING)],
        'USB-lip-seal-tesa-68822-50um.dxf': [_rounded(*RING_OUTER), _rounded(*RING_INNER)],
        'USB-mask-side-guards-Toray-X30-50um.dxf': _guard_outlines(),
        'USB-anchor-X30-50um-plus-tesa-50um.dxf': [anchor],
    }
    for filename, outlines in patterns.items():
        sketch = cq.Workplane('XY').add(cq.Compound.makeCompound(outlines))
        cq.exporters.export(sketch, str(directory / filename))
