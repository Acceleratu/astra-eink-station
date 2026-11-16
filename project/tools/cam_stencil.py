"""Specify stepped foil using the measured apertures on the finished paste plot."""
from shapely import union_all
from shapely.geometry import box


def stencil_plan(apertures, contacts):
    owners = [{p.ref for p in pads} for pads in contacts]
    pockets = []
    assigned = {}
    for family, thickness in [('WLCSP', .08), ('FH12', .15)]:
        targets = {i for i, pads in enumerate(contacts) if any(family in p.package.upper() for p in pads)}
        if not targets:
            continue
        while True:
            left, bottom, right, top = union_all([apertures[i] for i in targets]).bounds
            rectangle = box(left - 1.55, bottom - 1.55, right + 1.55, top + 1.55)
            touched = {i for i, ap in enumerate(apertures) if rectangle.covers(ap) or rectangle.boundary.distance(ap) < 1.52}
            devices = set().union(*(owners[i] for i in touched))
            enlarged = targets | touched | {i for i, refs in enumerate(owners) if refs & devices}
            if targets == enlarged:
                break
            targets = enlarged
        clearance = min(rectangle.boundary.distance(ap) for ap in apertures)
        if clearance < 1.5 or assigned.keys() & targets:
            raise ValueError('Stencil zones overlap or violate step-edge clearance')
        assigned.update({i: thickness for i in targets})
        pockets.append({'family': family, 'thickness_mm': thickness, 'bounds_xyxy_mm': [round(v, 5) for v in rectangle.bounds],
                        'active_apertures': len(targets), 'populated_refs': sorted(devices), 'closest_aperture_to_step_mm': round(clearance, 5)})
    if len(pockets) > 1 and box(*pockets[0]['bounds_xyxy_mm']).intersects(box(*pockets[1]['bounds_xyxy_mm'])):
        raise ValueError('Physical stencil pockets overlap')
    report = []
    for i, aperture in enumerate(apertures):
        thickness = assigned.get(i, .10)
        report.append({'contacts': [p.ref + '.' + p.pin for p in contacts[i]],
                       'center_xy_mm': [round(v, 4) for v in aperture.centroid.coords[0]], 'foil_mm': thickness,
                       'area_ratio': round(aperture.area / (aperture.length * thickness), 4),
                       'nominal_print_mm3': round(aperture.area * thickness, 6)})
    return pockets, report


def write_step_dxf(path, zones):
    # Distinct named DXF layers are process regions. Paste openings stay in GTP.
    chunks = [(0,'SECTION'),(2,'HEADER'),(9,'$ACADVER'),(1,'AC1009'),(9,'$MEASUREMENT'),(70,1),(0,'ENDSEC'),
              (0,'SECTION'),(2,'TABLES'),(0,'TABLE'),(2,'LAYER'),(70,len(zones))]
    for zone in zones:
        name = f"FOIL_{round(zone['thickness_mm']*1000):03d}UM"
        chunks.extend([(0,'LAYER'),(2,name),(70,0),(62,5 if zone['thickness_mm'] < .1 else 1),(6,'CONTINUOUS')])
    chunks.extend([(0,'ENDTAB'),(0,'ENDSEC'),(0,'SECTION'),(2,'ENTITIES')])
    for zone in zones:
        name = f"FOIL_{round(zone['thickness_mm']*1000):03d}UM"
        x0,y0,x1,y1 = zone['bounds_xyxy_mm']
        points = [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
        for start,end in zip(points,points[1:] + points[:1]):
            chunks.extend([(0,'LINE'),(8,name),(10,start[0]),(20,start[1]),(30,0),(11,end[0]),(21,end[1]),(31,0)])
    chunks.extend([(0,'ENDSEC'),(0,'EOF')])
    path.write_text(''.join(f'{code}\n{value}\n' for code,value in chunks))
