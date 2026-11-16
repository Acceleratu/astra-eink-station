"""Export aligned production layers, native overlays, component cross-references and vector sheets."""
import argparse
import csv
import json
import math
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
from html import escape
import fitz

P=Path(__file__).resolve().parents[2]
OUT=P/'explorer/data'
VIEW='-6 -92 124 100'
LAYERS=[
 ('bottomCopper','B_Cu.gbl','#b78edc'),('topCopper','F_Cu.gtl','#deae60'),
 ('bottomMask','B_Mask.gbs','#89aec6'),('topMask','F_Mask.gts','#39c29a'),
 ('paste','F_Paste.gtp','#d4dad2'),('bottomSilk','B_Silkscreen.gbo','#92a3b6'),
 ('topSilk','F_Silkscreen.gto','#edeecd'),('edge','Edge_Cuts.gm1','#ddede2'),
 ('pth','PTH.drl','#69c5ea'),('npth','NPTH.drl','#ef9584')]
def svg(body):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEW}" width="1240" height="1000">{body}</svg>'
def write_layer(name,body):(OUT/(name+'.svg')).write_text(svg(body))
def gerbers():
    with tempfile.TemporaryDirectory() as tmp:
        for key,suffix,color in LAYERS:
            out=Path(tmp)/'gerber.svg'
            subprocess.run(['gerbv','-q','-x','svg','-f','#ffffff','-b','#000000','-o',str(out),str(P/'project/fab/Gerbers'/('astra-'+suffix))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            text=out.read_text()
            style=re.search(r'<style>(.*?)</style>',text,re.S)[1]
            paths=text.split('</defs>',1)[1].split('</svg>',1)[0]
            paths,n=re.subn(r'<g transform="translate\([^"]+?\) scale\([^"]+?\)">','<g transform="scale(25.4,-25.4)">',paths,count=1)
            assert n==1 and '<image' not in paths
            write_layer(key,f'<defs><style>{style}</style><mask id="film" maskUnits="userSpaceOnUse" x="-6" y="-92" width="124" height="100">{paths}</mask></defs><rect x="-6" y="-92" width="124" height="100" fill="{color}" mask="url(#film)"/>')
def draw_native(e):
    g=e.get
    if e.tag=='polygon':
        return '<polygon points="'+ ' '.join(f'{p.get("x")},{p.get("y")}' for p in e.findall('vertex'))+'" fill-opacity=".35" stroke-width=".12"/>'
    if e.tag=='wire':return f'<line x1="{g("x1")}" y1="{g("y1")}" x2="{g("x2")}" y2="{g("y2")}" stroke-width="{g("width","0.1")}"/>'
    if e.tag=='circle':return f'<circle cx="{g("x")}" cy="{g("y")}" r="{g("radius")}" fill="none" stroke-width="{g("width",".1")}"/>'
    if e.tag=='text' and e.text and not e.text.startswith('>'):
        return f'<text transform="translate({g("x")} {g("y")}) rotate({g("rot","R0").lstrip("R")}) scale(1 -1)" font-family="sans-serif" font-size="{g("size")}" stroke="none">{escape(e.text)}</text>'
    return ''
def board_lands(package, part):
    angle = math.radians(part['rot'])
    co, si = math.cos(angle), math.sin(angle)
    lands = []
    for smd in package.findall('smd'):
        x, y, w, h = (float(smd.get(k)) for k in ('x', 'y', 'dx', 'dy'))
        if not math.isclose(co*si, 0, abs_tol=1e-8) or smd.get('rot','R0')!='R0':
            raise ValueError('Expected axis-aligned board pads')
        if abs(si) > .5:
            w, h = h, w
        lands.append([round(part['x']+co*x-si*y,4), round(part['y']+si*x+co*y,4),
                      w, h, round(min(w,h) * float(smd.get('roundness',0)) / 200, 4)])
    return lands

def data(pdf):
    board=ET.parse(P/'project/board/astra.brd').find('.//board')
    pk={p.get('name'):p for p in board.findall('.//packages/package')}
    refs={};nets={};over=defaultdict(list)
    bom={}
    for row in csv.DictReader((P/'project/fab/BOM-JLCPCB.csv').open()):
        for ref in row['Designator'].split(','):bom[ref.strip()]=row['Manufacturer Part Number']
    def native(item,tf=''):
        layer=item.get('layer')
        if layer in ['27','41','42','43','51']:over[layer].append(f'<g transform="{tf}">{draw_native(item)}</g>')
    for shape in board.find('plain'):native(shape)
    def num(e,n):return float(e.get(n))
    for e in board.findall('./elements/element'):
        ref=e.get('name');x,y=num(e,'x'),num(e,'y');a=float(e.get('rot','R0').lstrip('R'))
        refs[ref]=dict(x=x,y=y,rot=a,pkg=e.get('package'),value=e.get('value',''),mpn=bom.get(ref,''),nets=[],sheets=[])
        refs[ref]['lands']=board_lands(pk[e.get('package')],refs[ref])
        for shape in pk[e.get('package')]:native(shape,f'translate({x} {y}) rotate({a})')
        # The native tValues attributes are hidden and share an anchor. Spread the labels
        # vertically in this optional inspection overlay so both catalog codes can be read.
        attributes=[a for a in e.findall('attribute') if a.get('layer')=='27' and a.get('value')]
        for i,shape in enumerate(attributes):
            txt=ET.Element('text',dict(shape.attrib))
            txt.set('size','.48');txt.set('y',str(num(shape,'y')-i*.6));txt.text=shape.get('value');native(txt)
    for s in board.findall('./signals/signal'):
        name=s.get('name');points=[];contacts=[];vias=[]
        for c in s.findall('contactref'):
            ref=c.get('element');part=refs[ref];pad=c.get('pad')
            el=next((m for m in pk[part['pkg']] if m.tag in ('pad','smd') and m.get('name')==pad),None)
            if el is None:raise ValueError((ref,pad))
            a=math.radians(part['rot']);x,y=num(el,'x'),num(el,'y')
            contacts.append([ref,pad,round(part['x']+x*math.cos(a)-y*math.sin(a),4),round(part['y']+x*math.sin(a)+y*math.cos(a),4)])
            if name not in part['nets']:part['nets'].append(name)
        for w in s.findall('wire'):points.append([num(w,k) for k in ('x1','y1','x2','y2','width')]+[int(w.get('layer'))])
        for v in s.findall('via'):vias.append([num(v,'x'),num(v,'y')])
        nets[name]=dict(wires=points,contacts=contacts,vias=vias)
    for key,col in [('27','#b0cbe1'),('41','#f39575'),('42','#c18bea'),('43','#ebc156'),('51','#94bcff')]:
        write_layer('native'+key,f'<g transform="scale(1 -1)" stroke="{col}" fill="{col}">'+''.join(over[key])+'</g>')
    sheets=[]
    for i,page in enumerate(fitz.open(pdf)):
        file=f'sheet-{i+1}.svg'
        (OUT/file).write_text(page.get_svg_image(text_as_path=True))
        labels=[];netlabels=[]
        seen=set()
        for x,y,x2,y2,word,*_ in page.get_text('words'):
            if word in nets:netlabels.append([word,round(x,2),round(y,2),round(x2-x,2),round(y2-y,2)])
            if word in refs and word not in seen:
                seen.add(word);refs[word]['sheets'].append(i);labels.append([word,round(x,2),round(y,2),round(x2-x,2),round(y2-y,2)])
        sheets.append(dict(file=file,width=page.rect.width,height=page.rect.height,labels=labels,netLabels=netlabels))
    assert all(x['sheets'] for x in refs.values())
    (OUT/'design.json').write_text(json.dumps(dict(refs=refs,nets=nets,sheets=sheets),separators=(',',':')))
    print(len(refs),'refs',len(nets),'nets',len(sheets),'sheets')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('vector_pdf');args=parser.parse_args()
    gerbers();data(args.vector_pdf)
