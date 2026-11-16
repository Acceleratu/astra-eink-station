# D01–D03. Cadre de probă pentru panoul fizic

Acest protocol folosește aceeași funcție de randare, același jurnal și același traseu SPI ca executabilul livrat. Imaginea este asimetrică. Antetul ASTRA METEO și temperatura mare se află în stânga sus, UTC și KEYS în stânga jos, iar partea dreaptă rămâne albă. O fotografiere în oglindă sau rotită poate astfel fi recunoscută la D01. Reglajele pentru măsurarea optică și etaloanele complet alb/negru sunt în documentația afișajului. [Protocolul de optică](../docs/display.md)

Pentru D02, doar cifrele temperaturii se modifică. Geometria modificată se află între x=44…138 și y=50…84 inclusiv, cu originea în colțul stânga sus. Fiecare temperatură de cameră are propriul fișier `mask.txt` și patru etaloane. `old.raw` și `new.raw` sunt fluxurile de câte 15.000 de octeți pe magistrală, cu 1=alb. Fișierele PBM exprimă aceleași culori în convenția PBM. Pe ecranul de probă cifrele temperaturii reprezintă valori impuse prin debugger. Temperatura fizică a sticlei se măsoară independent. Etaloanele celor trei temperaturi

| Cameră | `temp_centi_c` inițial | `temp_centi_c` nou | Pixeli alb→negru | Pixeli negru→alb |
|---|---:|---:|---:|---:|
| 15 °C | 1568 | 1633 | 250 | 350 |
| 25 °C | 2368 | 2433 | 425 | 500 |
| 35 °C | 3368 | 3433 | 425 | 500 |

1. Alimentați placa în condițiile nominale ale testului. Verificați termic panoul, bateria, VMAIN, BME280 și tensiunea reală la terminalul VBAT. Începeți la cel puțin 180 s de la ultima activare reală. Porniți captura SCK, MOSI, CS, DC, RST, BUSY și alimentări. Conectați fixture-ul SWD conform procedurii de aducere în funcțiune. [Alimentarea și conectarea fixture-ului](README.md)
2. Cu ELF-ul livrat încărcat în GDB, opriți la intrarea exactă în `choose_refresh`. Funcția primește `const struct scene *` în R0 conform ABI ARM. Codul de mai jos impune scena inițială pentru camera de 25 °C. Pentru celelalte temperaturi modificați unicul câmp conform tabelului. Returnarea explicită a valorii 1 forțează o singură **actualizare completă** pentru etalon. Lăsați să se finalizeze BUSY și confirmarea în RRAM. În traficul SPI, ambele plane trebuie să coincidă octet cu octet cu `old.raw`.

```gdb
hbreak *choose_refresh
continue
set $s = (struct scene *)$r0
set $s->seconds = 45779
set $s->pressure_pa = 101325
set $s->temp_centi_c = 2368
set $s->humidity_centi_pct = 5000
set $s->battery_mv = 3900
set $s->flags = 1
set $s->buttons = 0
return (enum refresh)1
continue
```

3. Eliberați menținerea manuală și deconectați sonda pentru coborârea reală a VMAIN. Fotografiați etalonul și înregistrați scăderea **ambelor** alimentări ale panoului conform D02. Așteptați ≥180 s reali. Pentru captura controlată la următoarea trezire se poate ține nRESET la GND cu un contact pasiv, apoi se ridică VMAIN prin trezire normală, se atașează debuggerul după revenirea VMAIN și se oprește la reset înainte de eliberarea nRESET. Recreați breakpoint-ul hardware pentru noua alimentare. Dacă s-a produs o altă actualizare între cele două probe, repetați etalonul de la pasul 2.
4. La intrarea în `choose_refresh` setați aceleași câmpuri pentru scena următoare. **Lăsați funcția să decidă și să se întoarcă normal.** Nu folosiți `return` la această etapă. Timpul sintetic al primei imagini corespunde orei 12:42:59, iar al celei de a doua orei 12:42:00 din ziua următoare. Astfel ceasul afișat rămâne identic, există 86.341 s de timp logic între imagini, iar politica de 24 h permite încă o actualizare diferențială. Aceasta este o injecție de date pentru verificarea optică. Cadența fizică de 15 min se măsoară separat la W01 cu ceasul real.

```gdb
hbreak *choose_refresh
continue
set $s = (struct scene *)$r0
set $s->seconds = 132120
set $s->pressure_pa = 101325
set $s->temp_centi_c = 2433
set $s->humidity_centi_pct = 5000
set $s->battery_mv = 3900
set $s->flags = 1
set $s->buttons = 0
continue
```

5. Confirmați pe analizor că `0x26` primește `old.raw`, `0x24` primește `new.raw`, `0x22` primește `0xFF` și `0x20` precedă BUSY sus→jos. `astra_report.mode` trebuie să fie 2; păstrați fotografiile și evaluați cele patru tranziții cu procedura D02. Pentru D03, întrerupeți în fereastra stabilită și păstrați cel puțin 180 s înainte de reaplicare. După un jurnal neconfirmat, operația permisă trebuie să fie completă (`mode=1`, `0x22 0xF7`). În cazul întreruperii **înainte** de scrierea intenției, ultimul raster confirmat rămâne utilizabil și o operație parțială este permisă.
6. La terminarea probelor, setați UTC real, reveniți la măsurarea BME280, așteptați intervalul permis și sincronizați fizic cu o actualizare completă. Etaloanele digitale se regenerează cu `firmware/tests/make_fixtures.sh verification/firmware/fixture`. Dovezile optice fizice se înregistrează de tehnician pe prototip. [Criteriile D01–D03](../docs/qualification.md)
