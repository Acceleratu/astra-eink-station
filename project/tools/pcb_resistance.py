"""Estimate DC supply-path resistance from the released native centerlines.

A pad is equipotential over its solder land. A track is split at each geometric
junction. Resistance is evaluated along the lowest-resistance path, with a
cylindrical wall for each through via. Ground-plane and source impedances
are outside this centerline calculation.
"""
from collections import defaultdict
from hashlib import sha256
from heapq import heappop, heappush
from math import pi

from shapely.geometry import LineString, Point
from shapely.ops import nearest_points
from shapely.strtree import STRtree

from pcb_check import parse, dims
from pcb_model import BASE, write

COPPER_RHO_20C = 1.724e-8
COPPER_ALPHA = .00393
COPPER_UM = 35.
BARREL_UM = 18.
THICKNESS_MM = 1.


def copper_graph(signal, native):
    pieces = []
    pads = {}
    adj = defaultdict(list)
    def link(a,b,resistance,length=0.,vias=0):
        adj[a].append((b,resistance,length,vias))
        adj[b].append((a,resistance,length,vias))

    for p in native:
        if p['net'] != signal.get('name') or p['kind'] != 'smd':
            continue
        node=('pad',p['name'])
        pads[p['name']]=node
        pieces.append((1,p['geom'],p['geom'],node,None))
    splits = defaultdict(set)
    for k, w in enumerate(signal.findall('wire')):
        axis=LineString([dims(w,'x1','y1'),dims(w,'x2','y2')])
        width=float(w.get('width'))
        if axis.length < .0000001:
            continue
        pieces.append((int(w.get('layer')),axis.buffer(width/2,quad_segs=32),axis,k,width))
        splits[k].update([0.,round(axis.length,6)])
    for j,via in enumerate(signal.findall('via')):
        xy=Point(*dims(via,'x','y'))
        dr=float(via.get('drill'))
        for layer in (1,16):
            pieces.append((layer,xy.buffer(float(via.get('diameter'))/2,quad_segs=32),xy,('via',j,layer),None))
        # Diameter at the inner wall gives a conservative barrel area for the
        # assumed plating thickness; actual plating must be confirmed on coupons.
        barrel=COPPER_RHO_20C*(THICKNESS_MM*.001)/(pi*dr*.001*BARREL_UM*1e-6)
        link(('via',j,1),('via',j,16),barrel,vias=1)
    def at(piece,p):
        axis,key,width=piece[2:]
        if width is None:
            return key
        s=round(axis.project(p),6)
        splits[key].add(s)
        return ('wire',key,s)
    for layer in (1,16):
        local=[p for p in pieces if p[0]==layer]
        index=STRtree([p[1] for p in local])
        for i,p in enumerate(local):
            for j in index.query(p[1],predicate='dwithin',distance=.00020):
                if j<=i:
                    continue
                q=local[j]
                a,b=nearest_points(p[2],q[2])
                link(at(p,a),at(q,b),0.)
    for layer,geom,axis,key,width in pieces:
        if width is None:
            continue
        positions=sorted(splits[key])
        for s,t in zip(positions,positions[1:]):
            length=t-s
            resistance=COPPER_RHO_20C * length / (width*COPPER_UM*1e-6)
            link(('wire',key,s),('wire',key,t),resistance,length=length)
    return pads,adj


def measure(adj,source,target):
    queue=[(0.,0,0.,0,source)]
    done=set()
    sequence=0
    while queue:
        res,_,length,vias,p=heappop(queue)
        if p in done:
            continue
        done.add(p)
        if p==target:
            return res,length,vias
        for q,r,d,n in adj[p]:
            sequence+=1
            if q not in done:
                heappush(queue,(res+r,sequence,length+d,vias+n,q))
    raise ValueError(f"No physical path {source} to {target}")


def main():
    src=BASE/'board/astra.brd'
    board,_,_,objects,*_=parse(src)
    # The currents are independent stress cases, never a summed system load.
    loads=[
        ('VBUS','J101.B9','U103.3',101), ('VBAT','J102.3','U102.2',250),
        ('PV_RAW','J103.1','D102.2',230), ('PV_IN','D102.1','R126.2',230), ('PV_IC_IN','R126.1','U101.20',230),
        ('CHG_IN','U103.2','U102.13',100), ('SYS_AON','U102.10','R124.2',250),
        ('RT_VIN_LOCAL','R124.1','U104.A2',250), ('RT_VOUT_LOCAL','U104.E2','R125.1',250),
        ('VMAIN','R125.2','U201.9',100), ('VMAIN','R125.2','L301.1',250),
        ('VMAIN','R125.2','J301.15',100), ('VMAIN','R125.2','U404.8',5),
        ('VAON','U401.5','U403.8',1)]
    graphs={}
    out=[]
    for net,a,b,current_ma in loads:
        if net not in graphs:
            signal=board.find("signals/signal[@name='"+net+"']")
            graphs[net]=copper_graph(signal,objects)
        pads,adj=graphs[net]
        r,length,vias=measure(adj,pads[a],pads[b])
        h=r*(1+COPPER_ALPHA*(60-20))
        out.append(dict(net=net,source=a,load=b,trace_mm=round(length,3),through_vias=vias,
                        milliohms_20C=round(r*1000,2),milliohms_60C=round(h*1000,2),
                        stress_current_mA=current_ma,drop_mV_60C=round(current_ma*h,2)))
    report=dict(source='board/astra.brd',sha256=sha256(src.read_bytes()).hexdigest(),model=dict(
           trace_copper_um=COPPER_UM,barrel_plating_assumption_um=BARREL_UM,board_thickness_mm=THICKNESS_MM,
           rho_20C_ohm_m=COPPER_RHO_20C,temperature_coefficient_per_K=COPPER_ALPHA),
           limitations='DC positive rail centerlines; equipotential solder lands; lowest-resistance route. No connector, resistor jumper, source, ground plane, inductance or decoupling impedance included. Currents are separate stress cases.',
           paths=out)
    write(BASE/'verification/layout/supply-resistance.json',report)
    for v in out:
        print(v['source'],v['load'],v['trace_mm'],v['drop_mV_60C'])


if __name__=='__main__':
    main()
