"""Independent planar preflight on the saved EAGLE board (no router state is read).

Requires Shapely 2. The ground-fill reconstruction conservatively removes all
other-net copper plus the specified pour clearance; CAM refill remains a
separate check. Copper distances use rounded native lines/pads.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
from hashlib import sha256
from xml.etree import ElementTree as ET
import argparse
import json
import re

from shapely import affinity
from shapely.geometry import Point, box, Polygon, LineString
from shapely.ops import unary_union, polygonize
from shapely.strtree import STRtree

ROOT=Path(__file__).resolve().parents[1]
TOL=.00025

def f(el,key,default=0):
    return float(el.get(key,default))


def dims(el,*attrs): return tuple(f(el,a) for a in attrs)


def disk(x,y,r): return Point(x,y).buffer(r,quad_segs=48)


def rr(w,h,rounded):
    r=min(w,h)*rounded/200
    if r < 1e-8: return box(-w/2,-h/2,w/2,h/2)
    if abs(w-h)<1e-8 and abs(2*r-w)<1e-8: return disk(0,0,r)
    return box(-w/2+r,-h/2+r,w/2-r,h/2-r).buffer(r,quad_segs=32)


def rot(node):
    s=node.get("rot","R0")
    return float(s[s.index("R")+1:])


def primitive(e):
    if e.tag=="polygon":
        pts=[dims(v,"x","y") for v in e.findall("vertex")]
        return Polygon(pts).buffer(f(e,"width")/2,quad_segs=32)
    if e.tag=="rectangle":
        return box(*dims(e,"x1","y1","x2","y2"))
    if e.tag=="wire":
        return LineString([dims(e,"x1","y1"),dims(e,"x2","y2")]).buffer(f(e,"width")/2,quad_segs=32)
    if e.tag in ("circle","hole"):
        x,y=dims(e,"x","y")
        if e.tag=="hole": return disk(x,y,f(e,"drill")/2)
        r,w=dims(e,"radius","width")
        return disk(x,y,r+w/2).difference(disk(x,y,max(0,r-w/2)))
    raise ValueError(f"unknown shape {e.tag}")


def placed(shape,element):
    geom=affinity.rotate(shape,rot(element),origin=(0,0))
    return affinity.translate(geom,*dims(element,"x","y"))


def parse(path):
    board=ET.parse(path).find(".//board")
    packages={p.get("name"):p for p in board.findall("libraries/library/packages/package")}
    attrs={a.get("name"):a.get("value") for a in board.findall("designrules/param")}
    contact_nets={(r.get("element"),r.get("pad")):s.get("name") for s in board.findall("signals/signal") for r in s.findall("contactref")}
    objects=[]; holes=[]; restrict=defaultdict(list); pours=defaultdict(list); cut=defaultdict(list)
    elements={}
    def add(name,net,typ,layers,geom,contact=False,drill=None):
        objects.append(dict(name=name,net=net,kind=typ,layers=layers,geom=geom,contact=contact,drill=drill))
    for j,el in enumerate(board.findall("elements/element")):
        pkg=packages[el.get("package")]
        ref=el.get("name"); elements[ref]=dict(x=f(el,"x"),y=f(el,"y"),rot=rot(el),package=el.get("package"))
        for p in pkg:
            if p.tag in ("smd","pad"):
                n=p.get("name")
                net=contact_nets.get((ref,n),"@"+ref+"."+n)
                hshape=None
                if p.tag=="smd":
                    shape=rr(f(p,"dx"),f(p,"dy"),f(p,"roundness"))
                    ls=[int(p.get("layer"))]
                else:
                    diam=f(p,"diameter")
                    shape=disk(0,0,diam/2) if p.get("shape","round")=="round" else rr(diam,diam,0)
                    hshape=placed(disk(f(p,"x"),f(p,"y"),f(p,"drill")/2),el)
                    ls=[1,16]
                    holes.append((ref+"."+n,net,hshape))
                shape=affinity.rotate(shape,rot(p),origin=(0,0))
                shape=placed(affinity.translate(shape,f(p,"x"),f(p,"y")),el)
                add(ref+"."+n,net,p.tag,ls,shape,True,hshape)
            if p.tag=="hole": holes.append((ref+".hole",None,placed(primitive(p),el)))
            l=p.get("layer")
            if p.tag in ("rectangle","polygon","circle","wire") and l in ("41","42","43"):
                restrict[int(l)].append(placed(primitive(p),el))
    for j,p in enumerate(board.findall("plain/*")):
        l=p.get("layer")
        if p.tag=="hole": holes.append(("H"+str(j),None,primitive(p)))
        if p.tag in ("rectangle","polygon","circle","wire"):
            if l in ("41","42","43"): restrict[int(l)].append(primitive(p))
            if l in ("1","16"): add("plain-"+str(j),"@PLAIN"+str(j),p.tag,[int(l)],primitive(p))
    edges=[LineString([dims(e,"x1","y1"),dims(e,"x2","y2")]) for e in board.findall("plain/wire[@layer='20']")]
    enclosure=list(polygonize(edges))
    if len(enclosure)!=1: raise ValueError(f"Expected exactly one board perimeter, found {len(enclosure)}")
    for s in board.findall("signals/signal"):
        net=s.get("name")
        for j,w in enumerate(s):
            nm=net+":"+str(j)
            if w.tag=="via":
                x,y=dims(w,"x","y")
                hshape=disk(x,y,f(w,"drill")/2); holes.append((nm,net,hshape))
                add(nm,net,"via",[1,16],disk(x,y,f(w,"diameter")/2),drill=hshape)
            if w.tag=="wire":
                add(nm,net,"wire",[int(w.get("layer"))],primitive(w))
            if w.tag=="polygon":
                l=int(w.get("layer"))
                if w.get("pour")=="cutout": cut[l].append(primitive(w))
                else: pours[l].append((net,primitive(w),f(w,"isolate")))
    return board,attrs,enclosure[0],objects,holes,restrict,pours,cut,elements


class Union:
    def __init__(self,n): self.rep=list(range(n))
    def root(self,i):
        while i!=self.rep[i]:
            self.rep[i]=self.rep[self.rep[i]];i=self.rep[i]
        return i
    def union(self,i,j):
        a,b=self.root(i),self.root(j)
        if a!=b:self.rep[b]=a


def run(src,placement=None):
    board,attrs,edge,objs,holes,rules,pours,cut,elements=parse(src)
    err=[]; min_clear={}; min_drill=None
    getmm=lambda v: float(v.replace("mm",""))
    minedge=getmm(attrs["mdCopperDimension"])
    def issue(category,**fields): err.append({"category":category,**fields})
    minwidth=getmm(attrs["msWidth"])
    widths={str(c.get("number")):float(c.get("width","0")) for c in board.findall("classes/class")}
    observed_widths=defaultdict(Counter)
    for sig in board.findall("signals/signal"):
        net=sig.get("name");cls=sig.get("class","0");nominal=max(minwidth,widths[cls])
        for w in sig.findall("wire"):
            width=f(w,"width");observed_widths[cls][width]+=1
            if width<nominal-.000001:
                issue("minimum track width",net=net,net_class=cls,actual_mm=width,required_mm=nominal,
                      layer=w.get("layer"),midpoint=[round((f(w,"x1")+f(w,"x2"))/2,5),round((f(w,"y1")+f(w,"y2"))/2,5)])
    for layer in (1,16):
        ind=[i for i,x in enumerate(objs) if layer in x["layers"]]
        geoms=[objs[i]["geom"] for i in ind]
        tree=STRtree(geoms)
        for j,g in enumerate(geoms):
            a=objs[ind[j]]
            if not edge.buffer(TOL).covers(g) or edge.boundary.distance(g)<minedge-TOL:
                issue("edge clearance",name=a["name"],layer=layer,actual_mm=round(edge.boundary.distance(g),5),required_mm=minedge)
            for k in tree.query(g,predicate="dwithin",distance=.45):
                if k<=j:continue
                b=objs[ind[k]]
                if a["net"]==b["net"]:
                    if {a["kind"],b["kind"]} in ({"smd","via"},{"smd","pad"},{"smd"}):
                        d=g.distance(geoms[k])
                        if d+TOL<.15:
                            issue("same-signal land clearance",a=a["name"],b=b["name"],layer=layer,actual_mm=round(d,6),required_mm=.15)
                    continue
                d=g.distance(geoms[k])
                types=":".join(sorted([a["kind"],b["kind"]]))
                if d<min_clear.get(types,{"mm":100})["mm"]:
                    min_clear[types]={"mm":round(d,6),"a":a["name"],"b":b["name"],"layer":layer}
                pair=sorted((a["kind"],b["kind"]))
                threshold=.15
                if d+TOL < threshold:
                    issue("foreign copper clearance",a=a["name"],b=b["name"],layer=layer,actual_mm=round(d,6),required_mm=threshold)
            rr=rules[41 if layer==1 else 42]
            if rr and any(r.intersects(g) for r in rr):
                issue("copper inside restrict",name=a["name"],layer=layer)
        for hn,net,dr in holes:
            threshold=.28 if any(x["kind"]=="pad" and x["name"]==hn for x in objs) else .20
            for k in tree.query(dr,predicate="dwithin",distance=threshold):
                a=objs[ind[k]]
                if net and net==a["net"]:continue
                d=dr.distance(a["geom"])
                if d+TOL<threshold:
                    issue("drill to foreign copper",hole=hn,other=a["name"],layer=layer,actual_mm=round(d,6),required_mm=threshold)
    if holes:
        ht=STRtree([v[2] for v in holes])
        for j,(name,net,geo) in enumerate(holes):
            for k in ht.query(geo,predicate="dwithin",distance=.5):
                if k<=j:continue
                nm,n,g=holes[k];d=geo.distance(g)
                if min_drill is None or d<min_drill["mm"]: min_drill={"a":name,"b":nm,"mm":round(d,5)}
                if d+TOL<.25:issue("drill-to-drill",a=name,b=nm,actual_mm=round(d,5),required_mm=.25)
    # Rebuild ground pours separately on each copper layer. Ground pads and
    # wires participate in connectivity. Top thermal-spoke details are further
    # verified on KiCad's independent actual zone refill and the CAM outputs.
    for layer in (1,16):
        for net,poly,spacing in pours[layer]:
            obstacles=[v["geom"].buffer(spacing,quad_segs=16) for v in objs if layer in v["layers"] and v["net"]!=net]
            obstacles+=cut[layer]+rules[41 if layer==1 else 42]
            obstacles += [h.buffer(.20) for _,n,h in holes if n is None]
            fill=poly.difference(unary_union(obstacles))
            solids=[fill] if fill.geom_type=="Polygon" else list(fill.geoms)
            for j,area in enumerate(solids):
                if area.area>.0001: objs.append(dict(name=f"{net} plane {layer}/{j}",kind="pour",net=net,layers=[layer],geom=area,contact=False))
    uf=Union(len(objs))
    for layer in (1,16):
        inds=[i for i,ob in enumerate(objs) if layer in ob["layers"]]
        geoms=[objs[i]["geom"] for i in inds];tree=STRtree(geoms)
        for j,g in enumerate(geoms):
            for k in tree.query(g,predicate="dwithin",distance=TOL):
                if k>j and objs[inds[k]]["net"]==objs[inds[j]]["net"]:uf.union(inds[j],inds[k])
    con=defaultdict(lambda:defaultdict(list))
    for i,o in enumerate(objs):
        if o.get("contact") and not str(o["net"]).startswith("@"):
            con[o["net"]][uf.root(i)].append(o["name"])
    for net,groups in con.items():
        if len(groups)>1:issue("disconnected net",net=net,groups=list(groups.values()))
    # Explicitly test via-in-pad on every net including ground, regardless of
    # whether same-net copper passes normal electrical clearance checks.
    surface=[o for o in objs if o["kind"]=="smd"];st=STRtree([o["geom"] for o in surface])
    for via in (o for o in objs if o["kind"]=="via"):
        h=via["drill"]
        for j in st.query(h,predicate="intersects"):
            issue("via drill in solder land",via=via["name"],pad=surface[j]["name"])
    data={"source":"board/astra.brd" if src.resolve()==(ROOT/"board/astra.brd").resolve() else str(src),"sha256":sha256(src.read_bytes()).hexdigest(),"counts":{"contacts":sum(o.get("contact",False) for o in objs),"nets":len(con),
          "routed_segments":sum(o["kind"]=="wire" for o in objs),"through_vias":sum(o["kind"]=="via" for o in objs),
          "mechanical_and_plated_holes":len(holes)},"minimum_observed_distances_mm":min_clear,"closest_holes":min_drill,"routed_widths_by_native_class":observed_widths,
          "errors":err,"status":"PASS" if not err else "FAIL"}
    return data


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("board",type=Path,nargs="?",default=ROOT/"board"/"astra.brd")
    ap.add_argument("--out",type=Path,default=ROOT/"verification"/"layout"/"copper-audit.json")
    a=ap.parse_args();report=run(a.board)
    a.out.write_text(json.dumps(report,indent=2)+"\n")
    print(report["status"],dict(Counter(e["category"] for e in report["errors"])),report["counts"])
    raise SystemExit(0 if not report["errors"] else 1)
