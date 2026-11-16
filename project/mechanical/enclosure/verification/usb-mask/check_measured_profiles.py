"""Score five registered contours from a calibrated microscope, in millimetres.

For synthetic controls: python check_measured_profiles.py --self-test
For a real part: python check_measured_profiles.py specimen.json --output receipt.json
"""
import argparse
import json
import math
from pathlib import Path

from shapely import affinity
from shapely.geometry import Polygon, box

from registered_optics import DATUMS, verify_optics

PROFILES = ('metal_bore', 'metal_outer', 'pet_hole', 'psa_hole', 'psa_outer')


def margin(outer, inner):
    if outer.contains(inner):
        return outer.boundary.distance(inner.boundary)
    return 0.0


def check(specimen):
    uncertainty = float(specimen['expanded_pairwise_uncertainty_mm'])
    if not 0. < uncertainty <= .010:
        raise ValueError('Provide a calibrated pairwise expanded uncertainty from 0 to 0.010 mm.')
    polygons = {key: Polygon(specimen[key]) for key in PROFILES}
    if not all(p.is_valid and not p.is_empty and p.area > 0 for p in polygons.values()):
        raise ValueError('Each profile must be a valid enclosed area in the same mm reference frame.')
    bore, metal, film, adhesive_hole, adhesive_outer = (polygons[key] for key in PROFILES)
    contact_outer = metal.intersection(adhesive_outer)
    contact_inner = bore.union(adhesive_hole)
    readings = {'free_PET_border': margin(film, bore),
                'adhesive_setback_from_PET': margin(adhesive_hole, film),
                'circumferential_steel_adhesive_bearing': margin(contact_outer, contact_inner)}
    limits = {'free_PET_border':.025, 'adhesive_setback_from_PET':.010,
              'circumferential_steel_adhesive_bearing':.035}
    conservative = {key:value-uncertainty for key, value in readings.items()}
    centre_distance = bore.centroid.distance(film.centroid)
    passed = all(conservative[k] >= limits[k] for k in limits) and centre_distance+uncertainty <= .035
    optics = verify_optics(specimen, polygons, uncertainty)
    return {'serial':specimen['serial'], 'expanded_pairwise_uncertainty_mm':uncertainty,
            'measured_minimum_distances_mm':readings, 'lower_confidence_bounds_mm':conservative,
            'limits_mm':limits, 'radial_PET_to_bore_center_mm':centre_distance,
            'upper_confidence_radial_center_mm':centre_distance+uncertainty,
            'maximum_radial_center_mm':.035, 'geometry_pass':passed,
            'transparent_PSA_oblique_check':optics, 'release_pass':bool(passed and optics['pass'])}


def suggest_recenter(specimen):
    """Search the jig's YZ adjustments before press. Actual parts must be rescanned."""
    first = check(specimen)
    if first['release_pass']:
        return {'action':'Current measured position passes.', 'shift_yz_mm':[0.,0.]}
    if first['transparent_PSA_oblique_check']['status']=='missing or mismatched housing revision':
        return {'action':'Identify the qualified enclosure or qualify the different housing before using the projector.'}
    if first['transparent_PSA_oblique_check']['status'].startswith('missing'):
        return {'action':'Measure the axial gap and housing first.'}
    shapes = {k:Polygon(specimen[k]) for k in PROFILES}
    hole, window = shapes['metal_bore'].centroid, shapes['pet_hole'].centroid
    radius = .035-first['expanded_pairwise_uncertainty_mm']
    moves=[]
    for iy in range(-7,8):
        for iz in range(-7,8):
            target=(.005*iy,.005*iz)
            if math.hypot(*target) <= radius:
                dy=hole.x-window.x+target[0]
                dz=hole.y-window.y+target[1]
                moves.append((math.hypot(dy,dz),dy,dz))
    for _,dy,dz in sorted(moves):
        moved={**specimen}
        for k in ('pet_hole','psa_hole','psa_outer'):
            moved[k]=list(affinity.translate(shapes[k],dy,dz).exterior.coords)
        trial=check(moved)
        if trial['release_pass']:
            return {'action':'Move the registered PET/PSA assembly on the XY stage before pressing, then rescan all five contours.',
                    'shift_yz_mm':[dy,dz], 'target_grid_step_mm':.005,
                    'predicted_transparent_land_lower_mm':trial['transparent_PSA_oblique_check']['minimum_land_after_uncertainty_mm'],
                    'predicted_only':True}
    return {'action':'No passing pose on the 0.005 mm grid. Recut a fresh skirt to the inward process target within drawing tolerance, or try a different measured laminate; rescan all five contours.',
            'target_grid_step_mm':.005, 'recommended_inward_process_target_mm':.020,
            'approved_by_grid_search':False}


def synthetic(w, h, r):
    return box(-w/2+r,-h/2+r,w/2-r,h/2-r).buffer(r, quad_segs=128)


def test():
    geometry = dict(metal_bore=synthetic(8.34,2.56,.95), metal_outer=synthetic(8.94,3.16,1.25),
                    pet_hole=synthetic(8.68,2.90,1.08), psa_hole=synthetic(8.74,2.96,1.11),
                    psa_outer=synthetic(11.20,3.20,1.25))
    def specimen(offset):
        return {'serial':'SYNTHETIC-control', 'expanded_pairwise_uncertainty_mm':.005,
                'case_step_sha256':DATUMS['case_step_sha256'],
                'pet_back_to_steel_upper_mm':.055,'pocket_within_projection_bounds':True,
                **{k:list(affinity.translate(v, xoff=offset if k in ('pet_hole','psa_hole','psa_outer') else 0.).exterior.coords)
                   for k,v in geometry.items()}}
    nominal = check(specimen(0.))
    shifted = check(specimen(.12))
    exposed = specimen(0.)
    exposed['psa_hole'] = list(synthetic(8.66,2.88,1.08).exterior.coords)
    recessed = specimen(0.)
    recessed['metal_outer'] = list(synthetic(8.75,2.97,1.12).exterior.coords)
    bearings = check(recessed)
    assert nominal['release_pass'] and not shifted['release_pass']
    assert not check(exposed)['geometry_pass'] and not bearings['geometry_pass']
    assert math.isclose(nominal['measured_minimum_distances_mm']['circumferential_steel_adhesive_bearing'], .08343, abs_tol=.00005)
    return {'synthetic_only':True, 'expected_nominal_pass':nominal,
            'misregistration_rejected':not shifted['geometry_pass'],
            'PSA_intrusion_rejected':not check(exposed)['geometry_pass'],
            'insufficient_circumferential_bearing_rejected':not bearings['geometry_pass']}


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('specimen', type=Path, nargs='?')
    cli.add_argument('--self-test', action='store_true')
    cli.add_argument('--output', type=Path)
    cli.add_argument('--suggest-recenter', action='store_true', help='Suggest a reversible pre-press jig adjustment.')
    args = cli.parse_args()
    if bool(args.self_test) == bool(args.specimen):
        cli.error('Choose a specimen JSON or --self-test.')
    if args.self_test:
        result=test()
    else:
        specimen=json.loads(args.specimen.read_text())
        result=check(specimen)
        if args.suggest_recenter:
            result['suggested_adjustment']=suggest_recenter(specimen)
    encoded = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end='')
    if result.get('release_pass') is False:
        raise SystemExit(1)
