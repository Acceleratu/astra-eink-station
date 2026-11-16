import {updateSheetDetail} from './sheet-detail.js';
import {nativePCB} from './fusion.js';
const NS='http://www.w3.org/2000/svg';
function el(tag,attrs,parent){
  const e=document.createElementNS(NS,tag);
  for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);
  parent?.append(e);return e;
}
export class FlatView {
  constructor(host,onPick,onMeasure,onNet){
    this.svg=el('svg',{'aria-hidden':'true'});this.host=host;this.pick=onPick;this.pickNet=onNet;this.report=onMeasure;
    new ResizeObserver(()=>updateSheetDetail(this.svg,this.detail)).observe(host);
    this.pointers=new Map();this.points=[];
    this.svg.addEventListener('wheel',e=>{e.preventDefault();this.zoom(Math.exp(Math.max(-.7,Math.min(.7,e.deltaY*.002))),this.point(e.clientX,e.clientY))},{passive:false});
    this.svg.addEventListener('pointerdown',e=>{
      if(e.button!==0)return;
      this.gesture={x:e.clientX,y:e.clientY,hit:e.target.closest('[data-ref]')?.dataset.ref,net:e.target.closest('[data-net]')?.dataset.net,drag:false};
      this.pointers.set(e.pointerId,[e.clientX,e.clientY]);if(this.pointers.size>1)this.gesture.drag=true;
      this.svg.setPointerCapture(e.pointerId);
    });
    this.svg.addEventListener('pointermove',e=>{
      if(!this.pointers.has(e.pointerId))return;
      const old=[...this.pointers.values()],prev=this.pointers.get(e.pointerId),now=[e.clientX,e.clientY];
      this.pointers.set(e.pointerId,now);
      if(this.pointers.size===2){
        const pair=[...this.pointers.values()];const dist=p=>Math.hypot(p[0][0]-p[1][0],p[0][1]-p[1][1]);
        const center=p=>this.point((p[0][0]+p[1][0])/2,(p[0][1]+p[1][1])/2);
        const a=center(old);this.zoom(dist(old)/Math.max(.01,dist(pair)),a);const b=center(pair);
        this.pan(a.x-b.x,a.y-b.y);return;
      }
      if(Math.hypot(e.clientX-this.gesture.x,e.clientY-this.gesture.y)>3)this.gesture.drag=true;
      if(this.gesture.drag){const a=this.point(...prev),b=this.point(...now);this.pan(a.x-b.x,a.y-b.y)}
    });
    this.svg.addEventListener('pointerup',e=>{
      if(this.pointers.has(e.pointerId)&&!this.gesture.drag){
        if(this.measuring){const p=this.point(e.clientX,e.clientY);this.addPoint(this.flip?112-p.x:p.x,-p.y)}
        else if(this.gesture.hit)this.pick(this.gesture.hit);else if(this.gesture.net)this.pickNet(this.gesture.net);
      }
      this.pointers.delete(e.pointerId);
    });
    this.svg.addEventListener('pointercancel',e=>{this.pointers.delete(e.pointerId);if(this.gesture)this.gesture.drag=true});
  }
  point(x,y){return new DOMPoint(x,y).matrixTransform(this.svg.getScreenCTM().inverse())}
  setBox(box){this.box=box;this.svg.setAttribute('viewBox',box.join(' '));updateSheetDetail(this.svg,this.detail)}
  zoom(f,p){if(!this.box)return;const [x,y,w,h]=this.box;
    f=Math.min(this.base[2]*6/w,Math.max(this.base[2]/200/w,f));
    p=p||{x:x+w/2,y:y+h/2};this.setBox([p.x+(x-p.x)*f,p.y+(y-p.y)*f,w*f,h*f]);
  }
  pan(x,y){if(this.box)this.setBox([this.box[0]+x,this.box[1]+y,...this.box.slice(2)])}
  focus(target){
    if(!target){this.setBox([...this.base]);return}
    let [x,y,w,h]=target;const ratio=this.base[2]/this.base[3];w=Math.max(w,h*ratio);h=w/ratio;
    this.setBox([x-w/2,y-h/2,w,h]);
  }
  addPoint(x,y){
    if(this.points.length===2)this.points=[];
    this.points.push([x,y]);this.renderMeasure();
  }
  renderMeasure(){
    if(!this.measureGroup)return;
    this.measureGroup.replaceChildren();
    this.points.forEach(([x,y])=>el('circle',{cx:x,cy:-y,r:'.38',fill:'#fff',stroke:'#dc6443','stroke-width':'.15'},this.measureGroup));
    if(this.points.length===2){
      const [[x,y],[a,b]]=this.points;
      el('line',{x1:x,y1:-y,x2:a,y2:-b,stroke:'#ff8a67','stroke-width':'.28'},this.measureGroup);
      this.report(Math.hypot(x-a,y-b));
    }else this.report(null);
  }
  render(state,reset=false){
    if(!this.host.contains(this.svg))this.host.replaceChildren(this.svg);
    const {mode,data,sheet,selected,net,layers,flip,measure}=state;
    this.flip=flip;this.measuring=mode==='board'&&measure;
    this.svg.replaceChildren();this.measureGroup=null;this.detail=null;
    if(mode==='schematic'){
      const s=data.sheets[sheet];this.base=[0,0,s.width,s.height];
      const drawing=state.schematic.sheets[sheet];
      if(state.sheetStyle==='fusion'){
        const [x,y,width,height]=state.native.sheets[sheet];
        el('image',{href:'explorer/native/sheet-'+String(sheet+1).padStart(2,'0')+'.webp',x,y,width,height,preserveAspectRatio:'none'},this.svg);
        const group=el('g',{'pointer-events':'none'},this.svg);
        this.detail={group,sheet:drawing,number:sheet+1,tileSize:state.schematic.tileSize,previewWidth:drawing.previewWidth};
      }else el('image',{href:'explorer/data/'+s.file,x:0,y:0,width:s.width,height:s.height},this.svg);
      for(const [ref,[x,y,width,height]] of Object.entries(drawing.bodies)){
        el('rect',{x,y,width,height,'data-ref':ref,class:'symbol-hit'},this.svg);
      }
      for(const [key,d] of Object.entries(drawing.pinPaths||{})){
        el('path',{d,'data-net':key,class:'schematic-pin'},this.svg);
      }
      for(const [key,d] of Object.entries(drawing.paths)){
        el('path',{d,'data-net':key,class:'schematic-wire'},this.svg);
      }
      if(net && drawing.paths[net]){
        const selectedNet=el('g',{'pointer-events':'none',class:'schematic-net-selected'},this.svg);
        el('path',{d:drawing.paths[net]},selectedNet);
        for(const [cx,cy] of drawing.junctions[net]||[])el('circle',{cx,cy,r:1.35},selectedNet);
      }
      for(const [key,x,y,w,h] of drawing.netLabels){
        const mark=el('rect',{x:x-1,y:y-1,width:w+2,height:h+2,rx:1,'data-net':key,class:key===net?'net-mark selected':'net-mark'},this.svg);
        el('title',{},mark).textContent=key;
      }
      for(const [ref,x,y,w,h] of s.labels){
        const mark=el('rect',{x:x-2,y:y-2,width:w+4,height:h+4,rx:1.5,'data-ref':ref,class:ref===selected?'ref-mark selected':'ref-mark'},this.svg);
        el('title',{},mark).textContent=ref;
      }
    }else{
      this.base=[-6,-92,124,100];
      const g=el('g',{transform:flip?'translate(112 0) scale(-1 1)':'scale(1)'},this.svg);
      if(state.boardStyle==='fusion')nativePCB(g,state,el);
      else {el('path',{d:'M0 -1.5 L1.5 0 H110.5 L112 -1.5 V-82.5 L110.5 -84 H1.5 L0 -82.5 Z',fill:'#19443d'},g);
      for(const key of state.layerOrder)if(layers.has(key))el('image',{href:'explorer/data/'+key+'.svg',x:-6,y:-92,width:124,height:100,'pointer-events':'none'},g);}
      const copperVisible=layer=>state.boardStyle==='fusion'?state.nativeLayers.has(layer):layers.has(layer===1?'topCopper':'bottomCopper');
      // Pick only visible copper. When both faces coincide, prefer the face being viewed.
      for(const layer of (flip?[1,16]:[16,1]).filter(copperVisible)){
        for(const [key,network] of Object.entries(data.nets)){
          const path=network.wires.filter(w=>w[5]===layer).map(([x,y,a,b])=>'M'+x+' '+(-y)+'L'+a+' '+(-b)).join('');
          if(path)el('path',{d:path,'data-net':key,class:'board-wire'},g);
        }
      }
      if(net && data.nets[net]){
        const n=data.nets[net];const traces=el('g',{'pointer-events':'none'},g);
        for(const [x,y,x2,y2,w,layer] of n.wires)if(copperVisible(layer))el('line',{x1:x,y1:-y,x2,y2:-y2,stroke:layer===1?'#fff291':'#dbb5ff','stroke-width':Math.max(.32,w),'stroke-linecap':'round'},traces);
        for(const [, ,x,y] of n.contacts)el('circle',{cx:x,cy:-y,r:.38,fill:'#ffec90',stroke:'#50351c','stroke-width':.1},traces);
        for(const [x,y] of n.vias)el('circle',{cx:x,cy:-y,r:.3,fill:'none',stroke:'#fff8c5','stroke-width':.18},traces);
      }
      for(const [ref,{x,y,lands}] of Object.entries(data.refs)){
        for(const [cx,cy,w,h,radius] of lands||[]){
          el('rect',{x:cx-w/2,y:-cy-h/2,width:w,height:h,rx:radius,'data-ref':ref,class:'pcb-hit'},g);
        }
        const hit=el('circle',{cx:x,cy:-y,r:.87,'data-ref':ref,class:'pcb-hit'},g);el('title',{},hit).textContent=ref;
      }
      const part=data.refs[selected];
      if(part){
        const {x,y}=part;
        el('circle',{cx:x,cy:-y,r:1.6,fill:'none',stroke:'#fff5cf','stroke-width':.46,'pointer-events':'none'},g);
        const label=el('text',{transform:'translate('+x+' '+(-y-2.6)+') scale('+(flip?-1:1)+' 1)','text-anchor':'middle',class:'board-label','pointer-events':'none'},g);label.textContent=selected;
      }
      this.measureGroup=el('g',{'pointer-events':'none'},g);
      if(this.measuring)this.renderMeasure();
    }
    if(reset||!this.box)this.focus();else updateSheetDetail(this.svg,this.detail);
  }
}
