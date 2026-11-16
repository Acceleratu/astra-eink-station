"""One-piece gravity cradle for the Astra portrait case, in millimetres.

print_shape() uses print-world +X right, +Y away from the viewer, +Z up.
assembled_shape() returns the same solid in the released PCB coordinate frame.
Run this file with CadQuery 2.6.1 to write a print STL, both STEP poses and the
installed transform. The independent checks are in verification/stand/check_stand.py.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
from pathlib import Path

import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / "verification" / "stand"
ANGLE = 12.0
RAD = math.radians(ANGLE)
S, C = math.sin(RAD), math.cos(RAD)
CASE_CENTER_X = 57.0
CASE_BOTTOM_Y = 96.0
CASE_TOP_Y = -100.0
CASE_FRONT_Z = -9.0
CASE_REAR_Z = 15.0
CASE_WIDTH = 134.0
THICKNESS = CASE_REAR_Z - CASE_FRONT_Z
REAR_SEAT_HEIGHT = 9.0
FRONT_SEAT_HEIGHT = REAR_SEAT_HEIGHT + THICKNESS * S
BASE_THICKNESS = 5.5
SOLE_HALF_WIDTH = 72.0
SOLE_FRONT = -38.0
SOLE_BACK = 86.0
SHOES = ((6.0, 20.0), (88.0, 100.0))
FRONT_CLEARANCE = 1.05
SIDE_CLEARANCE = .70
FRONT_ENGAGEMENT = 5.5
REAR_HEIGHT = 86.0


def yz_at(u: float, v: float) -> tuple[float, float]:
    """Depth/height on desk from rearwards u and upwards v measured from front-bottom."""
    return u*C + v*S, FRONT_SEAT_HEIGHT - u*S + v*C


def to_print_point(x: float, y: float, z: float) -> tuple[float, float, float]:
    depth, height = yz_at(z-CASE_FRONT_Z, CASE_BOTTOM_Y-y)
    return x-CASE_CENTER_X, depth, height


def to_pcb_point(x: float, y: float, z: float) -> tuple[float, float, float]:
    h = z - FRONT_SEAT_HEIGHT
    u, v = y*C-h*S, y*S+h*C
    return x+CASE_CENTER_X, CASE_BOTTOM_Y-v, u+CASE_FRONT_Z


def pcb_to_print_location() -> cq.Location:
    return cq.Location(cq.Vector(*to_print_point(0, 0, 0)), cq.Vector(1, 0, 0), -90-ANGLE)


def pcb_to_print_matrix() -> list[list[float]]:
    tx, ty, tz = to_print_point(0, 0, 0)
    return [[1, 0, 0, tx], [0, -S, C, ty], [0, -C, -S, tz], [0, 0, 0, 1]]


def _yz_prism(x_start, x_end, profile):
    return (cq.Workplane("YZ", origin=(x_start, 0, 0)).polyline(profile)
            .close().extrude(x_end - x_start).val())


def _sole():
    # The U remains open to the room below the lower-edge sensor inlet. A single
    # rear cross-member joins the feet; all bed-contact faces are coplanar.
    points = [(-SOLE_HALF_WIDTH, SOLE_FRONT), (-35, SOLE_FRONT), (-35, 58),
              (30, 58), (30, SOLE_FRONT), (SOLE_HALF_WIDTH, SOLE_FRONT),
              (SOLE_HALF_WIDTH, SOLE_BACK), (-SOLE_HALF_WIDTH, SOLE_BACK)]
    return (cq.Workplane("XY").polyline(points).close().extrude(BASE_THICKNESS)
            .edges("|Z").fillet(6).faces(">Z").edges().fillet(1).val())


def _shoe(x0, x1):
    t = THICKNESS
    # Front contact has room for tolerance. A recess at the rear-bottom corner
    # prevents an unchamfered shell from bearing on the slicer's inside radius.
    uv = [(-4.5, 2.3), (-4.5, 4.2), (-3.5, FRONT_ENGAGEMENT),
          (-2.1, FRONT_ENGAGEMENT), (-FRONT_CLEARANCE, 4.2),
          (-FRONT_CLEARANCE, 0), (t-.65, 0), (t+.55, -.55),
          (t+.65, -.55), (t+.65, 1.15), (t, 1.9),
          (t, REAR_HEIGHT-1.6), (t+1.35, REAR_HEIGHT),
          (t+3.4, REAR_HEIGHT), (t+4.7, REAR_HEIGHT-1)]
    profile = [(-21, BASE_THICKNESS-.40)] + [yz_at(u,v) for u,v in uv]
    profile.append((64, BASE_THICKNESS-.40))
    return _yz_prism(x0-CASE_CENTER_X, x1-CASE_CENTER_X, profile)


def _side_guide(right):
    # Separate short ears limit left/right slip, while the two bearing shoes
    # support the bottom edge. Contact starts above the 7 mm case corner radius.
    half = CASE_WIDTH/2 + SIDE_CLEARANCE
    xmin,xmax = (half,half+3.1) if right else (-half-3.1,-half)
    profile = [(3.2, BASE_THICKNESS-.40), yz_at(3.0, 7.8),
               yz_at(5.3, 10.4), yz_at(17.0, 10.4),
               yz_at(20.0, 7.8), (24.0, BASE_THICKNESS-.40)]
    ear = _yz_prism(xmin, xmax, profile)
    # Chamfer the complete inner rim, including the approach above the datum,
    # without reducing the straight bearing thickness at the center of the ear.
    inner = "<X" if right else ">X"
    return cq.Workplane(obj=ear).faces(inner).edges().chamfer(.8).val()


@lru_cache(maxsize=1)
def print_shape() -> cq.Shape:
    solids = [_shoe(*span) for span in SHOES] + [_side_guide(False), _side_guide(True)]
    result = _sole().fuse(*solids).clean()
    if not result.isValid() or len(result.Solids()) != 1:
        raise RuntimeError("The cradle must be one valid solid")
    return result.Solids()[0]


def assembled_shape() -> cq.Shape:
    return print_shape().moved(pcb_to_print_location().inverse)


def export(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    shape = print_shape()
    cq.exporters.export(shape, str(directory/"stand-print.step"))
    cq.exporters.export(shape, str(directory/"stand-print.stl"), tolerance=.035, angularTolerance=.12)
    cq.exporters.export(assembled_shape(), str(directory/"stand-pcb.step"))
    cq.exporters.export(assembled_shape(), str(directory/"stand-pcb.stl"), tolerance=.035, angularTolerance=.12)
    bb = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped,bb,False,False)
    record = {"units":"mm","angle_back_degrees":ANGLE,
              "frame":"print +X right, +Y back, +Z up; PCB +Y down, -Z toward viewer",
              "pcb_to_print_matrix":pcb_to_print_matrix(),
              "print_to_pcb_matrix":[[1,0,0,CASE_CENTER_X],
                                     [0,-S,-C,CASE_BOTTOM_Y+FRONT_SEAT_HEIGHT*C],
                                     [0,C,-S,CASE_FRONT_Z+FRONT_SEAT_HEIGHT*S],
                                     [0,0,0,1]],
              "print_aabb":list(bb.Get()),
              "case_bounds_pcb":[-10,CASE_TOP_Y,CASE_FRONT_Z,124,CASE_BOTTOM_Y,CASE_REAR_Z],
              "seat_ranges_pcb_x_mm":SHOES,
              "nominal_thickness_fit_mm":THICKNESS+FRONT_CLEARANCE,
              "lateral_guide_inside_dimension_mm":CASE_WIDTH+2*SIDE_CLEARANCE,
              "front_engagement_mm":FRONT_ENGAGEMENT, "rear_height_mm":REAR_HEIGHT,
              "rear_bottom_case_world_height_mm":REAR_SEAT_HEIGHT}
    (directory/"transforms.json").write_text(json.dumps(record,indent=2)+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=EVIDENCE)
    args = parser.parse_args()
    export(args.out)
