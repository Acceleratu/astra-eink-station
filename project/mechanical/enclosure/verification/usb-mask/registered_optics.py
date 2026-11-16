"""Project the measured PET exit window past a bounded USB pocket to the metal face.

This sufficient enclosure test covers every direct ray and assigns zero opacity
and zero structural shadow to the pressure-sensitive tapes. All lengths are mm.
"""
import math
import json
from pathlib import Path

from shapely import affinity
from shapely.geometry import Point
from shapely.ops import unary_union

# The reopened front wall has this 17.120 × 10.215 section at board X = -8.75.
# Dimensions below are relative to the measured GCT admission centroid.
DATUMS=json.loads(Path(__file__).with_name('projection-datums.json').read_text())
half_width=DATUMS['BRep_section']['width_mm']/2
CHEEK_Y = (-half_width,half_width)
CHEEK_Z = (DATUMS['cheek_bottom_relative_to_GCT_axis_mm'],DATUMS['cheek_top_relative_to_GCT_axis_mm'])
EDGE_ALLOWANCE = DATUMS['max_outward_print_error_each_axis_mm']
REGISTRATION_LIMIT = DATUMS['max_rigid_to_GCT_axis_error_each_axis_mm']
MIN_METAL_TO_CHEEK_MM = DATUMS['minimum_cheek_to_metal_axial_mm']
REQUIRED_LAND_MM = DATUMS['minimum_directional_land_after_uncertainty_mm']


def projected_profile(profile, bore_center, gap):
    # The actual gap supplied on the traveler is an upper interval bound. L is
    # from the cheek to the PET rear face, hence L >= 8.40 - gap. This models
    # cheek/board axial variation separately from the film-to-metal distance.
    length = MIN_METAL_TO_CHEEK_MM-gap
    if not 0 < gap < MIN_METAL_TO_CHEEK_MM:
        raise ValueError('The measured axial gap must be positive and less than the cheek-to-metal span.')
    ratio = gap/length
    cx, cy = bore_center.x, bore_center.y
    profile = affinity.translate(profile.convex_hull, -cx, -cy)
    profile = affinity.scale(profile, xfact=1+ratio, yfact=1+ratio, origin=(0,0))
    margin = EDGE_ALLOWANCE+REGISTRATION_LIMIT
    bounds_y = (CHEEK_Y[0]-margin, CHEEK_Y[1]+margin)
    bounds_z = (CHEEK_Z[0]-margin, CHEEK_Z[1]+margin)
    # A ray through cheek point s and rear-window point p reaches metal at
    # (1+g/L)*p - (g/L)*s. The four corners enclose the entire rounded cheek.
    ends = [affinity.translate(profile, cx-ratio*y, cy-ratio*z)
            for y in bounds_y for z in bounds_z]
    return unary_union(ends).convex_hull, ratio


def distance_to_metal(metal, envelope):
    if metal.covers(envelope):
        return metal.boundary.distance(envelope.boundary)
    # For a nonconvex measured contour, a witnessed protrusion is sufficient to
    # fail; an incompletely sampled indentation never converts a fail to a pass.
    crossed = max(metal.distance(Point(x,y)) for x,y in envelope.exterior.coords)
    return -max(crossed, 1e-15)


def verify_optics(specimen, shapes, uncertainty):
    gap=specimen.get('pet_back_to_steel_upper_mm')
    fit=specimen.get('pocket_within_projection_bounds')
    if specimen.get('case_step_sha256')!=DATUMS['case_step_sha256']:
        return {'status':'missing or mismatched housing revision', 'pass':False,
                'required_case_step_sha256':DATUMS['case_step_sha256']}
    if gap is None or fit is not True:
        return {'status':'missing axial-gap measurement or pocket gauge', 'pass':False,
                'required_input':['pet_back_to_steel_upper_mm','pocket_within_projection_bounds']}
    if not math.isfinite(gap):
        raise ValueError('Record a finite upper bound for the PET back to steel axial distance.')
    metal=shapes['metal_outer']
    envelope, ratio=projected_profile(shapes['pet_hole'],shapes['metal_bore'].centroid,gap)
    nominal=distance_to_metal(metal,envelope)
    lower=nominal-(1+ratio)*uncertainty
    result={'status':'measured outlines and bounded pocket', 'pass':lower>=REQUIRED_LAND_MM,
            'required_after_uncertainty_mm':REQUIRED_LAND_MM,
            'pet_back_to_steel_upper_mm':gap, 'magnification_of_PAIR_uncertainty':1+ratio,
            'nominal_minimum_projected_land_mm':nominal,'minimum_land_after_uncertainty_mm':lower,
            'minimum_cheek_to_steel_mm':MIN_METAL_TO_CHEEK_MM,
            'max_cheek_edge_outwards_per_axis_mm':EDGE_ALLOWANCE,
            'max_board_to_pocket_centre_per_axis_mm':REGISTRATION_LIMIT,
            'case_step_sha256':DATUMS['case_step_sha256'],
            'usb_pocket_source_sha256':DATUMS['usb_pocket_source_sha256'],
            'credits_black_adhesive':False}
    # Optional diagnostic for a lot with a physically measured metal-side clear
    # layer. It never substitutes for the zero-credit release gate.
    skin=specimen.get('deepest_opaque_carrier_to_steel_upper_mm')
    if skin is not None:
        if not math.isfinite(skin) or not 0 < skin <=gap:
            raise ValueError('The clear acrylic thickness bound must be positive and no larger than the whole step.')
        through_carrier, carrier_ratio=projected_profile(shapes['psa_hole'],shapes['metal_bore'].centroid,skin)
        both=envelope.intersection(through_carrier)
        result['optional_measured_black_carrier']={'clear_acrylic_plus_air_upper_mm':skin,
             'changes_zero_credit_release_result':False}
        if both.is_empty or both.geom_type!='Polygon':
            result['optional_measured_black_carrier']['status']='No common projected aperture; inspect the invalid mutual registration.'
        else:
            with_tape=distance_to_metal(metal,both)-(1+max(ratio,carrier_ratio))*uncertainty
            result['optional_measured_black_carrier'].update(projected_land_after_uncertainty_mm=with_tape,
                                                            meets_same_land_threshold=with_tape>=REQUIRED_LAND_MM)
    return result
