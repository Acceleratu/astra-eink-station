# Conversie pentru o muchie FR4 avansată

Dacă fusta nominală de 125 µm are sub 0,020 mm joc față de muchia frezată a PCB-ului, măsurați poziția muchiei și verificați varianta cu bavetă înainte de a exclude placa. În ansamblul nominal, distanța între FR4 și PET este 0,0525 mm. Conversia înlocuiește subansamblul frontal livrat de convertor. Gura PET, poziția J101, adezivul pe oțel, cele două protecții laterale și ancora superioară au aceleași dimensiuni și poziții. [Subansamblul alternativ cu șapte componente numite](Board-edge-conversion.step) · [Secțiunea și inspecția versiunii nominale](../README.md)

## Alegerea piesei

În sistemul plăcii, comparați muchia FR4 cu fața metalică J101, X = −0,0025 mm. Suprafața dinspre PCB a bavetei este la X = −0,2275 mm. Pentru o muchie locală avansată până la X = −0,2075 mm, cu partea superioară a FR4 la Z ≤ 0, rămân 0,020 mm până la bavetă. Fusta superioară de 125 µm se termină la Z = +0,080 mm și eliberează colțul PCB. Verificați muchia reală, inclusiv masca de lipire sau bavurile, prin microscop înainte de montare. Cereți cel puțin 0,020 mm la oricare dintre cele trei straturi noi și 0,05–0,40 mm de la fața bavetei la peretele rigid al buzunarului. Distanța digitală la perete este 0,0725 mm pentru bavetă și 0,1725 mm pentru fusta superioară. Pentru alegere simultană se folosește placa, carcasa și conectorul aceleiași unități.

JLCPCB publică pentru contururi frezate o toleranță dimensională de ±0,20 mm la precizia uzuală. Cota de recepție relevantă aici este poziția efectivă a muchiei față de conector după asamblare. Ea include și plasarea conectorului pe PCB. [Capabilități JLCPCB pentru contururi frezate](https://jlcpcb.com/capabilities/pcb-capabilities)

## Piese de convertit industrial

În cele trei DXF, (0,0) este centrul gurii J101. Coordonata verticală a desenului devine Z − 1,725 mm la montaj. Fiecare dintre cele trei piese se livrează în registru pe același suport, complet prelaminată.

| Strat | Film și poziție | Șablon și suprafață |
|---|---|---|
| Fustă superioară | Toray #125-X30, X −0,1775…−0,0525 mm. Marginea inferioară la Z +0,080 ±0,010 mm. | Conturul superior păstrează gura 8,68 × 2,90 R1,08. [DXF pentru piesa superioară](Conversion-upper-X30-125um.dxf) |
| Bavetă | Toray #50-X30, X −0,2775…−0,2275 mm. | Urechi până la Z +2,225 mm, degajare 8,84 × 3,06 R1,16. [DXF pentru bavetă](Conversion-apron-X30-50um.dxf) |
| Legătură opacă între folii | tesa 68822 negru de 0,050 mm, X −0,2275…−0,1775 mm. | Suprafață lipită 13,487 mm², zonă centrală minimă de 0,075 mm și reazeme laterale late. [DXF pentru legătura opacă](Conversion-apron-bond-tesa-68822-50um.dxf) |

Convertorul prelaminează pe fața bavetei dinspre PCB, la X −0,2275 mm, legătura tesa tăiată pe liner, apoi o transferă pe fața vizibilă a fustei de 125 µm. Toate cele trei straturi sunt negre. În secțiune, baveta formează treapta spre exterior. Pe spate se montează subansamblul standard cu adezivul de pe buza conectorului și protecțiile urechilor. Folosiți laserul calificat pe același lot și masa cu repere optice. Acceptați excentricitate suplimentară bavetă–fustă ≤0,020 mm radial, intersecție verticală a foliilor ≥0,080 mm în secțiunea centrală și lățime fizică ≥0,040 mm pentru ligatura adezivă pe întregul interval Y 60,40…73,60 mm. Legătura trebuie să fie continuă, fără por, fibră, dezlipire sau întrerupere care traversează banda. Măsurați și opacitatea foliei de 50 µm din acest lot la pragul din fișa nominală. Păstrați piesa pe suport până la aplicarea pe J101.

Pe exemplarul cu placa liberă, se montează subansamblul alternativ întreg după aceeași procedură cu mandrină, masă XY, comparator și presă limitată. Verificați cele cinci criterii de recepție ale gurii, inclusiv proiecția fustei superioare PET pe oțel, și controlați ancora. Baveta păstrează fereastra nominală a fustei superioare. [Recepția direcțională](../optical-receiving.md) Efectuați proba de iluminare, retenție după 72 h, ciclurile de conectare și scoaterea verticală în carcasa asamblată. Un modul deja lipit se înlocuiește integral folosind procedura de refacere calificată a atelierului. Trageți numai de banda susținută, protejați limba J101 și inspectați suportul metalic și lipiturile înainte de aplicarea piesei noi. [Procedura pentru prinderea pe J101 și probele fizice](../README.md)

## Ce a verificat modelul

Verificatorul citește STEP-ul carcasei livrate, îl montează virtual cu subansamblul alternativ reimportat și caută intersecții cu PCB, J101, componentele din jur și carcasa. Testează apoi o extensie locală solidă a FR4 până la X −0,2075 mm și ridică prismatic cu 20 mm fiecare dintre cele trei straturi. Reuniunea frontală păstrează exact proiecția fustei nominale. În cotul inferior, volumul de la X −0,2775…−0,0525, Y 60,40…73,60, Z 0,130…0,150 mm este ocupat integral de PET negru sau tesa negru. O rază care ar trece între cele două folii întâlnește această bandă pe întreaga lățime accesibilă din exterior. La centrul deschiderii, baveta are încă 0,080 mm față de profilul PET original. Verificatorul variantei · [Rezultate pe STEP și șabloane](results.json)

Pe peretele reprofilat din STEP-ul `0ecf7606…cf062447`, jocul bavetei este 0,0725 mm atât în poziția montată, cât și la scoaterea pe 20 mm. Verificarea cu muchia FR4 extinsă până la X −0,2075 mm a păstrat jocul de 0,0200 mm. [Rezultatul verificării pe această carcasă](results.json)

Proba fizică de montare și calificarea convertorului rămân de executat. Această arhivă servește atelierului pentru cazurile în care muchia reală impune conversia. Lista și modelele de fabricație nominale din `templates/` descriu în continuare fusta plană.
