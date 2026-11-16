"""Export physical padstacks and protected routing to Specctra; import routed SES."""
from __future__ import annotations

import argparse
import math
import re
from collections import defaultdict
from pathlib import Path
from shapely.geometry import Point, Polygon, box

from pcb_model import BASE, LAYOUT, LAYERS, get_design, read, write, rotate, rect_poly, routing_fingerprint


def um(mm):
    return format(round(1000 * float(mm), 3), "g") if abs(float(mm))<100 else f"{1000*float(mm):.3f}".rstrip("0").rstrip(".")


def num(mm):
    return f"{float(mm):.6f}".rstrip("0").rstrip(".") or "0"


def dq(name):
    s=str(name)
    if '"' in s: raise ValueError(f"double quote in identifier {s}")
    return '"'+s+'"'


def path_coords(pts):
    return " ".join(f"{um(x)} {um(y)}" for x,y in pts)


def outline(design, inset=0.0):
    w,h=design.size
    d=design.config["outline_chamfer"]
    # Offset every side inward by exactly inset, including diagonal corners.
    stop=d+inset*(math.sqrt(2)-1)
    return [(stop,inset),(w-stop,inset),(w-inset,stop),(w-inset,h-stop),
            (w-stop,h-inset),(stop,h-inset),(inset,h-stop),(inset,stop)]


def net_width(design,net):
    override=design.config.get("widths",{}).get(net)
    if override: return float(override)
    if net in {"VBAT","VBUS","SYS_AON","VMAIN","PV_IN","SOLAR_IN","USB5V"}:
        return design.rules["power_width"]
    return design.rules["default_width"]


def region_shape(layer, rect):
    return f"(rect {layer} {' '.join(um(t) for t in rect)})"


def make_dsn(design):
    rules=design.rules
    shapes, padstacks, pad_names = {}, [], {}
    def padstack(item,offset):
        pd=item["pad"]
        part=item["part"]
        a = (float(pd.get("rot",0))+part.get("rot",0))%180
        w,h=float(pd.get("w")),float(pd.get("h"))
        top_and_bottom=bool(pd.get("drill"))
        is_round=(pd.get("roundness",0)==100 or pd.get("shape") in ("round","circle") or (top_and_bottom and pd.get("shape","round")=="round")) and abs(w-h)<1e-6
        # Conservative orthogonal rectangle encloses rounded-corner lands, making
        # the routing obstacle at least as large as the native copper.
        if abs(a-90)<1e-5: a,w,h=0,h,w
        if is_round: a=0
        rounding=float(pd.get("roundness",100 if is_round else 0))
        ox,oy=offset
        key=(round(w,6),round(h,6),round(a,6),top_and_bottom,is_round,rounding,ox,oy)
        if key in shapes: return shapes[key]
        pname="PS"+str(len(shapes)+1)
        shapes[key]=pname
        ll=[1,16] if top_and_bottom else [pd.get("layer",1)]
        def shape(layer):
            if is_round: return f"(circle {layer} {um(w)} {um(-ox)} {um(-oy)})"
            if rounding:
                geo=rect_poly(0,0,w,h,a,rounding)
                # Use rounded land geometry. A near-rectangular proxy creates
                # spurious corner violations on tightly spaced 0402 components.
                pts=list(geo.simplify(.001, preserve_topology=True).exterior.coords)[:-1]
                return f"(polygon {layer} 0 {path_coords([(x-ox,y-oy) for x,y in pts])})"
            if a==0: return region_shape(layer,[-w/2-ox,-h/2-oy,w/2-ox,h/2-oy])
            pts=[rotate(x,y,a) for x,y in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
            return f"(polygon {layer} 0 {path_coords([(x-ox,y-oy) for x,y in pts])})"
        ps=' '.join(f"(shape {shape(LAYERS[l])})" for l in ll)
        padstacks.append(f"    (padstack {pname} {ps} (attach off))")
        return pname

    name="astra"
    body=[f"(pcb {name}",'  (parser (string_quote ") (space_in_quoted_tokens on) (host_cad "ASTRA") (host_version "1"))',
          "  (resolution um 10)","  (unit um)","  (structure",
          "    (layer F.Cu (type signal) (property (index 0)))","    (layer B.Cu (type signal) (property (index 1)))"]
    contour=outline(design,rules["edge_clearance"])
    body.append(f"    (boundary (path pcb 0 {path_coords(contour+[contour[0]])}))")
    def circle_keep(name,x,y,dia,kind="keepout"):
        for layer in LAYERS.values():
            body.append(f"    ({kind} {dq(name)} (circle {layer} {um(dia)} {um(x)} {um(y)}))")
    for h in design.board_holes:
        circle_keep("mount",h["x"],h["y"],2*rules["mounting_keepout_radius"])
    for h in design.package_holes:
        circle_keep(h["owner"]+"_NPTH",h["x"],h["y"],h["drill"]+0.5)
    for x,y in design.config["fiducials"]:
        circle_keep("fiducial",x,y,2)
    for reg in design.keepouts:
        for l in reg.get("layers",[1,16]):
            body.append(f"    (keepout {dq(reg.get('name','keepout'))} {region_shape(LAYERS[l],reg['rect'])})")
    if design.config.get("bottom_ground") or design.config.get("strict_returns"):
        # A pour can be crossed by a signal in the router; the real copper
        # contour is recomputed by EAGLE and independently by CAM after routing.
        ground=Polygon(contour)
        for reg in design.keepouts:
            if 16 in reg.get("layers",[1,16]) and not reg.get("physical_clearance_only"):
                ground=ground.difference(box(*reg['rect']))
        for h in design.board_holes:
            ground=ground.difference(Point(h['x'],h['y']).buffer(rules['mounting_keepout_radius'],quad_segs=8))
        windows=[f"(window (polygon B.Cu 0 {path_coords(list(h.coords)[:-1])}))" for h in ground.interiors]
        if design.config.get("bottom_ground"):
            body.append(f"    (plane GND (polygon B.Cu 0 {path_coords(list(ground.exterior.coords)[:-1])}) {' '.join(windows)})")
        if design.config.get("top_ground"):
            ground=Polygon(contour)
            for reg in design.keepouts+design.config.get("pour_voids",[]):
                if 1 in reg.get("layers",[1,16]) and not reg.get("physical_clearance_only"):
                    ground=ground.difference(box(*reg['rect']))
            for h in design.board_holes:
                ground=ground.difference(Point(h['x'],h['y']).buffer(rules['mounting_keepout_radius'],quad_segs=8))
            for x,y in design.config["fiducials"]:
                ground=ground.difference(Point(x,y).buffer(1.16,quad_segs=8))
            windows=[f"(window (polygon F.Cu 0 {path_coords(list(h.coords)[:-1])}))" for h in ground.interiors]
            body.append(f"    (plane GND (polygon F.Cu 0 {path_coords(list(ground.exterior.coords)[:-1])}) {' '.join(windows)})")

        for reg in design.planes:
            # Guard the RF, crystal and switching return areas against bottom
            # signal routing. Open individual sockets only for designed returns.
            x1,y1,x2,y2=reg["rect"]
            boxes=[(x1,y1,x2,y2)]
            margin=.20
            for v in design.fixed_vias:
                if v["net"]!=reg.get("net","GND"):continue
                r=v.get("diameter",rules["via_diameter"])/2+margin
                ax,ay,bx,by=v['x']-r,v['y']-r,v['x']+r,v['y']+r
                new=[]
                for xlo,ylo,xhi,yhi in boxes:
                    if ax>=xhi or bx<=xlo or ay>=yhi or by<=ylo:
                        new.append((xlo,ylo,xhi,yhi));continue
                    for rr in ((xlo,ylo,min(ax,xhi),yhi),(max(bx,xlo),ylo,xhi,yhi),
                               (max(ax,xlo),ylo,min(bx,xhi),min(ay,yhi)),(max(ax,xlo),max(by,ylo),min(bx,xhi),yhi)):
                        if rr[2]-rr[0]>.01 and rr[3]-rr[1]>.01:new.append(rr)
                boxes=new
            for j,rr in enumerate(boxes):
                body.append(f"    (keepout {dq(reg['name']+str(j))} {region_shape('B.Cu',rr)})")
    else:
        for reg in design.planes:
            for l in reg.get("layers",[16]):
                x1,y1,x2,y2=reg["rect"]
                body.append(f"    (plane {dq(reg.get('net','GND'))} (polygon {LAYERS[l]} 0 {path_coords([(x1,y1),(x2,y1),(x2,y2),(x1,y2)])}))")
    via_by_size = {(rules["via_diameter"],rules["via_drill"]):"VIA_DEFAULT"}
    for v in design.fixed_vias:
        pair=(v.get("diameter",rules["via_diameter"]),v.get("drill",rules["via_drill"]))
        via_by_size.setdefault(pair,"VIA_"+str(len(via_by_size)+1))
    # Additional fixed via sizes are valid only for supplied vias; the router
    # uses VIA_DEFAULT throughout (0.30 mm standard mechanical drill).
    body.extend(["    (via "+" ".join(via_by_size.values())+")",
                 f"    (rule (width {um(rules['default_width'])}) (clearance {um(rules['route_clearance'])}) (clearance {um(rules['smd_clearance'])} (type smd_smd)))",
                 "  )","  (placement"])
    images=[]
    # Flatten each component into the physical, rotated package to preserve
    # custom pad rotations and signed insertion transforms without heuristics.
    for p in design.parts:
        ref=p["ref"]
        body.append(f"    (component {dq('FOOT_'+ref)} (place {dq(ref)} {um(p['x'])} {um(p['y'])} front 0))")
        im=[f"    (image {dq('FOOT_'+ref)}"]
        for (r,n),item in design.pads.items():
            if r!=ref: continue
            cx,cy=item["center"]
            offset=design.config.get("route_anchors",{}).get(ref+"."+n,[0.,0.])
            im.append(f"      (pin {padstack(item,offset)} {dq(n)} {um(cx+offset[0]-p['x'])} {um(cy+offset[1]-p['y'])})")
        im.append("    )")
        images.extend(im)
    body.extend(["  )","  (library",*images,*padstacks])
    for (dia,drill),name in via_by_size.items():
        body.append(f"    (padstack {name} (shape (circle F.Cu {um(dia)})) (shape (circle B.Cu {um(dia)})) (attach off))")
    body.extend(["  )","  (network"])
    classes=defaultdict(list)
    for net,contacts in sorted(design.nets.items()):
        names=" ".join(f"{r}-{n}" for r,n in contacts)
        body.append(f"    (net {dq(net)} (pins {names}))")
        classes[(net_width(design,net),net=="GND" and design.config.get("ground_by_pour",False))].append(net)
    for (width,plane_class),nets in sorted(classes.items()):
        names=" ".join(dq(n) for n in nets)
        label="GND_POUR" if plane_class else "width_"+um(width)
        body.append(f"    (class {label} {names} (circuit (use_via VIA_DEFAULT)) (rule (width {um(width)})))")
    body.extend(["  )","  (wiring"])
    for w in design.fixed_wires:
        for a,b in zip(w['points'],w['points'][1:]):
            body.append(f"    (wire (path {LAYERS[w.get('layer',1)]} {um(w['width'])} {path_coords((a,b))}) (net {dq(w['net'])}) (type protect))")
    for v in design.fixed_vias:
        ps=via_by_size[(v.get("diameter",rules["via_diameter"]),v.get("drill",rules["via_drill"]))]
        body.append(f"    (via {ps} {um(v['x'])} {um(v['y'])} (net {dq(v['net'])}) (type protect))")
    body.extend(["  )",")"])
    out=LAYOUT/"astra.dsn"
    out.write_text("\n".join(body)+"\n")
    (LAYOUT/"source-geometry.sha256").write_text(routing_fingerprint(design)+"\n")
    write(LAYOUT/"via-stacks.json",{name:{"diameter":d,"drill":h} for (d,h),name in via_by_size.items()})
    return out


def parse_sexpr(filename):
    # Session output has an ordinary atom grammar and double-quoted net names.
    tokens=re.findall(r'\(|\)|"[^"]*"|[^\s()]+',Path(filename).read_text())
    stack=[[]]
    for t in tokens:
        if t=='(':
            v=[]; stack[-1].append(v); stack.append(v)
        elif t==')': stack.pop()
        else: stack[-1].append(t.strip('"'))
    if len(stack)!=1: raise ValueError("incomplete SES file")
    return stack[0][0]


def sub(node,key):
    return [v for v in node if isinstance(v,list) and v[0]==key]


def import_ses(filename,via_stacks):
    data=parse_sexpr(filename)
    routes=sub(data,"routes")[0]
    unit,denom=sub(routes,"resolution")[0][1:]
    units={"mm":1,"um":.001,"mil":.0254,"inch":25.4}
    scale=units[unit]/float(denom)
    def mm(n): return round(float(n)*scale,6)
    wires,vias=[],[]
    for net in sub(sub(routes,"network_out")[0],"net"):
        name=net[1]
        for w in sub(net,"wire"):
            pat=sub(w,"path")
            if not pat: raise ValueError(f"unsupported wire form: {w}")
            _,l,width,*xy=pat[0]
            wires.append(dict(net=name,layer={v:k for k,v in LAYERS.items()}[l],width=mm(width),
                              points=[(mm(x),mm(y)) for x,y in zip(xy[::2],xy[1::2])],protected=bool(sub(w,"type"))))
        for v in sub(net,"via"):
            _,stack,x,y,*rest=v
            vias.append(dict(net=name,x=mm(x),y=mm(y),**via_stacks[stack]))
    # A pre-placed escape via can become redundant when the router attaches
    # the complete connection on F.Cu. GND vias connect both plane fills.
    sides=defaultdict(set)
    for wire in wires:
        for x,y in wire["points"]:
            sides[(wire["net"],x,y)].add(wire["layer"])
    vias=[via for via in vias if via['net']=='GND' or
          len(sides[(via['net'],via['x'],via['y'])])==2]
    return {"wires":wires,"vias":vias}


def export_session(design, routes, destination):
    """Write the fully edited Specctra session using 1 nm integer coordinates."""
    def ordinate(mm):
        return str(round(mm*1_000_000))
    lines = ['(session astra','  (base_design astra)','  (placement (resolution um 1000)']
    for part in design.parts:
        lines.append('    (component '+dq('FOOT_'+part['ref'])+' (place '+dq(part['ref'])+' '+
                     ordinate(part['x'])+' '+ordinate(part['y'])+' front 0))')
    lines += ['  )','  (routes (resolution um 1000)',
              '    (parser (host_cad ASTRA) (host_version "1"))','    (library_out']
    stacks=read(LAYOUT/'via-stacks.json')
    lookup={(v['diameter'],v['drill']):key for key,v in stacks.items()}
    for key,v in stacks.items():
        size=ordinate(v['diameter'])
        lines.append('      (padstack '+dq(key)+' (shape (circle F.Cu '+size+
                     ' 0 0)) (shape (circle B.Cu '+size+' 0 0)) (attach off))')
    lines += ['    )','    (network_out']
    for net in sorted(design.nets):
        lines.append('      (net '+dq(net))
        for w in routes['wires']:
            if w['net']!=net:
                continue
            coords=' '.join(ordinate(value) for point in w['points'] for value in point)
            protected=' (type protect)' if w.get('protected') else ''
            lines.append('        (wire (path '+LAYERS[w['layer']]+' '+ordinate(w['width'])+
                         ' '+coords+')'+protected+')')
        for v in routes['vias']:
            if v['net']==net:
                ps=lookup[v['diameter'],v['drill']]
                lines.append('        (via '+dq(ps)+' '+ordinate(v['x'])+' '+ordinate(v['y'])+')')
        lines.append('      )')
    lines += ['    )','  )',')']
    destination.write_text('\n'.join(lines)+'\n')


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("job",choices=["dsn","ses","export"])
    ap.add_argument("--session",type=Path,default=LAYOUT/"astra.ses")
    args=ap.parse_args()
    if args.job=="dsn":
        print(make_dsn(get_design()))
    elif args.job=="export":
        export_session(get_design(),read(LAYOUT/"routes.json"),args.session)
    else:
        routed=import_ses(args.session,read(LAYOUT/"via-stacks.json"))
        routed["source_geometry_sha256"]=(LAYOUT/"source-geometry.sha256").read_text().strip()
        write(LAYOUT/"routes.json",routed)
        print(f"{len(routed['wires'])} routed paths and {len(routed['vias'])} vias")
