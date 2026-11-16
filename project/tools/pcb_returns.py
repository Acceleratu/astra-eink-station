"""Measure critical routes and inspect the protected bottom return areas on saved EAGLE copper."""
from collections import defaultdict
from math import hypot
from hashlib import sha256

from shapely.geometry import box
from shapely.strtree import STRtree

from pcb_check import parse,dims,Union
from pcb_model import BASE,get_design,write

def check():
    src=BASE/'board/astra.brd';d=get_design()
    board,attrs,edge,objs,holes,restr,pours,cuts,parts=parse(src)
    failures=[];measure={}
    tags={'RTC_XI':3.4,'RTC_XO':3.4,'EPD_SW':12,'EPD_PUMP':7,'RT_SW1':9,'RT_SW2':9,'PV_HVSW':5,'PV_LVSW':6,'PV_MPP_REF':2.5}
    for s in board.findall('signals/signal'):
        net=s.get('name')
        if net not in tags:continue
        length=0; layers=set()
        for w in s.findall('wire'):
            x,y=dims(w,'x1','y1');x2,y2=dims(w,'x2','y2')
            length+=hypot(x-x2,y-y2);layers.add(int(w.get('layer')))
        vias=len(s.findall('via'))
        measure[net]=dict(top_trace_total_mm=round(length,3),layers=sorted(layers),vias=vias,maximum_mm=tags[net])
        if vias or layers!={1} or length>tags[net]:failures.append(f"{net} via/layer/length: {measure[net]}")
    regions=[]
    for reg in d.planes:
        area=box(*reg['rect']);non_ground=[]
        for o in objs:
            if 16 in o['layers'] and o['net']!='GND' and area.intersects(o['geom']):non_ground.append(o['name'])
        regions.append(dict(name=reg['name'],bounds_mm=reg['rect'],foreign_copper=non_ground))
        if non_ground:failures.append('Return interrupted: '+reg['name'])
    by_ref={p['ref']:p for p in d.parts}
    rf=by_ref['U201']; w,h=d.footprints[rf['footprint']]['body']
    # +local Y rotates to +global X. Every solder land must remain on the board.
    land_margin=min(edge.boundary.distance(pp['geom']) for (r,n),pp in d.pads.items() if r=='U201')
    assembly=dict(module=rf['mpn'],antenna_axis='+X',overhang_mm=round(rf['x']+float(h)/2-d.size[0],3),
                  minimum_land_edge_distance_mm=round(land_margin,3))
    if land_margin<d.rules['edge_clearance']:failures.append('RF lands too close to board edge')
    ground=[o for o in objs if o['net']=='GND' and 1 in o['layers']]
    graph=Union(len(ground)); tree=STRtree([o['geom'] for o in ground])
    for i,o in enumerate(ground):
        for j in tree.query(o['geom'],predicate='dwithin',distance=.0002):
            if j>i:
                graph.union(i,j)
    via_clusters=defaultdict(list)
    for i,o in enumerate(ground):
        if o['kind']=='via':
            via_clusters[graph.root(i)].append(o['geom'].centroid)
    ground_pins={}
    for i,o in enumerate(ground):
        if not o.get('contact'):
            continue
        center=o['geom'].centroid
        vias=via_clusters[graph.root(i)]
        near=min(vias,key=lambda v:v.distance(center)) if vias else None
        ground_pins[o['name']]=dict(explicit_top_copper_to_via=bool(vias),
            closest_via_center_mm=[round(near.x,5),round(near.y,5)] if near else None)
    digest=sha256(src.read_bytes()).hexdigest()
    write(BASE/'verification/layout/ground-returns.json',dict(board_sha256=digest,
        contacts=len(ground_pins),explicitly_connected_to_via=sum(p['explicit_top_copper_to_via'] for p in ground_pins.values()),
        pins=ground_pins,
        interpretation='The graph uses only actual top pads, wires and plated vias. Pads without an explicit path use the solid top ground pour; the independent cam audit verifies complete connectivity after planar fill.'))
    report=dict(status='PASS' if not failures else 'FAIL',board='board/astra.brd',sha256=digest,critical_nets=measure,protected_bottom_areas=regions,
                rf_module=assembly,failures=failures,
                interpretation='Two-layer carrier; RF feed and 2.4 GHz matching network are internal to the selected radio module. The area checks test foreign copper and vias on the carrier. RF radiation and EMC measurements require the assembled antenna, display and enclosure.')
    write(BASE/'verification/layout/critical-copper.json',report)
    print(report['status'],failures)
    return failures

if __name__=='__main__':raise SystemExit(bool(check()))
