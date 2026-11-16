"""Verify the actual USB front optical stack, cut drawings, and installed service path.

Run with CadQuery 2.6, ezdxf and numpy. The default consumes the released STEP.
Use --design for the component model before its top-level export.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import cadquery as cq
import ezdxf
from OCP.Bnd import Bnd_Box
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.BRepBndLib import BRepBndLib
from OCP.gp import gp_Dir, gp_Pln, gp_Pnt

HERE = Path(__file__).resolve().parent
ENCLOSURE = HERE.parents[1]
ROOT = ENCLOSURE.parents[1]
sys.path.insert(0, str(ENCLOSURE))
import usb_mask
import usb_pocket

GCT = ROOT / 'hardware/models/GCT_USB4135-GF-A.step'
MAIN = 'USB_black_PET_mask'
GLUE = 'USB_black_PSA_lip_seal'
CAPS = 'USB_black_PET_side_guards'
BRACE = 'USB_black_PET_anchor'
BRACE_GLUE = 'USB_black_PSA_anchor'
NAMES = (MAIN, GLUE, CAPS, BRACE, BRACE_GLUE)
BORE = (8.34, 2.56, .95)
METAL = (8.94, 3.16, 1.25)


def sha(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def rounded_area(w, h, r):
    return w*h - (4-math.pi)*r*r


def bounds(shape):
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped, box, False, False)
    return tuple(box.Get())


def cuboid(b):
    return cq.Solid.makeBox(b[3]-b[0], b[4]-b[1], b[5]-b[2], b[:3])


def positive(a, b):
    return max(0., a.intersect(b).Volume())


def box_spacing(a, b):
    return math.sqrt(sum(max(0., a[i]-b[i+3], b[i]-a[i+3])**2 for i in range(3)))


def compound(shapes):
    if len(shapes) == 1:
        return shapes[0]
    return cq.Compound.makeCompound(shapes)


def load_assembly(path):
    groups = {}
    for shape, path_name, placement, _ in cq.Assembly.importStep(str(path)):
        elements = path_name.split('/')
        group = (f"PCB:{elements[elements.index('Populated_PCB')+1]}"
                 if 'Populated_PCB' in elements else elements[1])
        groups.setdefault(group, []).append(shape.moved(placement))
    return {key: compound(items) for key, items in groups.items()}


def design_stage():
    connector = cq.importers.importStep(str(GCT)).val()
    connector = connector.rotate((0, 0, 0), (0, 0, 1), 270).translate((3.45, 67., .045))
    pieces = usb_mask.references()
    wall = usb_pocket.front_additions()[0]
    for cut in usb_pocket.front_cuts():
        wall = wall.cut(cut)
    return dict(pieces, **{'PCB:J101': connector, 'Front_shell': wall})


def dxf_receipt():
    expected = {
        'USB-mask-Toray-X30-125um.dxf': [(15., 7.4), (8.68, 2.90)],
        'USB-lip-seal-tesa-68822-50um.dxf': [(11.20, 3.20), (8.74, 2.96)],
        'USB-mask-side-guards-Toray-X30-50um.dxf': [],
        'USB-anchor-X30-50um-plus-tesa-50um.dxf': [(6., 4.0765928797)],
    }
    receipts = {}
    for name, want in expected.items():
        path = ENCLOSURE / 'templates' / name
        doc = ezdxf.readfile(path)
        wires = cq.importers.importDXF(str(path)).wires().vals()
        assert all(w.isValid() and w.IsClosed() for w in wires)
        sizes = []
        for wire in wires:
            x0, y0, _, x1, y1, _ = bounds(wire)
            sizes.append((x1-x0, y1-y0))
        sizes.sort(reverse=True)
        areas = sorted([cq.Face.makeFromWires(w).Area() for w in wires], reverse=True)
        assert doc.units == 4
        if want:
            assert len(want) == len(sizes)
            for actual, wanted in zip(sizes, want):
                assert all(abs(a-b) < .0001 for a, b in zip(actual, wanted))
        else:
            assert len(sizes) == 2 and abs(areas[0]-areas[1]) < .00001
            assert 3.0 < areas[0] < 3.2
        receipts[name] = dict(sha256=sha(path), insunits=doc.units,
                              closed_loops_mm=sizes, individual_loop_areas_mm2=areas)
    return receipts


def optical_projection(wall_margin, relative_yz, gap, axial_length, cut_tolerance):
    rear = (9.70/2+wall_margin, 3.90/2+wall_margin)
    mouth = (24.30/2+wall_margin, 13.30/2+wall_margin)
    slopes = [(a+b)/axial_length for a, b in zip(mouth, rear)]
    required = [a + relative_yz + gap*s for a, s in zip(rear, slopes)]
    skirt_half = [15/2-cut_tolerance, 7.40/2-cut_tolerance]
    # The entire projected rectangle lies between the two side skirt fillet tangencies.
    assert required[0] < skirt_half[0]-.80
    return dict(max_slope_yz=slopes, outside_projection_half_yz_mm=required,
                skirt_overlap_half_yz_mm=[s-r for s, r in zip(skirt_half, required)],
                assumed_rigid_dimensions_per_side_mm=wall_margin,
                max_relative_center_shift_per_axis_mm=relative_yz, rear_wall_to_skirt_mm=gap,
                min_outer_to_inner_aperture_distance_mm=axial_length,
                minimum_skirt_perimeter_tolerance_mm=cut_tolerance)


def normal_support(profile, angle):
    width, height, radius = profile
    c, s = abs(math.cos(angle)), abs(math.sin(angle))
    return (width/2-radius)*c + (height/2-radius)*s + radius


def wall_sections(parts):
    wall = parts['Front_shell']
    openings = {}
    stations = [(-9.9999, 24.30, 13.30, 1.725), (-8.75, 17.12, 10.215, .7125),
                (-6.40, 16.83, 9.59, 1.065), (-.3501, 9.70, 3.90, 1.725)]
    for x, width, height, centre_z in stations:
        section = BRepAlgoAPI_Section(wall.wrapped, gp_Pln(gp_Pnt(x, 67., 1.725), gp_Dir(1, 0, 0)), False)
        section.Build()
        wires = cq.Wire.combine(cq.Shape.cast(section.Shape()).Edges(), tol=1e-5)
        matched = []
        for wire in wires:
            _, y0, z0, _, y1, z1 = bounds(wire)
            if (wire.IsClosed() and abs((y0+y1)/2-67.) < .001 and abs((z0+z1)/2-centre_z) < .001
                    and abs(y1-y0-width) < .002 and abs(z1-z0-height) < .002):
                matched.append(dict(width_mm=y1-y0, height_mm=z1-z0, centre_yz_mm=[(y0+y1)/2, (z0+z1)/2]))
        assert len(matched) == 1, (x, matched)
        openings[str(x)] = matched[0]
    # A real inclined line clears the complete wall and crosses the installed skirt.
    # A film cut off at the throat's height would leave this same line unobstructed.
    def ray_z(x):
        return 1.725-6.10+(x+10)*8.0/9.65
    witness = cq.Edge.makeLine((-10.001, 67., ray_z(-10.001)), (.10, 67., ray_z(.10)))
    wall_intersection = sum(edge.Length() for edge in witness.intersect(wall).Edges())
    mask_intersection = sum(edge.Length() for edge in witness.intersect(parts[MAIN]).Edges())
    assert wall_intersection < 1e-6 and mask_intersection > .125 and ray_z(-.1775) > 1.725+3.90/2
    return dict(sections_at_x_mm=openings, negative_control_ray_points_mm=[[-10.001,67.,ray_z(-10.001)],
                [.10,67.,ray_z(.10)]], ray_length_in_wall_mm=wall_intersection,
                ray_length_in_real_skirt_mm=mask_intersection,
                ray_exceeds_hypothetical_short_skirt_edge_mm=ray_z(-.1775)-(1.725+3.90/2))


def old_peripheral_rays(wall):
    path = HERE/'peripheral-witnesses.json'
    record = json.loads(path.read_text())
    assert record['first_visible_old_part']=='PCB_1mm' and len(record['segments'])==41
    # This box clips the actual housing around the USB tunnel. Every old line
    # crosses the whole X length of the box on its way to the exposed board.
    local = wall.intersect(cuboid((-10.04, 50., -7., -.34, 84., 12.)))
    lengths = []
    for segment in record['segments']:
        ray = cq.Edge.makeLine(segment['from'], segment['to'])
        thickness = sum(edge.Length() for edge in ray.intersect(local).Edges())
        lengths.append(thickness)
    assert min(lengths) > .001, lengths
    return dict(old_step_sha256=record['old_case_sha256'], witness_file_sha256=sha(path),
                previously_visible_board_rays=len(lengths), now_blocked_by_front_wall=len(lengths),
                min_solid_PETG_path_mm=min(lengths), max_solid_PETG_path_mm=max(lengths),
                min_thickness_ray_1based=lengths.index(min(lengths))+1,
                solid_PETG_path_each_ray_mm=lengths)


def section_receipt(parts):
    connector = parts['PCB:J101']
    metal_faces = []
    for face in connector.Faces():
        b = bounds(face)
        if abs(b[0]+.0025) < 1e-5 and abs(b[3]+.0025) < 1e-5:
            metal_faces.append(face)
    measured_face_area = sum(face.Area() for face in metal_faces)
    expected_face_area = rounded_area(*METAL)-rounded_area(*BORE)
    assert len(metal_faces) == 2 and abs(measured_face_area-expected_face_area) < 1e-5
    # Sample the steel 5 µm inboard of its front, using the actual released adhesive
    # face translated into the metal. It measures true support after the independent export.
    glue = parts[GLUE]
    sections = [f for f in glue.Faces() if abs(bounds(f)[0]+.0025) < 1e-5
                and abs(bounds(f)[3]+.0025) < 1e-5]
    assert len(sections) == 1
    face = sections[0]
    slab = cq.Solid.extrudeLinear(face.outerWire(), face.innerWires(), (.005, 0, 0))
    bonded = positive(slab, connector)/.005
    expected_bond = rounded_area(*METAL)-rounded_area(8.74, 2.96, 1.11)
    assert abs(bonded-expected_bond) < .0001
    top = cuboid((.3275, 64., 3.300, 2.50, 70., 3.305))
    top_bonded = positive(top, connector)/.005
    assert abs(top_bonded-13.035) < .0001
    assert abs(parts[CAPS].distance(connector)-.15) < .0001
    # The nominal front/side-contour support bound over EVERY normal depends only
    # on |cos(t)|+|sin(t)| in [1,sqrt(2)]. Its extrema occur at 0 and 45 degrees.
    angles = (0., math.pi/4)
    cut = (8.68, 2.90, 1.08)
    inner = (8.74, 2.96, 1.11)
    gap = min(normal_support(cut, a) - normal_support(BORE, a)
              - .05 - .03 - .05*(math.cos(a)+math.sin(a)) for a in angles)
    dynamic = gap - .175*math.tan(math.radians(5))
    steel_under_adhesive = min(normal_support(METAL, a)-normal_support(inner, a) for a in angles)
    min_psa_setback = min(normal_support(inner, a)-normal_support(cut, a) for a in angles)
    assert dynamic > .020 and steel_under_adhesive > .083 and min_psa_setback > .02999
    contact_pairs = [(MAIN, GLUE), (MAIN, BRACE_GLUE), (GLUE, CAPS), (BRACE, BRACE_GLUE)]
    interface_gaps = {f'{a}/{b}': parts[a].distance(parts[b]) for a, b in contact_pairs}
    assert max(interface_gaps.values()) < .00001
    return dict(front_metal_planar_faces=len(metal_faces), front_metal_area_mm2=measured_face_area,
                complete_adhesive_face_area_mm2=face.Area(), adhesive_on_steel_mm2=bonded,
                min_nominal_adhesive_on_steel_normal_band_mm=steel_under_adhesive,
                min_nominal_PSA_setback_from_PET_mm=min_psa_setback,
                steel_top_anchor_bond_area_mm2=top_bonded, skirt_back_anchor_area_mm2=6*(5.11-3.685),
                steel_side_guard_spacing_mm=parts[CAPS].distance(connector), modeled_bond_gaps_mm=interface_gaps,
                independent_Y_Z_center_tolerance_mm=.05, PET_inward_profile_tolerance_mm=.05,
                full_3D_metal_admission_radial_growth_assumption_mm=.03,
                min_entire_admission_profile_clearance_mm=gap,
                min_clearance_with_5deg_straight_axis_tilt_mm=dynamic,
                physical_acceptance={'PET_offset_radial_target_mm':.035,
                                     'minimum_observed_PET_bore_border_mm':.025,
                                     'minimum_prebond_registered_continuous_metal_PSA_bearing_mm':.035,
                                     'min_measured_PSA_setback_from_PET_mm':.010,
                                     'actual_part_metal_corner_gauge_required':True})


def assembly_check(parts):
    all_boxes = {k:bounds(p) for k, p in parts.items()}
    colliding = {}
    for index, name in enumerate(NAMES):
        part = parts[name]
        assert part.isValid() and len(part.Solids()) == (2 if name == CAPS else 1)
        for other, target in parts.items():
            if other == name or other in NAMES[:index] or box_spacing(all_boxes[name], all_boxes[other]) > 1e-6:
                continue
            volume = positive(part, target)
            if volume > 1e-5:
                colliding[name+'/'+other] = volume
    # Envelope extended by 20 mm contains every material point throughout the lift.
    obstacles = {k:v for k,v in parts.items() if k in {'Front_shell', 'Upper_PCB_rail', 'Lower_PCB_rail'}
                 or k.startswith(('Rail_screw','Rail_insert','PCB_nut','Display_insert','Case_insert'))}
    travel = {}
    for name in NAMES:
        b = list(all_boxes[name]); b[5] += 20.
        swept = cuboid(b)
        best, hit = 1e6, None
        for key in sorted(obstacles, key=lambda k:box_spacing(b, all_boxes[k])):
            if box_spacing(b, all_boxes[key]) > best:
                break
            distance = swept.distance(obstacles[key])
            if distance < best:
                best, hit = distance, key
        travel[name] = dict(min_distance_mm=best, nearest=hit)
    board = parts.get('PCB:PCB_1mm')
    to_board = None if board is None else parts[MAIN].distance(board)
    if to_board is not None:
        assert .05 < to_board < .055
    return {'all_positive_overlaps_mm3':colliding, 'conservative_20mm_lift_to_fixed_case':travel,
            'minimum_installed_skirt_to_FR4_edge_mm':to_board,
            'minimum_installed_mask_to_front_wall_mm':parts[MAIN].distance(parts['Front_shell']),
            'part_volumes_mm3':{n:parts[n].Volume() for n in NAMES},
            'part_bounding_boxes_mm':{n:all_boxes[n] for n in NAMES}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--design', action='store_true')
    parser.add_argument('--assembly', type=Path, default=ENCLOSURE/'cad/Astra-enclosure-assembly.step')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    parts = design_stage() if args.design else load_assembly(args.assembly)
    nominal = optical_projection(0., 0., .1725, 9.65, 0.)
    tolerance = optical_projection(.25, .35, .40, 9.35, .05)
    assert min(tolerance['skirt_overlap_half_yz_mm']) > .70
    assert (3.90/2 - nominal['outside_projection_half_yz_mm'][1]) < 0
    result = dict(stage=('component design and pocket wall' if args.design else 'reopened released assembly'),
                  step_sha256=None if args.design else sha(args.assembly),
                  native_GCT_step_sha256=sha(GCT), module_sha256=sha(ENCLOSURE/'usb_mask.py'),
                  pocket_source_sha256=sha(ENCLOSURE/'usb_pocket.py'), checker_sha256=sha(Path(__file__)),
                  drawings=dxf_receipt(), section=section_receipt(parts),
                  complete_external_sightline_bound={'nominal':nominal,'tolerance_extrema':tolerance,
                                                    'actual_wall_sections_and_control':wall_sections(parts),
                                                    'recheck_of_previously_open_board_rays':old_peripheral_rays(parts['Front_shell'])},
                  installed=assembly_check(parts), physical_qualification_executed=False)
    checks = result['installed']
    pass_checks = (not checks['all_positive_overlaps_mm3'] and
                   min(row['min_distance_mm'] for row in checks['conservative_20mm_lift_to_fixed_case'].values()) > 0.)
    result['digital_checks_pass'] = pass_checks
    output = args.output or (HERE/'results.json' if not args.design else None)
    if output:
        output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'stage':result['stage'],'case_sha256':result['step_sha256'], 'geometry':checks,
                      'bond_area_mm2':result['section']['adhesive_on_steel_mm2'], 'passed':pass_checks}, indent=2))
    if not pass_checks:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
