"""Finite-difference DC sheet model of the native 35 µm bottom ground pour."""
from hashlib import sha256
from math import pi

import numpy as np
from scipy import ndimage
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import factorized
from shapely import intersects_xy
from shapely.geometry import Point
from shapely.ops import unary_union

from pcb_check import parse
from pcb_ground import filled_areas
from pcb_model import BASE, get_design, write
from pcb_resistance import COPPER_ALPHA, COPPER_RHO_20C, COPPER_UM, BARREL_UM, THICKNESS_MM


def solve_sheet(polygon, vias, step):
    """Cell-centered Cartesian finite volume sheet with insulated boundaries."""
    x1,y1,x2,y2=polygon.bounds
    xs=np.arange(x1+step/2,x2,step)
    ys=np.arange(y1+step/2,y2,step)
    xx,yy=xs[None,:],ys[:,None]
    inside=intersects_xy(polygon,xx,yy)
    components, count=ndimage.label(inside)
    areas=np.bincount(components.ravel())
    inside=components==np.argmax(areas[1:])+1
    n=int(inside.sum())
    numbers=np.full(inside.shape,-1,dtype=np.int32)
    numbers[inside]=np.arange(n,dtype=np.int32)
    # Conductance of a square equals the reciprocal of the sheet resistance.
    # Use unit conductance here and scale the resulting voltage by rho/t.
    a=numbers[:,:-1];b=numbers[:,1:];mask=(a>=0)&(b>=0)
    e=a[mask];f=b[mask]
    x=numbers[:-1,:];y=numbers[1:,:];mask=(x>=0)&(y>=0)
    e=np.r_[e,x[mask]];f=np.r_[f,y[mask]]
    diag=np.bincount(e,minlength=n)+np.bincount(f,minlength=n)
    row=np.r_[np.arange(n),e,f];col=np.r_[np.arange(n),f,e]
    values=np.r_[diag.astype(float),-np.ones(2*e.size)]
    system=coo_matrix((values,(row,col)),shape=(n,n)).tocsc()
    def ring(pt):
        hit=(xx-pt.x)**2+(yy-pt.y)**2 <= .30**2
        idx=numbers[inside & hit]
        if not idx.size:
            raise ValueError(f"No ground-plane catchment cells at {pt.wkt} for {step} mm mesh")
        return idx
    contact={name:ring(q) for name,q in vias.items()}
    sink=contact['C115.2']
    free=np.ones(n,dtype=bool)
    free[sink]=False
    solve=factorized(system[free,:][:,free].tocsc())
    sheet=COPPER_RHO_20C/(COPPER_UM*1e-6)
    out={}
    for k,cells in contact.items():
        if k=='C115.2':
            continue
        rhs=np.zeros(n);rhs[cells]=1/len(cells)
        voltage=np.zeros(n);voltage[free]=solve(rhs[free])
        residual=system @ voltage-rhs
        out[k]=dict(sheet_milliohms_20C=round(float(voltage[cells].mean()*sheet*1000),5),
                    source_cells=len(cells),grounded_cells=len(sink),
                    sink_current_A=round(float(-residual[sink].sum()),9),
                    max_abs_free_residual_A=float(np.max(np.abs(residual[free]))))
        if abs(out[k]['sink_current_A']-1.)>1e-6 or out[k]['max_abs_free_residual_A']>1e-7:
            raise ArithmeticError("Sheet current conservation failed")
    return dict(step_mm=step,connected_cells=n,paths=out)


def main():
    d=get_design();src=BASE/'board/astra.brd'
    _,_,_,objs,holes,r,p,c,_=parse(src)
    solid=max(filled_areas(16,objs,p,c,r,holes),key=lambda g:g.area)
    solid=solid.difference(unary_union([h for _,_,h in holes]))
    gnd=[v['geom'].centroid for v in objs if v['kind']=='via' and v['net']=='GND']
    refs=('C115.2','U201.37','C302.2','C109.2')
    ends={}
    for name in refs:
        pad=Point(d.pads[tuple(name.split('.'))]['center'])
        ends[name]=min(gnd,key=lambda g:g.distance(pad))
    meshes=[solve_sheet(solid,ends,h) for h in (.28,.19,.13,.10)]
    barrel=COPPER_RHO_20C*THICKNESS_MM*.001/(pi*.30*.001*BARREL_UM*1e-6)
    paths={}
    for k in refs[1:]:
        prev=meshes[-2]['paths'][k]['sheet_milliohms_20C']
        last=meshes[-1]['paths'][k]['sheet_milliohms_20C']
        total=(2*barrel*1000+last)*(1+COPPER_ALPHA*40)
        paths[k]=dict(finest_sheet_milliohms_20C=last,
            fine_vs_previous_percent=round(100*abs(last-prev)/last,2),
            bottom_sheet_and_two_barrels_milliohms_60C=round(total,4),
            at_250mA_drop_mV=round(total*.25,4))
    report=dict(sha256=sha256(src.read_bytes()).hexdigest(),source='board/astra.brd',
        copper_um=COPPER_UM,via_barrel_assumed_um=BARREL_UM,grounded_via_near='C115.2',
        via_centers_mm={k:[round(p.x,6),round(p.y,6)] for k,p in ends.items()}, meshes=meshes,
        paths=paths,limitations='DC finite-difference model of B.Cu alone. Actual via holes removed; uniform 1 A distributed into the copper annulus cells. Component-to-via F.Cu copper, F.Cu plane parallel paths, contact resistance, etch variation and AC inductance are outside this model.')
    write(BASE/'verification/layout/ground-plane-resistance.json',report)
    for k,val in paths.items():
        print(k,val,flush=True)


if __name__=='__main__':
    main()
