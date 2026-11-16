#!/usr/bin/env python3
"""Measure Ebyte antenna overhang and host copper exclusions in the native board.

Requires shapely 2.  Run: uv run --with shapely verification/independent/rf_geometry.py
This operates on native geometry without importing router or CAD-export code.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET
from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import polygonize, unary_union

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def angle(node):
    rot=node.get('rot','R0')
    if 'M' in rot:raise ValueError('Unexpected mirrored assembly object: '+str(node.attrib))
    return float(rot.removeprefix('S').removeprefix('R'))
def xy(node):return float(node.get('x','0')),float(node.get('y','0'))
def place(geom,node):
    return affinity.translate(affinity.rotate(geom,angle(node),origin=(0,0)),*xy(node))
def segment(w):
    if float(w.get('curve','0')):raise ValueError('Curved native wire not handled; inspect its geometry independently')
    return LineString([(float(w.get('x1')),float(w.get('y1'))),(float(w.get('x2')),float(w.get('y2')))])
def poly(p):
    if any(float(v.get('curve','0')) for v in p.findall('vertex')):raise ValueError('curved polygon')
    return Polygon([xy(v) for v in p.findall('vertex')])
def pads(pkg):
    for p in list(pkg):
        if p.tag=='smd':
            dx,dy=float(p.get('dx')),float(p.get('dy'))
            yield p.get('name'),place(box(-dx/2,-dy/2,dx/2,dy/2),p),p.get('layer')
        elif p.tag=='pad':
            diam=float(p.get('diameter',p.get('drill')));yield p.get('name'),Point(xy(p)).buffer(diam/2),'both'

def inspect(path):
    root=ET.parse(path);board=root.find('.//board');plain=board.find('plain')
    edge=unary_union([segment(w) for w in plain.findall("wire[@layer='20']")])
    outline=max(polygonize(edge), key=lambda g:g.area)
    elements={e.get('name'):e for e in board.findall('elements/element')}
    packages={(l.get('name'),p.get('name')):p for l in board.findall('libraries/library') for p in l.findall('packages/package')}
    mod=elements['U201']
    # Ebyte §3.1 module and upper antenna geometry; core tested a little
    # inside the manufacturer outline, independently of routing block files.
    antenna=place(box(-5.95,3.58,5.95,8.53),mod)
    shield_core=place(box(-4.6,-7.2,4.6,2.6),mod)
    full=place(box(-6,-8.6,6,8.6),mod)
    pad10=next(place(g,mod) for n,g,l in pads(packages[(mod.get('library'),mod.get('package'))]) if n=='10')
    overlap=antenna.intersection(outline)
    ax,ay=xy(mod);tip=place(Point(0,8.6),mod)
    errors=[];observed={}
    for a,b in (('1','41'),('16','42')):
        restrictions=[poly(p) for p in plain.findall(f"polygon[@layer='{b}']")]
        cuts=[poly(p) for p in board.findall(f"signals/signal/polygon[@layer='{a}'][@pour='cutout']")]
        candidates=[poly(p).buffer(float(p.get('width','0'))/2) for p in board.findall(f"signals/signal/polygon[@layer='{a}']") if p.get('pour')!='cutout']
        for r in plain.findall(f"rectangle[@layer='{b}']"):
            restrictions.append(box(*[float(r.get(k)) for k in ('x1','y1','x2','y2')]))
        restricted=overlap.difference(unary_union(restrictions)).area
        direct_cuts=overlap.difference(unary_union(cuts)).area
        observed[a]={'carrier_antenna_area_without_restrict_mm2':round(restricted,7),
                     'carrier_antenna_area_without_explicit_pour_cutout_mm2':round(direct_cuts,7),
                     'native_plane_unexcluded_overlap_mm2':round(overlap.intersection(unary_union(candidates)).difference(unary_union(restrictions+cuts)).area,7)}
        if restricted>1e-5:errors.append('Antenna not fully protected by native routing restriction, layer '+a)
        near=[]
        for s in board.findall('signals/signal'):
            net=s.get('name')
            for w in s.findall(f"wire[@layer='{a}']"):
                geom=segment(w).buffer(float(w.get('width'))/2)
                if geom.intersects(antenna):errors.append('wire enters antenna '+net+' layer '+a)
                if a=='16' and net!='GND' and geom.intersects(shield_core):
                    errors.append('bottom signal interrupts protected ground below shield core: '+net)
            for v in s.findall('via'):
                diam=float(v.get('diameter',v.get('drill')))
                geom=Point(xy(v)).buffer(diam/2)
                if geom.intersects(antenna):errors.append('via enters antenna '+net)
                if net=='GND':near.append(geom.distance(pad10))
        if near:observed[a]['nearest_GND_via_to_module_ground_pad10_mm']=round(min(near),4)
    for e in elements.values():
        if 'M' in e.get('rot',''):errors.append('component not exclusively top: '+e.get('name'));continue
        pkg=packages[(e.get('library'),e.get('package'))]
        for name,geom,layer in pads(pkg):
            if place(geom,e).intersects(antenna):
                errors.append('host pad enters antenna '+e.get('name')+'.'+name)
    # A nonzero sliver of antenna above host copper/FR4 is separately guarded
    # by genuine native layer restrictions; it must remain small.
    overhang=tip.distance(outline)
    if overhang<4.3 or overlap.area>6.5:errors.append('Module overhang below design clearance')
    return {'source':str(path.name),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'geometry':'Native pad, trace, via, routing restrictions and explicit pour cutouts; carrier pours still require independent post-CAM viewer.',
            'module_xy_mm':[ax,ay],'module_rotation_deg':angle(mod),'host_xy_bb_mm':list(outline.bounds),
            'nominal_module_transformed_bounds_mm':list(full.bounds),
            'antenna_tip_past_carrier_edge_mm':round(overhang,4),'antenna_test_core_over_carrier_area_mm2':round(overlap.area,6),
            'layers':observed,'errors':sorted(set(errors)),'status':'FAIL' if errors else 'PASS'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,default=ROOT/'board/astra.brd')
    ap.add_argument('--output',type=Path,default=HERE/'rf-geometry.json')
    args=ap.parse_args()
    if not args.board.is_file():ap.error('native board unavailable')
    result=inspect(args.board);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],result['antenna_tip_past_carrier_edge_mm'],'mm overhang',result['errors'])
    raise SystemExit(bool(result['errors']))

if __name__=='__main__':main()
