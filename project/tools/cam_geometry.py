#!/usr/bin/env python3
"""Compare manufactured copper, holes and aperture plots with the native EAGLE topology.

Dependencies: gerbonara 1.5, shapely 2.x. Coordinates in mm. The connected-component
check uses copper geometry and plated drill files; X2 net labels are not used for it.
"""
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from gerbonara import graphic_primitives as gp
from gerbonara.excellon import ExcellonFile
from gerbonara.rs274x import GerberFile
from gerbonara.utils import MM, approximate_arc
from shapely import affinity, make_valid, union_all, STRtree
from shapely.geometry import Point, Polygon, LineString, box, GeometryCollection
from cam_stencil import stencil_plan

SAGITTA = 0.0008


def primitive(p):
    if isinstance(p, gp.Circle):
        return Point(p.x, p.y).buffer(p.r, quad_segs=48)
    if isinstance(p, gp.Rectangle):
        g = box(p.x-p.w/2,p.y-p.h/2,p.x+p.w/2,p.y+p.h/2)
        return affinity.rotate(g, p.rotation, origin=(p.x,p.y), use_radians=True)
    if isinstance(p, gp.Line):
        return LineString([(p.x1,p.y1),(p.x2,p.y2)]).buffer(p.width/2, quad_segs=24)
    if isinstance(p, gp.Arc):
        coords = list(approximate_arc(p.cx,p.cy,p.x1,p.y1,p.x2,p.y2,p.clockwise,max_error=SAGITTA))
        return LineString(coords).buffer(p.width/2,quad_segs=32)
    if isinstance(p, gp.ArcPoly):
        if not p.outline:
            return GeometryCollection()
        coords = []
        for start,end,(clockwise,center) in p.segments:
            if clockwise is None:
                coords.append(start)
            else:
                points = list(approximate_arc(*center,*start,*end,clockwise,max_error=SAGITTA))
                coords.extend(points[:-1])
        if len(coords) < 3:
            return GeometryCollection()
        geom=Polygon(coords)
        return geom if geom.is_valid else make_valid(geom)
    raise ValueError('Unknown Gerber geometry: ' + repr(p))


def object_shape(obj):
    # An aperture macro's clear primitives are local to the flash. Only the resulting
    # aperture footprint clears or adds to earlier plotted objects.
    geom = GeometryCollection()
    raw=[]
    for p in obj.to_primitives(MM):
        shape=primitive(p)
        if p.polarity_dark == obj.polarity_dark:
            raw.append(shape)
        else:
            geom=union_all([geom,*raw]).difference(shape)
            raw=[]
    return union_all([geom,*raw]) if raw else geom


def layer(path):
    data=GerberFile.open(path)
    copper=GeometryCollection()
    positive=True
    batch=[]
    flashes={}
    properties=Counter()
    for obj in data.objects:
        shape=object_shape(obj)
        properties[type(obj).__name__]+=1
        if obj.polarity_dark != positive:
            group=union_all(batch)
            copper=copper.union(group) if positive else copper.difference(group)
            positive=obj.polarity_dark
            batch=[]
        batch.append(shape)
        if type(obj).__name__=='Flash' and isinstance(obj.attrs,dict) and '.P' in obj.attrs:
            ref_pin=tuple(obj.attrs['.P'][:2])
            flashes[ref_pin]=shape if ref_pin not in flashes else flashes[ref_pin].union(shape)
    group=union_all(batch)
    copper=copper.union(group) if positive else copper.difference(group)
    return copper,flashes,dict(properties)


def angle(value):
    r=value or 'R0'
    if 'M' in r:
        raise ValueError('Bottom-side/mirrored component in top-only build: '+r)
    return float(r.split('R')[-1])


def transform(element, x, y):
    a=math.radians(angle(element.get('rot')))
    return (float(element.get('x')) + x*math.cos(a)-y*math.sin(a),
            float(element.get('y')) + x*math.sin(a)+y*math.cos(a))


@dataclass
class Land:
    ref: str
    pin: str
    center: tuple
    net: str
    tag: str
    drill: float
    xml: ET.Element
    package: str


def source(board):
    root=ET.parse(board).getroot().find('drawing/board')
    packages={(lib.get('name'),pkg.get('name')):pkg for lib in root.findall('libraries/library') for pkg in lib.findall('packages/package')}
    signals={(r.get('element'),r.get('pad')):sig.get('name') for sig in root.findall('signals/signal') for r in sig.findall('contactref')}
    lands=[]
    drills=[]
    for v in root.findall('signals/signal/via'):
        drills.append(('PTH',float(v.get('x')),float(v.get('y')),float(v.get('drill'))))
    for h in root.findall('plain/hole'):
        drills.append(('NPTH',float(h.get('x')),float(h.get('y')),float(h.get('drill'))))
    for el in root.findall('elements/element'):
        ref=el.get('name')
        pkg=packages[el.get('library'),el.get('package')]
        for p in pkg:
            if p.tag not in ('smd','pad','hole'):
                continue
            center=transform(el,float(p.get('x')),float(p.get('y')))
            drill=float(p.get('drill') or 0)
            if drill:
                drills.append(('NPTH' if p.tag=='hole' else 'PTH',*center,drill))
            if p.tag!='hole':
                pin=p.get('name')
                net=signals.get((ref,pin))
                lands.append(Land(ref,pin,center,net,p.tag,drill,p,el.get('package')))
    return root,lands,drills


def holes(path, classification):
    stream=ExcellonFile.open(path,plated=classification=='PTH')
    actual=[]
    shapes=[]
    for obj in stream.objects:
        p=list(obj.to_primitives(MM))
        if len(p)!=1:
            raise ValueError(f'Unexpected drill object {obj}')
        shape=primitive(p[0]);shapes.append(shape)
        if isinstance(p[0],gp.Circle):
            a=p[0];actual.append((classification,a.x,a.y,2*a.r))
        elif isinstance(p[0],gp.Line):
            a=p[0];actual.append((classification+'-SLOT',a.x1,a.y1,a.x2,a.y2,a.width))
        else:
            raise ValueError(f'Unsupported drill/slot {p[0]}')
    return actual,shapes


def compare_drills(source, plotted):
    # Excellon MM decimal output uses a 1 µm coordinate grid. Either neighbour
    # is valid for a native coordinate exactly halfway between grid points.
    unused=list(plotted);missing=[];max_error=0;matched=0
    for entry in source:
        candidates=[]
        for i,plot in enumerate(unused):
            if entry[0]!=plot[0] or len(entry)!=len(plot) or abs(entry[-1]-plot[-1])>.000001:continue
            error=max(abs(s-t) for s,t in zip(entry[1:-1],plot[1:-1]))
            if error<=.000501:candidates.append((error,i))
        if not candidates:
            missing.append(entry);continue
        error,index=min(candidates);unused.pop(index);max_error=max(max_error,error);matched+=1
    return missing,unused,{'matched_one_to_one':matched,'grid_mm':.001,'maximum_axis_quantization_mm':round(max_error,7)}


def polygons(geom):
    if geom.geom_type=='Polygon':
        return [geom]
    if hasattr(geom,'geoms'):
        return [p for g in geom.geoms for p in polygons(g)]
    return []


class Groups:
    def __init__(self,count): self.parent=list(range(count))
    def root(self,i):
        while i!=self.parent[i]:
            self.parent[i]=self.parent[self.parent[i]];i=self.parent[i]
        return i
    def join(self,values):
        if values:
            lead=self.root(values[0])
            for i in values[1:]: self.parent[self.root(i)]=lead


def nearest_pairs(parts, labels, threshold, ignore=None):
    tree=STRtree(parts); closest=None; violations=[]
    for i, geom in enumerate(parts):
        for raw in tree.query(geom.buffer(max(.6,threshold+.02)),predicate='intersects'):
            j=int(raw)
            if j<=i or (ignore and ignore(i,j)):
                continue
            distance=geom.distance(parts[j]); a,b=labels[i],labels[j]
            if closest is None or distance<closest[0]: closest=(distance,a,b)
            if distance+0.0015<threshold: violations.append((round(distance,5),a,b))
    return {'minimum_within_search_radius_mm':round(closest[0],5) if closest else None,
            'closest_pair':list(closest[1:]) if closest else [],'threshold_mm':threshold,
            'violations':sorted(violations,key=lambda item:item[0])}


def edge_centers(path):
    from shapely.ops import polygonize
    data=GerberFile.open(path);segments=[]
    for obj in data.objects:
        for p in obj.to_primitives(MM):
            if isinstance(p,gp.Line): pts=[(p.x1,p.y1),(p.x2,p.y2)]
            elif isinstance(p,gp.Arc): pts=list(approximate_arc(p.cx,p.cy,p.x1,p.y1,p.x2,p.y2,p.clockwise,max_error=SAGITTA))
            else: raise ValueError('Profile contains a non-centreline item')
            segments.append(LineString([(round(x,6),round(y,6)) for x,y in pts]))
    contours=list(polygonize(segments));
    if not contours: raise ValueError('Gerber outline does not form a closed contour')
    largest=max(contours,key=lambda p:p.area)
    return largest,len(contours)


def native_axis(wire):
    x0,y0,x1,y1=(float(wire.get(k)) for k in ('x1','y1','x2','y2'))
    sweep=math.radians(float(wire.get('curve',0)))
    if abs(sweep)<1e-9:return LineString([(x0,y0),(x1,y1)])
    dx,dy=x1-x0,y1-y0;length=math.hypot(dx,dy);shift=length/(2*math.tan(sweep/2));cx=(x0+x1)/2-dy*shift/length;cy=(y0+y1)/2+dx*shift/length
    radius=math.hypot(x0-cx,y0-cy);a0=math.atan2(y0-cy,x0-cx);step=2*math.acos(max(-1,1-SAGITTA/radius));n=max(2,math.ceil(abs(sweep)/step))
    return LineString([(x0,y0)]+[(cx+radius*math.cos(a0+sweep*i/n),cy+radius*math.sin(a0+sweep*i/n)) for i in range(1,n)]+[(x1,y1)])


def centerline_comparison(board,gerbers):
    # Compare conductor skeletons and their exact widths. A plotter may split a
    # native segment or combine collinear segments without changing geometry.
    before=defaultdict(list);after=defaultdict(list)
    for net in board.findall('signals/signal'):
        for wire in net.findall('wire'):
            before[(int(wire.get('layer')),net.get('name'),round(float(wire.get('width')),5))].append(native_axis(wire))
    for side,suffix in [(1,'gtl'),(16,'gbl')]:
        data=GerberFile.open(next(gerbers.glob('*.'+suffix)))
        for obj in data.objects:
            if type(obj).__name__ not in ('Line','Arc') or not isinstance(obj.attrs,dict) or '.N' not in obj.attrs:continue
            if dict(obj.aperture.attrs or ()).get('.AperFunction')!=('Conductor',):continue
            for seg in obj.to_primitives(MM):
                if isinstance(seg,gp.Line):points=[(seg.x1,seg.y1),(seg.x2,seg.y2)]
                elif isinstance(seg,gp.Arc):points=list(approximate_arc(seg.cx,seg.cy,seg.x1,seg.y1,seg.x2,seg.y2,seg.clockwise,max_error=SAGITTA))
                else:raise ValueError('Unsupported Gerber conductor centreline')
                after[(side,obj.attrs['.N'][0],round(seg.width,5))].append(LineString(points))
    differences=[];longest=0
    for key in sorted(before.keys()|after.keys()):
        native=union_all(before[key]);plot=union_all(after[key]);missing=native.difference(plot.buffer(.0015)).length;extra=plot.difference(native.buffer(.0015)).length
        longest=max(longest,missing,extra)
        if max(missing,extra)>.003:differences.append({'layer':key[0],'net':key[1],'width_mm':key[2],'missing_length_mm':round(missing,5),'extra_length_mm':round(extra,5)})
    return {'native_segments':sum(map(len,before.values())),'gerber_segments':sum(map(len,after.values())),
            'xy_comparison_tolerance_mm':.0015,'maximum_residual_length_mm':round(longest,5),'differences':differences}


def check(board,gerbers):
    native,lands,expected_drills=source(board)
    shapes={};flashes={};counts={};hashes={}
    for label,suffix in [('top','gtl'),('bottom','gbl'),('top_mask','gts'),('bottom_mask','gbs'),('top_paste','gtp'),('top_silk','gto'),('bottom_silk','gbo'),('edge','gm1')]:
        path,=gerbers.glob('*.'+suffix)
        shapes[label],flashes[label],counts[label]=layer(path)
        hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    actual_drills=[];bore_shapes=[];plated_shapes=[]
    for label in ('PTH','NPTH'):
        file,=gerbers.glob(f'*-{label}.drl')
        hits,masks=holes(file,label);actual_drills.extend(hits);bore_shapes.extend(masks)
        if label=='PTH':plated_shapes.extend(masks)
        hashes[file.name]=hashlib.sha256(file.read_bytes()).hexdigest()
    missing,extra,drill_delta=compare_drills(expected_drills,actual_drills)
    bore=union_all(bore_shapes)
    top=polygons(shapes['top'].difference(bore));bottom=polygons(shapes['bottom'].difference(bore))
    tt,bt=STRtree(top),STRtree(bottom);groups=Groups(len(top)+len(bottom))
    missing_barrels=[]
    for hole in plated_shapes:
        rim=hole.buffer(0.004).difference(hole)
        ts=[int(i) for i in tt.query(rim,predicate='intersects')];bs=[len(top)+int(i) for i in bt.query(rim,predicate='intersects')]
        if not ts or not bs: missing_barrels.append(list(hole.centroid.coords[0]))
        groups.join(ts+bs)
    by_net=defaultdict(set);by_group=defaultdict(set);badcenters=[];flash_diffs=[];missing_x2=[];n_groups={};pinmap={}
    for pad in lands:
        key=(pad.ref,pad.pin);keystr=pad.ref+'.'+pad.pin
        pos=Point(*pad.center)
        exact_flash=flashes['top'].get(key)
        if exact_flash is None:
            missing_x2.append(keystr)
        elif exact_flash.centroid.distance(pos)>0.002:
            # Offset/long PTH pad copper need not be centred on its drill.
            if pad.xml.get('shape')!='offset':
                flash_diffs.append((keystr,round(exact_flash.centroid.distance(pos),5)))
        sample=pos if not pad.drill else pos.buffer(pad.drill/2+0.004,quad_segs=48).difference(bore)
        intersects=[int(i) for i in tt.query(sample,predicate='intersects')]
        if not intersects:
            badcenters.append(keystr);continue
        roots={groups.root(i) for i in intersects}
        net=pad.net or ('<NC> '+keystr)
        for g in roots: by_group[g].add(net)
        by_net[net].update(roots)
        pinmap[keystr]=list(sorted(roots))
    shorts=[sorted(nets) for nets in by_group.values() if len(nets)>1]
    opens={n:len(ids) for n,ids in by_net.items() if len(ids)>1}
    via_mismatch=[];via_count=0
    for sig in native.findall('signals/signal'):
        for via in sig.findall('via'):
            via_count+=1;x,y,d=(float(via.get(key)) for key in ('x','y','drill'));sample=Point(x,y).buffer(d/2+.006,quad_segs=48).difference(bore)
            names=sorted({name for i in tt.query(sample,predicate='intersects') for name in by_group[groups.root(int(i))]})
            if names!=[sig.get('name')]: via_mismatch.append({'via_xy':[x,y],'native_net':sig.get('name'),'physical_group_nets':names})
    # Check actual merged mask dams as plotted, before registration/fab tolerances.
    maskpolys=polygons(shapes['top_mask']);masktree=STRtree(maskpolys);maskpads=defaultdict(list)
    for pad in lands:
        for i in masktree.query(Point(*pad.center),predicate='intersects'):
            maskpads[int(i)].append(pad.ref+'.'+pad.pin)
    common_openings=[pins for pins in maskpads.values() if len(pins)>1]
    # Exact named WLCSP land areas and all mask/paste registrations where custom
    # apertures are defined are checked by the generic package audit below.
    mask_data={}
    for k in ('top_mask','top_paste'):
        polys=polygons(shapes[k]);tree=STRtree(polys);rows={}
        for pad in lands:
            idx=tree.query(Point(*pad.center),predicate='intersects')
            if len(idx)==1:
                g=polys[int(idx[0])];xmin,ymin,xmax,ymax=g.bounds
                rows[pad.ref+'.'+pad.pin]=[round(xmax-xmin,4),round(ymax-ymin,4),round(g.area,5)]
        mask_data[k]=rows
    maskpolys=polygons(shapes['top_mask']); masknames=[','.join(maskpads.get(i,[])) or ('opening '+str(i)) for i in range(len(maskpolys))]
    spacing={'solder_mask_web':nearest_pairs(maskpolys,masknames,.10)}
    for side,polys,offset in [('top',top,0),('bottom',bottom,len(top))]:
        labels=[','.join(sorted(by_group[groups.root(i+offset)])) or ('floating '+str(i)) for i in range(len(polys))]
        spacing[side+'_copper']=nearest_pairs(polys,labels,.10,lambda i,j:groups.root(i+offset)==groups.root(j+offset))
    mask_to_copper={}
    for side,polys,t,offset in [('top',top,tt,0),('bottom',bottom,bt,len(top))]:
        openings=polygons(shapes[side+'_mask']); violations=[];closest=None
        for idx,opening in enumerate(openings):
            touch=t.query(opening,predicate='intersects')
            own={groups.root(int(i)+offset) for i in touch}
            if len(own)>1:violations.append({'opening':idx,'clearance':0,'reason':'opens several copper islands'})
            candidates=t.query(opening.buffer(.40),predicate='intersects')
            for raw in candidates:
                i=int(raw);gid=groups.root(i+offset)
                if gid in own:continue
                dist=opening.distance(polys[i]);names=sorted(by_group[gid])
                row={'opening':idx,'xy_mm':[round(v,4) for v in opening.centroid.coords[0]],'clearance':round(dist,5),'near_net':names}
                if closest is None or dist<closest[0]:closest=(dist,row)
                if dist+0.0015<.09:violations.append(row)
        mask_to_copper[side]={'openings':len(openings),'closest_foreign_copper':closest[1] if closest else None,'violations':violations}
    active_land=[p for p in lands if p.tag=='smd' and (p.ref,p.pin) in flashes['top']]
    spacing['different_net_smd_pads']=nearest_pairs([flashes['top'][(p.ref,p.pin)] for p in active_land],
        [p.ref+'.'+p.pin for p in active_land],.15,lambda i,j:active_land[i].net is not None and active_land[i].net==active_land[j].net)
    profile, contour_count=edge_centers(next(gerbers.glob('*.gm1')))
    from shapely.ops import polygonize
    native_profiles=list(polygonize([native_axis(w) for w in native.findall('plain/wire[@layer="20"]')]))
    if not native_profiles:raise ValueError('Source outline has no closed contour')
    source_profile=max(native_profiles,key=lambda p:p.area)
    outline_delta={'native_contours':len(native_profiles),'gerber_contours':contour_count,
        'symmetric_difference_mm2':round(source_profile.symmetric_difference(profile).area,7),
        'boundary_hausdorff_mm':round(source_profile.boundary.hausdorff_distance(profile.boundary),7)}
    profile_results={}
    for side in ('top','bottom'):
        copper=shapes[side];profile_results[side]={'distance_to_milled_edge_mm':round(copper.distance(profile.boundary),5),
             'copper_outside_profile_area_mm2':round(copper.difference(profile).area,6)}
    holespace=nearest_pairs(bore_shapes,[f'{h[0]} ({h[1]:.3f},{h[2]:.3f})' for h in actual_drills],.20)
    pastepolys=polygons(shapes['top_paste']);pastetree=STRtree(pastepolys);owners=defaultdict(list)
    for p in active_land:
        for i in pastetree.query(flashes['top'][(p.ref,p.pin)],predicate='intersects'):owners[int(i)].append(p)
    zones,stencil=stencil_plan(pastepolys,[owners[i] for i in range(len(pastepolys))])
    native_bounds=[]
    for w in native.findall('plain/wire[@layer="20"]'):
        native_bounds.extend([(float(w.get('x1')),float(w.get('y1'))),(float(w.get('x2')),float(w.get('y2')))])
    xy=(min(x for x,y in native_bounds),min(y for x,y in native_bounds),max(x for x,y in native_bounds),max(y for x,y in native_bounds)) if native_bounds else None
    jobs=list(gerbers.glob('*.gbrjob'));job_data=json.loads(jobs[0].read_text()) if jobs else {}
    edge_bounds=list(shapes['edge'].bounds)
    return {'source':board.name,'source_sha256':hashlib.sha256(board.read_bytes()).hexdigest(), 'file_sha256':hashes,
            'maximum_curve_approximation_mm':SAGITTA,'native_outline_centerline_bounds_mm':xy,'plot_outline_ink_bounds_mm':edge_bounds,
            'job_specifications':job_data.get('GeneralSpecs',{}),'reopened_objects':counts, 'native_pad_count':len(lands),
            'native_signal_count':len(native.findall('signals/signal')),'native_drill_count':len(expected_drills),'reopened_drill_count':len(actual_drills),
            'native_vias_compared':via_count,'via_net_mismatches':via_mismatch,'track_centerlines':centerline_comparison(native,gerbers),'outline_comparison':outline_delta,
            'missing_native_drills':missing,'extra_plot_drills':extra,'drill_coordinate_comparison':drill_delta,'missing_plated_annulus':missing_barrels,
            'top_copper_islands_after_drill':len(top),'bottom_copper_islands_after_drill':len(bottom),'missing_copper_at_pads':badcenters,
            'shorted_nets_from_copper':shorts,'open_nets_from_copper':opens,'missing_x2_pad_attributes':missing_x2,'shifted_x2_pad_centers':flash_diffs,
            'merged_top_mask_openings':common_openings,'top_silk_to_mask_distance_mm':(shapes['top_silk'].distance(shapes['top_mask']) if not shapes['top_silk'].is_empty and not shapes['top_mask'].is_empty else None),
            'pad_physical_groups':pinmap,'aperture_size_xy_area_mm':mask_data,'manufactured_spacing':spacing,
            'drill_spacing':holespace,'mask_to_foreign_copper':mask_to_copper,'gerber_outline_contours':contour_count,'copper_to_gerber_outline':profile_results,
            'stencil_step_zones':zones,'stencil_apertures':stencil,'minimum_stencil_area_ratio':min((a['area_ratio'] for a in stencil),default=None)}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('board',type=Path);p.add_argument('gerbers',type=Path);p.add_argument('report',type=Path)
    a=p.parse_args();r=check(a.board,a.gerbers);a.report.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');
    print(json.dumps({k:v for k,v in r.items() if k in ('native_pad_count','reopened_drill_count','native_signal_count','shorted_nets_from_copper','open_nets_from_copper','missing_copper_at_pads','missing_native_drills','extra_plot_drills','missing_plated_annulus','merged_top_mask_openings')},indent=2))

if __name__=='__main__': main()
