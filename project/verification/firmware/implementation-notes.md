# Jurnalul firmware

| Problemă observată | Corecție și verificare |
|---|---|
| Prima configurație RTC folosea RV-3028. Verificarea stocului JLCPCB a produs zero bucăți pentru toate variantele evaluate. | Circuitul și firmware-ul folosesc PCF85063AT/AY la 0x51. Comparatoarele H:M:S sunt programate și recitite. Testul tuturor datelor calendaristice 2000–2099 include datele bisecte și trecerea peste miezul nopții. |
| Eticheta generică DT `rtc` a intrat în conflict la compilare cu verificarea Nordic a adreselor registrelor interne. | Eticheta a devenit `external_rtc`. Verificarea Nordic și linkarea completă a imaginii au trecut. |
| Regulatorul poate opri panoul între o tranziție optică și salvarea imaginii. | S-a introdus un jurnal cu intenție și confirmare separate, scrieri cu RRAMC READY/EMPTY, CRC, confirmare după BUSY sus→jos și recuperare prin formă de undă completă. Testele injectează întreruperi la fiecare octet și coruperea fiecărui bit al celui mai recent slot. |
| O schimbare voluntară a orei sau o resetare a RTC poate scurtcircuita limita de 180 s dintre refresh-uri. | Se înregistrează un reper fără activare. Un test demonstrează amânarea la 179 s și recuperarea completă la 180 s. |
| Filtrele RC ale tastelor pot indica o apăsare la prima alimentare a domeniului continuu. | Captura are loc imediat după inițializarea GPIO. Codul suprimă tastele de pornire dacă RTC își declară timpul invalid și limitează așteptarea de eliberare la 2 s. Comportamentul fizic al tastelor rămâne de măsurat. |
| ADC-ul necesita activarea explicită a comutatorului adăugat în revizia circuitului de măsură. | P1.09 jos la pornire, sus pentru măsură, 5 ms de stabilizare, achiziție 40 µs, apoi jos cu 1 ms descărcare. Verificarea pinilor a traversat biblioteca Fusion până la padul 1 al modulului. |
| Un depanator poate menține WAKE_MDRV activ după impulsul DONE sau după expirarea alarmei. | Firmware-ul rearmează RTC înainte de oprire, repetă DONE după eliberarea fixture-ului și reînnoiește alarma în timpul unei mențineri de durată. |
| Un prim comparator ELF/HEX a tratat octeții din golurile de aliniere/TLS ca date care ar trebui programate. | Comparatorul folosește fiecare secțiune ELF alocată și inițializată cu adresa sa fizică din PT_LOAD. Verifică egalitatea exactă a mulțimii adreselor și a fiecărui octet. În prima compilare existau 12 adrese de aliniere/TLS. În revizia livrată singurul gol dintre adresele inițializate este 0x47C…0x47F. |
| Niciun dispozitiv identificabil drept J-Link/CMSIS-DAP/nRF/ST-Link nu a apărut în arborele USB local. | S-au livrat ELF, HEX, verificările pe gazdă, raportul SWD și procedeul de banc. Măsurile analogice, optice și radio rămân deschise pentru prototip. |

Log de compilare · Verificare ELF/HEX · [Testele funcționale](host-tests.txt) · Pinout

## Reverificare pe placa rutată

Compararea codului cu cerința W01 a identificat acumularea duratei active dacă fiecare alarmă se programa la 15 minute după terminarea formei de undă. Firmware-ul programează acum sferturi de oră absolute, cu secunda zero. Un test pentru toate cele 86.400 de momente ale zilei și 96 de durate active variabile verifică lipsa derivației de fază introduse de software. Setările SPI au marjă explicită pentru setup/hold și CS inactiv între tranzacții. Verificatorul traversează biblioteca din schemă și validează cele două extremități în contactref-urile fișierului BRD. Comparația cu documentația de circuit · Verificarea pe fișierele identificate prin SHA-256
