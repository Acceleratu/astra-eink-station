# Firmware pentru punerea în funcțiune

Ținta este Cortex‑M33 din nRF54L15‑QFAA al modulului E73‑2G4M08S1F. `artifacts/astra.hex` se programează prin SWD. `artifacts/astra.elf` conține simbolurile pentru debugger. Rezultatele executate sunt în `artifacts/build.log`, `artifacts/image-check.txt` și `../verification/firmware/`. Probele pe placă sunt descrise mai jos și în raportul de calificare. [Procedura stației](../docs/qualification.md)

## Ce rulează la trezire

1. Codul captează nivelul celor trei butoane imediat după inițializarea GPIO, comandă DONE și VBAT_MEAS_EN la nivel jos, apoi recitește butoanele la începutul aplicației. La o pierdere a integrității RTC ignoră indicațiile tranzitorii produse de condensatoarele tastelor. Ținerea unei taste pe durata pornirii facilitează proba de banc.
2. Firmware-ul citește PCF85063A la `0x51`, dezactivează CLKOUT, confirmă sau inițializează calendarul și programează următoarea alarmă pe grila de sfert de oră, la minutele 00, 15, 30 și 45, cu secunda 00. Prima trezire după inițializare ajunge la următorul sfert de oră. Dacă o trezire manuală sau o eliberare a fixture-ului se produce cu cel mult 2 s înaintea unui prag, citirea în curs acoperă acel prag și se programează următorul. Timpul necesar formei de undă și debugului păstrează faza grilei. Comparatoarele secunde/minute/ore sunt active, comparațiile de zi/săptămână mascate. După alimentarea pentru prima oară, ceasul pornește cu o origine locală marcată `REL`; data și ora civilă devin `UTC` după setarea prin debugger. Secundele cu flag OS și datele BCD imposibile declanșează recuperarea. Baza temporală este calificată pentru 2000–2099. [NXP PCF85063A](https://www.nxp.com/docs/en/data-sheet/PCF85063A.pdf)
3. SAADC măsoară P1.04/AIN0 după activarea P1.09 și 5 ms de stabilizare. Rezoluția este 12 biți, referința internă 900 mV, câștigul 1/3, achiziția 40 µs. Intrarea vede jumătate din tensiunea terminalului VBAT. Comanda de măsurare revine jos, urmată de minimum 1 ms până la DONE. Tensiunea terminalului poate exista și fără acumulator, când este prezent USB. BME280 la `0x76` trebuie să răspundă cu ID `0x60`; driverul Zephyr măsoară temperatura, presiunea și umiditatea în mod forțat cu supraeșantionare ×1. [Driverul SAADC](https://github.com/zephyrproject-rtos/zephyr/blob/v4.3.0/drivers/adc/adc_nrfx_saadc.c) · [Driverul BME280](https://github.com/zephyrproject-rtos/zephyr/tree/v4.3.0/drivers/sensor/bosch/bme280)
4. O măsurare validă poate actualiza panoul Waveshare 13186 B/W V2 de 400 × 300 px. Firmware-ul inhibă forma de undă în afara intervalului 0–50 °C sau dacă terminalul VBAT măsurat este în afara intervalului 3,30–4,35 V. Limita conservatoare pentru actualizare diferențială este 15–35 °C. Actualizarea completă se impune la prima imagine, după cel mult cinci actualizări parțiale, la ≥24 h de la ultima completă, la apăsarea BTN1 sau la un jurnal nesigur. Se păstrează ≥180 s între activări pentru un ceas continuu. După discontinuități ale ceasului se scrie mai întâi un nou reper fără activarea panoului. BTN2 apare în masca tastelor, iar BTN3 solicită și o probă BLE. [Manualul panoului V2](https://files.waveshare.com/upload/9/97/4.2-inch-e-Paper-V2-user-manual.pdf) · [Driverul de referință Waveshare](https://github.com/waveshareteam/e-Paper/blob/master/Arduino/epd4in2_V2/epd4in2_V2.cpp)
5. La BTN3 și cu tensiune admisă, stiva BLE transmite timp de 2 s anunțuri neconectabile cu numele `Astra weather`, apoi oprește publicitatea. Rămâne disponibilă programarea SWD. HF/LF folosesc cristalele din modul cu încărcările interne 15.000/17.000 fF din firmware-ul de evaluare Ebyte. Interfața SSD1683 scrie SPI mode 0 la 2 MHz, cu 1 µs configurat înainte de primul front și după ultimul front sub CS activ. După fiecare transfer sincron impune încă 1 µs cu CS inactiv. Driverul SPIM Nordic aplică soluția pentru erratum 8 la mode 0 și prescaler >2. Driverul CLOCK tratează erratum 39, iar controlerul BLE solicită latență constantă pe durata activității radio. Configurația modulului · [Erata nRF54L15](https://docs.nordicsemi.com/r/bundle/errata_nrf54l15_rev2/page/err/nrf54l15/rev2/latest/err_l15_new.html) · [SPIM nrfx fixat la revizia compilată](https://github.com/zephyrproject-rtos/hal_nordic/blob/7858281d843468fe53c829995fb63f45a227387a/nrfx/drivers/src/nrfx_spim.c)
6. Înainte de DONE citește și rearmează următorul sfert de oră, astfel încât o oprire lungă în debugger să nu lase în urmă o alarmă consumată. P0.00 emite un impuls pozitiv de 10 ms. Dacă domeniul rămâne alimentat, repetă impulsul la ~100 ms pentru primele zece încercări, apoi la 1 s. Pe banc, după o menținere manuală îndelungată rearmează alarma la 14 minute. O defecțiune I²C face trei încercări inițiale cu recuperarea magistralei, apoi permite oprirea pentru a proteja bateria; butoanele rămân calea de relansare a circuitului one-shot.

## Starea optică după întreruperea VMAIN

RRAM rezervată ocupă `0x15D000…0x164FFF`, 512 înregistrări circulare de câte 64 de octeți. Fiecare înregistrare include temperatura, umiditatea, presiunea, tensiunea, timpul, masca tastelor și versiunea exactă a rasterizatorului. Înainte de pornirea panoului se invalidează confirmarea din poziția reutilizată, apoi se scrie și se verifică intenția cu CRC32. După fiecare scriere codul așteaptă `READY` și `WRITEBUFEMPTY` de la RRAMC și recitește datele. Fiecare actualizare folosește patru linii RRAM de 128 biți, iar linia de confirmare suportă două scrieri pe rotație. La 96 actualizări/zi și 10.000 cicluri/locație, plafonul aritmetic pentru această linie este de aproximativ 73 de ani. Durata de serviciu reală a ansamblului se stabilește separat. [Specificațiile memoriei Nordic](https://docs.nordicsemi.com/r/bundle/ps_nrf54l15/page/chapters/abs_max_ratings/doc/abs_max_ratings.html) · [Driverul RRAM Zephyr](https://github.com/zephyrproject-rtos/zephyr/blob/v4.3.0/drivers/flash/soc_flash_nrf_rram.c)

SSD1683 pierde memoria de referință la tăierea alimentării. La următoarea actualizare parțială codul reinițializează controlerul, resetează adresa XY și scrie toți cei 15.000 de octeți ai vechiului raster cu `0x26` și toți cei 15.000 de octeți ai noului raster cu `0x24`. Forma de undă diferențială se selectează cu `0x22 0xFF`, urmat de `0x20`. La actualizare completă, ambele memorii primesc noul raster și se utilizează `0x22 0xF7`. Confirmarea în RRAM urmează detectării BUSY sus și revenirii la nivel jos. Martorul de intenție rămas în urma unui brownout impune următoarea actualizare completă permisă. Un BUSY blocat sau o eroare SPI păstrează starea neconfirmată. Schimbările implementării de randare necesită actualizarea constantei `ASTRA_RENDERER`. Controlerul SSD1683 și panoul folosit

Fișierul `../verification/firmware/reference-frame.png` este rasterul de referință generat pe calculator pentru date sintetice. Calitatea optică a tranzițiilor, efectele de temperatură și ghosting-ul sunt probe fizice deschise. [Imagine de referință](../verification/firmware/reference-frame.png)

## Reconstrucție

S-a folosit Zephyr 4.3.0, commit `3568e1b6d5cdd51a6b964a2a1d6d29200fea2056`, Zephyr SDK 0.17.4 cu `arm-zephyr-eabi-gcc 12.2.0`, Python 3.12.13, west 1.5.0, CMake 3.31.10, Ninja 1.13.2 și DTC 1.8.1. SDK-ul oficial se instalează cu toolchain-ul `arm-zephyr-eabi` corespunzător sistemului gazdă. [Zephyr SDK 0.17.4](https://github.com/zephyrproject-rtos/sdk-ng/releases/tag/v0.17.4)

Exemplu pentru o clonă nouă. `ZEPHYR_SDK_INSTALL_DIR` se setează la directorul real de instalare al SDK. Copia locală a proiectului rămâne sursa firmware-ului custom.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install west==1.5.0 cmake==3.31.10 ninja==1.13.2 intelhex==2.3.0 pyelftools==0.33
git clone --depth 1 --branch v4.3.0 https://github.com/zephyrproject-rtos/zephyr.git zephyr
west init -l zephyr
west update --narrow --fetch-opt=--depth=1 cmsis cmsis_6 hal_nordic
pip install -r zephyr/scripts/requirements-base.txt
export ZEPHYR_BASE="$PWD/zephyr"
export ZEPHYR_SDK_INSTALL_DIR="/path/to/zephyr-sdk-0.17.4"
cd "/path/to/station-project"
firmware/build.sh
firmware/tests/run.sh
python firmware/tests/verify_pinmap.py
```

`build.sh` compilează într-un director temporar, copiază ELF, HEX, configurația și DTS-ul rezolvat în `firmware/artifacts/`, verifică fiecare octet emis în HEX față de secțiunile ELF inițializate, limitele partiției și vectorul de reset. Variabila `ASTRA_OUTPUT_DIR` schimbă destinația. Scriptul de verificare a pinilor acceptă și `--board path/to/astra.brd` pentru a verifica referințele fizice la contacte din placa Fusion. Pentru testele C pe calculator se folosește un compilator cu AddressSanitizer/UndefinedBehaviorSanitizer. Manifestul modulelor folosite

## Programare și examinare prin SWD

Folosiți o sondă J-Link/Debug Out cu suport nRF54L15‑M33. J201 are padurile 1 GND, 2 VMAIN ca referință de tensiune a sondei, 3 SWCLK, 4 SWDIO, 5 nRESET, 6 WAKE_MDRV și 7 VAON. Alimentați placa prin sursele proiectate. Lăsați contactul între 6 și 7 deschis la pornire. După prima urcare observată a VMAIN, sau după 500 ms de VAON stabil, închideți acest contact uscat pentru a ține activ domeniul. Portul USB-C alimentează circuitul de încărcare. [Conectorul de test și pregătirea fixture-ului](../docs/radio.md) · [J-Link Commander](https://kb.segger.com/J-Link_Commander)

Din directorul `firmware/artifacts`, porniți J-Link Commander cu `JLinkExe -device nRF54L15_M33 -if SWD -speed 1000 -autoconnect 1`. În consola de programare executați comenzile următoare și păstrați rezultatul verificării programatorului.

```text
h
loadfile astra.hex
r
g
exit
```

Pentru raport, deschideți `astra.elf` în GDB prin J-Link GDB Server. Un breakpoint pe `astra_done_hook` precedă ciclul DONE, iar `p astra_report` arată identitatea FICR, codurile RTC/senzor/ADC/panou/radio, tensiunea, timpul și numărul secvenței RRAM. Valoarea așteptată a `part` este `0x00054B15`. `variant` și `package` se păstrează împreună cu lotul modulului. Codul 0 marchează operația executată cu succes; `-ENODATA` pentru operațiile condiționale indică faptul că bucla curentă nu le-a executat. `mode` ia valorile 0 (păstrează imaginea), 1 (complet), 2 (diferențial), 3 (reper de timp, fără activarea panoului). Raportul verificării binare

Pentru setarea UTC, opriți execuția la `astra_fixture_hook`, completați câmpurile cu ora UTC actuală, apoi scrieți cookie-ul **ultimul** și continuați. Exemplul arată formatul datelor.

```gdb
set var astra_time_mailbox.value.year = 2026
set var astra_time_mailbox.value.month = 11
set var astra_time_mailbox.value.day = 15
set var astra_time_mailbox.value.hour = 12
set var astra_time_mailbox.value.minute = 0
set var astra_time_mailbox.value.second = 0
set var astra_time_mailbox.cookie = 0x41535455
continue
```

După eliberarea contactului 6–7, verificați că primul DONE acceptat oprește VMAIN și că ora rămâne validă pe VAON. Pentru testul radio țineți BTN3 la o trezire ulterioară, porniți scanarea înainte de trezire și confirmați reclama `Astra weather`. Măsurați RF/emisii cu metodele din planul de calificare.

## Dovezi și probe de banc

| Verificare | Rezultat |
|---|---|
| Trei compilări curate ale aceleiași surse | Comparație byte-for-byte a imaginilor HEX și hash-uri în `../verification/firmware/rebuild.txt`. ELF include căi ale directorului de compilare în informațiile DWARF. |
| Întreruperi de scriere / date corupte | 81 poziții de întrerupere într-un ciclu pe slot reutilizat și toate cele 512 inversări individuale de bit în cel mai recent slot. Au trecut recuperarea, consumarea mărcii intermediare și trecerea secvenței prin zero. |
| Comenzi SSD1683 | Receptorul SPI de test a verificat conținutul ambelor plane, adresele și ordinea. 30 de erori injectate la transfer pentru fiecare mod, BUSY blocat jos/sus și blocat înaintea inițializării. |
| RTC și cablare | Conversie și întoarcere pe toate cele 36.525 de date calendaristice din 2000–2099. Verificări distincte pentru BCD invalid, toate cele 86.400 de secunde ca momente de programare și 96 de rearmări cu timpi activi variabili, inclusiv trecerea peste miezul nopții. GPIO și padurile de la ambele capete au fost comparate cu schema, placa Fusion rutată și pinoutul Ebyte. |
| Probe fizice deschise | Programare reală prin pogo, precizia ADC, BME280 într-un mediu de referință, curenții de sleep/refresh, măsurarea intervalului real al RTC, tranziții optice după power-cut, radioul și încadrarea în limitele RF. |

Pragurile și succesiunile fizice, inclusiv întreruperea în timpul BUSY, sunt în planul de acceptare. Ieșirea testelor C · Corespondența pinilor · [Calificarea primelor exemplare](../docs/qualification.md)

La D02, cele trei perechi de imagini și comenzile GDB permit o schimbare controlată doar în cifrele mari ale temperaturii. Se compară direct și cei 15.000 de octeți capturați pentru fiecare plan. Protocol D01–D03 și etaloanele digitale
