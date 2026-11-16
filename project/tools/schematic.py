"""Generate the editable Fusion Electronics schematic and its local library."""
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from xml.etree import ElementTree as ET

from ecad_common import ROOT, LIBRARY, add_packages, box, line, load_design, num, scaffold, tag, write_xml

G = 2.54
WIDTH, HEIGHT = 160*G, 108*G
MANUAL = {
    ("power","Protected cell charger"): "charger-schematic.json",
    ("power","Solar MPPT"): "solar-schematic.json",
    ("display","Bipolar boost"): "display-boost-schematic.json",
    ("wake","Wake timer"): "timer-schematic.json",
    ("wake","Clock and alarm"): "rtc-schematic.json",
    ("power","Switched 3.3 V"): "regulator-schematic.json",
}
BLOCK_TITLES = {
    "power": ("Energy harvesting and power path", "Solar and USB-C input, protected cell, charge control and switched supply"),
    "radio": ("Radio and programming", "2.4 GHz radio, host connections and SWD access"),
    "display": ("Electrophoretic display", "24-contact panel interface, switched boost loop and panel bias supplies"),
    "wake": ("Timekeeping, sensing and controls", "Always-on wake logic, alarm, environmental sensor and battery measurement"),
}


def natural(s):
    return [(0, int(k)) if k.isdigit() else (1, k) for k in re.findall(r'\d+|\D+', str(s))]


def ascii_name(s):
    return re.sub(r'[^A-Za-z0-9_./+!-]', '_', str(s)).strip('_') or "P"


def label_text(parent, value, x, y, size, layer, align=None):
    item = tag(parent, "text", x=num(x), y=num(y), size=num(size), layer=layer, font="proportional",
               align=align)
    item.text = value
    return item


@dataclass
class Pin:
    pad: str
    name: str
    direction: str
    x: float = 0
    y: float = 0
    side: int = -1
    contacts: tuple = ()


@dataclass
class Device:
    name: str
    prefix: str
    footprint: str
    style: str
    pins: list
    width: float = 0
    halfheight: float = 0
    top: float = 0
    bottom: float = 0


def get_device(part, fp):
    ref = part["ref"]
    prefix = re.match(r'[A-Za-z]+', ref).group().upper()
    names = {str(k): str(v) for k,v in part.get("pin_names", {}).items()}
    types = {str(k): str(v) for k,v in part.get("pin_types", {}).items()}
    pad_ids = [str(p["n"]) for p in fp["pads"]]
    if len(set(pad_ids)) != len(pad_ids):
        raise ValueError(f"Repeated pad number on {part['footprint']}")
    if not (set(names) | set(types) | set(part["pins"])).issubset(pad_ids):
        raise ValueError(f"Pin table mismatch on {ref}: {(set(names)|set(types)|set(part['pins']))-set(pad_ids)}")
    # Copper-only hold-downs without a logical pin stay in the physical footprint.
    active_pads = [n for n in sorted(pad_ids,key=natural) if n in names or n in part["pins"]]
    style = "block"
    if len(active_pads) == 2 and prefix in ("R","C","L","D","F","FB","Y","X"):
        style = prefix
    elif len(active_pads) == 1 and prefix.startswith("TP"):
        style = "tp"
    pins, used = [], Counter()
    for pad in active_pads:
        raw = ascii_name(names.get(pad, pad))
        used[raw.upper()] += 1
        unique = raw if used[raw.upper()] == 1 else raw + "@" + ascii_name(pad)
        # EAGLE treats names case-insensitively and permits disambiguation with @.
        pins.append(Pin(pad, unique, types.get(pad, "pas")))
    # These are duplicated bond-outs of a single output in the manufacturers'
    # pin tables. Fusion's route=all requires every physical contact to reach copper.
    parallel_outputs={"TPS2116DRLR":("VOUT","2","7"),"BQ24074RGTR":("OUT","10","11"),
                      "RT6160AWSC":("VOUT","E2","E3")}
    if part.get("mpn") in parallel_outputs:
        name, first, second=parallel_outputs[part["mpn"]]
        a,b=(next(p for p in pins if p.pad==pad) for pad in (first,second))
        if a.direction!="out" or b.direction!="out" or part["pins"][first]!=part["pins"][second]:
            raise ValueError(f"Inconsistent duplicate output pads on {ref}")
        a.name=name;a.contacts=(first,second);pins.remove(b)
    if style != "block":
        name = prefix + "_" + ascii_name(part["footprint"])
    else:
        name = ascii_name(part.get("mpn") or part["footprint"])
    dev = Device(name,prefix,part["footprint"],style,pins)
    if style == "block":
        # Retain pad order for connectors, modules and packages: adjacent numbered pins
        # are easy to compare with the package table. Ground and power duplicates remain visible.
        half = (len(pins)+1)//2
        longest = max((len(p.name.split("@")[0]) for p in pins), default=4)
        dhalf = max(4, math.ceil((longest*1.55+3.5)/G))*G
        dev.width=2*dhalf
        dev.halfheight=max(2, half)*G
        for idx,pin in enumerate(pins):
            side = -1 if idx<half else 1
            i=idx if idx<half else idx-half
            pin.x=side*(dhalf+G)
            pin.y=(half-1-2*i)*G
            pin.side=side
        dev.top=dev.halfheight+4*G
        dev.bottom=dev.halfheight+2*G
    else:
        for i,pin in enumerate(pins):
            pin.side=-1 if i == 0 else 1
            pin.x=pin.side*3*G
        dev.top=2.8*G
        dev.bottom=2.2*G
    return dev


def make_symbol(symbols, devicesets, dev):
    symbol=tag(symbols,"symbol",name=dev.name)
    for p in dev.pins:
        tag(symbol,"pin",name=p.name,x=num(p.x),y=num(p.y),length="short",direction=p.direction,
            visible="both" if dev.style=="block" else "off",rot="R0" if p.side<0 else "R180")
    if dev.style=="block":
        box(symbol,0,0,dev.width,2*dev.halfheight,0.254,94)
        label_text(symbol,">NAME",-dev.width/2,dev.halfheight+1.6*G,2.25,95)
        label_text(symbol,">VALUE",-dev.width/2,dev.halfheight+.22*G,1.7,96)
    else:
        def glyph(a,b,c,d):
            line(symbol,a,b,c,d,.254,94)
        st=dev.style
        # Standard horizontal IEC symbols. The short native pins terminate at x = +/-5.08.
        if st=="C":
            for s in (-1,1):
                glyph(s*2*G,0,s*.46,0)
                glyph(s*.46,-1.65,s*.46,1.65)
        elif st=="D":
            anode_left=dev.pins[0].name.split("@")[0].upper() in ("A","ANODE")
            if not anode_left and dev.pins[1].name.split("@")[0].upper() not in ("A","ANODE"):
                raise ValueError(f"No A/K mapping for diode {dev.name}")
            s=1 if anode_left else -1
            glyph(-2*G,0,-1.2,0); glyph(1.2,0,2*G,0)
            glyph(-1.2*s,-1.55,-1.2*s,1.55)
            glyph(-1.2*s,1.55,1.2*s,0); glyph(1.2*s,0,-1.2*s,-1.55)
            glyph(1.2*s,1.55,1.2*s,-1.55)
            label_text(symbol,"K",1.55*s,-1.4*G,1.2,94)
        elif st in ("L","FB"):
            glyph(-2*G,0,-3,0); glyph(3,0,2*G,0)
            for i in range(4):
                line(symbol,-3+i*1.5,0,-1.5+i*1.5,0,.254,94,curve="-180")
        elif st in ("Y","X"):
            for s in (-1,1):
                glyph(s*2*G,0,s*1.9,0);glyph(s*1.9,-1.6,s*1.9,1.6)
            box(symbol,0,0,1.65,3.6,.254,94)
        elif st=="tp":
            glyph(-2*G,0,-.9,0)
            tag(symbol,"circle",x="0",y="0",radius=".9",width=".254",layer="94")
        else:
            glyph(-2*G,0,-2.25,0); glyph(2.25,0,2*G,0)
            box(symbol,0,0,4.5,1.75,.254,94)
        label_text(symbol,">NAME",0,1.12*G,1.8,95,"bottom-center")
        label_text(symbol,">VALUE",0,-.85*G,1.5,96,"top-center")
    ds=tag(devicesets,"deviceset",name=dev.name,prefix=dev.prefix,uservalue="yes")
    tag(tag(ds,"gates"),"gate",name="G$1",symbol=dev.name,x="0",y="0")
    variant=tag(tag(ds,"devices"),"device",name="",package=dev.footprint)
    connects=tag(variant,"connects")
    for p in dev.pins:
        tag(connects,"connect",gate="G$1",pin=p.name,pad=" ".join(p.contacts) if p.contacts else p.pad,
            route="all" if p.contacts else None)
    tag(tag(variant,"technologies"),"technology",name="")


@dataclass
class Stub:
    part: str
    pin: str
    net: str
    outer: tuple
    inner: tuple
    label: tuple
    links: list = field(default_factory=list)


def sheet_wiring(sheet,stubs,power_nets):
    nets=tag(sheet,"nets")
    by_net=defaultdict(list)
    for i,s in enumerate(stubs):
        by_net[s.net].append(i)
    for name,items in sorted(by_net.items()):
        net=tag(nets,"net",name=name,**{"class":"1" if name in power_nets else "0"})
        unseen=set(items)
        while unseen:
            initial=min(unseen)
            group,queue=[],[initial]
            while queue:
                n=queue.pop()
                if n in unseen:
                    unseen.remove(n);group.append(n);queue.extend(stubs[n].links)
            seg=tag(net,"segment")
            for idx in group:
                s=stubs[idx]
                tag(seg,"pinref",part=s.part,gate="G$1",pin=s.pin)
                line(seg,*s.inner,*s.outer,.1524,91)
                for other in s.links:
                    if idx<other:
                        line(seg,*s.outer,*stubs[other].outer,.1524,91)
                if len(s.links)>1:
                    tag(seg,"junction",x=num(s.outer[0]),y=num(s.outer[1]))
            # Place the label at an actual wire point, on the first branch of a common rail.
            s=stubs[min(group)]
            tag(seg,"label",x=num(s.label[0]),y=num(s.label[1]),size="1.55",layer="95")
    return nets


def instance(instances, symbols, part, device, x, y, angle=0, text_positions=None):
    inst=tag(instances,"instance",part=part["ref"],gate="G$1",x=num(x),y=num(y),
             rot="R"+str(angle),smashed="yes")
    sym=next(s for s in symbols if s.get("name")==device.name)
    for t in sym.findall("text"):
        if t.text not in (">NAME",">VALUE"): continue
        key=t.text[1:]
        attrs=dict(t.attrib)
        attrs.update(x=num(x+float(attrs["x"])),y=num(y+float(attrs["y"])),rot="R0")
        if text_positions and key.lower() in text_positions:
            at=text_positions[key.lower()]
            attrs.update(x=num(at[0]),y=num(at[1]),align="bottom-left")
        tag(inst,"attribute",name=key,**attrs)


def draw_circuit(spec, origin, parts, devices, symbols, instances, nets, power_nets):
    """Place explicitly drafted circuits; derive native pinrefs from real wire endpoints."""
    def world(x,y):
        return round(origin[0]+G*x,5),round(origin[1]+G*y,5)
    nodes=defaultdict(lambda:defaultdict(list))
    for ref,(x,y,angle) in spec["instances"].items():
        part,dev=parts[ref],devices[ref]
        text_pos={k:world(*v) for k,v in spec.get("text_positions",{}).get(ref,{}).items()}
        instance(instances,symbols,part,dev,*world(x,y),angle,text_pos)
        rad=math.radians(angle)
        for p in dev.pins:
            if not part["pins"].get(p.pad):continue
            px=p.x/G;py=p.y/G
            at=(round(x+px*math.cos(rad)-py*math.sin(rad),5),round(y+px*math.sin(rad)+py*math.cos(rad),5))
            nodes[part["pins"][p.pad]][at].append((ref,p.name))
    if set(nodes)!=set(spec["netlines"]): raise ValueError("Drafted net set differs from pin table")
    for name, lines in spec["netlines"].items():
        net=next((n for n in nets if n.get("name")==name),None)
        if net is None:net=tag(nets,"net",name=name,**{"class":"1" if name in power_nets else "0"})
        adjacency=defaultdict(set)
        for x1,y1,x2,y2 in lines:
            a,b=(x1,y1),(x2,y2)
            adjacency[a].add(b);adjacency[b].add(a)
        missing=set(nodes[name])-set(adjacency)
        if missing:raise ValueError(f"Unwired {name} pin(s) in manual draft: {missing}")
        labels=spec.get("labels",{}).get(name,[])
        if labels and not isinstance(labels[0],list):labels=[labels]
        unseen=set(adjacency)
        while unseen:
            component=set();pending=[min(unseen)]
            while pending:
                at=pending.pop()
                if at in unseen:
                    unseen.remove(at);component.add(at);pending.extend(adjacency[at])
            seg=tag(net,"segment")
            for at in sorted(component):
                for ref,pin in nodes[name].get(at,[]):
                    tag(seg,"pinref",part=ref,gate="G$1",pin=pin)
                for other in sorted(adjacency[at]):
                    if at<other:line(seg,*world(*at),*world(*other),.1524,91)
                if len(adjacency[at])+len(nodes[name].get(at,[]))>2:
                    tag(seg,"junction",x=num(world(*at)[0]),y=num(world(*at)[1]))
            anchors=[at for at in labels if tuple(at) in component]
            if not anchors: raise ValueError(f"Unlabelled {name} segment in drafted circuit")
            for at in anchors:
                lx,ly=world(*at);tag(seg,"label",x=num(lx),y=num(ly),size="1.55",layer="95")


def page_layout(parts,devs):
    pages=[]
    top=95*G; bottom=6*G
    for block in BLOCK_TITLES:
        rows=[p for p in parts if p["block"]==block]
        groups=defaultdict(list)
        for p in rows:
            groups[p.get("function") or BLOCK_TITLES[block][0]].append(p)
        if not groups: continue
        block_pages=[]
        def new_page():
            page={"block":block,"groups":[],"items":[],"manual":[],"levels":[top,top,top]}
            pages.append(page);block_pages.append(page)
            return page
        new_page()
        for title,items in groups.items():
            manual=MANUAL.get((block,title))
            if manual and (ROOT/"hardware"/manual).exists():
                spec=json.loads((ROOT/"hardware"/manual).read_text())
                if set(spec["instances"])!={p["ref"] for p in items}:raise ValueError(f"Incomplete {manual}")
                height=spec.get("height",max(max(y for x,y,a in spec["instances"].values())+7,
                           max(max(l[1],l[3]) for lines in spec["netlines"].values() for l in lines)+4))
                slots=[(page,c,y) for page in block_pages for c,y in enumerate(page["levels"])
                       if y-bottom>=(height+3)*G]
                page,col,y=min(slots,key=lambda a:a[2]) if slots else (new_page(),0,top)
                x=(27+col*53)*G
                page["groups"].append((x,y,title))
                oy=G*math.floor(y/G-height-2+1e-6)
                page["manual"].append((spec,(x-24*G,oy),title))
                page["levels"][col]=oy-2*G
                continue
            def order(p):
                d=devs[p["ref"]]
                if d.style=="block": return (0, -len(d.pins), natural(p["ref"]))
                if d.style=="tp": return (2, "",natural(p["ref"]))
                return (1, tuple(p["pins"].values()),natural(p["ref"]))
            remaining=sorted(items,key=order)
            while remaining:
                total=sum(math.ceil(devs[p["ref"]].top/G)*G+devs[p["ref"]].bottom+G for p in remaining)+5*G
                first=devs[remaining[0]["ref"]]
                min_room=math.ceil(first.top/G)*G+first.bottom+4*G
                slots=[(page,c,y) for page in block_pages for c,y in enumerate(page["levels"])]
                fits=[slot for slot in slots if slot[2]-bottom >= total-1e-6]
                useful=[slot for slot in slots if slot[2]-bottom >= min_room-1e-6]
                if fits:
                    page,col,y=min(fits,key=lambda a:a[2])
                elif useful:
                    page,col,y=max(useful,key=lambda a:a[2])
                else:
                    page,col,y=new_page(),0,top
                x=(27+col*53)*G
                page["groups"].append((x,y,title));y-=4*G
                count=0
                while remaining:
                    p=remaining[0];d=devs[p["ref"]]
                    anchor=math.floor((y-d.top)/G+1e-6)*G
                    if anchor-d.bottom < bottom-1e-6: break
                    page["items"].append((p,x,anchor,col,title))
                    y=anchor-d.bottom-G;remaining.pop(0);count+=1
                if count==0: raise ValueError(f"Symbol exceeds sheet space: {remaining[0]['ref']}")
                page["levels"][col]=y-2*G
    return pages


def overview(sheets, pages):
    """An unambiguous reading map for the multi-sheet net labels and power domains."""
    sheet=tag(sheets,"sheet")
    tag(sheet,"description").text="System architecture and design index"
    plain=tag(sheet,"plain")
    box(plain,WIDTH/2,HEIGHT/2,WIDTH,HEIGHT,.25,97)
    def caption(s,x,y,h=1.9): label_text(plain,s,x,y,h,97)
    def group(x,y,w,h,title,detail):
        box(plain,x+w/2,y+h/2,w,h,.25,97)
        caption(title,x+3,y+h-6,2.2)
        for j,t in enumerate(detail):caption(t,x+3,y+h-12-4.2*j,1.72)
    def flow(points):
        for a,b in zip(points,points[1:]):line(plain,*a,*b,.32,97)
        a,b=points[-2:]
        dx,dy=b[0]-a[0],b[1]-a[1];d=math.hypot(dx,dy);u,v=dx/d,dy/d
        for side in (-1,1):line(plain,*b,b[0]-2.4*u-side*v,b[1]-2.4*v+side*u,.32,97)
    caption("ASTRA   /   ENGINEERING SCHEMATIC",8,264,1.9)
    caption("Solar e-ink weather station",8,251,5.1)
    caption("System architecture",8,241,2.7)
    caption("PROTOTYPE  A",350,264,1.9)
    line(plain,8,236,WIDTH-8,236,.2,97)
    group(9,198,60,26,"Solar input",["5 V / 230 mA at MPP","J103 wire lands"])
    group(9,156,60,26,"USB-C input",["5 V sink, two Rd resistors","J101 charge input"])
    group(86,198,67,26,"SPV1050",["PV tracking and storage","PV_VALID to source switch"])
    group(171,171,64,27,"TPS2116",["Priority source selection","USB priority"])
    group(250,171,65,27,"BQ24074",["Power path and charging","Pack NTC window"])
    group(330,171,66,27,"Protected LiPo",["250 mAh / 1S","J102 keyed 3-wire pack"])
    flow([(69,211),(86,211)]);flow([(153,211),(162,211),(162,191),(171,191)])
    flow([(69,168),(161,168),(161,179),(171,179)])
    flow([(235,184),(250,184)]);flow([(315,187),(330,187)]);flow([(330,178),(315,178)])
    group(246,118,70,28,"RT6160A",["Switched 3.3 V VMAIN","Enable = MAIN_EN"])
    group(121,118,79,28,"Always-on domain",["TPS7A02, PCF85063A, TPL5111","Alarm or pushbutton starts VMAIN"])
    flow([(282,171),(282,146)])
    flow([(282,157),(160,157),(160,146)])
    flow([(200,129),(246,129)])
    caption("SYS_AON",201,158,1.8);caption("MAIN_EN",211,131,1.8)
    group(80,66,76,29,"BME280 and controls",["I2C 0x76, three button inputs","Switched battery measurement"])
    group(203,66,82,29,"Ebyte E73 module",["nRF54L15-QFAA, 2.4 GHz","Retained RRAM journal and SWD"])
    group(323,66,73,29,"Waveshare 4.2 V2",["SSD1683, 400 x 300, FPC24","Switched bias pump and SPI"])
    flow([(256,118),(256,95)])
    flow([(156,82),(203,82)]);flow([(285,82),(323,82)])
    caption("SDA / SCL",164,84,1.7);caption("4-wire SPI",291,84,1.7)
    caption("Wake sequence",9,48,2.8)
    caption("Read RTC, keys and BME280. Restore both controller image planes for a valid differential update.",9,40)
    caption("A failed or interrupted optical update requires a full refresh. Commit the new state before asserting TIMER_DONE.",9,34)
    caption("Sheet index",9,21,2.3)
    labels=[]
    for b,(title,_) in BLOCK_TITLES.items():
        nums=[i for i,p in enumerate(pages,2) if p["block"]==b]
        if nums:labels.append(f"{nums[0]}"+(f"-{nums[-1]}" if len(nums)>1 else "")+"  "+title)
    caption("     |     ".join(labels),9,13,1.75)
    tag(sheet,"instances");tag(sheet,"busses");tag(sheet,"nets")


def generate(outdir=None):
    parts, footprints = load_design()
    if not parts:
        raise ValueError("No electrical blocks found")
    needed={p["footprint"]:footprints[p["footprint"]] for p in parts}
    library=ET.Element("library",{"name":LIBRARY})
    tag(library,"description").text="Astra e-ink weather station. Locally editable parts and land patterns."
    add_packages(library,needed)
    symbols=tag(library,"symbols");devsets=tag(library,"devicesets")
    definitions,ref_device={},{}
    for p in parts:
        d=get_device(p,needed[p["footprint"]])
        key=(d.name,d.footprint,tuple((a.pad,a.name,a.direction) for a in d.pins))
        if key not in definitions:
            if any(v.name==d.name for v in definitions.values()):
                d.name += "_" + hashlib.sha256(repr(key).encode()).hexdigest()[:5].upper()
            make_symbol(symbols,devsets,d);definitions[key]=d
        ref_device[p["ref"]]=definitions[key]
    base=ROOT if outdir is None else Path(outdir)
    r,dr=scaffold()
    l=deepcopy(library);l.attrib.pop("name");dr.append(l)
    write_xml(r,base/"hardware"/"astra.lbr")
    r,dr=scaffold();sch=tag(dr,"schematic",xreflabel="%F%N/%S.%C%R",xrefpart="/%S.%C%R")
    tag(sch,"libraries").append(library)
    tag(sch,"attributes");tag(sch,"variantdefs")
    classes=tag(sch,"classes")
    tag(classes,"class",number="0",name="default",width="0",drill="0")
    config=json.loads((ROOT/"layout"/"placement.json").read_text())
    power_width=config["rules"]["power_width"]
    power_nets={"VBAT","VBUS","SYS_AON","VMAIN","PV_IN","SOLAR_IN","USB5V"}
    for name,width in config.get("widths",{}).items():
        if width == power_width: power_nets.add(name)
        else: power_nets.discard(name)
    tag(classes,"class",number="1",name="power",width=num(power_width),drill="0")
    lookup=tag(sch,"parts")
    for p in parts:
        pt=tag(lookup,"part",name=p["ref"],library=LIBRARY,deviceset=ref_device[p["ref"]].name,device="",value=p["value"])
        for k,v in (("MPN",p.get("mpn")),("LCSC",p.get("lcsc"))):
            if v: tag(pt,"attribute",name=k,value=v)
    sheets=tag(sch,"sheets");pages=page_layout(parts,ref_device)
    index=[]
    overview(sheets,pages)
    for i,page in enumerate(pages,2):
        b=page["block"]; title, sub=BLOCK_TITLES[b]
        groups={name for _,_,name in page["groups"]}
        if b=="power" and "Protected cell charger" in groups:
            title,sub="USB-C, battery charging and system rail","USB priority, protected LiPo power path and switched 3.3 V"
        elif b=="power" and "Solar MPPT" in groups:
            title,sub="Solar harvesting and pack temperature","SPV1050 reservoir, maximum-power-point setting and pack temperature window"
        elif b=="wake" and "Wake timer" in groups:
            title,sub="Wake timing, clock and ambient sensor","Always-on timer, calendar alarm, environmental sensor and wake pulse"
        elif b=="wake" and "Battery ADC" in groups:
            title,sub="User controls and battery measurement","Three wake keys, key decoding and the switched battery divider"
        sheet=tag(sheets,"sheet");tag(sheet,"description").text=title
        drawing=tag(sheet,"plain")
        box(drawing,WIDTH/2,HEIGHT/2,WIDTH,HEIGHT,.25,97)
        label_text(drawing,"ASTRA   /   SOLAR WEATHER STATION",3*G,104*G,1.65,97)
        label_text(drawing,title,3*G,99.5*G,4.1,97)
        label_text(drawing,sub,3*G,97.4*G,1.6,97)
        label_text(drawing,f"PROTOTYPE  A  /  SHEET  {i:02d}  OF  {len(pages)+1:02d}",WIDTH-3*G,104*G,1.65,97,"bottom-right")
        line(drawing,3*G,96.3*G,WIDTH-3*G,96.3*G,.20,97)
        label_text(drawing,"Identical net labels connect across sheets.   |   Pin numbers refer to the top-side package.",3*G,1.75*G,1.55,97)
        for x,y,section in page["groups"]:
            label_text(drawing,str(section).replace("_"," ").strip().upper(),x-24*G,y-G,1.9,97)
        instances=tag(sheet,"instances");tag(sheet,"busses");stubs=[]
        previous=None
        for p,x,y,col,section in page["items"]:
            d=ref_device[p["ref"]]
            instance(instances,symbols,p,d,x,y)
            left=x-24*G;right=x+23*G
            this={}
            for pin in d.pins:
                net=p["pins"].get(pin.pad)
                if not net: continue
                inner=(x+pin.x,y+pin.y);outer=(left if pin.side<0 else right,inner[1])
                label=(outer[0] if pin.side<0 else inner[0]+G,inner[1])
                idx=len(stubs);stubs.append(Stub(p["ref"],pin.name,net,outer,inner,label))
                if d.style!="block":this[pin.side]=idx
            if previous is not None and previous[:2]==(col,section):
                for side,idx in this.items():
                    other=previous[2].get(side)
                    if other is not None and stubs[idx].net==stubs[other].net:
                        stubs[idx].links.append(other);stubs[other].links.append(idx)
            previous=(col,section,this)
            index.append((i,section,p["ref"]))
        nets=sheet_wiring(sheet,stubs,power_nets)
        by_ref={p["ref"]:p for p in parts}
        for spec,origin,section in page["manual"]:
            draw_circuit(spec,origin,by_ref,ref_device,symbols,instances,nets,power_nets)
            index.extend((i,section,ref) for ref in spec["instances"])
    write_xml(r,base/"schematic"/"astra.sch")
    print(f"{len(parts)} parts, {len(definitions)} devices, {len(needed)} footprints, {len(pages)+1} sheets")
    return index


if __name__=="__main__":
    generate()
