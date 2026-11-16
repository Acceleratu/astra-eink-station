# Fișă banc — o copie pentru fiecare exemplar

**Stare inițială: NEEXECUTAT.** Nu se marchează „trecut” fără date măsurate. Pragurile și ordinea completă se găsesc în [procedură](../../docs/qualification.md). Dacă rezultatul este neconform, se notează condiția, se izolează defectul și se repetă probele afectate după modificare.

| Identificare | De completat |
|---|---|
| Placă, lot, data, operator | |
| SHA-256 schemă / PCB / firmware | |
| Marcaj U201, FICR.PART/PACKAGE, mark V2 / lot FPC | |
| Pack, lot, cavități 1/2/3 măsurate, polaritate, V, Ω și °C | |
| PV, polaritate, Voc rece, Vmp/Imp STC, metodă iradianță | |
| Sursă USB/emulator PV/simulator baterie, seriile | |
| Analizor curent / șunt, bandwidth, offset, burden, calibrare | |
| Temperatura / RH / etalon / cabluri / poziție metal și sticlă | |
| Locația datelor brute, fotografiilor și oscilogramelor | |

| Probă | Valori, condiții, repetări, fișier brut | Trecut / respins / neexecutat |
|---|---|---|
| M01 — polaritate, AOI, X-ray, înălțime și încadrare mecanică | | Neexecutat |
| P01 — VAON/VMAIN și sleep cu baterie | | Neexecutat |
| P02 — USB în ambele orientări, CC/CV/precharge | | Neexecutat |
| P03 — fereastră termică, CE la NTC defect și UVLO | | Neexecutat |
| P04 — cele 8 stări și 24 tranziții de surse | | Neexecutat |
| P05 — MPPT, STC și umbrire | | Neexecutat |
| P06 — temperaturi și efect termic asupra BME | | Neexecutat |
| W01 — RTC, tastă blocată, timeout, revenire | | Neexecutat |
| W02 — 7 pogo, SWD, două programări și 100 porniri | | Neexecutat |
| D01 — boost, polaritate, raster și contrast full | | Neexecutat |
| D02 — cinci diferențiale după cădere reală, drift optic | | Neexecutat |
| D03 — brownout în patru faze, CRC și versiune renderer | | Neexecutat |
| S01 — ID / T / RH / P / tensiune BAT, interblocare | | Neexecutat |
| R01 — BLE pe canale / RSSI deschis și montat | | Neexecutat |
| E01 — înregistrare de 24 h, integrala energiei și vârfuri | | Neexecutat |

**Pentru P04:** copiază [matricea cu cele 24 de tranziții și pragurile lor](source-transitions.csv) pentru fiecare exemplar și regim de iluminare. Fiecare rând `(USB,PV,pack) înainte→după` are câmpuri pentru tensiunile minime `CHG_IN/SYS_AON/VMAIN/VAON`, curent de întoarcere, reset RTC, rezultat afișare, numele oscilogramei și concluzie. De exemplu, `111→011` dezactivează numai USB. Separă scoaterea bruscă și rampa lentă. Pentru PV înregistrează și tensiunea de fiecare parte a R126, valoarea șuntului introdus, curentul și căderea de tensiune. Pentru acceptarea finală repetă cu R126 de 0 Ω montat. Adaugă rânduri pentru scoaterea simultană USB + PV, cu și fără pack.

**Pentru E01:** atașează CSV sincronizat, rezultate json ale reducerii și datele brute cu bandă ridicată pe intervalul de boot. Salvează analiza înainte de a converti pentru grafic. Înregistrările sintetice și simulările se păstrează separat de dosarele plăcilor fizice.
