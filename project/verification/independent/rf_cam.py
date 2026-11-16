#!/usr/bin/env python3
"""Independently measure finished RF copper in Gerbv's rendered photoplots.

Requires Gerbv, Pillow and Shapely. Example:
  uv run --with pillow --with shapely verification/independent/rf_cam.py --top path/F_Cu.gbr --bottom path/B_Cu.gbr
All coordinates come from actual placement and the published module dimensions.
The render is a complementary 10 µm/pixel check, not a full copper-net extraction.
"""
from argparse import ArgumentParser
from hashlib import sha256
import json
from math import floor,ceil
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET
from PIL import Image
from shapely.geometry import Point,box
from rf_geometry import ROOT,HERE,place,pads,segment,poly,xy

S=100  # px/mm at 2540 DPI
def render(gerbv,path,target,roi):
    x0,y0,x1,y1=roi
    cmd=[gerbv,'-x','png','-D',str(round(S*25.4)),'-w',f'{round((x1-x0)*S)}x{round((y1-y0)*S)}',
         '-O',f'{x0/25.4:.6f};{y0/25.4:.6f}','-B','0','-b','#000000','-f','#FFFFFF','-o',str(target),str(path)]
    run=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
    if run.returncode:raise RuntimeError(run.stderr+run.stdout)
    with Image.open(target) as image:return image.convert('L').point(lambda i:255 if i>=32 else 0)
def px(x,y,roi):return (round((x-roi[0])*S),round((roi[3]-y)*S))
def geom_bbox(geom,roi):
    left,bottom,right,top=geom.bounds
    return (*px(left,top,roi),*px(right,bottom,roi))
def copper_fraction(mask,geometry,roi):
    sub=mask.crop(geom_bbox(geometry,roi))
    return sub.histogram()[255]/(sub.width*sub.height)
def self_test(gerbv):
    # Positive and negative controls. Asymmetric native-coordinate flashes
    # detect translation, scale and mirroring errors independently of the board.
    with TemporaryDirectory() as work:
        work=Path(work)
        src=work/'synthetic.gbr'
        src.write_text('G04 Synthetic coordinate control*\n%FSLAX36Y36*%\n%MOMM*%\n%ADD10C,1.000*%\n%LPD*%\nD10*\nX100000000Y50000000D03*\nX110000000Y60000000D03*\nM02*\n')
        roi=98,48,117,64
        mask=render(gerbv,src,work/'synthetic.png',roi)
        assert mask.size==(1900,1600)
        assert [bool(mask.getpixel(px(x,y,roi))) for x,y in ((100,50),(110,60),(110,50),(100,60))]==[True,True,False,False]
        assert abs(copper_fraction(mask,box(99,49,101,51),roi)-3.14159/16)<.005

def returns(doc,gerbv,bottom,out):
    """Look at actual bottom copper separately from the absence of native foreign tracks."""
    b=doc.find('.//board');elements={e.get('name'):e for e in b.findall('elements/element')}
    pkgs={(l.get('name'),p.get('name')):p for l in b.findall('libraries/library') for p in l.findall('packages/package')}
    foreign=[]; contacts={}
    for net in b.findall('signals/signal'):
        n=net.get('name')
        for c in net.findall('contactref'):contacts[c.get('element'),c.get('pad')]=n
        if n=='GND':continue
        for w in net.findall("wire[@layer='16']"):foreign.append((n,segment(w).buffer(float(w.get('width'))/2)))
        for v in net.findall('via'):foreign.append((n,Point(xy(v)).buffer(float(v.get('diameter',v.get('drill')))/2)))
        for p in net.findall("polygon[@layer='16']"):
            if p.get('pour')!='cutout':foreign.append((n,poly(p)))
    for el,e in elements.items():
        for pin,g,l in pads(pkgs[(e.get('library'),e.get('package'))]):
            n=contacts.get((el,pin),'NC')
            if l in ('both','16') and n!='GND':foreign.append((f'{el}.{pin}/{n}',place(g,e)))
    areas=[('RT6160 hot loop','U104',(-2.1,-4.7,2.2,.7)),('SPV1050 switch return','U101',(-.8,-.6,4.9,1.6)),
           ('SSD1683 booster return','Q301',(-4.95,-.75,9.75,5.35)),('RTC external crystal','Y401',(-.8,-1.65,3.1,1.7))]
    result={}
    for name,ref,(dx0,dy0,dx1,dy1) in areas:
        x,y=xy(elements[ref]);bounds=(x+dx0,y+dy0,x+dx1,y+dy1);core=box(*bounds)
        roi=(floor(bounds[0])-1,floor(bounds[1])-1,ceil(bounds[2])+1,ceil(bounds[3])+1)
        mask=render(gerbv,bottom,out/f'return-{ref}-gerbv.png',roi)
        result[ref]={'function':name,'bounds_mm':[round(t,4) for t in bounds],
                     'foreign_native_bottom_nets':sorted({n for n,g in foreign if g.intersects(core)}),
                     'bottom_copper_fraction_before_drill':round(copper_fraction(mask,core,roi),6)}
    return result

def audit(board,top,bottom,out,gerbv,receipt=None):
    doc=ET.parse(board);mod=doc.find(".//board/elements/element[@name='U201']")
    lib=doc.find(f".//board/libraries/library[@name='{mod.get('library')}']")
    pkg=lib.find(f"packages/package[@name='{mod.get('package')}']")
    full=place(box(-6,-8.6,6,8.6),mod)
    # Whole antenna core including its small over-carrier strip. Core bounds
    # lie inside the Ebyte art and avoid the illustrator's ±0.2mm envelope.
    ant=place(box(-5.85,3.65,5.85,8.35),mod)
    shield=place(box(-4.25,-6.8,4.25,2.5),mod)
    a,b,c,d=full.bounds;roi=floor(a)-1,floor(b)-1,ceil(c)+1,ceil(d)+1
    controls={n:place(g,mod).centroid for n,g,l in pads(pkg) if n in ('9','10','37','38','39','40')}
    result={'method':'Gerbv command-line render of original exported photoplots; synthetic orientation/scale controls and six physical reference pads.',
            'native_board_sha256':sha256(board.read_bytes()).hexdigest(),'roi_mm':roi,
            'micrometers_per_pixel':1000/S,'files':{},'errors':[]}
    for layer,path in [('top',top),('bottom',bottom)]:
        output=out/f'rf-{layer}-gerbv.png';mask=render(gerbv,path,output,roi)
        ant_f=copper_fraction(mask,ant,roi)
        record={'source':path.name,'sha256':sha256(path.read_bytes()).hexdigest(),
                'antenna_copper_fraction':round(ant_f,8),'shield_core_copper_fraction':round(copper_fraction(mask,shield,roi),6)}
        if ant_f:result['errors'].append(f'{layer} contains plotted copper in antenna core')
        if layer=='top':
            record['module_pad_controls']={n:bool(mask.getpixel(px(p.x,p.y,roi))) for n,p in controls.items()}
            if len(controls)!=6 or not all(record['module_pad_controls'].values()):result['errors'].append('Top pad controls absent; do not infer an empty antenna from an unregistered render')
        elif record['shield_core_copper_fraction']<.85:
            result['errors'].append('Less than 85% copper in protected carrier shield core')
        result['files'][layer]=record
    result['bottom_reference_regions']=returns(doc,gerbv,bottom,out)
    for ref,ar in result['bottom_reference_regions'].items():
        if ar['foreign_native_bottom_nets'] or ar['bottom_copper_fraction_before_drill']<.99:
            result['errors'].append(f'{ref}: return region contains foreign copper or less than 99% actual copper photoplot')
    if receipt is not None:
        cam=json.loads(receipt.read_text()); linked=cam['source_sha256']==result['native_board_sha256']
        linked=linked and all(cam['file_sha256'].get(f['source'])==f['sha256'] for f in result['files'].values())
        result['registered_CAM_export']={'file':receipt.name,'sha256':sha256(receipt.read_bytes()).hexdigest(),
                                         'identical_board_and_plots':linked}
        if not linked:result['errors'].append('CAM manifest and native board / actual copper photoplots have different SHA-256 hashes')
    result['status']='FAIL' if result['errors'] else 'PASS'
    (out/'rf-gerber.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def main():
    ap=ArgumentParser(description=__doc__)
    ap.add_argument('--board',type=Path,default=ROOT/'board/astra.brd')
    ap.add_argument('--top',type=Path);ap.add_argument('--bottom',type=Path)
    ap.add_argument('--receipt',type=Path,help='Require a matching gerber-vs-native.json receipt for the final check')
    ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args();viewer=shutil.which('gerbv')
    if not viewer:ap.error('gerbv unavailable')
    self_test(viewer)
    if args.self_test:
        print('PASS Gerbv coordinates: two asymmetric synthetic positive flashes, two negative controls and area test.');return
    if not(args.top and args.bottom and args.board.is_file()):ap.error('native board plus --top and --bottom Gerber files required')
    args.output_dir.mkdir(parents=True,exist_ok=True)
    result=audit(args.board,args.top,args.bottom,args.output_dir,viewer,args.receipt)
    print(result['status'],result['files'],result['errors'])
    raise SystemExit(bool(result['errors']))

if __name__=='__main__':main()
