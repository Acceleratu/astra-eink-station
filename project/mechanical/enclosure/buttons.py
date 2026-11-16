"""Rear switch mechanism. All returned geometry is a CadQuery Shape in mm.

PCB component side is Z=0. Apply additions, then cutters, to the 2.4 mm
rear skin. Install the three side-printed keys from the inside, then the
one-piece keeper with two M2.5 x 6 socket screws in the tapped case bosses.
"""
from math import atan, degrees

import cadquery as cq


CENTRES = ((47.0, 79.1), (63.0, 79.1), (79.0, 79.1))
NAMES = ("SW401", "SW402", "SW403")
REAR_Z = 15.0
SKIN = 2.4
KEY_TOP = 16.10
GUIDE_BASE = 11.40
FLANGE_BASE = 10.00
STROKE = 1.60
STOP_Z = FLANGE_BASE - STROKE
KEEPER_BASE = 7.20
NOSE_Z = 2.80
NOSE_RADIUS = 2.95
NOSE_FLAT = .030
SOLDERED_SWITCH_Z = 2.545
KEY_WIDTH = 7.60
KEY_DEPTH = 6.20
RADIAL_PLAY = .35
LEAF_L = 12.30
LEAF_T = 1.40
SPRING_BASE = 4.75
ROOT_BASE = 6.05
FINGER_T = .80
FINGER_W = 1.30
FINGER_ROOT = 87.90
FINGER_TIP = 77.35
LOWER_GUIDE_Y = 74.60
PRELOAD = .20
SCREW_CENTRES = ((55., 79.35), (71., 79.35))


def _box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, (x0, y0, z0))


def _cyl(r, z0, z1, x=0., y=0.):
    return cq.Solid.makeCylinder(r, z1-z0, (x, y, z0))


def _fuse(pieces):
    return pieces[0].fuse(*pieces[1:]).clean()


def _rounded(w, d, r, z0, z1):
    return (cq.Workplane("XY").box(w, d, z1-z0, centered=(True, True, False))
            .edges("|Z").fillet(r).val().translate((0, 0, z0)))


def _rounded_wire(w, d, r, z):
    face = _rounded(w, d, r, z, z+.05).Faces()
    return min(face, key=lambda f: f.Center().z).outerWire()


def _opening():
    w = KEY_WIDTH + 2*RADIAL_PLAY
    d = KEY_DEPTH + 2*RADIAL_PLAY
    bore = _rounded(w, d, 1.25, GUIDE_BASE-.15, REAR_Z+.15)
    # The flared mouth lets a fingertip follow the key below the rear plane.
    mouth = cq.Solid.makeLoft([_rounded_wire(w, d, 1.25, 14.15),
                               _rounded_wire(12.1, 10.1, 2.85, REAR_Z+.02)], True)
    return _fuse([bore, mouth])


def cutters():
    """Through-guides, finger recesses and two blind tap pilots in global XYZ."""
    mouth = _opening()
    guides = [mouth.translate((x, y, 0)) for x, y in CENTRES]
    pilots = [_cyl(1.025, STOP_Z-.18, 14.0, x, y) for x, y in SCREW_CENTRES]
    return tuple(guides + pilots)


def additions():
    """Hollow guide lips and pilot-drilled keeper bosses fused into rear skin."""
    bore = _rounded(KEY_WIDTH+2*RADIAL_PLAY, KEY_DEPTH+2*RADIAL_PLAY, 1.25,
                    GUIDE_BASE-.1, REAR_Z+.1)
    lip = _rounded(11.1, 9.5, 2.55, GUIDE_BASE, REAR_Z-SKIN+.15).cut(bore)
    guides = [lip.translate((x, y, 0)) for x, y in CENTRES]
    bosses = [_cyl(2.85, STOP_Z, REAR_Z-SKIN+.15, x, y).cut(
              _cyl(1.025, STOP_Z-.1, REAR_Z+.1, x, y)) for x,y in SCREW_CENTRES]
    return tuple(guides + bosses)


def _unit_bend(s):
    """Euler–Bernoulli cantilever with a point-loaded free end, s=0 at clamp."""
    return s*s*(3-s)/2


def _section(y, width, low, thick):
    a=width/2
    return cq.Wire.makePolygon([(-a,y,low),(a,y,low),(a,y,low+thick),
                                (-a,y,low+thick)], close=True)


def _leaf_below_key(flex, tip_shift):
    wires=[]
    stations=sorted({-1.43,0.,1.55,3.05,*[LEAF_L*i/12 for i in range(1,13)],LEAF_L+.16})
    for y in stations:
        s=max(0.,1-y/LEAF_L)
        low=SPRING_BASE + (ROOT_BASE-SPRING_BASE)*y/LEAF_L
        low+=flex*_unit_bend(s)
        # The free end passes between the two return fingers on a side press.
        width=(3.1 if y<0 else 3.90+min(1.,max(0.,(y-1.55)/1.50))*(KEY_WIDTH-3.90))
        wires.append(_section(y,width,low,LEAF_T if y>=0 else .84))
    blade=cq.Solid.makeLoft(wires,True)
    z0=NOSE_Z+tip_shift
    nose=cq.Solid.makeCone(1.17,1.80,SPRING_BASE+.30-z0-.22,(0,0,z0+.22))
    # A small flat gives a printable, manifold contact. The skirt rolls onto
    # its spherical shoulder as the blade bends under load.
    ball=cq.Solid.makeSphere(NOSE_RADIUS,(0,0,z0+NOSE_RADIUS-NOSE_FLAT),
                             angleDegrees1=-90,angleDegrees2=90)
    dome=ball.intersect(_box(-3.1,3.1,-3.1,3.1,z0,z0+.235))
    nose=_fuse([nose,dome])
    nose=nose.rotate((0,0,SPRING_BASE),(1,0,SPRING_BASE),
                     -degrees(atan(1.5*flex/LEAF_L))).translate((0,0,flex))
    return _fuse([blade,nose])


def _root_gusset():
    # The 0.75 mm runout spreads bending stress into the vertical root.
    y=LEAF_L; z=ROOT_BASE+LEAF_T
    wire=cq.Wire.makePolygon([(-KEY_WIDTH/2,y-.78,z-.15),
                               (-KEY_WIDTH/2,y+.04,z-.15),
                               (-KEY_WIDTH/2,y+.04,z+.72)], close=True)
    return cq.Solid.extrudeLinear(wire,[],(KEY_WIDTH,0,0))


def _key(index, stroke, flex, tip_shift=0.):
    head=_rounded(KEY_WIDTH,KEY_DEPTH,.9,GUIDE_BASE-.12,KEY_TOP)
    head=cq.Workplane(obj=head).faces(">Z").edges().fillet(.32).val()
    # One, two and three shallow grooves identify the independent keys by touch.
    for i in range(index+1):
        x=(i-index/2)*1.50
        notch=_rounded(.68,3.50,.31,KEY_TOP-.26,KEY_TOP+.2).translate((x,0,0))
        head=head.cut(notch)
    top=_box(-KEY_WIDTH/2,KEY_WIDTH/2,-5.0,LEAF_L+1.40,FLANGE_BASE,GUIDE_BASE)
    # A second, separated bearing guides side presses and limits nose offset.
    guide_y=LOWER_GUIDE_Y-CENTRES[index][1]
    tongue=_box(-KEY_WIDTH/2,KEY_WIDTH/2,guide_y-.55,guide_y+.55,5.70,FLANGE_BASE+.12)
    clamp=_box(-KEY_WIDTH/2,KEY_WIDTH/2,LEAF_L,LEAF_L+1.40,ROOT_BASE,GUIDE_BASE)
    key=_fuse([head,top,tongue,clamp,_root_gusset(),_leaf_below_key(flex,tip_shift)])
    x,y=CENTRES[index]
    return key.translate((x,y,-stroke))


def _return_finger(x, drop):
    length=FINGER_ROOT-FINGER_TIP
    wires=[]
    for i in range(13):
        s=i/12
        y=FINGER_ROOT-length*s
        low=KEEPER_BASE-drop*_unit_bend(s)
        wires.append(_section(y,FINGER_W,low,FINGER_T))
    finger=cq.Solid.makeLoft(wires,True).translate((x,0,0))
    # The small shoe remains centred on its bearing as the finger bends.
    end=KEEPER_BASE+FINGER_T
    shoe=_box(x-.63,x+.63,FINGER_TIP-.60,FINGER_TIP+.40,
              end-.18,FLANGE_BASE+PRELOAD)
    shoe=shoe.rotate((x,FINGER_TIP,end),(x+1,FINGER_TIP,end),
                     degrees(atan(1.5*drop/length))).translate((0,0,-drop))
    # The contact point is the high edge of the inclined shoe under a flat key.
    shoe=shoe.translate((0,0,FLANGE_BASE+PRELOAD-drop-shoe.BoundingBox().zmax))
    return _fuse([finger,shoe])


def keeper(strokes=(0.,0.,0.), free=False):
    """Removable keeper. Six PETG tongues return the three keys individually."""
    x0,x1=41.0,85.0
    front=_box(x0,x1,73.15,76.35,KEEPER_BASE,STOP_Z)
    for x,_ in CENTRES:
        front=front.cut(_box(x-KEY_WIDTH/2-RADIAL_PLAY,x+KEY_WIDTH/2+RADIAL_PLAY,
                             LOWER_GUIDE_Y-.55-RADIAL_PLAY,LOWER_GUIDE_Y+.55+RADIAL_PLAY,
                             KEEPER_BASE-.1,STOP_Z+.1))
    rear=_box(x0,x1,87.77,89.50,KEEPER_BASE,STOP_Z)
    for x,_ in CENTRES:
        rear=rear.cut(_box(x-4.22,x+4.22,88.55,89.56,KEEPER_BASE-.08,7.60))
    rails=[front,rear]
    for x,y in SCREW_CENTRES:
        rails += [_box(x-2.0,x+2.0,73.7,89.15,KEEPER_BASE,STOP_Z),
                  _cyl(3.15,KEEPER_BASE,STOP_Z,x,y)]
    pieces=rails[:]
    for x,index in zip((c[0] for c in CENTRES),range(3)):
        drop=0. if free else PRELOAD+strokes[index]
        pieces += [_return_finger(x+side,drop) for side in (-2.95,2.95)]
    body=_fuse(pieces)
    for x,y in SCREW_CENTRES:
        body=body.cut(_cyl(1.40,KEEPER_BASE-.10,STOP_Z+.10,x,y))
    return body.clean()


def parts(strokes=(0.,0.,0.), flexes=(0.,0.,0.), tip_shifts=(0.,0.,0.)):
    """Four fitted printed solids in board coordinates, normally at rest.

    strokes are distances towards the PCB. flexes are elastic upward tip
    displacements relative to each moving key. The checking script supplies
    the latter from switch travel under load; CAD exports default to rest.
    tip_shifts are three signed nozzle trims. Raise a tip to increase clearance.
    """
    if len(strokes)!=3 or len(flexes)!=3 or any(s<0 or s>STROKE+.001 for s in strokes):
        raise ValueError("Provide three strokes between zero and the hard stop")
    if len(tip_shifts)!=3 or any(abs(t)>.30 for t in tip_shifts):
        raise ValueError("Each fitted nozzle trim must be within ±0.30 mm")
    result={name:_key(i,strokes[i],flexes[i],tip_shifts[i]) for i,name in enumerate(NAMES)}
    result["key_keeper"]=keeper(strokes)
    return result


def print_parts(tip_shifts=(0.,0.,0.)):
    """Keys on their flat X-sided root and blade; keeper flat, springs unstressed."""
    if len(tip_shifts)!=3 or any(abs(t)>.30 for t in tip_shifts):
        raise ValueError("Each printed nozzle trim must be within ±0.30 mm")
    fitted={name:_key(i,0.,0.,tip_shifts[i]) for i,name in enumerate(NAMES)}
    result={}
    for name,shape in fitted.items():
        p=shape.rotate((0,0,0),(0,1,0),-90)
        b=p.BoundingBox()
        result[name]=p.translate((-b.xmin,-b.ymin,-b.zmin))
    p=keeper(free=True)
    b=p.BoundingBox()
    result["key_keeper"]=p.translate((-b.xmin,-b.ymin,-b.zmin))
    return result


def hardware():
    """M2.5 x 6 ISO 4762 socket screws, non-printing check solids."""
    result={}
    for i,(x,y) in enumerate(SCREW_CENTRES,1):
        head=_cyl(2.25,KEEPER_BASE-2.5,KEEPER_BASE,x,y)
        shank=_cyl(1.25,KEEPER_BASE-.02,KEEPER_BASE+6.,x,y)
        result[f"keeper_screw_{i}"]=_fuse([head,shank])
    return result
