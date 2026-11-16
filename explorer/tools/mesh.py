"""Build browser meshes from a qualified enclosure presentation scene and populated PCB STEP."""
import argparse
from collections import defaultdict
from pathlib import Path
import json
import struct

import cadquery as cq
import numpy as np


class Model:
    def __init__(self):
        self.data = bytearray()
        self.doc = {k: [] for k in ('bufferViews', 'accessors', 'materials', 'meshes', 'nodes')}
        self.materials = {}

    def array(self, arr, kind, component, target):
        self.data.extend(b'\0' * (-len(self.data) % 4))
        raw = arr.tobytes()
        view = len(self.doc['bufferViews'])
        self.doc['bufferViews'].append(dict(buffer=0, byteOffset=len(self.data), byteLength=len(raw), target=target))
        self.data.extend(raw)
        acc = dict(bufferView=view, componentType=component, count=len(arr), type=kind)
        if kind == 'VEC3':
            acc.update(min=arr.min(axis=0).tolist(), max=arr.max(axis=0).tolist())
        self.doc['accessors'].append(acc)
        return len(self.doc['accessors']) - 1

    def primitive(self, points, faces, color, alpha=1):
        vertices, inv = np.unique(np.asarray(points, dtype='<f4'), axis=0, return_inverse=True)
        indices = inv[np.asarray(faces).reshape(-1)].reshape(-1)
        ushort = len(vertices) <= 65535
        attrs = {'POSITION': self.array(vertices, 'VEC3', 5126, 34962)}
        index = self.array(indices.astype('<u2' if ushort else '<u4'), 'SCALAR', 5123 if ushort else 5125, 34963)
        key = (*color, alpha)
        if key not in self.materials:
            self.materials[key] = len(self.doc['materials'])
            linear = [((c+.055)/1.055)**2.4 if c>.04045 else c/12.92 for c in color]
            mat = dict(pbrMetallicRoughness=dict(baseColorFactor=[*linear, alpha],metallicFactor=0,roughnessFactor=.74), doubleSided=True)
            if alpha<1:mat['alphaMode']='BLEND'
            self.doc['materials'].append(mat)
        return dict(attributes=attrs, indices=index, material=self.materials[key])

    def node(self, name, group, explode, primitives):
        self.doc['nodes'].append(dict(name=name, mesh=len(self.doc['meshes']), extras=dict(group=group,explode=explode)))
        self.doc['meshes'].append(dict(primitives=primitives))

    def save(self, path):
        self.data.extend(b'\0' * (-len(self.data) % 4))
        parts=list(range(len(self.doc['nodes'])))
        self.doc['nodes'].append(dict(name='CAD_to_metres',children=parts,scale=[.001,.001,.001]))
        self.doc.update(asset=dict(version='2.0'),scenes=[dict(nodes=[len(parts)])],scene=0,buffers=[dict(byteLength=len(self.data))])
        meta=json.dumps(self.doc,separators=(',',':')).encode()
        meta+=b' '*(-len(meta)%4)
        path.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(meta)+len(self.data))+struct.pack('<I4s',len(meta),b'JSON')+meta+struct.pack('<I4s',len(self.data),b'BIN\0')+self.data)
        print(path.name,len(self.doc['nodes']),'nodes',path.stat().st_size,'bytes',flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('scene',type=Path);ap.add_argument('board',type=Path);ap.add_argument('dest',type=Path)
    args=ap.parse_args()
    enclosure=Model()
    scene=json.loads(args.scene.read_text())
    dtype=np.dtype([('normal','<f4',3),('v','<f4',(3,3)),('attribute','<u2')])
    for item in scene['entries']:
        if item['group']=='pcb':continue
        path=args.scene.parent/item['mesh']
        triangles=np.frombuffer(path.read_bytes(),offset=84,dtype=dtype)['v'].reshape(-1,3)
        prim=enclosure.primitive(triangles,np.arange(len(triangles)),item['color'],.13 if item['group']=='lens' else 1)
        enclosure.node(item['id'],item['group'],item['explode'],[prim])
    enclosure.save(args.dest/'enclosure.glb')
    model=Model()
    carrier=next(c for c in cq.Assembly.load(str(args.board)).children if c.name=='Populated_PCB')
    parts=defaultdict(list)
    for shape,path,loc,color in carrier:
        ref=path.split('/')[1]
        vertices,indices=shape.moved(loc).tessellate(.035,.16)
        if not indices:continue
        rgb=color.toTuple()[:3] if color else (.44,.48,.46)
        parts[ref].append(model.primitive([v.toTuple() for v in vertices],indices,rgb))
    for ref,prims in parts.items():model.node(ref,'pcb',[0,0,26],prims)
    model.save(args.dest/'pcb.glb')

if __name__=='__main__':main()
