#!/usr/bin/env python3
"""Measure exposed test access and create board-centric top assembly drawings."""
import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
from shapely import affinity
from shapely.geometry import Point, box
import pymupdf as pdf
from cam_stock import ROOT, MODULES, populated
from cam_geometry import angle, transform, edge_centers, layer, polygons
from cam_spacing import assembly_spacing, boost_package_tolerance


def board_items(board):
    parts={p['ref']:p for block in MODULES for p in json.loads((ROOT/f'hardware/{block}.json').read_text())['parts']}
    geometries={key:geom for f in (ROOT/'hardware').glob('*-footprints.json') for key,geom in json.loads(f.read_text()).items()}
    native=ET.parse(board).find('drawing/board');shapes={};points=[];entries={}
    for element in native.findall('elements/element'):
        ref=element.get('name');p=parts[ref];fp=geometries[p['footprint']]
        coords={str(v['n']):transform(element,v['x'],v['y']) for v in fp['pads']}
        cx,cy=transform(element,*fp.get('body_center',(0,0)));w,h=fp['body'][:2]
        shell=affinity.rotate(box(cx-w/2,cy-h/2,cx+w/2,cy+h/2),angle(element.get('rot'))+fp.get('body_rot',0),origin=(cx,cy))
        entries[ref]={'part':p,'body':shell,'pads':coords,'xy':(cx,cy),'fp':fp,'element':element}
        if populated(p):shapes[ref]=shell
        elif (p['footprint']=='TP' or 'SWD_FIXTURE' in p['footprint'] or p['footprint']=='PV_WIRE_PAIR'):
            for pad in fp['pads']:
                name=str(pad['n']);points.append({'ref':ref,'pad':name,'net':p['pins'].get(name),'xy':coords[name],
                    'width':min(pad['w'],pad['h']),'kind':'terminal' if p['footprint']=='PV_WIRE_PAIR' else 'pogo'})
    return parts,native,entries,shapes,points


def metrics(board,gerbers):
    parts,native,entries,bodies,points=board_items(board)
    profile,_=edge_centers(next(gerbers.glob('*.gm1')))
    mask=layer(next(gerbers.glob('*.gts')))[0];paste=layer(next(gerbers.glob('*.gtp')))[0];cu,lands,_=layer(next(gerbers.glob('*.gtl')));exposed=mask.intersection(cu)
    metrics=[]
    for p in points:
        pt=Point(*p['xy']);target=pt.buffer(p['width']/2,quad_segs=48);near,refpart=min((target.distance(shape),ref) for ref,shape in bodies.items());
        nearest=min((pt.distance(Point(*q['xy'])) for q in points if round(pt.distance(Point(*q['xy'])),4)>0),default=None)
        cxy=exposed.covers(pt);usable=2*pt.distance(exposed.boundary) if cxy else 0
        is_signal=p['net'] not in ('GND','VMAIN','VBAT','PV_STORE','SYS_AON','CHG_IN','VAON')
        criteria={'center_exposed':cxy,'no_stencil':target.intersection(paste).area<.0001,'minimum_land':usable>=(.8 if is_signal else 1.)-.002,
              'probe_body_clearance':near>=.50-.001,'setback_to_routed_edge':target.distance(profile.boundary)>=3.2-.001,'probe_pitch':nearest is None or nearest>=1.27-.001}
        metrics.append({**p,'exposed_inscribed_diameter_mm':round(usable,3),'body_edge_clearance_mm':round(near,3),'nearest_body':refpart,
          'land_to_board_edge_mm':round(target.distance(profile.boundary),3),'nearest_probe_pitch_mm':round(nearest,3) if nearest is not None else None,
          'criteria':criteria,'status':'PASS' if all(criteria.values()) else 'REVIEW'})
    spacing=assembly_spacing(parts,bodies,lands)
    spacing['boost_max_case_to_foreign_paste']=boost_package_tolerance(entries,lands,polygons(paste))
    return metrics,native,entries,bodies,spacing


def draw(board,gerbers,out,verify):
    source_hash=hashlib.sha256(board.read_bytes()).hexdigest()
    measures,native,entries,bodies,spacing=metrics(board,gerbers)
    verify.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
    (verify/'probe-access.json').write_text(json.dumps(measures,indent=2)+'\n')
    (verify/'body-terminal-spacing.json').write_text(json.dumps(spacing,indent=2)+'\n')
    with (out/'probe-map.csv').open('w',newline='') as handle:
        wr=csv.writer(handle);wr.writerow(['Designator','Physical pad','Net','Center X mm','Center Y mm','Exposed diameter mm','Nearest populated body','Body clearance mm','Land to milled edge mm','Minimum pitch mm','Review']);
        for p in measures:wr.writerow([p['ref'],p['pad'],p['net'],*(f'{c:.4f}' for c in p['xy']),p['exposed_inscribed_diameter_mm'],p['nearest_body'],p['body_edge_clearance_mm'],p['land_to_board_edge_mm'],p['nearest_probe_pitch_mm'],p['status']])
    with (out/'measurement-links.csv').open('w',newline='') as handle:
        wr=csv.writer(handle);wr.writerow(['Designator','Manufacturer part','Pad 1 net','Pad 1 X mm','Pad 1 Y mm','Pad 2 net','Pad 2 X mm','Pad 2 Y mm'])
        for ref in ('R124','R125','R126'):
            if ref in entries:
                link=entries[ref];p=link['part'];wr.writerow([ref,p['mpn'],p['pins']['1'],*(f'{v:.4f}' for v in link['pads']['1']),p['pins']['2'],*(f'{v:.4f}' for v in link['pads']['2'])])
    profile,_=edge_centers(next(gerbers.glob('*.gm1')));doc=pdf.open()
    all_refs=list(entries);groups=[('Full board',all_refs)]
    for block in MODULES:
        parts=json.loads((ROOT/f'hardware/{block}.json').read_text())['parts']
        if block=='power':
            blocks=defaultdict(list)
            for part in parts:blocks[part['function']].append(part['ref'])
            groups.extend((label,refs) for label,refs in blocks.items())
        elif block=='wake':
            sensor=[p['ref'] for p in parts if p['function']=='Ambient sensor' and not p['ref'].startswith('R')]
            groups.append(('Always-on logic and measurement',[p['ref'] for p in parts if p['ref'] not in sensor and not p['ref'].startswith('SW')]))
            groups.append(('Environmental sensor',sensor))
            groups.append(('User buttons',[p['ref'] for p in parts if p['ref'].startswith('SW')]))
        else:
            groups.append((block.capitalize()+' circuit',[p['ref'] for p in parts]))
    for group,refs in groups:
        pg=doc.new_page(width=842,height=595);pg.insert_text((28,33),'ASTRA  /  TOP ASSEMBLY',fontsize=17,fontname='hebo',color=(.1,.16,.20));pg.insert_text((28,52),group+'  |  View from the populated side  |  Dimensions in mm',fontsize=10)
        poly=profile if group=='Full board' else None
        bounds=(min(poly.bounds[0],*(g.bounds[0] for g in bodies.values())),min(poly.bounds[1],*(g.bounds[1] for g in bodies.values())),max(poly.bounds[2],*(g.bounds[2] for g in bodies.values())),max(poly.bounds[3],*(g.bounds[3] for g in bodies.values()))) if poly is not None else (min(entries[r]['body'].bounds[0] for r in refs)-1.8,min(entries[r]['body'].bounds[1] for r in refs)-1.8,max(entries[r]['body'].bounds[2] for r in refs)+1.8,max(entries[r]['body'].bounds[3] for r in refs)+1.8)
        x0,y0,x1,y1=bounds;left,top,right,bottom=28,70,635,540;scale=min((right-left)/(x1-x0),(bottom-top)/(y1-y0));centerx=(left+right)/2;centery=(top+bottom)/2
        def pt(point):return pdf.Point(centerx+(point[0]-(x0+x1)/2)*scale,centery-(point[1]-(y0+y1)/2)*scale)
        def draw_geom(geom,color,fill=None,width=.5):
            coords=list(geom.exterior.coords);sh=pg.new_shape();sh.draw_polyline([pt(q) for q in coords]);sh.finish(color=color,fill=fill,width=width);sh.commit()
        if group=='Full board':draw_geom(profile,(.11,.23,.25),(.95,.97,.95),1.1)
        for hole in native.findall('plain/hole'):
            x,y=float(hole.get('x')),float(hole.get('y'))
            if x0<=x<=x1 and y0<=y<=y1:pg.draw_circle(pt((x,y)),scale*float(hole.get('drill'))/2,color=(.33,.35,.36),fill=(1,1,1),width=.6)
        if group=='Full board':
            for fid in native.findall('plain/polygon[@layer="1"]'):
                vv=[(float(v.get('x')),float(v.get('y'))) for v in fid.findall('vertex')]
                if len(vv)>40 and .95<=max(x for x,y in vv)-min(x for x,y in vv)<=1.05:
                    xy=(sum(x for x,y in vv)/len(vv),sum(y for x,y in vv)/len(vv))
                    pg.draw_circle(pt(xy),scale*.5,color=(.3,.36,.34),fill=(.3,.36,.34),width=.2)
        viewport=box(*bounds)
        for ref,e in entries.items():
            if ref in refs:continue
            clipped=e['body'].intersection(viewport)
            if not clipped.is_empty and clipped.geom_type=='Polygon':draw_geom(clipped,(.87,.87,.86),None,.4)
        keys=[];labels=[]
        for ref in refs:
            e=entries[ref];v=e['part'];is_test=not populated(v)
            if is_test:
                for coord in e['pads'].values():pg.draw_circle(pt(coord),max(1,scale*.4),color=(.18,.45,.48),width=.4)
            else:draw_geom(e['body'],(.18,.28,.33),(.83,.89,.88),.5)
            # Correct labels for polarized asymmetrical parts; pin A1 and ball 1
            # are body-local datums. Power-only Type C uses explicit B12 contact.
            first=next((pin for pin in ('A1','1','B12','K','A') if pin in e['pads']),None)
            if first and ref.startswith(('U','D','Q','J','Y','SW')):
                at=pt(e['pads'][first]);pg.draw_circle(at,max(1.2,min(2.2,scale*.12)),color=(.54,.18,.10),fill=(.54,.18,.10),width=.3);keys.append((ref,v['mpn'],first))
            if v['mpn']=='XGL4015-471MEC':
                start,end = pt(e['pads']['1']),pt(e['pads']['2']);pg.draw_line(start,end,color=(.56,.22,.12),width=1.1)
                pg.draw_circle(start,max(1.1,min(2.2,scale*.12)),color=(.54,.18,.10),fill=(.54,.18,.10),width=.3);keys.append((ref,v['mpn'],'1 = short lead'))
            if group!='Full board' or ref.startswith(('U','J','SW','TP')):
                at=pt(e['xy']);txt_size=6.5 if group=='Full board' else max(7,min(9,scale*.65));tw=pdf.get_text_length(ref,fontname='hebo',fontsize=txt_size)
                offsets=[(1,-1),(2,-7),(2,9),(-tw-2,-2),(-tw-2,9),(2,-15),(-tw-2,-15),(2,18)]
                def rect(offset):
                    x,y=at.x+offset[0],at.y+offset[1];return pdf.Rect(x-1,y-txt_size-1,x+tw+1,y+1.1)
                offset=next((v for v in offsets if all(not rect(v).intersects(previous) for previous in labels)),offsets[0]);labels.append(rect(offset))
                x,y=at.x+offset[0],at.y+offset[1]
                if abs(offset[1])>7 or offset[0]<0:pg.draw_line(at,(x+tw/2,y-2),color=(.50,.53,.53),width=.3)
                pg.insert_text((x,y),ref,fontsize=txt_size,fontname='hebo',color=(.08,.15,.18))
        pg.insert_text((662,84),'ORIENTATION DATUMS',fontsize=10,fontname='hebo');pg.insert_text((662,100),'Dot = named pad. L102 line = terminal axis.',fontsize=7)
        y=123
        for ref,mpn,first in keys:
            if group=='Full board' and ref not in ('J101','J102','U104','L102','J201','U201','J301','U403','U404'):continue
            if y>508:break
            pg.insert_text((662,y),ref+'   '+first,fontsize=8,fontname='hebo');pg.insert_text((662,y+11),mpn[:33],fontsize=7);y+=26
        pg.insert_text((28,566),'Board coordinate origin and numeric component centres are defined by the CPL. Consult the per-circuit pages for smaller components.',fontsize=8)
    doc.set_metadata({'title':'Astra top assembly and orientation','author':'Astra weather station design'});doc.save(out/'assembly-top.pdf',garbage=3,deflate=True)
    files=[next(gerbers.glob('*.'+ext)) for ext in ('gm1','gtl','gts','gtp')]
    results=[verify/'body-terminal-spacing.json',verify/'probe-access.json',out/'probe-map.csv',out/'measurement-links.csv',out/'assembly-top.pdf']
    if source_hash!=hashlib.sha256(board.read_bytes()).hexdigest():raise RuntimeError('Native board changed during assembly inspection')
    (verify/'assembly-geometry-inputs.json').write_text(json.dumps({'native_sha256':source_hash,
        'plot_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'result_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in results}},indent=2)+'\n')
    print('Probe locations:',len(measures),'requiring review:',[(p['ref'],p['pad'],p['criteria']) for p in measures if p['status']=='REVIEW'])

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--board',type=Path,default=ROOT/'board/astra.brd');a.add_argument('--gerbers',type=Path,default=ROOT/'fab/Gerbers');a.add_argument('--out',type=Path,default=ROOT/'fab');a.add_argument('--verify',type=Path,default=ROOT/'verification/manufacturing/assembly');opts=a.parse_args();draw(opts.board,opts.gerbers,opts.out,opts.verify)
