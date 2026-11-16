"""Regenerate the enclosure, the installed STEP assembly and the presentation mesh manifest.

Usage: python build.py --output /path/to/enclosure --scene /path/to/review-scene
CadQuery 2.6.1, Shapely 2, Pillow and matplotlib are required. All native units are mm.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from PIL import Image
from shapely.geometry import box as rect
from shapely.ops import unary_union

import buttons
import housing as h
import power_parts as power
import stand
import usb_internal
import usb_mask

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BOARD_DIGEST='195c8935a587a71a5b7a1ee811ed1843ba1d3083438c911b11dcff17b4931b00'
SHELL=(.78,.78,.70); LID=(.22,.26,.26); CRADLE=(.17,.21,.21); KEY=(.81,.47,.16)
GREY=(.38,.43,.43); FOAM=(.24,.25,.23); STEEL=(.64,.66,.65); BRASS=(.70,.51,.24)


def sha(path):
    with path.open('rb') as source: return hashlib.file_digest(source,'sha256').hexdigest()


def compound(shapes):
    return cq.Compound.makeCompound(list(shapes))

def remove_repeated_vertex_facets(path):
    """Discard only binary STL records with two bit-identical vertex coordinates."""
    data=path.read_bytes();count=struct.unpack_from('<I',data,80)[0]
    if len(data)!=84+50*count:
        raise ValueError(f'Unexpected STL encoding in {path.name}')
    triangles=[data[i:i+50] for i in range(84,len(data),50)]
    kept=[r for r in triangles if len({r[12:24],r[24:36],r[36:48]})==3]
    if len(kept)!=count:
        path.write_bytes(data[:80]+struct.pack('<I',len(kept))+b''.join(kept))
    return count-len(kept)


def on_bed(shape,reverse=False):
    rotation=cq.Location((0,0,0),(1,0,0),180 if reverse else 0)
    b=Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.moved(rotation).wrapped,b,False,False)
    x0,y0,z0,x1,y1,_=b.Get()
    return cq.Location((-(x1+x0)/2,-(y1+y0)/2,-z0))*rotation


def loc_matrix(loc):
    t=loc.wrapped.Transformation()
    return [[round(t.Value(i,j),10) for j in (1,2,3,4)] for i in (1,2,3)]+[[0,0,0,1]]


def ink():
    img=Image.open(ROOT/'verification/firmware/reference-frame.png').convert('L')
    if img.size!=(400,300): raise ValueError('Firmware preview has different pixel dimensions')
    pixels=img.load(); runs=[]
    for row in range(img.height):
        col=0
        while col<img.width:
            if pixels[col,row]>=128:
                col+=1;continue
            end=col+1
            while end<img.width and pixels[end,row]<128: end+=1
            runs.append(rect(col,row,end,row+1)); col=end
    areas=unary_union(runs)
    def wire(ring):
        return cq.Wire.makePolygon([(27.55+x*.212,-87.50+y*.212,-.016) for x,y in ring.coords[:-1]],close=True)
    solids=[cq.Solid.extrudeLinear(wire(poly.exterior),[wire(hole) for hole in poly.interiors],(0,0,.004)) for poly in areas.geoms]
    return compound(solids)


class Release:
    def __init__(self,out,scene):
        self.out,self.scene=out,scene
        self.assembly=cq.Assembly(name='Astra_Enclosure_A');self.entries=[];self.prints={};self.physical={}
        for sub in ('print','cad','templates','verification'): (out/sub).mkdir(parents=True,exist_ok=True)
        scene.mkdir(parents=True,exist_ok=True)

    def mesh(self,label,shape,rgb,group,explode):
        path=self.scene/(label+'.stl')
        shape.exportStl(str(path),tolerance=.035,angularTolerance=.14,relative=False)
        self.entries.append(dict(id=label,mesh=path.name,color=list(rgb[:3]),group=group,explode=explode))

    def component(self,name,shape,rgb,group,offset=(0,0,0), *,show=True):
        if shape.isNull() or not shape.Solids() or not shape.isValid(): raise ValueError('Invalid body: '+name)
        self.assembly.add(shape,name=name,color=cq.Color(*rgb)); self.physical[name]=shape
        if show: self.mesh(name.lower(),shape,rgb,group,offset)

    def printable(self,name,shape,rgb,group,offset, *,reverse=False,print_shape=None,pose=None):
        self.component(name,shape,rgb,group,offset)
        if len(shape.Solids())!=1: raise ValueError(f'Print part {name} contains {len(shape.Solids())} bodies')
        if print_shape is None:
            pose=pose or on_bed(shape,reverse); print_shape=shape.moved(pose)
        path=self.out/'print'/(name+'.stl')
        print_shape.exportStl(str(path),tolerance=.035,angularTolerance=.14,relative=False)
        removed=remove_repeated_vertex_facets(path)
        j=dict(sha256=sha(path),volume_mm3=round(shape.Volume(),4),assembly_name=name,
               zero_area_facets_removed=removed)
        if pose is not None: j['assembly_to_print']=loc_matrix(pose)
        self.prints[path.name]=j

    def electronics(self,source):
        if sha(source)!=BOARD_DIGEST: raise ValueError('Unqualified electronics STEP')
        original=cq.Assembly.load(str(source));carrier=next(c for c in original.children if c.name=='Populated_PCB')
        self.assembly.add(carrier,name='Populated_PCB')
        groups=defaultdict(list)
        for shape,path,pose,color in carrier:
            ref=path.split('/')[1]; tint=tuple(round(c,4) for c in color.toTuple()[:3]) if color else GREY
            label=ref if ref in ('PCB_1mm','Exposed_lands','J101','J102','J301','U201','U404','SW401','SW402','SW403') else 'components'
            groups[label,tint].append(shape.moved(pose))
        for i,((label,tint),shapes) in enumerate(groups.items()):
            self.mesh(f'board_{label}_{i}',compound(shapes),tint,'pcb',(0,0,26))


def drawings(out):
    wire=h.outline((0,0,100.6,79.7),2.7,0)
    cq.exporters.export(cq.Workplane('XY').add(wire),str(out/'templates/Lens-1mm-PC.dxf'))
    # Both exact contours of the tape ring share the lens' local lower-left datum.
    tape=h.lens_tape();face=max(tape.Faces(),key=lambda f:f.Area())
    wires=[w.translate((-19.65,95.55,7.75)) for w in face.Wires()]
    cq.exporters.export(cq.Workplane('XY').add(compound(wires)),str(out/'templates/Lens-tape-0p2mm.dxf'))
    usb_mask.drawings(out/'templates')
    usb_internal.drawings(out/'templates')


def run(out,scene):
    sources=tuple(HERE/name for name in ('build.py','housing.py','buttons.py','stand.py','power_parts.py',
                                         'usb_pocket.py','usb_mask.py','usb_internal.py'))
    source_hashes={f.name:sha(f) for f in sources}
    r=Release(out,scene)
    r.printable('Front_shell',h.front_shell(power),SHELL,'front',(0,0,-5))
    r.printable('Rear_cover',h.rear_shell(power,buttons),LID,'rear',(0,0,77),reverse=True)
    r.printable('Display_retainer',h.display_retainer(),GREY,'retainer',(0,0,35))
    for name,y,anchor_y in [('Upper_PCB_rail',3.8,h.UPPER_RAIL_Y),('Lower_PCB_rail',80.2,h.LOWER_RAIL_Y)]:
        r.printable(name,h.carrier(y,anchor_y),GREY,'rail',(0,0,13))
    for name,shape in power.parts().items(): r.printable(name,shape,power.COLORS.get(name,GREY),'battery_guard',(0,0,57))
    bed_keys=buttons.print_parts()
    for name,shape in buttons.parts().items():
        key=name.startswith('SW');label='Key_'+name if key else name
        r.printable(label,shape,KEY if key else GREY,'key' if key else 'keeper',(0,0,69 if key else 55),print_shape=bed_keys[name])
    r.printable('Desktop_stand',stand.assembled_shape(),CRADLE,'stand',(0,32,0),pose=stand.pcb_to_print_location())
    for provider in (usb_mask,usb_internal):
        for label,shape in provider.references().items():
            r.component(label,shape,provider.COLORS[label],'usb_mask',(0,0,26))
    for label,shape in h.display_references().items():
        if label=='Display_active': color,group,sep=(.84,.85,.77),'display',8
        elif label=='Display_glass': color,group,sep=(.37,.38,.34),'display',8
        elif label=='Display_FPC': color,group,sep=(.79,.48,.16),'flex',8
        elif label=='Optical_lens': color,group,sep=(.86,.94,.92,.15),'lens',-28
        elif label=='Lens_tape': color,group,sep=FOAM,'seal',-19
        else: color,group,sep=FOAM,'pads',8
        r.component(label,shape,color,group,(0,0,sep))
    r.component('Display_reference_ink',ink(),(.13,.15,.15),'ink',(0,0,8),show=False)
    for label,shape in power.references().items():
        group='pv' if label.startswith('Solar') else 'battery'
        r.component(label,shape,power.COLORS.get(label,STEEL),group,(0,0,-17 if group=='pv' else 63))
    for label,shape in h.board_fasteners().items():
        color=BRASS if 'insert' in label.lower() else STEEL
        sep=95 if label.startswith('Case_screw_') else 17 if label.startswith('Rail_') else 33
        if label.startswith('Case_insert_'): sep=-5
        r.component(label,shape,color,'fixing',(0,0,sep))
    for label,shape in buttons.hardware().items(): r.component('Key_'+label,shape,STEEL,'fixing',(0,0,52))
    r.electronics(ROOT/'mechanical/astra.step')
    dest=out/'cad/Astra-enclosure-assembly.step';r.assembly.save(str(dest))
    drawings(out)
    # A manifest for Blender and an independent assembly-to-print registration record.
    board_points=stand.pcb_to_print_matrix()
    scene_data=dict(units='mm',front=[0,0,-1],up=[0,-1,0],desk_transform=board_points,entries=r.entries,
        screen=dict(entity='display_active',image=str(ROOT/'verification/firmware/reference-frame.png'),origin_mm=[27.55,-23.90,-.012],
                    u=[1,0,0],v=[0,-1,0],normal=[0,0,-1],size_mm=[84.80,63.60]))
    (scene/'scene.json').write_text(json.dumps(scene_data,indent=2)+'\n')
    if source_hashes!={f.name:sha(f) for f in sources}:
        raise RuntimeError('Mechanical sources changed during generation. Rebuild from the frozen revision.')
    usb_bodies={n:{'solid_count':len(s.Solids()),'volume_mm3':round(s.Volume(),7)}
                for n,s in r.physical.items() if n.startswith('USB_')}
    info=dict(source_electronics_sha256=BOARD_DIGEST,assembly_step_sha256=sha(dest),case_bounds_mm=list(h.OUTLINE),
              front_z=h.FRONT_Z,back_z=h.BACK_Z,printed_parts=r.prints,mechanical_components=list(r.physical),
              usb_bodies=usb_bodies, source_sha256=source_hashes,
              cutting_templates={p.name:sha(p) for p in sorted((out/'templates').glob('*.dxf'))})
    (out/'verification/build.json').write_text(json.dumps(info,indent=2)+'\n')
    print(f'{len(r.prints)} printable pieces, {len(r.physical)} native mechanical components and the populated PCB; {dest.stat().st_size} STEP bytes',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE)
    p.add_argument('--scene',type=Path,default=Path('/tmp/astra-enclosure/scene'))
    args=p.parse_args();run(args.output,args.scene)
