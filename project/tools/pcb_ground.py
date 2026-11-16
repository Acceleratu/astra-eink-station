"""Add ground-plane connections for physically isolated top copper islands.

Each new via meets the same mechanical drill and annular geometry as other
through vias. The top trace is anchored at an actual pad centre. The lower
end lies in the largest continuous grounded bottom copper region.
"""
from __future__ import annotations
import ctypes
import math

import numpy as np
from shapely import intersects_xy

from shapely.geometry import Point,LineString,Polygon,box
from shapely.ops import unary_union
from shapely.strtree import STRtree

from pcb_model import BASE,LAYOUT,get_design,read,write
from pcb_check import parse,run
from pcb_board import main as make_board
from pcb_finish import native_solver


def filled_areas(l,objs,pours,cuts,restricted,holes):
    net='GND'
    poly=next(shape for name,shape,dist in pours[l] if name==net)
    clearance=next(dist for name,shape,dist in pours[l] if name==net)
    blocked=[s['geom'].buffer(clearance,quad_segs=24) for s in objs if l in s['layers'] and s['net']!=net]
    blocked += list(cuts[l])+list(restricted[41 if l==1 else 42])+[g.buffer(.20) for name,n,g in holes if n is None]
    fill=poly.difference(unary_union(blocked))
    areas=[fill] if fill.geom_type=='Polygon' else [g for g in fill.geoms if g.geom_type=='Polygon']
    return areas


def raster_path(anchor, top_guard, via_guard, main_plane, connected_lands,
                additions, edge, clearance, diameter, step=.04, extent=7.0):
    """Reach a legal return via, or copper already tied to the ground plane."""
    n = math.ceil(extent / step)
    size = 2 * n + 1
    xs = anchor[0] + step * np.arange(-n, n+1)
    ys = anchor[1] + step * np.arange(-n, n+1)
    xx, yy = xs[None,:], ys[:,None]
    window = box(xs[0]-step, ys[0]-step, xs[-1]+step, ys[-1]+step)
    def local(tree):
        return unary_union(tree.geometries.take(tree.query(window)))
    top = local(top_guard)
    blocked_vias = local(via_guard)
    previous = [Point(v["x"], v["y"]).buffer(diameter+.25) for v in additions]
    if previous:
        blocked_vias = unary_union([blocked_vias, *previous])
    allowed = intersects_xy(edge.buffer(-clearance), xx, yy) & ~intersects_xy(top, xx, yy)
    valid_via = (intersects_xy(main_plane, xx, yy)
                 & intersects_xy(edge.buffer(-diameter/2-clearance), xx, yy)
                 & ~intersects_xy(blocked_vias, xx, yy))
    # Route to real solder lands or via centers already shown by independent
    # connectivity to be on the main ground. Centerline targets avoid a
    # marginal tangential connection dependent on Gerber rounding.
    known = local(connected_lands)
    existing = intersects_xy(known, xx, yy)
    empty = np.zeros((size,size), dtype=np.uint8)
    start = empty.copy()
    start[n,n] = 1
    def layers(grid):
        return np.ascontiguousarray([grid,empty], dtype=np.uint8)
    arrays = (layers(allowed),empty,layers(start),layers((valid_via | existing) & allowed))
    output = np.zeros(size*size*2,dtype=np.int32)
    ptr = ctypes.POINTER(ctypes.c_ubyte)
    count = native_solver()(size,size,*[v.ctypes.data_as(ptr) for v in arrays],
                            output.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),output.size)
    if count < 2:
        return None
    cells = list(reversed(output[:count].tolist()))
    pts, last_dir = [], None
    for i, k in enumerate(cells):
        xy = [round(float(xs[k % size]),5),round(float(ys[k // size]),5)]
        direction = k-cells[i-1] if i else None
        if direction == last_dir and i > 1:
            pts[-1] = xy
        else:
            pts.append(xy)
        last_dir = direction
    end=cells[-1]
    if top.intersects(LineString(pts)):
        return None
    return pts, not bool(existing[end//size,end%size])


def add_ground_returns(design,route,groups,board):
    _,_,edge,objs,holes,restrict,pours,cuts,_=parse(board)
    main_plane=max(filled_areas(16,objs,pours,cuts,restrict,holes),key=lambda q:q.area)
    dia=design.rules['via_diameter'];drill=design.rules['via_drill']
    margin=design.rules['route_clearance']+.006
    radii=[.75+.10*i for i in range(68)]
    directions=[i*math.pi/4 for i in range(8)]+[(i+.5)*math.pi/4 for i in range(8)]
    top_w=.18
    mnt=[g for key in (41,42,43) for g in restrict[key]]
    fid=[Point(x,y).buffer(1.16) for x,y in design.config['fiducials']]
    foreign_top=[o['geom'] for o in objs if 1 in o['layers'] and o['net']!='GND']
    top_guard=STRtree([g.buffer(margin+top_w/2,quad_segs=32) for g in foreign_top+list(restrict[41])+fid])
    forbid_via=[o['geom'] for o in objs if o['net']!='GND' or o['kind'] in ('smd','pad','via')]
    relaxed_top=STRtree([g.buffer(.155+.15/2,quad_segs=32) for g in foreign_top+list(restrict[41])+fid])
    relaxed_via=STRtree([o['geom'].buffer(dia/2+.156,quad_segs=32)
                        for o in objs if o['net']!='GND' or o['kind'] in ('smd','pad','via')]
                       +[g.buffer(dia/2+.18) for g in mnt+fid]
                       +[g.buffer(.25+drill/2,quad_segs=24) for _,_,g in holes])
    via_guard=STRtree([g.buffer(margin+dia/2,quad_segs=32) for g in forbid_via+mnt+fid]+
                      [g.buffer(.25+drill/2,quad_segs=24) for _,_,g in holes])
    pads={r+'.'+p:info for (r,p),info in design.pads.items()}
    additions=[];failed=[]
    groups=sorted(groups,key=len,reverse=True)
    main=set(groups[0])
    tied=[o['geom'].buffer(-.08) for o in objs if o['name'] in main or
          (o['net']=='GND' and o['kind']=='via' and main_plane.covers(o['geom'].centroid))]
    tied_tree=STRtree([g for g in tied if not g.is_empty])
    for area in filled_areas(1,objs,pours,cuts,restrict,holes):
        if area.area > .1 and tied_tree.query(area,predicate='intersects').size:
            tied.append(area.buffer(-.10))
    connected_lands=STRtree([g for g in tied if not g.is_empty])
    groups=groups[1:]
    for group in sorted(groups,key=len):
        candidates=[(n,pads[n]['center']) for n in group if n in pads]
        chosen_width=top_w
        chosen=None
        for radius in radii:
            if chosen:break
            for a in directions:
                if chosen:break
                dx=radius*math.cos(a);dy=radius*math.sin(a)
                for ref,anchor in candidates:
                    xy=(round(anchor[0]+dx,5),round(anchor[1]+dy,5));pt=Point(xy)
                    if not main_plane.covers(pt) or pt.distance(edge.boundary)<dia/2+design.rules['edge_clearance']:continue
                    if via_guard.query(pt,predicate='intersects').size:continue
                    if any(pt.distance(Point(v['x'],v['y']))<dia+.25 for v in additions):continue
                    line=LineString([anchor,xy])
                    if top_guard.query(line,predicate='intersects').size:continue
                    chosen=(ref,[list(anchor),list(xy)],True);break
        if chosen is None:
            for ref,anchor in candidates:
                path = raster_path(anchor, top_guard, via_guard, main_plane, connected_lands,
                                   additions, edge, design.rules['edge_clearance'], dia)
                if path:
                    chosen = (ref,*path)
                    break
        if chosen is None:
            for ref,anchor in candidates:
                path = raster_path(anchor, relaxed_top, relaxed_via, main_plane, connected_lands,
                                   additions, edge, design.rules['edge_clearance'], dia, step=.025)
                if path:
                    chosen = (ref,*path)
                    chosen_width=.15
                    break
        if chosen is None:
            failed.append(group)
            continue
        ref,points,needs_via=chosen
        x,y=points[-1]
        route['wires'].append(dict(net='GND',width=chosen_width,layer=1,points=points,protected=True))
        if needs_via:
            route['vias'].append(dict(net='GND',x=x,y=y,diameter=dia,drill=drill))
        additions.append(dict(x=x,y=y,via=needs_via,pad=ref,
                         trace_length_mm=round(LineString(points).length,3),island=group))
    return additions,failed


def main():
    d=get_design();board=BASE/'board/astra.brd';route=read(LAYOUT/'routes.json');logs=[]
    for i in range(6):
        audit=run(board)
        other=[e for e in audit['errors'] if e.get('category')!='disconnected net' or e.get('net')!='GND']
        ground=[e for e in audit['errors'] if e['category']=='disconnected net' and e['net']=='GND']
        if other:
            print(f'{len(other)} other issues still present; first: {other[0]}')
        if not ground:break
        returns,failed=add_ground_returns(d,route,ground[0]['groups'],board)
        logs.append(dict(iteration=i+1,connected=returns,unfilled=failed))
        print('Added',len(returns),'connected ground returns; remaining unreachable groups',failed,flush=True)
        if not returns:break
        write(LAYOUT/'routes.json',route);make_board()
    write(BASE/'verification/layout/ground-finishing-history.json',logs)
    report=run(board);write(BASE/'verification/layout/copper-audit.json',report)
    if report['errors']:
        print('Open:',[(e.get('net'),e.get('groups')) for e in report['errors'] if e['category']=='disconnected net'])
    return bool(report['errors'])

if __name__=='__main__':raise SystemExit(main())
