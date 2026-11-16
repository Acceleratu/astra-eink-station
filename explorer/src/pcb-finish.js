import * as THREE from 'three';
import {cameras} from './fusion.js';

// The depth atlas records the frontmost CAD body and distance at each sample.
// Look up colours in original board coordinates, also when the part is lifted.
export async function finishBoard(root,loader,clip,anisotropy){
  const load=async file=>{
    const tex=await loader.loadAsync('explorer/native/'+file);
    tex.colorSpace=THREE.SRGBColorSpace;tex.anisotropy=anisotropy;
    return tex;
  };
  const [under,bottom,lands,coating,depth,views]=await Promise.all([
    load('board-under-lands.webp'),load('board-bottom.webp'),load('board-top.webp'),
    load('board-packages.webp'),loader.loadAsync('explorer/native/board-depth.png'),
    fetch('explorer/data/pcb-appearance.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json()})
  ]);
  depth.minFilter=depth.magFilter=THREE.NearestFilter;depth.generateMipmaps=false;
  coating.minFilter=THREE.LinearFilter;coating.generateMipmaps=false;
  const frames=views.map(({camera,gain,pose})=>{
    const [target,eye,vertical,extent]=pose||cameras.pcb3[camera],dir=new THREE.Vector3(...eye).normalize();
    const right=new THREE.Vector3(...vertical).cross(dir).normalize(),up=dir.clone().cross(right);
    return {dir,right,up,extent,target:new THREE.Vector3(...target),gain:new THREE.Vector3(...gain)};
  });
  const count=frames.length,weights=new Float32Array(count),gain=new THREE.Vector3(1,1,1);
  const uniforms={
    pcbCoating:{value:coating},pcbDepth:{value:depth},boardAssembled:{value:1},showLands:{value:1},boardWithLands:{value:lands},pcbGain:{value:gain},viewWeight:{value:weights},
    frameCenter:{value:frames.map(f=>f.target)},frameDir:{value:frames.map(f=>f.dir)},
    frameRight:{value:frames.map(f=>f.right)},frameUp:{value:frames.map(f=>f.up)},
    frameExtent:{value:frames.map(f=>f.extent)}
  };
  const directions=frames.map(f=>f.dir),sight=new THREE.Vector3();
  for(const node of root.children){
    node.traverse(mesh=>{
      if(!mesh.isMesh)return;
      const mat=mesh.material.clone(),kind=mat.name;
      mat.clippingPlanes=[clip];mesh.material=mat;
      const isSurface=['top','bottom','land'].includes(kind);
      if(node.name==='PCB_1mm'&&!isSurface)return;
      const board=node.name==='PCB_1mm';
      mat.customProgramCacheKey=()=>[kind,board].join('-');
      mat.onBeforeCompile=shader=>{
        Object.assign(shader.uniforms,uniforms);
        shader.uniforms.bodyId={value:node.userData.owner};
        shader.uniforms.boardFace={value:kind==='bottom'?bottom:kind==='land'?lands:under};
        shader.uniforms.faceSide={value:kind==='bottom'?-1:1};
        shader.vertexShader='varying vec3 pcbPoint;\n'+shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\npcbPoint=position;');
        let apply='';
        if(isSurface)apply+=`
          vec3 n=normalize(cross(dFdx(pcbPoint),dFdy(pcbPoint)));
          vec2 faceUV=.5+(pcbPoint.xy-vec2(56.,42.))*vec2(faceSide*.75,1.)/86.;
          vec3 bare=texture2D(boardFace,faceUV).rgb;
          ${kind==='top'?'if(showLands>.5)bare=texture2D(boardWithLands,faceUV).rgb;':''}
          vec3 finishGain=mix(vec3(1.),pcbGain,smoothstep(.01,.08,bare.g-bare.r));
          outgoingLight=mix(outgoingLight,bare*finishGain,smoothstep(.85,.98,abs(n.z)));
        `;
        apply+=`
          if(${board?'boardAssembled>.5':'true'}){
          vec3 finish=vec3(0.);float total=0.;
          for(int i=0;i<${count};i++){
            if(viewWeight[i]<.0001)continue;
            vec3 delta=pcbPoint-frameCenter[i];
            vec2 uv=.5+vec2(dot(delta,frameRight[i])*.65625,dot(delta,frameUp[i]))/frameExtent[i];
            float edge=min(min(uv.x,uv.y),min(1.-uv.x,1.-uv.y));
            if(edge<=.002)continue;
            vec2 tile=vec2(mod(float(i),4.),3.-floor(float(i)/4.));
            vec2 at=(tile+uv)*.25;vec3 code=floor(texture2D(pcbDepth,at).rgb*255.+.5);
            if(abs(code.r-bodyId)>.1)continue;
            float dist=(code.g*256.+code.b)/200.-160.;
            float tolerance=max(.06,frameExtent[i]/525.*1.5);
            float visible=1.-smoothstep(tolerance,tolerance*2.,abs(dist-dot(delta,frameDir[i])));
            float w=viewWeight[i]*visible*smoothstep(.002,.012,edge)*clamp(35./frameExtent[i],.35,3.);
            finish+=texture2D(pcbCoating,at).rgb*w;total+=w;
          }
          outgoingLight=mix(outgoingLight,finish/max(total,.000001),smoothstep(.0005,.022,total));
          }
        `;
        shader.fragmentShader=`varying vec3 pcbPoint;
          uniform sampler2D pcbDepth,pcbCoating,boardFace,boardWithLands;
          uniform float bodyId,faceSide,boardAssembled,showLands;uniform vec3 pcbGain;
          uniform vec3 frameCenter[${count}],frameDir[${count}],frameRight[${count}],frameUp[${count}];
          uniform float frameExtent[${count}],viewWeight[${count}];
        `+shader.fragmentShader.replace('#include <opaque_fragment>',apply+'\n#include <opaque_fragment>');
      };
    });
  }
  return (camera,assembled,landsAtRest)=>{
    uniforms.boardAssembled.value=assembled?1:0;uniforms.showLands.value=landsAtRest?1:0;
    camera.getWorldDirection(sight).negate();gain.set(0,0,0);let total=0;
    directions.forEach((d,i)=>{
      const angle=Math.max(0,1-sight.dot(d));
      weights[i]=Math.pow(.025/(.025+angle),2.8);
      if(d.z*sight.z>=0){gain.addScaledVector(frames[i].gain,weights[i]);total+=weights[i]}
    });
    if(total){gain.divideScalar(total);gain.multiply(gain)}else gain.set(1,1,1);
  };
}
