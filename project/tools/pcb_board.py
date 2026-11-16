"""Create a native, paired EAGLE/Fusion PCB from verified placement and routed SES."""
from __future__ import annotations

from collections import Counter
from math import cos, sin, pi
import csv

from shapely.geometry import Point, LineString, box, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

from ecad_common import LIBRARY, add_packages, line, num, rotation, scaffold, tag, write_xml
from pcb_model import BASE, LAYOUT, get_design, read, write, body_shape, routing_fingerprint
from pcb_route import outline, net_width
from pcb_fusion_rules import apply_profile


def polygon_node(parent, coords, layer, width=0, **extra):
    elem=tag(parent,"polygon",width=num(width),layer=layer,**extra)
    for x,y in coords: tag(elem,"vertex",x=num(x),y=num(y))
    return elem


def disc_points(x,y,r,n=48):
    return [(x+r*cos(i*2*pi/n),y+r*sin(i*2*pi/n)) for i in range(n)]


def text_node(parent,value,x,y,layer=21,height=1,ratio=15,**other):
    el=tag(parent,"text",x=num(x),y=num(y),size=num(height),layer=layer,font="vector",ratio=ratio,**other)
    el.text=str(value)


def features(plain,design):
    boundary=outline(design)
    for p,q in zip(boundary,boundary[1:]+boundary[:1]): line(plain,*p,*q,0,20)
    for h in design.board_holes:
        tag(plain,"hole",x=num(h["x"]),y=num(h["y"]),drill=num(h["drill"]))
        # Screw head and washer land on bare laminate, with no surface copper
        # or through vias within the hardware envelope.
        # Four annular sectors leave the representable NPTH object itself
        # outside the keepout while excluding copper through the screw land.
        # This survives EAGLE→KiCad import, where holes become NPTH pads.
        ro = design.rules["mounting_keepout_radius"]
        ri = h["drill"]/2 + .04
        for q in range(4):
            angles = [(q + i/24)*pi/2 for i in range(25)]
            sector = [(h["x"]+ro*cos(a),h["y"]+ro*sin(a)) for a in angles]
            sector += [(h["x"]+ri*cos(a),h["y"]+ri*sin(a)) for a in reversed(angles)]
            for layer in (41,42,43):
                polygon_node(plain,sector,layer)
    for rx,ry in design.config["fiducials"]:
        polygon_node(plain,disc_points(rx,ry,0.50,96),1)
        polygon_node(plain,disc_points(rx,ry,1.00,96),29)
    for reg in design.keepouts:
        x1,y1,x2,y2=reg["rect"]
        vertices=[(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
        if reg.get("physical_clearance_only"):
            continue
        layers=reg.get("layers",[1,16])
        for l in layers:
            if reg.get("route_only"): continue
            polygon_node(plain,vertices,{1:41,16:42}[l])
        if set(layers)=={1,16} and not reg.get("route_only"):
            polygon_node(plain,vertices,43)


def add_rules(board,design):
    rules=tag(board,"designrules",name="ASTRA_JLC_STD_2L_1MM_ENIG")
    tag(rules,"description",language="en").text="2-layer FR4, finished 1 mm, 1 oz external copper, green LPI and ENIG; Standard PCBA. Regular vias 0.30 mm drill / 0.60 mm copper. See fabrication profile and independently opened CAM."
    data={
        "layerSetup":"(1*16)","mtCopper":" ".join(["0.035mm"]*16),
        "mtIsolate":" ".join(["0.93mm"]+["0.15mm"]*14),
        "mdWireWire":"0.15mm","mdWirePad":"0.15mm","mdWireVia":"0.15mm",
        "mdPadPad":"0.15mm","mdPadVia":"0.15mm","mdViaVia":"0.15mm",
        "mdSmdPad":"0.15mm","mdSmdVia":"0.15mm","mdSmdSmd":"0.15mm",
        "mdViaViaSameLayer":"0.15mm","mdCopperDimension":num(design.rules["edge_clearance"])+"mm",
        "mdDrill":"0.25mm","mdSmdStop":"0.05mm",
        "msWidth":"0.15mm","msDrill":"0.25mm","msMicroVia":"9.99mm",
        "rvPadTop":"0.25","rvPadInner":"0.25","rvPadBottom":"0.25",
        "rvViaOuter":"0.25","rvViaInner":"0.25",
        "rlMinPadTop":"0.20mm","rlMinPadInner":"0.20mm","rlMinPadBottom":"0.20mm",
        "rlMaxPadTop":"0.50mm","rlMaxPadInner":"0.50mm","rlMaxPadBottom":"0.50mm",
        "rlMinViaOuter":"0.125mm","rlMaxViaOuter":"0.30mm",
        "rlMinViaInner":"0.125mm","rlMaxViaInner":"0.30mm",
        "mvStopFrame":"1","mlMinStopFrame":"0.025mm","mlMaxStopFrame":"0.025mm",
        "mvCreamFrame":"0","mlMinCreamFrame":"0mm","mlMaxCreamFrame":"0mm",
        "mlViaStopLimit":"0.35mm","slThermalIsolate":"0.25mm",
        "slThermalsForVias":"0","checkAngle":"0","checkFont":"1","checkRestrict":"1",
        "useDiameter":"13","maxErrors":"999"
    }
    for name,v in data.items(): tag(rules,"param",name=name,value=v)
    apply_profile(rules)


def stitch_ground(d,route_data):
    """Seed through-ground stitching where both metal layers and holes are clear."""
    w,h=d.size
    blocked=[p["geom"].buffer(.21) for p in d.pads.values()]
    blocked += [body_shape(p,d.footprints[p["footprint"]]).buffer(.35) for p in d.parts if d.footprints[p["footprint"]].get("body")]
    for a in d.board_holes:
        blocked.append(Point(a["x"],a["y"]).buffer(d.rules["mounting_keepout_radius"]+.20))
    for a in d.package_holes:
        blocked.append(Point(a["x"],a["y"]).buffer(a["drill"]/2+.25))
    for x,y in d.config["fiducials"]: blocked.append(Point(x,y).buffer(1+.20))
    for reg in d.keepouts: blocked.append(box(*reg["rect"]).buffer(.30))
    for wi in route_data["wires"]:
        if len(wi["points"])>=2:
            blocked.append(LineString(wi["points"]).buffer(wi["width"]/2+.21))
    for v in route_data["vias"]: blocked.append(Point(v["x"],v["y"]).buffer(v["diameter"]/2+.25))
    occupied=STRtree(blocked)
    cands=[(x,y) for x in range(6,round(w)-2,8) for y in (1.65,h-1.65)]
    cands += [(x,y) for y in range(9,round(h)-2,8) for x in (1.65,w-1.65)]
    cands += [(x,y) for x in range(9,round(w)-3,13) for y in range(10,round(h)-3,13)]
    cands += [tuple(p) for p in d.config.get("stitch_candidates",[])]
    out=[]
    for x,y in cands:
        g=Point(x,y).buffer(d.rules["via_diameter"]/2)
        if occupied.query(g,predicate="intersects").size: continue
        if any((x-v["x"])**2+(y-v["y"])**2 < 1.20**2 for v in out): continue
        out.append(dict(net="GND",x=x,y=y,drill=d.rules["via_drill"],diameter=d.rules["via_diameter"],stitch=True))
    return out


def names(plain,d):
    board_outline=Polygon(outline(d,0.40))
    bounds=[p["geom"].buffer(.22) for p in d.pads.values()]
    bounds += [body_shape(p,d.footprints[p["footprint"]]).buffer(.25) for p in d.parts if d.footprints[p["footprint"]].get("body")]
    bounds += [Point(h["x"],h["y"]).buffer(d.rules["mounting_keepout_radius"]+.2) for h in d.board_holes]
    bounds += [Point(x,y).buffer(1.1) for x,y in d.config["fiducials"]]
    bounds += [box(*reg["rect"]) for reg in d.keepouts]
    bounds += [box(*r) for r in d.config.get("no_legend",[])]
    placed=[]
    left={}
    for note in d.config.get("legend",[]):
        label=note["text"]; x,y=note["xy"]; height=note.get("h",1)
        area=box(x-.17,y-.17,x+height*(.85*len(label)+.20),y+height+.2)
        if any(z.intersects(area) for z in bounds+placed): raise ValueError(f"fixed legend clashes with feature: {label}")
        placed.append(area); text_node(plain,label,x,y,height=height)
    # Prioritize labels needed for orientation at assembly, programming and bench test.
    def priority(part):
        r=part["ref"]
        if r.startswith(("J","TP","SW","BT","U","ANT")): return (0,r)
        if r.startswith(("Q","Y","D","L")): return (1,r)
        return (2,r)
    for p in sorted(d.parts,key=priority):
        ref=p["ref"]; f=d.footprints[p["footprint"]]
        x,y=p["x"],p["y"]
        nativebody=body_shape(p,f)
        lo,bo,hi,to=nativebody.bounds
        label=d.config.get("labels",{}).get(ref,ref)
        text_node(plain,ref,x,y,51,.52,11,align="center")
        th=1.2; tw=th*(.83*len(label)+.20)
        choice=[]
        for dist in (.40,1.5,2.6,3.7):
            choice.extend([(x-tw/2,to+dist),(x-tw/2,bo-dist-th),(hi+dist,y-th/2),(lo-dist-tw,y-th/2),
                           (hi+dist,to+dist),(lo-dist-tw,to+dist),(hi+dist,bo-dist-th),(lo-dist-tw,bo-dist-th)])
            if priority(p)[0]==2 and dist>=1.5: break
        for lx,ly in choice:
            area=box(lx-.13,ly-.13,lx+tw+.13,ly+th+.13)
            if board_outline.contains(area) and not any(z.intersects(area) for z in bounds+placed):
                text_node(plain,label,lx,ly,height=th)
                placed.append(area)
                break
        else: left[ref]=label
    return left


def main():
    d=get_design()
    if any(not any(p["block"]==b for p in d.parts) for b in d.config["blocks"]):
        raise RuntimeError("Board generation requires all four populated design blocks")
    route=read(LAYOUT/"routes.json")
    signature=route.get("source_geometry_sha256")
    if signature is not None and signature!=routing_fingerprint(d):
        raise ValueError("Routed geometry belongs to another placement or netlist. Regenerate the routing inputs.")
    stitches=stitch_ground(d,route)
    root,drawing=scaffold()
    root.set("version","9.7.0")
    board=tag(drawing,"board")
    plain=tag(board,"plain")
    features(plain,d)
    unprinted=names(plain,d)
    libs=tag(board,"libraries"); lib=tag(libs,"library",name=LIBRARY)
    used={p["footprint"] for p in d.parts}
    add_packages(lib,{n:d.footprints[n] for n in sorted(used)})
    tag(board,"attributes");tag(board,"variantdefs")
    classes=tag(board,"classes")
    tag(classes,"class",number="0",name="default",width="0",drill="0")
    tag(classes,"class",number="1",name="power",width=num(d.rules["power_width"]),drill="0")
    add_rules(board,d)
    tag(board,"autorouter")
    els=tag(board,"elements")
    for p in d.parts:
        el=tag(els,"element",name=p["ref"],library=LIBRARY,package=p["footprint"],value=p["value"],x=num(p["x"]),y=num(p["y"]),rot=rotation(p.get("rot",0)))
        for key,value in (("MPN",p.get("mpn")),("LCSC",p.get("lcsc"))):
            if value:
                tag(el,"attribute",name=key,value=value,x=num(p["x"]),y=num(p["y"]),size="1.27",layer=27,display="off")
    signals=tag(board,"signals")
    for n,contacts in sorted(d.nets.items()):
        net=tag(signals,"signal",name=n,**({"class":1} if net_width(d,n)==d.rules["power_width"] else {}))
        for ref,pad in contacts: tag(net,"contactref",element=ref,pad=pad)
        for w in route["wires"]:
            if w["net"]==n:
                for a,b in zip(w["points"],w["points"][1:]):
                    if a!=b: line(net,*a,*b,w["width"],w["layer"])
        for v in route["vias"]+stitches:
            if v["net"]==n:
                tag(net,"via",x=num(v["x"]),y=num(v["y"]),extent="1-16",drill=num(v["drill"]),diameter=num(v["diameter"]))
        if n=="GND":
            for layer in (1,16):
                # Account for the polygon contour stroke in the finished edge clearance.
                polygon_node(net,outline(d,d.rules["edge_clearance"]+.10),layer,.15,
                             isolate=num(d.rules["pour_isolation"]),thermals="no",orphans="no",rank="6")
            for x,y in d.config["fiducials"]:
                polygon_node(net,disc_points(x,y,1.16),1,.06,pour="cutout")
            # Give individual chip ground lands a defined, trace-fed soldering
            # neck. Exposed IC lands and switcher power returns retain solid ground.
            exempt={"C113","C114","C115","C116","C201","C202","R302"}
            for (ref,pin),item in d.pads.items():
                part=item["part"]
                if item["net"]!="GND" or ref in exempt or part["footprint"] not in ("C0402","R0402","C0603","R0603"):continue
                x1,y1,x2,y2=item["geom"].bounds
                gap=.20
                polygon_node(net,[(x1-gap,y1-gap),(x2+gap,y1-gap),(x2+gap,y2+gap),(x1-gap,y2+gap)],1,.035,pour="cutout")
            for region in d.config.get("pour_voids",[]):
                x1,y1,x2,y2=region["rect"]
                for layer in region.get("layers",[1,16]):
                    polygon_node(net,[(x1,y1),(x2,y1),(x2,y2),(x1,y2)],layer,.06,pour="cutout")
    write_xml(root,BASE/"board"/"astra.brd")
    write(BASE/"verification"/"layout"/"layout-summary.json",dict(board_size_mm=d.size,parts=len(d.parts),nets=len(d.nets),
          copper_wires=sum(len(w["points"])-1 for w in route["wires"]),routed_vias=len(route["vias"]),
          stitching_vias=len(stitches),omitted_silk_references=list(unprinted),board_holes=d.board_holes,
          legend_note="Each component has a centered designator on assembly layer 51. Surface legend omits labels without placement clearance."))
    print(f'{len(d.parts)} components, {len(d.nets)} nets, {len(stitches)} stitching vias, {len(unprinted)} designators only on assembly layer')

if __name__=="__main__":
    main()
