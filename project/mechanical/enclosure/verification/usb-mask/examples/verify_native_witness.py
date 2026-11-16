"""Cast the physical-size rejected example through the released native STEP, with all PSA transparent."""
import hashlib
import json
import math
import sys
from pathlib import Path

import cadquery as cq
from shapely import affinity
from shapely.geometry import Polygon

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import check_mask as baseline
import usb_mask
from check_measured_profiles import check, synthetic

CASE=baseline.ENCLOSURE/'cad/Astra-enclosure-assembly.step'
ORIGIN=(-10.018,57.158273847563486,5.603447101240016)
LIP=(-.0025,71.28043019381612,.7210212890960166)
SHIFT=(.022,-.022)


def point_at(x):
    span=LIP[0]-ORIGIN[0]
    return tuple(LIP[i]+(x-LIP[0])*(LIP[i]-ORIGIN[i])/span for i in range(3))


def signed_distance_to_round_profile(point,profile,centre):
    y,z=point[1:]
    w,h,r=profile
    v=abs(y-centre[0])-(w/2-r)
    t=abs(z-centre[1])-(h/2-r)
    return math.hypot(max(v,0.),max(t,0.))+min(max(v,t),0.)-r


def main():
    spec=HERE/'02-fail-oblique.json';data=json.loads(spec.read_text());old_gates=check(data)
    assert old_gates['geometry_pass'] and not old_gates['release_pass']
    assert data['case_step_sha256']==baseline.sha(CASE)
    expected={'metal_outer':(8.94,3.16,1.25),'metal_bore':(8.34,2.56,.95),
              'pet_hole':(8.72,2.94,1.10),'psa_hole':(8.748,2.968,1.114),'psa_outer':(11.20,3.20,1.25)}
    for key,profile in expected.items():
        reference=synthetic(*profile)
        if key.startswith(('pet_','psa_')):
            reference=affinity.translate(reference,*SHIFT)
        assert Polygon(data[key]).boundary.hausdorff_distance(reference.boundary)<.0003
    parts=baseline.load_assembly(CASE)
    explicit_cut=(8.72,2.94,1.100) # Actual PET profile is a +.020 mm normal dilation.
    parts[baseline.MAIN]=usb_mask._annulus(usb_mask.SKIRT,explicit_cut,usb_mask.MASK_FRONT_X,usb_mask.FILM_THICKNESS)
    for name in (baseline.MAIN,baseline.CAPS,baseline.BRACE):
        parts[name]=parts[name].translate((0,*SHIFT))
    r=cq.Edge.makeLine(ORIGIN,point_at(5.0));rb=baseline.bounds(r);hits=[]
    for name,shape in parts.items():
        if 'PSA' in name or baseline.box_spacing(baseline.bounds(shape),rb)>1e-5:
            continue
        clipped=r.intersect(shape)
        edges=clipped.Edges()
        if edges:
            first=min((v.toTuple() for v in clipped.Vertices()),key=lambda v:v[0])
            hits.append({'body':name,'first_xyz_mm':first,'ray_length_in_solid_mm':sum(e.Length() for e in edges)})
    hits.sort(key=lambda h:h['first_xyz_mm'][0]);assert hits[0]['body']=='PCB:PCB_1mm'
    physical_lip=signed_distance_to_round_profile(LIP,(8.94,3.16,1.25),(67.,1.725))
    assert physical_lip>.006
    actual_psa=(8.748,2.968,1.114);c=(67.+SHIFT[0],1.725+SHIFT[1]);layer={}
    for z in (.0,.010,.015,.020,.025,.030,.035,.040,.05):
        layer[str(z)]=signed_distance_to_round_profile(point_at(LIP[0]-z),actual_psa,c)
    assert layer['0.02']>.027 and layer['0.04']<0
    result={'case_step_sha256':baseline.sha(CASE),'example_sha256':hashlib.sha256(spec.read_bytes()).hexdigest(),
            'status':'Synthetic in-tolerance cut and placement on the measured production CAD, no physical test',
            'metal_and_all_downstream_native_geometry':'unchanged','all_PSA':'transparent for primary witness',
            'PET_normal_cut_deviation_mm':.020,'PSA_normal_cut_deviation_mm':.004,'registration_yz_mm':SHIFT,
            'external_origin_xyz_mm':ORIGIN,'metal_face_intercept_xyz_mm':LIP,
            'passed_three_original_dimensional_gates_and_registration':old_gates['geometry_pass'],
            'passes_new_zero_credit_optical_gate':old_gates['release_pass'],
            'ray_outside_true_outer_steel_at_lip_mm':physical_lip,'native_hits_in_order':hits,
            'ray_signed_distance_beyond_inner_PSA_profile_mm_by_clear_depth_from_steel_mm':layer,
            'layer_note':'A positive distance is inside the black carrier material if a continuous opaque carrier actually occupies this axial plane. Negative is within its aperture. The vendor does not publish the thickness of the separate acrylic skins.'}
    (HERE/'native-ray.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
