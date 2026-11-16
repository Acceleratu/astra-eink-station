"""Check component geometry, native copper at placement and locked paths before routing."""
from collections import Counter
from pathlib import Path
import argparse
import json

from shapely.geometry import Point, Polygon, box, LineString
from shapely.strtree import STRtree

from pcb_model import BASE, get_design, body_shape
from pcb_route import outline

EPS=.00025

def is_ic(p):
    return p["ref"].startswith("U") and any(t in p["footprint"].upper() for t in ("QFN","LGA","WLCSP","DFN","BGA","LFCSP"))

def body_gap(a,b):
    # Manufacturer recommended assembly rework spacing is determined by the two technologies.
    if is_ic(a) or is_ic(b):return 1.0
    af,bf=a["footprint"],b["footprint"]
    if "0402" in af and "0402" in bf:return .15
    if "0402" in af or "0402" in bf:return .18
    return .20

def check(d):
    errors=[]; min_gap=None
    perim=Polygon(outline(d)); r=d.rules["mounting_keepout_radius"]
    keepouts=[box(*g["rect"]) for g in d.keepouts]
    mounted=[p for p in d.parts if p.get("populate",True) and not p.get("dnp",False) and float(p.get("height_mm",0))>0]
    bodies={p["ref"]:body_shape(p,d.footprints[p["footprint"]]) for p in mounted}
    rec={p["ref"]:p for p in mounted}
    def fail(c,**kw): errors.append(dict(category=c,**kw))
    for i,a in enumerate(mounted):
        g=bodies[a["ref"]]
        if a["ref"]!="U201" and not perim.buffer(.002).covers(g):fail("component over board edge",ref=a["ref"],bounds=g.bounds)
        if float(a.get("height_mm",d.footprints[a["footprint"]].get("height_mm",0)))>4.1+EPS: fail("height limit",ref=a["ref"])
        for h in d.board_holes:
            if g.intersects(Point(h["x"],h["y"]).buffer(r)):fail("fastener clearance",ref=a["ref"],hole=h)
        for j,keep in enumerate(keepouts):
            if 1 not in d.keepouts[j].get("layers",[1,16]):continue
            if a["ref"]=="U201" and "U201" in d.keepouts[j].get("name",""):continue
            if g.intersects(keep):fail("physical keepout",ref=a["ref"],region=d.keepouts[j].get("name","keepout"))
        for b in mounted[i+1:]:
            bg=bodies[b["ref"]]; dist=g.distance(bg); req=body_gap(a,b)
            if min_gap is None or dist<min_gap["actual"]:
                min_gap=dict(a=a["ref"],b=b["ref"],actual=round(dist,5),required=req)
            if dist+EPS<req:fail("body to body",a=a["ref"],b=b["ref"],actual=round(dist,5),required=req)
    for name,c in d.pads.items():
        g=c["geom"]
        if not perim.buffer(.001).covers(g) or perim.boundary.distance(g)+EPS<d.rules["edge_clearance"]:
            fail("land to edge",pad=name,actual=round(g.distance(perim.boundary),5))
    pads=list(d.pads.items())
    for i,(name,a) in enumerate(pads):
        for n2,b in pads[i+1:]:
            if a["net"] and b["net"]==a["net"]:continue
            if a["geom"].distance(b["geom"])+EPS<d.rules["smd_clearance"]:
                fail("land copper",a=name,b=n2,actual=round(a["geom"].distance(b["geom"]),5),required=d.rules["smd_clearance"])
    paths=[(w,LineString(w["points"]).buffer(w["width"]/2,quad_segs=32)) for w in d.fixed_wires]
    for w,geo in paths:
        for key,p in pads:
            if p["net"]==w["net"] or (not p["pad"].get("drill") and p["pad"].get("layer",1)!=w.get("layer",1)):continue
            dist=p["geom"].distance(geo)
            if dist+EPS<.15:fail("fixed track to land",net=w["net"],pad=key,actual=round(dist,5))
        for other,g in paths:
            if other["net"]!=w["net"] and other.get("layer",1)==w.get("layer",1) and g.distance(geo)+EPS<.15:
                fail("fixed track to track",net=w["net"],other=other["net"],actual=round(g.distance(geo),5))
    for via in d.fixed_vias:
        copper=Point(via["x"],via["y"]).buffer(via["diameter"]/2,quad_segs=32)
        for key,p in pads:
            if p["net"]!=via["net"] and copper.distance(p["geom"])+EPS<.15:
                fail("fixed via to land",via=via,pad=key,actual=round(copper.distance(p["geom"]),5))
        for w,g in paths:
            if via["net"]!=w["net"] and copper.distance(g)+EPS<.15:
                fail("fixed via to track",via=via,net=w["net"],actual=round(copper.distance(g),5))
    return dict(status="PASS" if not errors else "FAIL",parts=len(d.parts),placed_bodies=len(mounted),
                closest_nominal_bodies_mm=min_gap,errors=errors)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,default=BASE/"verification/layout/placement.json")
    opt=ap.parse_args(); d=get_design();out=check(d)
    print(out['status'],out['parts'],dict(Counter(e["category"] for e in out["errors"])))
    opt.out.write_text(json.dumps(out,indent=2)+"\n")
    raise SystemExit(1 if out["errors"] else 0)
