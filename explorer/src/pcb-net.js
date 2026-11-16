import * as THREE from 'three';

// Geometry is in board millimetres. Face and land heights are set by the active
// PCB model, so the same routing follows both the finished and exploded views.
function stripe(vertices,x,y,endX,endY,width){
  const length=Math.hypot(endX-x,endY-y);
  if(!length)return;
  const dx=-(endY-y)*width/(2*length),dy=(endX-x)*width/(2*length);
  vertices.push(x+dx,y+dy,0,x-dx,y-dy,0,endX-dx,endY-dy,0,
    endX-dx,endY-dy,0,endX+dx,endY+dy,0,x+dx,y+dy,0);
}

function ring(vertices,x,y,radius){
  for(let i=0;i<12;i++){
    const a=i*Math.PI/6,b=(i+1)*Math.PI/6;
    stripe(vertices,x+radius*Math.cos(a),y+radius*Math.sin(a),
      x+radius*Math.cos(b),y+radius*Math.sin(b),.10);
  }
}

export class PCBNet extends THREE.Group {
  constructor(){
    super();
    this.materials=[0xffe06d,0xd9a8ff,0xffed9c].map(color=>new THREE.MeshBasicMaterial({
      color,side:THREE.DoubleSide,depthWrite:false,toneMapped:false
    }));
    for(const material of this.materials){
      const mesh=new THREE.Mesh(new THREE.BufferGeometry(),material);
      mesh.renderOrder=35;this.add(mesh);
    }
  }
  setNetwork(network){
    this.visible=Boolean(network);
    if(this.network===network)return;
    this.network=network;
    const vertices=[[],[],[]];
    if(network){
      for(const [x,y,a,b,width,layer] of network.wires)stripe(vertices[layer===1?0:1],x,y,a,b,Math.max(.20,width));
      for(const [x,y] of network.vias){
        ring(vertices[0],x,y,.25);ring(vertices[1],x,y,.25);
      }
      for(const [,,x,y] of network.contacts)ring(vertices[2],x,y,.21);
    }
    this.children.forEach((mesh,i)=>{
      mesh.geometry.dispose();
      const geometry=new THREE.BufferGeometry();
      geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices[i],3));
      mesh.geometry=geometry;
    });
  }
}
