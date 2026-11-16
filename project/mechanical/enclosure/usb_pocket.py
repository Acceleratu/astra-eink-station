"""Closed side pocket for the GCT USB4135, in the populated board's mm datum.

The pale front owns the whole pocket and the raised side panel. The lid opens
in +Z behind it. Its joint has a separate overlapping inner tongue. The last
rigid cut clears the board/printing tolerance; the registered optical mask
behind it closes the clearance around the stainless receptacle.
"""
from functools import lru_cache

import cadquery as cq


Y, Z = 67.000, 1.725
LAND_FACE, SHOULDER_FACE, LAND_BACK = -1.20, -1.08, -.35


def profile(x, width, height, radius, centre_z=Z):
    points = [(x, Y + y*width/2, centre_z + z*height/2)
              for y, z in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    wire = cq.Wire.makePolygon(points, close=True)
    return wire.fillet2D(radius, wire.Vertices())


def pocket_loft(stations):
    return cq.Solid.makeLoft([profile(*s) for s in stations], ruled=True)


def side_panel(x0, x1, base, top, bottom_left, top_left, radius):
    # The upper trapezoid moves the two-colour joint clear of the cable entry.
    yz = ((bottom_left, base), (top_left, top),
          (2*Y-top_left, top), (2*Y-bottom_left, base))
    wire = cq.Wire.makePolygon([(x0, y, z) for y, z in yz], close=True)
    wire = wire.fillet2D(radius, wire.Vertices())
    return cq.Solid.extrudeLinear(wire, [], (x1-x0, 0, 0))


@lru_cache(maxsize=1)
def front_additions():
    wall = pocket_loft([
        (-10.00, 27.80, 16.80, 5.50), (-8.00, 25.30, 15.20, 4.70),
        (-4.00, 21.10, 12.75, 3.55), (-2.50, 20.00, 12.20, 3.20),
        (LAND_FACE, 18.90, 11.90, 2.85), (LAND_BACK, 17.50, 10.50, 2.40)])
    raised = side_panel(-10.00, -6.35, 5.12, 11.48, 49.22, 55.60, .85)
    # A free-standing inner overlap shields the assembly gap. Its top clears
    # the closed lid roof by 0.45 mm and its outer face clears the lid side.
    overlap = side_panel(-7.16, -5.82, 3.32, 12.15, 46.30, 54.10, .70)
    # Close the underside of the inner tongue against the lower shell wall.
    # A grazing ray can otherwise round the bottom corner of the stepped seam.
    # Draft the underside from the existing sidewall so that the outer ends
    # of the shelf do not need a support tower beside the case screw post.
    shelf_section = cq.Wire.makePolygon([(x,46.45,z) for x,z in
        ((-7.76,1.32),(-7.54,1.32),(-5.76,3.40),(-5.76,4.50),(-7.76,4.50))],close=True)
    shelf = cq.Solid.extrudeLinear(shelf_section,[],(0,41.1,0))
    # Build the enclosed underside directly onto the front skin. This removes
    # the shallow blind support pocket below the well before PCB installation.
    foot_wire = cq.Wire.makePolygon([(-7.86,58.80,-6.74),(-1.62,58.80,-6.74),
                                     (-1.62,75.16,-6.74),(-7.86,75.16,-6.74)],close=True)
    foot_wire = foot_wire.fillet2D(.60,foot_wire.Vertices())
    foot = cq.Solid.extrudeLinear(foot_wire,[],(0,0,4.15))
    return wall, raised, overlap, foot, shelf


@lru_cache(maxsize=1)
def front_cuts():
    # Keep the rim open for locating the plug by feel, then curve the cheeks
    # inward. The throat screens the strips of PCB on either side of J101
    # from grazing exterior views. The roof screens its four shield feet.
    # Each entry describes X, width, floor Z, ceiling Z and corner radius.
    stations = [(-10.10,24.30,-4.925,8.375,4.05),(-10.,24.30,-4.925,8.375,4.05),
                (-9.75,22.72,-4.765,7.87,3.40),(-9.38,19.42,-4.560,6.66,2.55),
                (-9.06,17.58,-4.490,6.03,1.92),(-8.75,17.12,-4.395,5.82,1.82),
                (-8.45,17.06,-4.308,5.82,1.80),(-6.40,16.83,-3.730,5.86,1.73),
                (-2.35,16.12,-2.655,6.05,1.60),(-1.42,15.40,-2.420,5.87,1.31),
                (LAND_FACE,15.32,-2.385,5.835,1.22)]
    well = cq.Solid.makeLoft([profile(x,w,hi-lo,r,(hi+lo)/2) for x,w,lo,hi,r in stations],ruled=True)
    # The full 13 x 7 mm overmould enters this shallow rebate even at the
    # offset corners. The small-radius corners clear a rectangular overmould.
    shoulder = pocket_loft([
        (LAND_FACE-.03, 14.30, 8.04, .63), (LAND_FACE, 14.30, 8.04, .63),
        (SHOULDER_FACE, 14.08, 7.86, .52)])
    mouth = pocket_loft([
        (SHOULDER_FACE-.02, 10.10, 4.30, 1.65), (SHOULDER_FACE, 10.10, 4.30, 1.65),
        (SHOULDER_FACE+.20, 9.70, 3.90, 1.45), (LAND_BACK+.05, 9.70, 3.90, 1.45)])
    return well, shoulder, mouth


@lru_cache(maxsize=1)
def lid_cut():
    # A printed fit gap follows only the local panel. No lid seam crosses the
    # cable recess, either in front of or behind the metal mouth.
    return side_panel(-10.15, -7.52, 4.86, 11.90, 48.37, 55.43, .85)
