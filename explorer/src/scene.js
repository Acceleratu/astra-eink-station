import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

import {PCBNet} from './pcb-net.js';
import {finishBoard} from './pcb-finish.js';
import {NavigationCube} from './navigation.js';
import {cameras,savedVisibility} from './fusion.js';
const vec = (x,y,z) => new THREE.Vector3(x,y,z);
const films = {
  bottomCopper:-1.03, topCopper:.04, bottomMask:-1.045, topMask:.055,
  paste:.075, bottomSilk:-1.09, topSilk:.09, edge:.11, pth:.13, npth:.15,
  native27:.17,native41:.19,native42:-1.19,native43:.21,native51:.23
};
const caseFamily = group => ({
  pcb:'pcb',front:'housing',rear:'housing',rail:'housing',stand:'stand',
  display:'display',lens:'display',seal:'display',flex:'display',retainer:'display',
  pv:'solar',battery:'battery',battery_guard:'battery',key:'controls',keeper:'controls',
  usb_mask:'usb',pads:'fixings',fixing:'fixings'
})[group] || group;

export class SceneView {
  constructor(container, onPick, onOrbit, onNet) {
    this.container=container;this.onPick=onPick;this.renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
    this.renderer.setPixelRatio(Math.min(devicePixelRatio,2));this.renderer.localClippingEnabled=true;
    this.scene=new THREE.Scene();this.scene.background=new THREE.Color(0x2e3440);this.camera=new THREE.OrthographicCamera(-120,120,100,-100,.05,4000);
    this.renderer.domElement.setAttribute('aria-hidden','true');
    this.controls=new OrbitControls(this.camera,this.renderer.domElement);this.controls.enableDamping=false;
    this.controls.minZoom=.12;this.controls.maxZoom=140;
    let navigating=false;
    this.controls.addEventListener('start',()=>{navigating=true});
    this.controls.addEventListener('end',()=>{navigating=false});
    this.controls.addEventListener('change',()=>{
      if(navigating && this.savedRecord)onOrbit();
      this.draw();
    });
    this.scene.add(new THREE.HemisphereLight(0xffffff,0xb3b7bb,1.52));
    for(const [x,y,z,power] of [[-120,-210,-190,1.04],[150,-60,210,1.3]]){
      const light=new THREE.DirectionalLight(0xffffff,power);light.position.set(x,y,z);this.scene.add(light);
    }
    const gridMaterial=new THREE.ShaderMaterial({
      uniforms:{stepSize:{value:10},pcbGrid:{value:0}},side:THREE.DoubleSide,depthTest:false,depthWrite:false,
      vertexShader:`varying vec2 ground;void main(){ground=position.xy;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
      fragmentShader:`varying vec2 ground;uniform float stepSize,pcbGrid;
        void main(){
          vec2 uv=ground/stepSize,fw=max(fwidth(uv),vec2(.0001));
          vec2 distanceToLine=abs(fract(uv+.5)-.5)/fw;
          float line=(1.-smoothstep(.16,1.,min(distanceToLine.x,distanceToLine.y)))*(1.-smoothstep(.09,.32,max(fw.x,fw.y)));
          gl_FragColor=pcbGrid>.5?vec4(vec3(.74,.76,.79),line*.115):vec4(mix(vec3(46.,52.,64.),vec3(74.,79.,89.),line)/255.,1.);
        }`
    });
    this.grid=new THREE.Mesh(new THREE.PlaneGeometry(12000,12000),gridMaterial);
    this.grid.renderOrder=-100;this.scene.add(this.grid);
    this.cube=new NavigationCube(container.parentElement.querySelector('.ex-cube'),axis=>{onOrbit();this.face(axis)});
    this.roots={};this.loads={};this.layers=new Map();this.layerLoads=new Map();this.ray=new THREE.Raycaster();
    this.clipMat=new THREE.Plane(vec(-1,0,0),60);
    this.netOverlay=new PCBNet();this.scene.add(this.netOverlay);
    for(const mat of this.netOverlay.materials)mat.clippingPlanes=[this.clipMat];
    this.loader=new GLTFLoader();this.visibleFamilies=new Set();
    this.tex=new THREE.TextureLoader();this.films=new THREE.Group();this.scene.add(this.films);
    const canvas=this.renderer.domElement;
    canvas.addEventListener('pointerdown',e=>{if(e.isPrimary)this.down=[e.clientX,e.clientY];else this.down=null});
    canvas.addEventListener('pointerup',e=>{
      if(!this.down || e.button!==0 || Math.hypot(e.clientX-this.down[0],e.clientY-this.down[1])>4)return;
      const r=canvas.getBoundingClientRect();
      this.ray.setFromCamera(new THREE.Vector2(2*(e.clientX-r.left)/r.width-1,1-2*(e.clientY-r.top)/r.height),this.camera);
      const hit=this.ray.intersectObjects(this.nodes().filter(n=>n.visible),true).find(h=>h.object.isMesh&&(!this.cut || this.clipMat.distanceToPoint(h.point)>=0));
      if(this.mode==='pcb3' && this.films.visible){
        for(const film of this.ray.intersectObjects([...this.layers.values()].filter(m=>m.visible && m.userData.copperLayer))){
          if(hit && film.distance>hit.distance+.001)break;
          if(this.cut && this.clipMat.distanceToPoint(film.point)<0)continue;
          const net=this.copperAt(film.point,film.object.userData.copperLayer);
          if(net){onNet(net);return}
        }
      }
      if(!hit)return;
      let node=hit.object;
      while(node && !node.userData.group)node=node.parent;
      if(!node)return;
      let name=node.name;
      if(name==='Exposed_lands'){
        const {x,y}=node.worldToLocal(hit.point.clone());
        for(const [ref,part] of Object.entries(this.references)){
          if(part.lands.some(([cx,cy,w,h,r])=>{
            const dx=Math.abs(x-cx)-w/2+r,dy=Math.abs(y-cy)-h/2+r;
            return Math.hypot(Math.max(0,dx),Math.max(0,dy))<=r+.001;
          })){name=ref;break}
        }
      }
      this.onPick(name);
    });
    this.observer=new ResizeObserver(()=>this.resize());this.observer.observe(container);
  }
  draw(){if(this.container.contains(this.renderer.domElement)){
    this.grid.rotation.x=Math.abs(this.camera.getWorldDirection(vec(0,0,0)).z)<.999?Math.PI/2:0;
    const height=200/this.camera.zoom;
    const steps=[.25,.5,1,2.5,5,10,25,50,100,250];
    const pcbSteps=[[2,.1],[9,.5],[38,1],[75,5],[180,10],[500,25],[1500,100]];
    this.grid.material.uniforms.stepSize.value=this.mode==='pcb3'?(pcbSteps.find(([limit])=>height<=limit)?.[1]||250):(steps.find(s=>s>=height/12)||250);
    if(this.surfaceMode&&this.updateBoardFinish)this.updateBoardFinish(this.camera,this.boardAssembled,this.landsAtRest);
    this.renderer.render(this.scene,this.camera);this.cube.update(this.camera,this.mode)}}
  face(direction){
    this.savedRecord=null;
    const center=this.controls.target,up=this.mode==='case'?vec(0,-1,0):vec(0,1,0);
    this.camera.up.copy(Math.abs(up.dot(direction))>.98?vec(0,0,this.mode==='case'?-1:1):up);
    this.camera.position.copy(center).addScaledVector(direction,600);this.camera.lookAt(center);this.controls.update();this.draw();
  }
  captureCamera(){
    return {position:this.camera.position.clone(),up:this.camera.up.clone(),zoom:this.camera.zoom,
      target:this.controls.target.clone(),followPort:this.followPort};
  }
  restoreCamera(pose){
    this.savedRecord=null;
    this.controls.target.copy(pose.target);this.camera.position.copy(pose.position);
    this.camera.up.copy(pose.up);this.camera.zoom=pose.zoom;
    this.camera.lookAt(pose.target);this.camera.updateProjectionMatrix();this.controls.update();this.draw();
  }
  keepInView(name,onReframe){
    const bounds=this.bounds(name);if(!bounds)return;
    const point=bounds.getCenter(vec(0,0,0)).project(this.camera);
    if(Math.abs(point.x)<=.95 && Math.abs(point.y)<=.95 && Math.abs(point.z)<=1)return;
    onReframe();
    const target=bounds.getCenter(vec(0,0,0));
    this.camera.position.add(target.clone().sub(this.controls.target));
    this.controls.target.copy(target);this.followPort=false;this.controls.update();this.draw();
  }
  savedCamera(record){
    this.savedRecord=record;
    const [target,direction,up,assembledExtent]=record;
    const explodedFrame=record[7];
    const extent=explodedFrame?THREE.MathUtils.lerp(assembledExtent,explodedFrame[1],this.explode):assembledExtent;
    const {width,height}=this.container.getBoundingClientRect();
    if(!width||!height)return;
    this.camera.left=-100*width/height;this.camera.right=100*width/height;

    this.controls.target.set(...target);
    if(explodedFrame)this.controls.target.lerp(vec(...explodedFrame[0]),this.explode);
    if(this.followPort)this.controls.target.add(this.portOffset(this.explode));this.camera.up.set(...up);
    const eye=vec(...direction);
    if(this.mode==='pcb3')eye.multiplyScalar(220);
    else eye.normalize().multiplyScalar(600);
    this.camera.position.copy(this.controls.target).add(eye);
    this.camera.zoom=200/extent*Math.min(1,(this.camera.right-this.camera.left)/200/(this.mode==='case'?1400/1180:1600/1050));
    this.camera.lookAt(this.controls.target);this.camera.updateProjectionMatrix();this.controls.update();this.draw();
  }
  portOffset(fraction){
    const offset=this.roots.pcb.getObjectByName('J101').userData.explode;
    return vec(...offset).multiplyScalar(1.65*fraction);
  }
  panMode(on){
    this.controls.mouseButtons.LEFT=on?THREE.MOUSE.PAN:THREE.MOUSE.ROTATE;
    this.controls.touches.ONE=on?THREE.TOUCH.PAN:THREE.TOUCH.ROTATE;
  }
  async usbAppearance(){
    if(this.usbMaterials)return this.usbMaterials;
    const angles=['05-usb','10-usb-axial','11-usb-opposite'];
    const parts=[[this.roots.pcb,'J101','finish',14],[this.roots.enclosure,'front_shell','shell',28]];
    this.usbMaterials=Promise.all(parts.map(async ([root,name,prefix,extent])=>{
      const mesh=root.getObjectByName(name),material=mesh.material.clone();
      const maps=await Promise.all(angles.map(async key=>{
        const texture=await this.tex.loadAsync('explorer/native/'+prefix+'-'+key+'.webp');
        texture.colorSpace=THREE.SRGBColorSpace;
        // Alpha encodes CAD depth. Mipmaps would average unrelated surfaces.
        texture.generateMipmaps=false;texture.minFilter=THREE.LinearFilter;
        return texture;
      }));
      material.clippingPlanes=[this.clipMat];
      material.onBeforeCompile=shader=>{
        shader.vertexShader='varying vec3 usbPoint;\n'+shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nusbPoint=position-vec3(-3.2,67.,1.725);');
        shader.uniforms.usbExtent={value:extent};
        let uniforms='',samples='';
        angles.forEach((key,i)=>{
          shader.uniforms['usbMap'+i]={value:maps[i]};
          shader.uniforms['usbEye'+i]={value:vec(...cameras.case[key][1]).normalize()};
          uniforms+='uniform sampler2D usbMap'+i+'; uniform vec3 usbEye'+i+';\n';
          samples+='samplePort(usbMap'+i+',usbEye'+i+',eye,finish,total);\n';
        });
        shader.fragmentShader=uniforms+`
          varying vec3 usbPoint;uniform float usbExtent;
          void samplePort(sampler2D image,vec3 dir,vec3 eye,inout vec3 finish,inout float total){
            vec3 right=normalize(cross(vec3(0.,-1.,0.),dir));
            vec3 up=cross(dir,right);
            vec2 uv=.5+vec2(dot(usbPoint,right),dot(usbPoint,up))/usbExtent;
            float edge=min(min(uv.x,uv.y),min(1.-uv.x,1.-uv.y));
            vec4 texel=texture2D(image,uv);
            float depth=(texel.a*255.-1.)/7.8-16.;
            float visible=step(.003,texel.a)*(1.-smoothstep(.10,.32,abs(depth-dot(usbPoint,dir))));
            float angle=max(0.,1.-dot(eye,dir));
            float weight=visible*smoothstep(0.,.045,edge)*pow(.012/(.012+angle),3.);
            finish+=texel.rgb*weight;total+=weight;
          }
        `+shader.fragmentShader.replace('#include <opaque_fragment>',`
          vec3 eye=normalize(vec3(viewMatrix[0][2],viewMatrix[1][2],viewMatrix[2][2]));
          vec3 finish=vec3(0.);float total=0.;
          `+samples+`
          outgoingLight=mix(outgoingLight,finish/max(.000001,total),smoothstep(.001,.10,total));
          #include <opaque_fragment>`);
      };
      return {mesh,material};
    })).catch(e=>{this.usbMaterials=null;throw e});
    return this.usbMaterials;
  }
  resize(){
    const {width,height}=this.container.getBoundingClientRect();if(!width||!height)return;
    this.renderer.setSize(width,height,false);const aspect=width/height;
    this.camera.left=-100*aspect;this.camera.right=100*aspect;this.camera.top=100;this.camera.bottom=-100;
    this.camera.updateProjectionMatrix();if(this.savedRecord)this.savedCamera(this.savedRecord);else this.draw();
  }
  async load(key){
    if(!this.loads[key])this.loads[key]=this.loader.loadAsync('explorer/data/'+key+'.glb').then(async g=>{
      // Engineering overlays and camera controls use millimetres. The standalone glTF uses metres.
      const root=g.scene.getObjectByName('CAD_to_metres');root.scale.setScalar(1);root.visible=false;
      for(const n of root.children){
        n.userData.base=n.position.clone();
        n.traverse(m=>{if(m.isMesh){m.material.flatShading=true;m.material.clippingPlanes=[this.clipMat];m.material.needsUpdate=true;
          if(m.material.transparent)m.material.depthWrite=false;}});
      }
      if(key==='finished')this.updateBoardFinish=await finishBoard(root,this.tex,this.clipMat,Math.min(8,this.renderer.capabilities.getMaxAnisotropy()));
      this.roots[key]=root;this.scene.add(root);
      if(key==='enclosure'){
        for(const part of ['solar_cells','solar_panel_abra']){
          const panel=root.getObjectByName(part);
          panel?.traverse(m=>{if(m.isMesh){m.material=m.material.clone();m.material.color.multiplyScalar(.18);m.material.clippingPlanes=[this.clipMat]}});
        }
        for(const node of root.children){
          const factor=node.userData.group==='usb_mask'?.08:({desktop_stand:.52,rear_cover:.62})[node.name];
          if(factor)node.traverse(m=>{
            if(m.isMesh){m.material=m.material.clone();m.material.color.multiplyScalar(factor);m.material.clippingPlanes=[this.clipMat];
              if(node.userData.group==='usb_mask')m.material.roughness=1;}
          });
        }
        const active=root.getObjectByName('display_active');
        if(active){
          const texture=await this.tex.loadAsync('project/verification/firmware/reference-frame.png');
          texture.colorSpace=THREE.SRGBColorSpace;
          active.traverse(m=>{
            if(!m.isMesh)return;
            const pos=m.geometry.attributes.position,uv=new Float32Array(pos.count*2);
            for(let i=0;i<pos.count;i++){
              uv[2*i]=(pos.getX(i)-27.55)/84.8;uv[2*i+1]=(-23.9-pos.getY(i))/63.6;
            }
            m.geometry.setAttribute('uv',new THREE.BufferAttribute(uv,2));
            m.material=new THREE.MeshBasicMaterial({map:texture,color:0xb8bda9,side:THREE.DoubleSide,clippingPlanes:[this.clipMat]});
          });
        }
      }
      return root;
    }).catch(e=>{delete this.loads[key];throw e});
    return this.loads[key];
  }
  async show(mode){
    this.followPort=false;this.savedRecord=null;this.mode=mode;this.container.replaceChildren(this.renderer.domElement);
    await Promise.all((mode==='case'?['pcb','enclosure']:['pcb','finished']).map(k=>this.load(k)));
    if(this.mode!==mode||!this.container.contains(this.renderer.domElement))return;
    if(mode==='case'){
      const surfaces=await this.usbAppearance();
      if(this.mode!==mode)return;
      for(const item of surfaces){
        if(item.mesh.material!==item.material){item.previous=item.mesh.material;item.mesh.material=item.material}
      }
    }else{
      if(this.usbMaterials)for(const item of await this.usbMaterials){
        if(this.mode!==mode)return;
        if(item.mesh.material===item.material)item.mesh.material=item.previous;
      }

    }
    this.resize();
  }
  members(group){return this.nodes().filter(n=>caseFamily(n.userData.group)===group).map(n=>n.name)}
  reveal(name,families){
    const n=this.nodes().find(node=>node.name===name);
    if(n)families.add(caseFamily(n.userData.group));
    else if(this.references?.[name]?.lands)families.add('pcb');
  }
  nodes(){const pcb=this.mode==='pcb3'&&this.surfaceMode?this.roots.finished:this.roots.pcb;return [...(pcb?.children||[]),...(this.mode==='case'?(this.roots.enclosure?.children||[]):[])]}
  copperAt(point,layer){
    let closest=null,best=Infinity;
    for(const [name,network] of Object.entries(this.networks)){
      for(const [x,y,a,b,width,side] of network.wires){
        if(side!==layer)continue;
        const dx=a-x,dy=b-y;
        const t=THREE.MathUtils.clamp(((point.x-x)*dx+(point.y-y)*dy)/(dx*dx+dy*dy||1),0,1);
        const distance=Math.hypot(point.x-x-t*dx,point.y-y-t*dy);
        if(distance<=width/2 && distance<best){closest=name;best=distance}
      }
    }
    return closest;
  }
  async addFilm(key){
    if(!this.layerLoads.has(key)){
      this.layerLoads.set(key,this.tex.loadAsync('explorer/data/'+key+'.svg').then(map=>{
        map.colorSpace=THREE.SRGBColorSpace;map.anisotropy=Math.min(4,this.renderer.capabilities.getMaxAnisotropy());
        const mat=new THREE.MeshBasicMaterial({map,transparent:true,depthWrite:false,side:THREE.DoubleSide,clippingPlanes:[this.clipMat],alphaTest:.015});
        const mesh=new THREE.Mesh(new THREE.PlaneGeometry(124,100),mat);if(key==='topCopper'||key==='bottomCopper')mesh.userData.copperLayer=key==='topCopper'?1:16;
        mesh.position.set(56,42,films[key]);mesh.renderOrder=films[key]>0?10+films[key]:10-films[key];this.films.add(mesh);this.layers.set(key,mesh);
        this.updateFilms();this.draw();
      }).catch(e=>{this.layerLoads.delete(key);throw e}));
    }
    return this.layerLoads.get(key);
  }
  updateFilms(){
    this.films.visible=this.mode==='pcb3'&&!this.isolated&&!this.surfaceMode;
    for(const [key,m] of this.layers){
      m.visible=this.enabledLayers?.has(key);m.position.z=films[key]+Math.sign(films[key])*(2+Object.keys(films).indexOf(key)*1.6)*(this.explode||0);
    }
  }
  update({families,layers,explode,cut,clip,isolated,selected,grid,edges,physical,savedFilter,pan,hiddenParts,network,named}){
    this.panMode(pan);
    this.grid.visible=grid;this.grid.position.set(0,0,0);
    const pcbGrid=this.mode==='pcb3';
    this.grid.material.uniforms.pcbGrid.value=pcbGrid?1:0;
    this.grid.material.transparent=pcbGrid;this.grid.material.depthTest=pcbGrid;
    this.grid.renderOrder=pcbGrid?4:-100;
    this.surfaceMode=this.mode==='pcb3'&&physical;
    this.landsAtRest=explode===0&&!hiddenParts.has('Exposed_lands')&&(!isolated||isolated==='Exposed_lands');
    this.boardAssembled=explode===0&&!cut&&!isolated&&(!this.surfaceMode||!this.roots.finished.children.some(n=>hiddenParts.has(n.name)));
    const board=this.roots.pcb?.getObjectByName('PCB_1mm');
    if(board?.isMesh){
      board.userData.nativeMaterial ||= board.material;
      if(this.mode==='case'&&!board.userData.enclosureMaterial){
        const mat=board.userData.nativeMaterial.clone();
        mat.color.setRGB(.029,.047,.041);mat.clippingPlanes=[this.clipMat];
        board.userData.enclosureMaterial=mat;
      }
      board.material=this.mode==='case'?board.userData.enclosureMaterial:board.userData.nativeMaterial;
    }
    const inspectingPort=this.mode==='case' && !named && selected==='J101';
    if((this.followPort || inspectingPort) && Number.isFinite(this.explode) && explode!==this.explode){
      const shift=this.portOffset(explode-this.explode);
      this.controls.target.add(shift);this.camera.position.add(shift);
    }
    this.isolated=isolated;this.enabledLayers=layers;this.explode=explode;this.cut=cut;this.clipMat.constant=cut?clip:10000;
    if(this.roots.enclosure)this.roots.enclosure.visible=this.mode==='case';
    if(this.roots.pcb)this.roots.pcb.visible=!this.surfaceMode;
    if(this.roots.finished)this.roots.finished.visible=this.surfaceMode;
    for(const n of this.nodes()){
      const group=caseFamily(n.userData.group);
      n.visible=(this.mode==='pcb3'||families.has(group))&&(!isolated||n.name===isolated)&&!hiddenParts.has(n.name)&&savedVisibility(n.name,this.mode==='case'?savedFilter:'all');
      if(edges&&!n.userData.outlines){
        n.userData.outlines=[];const meshes=[];n.traverse(m=>{if(m.isMesh)meshes.push(m)});
        this.lineMaterial ||= new THREE.LineBasicMaterial({color:0x252b32,transparent:true,opacity:.63,clippingPlanes:[this.clipMat]});
        for(const m of meshes){const line=new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry,38),this.lineMaterial);m.add(line);n.userData.outlines.push(line)}
      }
      for(const l of n.userData.outlines||[])l.visible=edges;
      const delta=this.mode==='case'?n.userData.explode:[0,0, n.name==='PCB_1mm'?0:n.name==='Exposed_lands'?2:12];
      n.position.copy(n.userData.base).addScaledVector(vec(...delta),explode*(this.mode==='case'?1.65:1));
    }
    this.films.visible=this.mode==='pcb3';this.updateFilms();
    if(this.mode==='pcb3'&&!isolated&&!this.surfaceMode)for(const key of layers)this.addFilm(key).catch(()=>{});
    if(isolated)this.films.visible=false;
    const inCase=this.mode==='case';
    this.netOverlay.setNetwork(!isolated && (!inCase || board?.visible) ? network : null);
    if(inCase && board)this.netOverlay.position.copy(board.position);
    else this.netOverlay.position.set(0,0,0);
    if(this.netOverlay.visible){
      const [top,bottom,lands]=this.netOverlay.children;
      top.visible=inCase || physical || layers.has('topCopper');bottom.visible=inCase || physical || layers.has('bottomCopper');
      const filmZ=key=>films[key]+Math.sign(films[key])*(2+Object.keys(films).indexOf(key)*1.6)*explode;
      if(inCase){
        top.position.z=.046;bottom.position.z=-1.012;lands.position.z=.048;
      }else{
        top.position.z=physical?1.012:filmZ('topCopper')+.008;
        bottom.position.z=physical?-.012:filmZ('bottomCopper')-.008;
        lands.position.z=(physical?1.016:.048)+2*explode;
      }
      lands.visible=!hiddenParts.has('Exposed_lands');
    }
    this.select(selected);this.draw();
  }
  bounds(only){
    const box=new THREE.Box3();
    for(const n of this.nodes())if(n.visible&&(!only||n.name===only))box.expandByObject(n);
    const pads=this.references?.[only]?.lands;
    if(box.isEmpty() && pads && !this.nodes().some(n=>n.name===only)){
      const owner=this.nodes().find(n=>n.name==='Exposed_lands');
      if(owner?.visible){
        const z=owner.position.z+(this.surfaceMode?1:.035);
        for(const [x,y,w,h] of pads){
          box.expandByPoint(vec(x-w/2+owner.position.x,y-h/2+owner.position.y,z-.04));
          box.expandByPoint(vec(x+w/2+owner.position.x,y+h/2+owner.position.y,z+.04));
        }
      }
    }
    if(box.isEmpty())return null;return box;
  }
  select(name){
    for(const marker of [this.highlight,this.occludedHighlight]){
      if(marker){this.scene.remove(marker);marker.geometry.dispose();marker.material.dispose()}
    }
    this.highlight=this.occludedHighlight=null;
    if(!name)return;
    const box=this.bounds(name);if(!box)return;
    box.expandByScalar(.2);this.highlight=new THREE.Box3Helper(box,0x65c8ff);this.highlight.material.depthTest=true;this.highlight.renderOrder=20;this.highlight.material.depthWrite=false;this.scene.add(this.highlight);
    if(this.mode==='case' && this.references[name]){
      // Keep an internal connector locatable through the housing. Only the
      // edges behind an opaque surface receive this subdued outline.
      const marker=new THREE.Box3Helper(box,0x65c8ff);
      marker.material.depthFunc=THREE.GreaterDepth;marker.material.depthWrite=false;
      marker.material.transparent=true;marker.material.opacity=.7;
      marker.renderOrder=21;this.scene.add(marker);this.occludedHighlight=marker;
    }
  }
  fit(preset='iso',only=null){
    this.savedRecord=null;this.followPort=false;
    const box=this.bounds(only);if(!box)return;
    const center=box.getCenter(vec(0,0,0));const enclosure=this.mode==='case';
    const dirs=enclosure?{iso:[-.56,-.32,-1],front:[0,0,-1],back:[0,0,1],side:[-1,0,0],usb:[-1,.20,.22]}:{iso:[-.48,-.6,1],front:[0,0,1],back:[0,0,-1],side:[-1,0,.001]};
    const dir=preset==='current'?this.camera.position.clone().sub(this.controls.target).normalize():vec(...dirs[preset]).normalize();
    this.camera.up.copy(enclosure?vec(0,-1,0):vec(0,1,0));this.controls.target.copy(center);this.camera.position.copy(center).addScaledVector(dir,600);
    this.camera.lookAt(center);this.camera.updateMatrixWorld();
    const right=vec(1,0,0).applyQuaternion(this.camera.quaternion),up=vec(0,1,0).applyQuaternion(this.camera.quaternion);
    const span=box.getSize(vec(0,0,0));const extent=axis=>Math.abs(axis.x)*span.x+Math.abs(axis.y)*span.y+Math.abs(axis.z)*span.z;
    this.camera.zoom=Math.min((this.camera.right-this.camera.left)/Math.max(3,extent(right)),200/Math.max(3,extent(up)))*.88;
    this.camera.updateProjectionMatrix();this.controls.update();this.draw();
  }
  zoom(by){this.savedRecord=null;this.camera.zoom=THREE.MathUtils.clamp(this.camera.zoom*by,.12,140);this.camera.updateProjectionMatrix();this.draw()}
  rotate(dx,dy){this.savedRecord=null;const offset=this.camera.position.clone().sub(this.controls.target);offset.applyAxisAngle(this.camera.up,dx);offset.applyAxisAngle(vec(1,0,0).applyQuaternion(this.camera.quaternion),dy);this.camera.position.copy(this.controls.target).add(offset);this.controls.update();this.draw()}
}
