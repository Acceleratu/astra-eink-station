"""Solar cassette and protected pouch mounting for Astra, Rev A.

All solids use millimetres in final board coordinates. +Z is the component/lid
side. Factory dimensions and the acceptance gauges are in verification/power-datums.md.
The four *_adds/*_cuts entry points return tuples of B-reps. parts() contains
printable pieces. references() contains purchased hardware and installed wiring.
"""
from functools import lru_cache
from pathlib import Path
from math import atan2, cos, hypot, radians, sin, tan

import numpy as np

import cadquery as cq


PV_CENTRE = (50.50, 45.50)
PV_SIZE = (100.8, 82.5, 3.0)
PV_GAUGE = (101.4, 83.1, 3.2)
PV_APERTURE = (-0.55, 3.60, 101.55, 87.40)
PV_SEATS = ((18., False), (50., False), (82., False),
            (18., True), (50., True), (82., True))
PV_LANDS = {'red': (67.5, 75.75), 'black': (33.5, 75.75)}
PV_BOARD = {'red': (13.7, 75.0), 'black': (13.7, 71.50)}
PACK_CENTRE = (48.0, 43.25)
PACK_SIZE = (34., 40., 3.2)
PACK_MAX = (34.5, 41., 3.5)
PACK_ROOF, PACK_FACE, GUARD_TOP = 12.60, 12.45, 7.50
GUARD_POSTS = ((27.15,28.), (68.85,28.), (27.15,58.), (68.85,58.))
BAT_PINS = {'black': 1, 'yellow': 2, 'red': 3}
PV_RADIUS = 0.023 * 25.4 / 2
PV_TURN_RADIUS, PV_PLAN_BEND, PV_TURN_ANGLE = 2.65, 3.00, radians(40.0)
PV_APEX = {'black': (-4.05,79.82,-1.95), 'red': (-4.05,81.02,-1.95)}
PV_EYE = (-7.70,79.75,-4.65,84.45)
BAT_RADIUS = .285
V = cq.Vector


def _box(x0, y0, z0, x1, y1, z1):
    return cq.Solid.makeBox(x1-x0, y1-y0, z1-z0, (x0,y0,z0))


def _cylinder(x, y, z0, z1, r):
    return cq.Solid.makeCylinder(r, z1-z0, (x,y,z0))


def _profile(bounds, radius, z):
    a,b,c,d = bounds
    wire = cq.Wire.makePolygon([(a,b,z),(c,b,z),(c,d,z),(a,d,z)], close=True)
    return wire.fillet2D(radius, wire.Vertices()) if radius else wire


def _slab(bounds, r, z0, z1):
    return cq.Solid.extrudeLinear(_profile(bounds,r,z0), [], (0,0,z1-z0))


def _compound(shapes):
    return cq.Compound.makeCompound(list(shapes))


def _bezier(points):
    return cq.Edge.makeBezier([V(*p) for p in points])


def _pipe(path, radius):
    ring = cq.Wire.makeCircle(radius, path.startPoint(), path.tangentAt(0))
    return cq.Solid.sweep(ring, [], path, isFrenet=False)


@lru_cache(maxsize=1)
def front_cuts():
    # Cut through the 2.4 mm front skin. The front panel enters along +Z.
    return (_slab(PV_APERTURE,.48,-9.15,-4.2),)


def _seat(x, north):
    # The horizontal lip bears the back of the panel through 0.15 mm adhesive.
    # Its foot overlaps the existing face wall for a single printable shell.
    if north:
        stem=(x-6.4,87.42,x+6.4,89.35)
        ledge=(x-6.4,83.45,x+6.4,89.35)
    else:
        stem=(x-6.4,1.65,x+6.4,3.58)
        ledge=(x-6.4,1.65,x+6.4,7.55)
    return _slab(stem,.60,-6.85,-4.02).fuse(
        _slab(ledge,.68,-5.35,-4.02)).clean()


@lru_cache(maxsize=1)
def front_adds():
    # A horizontal through-tunnel accepts the lacing cord from either Y end.
    # It is molded onto the front skin and never needs the board screw as a clamp.
    eye = _slab(PV_EYE,.58,-6.85,-.65).cut(
        _box(-6.65,PV_EYE[1]-.20,-5.60,-5.60,PV_EYE[3]+.20,-2.15))
    return tuple(_seat(x,n) for x,n in PV_SEATS) + (eye,)


@lru_cache(maxsize=1)
def back_cuts():
    # Each blind insert bore ends below the roof underside. The support pillars
    # are pre-bored so the host may apply cuts before fusing back_adds().
    return ()


@lru_cache(maxsize=1)
def back_adds():
    # Intermittent rounding-ended stops leave both the PCM lead corner and the
    # stretch-release pull tabs free. Their faces never preload a centered pack.
    rails = [
        (28.6,32.,30.,51.), (66.,32.,67.4,51.),
        (35.5,20.35,59.0,21.75), (39.,64.75,58.,66.15),
    ]
    pieces=[_slab(b,.60,7.52,12.80) for b in rails]
    for x,y in GUARD_POSTS:
        post=_cylinder(x,y,GUARD_TOP,12.80,2.75)
        # CNC Kitchen TC-M2x3.0 installation bore; qualify diameter on PETG coupon.
        post=post.cut(_cylinder(x,y,GUARD_TOP-.1,11.50,1.60))
        pieces.append(post)
    return tuple(pieces)


@lru_cache(maxsize=1)
def _guard():
    # Flat, full face catches a released pouch above all PCB components. Four
    # side ears transfer screw load to rigid bosses instead of through the pouch.
    guard=_slab((29.6,21.6,66.4,65.0),2.3,6.30,GUARD_TOP)
    ears=[]
    for x,y in GUARD_POSTS:
        inside = 32. if x<48 else 64.
        ears.extend((_cylinder(x,y,6.30,GUARD_TOP,2.75),
                     _box(min(x,inside),y-2.75,6.30,max(x,inside),y+2.75,GUARD_TOP)))
    guard=guard.fuse(*ears).clean()
    return guard.cut(*[_cylinder(x,y,6.15,GUARD_TOP+.15,1.22)
                       for x,y in GUARD_POSTS]).clean()


@lru_cache(maxsize=1)
def parts():
    return {'Battery_guard': _guard()}


def _pack_body(size):
    w,l,t=size
    x,y=PACK_CENTRE
    return _slab((x-w/2,y-l/2,x+w/2,y+l/2),.72,PACK_FACE-t,PACK_FACE)


@lru_cache(maxsize=1)
def maximum_pack():
    """Incoming-drawing maximum pouch envelope in its centered position."""
    return _pack_body(PACK_MAX)


def _pv_tape(x,n):
    b=(x-5.2,83.68,x+5.2,86.31) if n else (x-5.2,4.69,x+5.2,7.32)
    return _slab(b,.25,-5.50,-5.35)


def _offset_arcs(start,end):
    """Two tangent circular bends joining parallel +X cable runs in 3D."""
    dx,dy,dz=(q-p for p,q in zip(start,end))
    lateral=hypot(dy,dz)
    half_angle=atan2(lateral,dx)
    radius=(dx*dx+lateral*lateral)/(4*lateral)
    displacement=radius*(1-cos(half_angle))
    first=(start[0]+radius*sin(half_angle),start[1]+displacement*dy/lateral,
           start[2]+displacement*dz/lateral)
    middle=tuple((p+q)/2 for p,q in zip(start,end))
    second=tuple(2*m-p for m,p in zip(middle,first))
    return (cq.Edge.makeThreePointArc(start,first,middle),
            cq.Edge.makeThreePointArc(middle,second,end))


@lru_cache(maxsize=2)
def _pv_segments(colour):
    # These two smooth leads follow the same raised channel under the PCB.
    # The 180-degree turn is entirely outside the left board edge.
    x,y=PV_LANDS[colour]
    bx,by=PV_BOARD[colour]
    entry_lane=76.40 if colour=='red' else 74.55
    lane=75.75 if colour=='red' else 74.55
    start=(x,y,-5.17)
    strip=(x-2.00,y,-5.17)
    first=(x-7.0,entry_lane,-4.60)
    transition_start=(min(26.,x-8.0),entry_lane,-4.60)
    transition_end=(7.0,lane,-4.60)
    # Tilt the U away from the USB pocket. The two tangential plan-view
    # arcs bring the harness back into its PCB lanes before the mounting boss.
    ax,ay,az=PV_APEX[colour]
    a=PV_TURN_ANGLE
    centre_x=ax+PV_TURN_RADIUS*cos(a)
    centre_y=ay-PV_TURN_RADIUS*sin(a)
    tangent_y=lane+PV_PLAN_BEND*(1-cos(a))
    tangent_x=centre_x+(centre_y-tangent_y)/tan(a)
    flat_x=tangent_x+PV_PLAN_BEND*sin(a)
    def bend(z):
        rising=(tangent_x,tangent_y,z)
        flat=(flat_x,lane,z)
        mid=(flat_x-PV_PLAN_BEND*sin(a/2),lane+PV_PLAN_BEND*(1-cos(a/2)),z)
        return rising,mid,flat
    low,low_mid,low_flat=bend(-4.60)
    # The black tail crosses the foot of the opaque J101 hood. Raise it
    # before it reaches the PCB and turn toward J103 after its rear corner.
    lane_z=1.12 if colour=='black' else .70
    high,high_mid,high_flat=bend(lane_z)
    bot=(centre_x,centre_y,-4.60)
    top=(centre_x,centre_y,.70)
    near=(bx-1.25,by,.44)
    if colour=='black':
        dx,dy=(high[0]-top[0])/3,(high[1]-top[1])/3
        upper_entry=_bezier([top,(top[0]+dx,top[1]+dy,top[2]),
                             (high[0]-dx,high[1]-dy,lane_z),high])
        # These offsets carry the jacket around the full-height rear curtain.
        guide=(6.90,75.18,1.48)
        tail=(*_offset_arcs(high_flat,guide),*_offset_arcs(guide,near))
    else:
        upper_entry=cq.Edge.makeLine(top,high)
        run=(5.50,lane,lane_z)
        tail=(cq.Edge.makeLine(high_flat,run),_bezier([run,(8.05,lane,lane_z),(bx-3.4,by,.44),near]))
    end=(bx,by,.44)
    jacket=cq.Wire.assembleEdges([
        # Keep the first permanent bend at the panel solder joint as broad
        # as the side return even on the more displaced negative cable.
        _bezier([strip,(x-3.65,y,-5.17),(x-5.20,entry_lane,-4.60),first]),
        cq.Edge.makeLine(first,transition_start),
        _bezier([transition_start,(transition_start[0]-4.5,entry_lane,-4.60),
                 (11.5,lane,-4.60),transition_end]),
        cq.Edge.makeLine(transition_end,low_flat),
        cq.Edge.makeThreePointArc(low_flat,low_mid,low),
        cq.Edge.makeLine(low,bot),
        cq.Edge.makeThreePointArc(bot,(ax,ay,az),top),
        upper_entry,
        cq.Edge.makeThreePointArc(high,high_mid,high_flat),
        *tail
    ])
    return cq.Edge.makeLine(start,strip),jacket,cq.Edge.makeLine(near,end)


def pv_path(colour):
    start,jacket,end=_pv_segments(colour)
    return cq.Wire.assembleEdges([start,*jacket.Edges(),end])


def _pv_termination(colour):
    start,_,end=_pv_segments(colour)
    x,y=PV_LANDS[colour]
    bx,by=PV_BOARD[colour]
    panel_joint=_slab((x-.46,y-.34,x+.37,y+.34),.27,-5.40,-5.04)
    board_joint=_slab((bx-.63,by-.36,bx+.36,by+.36),.26,.035,.50)
    return _compound([_pipe(cq.Wire.assembleEdges([start]),.135).fuse(panel_joint).clean(),
                      _pipe(cq.Wire.assembleEdges([end]),.135).fuse(board_joint).clean()])


def _pv_lacing():
    # One installed loop before trimming the knot. A closed rounded rectangle
    # passes through both Y mouths and loosely around the two insulated leads.
    outer=_profile((-6.13,78.86,-3.08,85.10),.67,-2.85)
    return _pipe(outer,.30)


BAT_BEND_RADIUS = 2.60

def _battery_nodes(pin, opening, handle):
    k=2-pin
    sx=22.30+1.20*k
    ex=32.35+.72*k
    # First rise clears R116, C112 and U105. The folded part stays left of
    # the BME air duct and out of the PCB mounting rail. At the far bend the
    # three wires fan above one another, keeping their insulation separated.
    return np.array([
        (sx,47.08,1.0),(sx,49.20,1.0),(sx,53.25,4.75),
        (sx,56.30,5.05),(21.50-handle+1.20*k,64.50,5.75+.20*opening),
        (21.50-handle+1.20*k,71.50-.16*opening,7.75+.55*opening-1.0*k),
        (ex,70.60-.10*opening+1.0*k,10.90+opening),
        (ex,63.25,10.90+opening)],dtype=float)


def _round_battery_nodes(nodes):
    chords=np.diff(nodes,axis=0)
    lengths=np.linalg.norm(chords,axis=1)
    directions=chords/lengths[:,None]
    cosines=np.clip((directions[:-1]*directions[1:]).sum(axis=1),-1,1)
    angles=np.arccos(cosines)
    trim=BAT_BEND_RADIUS*np.tan(angles/2)
    straight=lengths-np.r_[0,trim]-np.r_[trim,0]
    entry=nodes[1:-1]-directions[:-1]*trim[:,None]
    leave=nodes[1:-1]+directions[1:]*trim[:,None]
    inward=directions[1:]-directions[:-1]*cosines[:,None]
    inward/=np.linalg.norm(inward,axis=1)[:,None]
    centres=entry+inward*BAT_BEND_RADIUS
    length=float(straight.sum()+angles.sum()*BAT_BEND_RADIUS)
    return length,straight,entry,leave,centres,directions,angles


@lru_cache(maxsize=192)
def battery_path(colour, opening_mm=0.0, free_length_mm=50.0):
    """Physical 3D lead: fixed arc length, 2.60 mm tangential bend radii."""
    pin=BAT_PINS[colour]
    lo,hi=-4.5,18.
    for _ in range(25):
        mid=(lo+hi)/2
        nodes=_battery_nodes(pin,opening_mm,mid)
        length,straight,entry,leave,centres,directions,angles=_round_battery_nodes(nodes)
        if length<free_length_mm:
            lo=mid
        else:
            hi=mid
    if abs(length-free_length_mm)>.002 or min(straight)<.02:
        raise ValueError('Lead length or opening falls outside the qualified harness geometry')
    edges=[]
    previous=nodes[0]
    for i,(start,finish,centre) in enumerate(zip(entry,leave,centres)):
        angle=angles[i]/2
        middle=centre+(start-centre)*cos(angle)+directions[i]*BAT_BEND_RADIUS*sin(angle)
        edges.append(cq.Edge.makeLine(V(*previous),V(*start)))
        edges.append(cq.Edge.makeThreePointArc(V(*start),V(*middle),V(*finish)))
        previous=finish
    edges.append(cq.Edge.makeLine(V(*previous),V(*nodes[-1])))
    return cq.Wire.assembleEdges(edges)


def _guard_screw(x,y):
    # ISO 7045 M2x4, model of thread major envelope and cross recess.
    shaft=_cylinder(x,y,6.29,10.30,.98)
    head=_cylinder(x,y,4.70,6.30,2.00)
    cross=(_box(x-1.1,y-.22,4.67,x+1.1,y+.22,5.50),
           _box(x-.22,y-1.1,4.67,x+.22,y+1.1,5.50))
    return shaft.fuse(head.cut(*cross)).clean()


def _pack_plug():
    # JST ACH three-way mating housing: the sidewalls and open wire cavities
    # remain visible in the assembled view. The installed header is in the PCB.
    model=Path(__file__).parent/'verification'/'power-datums.achr.step'
    if model.is_file():
        return cq.importers.importStep(str(model)).val()
    body=_slab((19.95,44.0,24.65,47.30),.16,.26,1.31)
    crimp_channels=[_box(x-.45,44.80,.48,x+.45,47.39,1.30)
                    for x in (21.1,22.3,23.5)]
    # The generic mated housing is reconstructed within its catalogue outline.
    # Tool its contact slots and mating faces against the actual released
    # receptacle. This is a fit reference, not a substitute JST tooling model.
    header_file=Path(__file__).resolve().parents[2]/'hardware/models/JST_BM03B-ACHSS-GAN-ETF.step'
    raw=cq.importers.importStep(str(header_file)).val()
    header=raw.rotate((0,0,0),(0,0,1),-90).translate((.07657,.00005,.05))
    header=header.rotate((0,0,0),(0,0,1),270).translate((22.3,45.2,.045))
    return body.cut(*crimp_channels,header).clean()


def _solar_face():
    # Rectified ABRA image width spans 100.8 mm. The horizontal busbar is
    # visible at 39.0 mm from the image's top edge. Dark vertical strokes
    # below are displacements measured from the same photographic datum.
    inner=(1.36,5.55,99.64,85.45)
    face=_slab(inner,.34,-8.5,-8.46)
    bus=_slab((1.72,42.66,99.20,43.81),.13,-8.50,-8.47)
    strokes=(4.2,7.2,11.2,21.6,25.4,29.0,32.2,37.0,40.2,44.4,47.2,
             49.8,56.2,59.6,62.6,65.8,69.8,73.2,76.2,81.4,84.4,88.2,92.4,96.6)
    lines=[]
    for dx in strokes:
        width=.32 if dx in (11.2,21.6,40.2,59.6,69.8,88.2) else .16
        x=.10+dx
        for lo,hi in ((6.15,42.66),(43.81,84.85)):
            lines.append(_box(x-width/2,lo,-8.50,x+width/2,hi,-8.47))
    marks=_compound(lines)
    return face.cut(bus,marks),bus,marks


def _solder_land(x,y):
    return _slab((x-1.8,y-.83,x+1.8,y+.83),.40,-5.50,-5.40)


def _pack_tape(x):
    # Tabs point to the unobstructed short edge (opposite the PCM). The folded
    # release liner is a pull handle, not additional adhesive on the pouch.
    return _slab((x-2.25,25.65,x+2.25,50.5),.40,12.45,12.60)


@lru_cache(maxsize=1)
def references():
    # One reference per bought item/material. Contacts are represented at their
    # installed interfaces. The renderer can assign separate colors by name.
    panel=_slab((.10,4.25,100.90,86.75),.65,-8.50,-5.50)
    active,bus,scribe=_solar_face()
    panel=panel.cut(_slab((1.36,5.55,99.64,85.45),.34,-8.55,-8.46))
    full_pack=_pack_body(PACK_SIZE)
    pcm=full_pack.intersect(_box(30.9,59.85,9.15,65.1,63.35,12.55))
    refs={'Solar_panel_ABRA':panel, 'Solar_cells':active,
          'Solar_strain_relief_cord':_pv_lacing(),'Battery_PCM_Kapton':pcm,
          'Solar_collector':bus,'Solar_cell_lines':scribe, 'Battery_LP223439':full_pack.cut(pcm).clean(),
          'Battery_plug_JST_ACHR_03V_S':_pack_plug(),
          'Solar_seat_tape':_compound(_pv_tape(x,n) for x,n in PV_SEATS),
          'Battery_seat_tape':_compound(_pack_tape(x) for x in (39.,56.)),
          'Solar_back_contacts':_compound(_solder_land(x,y) for x,y in PV_LANDS.values())}
    # The first few mm of wire skin and the solder wets the projected contact.
    for colour,(x,y) in PV_LANDS.items():
        refs['Solar_lead_'+colour]=_pipe(_pv_segments(colour)[1],PV_RADIUS)
        refs['Solar_solder_'+colour]=_pv_termination(colour)
    for colour in BAT_PINS:
        refs['Battery_lead_'+colour]=_pipe(battery_path(colour),BAT_RADIUS)
    for i,(x,y) in enumerate(GUARD_POSTS,1):
        refs['Battery_guard_screw_'+str(i)]=_guard_screw(x,y)
        # This is the installed 3.2 mm bore envelope. The insert's outer knurls
        # displace host PETG. The M2 thread is represented by its major envelope.
        refs['Battery_guard_insert_'+str(i)]=_cylinder(x,y,7.50,10.50,1.60).cut(
            _cylinder(x,y,7.45,10.56,1.00))
    return refs


def service_references(opening_mm=12.0, free_length_mm=50.0):
    """Lid-bound purchased references + stationary JST + re-formed wire loop."""
    result={}
    for name,shape in references().items():
        if name=='Battery_plug_JST_ACHR_03V_S':
            result[name]=shape
        elif name.startswith('Battery_lead_'):
            colour=name.rsplit('_',1)[1]
            result[name]=_pipe(battery_path(colour,opening_mm,free_length_mm),BAT_RADIUS)
        elif name.startswith('Battery_'):
            result[name]=shape.translate((0,0,opening_mm))
    return result


COLORS={
    'Battery_guard':(.23,.28,.31), 'Solar_panel_ABRA':(.09,.09,.10),
    'Solar_cells':(.145,.158,.198), 'Solar_collector':(.62,.62,.60),
    'Solar_cell_lines':(.080,.087,.11),
    'Battery_LP223439':(.68,.70,.71), 'Battery_plug_JST_ACHR_03V_S':(.91,.89,.78),
    'Solar_seat_tape':(.35,.36,.37), 'Battery_seat_tape':(.35,.36,.37),
    'Solar_back_contacts':(.67,.65,.59), 'Solar_strain_relief_cord':(.45,.42,.35),
    'Solar_solder_red':(.57,.58,.55), 'Solar_solder_black':(.57,.58,.55),
    'Battery_PCM_Kapton':(.75,.52,.12),
}
for _prefix in ('Solar_lead_', 'Battery_lead_'):
    for _col,_rgb in {'red':(.71,.065,.040),'black':(.075,.073,.070),'yellow':(.91,.71,.06)}.items():
        COLORS[_prefix+_col]=_rgb
for _i in range(1,5):
    COLORS['Battery_guard_screw_'+str(_i)]=(.49,.51,.52)
    COLORS['Battery_guard_insert_'+str(_i)]=(.70,.48,.18)
