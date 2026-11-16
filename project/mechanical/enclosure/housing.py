"""Astra A desktop weather station. B-rep geometry in board coordinates, millimetres.

The front looks toward -Z; +X is the display's right and +Y points down. PCB top is Z=0.
The front panel carries the electronics so the cover and battery can be serviced separately.
"""
from functools import lru_cache
from math import cos, pi, sin, sqrt
import cadquery as cq
from matplotlib import font_manager

import usb_pocket

FRONT_Z, BACK_Z, SEAM = -9.0, 15.0, 5.6
OUTLINE = (-10.0, -100.0, 124.0, 96.0)
WALL = 2.4
GLASS = (24.45, -90.60, 115.45, -13.60)
ACTIVE = (27.55, -87.50, 112.35, -23.90)
THROAT = (26.05, -89.0, 113.85, -22.40)
FLARE = (21.30, -93.90, 118.60, -17.50)
LENS_RECESS = (19.35, -95.85, 120.55, -15.55)
LENS_EDGES = (19.65, -95.55, 120.25, -15.85)
CASE_SCREWS = ((-4.1,-94.8),(118.55,-95.30),(-4.2,-10.0),(118.1,-6.0),(-4.2,90.0),(118.1,90.0))
DISPLAY_SCREWS = ((19.6,-77.0),(119.55,-77.0),(19.6,-31.5),(119.55,-31.5))
UPPER_RAIL_Y = -5.7
LOWER_RAIL_Y = 90.6
RAIL_ANCHORS = ((9.5,UPPER_RAIL_Y),(102.5,UPPER_RAIL_Y),(7.5,LOWER_RAIL_Y),(102.5,LOWER_RAIL_Y))
MOUNT_HOLES = ((3.8,3.8),(108.2,3.8),(3.8,80.2),(108.2,80.2))
FRONT_PADS = ((24.85,-77,25.95,-63),(24.85,-49,25.95,-35),(114.0,-77,115.10,-63),(114.0,-49,115.10,-35))
BACK_PADS = ((29.,-79.,41.,-65.),(29.,-52.,41.,-38.),(99.,-79.,111.,-65.),(99.,-52.,111.,-38.))


def box(x0,y0,z0,x1,y1,z1):
    return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,(x0,y0,z0))


def cylinder(x,y,z0,z1,r):
    return cq.Solid.makeCylinder(r,z1-z0,(x,y,z0))


def outline(bounds,r,z):
    x0,y0,x1,y1=bounds
    w=cq.Wire.makePolygon([(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],close=True)
    return w.fillet2D(r,w.Vertices()) if r else w


def slab(bounds,r,z0,z1):
    return cq.Solid.extrudeLinear(outline(bounds,r,z0),[],(0,0,z1-z0))


def inset(bounds,n):
    x0,y0,x1,y1=bounds
    return (x0+n,y0+n,x1-n,y1-n)


def loft(stations):
    return cq.Solid.makeLoft([outline(b,r,z) for b,r,z in stations],ruled=True)


def merged(base, other):
    shapes=list(other)
    return base.fuse(*shapes).clean() if shapes else base


def subtract(base, tools):
    cuts=list(tools)
    return base.cut(*cuts).clean() if cuts else base


def hexprism(x,y,z0,z1,af):
    r=af/sqrt(3)
    w=cq.Wire.makePolygon([(x+r*cos(i*pi/3),y+r*sin(i*pi/3),z0) for i in range(6)],close=True)
    return cq.Solid.extrudeLinear(w,[],(0,0,z1-z0))


def shell_skin(front):
    if front:
        body=loft([(inset(OUTLINE,.7),6.3,FRONT_Z),(OUTLINE,7,FRONT_Z+.7),(OUTLINE,7,SEAM)])
        return body.cut(slab(inset(OUTLINE,WALL),4.6,-6.6,SEAM+.1))
    body=loft([(OUTLINE,7,SEAM),(OUTLINE,7,BACK_Z-.7),(inset(OUTLINE,.7),6.3,BACK_Z)])
    return body.cut(slab(inset(OUTLINE,WALL),4.6,SEAM-.1,12.6))


def insert_boss(x,y,base,top,r):
    return cylinder(x,y,base,top,r)

def rim_tab(axis,span,inner,sign):
    # Along the outside-down print every new layer widens the tab by <0.20 mm.
    # At the mating end the outer face steps away from the opposing tub wall.
    profile=[(-.45,9.45),(.02,9.45),(1.78,7.35),(1.78,4.10),
             (.32,4.10),(.32,5.61),(-.45,5.61)]
    if axis=="x":
        wire=cq.Wire.makePolygon([(inner+sign*a,span[0],z) for a,z in profile],close=True)
        return cq.Solid.extrudeLinear(wire,[],(0,span[1]-span[0],0))
    wire=cq.Wire.makePolygon([(span[0],inner+sign*a,z) for a,z in profile],close=True)
    return cq.Solid.extrudeLinear(wire,[],(span[1]-span[0],0,0))


def lens_tape():
    return slab(inset(LENS_EDGES,.12),2.6,-7.75,-7.55).cut(slab(inset(FLARE,-.13),1.6,-7.8,-7.50))


def front_shell(power=None):
    face=shell_skin(True)
    sides=[slab((19.4,-95.7,120.25,-15.7),3.0,-6.68,-.505), *usb_pocket.front_additions()]
    for x,y in CASE_SCREWS: sides.append(insert_boss(x,y,-6.75,SEAM,4.15))
    for x,y in DISPLAY_SCREWS:
        boss=insert_boss(x,y,-6.75,1.85,3.4)
        if x>100:
            # Leave the same lateral margin as the rigid glass locator over the entire drop.
            boss=boss.cut(box(x-3.55,y-3.55,-.55,116.65,y+3.55,1.91))
        sides.append(boss)
    for x,y in RAIL_ANCHORS: sides.append(insert_boss(x,y,-6.75,-2.45,3.4))
    # Sparse vertical locators leave the projecting transport tab, wire bond and flex free.
    for y0,y1 in [(-78.,-66.),(-51.,-39.)]:
        sides.extend((box(22.15,y0,-.57,23.45,y1,1.52),box(116.65,y0,-.57,117.95,y1,1.52)))
    for x0,x1 in [(39.,52.),(89.,102.)]: sides.append(box(x0,-93.50,-.57,x1,-91.95,1.52))
    for x0,x1 in [(29.,36.),(87.,98.)]:
        # Lower-edge stops extend to the thicker inactive strip, clear of the FPC bond.
        sides.append(box(x0,-16.6,-6.66,x1,-11.4,-.505))
        sides.append(box(x0,-12.40,-.56,x1,-11.4,1.52))
    face=merged(face,sides)
    aperture=loft([(FLARE,1.7,-9.1),(FLARE,1.7,-7.55),(THROAT,.6,-.505),(THROAT,.6,1)])
    # Cut the maker's mark into the physical front, rotated to read along the left bezel.
    font=font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans",weight="bold"))
    mark=cq.Workplane("XY").text("ASTRA",5.8,.52,fontPath=font,combine=False).val()
    mark=mark.rotate((0,0,0),(1,0,0),180).rotate((0,0,0),(0,0,1),-90).translate((6.7,-55.7,-8.50))
    cuts=[aperture,slab(LENS_RECESS,3.0,-9.15,-7.55),*usb_pocket.front_cuts(),mark]
    for x,y in CASE_SCREWS: cuts.append(cylinder(x,y,SEAM-6.8,SEAM+.15,2.0))
    for x,y in DISPLAY_SCREWS:
        cuts.append(cylinder(x,y,-3.25,2.0,1.6))
        if x>100:
            cuts.append(cylinder(x,y,1.85,SEAM+.15,2.6))
    for x,y in RAIL_ANCHORS: cuts.append(cylinder(x,y,-7.55,-2.30,1.6))
    face=subtract(face,cuts)
    if power:
        face=subtract(face,power.front_cuts());face=merged(face,power.front_adds())
    return face


def rear_shell(power=None,buttons=None):
    lid=shell_skin(False)
    adds=[];cuts=[usb_pocket.lid_cut()]
    for x,y in CASE_SCREWS:
        adds.append(cylinder(x,y,SEAM,12.8,4.15))
        cuts.extend((cylinder(x,y,SEAM-.15,15.2,1.45),cylinder(x,y,12.35,15.2,2.6)))
    # Short alignment tabs retain 0.32 mm per side and leave the ventilation/USB regions unobstructed.
    for x0,x1 in ((2,16),(84,103)):
        adds.extend((rim_tab("y",(x0,x1),OUTLINE[1]+WALL,1),
                     rim_tab("y",(x0,x1),OUTLINE[3]-WALL,-1)))
    for y0,y1 in ((-62,-45),(16,30)):
        adds.extend((rim_tab("x",(y0,y1),-7.6,1),rim_tab("x",(y0,y1),121.6,-1)))
    # A light baffle separates the two external openings from Bosch's upward-facing port.
    for left,right in ((27.4,28.8),(39.0,40.4)):
        adds.extend((box(left,75.0,2.3,right,93.30,12.75),
                     box(left,93.2,SEAM+.05,right,94.1,12.75)))
    adds.extend((
                 box(27.4,74.5,2.3,40.4,75.9,12.75),box(28.7,84.6,6.1,39.1,85.85,12.75)))
    for x0,x1 in ((28.8,32.95),(34.65,39.0)):
        cuts.append(box(x0,93.4,7.05,x1,96.2,10.7))
    for yy in (87.5,90.0,92.45):
        cuts.append(slab((29.3,yy-.69,38.5,yy+.69),.64,12.45,15.2))
    lid=merged(lid,adds);lid=subtract(lid,cuts)
    if power:
        lid=subtract(lid,power.back_cuts());lid=merged(lid,power.back_adds())
    if buttons:
        lid=merged(lid,buttons.additions());lid=subtract(lid,buttons.cutters())
    return lid


def display_retainer():
    r=slab((21.1,-92.75,118.9,-13.8),2,1.85,4.05)
    r=r.cut(slab((26.25,-88.85,113.6,-18.95),1.0,1.7,4.2))
    r=r.cut(box(38.2,-23.75,1.7,81.4,-12.0,4.2))
    # Wide backing fingers above each closed-cell pad transfer the weight without bending the glass.
    for x0,y0,x1,y1 in BACK_PADS:
        b=(22.0,y0-.45,x1+.5,y1+.45) if x0<60 else (x0-.5,y0-.45,118.0,y1+.45)
        r=merged(r,[slab(b,.85,1.85,4.05)])
    r=merged(r,[cylinder(x,y,1.85,4.05,2.2 if x>100 else 3.4) for x,y in DISPLAY_SCREWS])
    cuts=[cylinder(x,y,1.75,4.15,1.175) for x,y in DISPLAY_SCREWS]
    x,y=CASE_SCREWS[1]
    cuts.append(cylinder(x,y,1.7,4.2,4.60))
    return subtract(r,cuts)


def carrier(y_mount,anchor_y):
    direction=1 if anchor_y>y_mount else -1
    beam_y=y_mount if direction>0 else -1.4
    r=slab((.3,beam_y-2.65,111.7,beam_y+2.65),1.5,-4.18,-2.05)
    add=[]; cuts=[]
    for x in (3.8,108.2):
        if beam_y!=y_mount:
            add.append(box(x-2.85,beam_y,-4.18,x+2.85,y_mount,-2.05))
        add.append(cylinder(x,y_mount,-4.18,-2.05,3.8))
        add.append(cylinder(x,y_mount,-2.10,-1.0,3.25))
        cuts.extend((hexprism(x,y_mount,-4.25,-2.14,5.22),cylinder(x,y_mount,-4.3,-.92,1.37)))
    for x,ay in RAIL_ANCHORS:
        if ay!=anchor_y: continue
        start,end=sorted((beam_y,anchor_y-direction*2.45))
        add.append(box(x-2.9,start,-4.18,x+2.9,end,-2.05))
        start,end=sorted((anchor_y-direction*3.5,anchor_y-direction*1.65))
        add.append(box(x-2.9,start,-4.18,x+2.9,end,-.30))
        add.append(cylinder(x,anchor_y,-2.45,-.30,3.7))
        cuts.append(cylinder(x,anchor_y,-4.25,-.2,1.175))
        # The front post seats directly against the flat face underneath the ear.
        cuts.append(cylinder(x,anchor_y,-4.4,-2.45,3.44))
    if direction>0:
        cuts.append(box(-11,93.25,-4.4,125,96,.1))
    return subtract(merged(r,add),cuts)


def board_fasteners():
    result={}
    def screw(name,x,y,seat,length,r,headr,h):
        # Major diameter envelope; a real recessed hex shows both insertion side and driver reach.
        shaft=cylinder(x,y,seat-length,seat+.02,r)
        head=cylinder(x,y,seat,seat+h,headr).cut(hexprism(x,y,seat+h*.42,seat+h+.02,r*1.6))
        result[name]=shaft.fuse(head).clean()
    def insert(name,x,y,top,h,r,bore):
        # Reference is the installed bore envelope. The knurls displace polymer during heat insertion.
        result[name]=cylinder(x,y,top-h,top,r).cut(cylinder(x,y,top-h-.01,top+.01,bore))
    for i,(x,y) in enumerate(CASE_SCREWS,1):
        screw(f'Case_screw_{i}',x,y,12.35,12,1.25,2.25,2.5)
        insert(f'Case_insert_{i}',x,y,SEAM,5.7,2.0,1.26)
    for i,(x,y) in enumerate(DISPLAY_SCREWS,1):
        screw(f'Display_screw_{i}',x,y,4.05,6,1.0,1.9,2.0)
        insert(f'Display_insert_{i}',x,y,1.85,4.,1.6,1.01)
    for i,(x,y) in enumerate(RAIL_ANCHORS,1):
        screw(f'Rail_screw_{i}',x,y,-.30,6,1.0,1.9,2.0)
        insert(f'Rail_insert_{i}',x,y,-2.45,4.,1.6,1.01)
    for i,(x,y) in enumerate(MOUNT_HOLES,1):
        screw(f'PCB_screw_{i}',x,y,0,4,1.25,2.25,2.5)
        result[f'PCB_nut_{i}']=hexprism(x,y,-4.14,-2.14,5.0).cut(cylinder(x,y,-4.2,-2.1,1.26))
    return result


def display_references():
    result={'Display_glass':slab(GLASS,.02,-.005,1.195),
            'Display_active':slab(ACTIVE,.02,-.012,-.005),
            'Optical_lens':slab(LENS_EDGES,2.7,-8.75,-7.75),'Lens_tape':lens_tape()}
    # The wide shoulder is an assembly exclusion envelope derived from the manufacturer's drawing.
    # Referenced in the fit checker rather than inventing a flex route through this region.
    fpc=box(41.25,-13.60,.595,53.75,4.9,.895)
    shoulder=box(41.25,-13.60,.595,77.95,-2.60,.745)
    result['Display_FPC']=fpc.fuse(shoulder).clean()
    for i,p in enumerate(FRONT_PADS,1):
        result[f'EPD_front_guard_{i}']=slab(p,.18,-.505,-.255)
    for i,p in enumerate(BACK_PADS,1):
        result[f'EPD_back_pad_{i}']=slab(p,.65,1.25,1.85)
    for i,(x0,x1) in enumerate(((29.7,35.3),(88.,96.)),1):
        # Soft stop at the vertical edge, set to the measured length of the fully seated flex.
        result[f'EPD_lower_edge_stop_{i}']=box(x0,-13.47,.18,x1,-12.40,.92)
    for i,y in enumerate((-72.,-44.),1):
        result[f'EPD_side_edge_stop_{i}']=box(23.45,y,.18,24.28,y+4.,.92)
        result[f'EPD_far_edge_stop_{i}']=box(115.62,y,.18,116.65,y+4.,.92)
    return result
