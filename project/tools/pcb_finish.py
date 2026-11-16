"""Finish outstanding physical copper connections with clearance-aware 2-layer search.

Takes the native SES geometry as the starting point. Each new segment is added
to the native route dataset and audited again against the exported EAGLE board.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import ctypes
import hashlib
from pathlib import Path
import subprocess
import tempfile

import numpy as np
from shapely import intersects_xy
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union
from shapely.strtree import STRtree

from pcb_model import BASE,LAYOUT,get_design,write,read
from pcb_route import outline,net_width
from pcb_check import Union
from pcb_board import main as make_board


def connections(d,route,net):
    # Carry both copper geometry for obstacle checks and exact centreline for
    # endpoint anchoring. A via contributes one node spanning both layers.
    items=[];others=[]
    for key,pp in d.pads.items():
        geom=pp["geom"]
        layer=[1,16] if pp["type"]=="pth" else [pp["pad"].get("layer",1)]
        p={"layers":layer,"geom":geom,"axis":Point(pp["center"]),"pad":key,"net":pp["net"]}
        (items if p["net"]==net else others).append(p)
    for w in route["wires"]:
        if len(w["points"])<2:continue
        line=LineString(w["points"])
        p=dict(layers=[w["layer"]],geom=line.buffer(w["width"]/2,quad_segs=24),axis=line,net=w["net"])
        (items if p["net"]==net else others).append(p)
    for v in route["vias"]:
        pt=Point(v["x"],v["y"]);p=dict(layers=[1,16],geom=pt.buffer(v["diameter"]/2,quad_segs=32),axis=pt,net=v["net"])
        (items if p["net"]==net else others).append(p)
    uf=Union(len(items))
    for layer in (1,16):
        ids=[i for i,p in enumerate(items) if layer in p["layers"]]
        geoms=[items[i]["geom"] for i in ids]
        if not ids:continue
        index=STRtree(geoms)
        for j,g in enumerate(geoms):
            for k in index.query(g,predicate="dwithin",distance=.0003):
                if k>j:uf.union(ids[j],ids[k])
    groups=defaultdict(list)
    for i,p in enumerate(items):groups[uf.root(i)].append(p)
    return [g for g in groups.values() if any(i.get("pad") for i in g)],others


def native_solver():
    source=BASE/"tools"/"pcb_grid.cpp"
    hashval=hashlib.sha256(source.read_bytes()).hexdigest()[:12]
    dest=Path(tempfile.gettempdir())/f"astra-route-grid-{hashval}.dylib"
    if not dest.exists():
        subprocess.run(["c++","-O3","-std=c++17","-shared","-fPIC",str(source),"-o",str(dest)],check=True)
    fn=ctypes.CDLL(str(dest)).trace_grid
    u8=ctypes.POINTER(ctypes.c_ubyte)
    fn.argtypes=[ctypes.c_int,ctypes.c_int,u8,u8,u8,u8,ctypes.POINTER(ctypes.c_int),ctypes.c_int]
    return fn


def finish_one(d,route,net,step=.06,conductor_width=None):
    groups,ob=connections(d,route,net)
    if len(groups)<=1:return None
    # Reconnect the closest pair of disconnected copper islands first.
    weighted=[(min(x["geom"].distance(y["geom"]) for x in g for y in h),i,j) for i,g in enumerate(groups) for j,h in enumerate(groups[:i])]
    _,i,j=min(weighted); src,dst=groups[i],groups[j]
    w=conductor_width or net_width(d,net); dia=d.rules["via_diameter"];via_margin=dia/2+.176
    width,height=d.size
    anchor=min((i for i in src+dst if i.get("pad")),key=lambda i:i["geom"].area)["axis"]
    ox=anchor.x%step;oy=anchor.y%step
    xt=np.arange(ox,width+step/2,step);yt=np.arange(oy,height+step/2,step)
    xx=xt[None,:]; yy=yt[:,None];nx,ny=len(xt),len(yt)
    def grid(shape):return intersects_xy(shape,xx,yy)
    def locally_draw(geoms,arr):
        for obj in geoms:
            x1,y1,x2,y2=obj.bounds
            c0=max(0,int(x1/step)-1);c1=min(nx,int(x2/step)+2)
            r0=max(0,int(y1/step)-1);r1=min(ny,int(y2/step)+2)
            if c0>=c1 or r0>=r1:continue
            arr[r0:r1,c0:c1] |= intersects_xy(obj,xt[None,c0:c1],yt[r0:r1,None])
    dead=[Point(h["x"],h["y"]).buffer(d.rules["mounting_keepout_radius"]) for h in d.board_holes]
    dead += [Point(h["x"],h["y"]).buffer(h["drill"]/2+.28) for h in d.package_holes]
    dead += [Point(x,y).buffer(1.0) for x,y in d.config["fiducials"]]
    pads=[p["geom"] for p in d.pads.values()]
    zone=[box(*reg["rect"]) for reg in d.planes if 16 in reg.get("layers",[16])]
    inner=Polygon(outline(d,d.rules["edge_clearance"])).buffer(-w/2-.010)
    allowed0=grid(inner); vm=grid(Polygon(outline(d,d.rules["edge_clearance"])).buffer(-dia/2-.02))
    blocked_via=np.zeros((ny,nx),bool)
    via_features=dead+pads+[p["geom"] for p in ob]+[p for p in zone]
    # Tented vias may connect to same-net tracks but must stay off solder lands.
    locally_draw([g.buffer(via_margin,quad_segs=16) for g in via_features],blocked_via)
    for v in route["vias"]:
        if v["net"]==net:
            locally_draw([Point(v['x'],v['y']).buffer(v['diameter']/2+via_margin)],blocked_via)
    allow=[]; starts=[]; goals=[]; axes=[]
    expansion=d.rules["route_clearance"] + w/2 + .010
    for li,layer in enumerate((1,16)):
        blocked=np.zeros((ny,nx),bool)
        foreign=[p["geom"] for p in ob if layer in p["layers"]]
        local=dead+[box(*reg["rect"]) for reg in d.keepouts if layer in reg.get("layers",[1,16])]
        if layer==16 and net!="GND":local+=zone
        locally_draw([g.buffer(expansion,quad_segs=16) for g in foreign+local],blocked)
        legal=allowed0 & ~blocked
        pair=[]
        for group,targets in ((src,starts),(dst,goals)):
            center_axes=[p["axis"] for p in group if layer in p["layers"]]
            g=unary_union(center_axes)
            a=np.zeros((ny,nx),bool)
            locally_draw([c.buffer(step*.73) for c in center_axes],a)
            targets.append(a & legal);pair.append(g)
        axes.append(pair);allow.append(legal)
    def cont(a):return np.ascontiguousarray(a,dtype=np.uint8)
    a,via,sta,go=map(cont,(allow,vm & ~blocked_via,starts,goals))
    if not sta.any() or not go.any():raise RuntimeError(f"{net}: a copper island has no legal escape anchors")
    fn=native_solver();ptr=ctypes.POINTER(ctypes.c_ubyte);ip=ctypes.POINTER(ctypes.c_int)
    result=np.zeros(nx*ny*2,dtype=np.int32)
    count=fn(nx,ny,*[v.ctypes.data_as(ptr) for v in (a,via,sta,go)],result.ctypes.data_as(ip),result.size)
    if count<1:raise RuntimeError(f"{net}: no clearance-compliant path at {step} mm grid")
    nodes=list(reversed(result[:count].tolist()))
    path=[(v//(nx*ny), round(xt[v%nx],6),round(yt[(v%(nx*ny))//nx],6)) for v in nodes]
    from shapely.ops import nearest_points
    def snap(li,p,side):
        q=nearest_points(Point(p),axes[li][side])[1]
        return [round(q.x,6),round(q.y,6)]
    wires=[];vias=[];current_layer=path[0][0];pts=[snap(current_layer,path[0][1:],0)]
    def save():
        compact=[]
        for q in pts:
            if compact and q==compact[-1]:continue
            if len(compact)>=2:
                s,t=compact[-2:]; cross=(t[0]-s[0])*(q[1]-t[1])-(t[1]-s[1])*(q[0]-t[0])
                dot=(t[0]-s[0])*(q[0]-t[0])+(t[1]-s[1])*(q[1]-t[1])
                if abs(cross)<1e-8 and dot>=0:compact.pop()
            compact.append(q)
        if len(compact)>1:wires.append(dict(net=net,width=w,layer=(1,16)[current_layer],points=compact,protected=True))
    for li,x,y in path:
        if li!=current_layer:
            save()
            vias.append(dict(net=net,x=x,y=y,diameter=dia,drill=d.rules["via_drill"]))
            pts=[];current_layer=li
        pts.append([x,y])
    pts.append(snap(path[-1][0],path[-1][1:],1));save()
    route["wires"].extend(wires);route["vias"].extend(vias)
    return dict(net=net,segments=sum(len(w['points'])-1 for w in wires),vias=len(vias),grid_mm=step)


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("nets",nargs="+");ap.add_argument("--routes",type=Path,default=LAYOUT/"routes.json")
    ap.add_argument("--report",type=Path,default=BASE/"verification/layout/finishing.json");ap.add_argument("--grid",type=float,default=.06)
    ap.add_argument("--width",type=float)
    a=ap.parse_args();d=get_design();r=read(a.routes);log=[]
    for net in a.nets:
        while True:
            result=finish_one(d,r,net,a.grid,a.width)
            if result is None:break
            log.append(result);print(result,flush=True)
            write(a.routes,r)
    write(a.report,log)
