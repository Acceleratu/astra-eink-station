# O stație meteo solară cu afișaj e-paper

Jurnalul de proiectare și prototipul sunt realizate de Acceleratu. Articolul este disponibil [în română](ro.html) și [în engleză](index.html). Ambele pagini se pot deschide direct de pe disc. În previzualizarea prin HTTP, documentele Markdown se deschid în limba selectată. Pentru fișierele hardware, descarcă [arhiva proiectului](station-project.zip).

Stația folosește un modul nRF54L15, un ecran e-paper Waveshare de 4,2 inchi, senzorul BME280, alimentare solară și încărcare prin USB-C. Hardware-ul a fost verificat în software. Prima pornire, încărcarea bateriei, raza radio, potrivirea fizică a fișei USB și imprimarea carcasei urmează să fie verificate pe prototip.

## Ce conține arhiva

- Deschide `schematic/astra.sch`, `board/astra.brd` și `hardware/astra.lbr` ca fișiere editabile Autodesk Electronics / EAGLE. Arhiva include și schema PDF și desenul de asamblare.
- În `fab/` găsești straturile de fabricație, găurile, lista de conexiuni IPC, lista de materiale, coordonatele de plasare, geometria șablonului de pastă și harta punctelor de test. Datele despre disponibilitatea componentelor reflectă catalogul la data proiectării.
- În `mechanical/` găsești placa echipată și carcasa asamblată în format STEP, generatorul carcasei, 11 piese STL imprimabile, desenele pentru piesele decupate și ghidul ilustrat de montaj. Fișierele STEP păstrează geometria ansamblului. Generatorul CAD conține dimensiunile editabile și logica de construcție.
- În `firmware/` găsești sursele Zephyr, testele care rulează pe calculator și fișierul Intel HEX compilat. Versiunile instrumentelor necesare compilării sunt în README-ul din acel director.
- În `docs/`, `verification/` și în jurnalul de proiect sunt consemnate deciziile tehnice, verificările digitale, excepțiile și probele fizice rămase.

## Cum se citesc rapoartele

Articolul folosește rapoartele originale de verificare. Valorile SHA-256 din rapoartele istorice identifică fișierele utilizate la testele respective. În pachetul distribuit au fost curățate anteturile STEP, metadatele imaginilor, PDF-urilor și desenelor, anteturile STL și comentariile din exporturile Gerber. Geometria STEP și triunghiurile STL sunt păstrate. Verificatorul zonei USB folosește suma de control a ansamblului distribuit. Pentru verificarea arhivei și a fișierelor folosește `SHA256SUMS` din rădăcina proiectului.

Arhivele conțin fișierele tehnice alese pentru livrare. Din distribuție au fost excluse instrumentele de compilare terțe, bibliotecile de componente ale furnizorilor, arhivele de proiect din cloud, conversațiile brute ale agenților și fișierele de compilare specifice calculatorului. Tabelul de consum însumează datele pentru cele trei cereri de proiectare hardware.

## Exploratorul interactiv

Ambele versiuni ale articolului includ același explorator local. Deschide-l prin HTTP. Pe cele șapte foi de schemă poți selecta componentele și etichetele de rețea. Vederea PCB combină cele zece straturi de fabricație cu cinci suprapuneri CAD și include o riglă în milimetri și căutare după componentă sau rețea. Modelul 3D al plăcii include 139 de componente montate. Carcasa adaugă 111 obiecte 3D denumite, o vedere explodată, o secțiune și un detaliu al portului USB. Modelele afișate servesc inspecției vizuale. Pentru lucrul tehnic folosește ansamblurile STEP și exporturile Gerber și drill.

Deschide `?view=case&pose=spread#explorer` pentru ansamblul explodat sau `?view=pcb3&part=J101#explorer` pentru conectorul USB. Pe un ecran tactil poți trage modelul sau poți apropia și depărta două degete pentru zoom. Din tastatură, activează zona de vizualizare și folosește săgețile, +, − și 0. Exploratorul servește local resursele și biblioteca Three.js. Pentru a reconstrui codul JavaScript, rulează `npm install` și `npm run build` în `explorer/`. Generatorul `explorer/tools/drawings.py` primește schema PDF vectorială. PDF-ul public este aplatizat. Convertorul de modele 3D folosește manifestul original al geometriei de prezentare CAD și fișierul STEP al plăcii echipate.

### Spațiul de lucru Fusion

Exploratorul pornește cu culorile din Fusion Electronics. Exporturile native ale celor șapte foi de schemă sunt aliniate cu etichetele interactive. Cele două fețe standard ale plăcii folosesc exporturile originale din Fusion. Pentru combinații de straturi, exploratorul folosește cele 37 de straturi exportate separat și aliniate la conturul plăcii. Din selectorul de afișare poți alege și PDF-ul vectorial sau straturile de fabricație.

Vederea 3D folosește camerele ortografice salvate în Fusion, ansamblul umbrit, cubul de orientare interactiv, grila, lista de componente și afișarea opțională a muchiilor. Modelul plăcii finite folosește geometriile din PCB-ul 3D nativ, inclusiv corpurile componentelor, găurile metalizate, padurile expuse și masca de lipire. Culorile suprafețelor provin din capturile Fusion. Fiecare punct proiectat este asociat corpului vizibil și adâncimii sale. Vederile de detaliu acoperă conectorii USB-C și FPC, modulul radio, circuitul de captare a energiei solare, senzorul și butonul. Capturile originale își păstrează pixelii fără pierderi și sunt disponibile la rezoluție completă pentru comparație. Browserul folosește WebGL pentru orientările alese liber.

Deschide `?workspace=1&view=case&camera=05-usb#explorer` pentru a vedea portul USB cu camera de inspecție, în spațiul de lucru extins pe toată fereastra. Distribuția locală include toate datele folosite de aceste vederi.
