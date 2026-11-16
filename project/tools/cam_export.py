#!/usr/bin/env python3
"""Import the native board into KiCad and reopen every exported fabrication layer."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
from cam_geometry import check, edge_centers, native_axis
from shapely.ops import polygonize

ROOT=Path(__file__).resolve().parents[1]


def run(args,log,allowed=(0,)):
    proc=subprocess.run([str(a) for a in args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    with log.open('a') as file:
        file.write('$ '+str(args[0])+' '+' '.join(map(str,args[1:]))+'\n'+proc.stdout+f'\nexit {proc.returncode}\n')
    if proc.returncode not in allowed: raise RuntimeError(f'{args[0]} returned {proc.returncode}: {proc.stdout[-800:]}')
    return proc


def rules(out,name,source):
    # These are supplier design thresholds, set *before* running DRC. Native board
    # settings and the geometric independent extraction are retained alongside them.
    r={'min_clearance':.10,'min_connection':0,'min_copper_edge_clearance':.20,
       'min_hole_clearance':.20,'min_hole_to_hole':.20,'min_silk_clearance':.15,
       'min_text_height':1.0,'min_text_thickness':.15,'min_through_hole_diameter':.15,
       'min_track_width':.10,'min_via_annular_width':.075,'min_via_diameter':.25,
       'solder_mask_to_copper_clearance':.09,'max_error':.002,
       'min_resolved_spokes':2}
    native=ET.parse(source).find('drawing/board')
    values={p.get('name'):p.get('value') for p in native.findall('designrules/param')}
    def native_mm(key,fallback):
        value=values.get(key)
        if not value:return fallback
        raw=re.fullmatch(r'([0-9.]+)(mm|mil|inch)?',value)
        if not raw:raise ValueError(f'Unsupported design-rule dimension {key}: {value}')
        return float(raw.group(1))*{'mm':1,'mil':.0254,'inch':25.4,None:1}[raw.group(2)]
    r['min_clearance']=max(r['min_clearance'],native_mm('mdWireWire',0))
    r['min_track_width']=max(r['min_track_width'],native_mm('msWidth',0))
    r['min_hole_to_hole']=max(r['min_hole_to_hole'],native_mm('mdDrill',0))
    r['min_through_hole_diameter']=max(r['min_through_hole_diameter'],native_mm('msDrill',0))
    r['min_via_annular_width']=max(r['min_via_annular_width'],native_mm('rlMinViaOuter',0))
    r['min_copper_edge_clearance']=max(r['min_copper_edge_clearance'],native_mm('mdCopperDimension',0))
    pro={'board':{'design_settings':{'rules':r,'drc_exclusions':[],
         'rule_severities':{'track_not_centered_on_via':'warning','footprint_type_mismatch':'warning'}}},
         'net_settings':{'meta':{'version':3},'classes':[{'name':'Default','clearance':r['min_clearance'],'track_width':.18,'via_diameter':.6,'via_drill':.3}]},
         'meta':{'filename':name+'.kicad_pro','version':1}}
    (out/(name+'.kicad_pro')).write_text(json.dumps(pro,indent=2)+'\n')
    custom=Path(__file__).with_name('cam_jlc.kicad_dru').read_text()
    for entry in native.findall('classes/class'):
        width=float(entry.get('width','0'));number=entry.get('number')
        nets=[s.get('name') for s in native.findall('signals/signal') if s.get('class','0')==number]
        if width<=r['min_track_width'] or not nets:continue
        if any(not re.fullmatch('[a-zA-Z0-9_+-]+',n) for n in nets):raise ValueError('Unexpected net name in class rule')
        condition=' || '.join(f"A.NetName == '{n}'" for n in nets)
        custom+=f'\n(rule "Native net class {entry.get("name")}"\n  (condition "{condition}")\n  (constraint track_width (min {width}mm)))\n'
    (out/(name+'.kicad_dru')).write_text(custom)


def stack(derived,thickness,revision):
    txt=derived.read_text()
    m=re.match(r'.*?\(general\s+\(thickness ([\d\.]+)\)',txt,re.S)
    if not m:raise ValueError('KiCad board omits thickness')
    txt=txt[:m.start(1)]+str(thickness)+txt[m.end(1):]
    if not re.fullmatch(r'[A-Za-z0-9_. -]+',revision):raise ValueError('Unsupported release revision')
    if '(title_block' not in txt:
        txt=txt.replace('(layers',f'(title_block (rev "{revision}"))\n\t(layers',1)
    elif f'(rev "{revision}")' not in txt:
        raise ValueError('Imported title-block revision disagrees with the requested release')
    # KiCad's EAGLE converter does not transfer the final finish. The explicit
    # stack supplies the order thickness (outer Cu + dielectric + mask), mask,
    # finish and colour. No copper, pad, trace, hole or placement is rewritten.
    if '(stackup' not in txt:
        stackup='''(stackup
            (layer "F.SilkS" (type "Top Silk Screen") (color "White"))
            (layer "F.Paste" (type "Top Solder Paste"))
            (layer "F.Mask" (type "Top Solder Mask") (thickness 0.01) (color "Green"))
            (layer "F.Cu" (type "copper") (thickness 0.035))
            (layer "dielectric 1" (type "core") (thickness CORE) (material "FR4") (epsilon_r 4.5))
            (layer "B.Cu" (type "copper") (thickness 0.035))
            (layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01) (color "Green"))
            (layer "B.Paste" (type "Bottom Solder Paste"))
            (layer "B.SilkS" (type "Bottom Silk Screen") (color "White"))
            (copper_finish "ENIG"))'''.replace('CORE',str(round(thickness-.09,4)))
        txt=txt.replace('(setup','(setup\n'+stackup,1)
    derived.write_text(txt)


def render(gerb,gerbers,out,log,board):
    out.mkdir(parents=True,exist_ok=True)
    def path(ext):return next(gerbers.glob('*.'+ext))
    outline=path('gm1');drills=[f for f in gerbers.glob('*.drl')]
    jobs={
      'top-copper':[('gtl','#f9c65d')], 'bottom-copper':[('gbl','#9ae1ee')],
      'top-mask-openings':[('gts','#f6c66d')],'bottom-mask-openings':[('gbs','#e5bea6')],
      'top-stencil':[('gtp','#dce4e4')],'top-silk':[('gto','#fffdf2')], 'bottom-silk':[('gbo','#f3f5f4')],
      'outline':[], 'drill-map':[], 'superimposed-copper':[('gtl','#f6af57c5'),('gbl','#63cfe3aa')]}
    for name,layers in jobs.items():
        layers=[(path(key),color) for key,color in layers]
        if name in ('drill-map','superimposed-copper'):layers+=[(f,'#eeffed' if f.name.endswith('-PTH.drl') else '#f093a9') for f in drills]
        layers.append((outline,'#9eaaa7'))
        cmd=[gerb,'-q','-x','png','-w','1800x1400','-B','3','-b','#202427','-o',out/(name+'.png')]
        for f,color in layers:cmd+=['-f',color]
        cmd+=[f for f,color in layers]
        run(cmd,log)
    elements={e.get('name'):e for e in ET.parse(board).findall('drawing/board/elements/element')}
    plated=next(gerbers.glob('*-PTH.drl'))
    for title,ref,wmm,hmm in [('wlcsp-lands','U104',5,4),('fpc-contacts','J301',19,9),
        ('harvester-lands','U101',8,8),('charger-lands','U102',7,6),('module-antenna','U201',24,24)]:
        if ref not in elements:continue
        e=elements[ref];cx,cy=float(e.get('x')),float(e.get('y'));x=(cx-wmm/2)/25.4;y=(cy-hmm/2)/25.4
        dpi=round(1200*25.4/wmm);size=f'1200x{round(1200*hmm/wmm)}';origin=f'{x:.6f}x{y:.6f}'
        if ref=='U201':
            stack=[(outline,'#f3f0ddff'),(plated,'#d987b8ff'),(path('gtl'),'#e6b8559f'),(path('gbl'),'#66bfcfa0')]
        else:
            stack=[(path('gtp'),'#f3986aff'),(path('gts'),'#f3d769a5'),(plated,'#ec9ad3ff'),(path('gtl'),'#64abb8ff')]
        cmd=[gerb,'-q','-a','-x','png','-D',str(dpi),'-O',origin,'-w',size,'-B','0','-b','#202427','-o',out/(title+'.png')]
        for file,color in stack:cmd+=['-f',color]
        run(cmd+[file for file,color in stack],log)


def publish_job(job,gerbers,board,work,revision,thickness):
    raw=job.read_bytes();metadata=json.loads(raw);spec=metadata['GeneralSpecs']
    if spec['LayerNumber']!=2 or abs(spec['BoardThickness']-thickness)>1e-4:raise ValueError(f'Derived stack: {spec}')
    profile,n=edge_centers(next(gerbers.glob('*.gm1')))
    native=list(polygonize([native_axis(w) for w in ET.parse(board).findall('drawing/board/plain/wire[@layer="20"]')]))
    if n!=1 or len(native)!=1 or native[0].boundary.hausdorff_distance(profile.boundary)>.0015:
        raise ValueError('Native and manufactured profile centrelines differ')
    layer_revisions={}
    for plot in sorted(gerbers.glob('*.g??')):
        x2=re.search(r'^%TF\.ProjectId,[^,\n]+,[^,\n]+,([^*]+)\*%$',plot.read_text(),re.M)
        if not x2 or x2.group(1)!=revision:raise ValueError(f'Gerber layer {plot.name} has inconsistent X2 project revision')
        layer_revisions[plot.name]=x2.group(1)
    x0,y0,x1,y1=profile.bounds;dims={'X':round(x1-x0,5),'Y':round(y1-y0,5)}
    provenance={'native_sha256':hashlib.sha256(board.read_bytes()).hexdigest(),'raw_KiCad_job_sha256':hashlib.sha256(raw).hexdigest(),
       'raw_ink_bounds_size_mm':spec['Size'],'raw_KiCad_revision':spec['ProjectId']['Revision'],'finished_profile_centerline_mm':dims,'release_revision':revision,
       'individual_Gerber_X2_revisions':layer_revisions,
       'reason':'KiCad job dimensions include the width of the plotted outline stroke. Finished CNC dimensions are measured on its centreline. The CAM title block carries the release revision into the Gerber X2 files.'}
    (work/(job.stem+'-original.gbrjob')).write_bytes(raw)
    spec['Size']=dims;spec['ProjectId']['Revision']=revision
    job.write_text(json.dumps(metadata,indent=2)+'\n');provenance['shipped_job_sha256']=hashlib.sha256(job.read_bytes()).hexdigest()
    (work.parent/'gerber-job-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--board',type=Path,default=ROOT/'board/astra.brd');p.add_argument('--thickness',type=float,default=1.0)
    p.add_argument('--revision',default='A')
    p.add_argument('--out',type=Path,default=ROOT/'fab');p.add_argument('--verify',type=Path,default=ROOT/'verification/manufacturing');p.add_argument('--no-render',action='store_true')
    p.add_argument('--kicad',default=os.environ.get('KICAD_CLI') or shutil.which('kicad-cli') or '/tmp/astra-cam/kicad-volume/KiCad/KiCad.app/Contents/MacOS/kicad-cli');p.add_argument('--gerbv',default=os.environ.get('GERBV') or shutil.which('gerbv'))
    a=p.parse_args();native_input=a.board.resolve();ver=a.verify.resolve();fab=a.out.resolve();name=native_input.stem;work=ver/'independent-board';
    ver.mkdir(parents=True,exist_ok=True);work.mkdir(parents=True,exist_ok=True);gerbers=fab/'Gerbers';gerbers.mkdir(parents=True,exist_ok=True)
    snapshot=work/'input';snapshot.mkdir(exist_ok=True);board=snapshot/native_input.name
    original=native_input.read_bytes();original_hash=hashlib.sha256(original).hexdigest();board.write_bytes(original)
    log=ver/'cam-run.log';log.write_text('Native board '+str(native_input)+'\nNative board SHA256 '+original_hash+'\n')
    candidate=work/(name+'.kicad_pcb');run([a.kicad,'version'],log);run([a.kicad,'pcb','import','--format','eagle','--report-format','json','--report-file',work/'import.json','--output',candidate,board],log)
    rules(work,name,board);stack(candidate,a.thickness,a.revision)
    drc=ver/'independent-drc.json'
    result=run([a.kicad,'pcb','drc','--format','json','--severity-all','--all-track-errors','--refill-zones','--save-board','--exit-code-violations','-o',drc,candidate],log,allowed=(0,5))
    run([a.kicad,'pcb','export','gerbers','--check-zones','-o',gerbers,'--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts',candidate],log)
    run([a.kicad,'pcb','export','drill','--excellon-separate-th','--excellon-units','mm','--generate-report','--report-path',ver/'drill-report.txt','-o',gerbers,candidate],log)
    run([a.kicad,'pcb','export','pos','--format','csv','--units','mm','-o',work/'raw-placements.csv',candidate],log)
    run([a.kicad,'pcb','export','ipcd356','-o',fab/(name+'.ipc'),candidate],log)
    job,=gerbers.glob('*.gbrjob');publish_job(job,gerbers,board,work,a.revision,a.thickness)
    with ZipFile(fab/(name+'-Gerber-drill.zip'),'w',compression=ZIP_DEFLATED) as archive:
        for member in sorted(gerbers.iterdir()):archive.write(member,member.name)
    geo=check(board,gerbers);(ver/'gerber-vs-native.json').write_text(json.dumps(geo,sort_keys=True,indent=2)+'\n')
    from cam_stencil import write_step_dxf
    write_step_dxf(fab/'stencil-step-zones-mm.dxf',geo['stencil_step_zones'])
    if not a.no_render:
        if not a.gerbv:raise FileNotFoundError('gerbv')
        run([a.gerbv,'--version'],log);render(a.gerbv,gerbers,ver/'viewer',log,board)
    candidate.with_suffix('.kicad_prl').unlink(missing_ok=True)
    if original_hash!=geo['source_sha256'] or original_hash!=hashlib.sha256(native_input.read_bytes()).hexdigest():raise RuntimeError('Native board changed during CAM. Rerun the exports on the new revision.')
    dr=json.loads(drc.read_text());print('KiCad DRC exit',result.returncode,'violations',Counter(v['type'] for v in dr['violations']),'unconnected',len(dr.get('unconnected_items',[])));print('Geometry-derived shorts',len(geo['shorted_nets_from_copper']),'opens',len(geo['open_nets_from_copper']))

if __name__=='__main__':main()
