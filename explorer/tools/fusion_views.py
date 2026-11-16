"""Build registered native view assets using the saved project inspection exports."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

dest=Path(__file__).resolve().parents[1]/'native'
source=Path(sys.argv[1])
pcb=source/'verification/fusion/pcb'
dest.mkdir(exist_ok=True)

def rgb(path):
    with Image.open(path) as im:
        return np.array(im.convert('RGB'))

def save(name, pixels):
    # Construct a new image from pixels. Keep no input metadata.
    Image.fromarray(pixels).save(dest/(name+'.webp'),lossless=True,method=4)

def registration(size,dpi):
    step=25.4/dpi
    # The native board outline starts at pixel (1,1) at the upper left (0,84).
    return [-1.5*step,-84-1.5*step,size[0]*step,size[1]*step]

meta={'layers':[],'sheets':[]}
baseline=rgb(pcb/'layer-20-Dimension.png')
meta['layerBox']=registration((baseline.shape[1],baseline.shape[0]),360)
for path in sorted(pcb.glob('layer-*.png')):
    _,number,name=path.stem.split('-',2)
    im=rgb(path);assert im.shape==baseline.shape
    diff=np.any(im!=(0 if number=='20' else baseline),axis=2)
    visible=bool(diff.any())
    if visible:save('layer-'+number,np.dstack((np.where(diff[:,:,None],im,0),diff.astype('uint8')*255)))
    meta['layers'].append({'id':int(number),'name':name,'file':'layer-'+number+'.webp' if visible else None})
for key,name in [('top','top-face'),('bottom','bottom-copper-top-view')]:
    im=rgb(pcb/(name+'.png'));save(key,im)
    meta['boardBox']=registration((im.shape[1],im.shape[0]),500)
for path in sorted((source/'verification/fusion/sheets').glob('sheet-*.png')):
    im=rgb(path);save(path.stem,im)
    # The Fusion export is cropped to the frame. The interactive labels use PDF points.
    # Locate the two outer frame lines in both axes and register their centres.
    grayscale=im.min(2)<220
    xprof=grayscale.sum(0);yprof=grayscale.sum(1)
    def edge_centres(profile):
        n=len(profile)
        left=np.flatnonzero(profile[:15]>0.85*profile[:15].max())
        right=np.flatnonzero(profile[-15:]>0.85*profile[-15:].max())+n-15
        return left.mean()+.5,right.mean()+.5
    x0,x1=edge_centres(xprof);y0,y1=edge_centres(yprof)
    sx=(1171.38-19.5)/(x1-x0);sy=(809.7-32.22)/(y1-y0)
    meta['sheets'].append([19.5-x0*sx,32.22-y0*sy,im.shape[1]*sx,im.shape[0]*sy])
for key,folder,files in [
    ('case','mechanical/enclosure/verification/fusion',['01-front','02-front-normal','03-back','04-open','05-usb','06-sensor','07-controls','08-back-interior','10-usb-axial','11-usb-opposite']),
    ('pcb','verification/fusion/3d',['assembled','top','bottom','usb-battery','harvester','radio-pogo','display','mated-display','external-panel'])]:
    for name in files:save(key+'-'+name,rgb(source/folder/(name+'.png')))
(dest/'views.json').write_text(json.dumps(meta,separators=(',',':')))
print(len(meta['layers']),'native layers;',len(meta['sheets']),'registered sheets')
