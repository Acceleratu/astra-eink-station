import * as THREE from 'three';
const NS='http://www.w3.org/2000/svg';
const faces=[
  [[1,0,0],'right','Right','Dreapta'],[[-1,0,0],'left','Left','Stânga'],
  [[0,1,0],'yplus','Front','Față'],[[0,-1,0],'yminus','Back','Spate'],
  [[0,0,1],'zplus','Top','Sus'],[[0,0,-1],'zminus','Bottom','Jos']
];
export class NavigationCube{
  constructor(svg,choose){
    this.svg=svg;this.items=[];
    const ro=document.documentElement.lang==='ro';
    for(const [axis,key,en,label] of faces){
      const group=document.createElementNS(NS,'g'),poly=document.createElementNS(NS,'polygon'),txt=document.createElementNS(NS,'text');
      txt.setAttribute('text-anchor','middle');txt.setAttribute('dominant-baseline','central');group.append(poly,txt);svg.append(group);
      group.setAttribute('role','button');const select=()=>choose(new THREE.Vector3(...axis));
      group.addEventListener('click',select);group.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select()}});
      this.items.push({axis:new THREE.Vector3(...axis),key,group,poly,txt,label:ro?label:en});
    }
  }
  update(camera,mode){
    const inv=camera.quaternion.clone().invert();const ro=document.documentElement.lang==='ro';
    for(const {axis,key,group,poly,txt,label} of this.items){
      const n=axis.clone().applyQuaternion(inv);
      const shown=n.z>.035;group.style.display=shown?'':'none';group.setAttribute('tabindex',shown?'0':'-1');if(!shown)continue;
      const u=axis.x?new THREE.Vector3(0,1,0):new THREE.Vector3(1,0,0);
      const v=axis.clone().cross(u);
      const corners=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>{
        const p=axis.clone().addScaledVector(u,a).addScaledVector(v,b).applyQuaternion(inv);
        return [46+22*p.x,42-22*p.y];
      });
      poly.setAttribute('points',corners.map(v=>v.join(',')).join(' '));const shade=Math.round(166+74*n.z);poly.setAttribute('fill','rgb('+[shade,shade+2,shade+3].join(',')+')');
      const cx=46+22*n.x,cy=42-22*n.y;txt.setAttribute('x',cx);txt.setAttribute('y',cy);
      const names=mode==='case'?{zminus:ro?'Față':'Front',zplus:ro?'Spate':'Back',yminus:ro?'Sus':'Top',yplus:ro?'Jos':'Bottom'}:{yplus:ro?'Spate':'Back',yminus:ro?'Față':'Front'};
      const title=names[key]||label;group.setAttribute('aria-label',title);txt.textContent=n.z>.38?title.toUpperCase():'';
    }
  }
}
