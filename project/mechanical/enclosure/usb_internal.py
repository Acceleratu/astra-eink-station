"""Removable, post-reflow opaque film parts outside GCT USB4135-GF-A (board mm).

The front saddle enters along +X. The mirror trays enter from opposite Y sides
between the shell solder pads. The preformed, two-piece PET hood lowers in -Z.
All PSA is on accessible flat exterior steel, soldermask or an optical film.
"""
from math import asin, cos, hypot, pi, sin, sqrt
from pathlib import Path

import cadquery as cq
import ezdxf


PORT_Y = 67.0
PI_T = .0254       # DuPont Kapton Black 100B
PET_T = .125       # Toray Lumirror X30 #125
PSA_T = .050       # tesa 68822
SADDLE_FRONT, CHEEK_END, SADDLE_END = .10, 1.95, 5.30
CENTRE_HALF, SADDLE_HALF = 3.22, 4.13
TRAY_FRONT, TRAY_BACK = 3.83, 5.52
TRAY_BEND_RADIUS = .12
TRAY_TOP = .345
TRAY_OUTER_TOP = .620
TRAY_TALL_WIDTH = 1.72
HOOD_X0, HOOD_X1 = .50, 7.62
HOOD_RADIUS = .3625  # PET neutral axis, inner R0.30
HOOD_PATH = ((58.00,.1125),(60.3425,.1125),(60.3425,3.8625),
             (73.6575,3.8625),(73.6575,.1125),(74.85,.1125))
CURTAIN_PATH = ((5.82,3.6875),(7.800,3.6875),(7.800,.065))
CURTAIN_Y0, CURTAIN_Y1 = 59.90, 74.10
CURTAIN_BOTTOM_SLOT=(65.40,68.60,.55)
CURTAIN_NARROW_Y0, CURTAIN_NARROW_Y1 = 61.21, 72.79
CURTAIN_STEP_Z = 3.27
TRAY_NAMES = ('USB_internal_tray_L','USB_internal_tray_R')
PI_COLOR = (.036,.039,.040)
PET_COLOR = (.030,.032,.035)
PSA_COLOR = (.050,.051,.052)
COLORS = {
    'USB_internal_lower_Kapton':PI_COLOR,
    **{name:PI_COLOR for name in TRAY_NAMES},
    'USB_internal_hood_PET':PET_COLOR,'USB_internal_curtain_PET':PET_COLOR,
    **{'USB_internal_'+name:PSA_COLOR for name in
       ('saddle_PSA_L','saddle_PSA_R','tray_PSA_L','tray_PSA_R',
        'hood_PSA_L','hood_PSA_R','curtain_PSA')},
}


def box(x0,x1,y0,y1,z0,z1):
    return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,(x0,y0,z0))


def lower_saddle():
    def path(offset):
        section = [(0,.120-offset),(CENTRE_HALF,.120-offset)]
        for i in range(1,43):
            t=pi*i/(2*42)
            section.append((CENTRE_HALF+(1.30+offset)*sin(t),1.395-(1.275+offset)*cos(t)))
        section.append((4.52+offset,2.080))
        return [(-y,z) for y,z in reversed(section[1:])] + section
    outline=path(0)+list(reversed(path(PI_T)))
    wire=cq.Wire.makePolygon([(SADDLE_FRONT,PORT_Y+y,z) for y,z in outline],close=True)
    formed=cq.Solid.extrudeLinear(wire,[],(SADDLE_END-SADDLE_FRONT,0,0))
    cuts=[box(CHEEK_END,SADDLE_END+.02,60.,PORT_Y-SADDLE_HALF,-.01,2.2),
          box(CHEEK_END,SADDLE_END+.02,PORT_Y+SADDLE_HALF,74.,-.01,2.2)]
    return formed.cut(*cuts).clean()


def _unit(a,b):
    x,y=b[0]-a[0],b[1]-a[1]
    l=hypot(x,y)
    return x/l,y/l


def _add(p,v,k):
    return (p[0]+k*v[0],p[1]+k*v[1])


def _left(v):
    return (-v[1],v[0])


def _sheet(points,radius,thickness,map3,extrusion):
    """One solid with tangent lines and real circular, constant-thickness bends."""
    def half(pts):
        o=thickness/2
        directions=[_unit(a,b) for a,b in zip(pts,pts[1:])]
        start=_add(pts[0],_left(directions[0]),o)
        edges=[]
        at=start
        for index,p in enumerate(pts[1:-1]):
            incoming,outgoing=directions[index:index+2]
            tangent=_add(p,incoming,-radius)
            centre=_add(tangent,outgoing,radius)
            a=_add(tangent,_left(incoming),o)
            c=_add(_add(p,outgoing,radius),_left(outgoing),o)
            diagonal=(a[0]+c[0]-2*centre[0],a[1]+c[1]-2*centre[1])
            rr=hypot(a[0]-centre[0],a[1]-centre[1])
            mid=_add(centre,diagonal,rr/hypot(*diagonal))
            edges.extend((cq.Edge.makeLine(map3(*at),map3(*a)),
                          cq.Edge.makeThreePointArc(map3(*a),map3(*mid),map3(*c))))
            at=c
        end=_add(pts[-1],_left(directions[-1]),o)
        edges.append(cq.Edge.makeLine(map3(*at),map3(*end)))
        return start,edges,end
    a,first,b=half(points);c,reverse,d=half(points[::-1])
    wire=cq.Wire.assembleEdges([*first,cq.Edge.makeLine(map3(*b),map3(*c)),
                                 *reverse,cq.Edge.makeLine(map3(*d),map3(*a))])
    return cq.Solid.extrudeLinear(wire,[],extrusion).clean()


def tray(side):
    # The cut-out alongside the centre of the connector leaves a raised lip
    # only alongside the shell corners. The tabs come in from their own side.
    outer,shoulder,inner=(60.60,63.03,63.35) if side=='L' else (73.40,70.97,70.65)
    ux=TRAY_BACK-PI_T/2
    path=((TRAY_FRONT,PSA_T+PI_T/2),(ux,PSA_T+PI_T/2),(ux,TRAY_TOP))
    folded=_sheet(path,TRAY_BEND_RADIUS,PI_T,lambda x,z:(x,outer,z),(0,shoulder-outer,0))
    # At the shoulder a common straight portion joins the folded and flat zones.
    flat=box(TRAY_FRONT,TRAY_BACK,min(shoulder,inner),max(shoulder,inner),PSA_T,PSA_T+PI_T)
    edge=outer+TRAY_TALL_WIDTH if side=='L' else outer-TRAY_TALL_WIDTH
    # The central flank stays under the curved steel. Only the free lateral
    # end rises farther, intercepting grazing views before the rear SH feet.
    tall=box(TRAY_BACK-PI_T,TRAY_BACK,min(outer,edge),max(outer,edge),TRAY_TOP,TRAY_OUTER_TOP)
    return folded.fuse(flat,tall).clean()


def references():
    hood=_sheet(HOOD_PATH,HOOD_RADIUS,PET_T,lambda y,z:(HOOD_X0,y,z),(HOOD_X1-HOOD_X0,0,0))
    curtain=_sheet(CURTAIN_PATH,HOOD_RADIUS,PET_T,lambda x,z:(x,CURTAIN_Y0,z),
                   (0,CURTAIN_Y1-CURTAIN_Y0,0))
    cuts=[box(5.60,7.98,CURTAIN_Y0-.02,CURTAIN_NARROW_Y0,CURTAIN_STEP_Z,4.0),
          box(5.60,7.98,CURTAIN_NARROW_Y1,CURTAIN_Y1+.02,CURTAIN_STEP_Z,4.0),
          box(7.62,7.98,*CURTAIN_BOTTOM_SLOT[:2],-.01,CURTAIN_BOTTOM_SLOT[2])]
    curtain=curtain.cut(*cuts).clean()
    return {
        'USB_internal_lower_Kapton':lower_saddle(),
        TRAY_NAMES[0]:tray('L'),TRAY_NAMES[1]:tray('R'),
        'USB_internal_hood_PET':hood,'USB_internal_curtain_PET':curtain,
        'USB_internal_saddle_PSA_L':box(.23,1.81,62.48,62.53,1.49,2.01),
        'USB_internal_saddle_PSA_R':box(.23,1.81,71.47,71.52,1.49,2.01),
        'USB_internal_tray_PSA_L':box(3.96,5.32,60.78,61.50,0,PSA_T),
        'USB_internal_tray_PSA_R':box(3.96,5.32,72.50,73.22,0,PSA_T),
        'USB_internal_hood_PSA_L':box(.80,6.80,58.40,58.90,0,PSA_T),
        'USB_internal_hood_PSA_R':box(.80,6.80,74.08,74.58,0,PSA_T),
        'USB_internal_curtain_PSA':box(5.96,6.90,61.35,72.65,3.75,3.80),
    }


def _rectangle(x,y):
    return [(0,0),(x,0),(x,y),(0,y)]


def _stationing(points,radius):
    lengths=[hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
    marks=[]
    distance=0.
    for i,seg in enumerate(lengths):
        distance+=seg-(radius if i>0 else 0)-(radius if i<len(lengths)-1 else 0)
        if i<len(lengths)-1:
            marks.append(distance+pi*radius/4)
            distance+=pi*radius/2
    return distance,marks


def _saddle_arc(theta):
    # Numerical length of the middle surface of the rolled lower film.
    rx,rz=1.30+PI_T/2,1.275+PI_T/2
    steps=200
    return sum(hypot(rx*cos(theta*(i+.5)/steps),rz*sin(theta*(i+.5)/steps))
               *theta/steps for i in range(steps))


def patterns():
    """Developed film neutral axes; each DXF has one closed 1:1 cut contour."""
    flat_width=CENTRE_HALF
    arc_total=_saddle_arc(pi/2)
    total=flat_width+arc_total+2.08-1.395
    arm=flat_width+_saddle_arc(asin((SADDLE_HALF-CENTRE_HALF)/(1.30+PI_T/2)))
    fore,reach=CHEEK_END-SADDLE_FRONT,SADDLE_END-SADDLE_FRONT
    saddle=[(0,0),(fore,0),(fore,total-arm),(reach,total-arm),(reach,total+arm),
            (fore,total+arm),(fore,2*total),(0,2*total)]
    s_lines=[((0,total-flat_width),(reach,total-flat_width)),((0,total+flat_width),(reach,total+flat_width)),
             ((0,total-flat_width-arc_total),(fore,total-flat_width-arc_total)),
             ((0,total+flat_width+arc_total),(fore,total+flat_width+arc_total))]
    p={'USB-internal-saddle-Kapton-100B.dxf':(saddle,s_lines)}
    ux=TRAY_BACK-PI_T/2
    path=((TRAY_FRONT,PSA_T+PI_T/2),(ux,PSA_T+PI_T/2),(ux,TRAY_TOP))
    reach,marks=_stationing(path,TRAY_BEND_RADIUS)
    flat=TRAY_BACK-TRAY_FRONT
    width=63.35-60.60
    lip=63.03-60.60
    high_reach=reach+TRAY_OUTER_TOP-TRAY_TOP
    profile=[(0,0),(high_reach,0),(high_reach,TRAY_TALL_WIDTH),(reach,TRAY_TALL_WIDTH),
             (reach,lip),(flat,lip),(flat,width),(0,width)]
    # A mirrored XY cut means the same face can be marked "up" on both trays.
    p['USB-internal-tray-L-Kapton-100B.dxf']=(profile,[((marks[0],0),(marks[0],lip))])
    p['USB-internal-tray-R-Kapton-100B.dxf']=(
        [(x,width-y) for x,y in profile],[((marks[0],width),(marks[0],width-lip))])
    length,marks=_stationing(HOOD_PATH,HOOD_RADIUS)
    depth=HOOD_X1-HOOD_X0
    p['USB-internal-hood-X30-125um.dxf']=(_rectangle(depth,length),[((0,m),(depth,m)) for m in marks])
    length,marks=_stationing(CURTAIN_PATH,HOOD_RADIUS)
    width=CURTAIN_Y1-CURTAIN_Y0
    step=length-(CURTAIN_STEP_Z-CURTAIN_PATH[-1][1])
    edge=CURTAIN_NARROW_Y0-CURTAIN_Y0
    slot_start=CURTAIN_BOTTOM_SLOT[0]-CURTAIN_Y0
    slot_end=CURTAIN_BOTTOM_SLOT[1]-CURTAIN_Y0
    relief=CURTAIN_BOTTOM_SLOT[2]-CURTAIN_PATH[-1][1]
    contour=[(0,edge),(step,edge),(step,0),(length,0),(length,slot_start),
             (length-relief,slot_start),(length-relief,slot_end),(length,slot_end),(length,width),(step,width),
             (step,width-edge),(0,width-edge)]
    p['USB-internal-curtain-X30-125um.dxf']=(contour,[((marks[0],edge),(marks[0],width-edge))])
    for suffix,w,h in [('saddle-PSA-cut2',1.58,.52),('tray-PSA-cut2',1.36,.72),
                       ('hood-PSA-cut2',6.,.50),('curtain-PSA-cut1',.94,11.30)]:
        p['USB-internal-'+suffix+'.dxf']=(_rectangle(w,h),[])
    return p


def drawings(directory):
    directory=Path(directory)
    directory.mkdir(parents=True,exist_ok=True)
    for filename,(contour,folds) in patterns().items():
        d=ezdxf.new('R2010');d.units=4
        d.layers.new('CUT',dxfattribs={'color':7})
        d.layers.new('BEND',dxfattribs={'color':5})
        model=d.modelspace()
        model.add_lwpolyline(contour,close=True,dxfattribs={'layer':'CUT'})
        for a,b in folds:
            model.add_line(a,b,dxfattribs={'layer':'BEND'})
        d.saveas(str(directory/filename))
