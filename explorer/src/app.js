import {loadLayerImage} from './layer-image.js';
import {cameras,explodedReferences,homeView,nativePresets,savedVisibility} from './fusion.js';
import {FlatView} from './flat.js';
const root=document.querySelector('#explorer');
const en=document.documentElement.lang!=='ro';
const t=(a,b)=>en?a:b;
const labels={
 schematic:t('Schematic','Schemă'),board:'PCB 2D',pcb3:'PCB 3D',case:t('Enclosure 3D','Carcasă 3D')
};
const sheetNames=en?['System overview','USB-C & charging','Solar harvesting','Radio & programming','E-paper display','Wake timer & clock','Controls & battery sensing']:['Ansamblul electric','USB-C și încărcare','Alimentare solară','Radio și programare','Afișajul e-paper','Trezire și ceas','Comenzi și măsurarea bateriei'];
const layers=[
 ['bottomCopper','#b78edc','Bottom copper','Cupru jos'],['topCopper','#deae60','Top copper','Cupru sus'],
 ['bottomMask','#89aec6','Bottom mask openings','Deschideri mască jos'],['topMask','#39c29a','Top mask openings','Deschideri mască sus'],
 ['paste','#d4dad2','Solder paste','Pastă de lipit'],['bottomSilk','#92a3b6','Bottom silkscreen (empty)','Serigrafie jos (goală)'],['topSilk','#edeecd','Top silkscreen','Serigrafie sus'],
 ['pth','#69c5ea','Plated drills','Găuri metalizate'],['npth','#ef9584','Mechanical drills','Găuri mecanice'],['edge','#ddede2','Board outline','Conturul plăcii'],
 ['native27','#b0cbe1','Part attributes (MPN / LCSC)','Coduri piese (MPN / LCSC)'],['native41','#f39575','Top copper keepout','Restricții cupru sus'],['native42','#c18bea','Bottom copper keepout','Restricții cupru jos'],['native43','#ebc156','Via keepout','Restricții via'],['native51','#94bcff','Assembly drawing','Desen de asamblare']
];
const stacks={
  copper:[[1,16],t('Both copper layers','Cupru pe ambele fețe')],
  routing:[[1,16,17,18,19,20],t('Routing and outline','Trasee și contur')],
  silk:[[20,21,22,25,26],t('Silkscreen and outline','Serigrafie și contur')],
  masks:[[20,29,30,31,32],t('Solder mask and paste','Mască și pastă de lipit')],
  holes:[[17,18,20,44,45],t('Pads, vias and holes','Paduri, vias și găuri')],
  restrict:[[1,16,20,41,42,43],t('Copper and keepouts','Cupru și restricții')]
};
function stackOptions(){
  return {...stacks,all:[state.native.layers.map(l=>l.id),t('All layers','Toate straturile')],none:[[],t('No layers','Niciun strat')]};
}
function stackKey(){
  return Object.entries(stackOptions()).find(([, [ids]])=>ids.length===state.nativeLayers.size && ids.every(id=>state.nativeLayers.has(id)))?.[0] || '';
}
const families={housing:t('Housing & rails','Carcasă și șine'),pcb:t('Populated board','Placa echipată'),display:t('Display, lens & flex','Afișaj, lentilă și flex'),solar:t('Solar panel','Panou solar'),battery:t('Battery & wiring','Baterie și cabluri'),controls:t('Buttons','Butoane'),usb:t('USB light shields','Ecrane optice USB'),fixings:t('Fasteners & pads','Șuruburi și distanțiere'),stand:t('Desk stand','Suport de birou')};
const presets={top:['topCopper','topSilk','edge','pth','npth'],bottom:['bottomCopper','bottomSilk','edge','pth','npth'],assembly:['native51','topMask','topSilk','edge','npth']};
const state={hiddenParts:new Set(),sheetStyle:'fusion',boardStyle:'fusion',nativeLayers:new Set(nativePresets.top),grid:true,edges:false,physical:true,pan:false,savedFilter:'all',named:null,mode:'board',sheet:0,selected:null,net:null,part:null,isolated:null,flip:false,measure:false,explode:0,cut:false,clip:55,families:new Set(Object.keys(families)),layers:new Set(presets.top),layerOrder:layers.map(l=>l[0])};
const viewPositions=new Map();
let view3, flat,version=0,ready=false,starting,modelReady=false;
const q=(s)=>root.querySelector(s);
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const btn=(key,label,extra='')=>'<button type="button" data-action="'+key+'" '+extra+'>'+label+'</button>';
const sel=(id,items,current,label)=>'<label class="ex-field">'+label+'<select id="'+id+'">'+items.map(([v,s])=>'<option value="'+escape(v)+'" '+(String(v)===String(current)?'selected':'')+'>'+escape(s)+'</option>').join('')+'</select></label>';
const opts=(keys)=>keys.map(k=>[k,k]);
const is3=()=>state.mode==='pcb3'||state.mode==='case';
const measureText=n=>n==null?t('Pick two points','Alege două puncte'):new Intl.NumberFormat(en?'en':'ro',{maximumFractionDigits:2}).format(n)+' mm';
const selectedName=()=>state.mode==='case'?state.part||state.selected:state.selected||state.part;
const cleanName=n=>n.replaceAll('_',' ');
const host=q('.ex-stage'),status=q('.ex-status');
const showStatus=msg=>{status.textContent=msg;status.hidden=!msg};
const showReadout=s=>{q('.ex-readout').textContent=s};
function setInspector(){
  const part=state.data.refs[state.selected],n=state.net&&state.data.nets[state.net];
  let html='';
  if(part){
    html='<strong>'+escape(state.selected)+'</strong><p>'+escape(part.value)+'</p><small>'+escape(part.mpn||part.pkg)+'</small>';
    html+='<div class="ex-links">'+Object.entries(labels).filter(([k])=>k!==state.mode&&(k!=='case'||state.mode==='pcb3')).map(([k,s])=>btn('cross',s+' ↗','data-mode="'+k+'"')).join('')+'</div>';
    html+=sel('ex-partnets',[['',t('Choose a net','Alege o rețea')],...opts(part.nets)],state.net||'',t('Connected nets','Rețele conectate'));
  }else if(state.part){html='<strong>'+escape(cleanName(state.part))+'</strong>'}
  if(n){
    const names=[...new Set(n.contacts.map(c=>c[0]))];
    html+='<p><b>'+escape(state.net)+'</b> · '+n.contacts.length+' '+t('pads','paduri')+'</p>';
    html+='<div class="ex-links">'+btn('netview',state.mode==='schematic'?t('Trace on PCB','Urmărește pe PCB'):t('Find on schematic','Găsește pe schemă'))+'</div>';
    html+='<details><summary>'+t('Connected parts','Piese conectate')+' ('+names.length+')</summary><div class="ex-links">'+names.map(r=>btn('netpart',r,'data-key="'+r+'"')).join('')+'</div></details>';
  }
  if(part&&is3()&&modelReady&&!view3.nodes().some(v=>v.name===state.selected))html+='<small>'+t('Pad location · no fitted component body','Poziția padului · fără corp de componentă montat')+'</small>';
  if(is3()&&selectedName()&&modelReady&&view3.nodes().some(v=>v.name===selectedName())){
    html+='<div class="ex-links">'+btn('focus',t('Frame part','Centrează piesa'))+btn('isolate',state.isolated?t('Show assembly','Arată ansamblul'):t('Isolate part','Izolează piesa'))+'</div>';
  }
  if(html)html+=btn('clear',t('Clear selection','Șterge selecția'),'class="ex-clear"');
  for(const button of root.querySelectorAll('[data-action=treepick]')){
    button.setAttribute('aria-pressed',String(button.dataset.key===selectedName()));
  }
  q('.ex-selection').innerHTML=html;
  q('.ex-selection').hidden=!html;
}
function panelBody(){
  const s=state;let html='';
  const openGroups=new Set([...q('.ex-specific').querySelectorAll('.ex-tree-branch[open]')].map(el=>el.dataset.group));
  if(s.mode==='schematic')html+=sel('ex-sheetstyle',[['fusion','Fusion Electronics'],['vector',t('Vector PDF','PDF vectorial')]],s.sheetStyle,t('Display','Afișare'));
  if(s.mode==='board')html+=sel('ex-boardstyle',[['fusion','Fusion Electronics'],['cam',t('Manufacturing plots','Fotoploturi de fabricație')]],s.boardStyle,t('Display','Afișare'));
  if(s.mode==='schematic')html+=sel('ex-sheet',sheetNames.map((n,i)=>[i,(i+1)+' / '+n]),s.sheet,t('Schematic sheet','Foaia de schemă'));
  if(s.mode==='board'||s.mode==='pcb3'){
    if(s.mode==='board')html+='<div class="ex-presets">'+[['top',t('Top','Față')],['bottom',t('Bottom','Verso')],['assembly',t('Assembly','Montaj')]].map(([k,n])=>btn('preset',n,'data-key="'+k+'"')).join('')+'</div>';
    if(s.mode==='board'&&s.boardStyle==='fusion'){
      html+=sel('ex-stack',[['',t('Selected layers','Straturile selectate')],...Object.entries(stackOptions()).map(([key,[,name]])=>[key,name])],stackKey(),t('Layer combinations','Combinații de straturi'));
      html+='<details class="ex-options" open><summary>'+t('Native layers','Straturi native')+' <span>'+s.native.layers.length+'</span></summary><div class="ex-layerlist ex-native-layers">'+s.native.layers.map(l=>'<label><input type="checkbox" data-native-layer="'+l.id+'" '+(s.nativeLayers.has(l.id)?'checked':'')+'><i aria-hidden="true" style="background:'+escape(l.color)+'"></i><span>'+String(l.id).padStart(2,'0')+'</span>'+escape(l.name)+'</label>').join('')+'</div></details>';
    }else if(s.mode!=='pcb3'||!s.physical)
    html+='<details class="ex-options" '+(s.mode==='board'?'open':'')+'><summary>'+t('Layers','Straturi')+' <span>'+layers.length+'</span></summary><div class="ex-layerlist">'+layers.map(([k,color,e,r])=>'<label><input type="checkbox" data-layer="'+k+'" '+(s.layers.has(k)?'checked':'')+'><i style="background:'+color+'"></i>'+t(e,r)+'</label>').join('')+'</div></details>';
    if(s.mode==='board')html+='<div class="ex-options ex-inline"><label><input id="ex-flip" type="checkbox" '+(s.flip?'checked':'')+'>'+t('Mirror board','Oglindește placa')+'</label><label><input id="ex-measure" type="checkbox" '+(s.measure?'checked':'')+'>'+t('Measure distance','Măsoară distanța')+'</label></div>';
  }
  if(is3()){
    if(s.mode==='pcb3')html+=sel('ex-surface',[['physical',t('Finished PCB','Placă finisată')],['cam',t('Manufacturing layers','Straturi de fabricație')]],s.physical?'physical':'cam',t('Display','Afișare'));
    html+=sel('ex-saved',[['',t('Free orbit','Orbită liberă')],...Object.entries(cameras[s.mode]).map(([id,v])=>[id,v[en?5:6]])],s.named||'',t('Fusion views','Vederi Fusion'));
    html+=sel('ex-view',[['iso',t('Isometric','Izometrică')],['front',s.mode==='case'?t('Front','Din față'):t('Top','De sus')],['back',s.mode==='case'?t('Rear','Din spate'):t('Bottom','De jos')],['side',t('Side','Din lateral')]],'iso',t('Camera view','Poziția camerei'));
    html+='<label class="ex-range">'+t('Exploded view','Vedere explodată')+' <output id="ex-percent">'+Math.round(s.explode*100)+'%</output><input type="range" id="ex-explode" min="0" max="100" value="'+Math.round(s.explode*100)+'"></label>';
    html+='<label class="ex-check"><input type="checkbox" id="ex-cut" '+(s.cut?'checked':'')+'>'+t('Section cut','Secțiune transversală')+'</label><label class="ex-range" id="ex-cutline" '+(s.cut?'':'hidden')+'>X <output id="ex-mm">'+s.clip+' mm</output><input type="range" id="ex-clip" min="-11" max="125" value="'+s.clip+'"></label>';
    if(s.mode==='case')html+='<div class="ex-presets">'+[['assembled',t('Assembled','Asamblată')],['spread',t('Exploded assembly','Ansamblu explodat')],['usb','USB-C']].map(([k,v])=>btn('casepreset',v,'data-key="'+k+'"')).join('')+'</div>';
    if(modelReady){
      const groups=s.mode==='case'?Object.entries(families):[['pcb',t('Populated board','Placa echipată')]];
      html+='<div class="ex-tree"><div class="ex-tree-title">'+t('Components','Componente')+'</div>'+groups.map(([key,name])=>{
        const names=view3.members(key);
        return '<details class="ex-tree-branch" data-group="'+key+'" '+(openGroups.has(key)?'open':'')+'><summary>'+escape(name)+' <small>'+names.length+'</small></summary><div class="ex-tree-children">'+
          (s.mode==='case'?'<label class="ex-check"><input type="checkbox" data-family="'+key+'" '+(s.families.has(key)?'checked':'')+'>'+t('Show group','Arată grupul')+'</label>':'')+
          names.map(n=>'<div><input type="checkbox" aria-label="'+escape(t('Show ','Arată ')+n)+'" data-body="'+escape(n)+'" '+(!s.hiddenParts.has(n)?'checked':'')+'>'+btn('treepick',escape(cleanName(n)),'data-key="'+escape(n)+'"')+'</div>').join('')+'</div></details>';
      }).join('')+'</div>';
    }
  }
  q('.ex-specific').innerHTML=html;
  if(is3()&&modelReady)for(const input of q('.ex-specific').querySelectorAll('[data-family]')){
    const key=input.dataset.family,names=view3.members(key),shown=names.filter(n=>s.families.has(key)&&!s.hiddenParts.has(n)).length;
    input.checked=shown>0;input.indeterminate=shown>0&&shown<names.length;
  }
  q('.ex-gesture').textContent=is3()?t('Drag to orbit · Shift-drag to pan · Scroll or pinch to zoom','Trage pentru rotire · Shift și tragere pentru deplasare · Scroll sau două degete pentru zoom'):s.mode==='schematic'?t('Drag to pan · Scroll or pinch to zoom · Click a symbol or wire','Trage pentru deplasare · Scroll sau două degete pentru zoom · Click pe un simbol sau fir'):t('Drag to pan · Scroll or pinch to zoom · Click a designator to inspect','Trage pentru deplasare · Scroll sau două degete pentru zoom · Click pe indicativ pentru detalii');
  for(const [action,on] of [['pan',s.pan],['grid',s.grid],['edges',s.edges]]){
    const button=q('[data-action="'+action+'"]');button.setAttribute('aria-pressed',String(on));
  }
  setInspector();
}
function renderFlat(reset=false){
  flat.render(state,reset);
  showReadout(state.mode==='schematic'?(state.sheet+1)+' / 7 · '+sheetNames[state.sheet]:state.measure?measureText(flat.points.length===2?Math.hypot(flat.points[1][0]-flat.points[0][0],flat.points[1][1]-flat.points[0][1]):null):state.flip?t('Bottom view · 112 × 84 mm','Vedere dinspre verso · 112 × 84 mm'):t('Top view · 112 × 84 mm','Vedere de sus · 112 × 84 mm'));
}
function pcbReadout(){return state.physical?'Fusion 3D PCB':t('Manufacturing layers · CAM','Straturi de fabricație · CAM')}
function update3(){if(modelReady&&is3())view3.update({...state,selected:selectedName(),network:state.data.nets[state.net]})}
function focusSelection(){
  if(is3()){if(modelReady){freeCamera();view3.fit('current',selectedName())}return}
  const p=state.data.refs[state.selected];if(!p)return;
  if(state.mode==='board')flat.focus([state.flip?112-p.x:p.x,-p.y,24,19]);
  else if(state.schematic.sheets[state.sheet].bodies[state.selected]){
    const [x,y,w,h]=state.schematic.sheets[state.sheet].bodies[state.selected];
    flat.focus([x+w/2,y+h/2,Math.max(140,w+90),Math.max(90,h+68)]);
  }else{const label=state.data.sheets[state.sheet].labels.find(a=>a[0]===state.selected);if(label)flat.focus([label[1]+label[3]/2,label[2]+label[4]/2,335,220]);}
}
function selectionSheet(){
  const matches=s=>(!state.selected||Object.hasOwn(s.bodies,state.selected))&&(!state.net||Object.hasOwn(s.paths,state.net));
  if((state.selected||state.net)&&!matches(state.schematic.sheets[state.sheet])){
    const next=state.schematic.sheets.findIndex(matches);
    if(next>=0)state.sheet=next;
  }
}
function pickNet(key){
  state.net=key||null;state.part=state.isolated=null;
  if(key && !state.data.refs[state.selected]?.nets.includes(key))state.selected=null;
  const previousSheet=state.sheet;
  if(state.mode==='schematic')selectionSheet();
  if(previousSheet!==state.sheet)panelBody();
  if(is3())update3();else renderFlat(previousSheet!==state.sheet);
  setInspector();
}
function pick(name,focus=false){
  if(!name)return;
  state.hiddenParts.delete(name);
  if(is3() && state.data.refs[name])state.hiddenParts.delete('Exposed_lands');
  if(state.mode==='case'&&modelReady)view3.reveal(name,state.families);
  state.isolated=null;
  if(!state.data.refs[name]?.nets.includes(state.net))state.net=null;
  if(state.data.refs[name]){state.selected=name;state.part=null;if(state.mode==='schematic')selectionSheet()}
  else{state.part=name;state.selected=null}
  panelBody();if(is3())update3();else renderFlat();
  if(focus)focusSelection();
}
function flatViewKey(){return state.mode==='schematic'?'sheet-'+state.sheet:'board'}
async function switchMode(mode,focus=false){
  if(!ready)return;
  // Keep the user's framing in the coordinate system of each drawing or model.
  if(is3() && modelReady){
    viewPositions.set(state.mode,{selected:state.selected,explode:state.explode,named:view3.savedRecord?state.named:null,
      hiddenParts:new Set(state.hiddenParts),families:new Set(state.families),cut:state.cut,clip:state.clip,camera:view3.captureCamera()});
  }else if(!is3() && flat.box){
    viewPositions.set(flatViewKey(),{selected:state.selected,box:[...flat.box]});
  }
  const turn=++version;
  state.mode=mode;state.isolated=null;state.part=null;state.savedFilter='all';modelReady=false;
  if(mode==='schematic')selectionSheet();
  const previous=viewPositions.get(is3()?mode:flatViewKey());
  const sameComponent=previous && previous.selected===state.selected;
  if(is3()){
    state.explode=previous?.explode??0;state.cut=previous?.cut??false;state.clip=previous?.clip??55;
    state.named=previous?previous.named:homeView(mode);
    state.hiddenParts=new Set(previous?.hiddenParts);
    if(mode==='case')state.families=new Set(previous?.families??Object.keys(families));
    if(state.selected){
      state.families.add('pcb');state.hiddenParts.delete(state.selected);state.hiddenParts.delete('Exposed_lands');
    }
  }else if(view3)view3.mode=null;
  q('.ex-find').value='';q('.ex-results').replaceChildren();q('.ex-results').hidden=true;
  root.dataset.mode=mode;
  root.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tab===mode)));
  panelBody();showStatus('');
  if(!is3()){
    renderFlat(true);
    if(previous)flat.setBox([...previous.box]);
    if(state.selected && !sameComponent && (focus || previous))focusSelection();
    return;
  }
  showReadout(mode==='pcb3'?pcbReadout():t('Complete assembly · CAD','Ansamblul complet · CAD'));
  showStatus(t('Loading the 3D model…','Se încarcă modelul 3D…'));
  try{
    const {SceneView}=await import('./scene.js');if(turn!==version)return;
    if(!view3){
      view3=new SceneView(host,n=>pick(n),freeCamera,key=>pickNet(key));
    }
    view3.references=state.data.refs;view3.networks=state.data.nets;
    await view3.show(mode);if(turn!==version)return;
    modelReady=true;update3();
    view3.followPort=previous?.camera.followPort??false;
    if(state.named)view3.savedCamera(cameras[mode][state.named]);
    else view3.restoreCamera(previous.camera);
    if(state.selected && !sameComponent){
      if(focus && mode==='pcb3')focusSelection();
      else view3.keepInView(state.selected,freeCamera);
    }
    panelBody();showStatus('');
  }catch(e){
    if(turn!==version)return;
    const img=new Image();img.alt=t('Static preview','Previzualizare statică');img.src=mode==='case'?'assets/exploded.webp':'assets/copper.webp';img.className='ex-fallback';host.replaceChildren(img);
    showStatus(t('3D unavailable here. Download the CAD files or open this page in a WebGL 2 browser.','3D indisponibil aici. Poți descărca fișierele CAD sau deschide pagina într-un browser cu WebGL 2.'));
  }
}
function search(){
  const term=q('.ex-find').value.trim().toLowerCase();const results=q('.ex-results');results.hidden=!term;
  if(!term){results.replaceChildren();return}
  const found=[];
  for(const [name,p] of Object.entries(state.data.refs)){
    const lower=name.toLowerCase();if([lower,p.value,p.mpn,p.pkg].some(v=>v.toLowerCase().includes(term)))found.push([lower===term?0:lower.startsWith(term)?1:3,'ref',name,p.value]);
  }
  for(const n of Object.keys(state.data.nets))if(n.toLowerCase().includes(term))found.push([n.toLowerCase()===term?0:2,'net',n,t('Electrical net','Rețea electrică')]);
  if(state.mode==='case'&&modelReady)for(const n of view3.nodes())if(n.userData.group!=='pcb'&&cleanName(n.name).toLowerCase().includes(term))found.push([2,'part',n.name,t('Assembly part','Piesă din ansamblu')]);
  found.sort((a,b)=>a[0]-b[0]||a[2].localeCompare(b[2]));
  results.innerHTML=found.slice(0,24).map(([,kind,key,detail])=>btn('result','<b>'+escape(cleanName(key))+'</b><small>'+escape(detail)+'</small>','data-key="'+escape(key)+'" data-kind="'+kind+'"')).join('')||'<p>'+t('No matches','Niciun rezultat')+'</p>';
}
function freeCamera(){
  state.named=null;if(view3)view3.savedRecord=null;const select=q('#ex-saved');if(select)select.value='';
}
function savedView(id, fraction=state.explode){
  const cam=cameras[state.mode]?.[id];if(!cam||!modelReady)return;
  state.hiddenParts=new Set(view3.nodes().filter(n=>!savedVisibility(n.name,cam[4])).map(n=>n.name));state.named=id;state.savedFilter='all';state.cut=false;state.explode=state.mode==='case'?fraction:0;state.isolated=null;
  if(state.mode==='case' && state.part && state.hiddenParts.has(state.part))state.part=null;
  state.families=new Set(Object.keys(families));
  view3.followPort=state.mode==='case'&&id.includes('usb');
  panelBody();update3();view3.savedCamera(cam);
}
function showReference(){
  if(!is3())return;
  const dlg=q('.ex-dialog'),list=q('.ex-reference-list'),mode=state.mode;
  const name=state.named||homeView(mode);
  const sheets={...cameras[mode]};
  if(mode==='pcb3'){
    sheets['mated-display']=[0,0,0,0,0,'Connected display flex','Flexul conectat'];
    sheets['external-panel']=[0,0,0,0,0,'External panel','Panoul extern'];
  }
  const options=Object.entries(sheets).map(([id,c])=>[id,c[en?5:6]]);
  if(mode==='case'){
    for(const item of options)item[1]+=' · 0%';
    for(const percent of [50,100])for(const id of explodedReferences){
      options.push([id+'@'+percent,sheets[id][en?5:6]+' · '+percent+'%']);
    }
  }
  list.innerHTML=options.map(([key,label])=>'<option value="'+key+'">'+escape(label)+'</option>').join('');
  const nearest=mode==='case'&&explodedReferences.includes(name)?Math.round(state.explode*2)*50:0;
  list.value=nearest?name+'@'+nearest:name;
  const update=()=>{
    const [id,percent]=list.value.split('@'),img=q('.ex-native-image');
    img.alt=list.selectedOptions[0].textContent;
    img.src='explorer/native/'+(mode==='case'?'case':'pcb')+'-'+(percent?percent+'-':'')+id+'.webp';
    q('.ex-open-original').href=img.src;q('[data-action="useref"]').hidden=!cameras[mode][id];
  };
  list.onchange=update;update();dlg.showModal();
}
function applyCasePreset(key){
  if(!modelReady)return;
  if(key==='usb'){savedView('05-usb');return}
  if(key==='assembled'){savedView('01-front',0);return}
  if(key==='spread')savedView('spread',1);
}
function mirrorBoard(flip){
  if(state.flip===flip)return;
  const [x,y,width,height]=flat.box;
  flat.setBox([112-x-width,y,width,height]);
  state.flip=flip;
}
function preset(key){
  state.nativeLayers=new Set(nativePresets[key]);state.layers=new Set(presets[key]);mirrorBoard(key==='bottom');panelBody();renderFlat();
}
async function fullscreen(){
  try{
    if(document.fullscreenElement){await document.exitFullscreen();return}
    if(!root.classList.contains('ex-expanded')&&root.requestFullscreen){await root.requestFullscreen();return}
  }catch{}
  root.classList.toggle('ex-expanded');document.documentElement.classList.toggle('ex-lock',root.classList.contains('ex-expanded'));fullLabel();
}
function fullLabel(){
  const active=!!document.fullscreenElement||root.classList.contains('ex-expanded');
  const b=q('[data-action="fullscreen"]');b.innerText=active?t('Exit fullscreen','Ieși din ecran complet'):t('Fullscreen','Ecran complet');b.setAttribute('aria-pressed',String(active));
}
document.addEventListener('fullscreenchange',fullLabel);
root.addEventListener('click',async e=>{
  if(e.target.closest('.ex-foot a')&&root.classList.contains('ex-expanded')){
    root.classList.remove('ex-expanded');document.documentElement.classList.remove('ex-lock');fullLabel();
  }
  if(e.target.closest('.ex-foot a')&&document.fullscreenElement)await document.exitFullscreen();
  const b=e.target.closest('button');if(!b)return;
  if(b.dataset.action==='fullscreen'){await fullscreen();return}
  if(!ready)return;
  if(b.dataset.tab){await switchMode(b.dataset.tab);return}
  const action=b.dataset.action;
  if(action==='treepick'){state.savedFilter='all';pick(b.dataset.key);return}
  if(action==='reference'){showReference();return}
  if(action==='closeref'){q('.ex-dialog').close();return}
  if(action==='useref'){const [key,percent]=q('.ex-reference-list').value.split('@');q('.ex-dialog').close();savedView(key,Number(percent||0)/100);return}
  if(['pan','grid','edges'].includes(action)){state[action]=!state[action];b.setAttribute('aria-pressed',String(state[action]));update3();return}
  if(action==='home'){savedView(homeView(state.mode),0);return}
  if(action==='casepreset'){applyCasePreset(b.dataset.key);return}
  if(action==='netpart'){pick(b.dataset.key,true);return}
  if(action==='netview'){
    const key=state.net;if(!key)return;
    await switchMode(state.mode==='schematic'?'board':'schematic');
    return;
  }
  if(action==='cross'){
    const mode=b.dataset.mode;
    await switchMode(mode,true);
    if(state.mode===mode && matchMedia('(max-width:650px)').matches){
      host.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'});
    }
    return;
  }
  if(action==='preset'){preset(b.dataset.key);return}
  if(action==='result'){
    const {key,kind}=b.dataset;q('.ex-find').value='';q('.ex-results').hidden=true;
    if(kind==='net')pickNet(key);
    else pick(key,true);return;
  }
  if(action==='zoomIn'||action==='zoomOut'){if(is3())freeCamera();const by=action==='zoomIn'?1.4:1/1.4;if(is3())view3?.zoom(by);else flat.zoom(1/by)}
  if(action==='fit'){if(is3()){freeCamera();view3?.fit('iso')}else flat.focus()}
  if(action==='clear'){state.selected=state.part=state.net=state.isolated=null;setInspector();if(is3())update3();else renderFlat()}
  if(action==='focus')focusSelection();
  if(action==='isolate'){state.isolated=state.isolated?null:selectedName();update3();view3.fit('current',state.isolated);setInspector()}
});
root.addEventListener('change',async e=>{
  if(!ready)return;
  const a=e.target;
  if(a.id==='ex-boardstyle'){state.boardStyle=a.value;panelBody();renderFlat();return}
  if(a.id==='ex-sheetstyle'){state.sheetStyle=a.value;renderFlat();return}
  if(a.id==='ex-stack' && a.value){state.nativeLayers=new Set(stackOptions()[a.value][0]);panelBody();renderFlat();return}
  if(a.dataset.nativeLayer){const n=Number(a.dataset.nativeLayer);if(a.checked)state.nativeLayers.add(n);else state.nativeLayers.delete(n);q('#ex-stack').value=stackKey();renderFlat();return}
  if(a.id==='ex-saved'){if(a.value)savedView(a.value);else freeCamera();return}
  if(a.id==='ex-surface'){state.physical=a.value==='physical';update3();panelBody();showReadout(pcbReadout());return}
  if(a.id==='ex-partnets'){pickNet(a.value);return}
  if(a.id==='ex-sheet'){state.sheet=+a.value;renderFlat(true)}
  if(a.dataset.layer){if(a.checked)state.layers.add(a.dataset.layer);else state.layers.delete(a.dataset.layer);if(is3())update3();else renderFlat()}
  if(a.dataset.body){if(a.checked)state.hiddenParts.delete(a.dataset.body);else state.hiddenParts.add(a.dataset.body);update3();return}
  if(a.dataset.family){
    if(a.checked){state.families.add(a.dataset.family);for(const n of view3.members(a.dataset.family))state.hiddenParts.delete(n)}
    else state.families.delete(a.dataset.family);
    panelBody();update3();
  }
  if(a.id==='ex-flip'){mirrorBoard(a.checked);flat.points=[];renderFlat()}
  if(a.id==='ex-measure'){state.measure=a.checked;flat.points=[];renderFlat()}
  if(a.id==='ex-cut'){state.cut=a.checked;q('#ex-cutline').hidden=!a.checked;update3()}
  if(a.id==='ex-view'&&modelReady){freeCamera();view3.fit(a.value)}
});
root.addEventListener('input',e=>{
  if(!ready)return;
  if(e.target.matches('.ex-find'))search();
  if(e.target.id==='ex-explode'){if(state.mode!=='case')freeCamera();state.explode=e.target.value/100;q('#ex-percent').value=e.target.value+'%';update3();if(view3.savedRecord?.[7])view3.savedCamera(view3.savedRecord)}
  if(e.target.id==='ex-clip'){state.clip=+e.target.value;q('#ex-mm').value=state.clip+' mm';update3()}
});
root.addEventListener('keydown',e=>{
  if(e.key==='Escape'&&root.classList.contains('ex-expanded')){fullscreen();return}
  if(!ready)return;
  if(e.target===q('.ex-find')&&e.key==='Enter'){q('.ex-results button')?.click();return}
  if(e.key==='Escape'){q('.ex-results').hidden=true;return}
  if(e.target!==host)return;
  const d={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]}[e.key];
  if(d){e.preventDefault();if(is3())view3?.rotate(d[0]*.12,d[1]*.12);else flat.pan(d[0]*flat.box[2]*.08,d[1]*flat.box[3]*.08)}
  if(['+','=','-','0'].includes(e.key)){e.preventDefault();q('[data-action="'+(e.key==='0'?'fit':e.key==='-'?'zoomOut':'zoomIn')+'"]').click()}
});
async function start(){
  if(starting)return starting;
  starting=(async()=>{
    try{
      const loadJSON=async path=>{
        const response=await fetch(path);if(!response.ok)throw Error(response.status);return response.json();
      };
      const [design,native,layerImage,schematic]=await Promise.all([loadJSON('explorer/data/design.json'),loadJSON('explorer/native/views.json'),loadLayerImage(),loadJSON('explorer/native/schematic/sheets.json')]);
      state.schematic=schematic;
      state.layerImage=layerImage.imageFor;state.data=design;state.native={...native,layers:layerImage.layers};flat=new FlatView(host,n=>pick(n),d=>showReadout(measureText(d)),key=>pickNet(key));ready=true;
      const query=new URLSearchParams(location.search),initial=query.get('view');
      const sheetNumber=Number(query.get('sheet'));
      if(initial==='schematic' && Number.isInteger(sheetNumber) && sheetNumber>=1 && sheetNumber<=design.sheets.length)state.sheet=sheetNumber-1;
      if(initial==='board' && query.has('layers')){
        const stack=stackOptions()[query.get('layers')];
        if(Array.isArray(stack))state.nativeLayers=new Set(stack[0]);
        else {
          const ids=query.get('layers').split(',').map(Number);
          if(ids.every(id=>native.layers.some(layer=>layer.id===id)))state.nativeLayers=new Set(ids);
        }
      }
      if(query.get('workspace')==='1'){
        root.classList.add('ex-expanded');document.documentElement.classList.add('ex-lock');fullLabel();
      }
      await switchMode(Object.hasOwn(labels,initial)?initial:'board');
      if(state.mode==='case'&&['spread','usb','assembled'].includes(query.get('pose')))applyCasePreset(query.get('pose'));
      if(state.mode==='case'&&query.has('explode')){
        const amount=Number(query.get('explode'));
        if(Number.isFinite(amount)){state.explode=Math.max(0,Math.min(100,amount))/100;panelBody();update3();if(view3.savedRecord?.[7])view3.savedCamera(view3.savedRecord)}
      }
      if(is3()&&query.get('camera'))savedView(query.get('camera'));
      const ref=query.get('part');
      if(ref && state.data.refs[ref]){
        const explicitCaseView=state.mode==='case' && (query.has('pose') || query.has('camera'));
        pick(ref,!explicitCaseView);
      }
    }catch{starting=null;showStatus(t('Could not load the design. Open the project through its local HTTP preview or GitHub Pages.','Datele nu s-au încărcat. Deschide proiectul prin previzualizarea HTTP locală sau prin GitHub Pages.'))}
  })();return starting;
}
for(const a of document.querySelectorAll('[data-open-view]'))a.addEventListener('click',async()=>{await start();await switchMode(a.dataset.openView);if(a.dataset.detail)applyCasePreset(a.dataset.detail)});
if(new URLSearchParams(location.search).get('workspace')==='1'){
  start();
}else if('IntersectionObserver' in window){
  const io=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){io.disconnect();start()}},{rootMargin:'300px'});io.observe(root);
}else start();
