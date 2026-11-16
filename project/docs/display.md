# Afișajul de 4,2″ și repornirea după întreruperea alimentării

## Identificarea panoului

Se comandă separat **Waveshare 13186, 4.2inch e-Paper, varianta alb/negru, panou fără placă, revizia V2 cu SSD1683**. Pagina de comandă identifica produsul ca disponibil la 15 noiembrie 2026. La recepție se înregistrează SKU, eticheta V2 de pe verso, seria sau marcajul flexului și fotografii ale ambelor fețe. Desenul cotat V2 precizează controlerul SSD1683, rezoluția 400 × 300, pasul pixelului de 0,212 mm și suprafața activă 84,80 × 63,60 mm. Edițiile V1 și cele cu pigmenți suplimentari au alte cerințe electrice sau alte forme de undă. [Produs Waveshare](https://www.waveshare.com/4.2inch-e-paper.htm) · Desen V2, pag. 4 · Fișa de achiziție datată

## Interfața cu placa

J301 este **Hirose FH12-24S-0.5SH(55)**, cod C202112, contact inferior, deschidere ZIF frontală și inserție orizontală. J301, Q301, D301–D303 și L301 au fost comparate cu desenele producătorilor. Inventarul de montaj păstrează ambele valori de disponibilitate returnate de JLCPCB pentru fiecare cod C. Panoul din sticlă și bateria se montează manual. [Fișa Hirose](https://www.hirose.com/en/product/p/CL0586-0521-0-55) · Instantaneu JLCPCB al blocului

| Pini J301 | Funcție verificată pe desen și în tabelul panoului | Conectare |
|---|---|---|
| 1, 4 | NC | Izolați individual |
| 2, 3 | GDR, RESE | Poarta Q301 și sursa Q301 cu șuntul R302 |
| 5 | VSH2 | C303 la masă |
| 6, 7 | TSCL, TSDA | Libere. Firmware selectează senzorul termic intern prin 18h = 80h |
| 8, 9, 10 | BS1, BUSY activ sus, reset activ jos | Masă pentru SPI pe patru fire, intrare BUSY și ieșire RESET la MCU |
| 11, 12, 13, 14 | D/C, CS activ jos, SCL, SDA | Comandă/date, selecție, SCK, MOSI |
| 15, 16, 17 | VDDIO, VCI, VSS | VMAIN comutat de 3,3 V la ambii pini de alimentare, masă la 17 |
| 18, 19 | VDD, VPP | C305, C306 la masă. VDD este ieșirea regulatorului intern de aproximativ 1,8 V. VPP are exclusiv bypass la utilizare normală |
| 20, 21, 22, 23, 24 | VSH1, VGH, VSL, VGL, VCOM | C307…C311 respectiv. TP301 accesează VGH, TP302 accesează VGL |
| MP1, MP2 | Ancore metalice | Masă |

Figura generică de la pag. 32 etichetează diferit unele contacte. Pentru 1/4/5 prevalează cele două surse concordante din manualul exact V2, desenul pag. 4 și tabelul pag. 5–6. Pinul 4 rămâne izolat. Intrările cu pull-up extern, CS și RESET, folosesc exclusiv VMAIN. Rezistorul de 100 kΩ la masă menține BUSY jos când lipsește FPC. Firmware cere atât frontul activ cât și revenirea pentru a confirma afișarea. Manual Waveshare V2 · [Datele editabile ale circuitului](../hardware/display.json)

La conectorul în rotația din proiect, privit de sus dinspre fața cu componente, pinul 1 este în stânga, intrarea cablului este spre marginea de jos a plăcii, iar deplasarea de inserție este spre +Y. Se introduc degetele aurite spre PCB, cu rigidizatorul în sus. Pasul este 0,50 mm, distanța între centrele 1 și 24 este 11,50 mm, grosimea capătului este 0,30 ±0,03 mm. Lățimea permisă de desenul panoului este 12,50 ±0,10 mm, iar recomandarea FH12 este 12,50 ±0,07 mm. Pentru prototip se măsoară și se acceptă 12,43…12,57 mm. Se introduce la rece, drept, până la opritor, înainte de închiderea capacului. Desen Waveshare · Catalog FH12, landuri și flex

Sticla măsoară 91 × 77 × 1,2 mm. Centrul cozii se află la 23,05 mm de muchia stângă a sticlei, din cotele 16,80 + 12,50/2. Vârful depășește muchia sticlei cu 18,50 ±0,50 mm. Secțiunea Hirose indică 3,1 mm de la intrare la contact și 1,3 mm de la contact la vârf. Rezultă o inserție nominală de 4,4 mm. Față de centrul J301, în montajul de verificare cu flex drept, sticla ocupă X = −23,05…+67,95 mm și Y = −93,90…−16,90 mm, cu suprafața de afișare spre −Z. Din secțiunea cotată s-a estimat planul de contact la Z ≈ 0,55 mm, centrul capătului ranforsat la ≈ 0,70 mm și suprafața rigidizatorului la ≈ 0,85 mm deasupra PCB. Estimarea folosește scara segmentului de 3,1 mm și presupune că terminalul este așezat pe PCB. Producătorul nu publică toleranța verticală a ansamblului cu flex. Conectorul închis are 2,0 mm înălțime, iar deschiderea clapetei cere aproximativ 4,8 mm spațiu de service. Sticla se sprijină separat. Secțiune Hirose, pag. 12 · [Poziția de montaj, câmpul panel_pose](../hardware/display.json) · Măsurarea conturului STEP și a secțiunii PDF

Modelul STEP al conectorului este modelul parametrizat al comunității KiCad pentru FH12-24S-0.5SH. Originea sa are nevoie de o translație locală (0, +1,6, 0) mm pentru centrul corpului utilizat aici. Corpurile și contactele simplificate descriu conectorul închis. În zona de strângere, starea închisă fără cablu poate diferi de forma cu un flex real introdus. Fișier STEP · [Sursa KiCad](https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Connector_FFC-FPC.3dshapes/Hirose_FH12-24S-0.5SH_1x24-1MP_P0.50mm_Horizontal.step) · Licența bibliotecii

## Convertorul bipolar și condensatoarele

SSD1683 comandă Q301 prin GDR și măsoară căderea de tensiune pe R302, 3 Ω. R301, 10 kΩ, descarcă poarta. L301, 10 µH, leagă VMAIN de nodul SW. D303 redresează vârfurile pozitive spre VGH. C301 și D301 fixează nivelul nodului pompei în faza pozitivă, apoi D302 încarcă negativ rezervorul VGL. La D301 catodul este la masă, la D302 catodul este la nodul pompei, iar la D303 catodul este la VGH. Banda de pe diodă corespunde padului 1. Q301 are 1 = G, 2 = S, 3 = D. Schema locală leagă direct cele nouă componente ale etajului. Bobina are DCR de maximum 180 mΩ, 1,3 A RMS și 1,4 A la scăderea inductanței cu 30%. Schema panoului, pag. 32 · BSS138L · MBR0530 · SRN4018

Condensatoarele cu tensiune ridicată folosesc capsule mai mari pentru păstrarea capacității sub polarizare. Valorile de mai jos provin din interpolarea curbei tipice DC pentru exact seria și dielectricul alese. Coloana de sensibilitate înmulțește rezultatul cu 0,90 pentru toleranța inițială și cu 0,85 pentru variația termică. Ea ilustrează un caz de dimensionare. Curba publicată nu stabilește o limită garantată pentru fiecare lot. Date Samsung și cele două puncte de interpolare pentru fiecare reper

| Poziție | Valoare nominală | Tensiune analizată | Capacitate tipică | Sensibilitate ×0,765 |
|---|---:|---:|---:|---:|
| C301, condensatorul volant | 4,7 µF / 50 V, 1210 | 20 V | 3,630 µF | 2,777 µF |
| C302, rezervor de intrare | 4,7 µF / 25 V, 0805 | 3,3 V | 3,942 µF | 3,016 µF |
| C308 și C310, rezervoarele VGH și VGL | 1 µF / 100 V, 1206 | 20 V | 0,839 µF | 0,642 µF |
| C303/C306/C307/C309/C311, bypassuri analogice | 1 µF / 50 V, 0805 | 15 V | 0,796 µF | 0,609 µF |

Ngspice 47 a rulat tranzitoriu cu modelele SPICE3 publicate de onsemi, conectate după numărul fizic al padului din fișierul electric. Excitația de laborator este de 0,8 µs la fiecare 7 µs, cu limitare artificială la 20,2 V, 20 Ω la poartă și câte 100 kΩ sarcină pe fiecare șină. Sursa urcă într-o milisecundă prin 50 mΩ. Temperatura modelelor semiconductoare este 25 °C. Modelele reproduc etajul extern. Temporizarea GDR, reglajul intern SSD1683, sarcina pixelilor și timpul optic rămân caracteristici de măsurat. Ngspice a ridicat o rezistență internă numerică din modelul MOS de la 10⁻¹⁵ la 10⁻¹² Ω, mesaj păstrat în log. [Modelul MOS onsemi](https://www.onsemi.com/download/models/sp3/bss138lt1.sp3) · [Modelul Schottky onsemi](https://www.onsemi.com/download/models/sp3/mbr0530t1.rev0.sp3) · Fișiere SPICE și rezultate

| Caz la 39,98 ms | VGH | VGL | Curent maxim prin L301 | Putere medie R302 |
|---|---:|---:|---:|---:|
| Intrare 3,3 V, L = 10 µH | +20,126 V | −20,646 V | 204 mA | 5,29 mW |
| Intrare 3,1 V, L = 12 µH, R = 3,03 Ω, capacități ×0,765 | +20,127 V | −20,647 V | 167 mA | 3,53 mW |
| Defect injectat, D302 montată invers | +20,133 V | +0,124 V | 219 mA | 4,79 mW |

În cazul nominal, tensiunea maximă inversă pe cele trei diode a fost 20,95 V față de limita de 30 V. Q301 a ajuns la 20,43 V drenă–sursă față de 50 V. Curentul de drenă simulat a atins 275 mA la frontul impulsului, sub limita de 800 mA pentru impulsuri ≤10 µs. Puterea medie drenă–sursă a fost 9,73 mW. Cu rezistența termică de referință de 556 °C/W rezultă o creștere staționară orientativă de 5,4 °C la aceeași putere medie. Înjumătățirea pasului maxim de integrare de la 100 la 50 ns a schimbat VGH cu 0,1 mV și VGL cu 0,3 mV. Verificatorul a respins cazul cu D302 inversată exclusiv pentru polarizarea incorectă a VGL. Comanda de reproducere este `python3 verification/display/boost.py`. Scriptul descarcă modelele în director temporar și verifică SHA-256 înainte de folosire. Scriptul și condițiile de test · Log nominal · Log de injecție a defectului

Pe traseele extrase din placa nativă, legătura D303.1–C308.1 măsoară 22,978 mm, iar D302.2–C310.1 măsoară 14,516 mm. Ambele sunt pe stratul superior, fără via. La 35 µm cupru și 20 °C, rezistențele calculate din lățimea fiecărui segment sunt 62,88 și 39,72 mΩ. Nodurile SW și PUMP au lungimi totale de ramuri de 8,60 și 4,19 mm, pe fața superioară. Separarea dintre padul 2 al L301 și corpul Q301 este 0,375 mm la dimensiuni nominale și 0,305 mm cu anvelopa maximă onsemi 3,04 × 1,40 mm. Punctul de pin 1 al Q301 are cel puțin 0,220 mm până la deschiderile de mască verificate. Auditul geometric al șinelor · Traseele critice ale plăcii

Un al cincilea caz introduce între redresoare și rezervoarele de pe PCB câte o impedanță serie ipotetică, 30 nH + 80 mΩ spre VGH și 20 nH + 60 mΩ spre VGL. ESR ale condensatoarelor sunt de 30…40 mΩ. Aceste valori delimitează o încercare de sensibilitate, fără extracție electromagnetică din placa fabricată. Prima încercare, cu limitator artificial liniar pe porțiuni și condensatoare ideale, a oprit integrarea la 34,218 ms. Cu caracteristică artificială de limitare netedă și ESR finit, simularea s-a încheiat la 40 ms. Tensiunile rezervoarelor au ajuns la +20,100 V și −20,600 V, iar diferența instantanee maximă în valoare absolută dintre terminalul redresorului și rezervor a fost 1,127 V. Cel mai solicitat redresor a atins 20,994 V invers. Pe placa reală se măsoară direct la terminalele diodelor cu buclă scurtă de sondă și se compară cu limita de 30 V. Reproducerea folosește `python3 verification/display/interconnect.py`. Condiții și rezultate · Logul final · Logul încercării oprite

## Actualizarea după oprirea completă a VMAIN

SSD1683 păstrează imaginea fizică prin bistabilitatea pigmentului. RAM-ul intern trebuie reîncărcat după întreruperea alimentării. În modul alb/negru, tabelul 6-5 al controlerului indexează patru tranziții din biții celor două memorii. Driverul Waveshare folosește 21h = 00h,00h, bordură 3Ch = 80h, apoi 22h = FFh și 20h pentru actualizarea parțială. Secțiunile 6.6 și 7 ale controlerului descriu LUT din OTP și selecția modului 2. Implementarea publică GxEPD2 a unui panou SSD1683 de aceeași rezoluție confirmă explicit asocierea memoriilor 26h cu imaginea anterioară și 24h cu imaginea nouă. Waveform-ul folosit de placa Astra este cel din OTP al panoului Waveshare V2. SSD1683 rev. 1.0, tabelul 6-5 și comenzi · [Driverul original Waveshare V2, revizie fixată](https://github.com/waveshareteam/e-Paper/blob/d28b3c4cfc78eef1c6cd6e6e3013654e449d2864/Arduino/epd4in2_V2/epd4in2_V2.cpp) · [Identificarea memoriilor în GxEPD2](https://github.com/ZinggJM/GxEPD2/blob/master/src/gdey/GxEPD2_420_GDEY042T81.cpp)

După fiecare pornire, firmware așteaptă alimentarea, generează reset fizic activ jos, trimite reset software 12h și selectează senzorul intern. Fereastra acoperă octeții X = 0…49 și liniile Y = 0…299, cu originea setată din nou înaintea fiecărui plan. O scenă confirmată din RRAM permite regenerarea exactă a celor 15 000 de octeți ai imaginii vechi. Firmware scrie planul vechi la 26h și cel nou la 24h. Peste tot unde imaginea rămâne identică, perechea este alb–alb sau negru–negru. La 2 MHz, cele două transmisii cer cel puțin 120 ms, la care se adaugă inițializarea, comenzile și forma de undă. [Implementarea electrică a secvenței](../firmware/src/panel.c) · [Structura scenei și a jurnalului](../firmware/src/state.h)

O tranzacție pregătită se scrie durabil înainte de lansarea comenzii 20h. Confirmarea este permisă numai după BUSY activ și revenit jos. Există praguri distincte pentru apariția BUSY, 250 ms, și pentru terminare, 25 s. O tranzacție întreruptă, un CRC deteriorat sau altă versiune a rendererului cer o resincronizare completă la următorul ciclu eligibil. Modul complet folosește 21h = 40h,00h, 3Ch = 05h, 22h = F7h și 20h. Firmware limitează secvența la cinci actualizări parțiale între două complete și la minimum 180 s între forme de undă. Acceptă parțial la 15…35 °C și complet în domeniul 0…50 °C dacă bateria permite. Criteriul software de 0…50 °C folosește BME280 de pe placă. Senzorul intern al SSD1683 selectează forma de undă. La calificarea în soare și la rece se măsoară separat temperatura spatelui sticlei și diferența față de BME280, pentru a stabili marja de exploatare a carcasei. La 24 h de la ultima completă, următorul ciclu eligibil devine complet. Încheierea secvenței trimite 10h = 01h, așteaptă 100 ms și permite întreruperea principală. Logul testelor cu întreruperi injectate și două planuri verificate · [Politica firmware](../firmware/src/state.c) · [Ghidul Waveshare](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_Manual)

La temperatura camerei, manualul specifică 0,42 s tipic pentru forma de undă parțială, 3 s tipic pentru cea completă și 18,48 mW tipic. Pagina produsului publică 0,4 s, 5 s și 26,4 mW. La 26,4 mW, calculul orientativ pentru forma de undă este 10,6 mJ parțial și 132 mJ complet. Energia reală a ciclului include boot, transfer SPI, scrieri RRAM, sistem radio și pierderi în alimentare. Manualul V2, pag. 8 · [Specificația comercială a panoului](https://www.waveshare.com/4.2inch-e-paper.htm)

Pentru revizia livrată au fost repetate auditul nativ, cele cinci cazuri electrice și verificările numerice ale fotografiilor sintetice. Fișa de reluare identifică intrările și ieșirile prin SHA-256. Rulările pe revizia finală

## Recepția optică și electrică a prototipului

Probele de mai jos sunt **neexecutate fizic**. Se păstrează înregistrările brute pentru exemplarul identificat, tensiunea sursei, temperatura, imaginea de referință și timpul de la ultima actualizare. Procedurile D01–D03 din planul comun definesc încercările la oprit/pornit și la întrerupere în tranzacție. [Planul complet al prototipului](qualification.md) · Cadre binare și procedura pe firmware pentru D01–D03

1. La 25 ±2 °C se verifică sub lupă orientarea pinului 1, banda pe padul 1 al fiecărui redresor și așezarea paralelă a flexului. Hirose recomandă șablon de 0,15 mm cu fante de 0,25 × 1,30 mm pentru contacte. La grosimea locală de 0,15 mm volumul geometric este 0,04875 mm³. O folie de 0,10 mm în aceleași fante oferă 0,03250 mm³. Pentru un procedeu cu altă grosime se înregistrează inspecția pastei, filletele celor 24 de contacte și continuitatea după montare. Landuri Hirose · Procesul de montaj
2. Se alimentează cu panoul conectat. Se urmăresc VMAIN la C304, RESET, CS, D/C, SCK, MOSI, BUSY și TP301/TP302 cu sonde de impedanță mare. Pentru D01 se măsoară separat după forma de undă completă contrastul ≥8:1 și reflectanța albă ≥30% cu etalon fotometric, iluminare la 45° și detecție perpendiculară, conform §8 Waveshare, pag. 28. Se decodează SPI la cel puțin 20 MS/s pentru magistrala de 2 MHz. Se acceptă VMAIN între 3,05 și 3,55 V în timpul refreshului, VGH pozitiv, VGL negativ și absența depășirii limitelor absolute individuale din tabelul de componente. Pentru verificarea explicită la comandă statică de ±20 V fără sarcina formei de undă, SSD1683 publică 19,5…20,5 V pentru VGH la VCI = 3,0 V și condițiile din tabelul 11-1. Se consemnează timpii, ripplul și energia reală la formele de undă ale lotului. Caracteristici Solomon Systech, pag. 43–44
3. Se afișează complet o tablă asimetrică și se fotografiază cu expunere și iluminare fixe. Se întrerupe efectiv VMAIN și se decuplează SWD. Se probează VCI/VDDIO pe C304 și VDD intern pe C305. Ambele trebuie să rămână sub 0,30 V timp de cel puțin 60 s, iar liniile de la analizor trebuie să fie în impedanță mare. Se consemnează și descărcarea VGH/VGL înaintea manipulării flexului. După minimum 180 s de la ultima formă de undă se trezește placa și se schimbă o regiune, păstrând zone etalon albe și negre. Se verifică la SPI planurile de 15 000 B, atribuirile 26h/24h și activarea FFh. Se repetă cinci cicluri la fiecare 15, 25 și 35 °C, plus un ciclu pentru confirmarea resincronizării complete. În lumină fixă și luminanță liniarizată, variația medie a zonelor nemodificate trebuie să fie ≤5% din diferența alb–negru etalon. La 25 °C se cere contrast alb/negru ≥6:1 în fotografia de după a cincea actualizare parțială, fără flash global la actualizarea parțială și tranzițiile alb→negru, negru→alb, alb→alb, negru→negru corecte. Pentru pixelii care trebuie să își schimbe culoarea se cere cel puțin 70% din intervalul optic de referință în direcția corectă.
4. Se întrerupe VMAIN înainte de 20h, în timp ce BUSY este sus și după revenirea BUSY înainte de confirmarea RRAM. La următoarea actualizare eligibilă, jurnalul incomplet determină F7h complet. Se scoate panoul la rece și apoi se repornește cu BUSY tras jos de R305. Confirmarea scenei trebuie să lipsească, iar așteptarea trebuie să expire. Acoperirea automată a acestor trasee software se păstrează separat de observația pe sticlă. Teste ale firmware-ului

Pentru evaluarea numerică D02 înregistrați și etaloanele complet alb și complet negru în aceeași poziție și expunere. Aliniați geometric cele patru fotografii la zona activă de 400 × 300 px. Salvați cele două rastere comandate pe magistrală drept PBM monocrom sau PNG binar. În RAM SSD1683 bitul 1 înseamnă alb, iar în formatul PBM P4 bitul 1 înseamnă negru. Conversia Pillow `Image.frombytes("1", (400, 300), payload).save("old.pbm")` păstrează culorile și face conversia necesară la scriere. Scriptul liniarizează sRGB, normalizează local cu cele două etaloane și exclude marginea de 1 px a fiecărei tranziții. Pentru imagini gri brute deja liniarizate folosiți `--linear`. Sunt necesare Python, Pillow și NumPy. Pauzele de la începutul și sfârșitul înregistrării video permit verificarea separată a flashului global. Analizorul pentru fotografiile prototipului · Autotestul numeric, cu imagini sintetice

```sh
python3 verification/display/score_optics.py --old-bits old.pbm --new-bits new.pbm \
  --before before.png --after after.png --white white.png --black black.png --temperature-c 25 --partial-count 5 --output D02.json
```

Pentru etaloanele integral alb și negru, executabilul normal exportă funcția `render_frame`. Într-o sesiune de fixture pe o actualizare **completă** se poate înlocui temporar rasterul SRAM după randare. Pregătiți două fișiere de exact 15 000 octeți, toți FFh pentru alb și toți 00h pentru negru. Așezați un breakpoint hardware chiar la prima instrucțiune a funcției. AAPCS folosește R1 pentru al doilea argument, adresa rasterului. La actualizarea completă aceeași memorie este scrisă în ambele planuri. Repetați pentru a doua culoare respectând timpul minim de 180 s. La final realizați obligatoriu o actualizare **completă normală**, cu rasterul produs de renderer, pentru ca pigmentul observat să corespundă scenei persistente înaintea testelor diferențiale. Secvența de fixture este documentată la nivel de ELF și nu a fost executată pe o placă fizică. Firmware și conectarea J-Link

```sh
python3 -c "from pathlib import Path; Path('white.raw').write_bytes(bytes([255])*15000); Path('black.raw').write_bytes(bytes(15000))"
```

```gdb
hbreak *render_frame
set $raster_break = $bpnum
continue
set $raster = (unsigned char *)$r1
finish
restore white.raw binary $raster
disable $raster_break
continue
```
