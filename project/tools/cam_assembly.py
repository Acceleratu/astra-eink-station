#!/usr/bin/env python3
"""Write JLC assembly tables and independently compare numbered lands to distributor CAD."""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from cam_stock import MODULES, ROOT, populated


HEADERS={'Accept':'application/json','Referer':'https://jlcpcb.com/','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36'}


def catalog(code):
    url=f'https://easyeda.com/api/products/{code}/components?version=6.5.51'
    result={'code':code,'source':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
    try:
        last_error=None
        for host in ('easyeda.com','lceda.cn','www.lceda.cn'):
            url=f'https://{host}/api/products/{code}/components?version=6.5.51'
            try:
                with urlopen(Request(url,headers=HEADERS),timeout=15) as response: raw=response.read()
                response=json.loads(raw)
                if not response.get('result'): raise ValueError(response.get('message') or 'No public component library')
                doc=response['result']['packageDetail'];result['source']=url;break
            except (OSError,ValueError,KeyError) as err:
                last_error=err
        else: raise last_error
        data=doc['dataStr']; pads={};multiple=[]
        for item in data['shape']:
            if not item.startswith('PAD~'): continue
            fields=item.split('~');name=fields[8]
            if name in pads: multiple.append(name)
            pads[name]=[float(fields[2])*.254,-float(fields[3])*.254]
        # Mirror the drawing's downwards screen axis to the Cartesian top view. An
        # asymmetric 3- or 4-sided package independently constrains the handedness.
        result.update(title=doc['title'],uuid=doc.get('uuid'),sha256=hashlib.sha256(raw).hexdigest(),pads=pads,repeated_numbers=multiple)
    except Exception as err:
        result['error']=str(err)
    return code,result


def csvwrite(path,header,lines):
    with path.open('w',newline='') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(lines)


def rotate(p,theta):
    a=math.radians(theta)
    return p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a)


def mean(points):return tuple(sum(v)/len(points) for v in zip(*points))


def fit(src,dst):
    cs,cd=mean(src),mean(dst)
    src=[(x-cs[0],y-cs[1]) for x,y in src];dst=[(x-cd[0],y-cd[1]) for x,y in dst]
    dot=sum(x*u+y*v for (x,y),(u,v) in zip(src,dst));cross=sum(x*v-y*u for (x,y),(u,v) in zip(src,dst))
    theta=math.degrees(math.atan2(cross,dot));nom=round(theta/90)*90
    # SMT variants usually rotate footprints in right angles. Preserve a documented
    # non-orthogonal placement separately rather than estimating it from rounded land art.
    errors=[math.dist(rotate(source,nom),target) for source,target in zip(src,dst)]
    return nom%360,round(abs(theta-nom),3),round(max(errors),4),round((sum(e**2 for e in errors)/len(errors))**.5,4)


def reference_rows(parts,footprints,out):
    codes=sorted({p['lcsc'] for p in parts if p.get('lcsc')})
    cache=out/'catalog-land-centers.json'
    catalogs={k:v for k,v in json.loads(cache.read_text()).items() if k in codes and v.get('pads')} if cache.exists() else {}
    with ThreadPoolExecutor(max_workers=3) as pool: catalogs.update(dict(pool.map(catalog,[c for c in codes if c not in catalogs])))
    out.mkdir(parents=True,exist_ok=True);(out/'catalog-land-centers.json').write_text(json.dumps(catalogs,indent=2,sort_keys=True)+'\n')
    results={}
    for part in parts:
        code=part.get('lcsc')
        key=(code,part['footprint'])
        if key in results:continue
        ds=catalogs.get(code,{});g=footprints[part['footprint']]
        ours={str(p['n']):(p['x'],p['y']) for p in g['pads']}
        mapped={str(k):str(v) for k,v in g.get('jlc_pad_names',{}).items()}
        a,b=[],[];common=[]
        for k,v in ours.items():
            pname=mapped.get(k,k)
            if pname in ds.get('pads',{}) and pname not in ds.get('repeated_numbers',[]):
                a.append(ds['pads'][pname]);b.append(v);common.append(k)
        coil_reel=part['mpn']=='XGL4015-471MEC' and len(a)<2
        if coil_reel:
            # Coilcraft: C above the value with the feed holes at the top. The
            # bar/short end is above C. A local land 1 at -X receives that end.
            # 2.37 mm is the manufacturer's centre-to-centre land dimension.
            common=['1','2'];a=[(0,1.185),(0,-1.185)];b=[ours[k] for k in common]
        fitdata=(None,None,None,None) if len(a)<2 else fit(a,b)
        r={'mpn':part['mpn'],'footprint':part['footprint'],'vendor_footprint':ds.get('title'),
            'design_land_count':len(ours),'vendor_land_count':len(ds.get('pads',{})),'named_land_pairs':common,
            'rotation_from_catalog_deg':fitdata[0],'deviation_from_orthogonal_deg':fitdata[1],
            'max_center_deviation_mm':fitdata[2],'rms_center_deviation_mm':fitdata[3]}
        if len(a)>=3:
            # Compare rigid fit to mirror alternative only for non-collinear point sets.
            cross=max(abs((x-a[0][0])*(v-a[0][1])-(y-a[0][1])*(u-a[0][0])) for x,y in a for u,v in a)
            if cross>.1: r['mirrored_rms_deviation_mm']=fit([(-x,y) for x,y in a],b)[3]
        if fitdata[0] is None: r['assessment']='Missing numbered pad pairs'
        elif fitdata[1]>3 or fitdata[2]>.65: r['assessment']='Compare with manufacturer land drawing'
        else: r['assessment']='Orientation matched by pad numbers'
        if coil_reel:
            r.update(assessment='Orientation matched to Coilcraft carrier tape, start lead to pad 1',
                     orientation_source='https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xgl/xgl4015/',
                     zero_rule='https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2',
                     evidence=['coilcraft-physical.gif','coilcraft-tape.gif','coilcraft-orientation.gif'])
        results[key]=r
    (out/'rotation-review.json').write_text(json.dumps({c+'/'+fp:r for (c,fp),r in results.items()},indent=2,sort_keys=True)+'\n')
    return results


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,default=ROOT/'board/astra.brd')
    ap.add_argument('--fab',type=Path,default=ROOT/'fab');ap.add_argument('--verify',type=Path,default=ROOT/'verification/manufacturing/assembly')
    ap.add_argument('--independent-pos',type=Path,default=ROOT/'verification/manufacturing/independent-board/raw-placements.csv')
    ap.add_argument('--modules',nargs='*',default=MODULES);ap.add_argument('--review-only',action='store_true');args=ap.parse_args()
    data=[p for name in args.modules for p in json.loads((ROOT/f'hardware/{name}.json').read_text())['parts']]
    allparts={p['ref']:p for p in data}
    if len(data)!=len(allparts):raise ValueError('Duplicate board designator')
    g={k:v for path in (ROOT/'hardware').glob('*-footprints.json') for k,v in json.loads(path.read_text()).items()}
    parts=[p for p in data if populated(p)]
    rots=reference_rows(parts,g,args.verify)
    for c,r in rots.items(): print(c,r['mpn'],r['rotation_from_catalog_deg'],r['named_land_pairs'][:3], r['max_center_deviation_mm'],r['assessment'])
    if args.review_only:return
    board=ET.parse(args.board).find('drawing/board');elements={e.get('name'):e for e in board.findall('elements/element')}
    if set(elements)!=set(allparts):raise ValueError('Native board and BOM part designators differ: '+str(sorted(set(elements)^set(allparts))))
    args.fab.mkdir(parents=True,exist_ok=True)
    groups=defaultdict(list);cpl=[];assembly=[];omitted=[]
    for ref,p in sorted(allparts.items()):
        el=elements[ref];rotation=el.get('rot','R0');
        if 'M' in rotation: raise ValueError(f'Unexpected bottom placement {ref}')
        attrs={v.get('name'):v.get('value','') for v in el.findall('attribute')}
        if el.get('package')!=p['footprint'] or (populated(p) and (attrs.get('MPN')!=p['mpn'] or attrs.get('LCSC')!=p['lcsc'])):
            raise ValueError(f'Native and procurement identity differ for {ref}: {attrs}')
        ang=float(rotation.split('R')[-1]);geom=g[p['footprint']];x=float(el.get('x'));y=float(el.get('y'))
        if not populated(p):omitted.append((ref,p['value'],p['footprint'],round(x,4),round(y,4)));continue
        r=rots[(p['lcsc'],p['footprint'])];bias=g[p['footprint']].get('body_center',(0,0));bx,by=rotate(bias,ang);x+=bx;y+=by
        corrections=geom.get('jlc_rotation_deg',None);base=r['rotation_from_catalog_deg']
        correction=corrections if corrections is not None else (base or 0);cpl_deg=(ang+correction)%360
        groups[(p['mpn'],p['lcsc'],p['value'],p['footprint'])].append(ref)
        cpl.append((ref,f'{x:.4f}',f'{y:.4f}','Top',f'{cpl_deg:g}'))
        assembly.append((ref,p['mpn'],p['lcsc'],p['footprint'],p['value'],p['height_mm'],f'{x:.4f}',f'{y:.4f}',f'{ang:g}',f'{cpl_deg:g}',r['assessment']))
    csvwrite(args.fab/'BOM-JLCPCB.csv',('Comment','Designator','Footprint','LCSC Part #','Manufacturer Part Number','Quantity per board'),
             [(val,','.join(refs),fp,code,mpn,len(refs)) for (mpn,code,val,fp),refs in sorted(groups.items())]);
    csvwrite(args.fab/'CPL-JLCPCB.csv',('Designator','Mid X','Mid Y','Layer','Rotation'),cpl)
    csvwrite(args.verify/'fitted-parts.csv',('Designator','MPN','JLCPCB','Package','Value','Height mm','Body center X mm','Body center Y mm','EAGLE rotation deg','CPL rotation deg','Catalog orientation'),assembly)
    csvwrite(args.verify/'unpopulated.csv',('Designator','Value','Footprint','Origin X mm','Origin Y mm'),omitted)
    with args.independent_pos.open(newline='') as f:
        imported={row['Ref']:row for row in csv.DictReader(f)}
    checked=[]
    for ref,mpn,code,fp,value,height,cx,cy,native_angle,placement_angle,review in assembly:
        row=imported[ref];theta=float(row['Rot']);dx,dy=rotate(g[fp].get('body_center',(0,0)),theta)
        discrepancy=math.dist((float(row['PosX'])+dx,float(row['PosY'])+dy),(float(cx),float(cy)))
        angle_error=abs((theta-float(native_angle)+180)%360-180)
        if row['Side']!='top' or row['Package']!=fp or discrepancy>.0002 or angle_error>.01:
            raise ValueError(f'Independent CAD position differs for {ref}: {row}')
        checked.append({'ref':ref,'cad_position_error_mm':round(discrepancy,6),'cad_rotation_error_deg':round(angle_error,5),
                        'catalog_correction_deg':(float(placement_angle)-theta)%360})
    (args.verify/'placement-vs-import.json').write_text(json.dumps({'source':args.board.name,
        'source_sha256':hashlib.sha256(args.board.read_bytes()).hexdigest(),'compared_rows':len(checked),'placements':checked},indent=2)+'\n')

if __name__=='__main__':main()
