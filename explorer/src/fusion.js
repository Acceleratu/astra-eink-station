// Saved orthographic inspection cameras. Target and vertical extent use millimetres.
export const cameras={
  case:{
    spread:[[63.12786,35.30838,59.22283],[1.9,-.30,-.83],[0,-1,0],360,'all','Exploded side view','Ansamblu din lateral'],
    '01-front':[[57,4.5,1.2],[-.32,-.12,-1],[0,-1,0],260,'all','Assembly','Ansamblu',[[41.149,29.321,3.294],323.25]],
    '02-front-normal':[[57,4.5,0],[0,0,-1],[0,-1,0],260,'all','Front','Față'],
    '03-back':[[57,4.5,3],[.25,-.15,1],[0,-1,0],260,'all','Rear','Spate',[[47.036,30.098,9.331],295.2]],
    '04-open':[[57,-2.5,1],[-.17,.12,1],[0,-1,0],247,'open','Cover removed','Capac demontat'],
    '05-usb':[[-3.4,67,1.725],[-1,.20,.22],[0,-1,0],32,'all','USB-C','USB-C'],
    '06-sensor':[[34,85.5,4],[.11,.32,1],[0,-1,0],34,'open','Sensor','Senzor'],
    '07-controls':[[66,72.5,14],[.04,.28,1],[0,-1,0],50,'nostand','Buttons','Butoane'],
    '08-back-interior':[[56,42.5,8],[.1,.1,-1],[0,-1,0],144,'lid','Inside rear cover','Interiorul capacului'],
    '10-usb-axial':[[-3.2,67,1.725],[-1,0,0],[0,-1,0],29,'all','USB-C axial','USB-C axial'],
    '11-usb-opposite':[[-3.4,67,1.725],[-1,-.32,-.34],[0,-1,0],32,'all','USB-C opposite angle','USB-C din unghiul opus']
  },
  pcb3:{
    assembled:[[58,42,1],[.28,-.60,1],[0,1,0],97,'all','Assembly','Ansamblu'],
    top:[[58,42,1],[0,0,1],[0,1,0],96,'all','Top','De sus'],
    bottom:[[58,42,1],[0,0,-1],[0,1,0],96,'all','Bottom','De jos'],
    'usb-battery':[[15,56,1.5],[-.50,-.50,.95],[0,1,0],47,'all','USB and battery','USB și baterie'],
    harvester:[[22,71.5,1.5],[.16,-.38,1],[0,1,0],36,'all','Solar harvester','Alimentare solară'],
    'radio-pogo':[[101.5,47.3,1.5],[.45,-.45,1],[0,1,0],48,'all','Radio and SWD','Radio și SWD'],
    display:[[46,9,1.5],[.15,-.70,1],[0,1,0],48,'all','Display connector','Conector afișaj'],
    'underside':[[56,42,0.45],[0.48,0.6,-0.78],[0,1,0],100,"all","Underside at an angle","Verso din unghi"],
    'usb-mouth':[[3.45,67,2.3],[-1,-0.28,0.47],[0,1,0],15,"all","J101 · USB-C opening","J101 · Deschiderea USB-C"],
    'fpc-contacts':[[47.5,3.3,2],[0.25,-0.88,0.67],[0,1,0],18,"all","J301 · FPC contacts","J301 · Contacte FPC"],
    'radio-module':[[108.05,56,2],[0.65,0.5,0.86],[0,1,0],21,"all","U201 · Radio module","U201 · Modul radio"],
    'bme280':[[33.5,80.6,1.5],[-0.4,0.5,0.9],[0,1,0],8,"all","U404 · BME280","U404 · BME280"],
    'key':[[47,79.1,2],[0.4,0.6,0.72],[0,1,0],9,"all","SW401 · Push button","SW401 · Buton"],
    'spv1050':[[20,69,1.5],[-0.42,-0.5,0.88],[0,1,0],10,"all","U101 · Solar harvester","U101 · Alimentare solară"]
  }
};
export const explodedReferences=['spread','01-front','03-back','05-usb','10-usb-axial','11-usb-opposite'];
export const nativePresets={top:[1,17,18,20,21,25],bottom:[16,17,18,20,22,26],assembly:[17,18,20,21,25,51]};
export const homeView=mode=>mode==='case'?'01-front':'assembled';
export function savedVisibility(name,mode){
  const rear=name==='rear_cover'||name==='key_keeper'||/^(battery|key_|case_screw|guard_)/.test(name);
  if(mode==='open')return !rear&&name!=='desktop_stand';
  if(mode==='lid')return rear;
  if(mode==='nostand')return name!=='desktop_stand';
  return true;
}
export function nativePCB(group,state,element){
  const {native,nativeLayers:enabled}=state;
  const [x,y,width,height]=native.boardBox;
  const face=['top','bottom'].find(key=>nativePresets[key].length===enabled.size && nativePresets[key].every(id=>enabled.has(id)));
  const href=face?'explorer/native/'+face+'.webp':state.layerImage(enabled);
  element('image',{href,x,y,width,height,'pointer-events':'none'},group);
}
