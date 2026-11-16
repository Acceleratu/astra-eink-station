# D01–D03. Test frames for the physical display

This protocol uses the same rendering function, the same journal, and the same SPI trace as the delivered executable. The image is asymmetric. The ASTRA METEO header and large temperature digits appear in the top-left corner, UTC and KEYS in the bottom-left corner, while the right side remains white. A mirror image or rotated photograph can thus be identified at D01. The optical measurement settings and full white/black calibration references are specified in the display documentation. [Optical Protocol](../docs/display.en.md)

For D02, only the temperature digits change. The modified geometry lies within x=44…138 and y=50…84 inclusive, with the origin at the top-left corner. Each ambient temperature has its own file `mask.txt` and four reference samples. `old.raw` and `new.raw` are data streams of 15,000 bytes each transmitted over the bus, with 1=white. The PBM files represent the same colors in the PBM convention. On the test screen, the temperature digits display values set via debugger. The physical temperature of the lens is measured independently. The reference samples for the three temperatures

| Chamber temperature | `temp_centi_c` initial | `temp_centi_c` new | White-to-black pixels | Black-to-white pixels |
|---|---:|---:|---:|---:|
| 15 °C | 1568 | 1633 | 250 | 350 |
| 25 °C | 2368 | 2433 | 425 | 500 |
| 35 °C | 3368 | 3433 | 425 | 500 |

1. Power the board under nominal test conditions. Check the thermal condition of the display and battery, VMAIN, the BME280 and the actual voltage at VBAT. Start at least 180 s after the last actual activation. Begin capturing SCK, MOSI, CS, DC, RST, BUSY and the supply rails. Connect the SWD fixture using the bring-up procedure. [Powering and connecting the fixture](README.en.md)
2. With the ELF loaded into GDB, halt at the exact entry point in `choose_refresh`. The function receives `const struct scene *` in R0 according to the ARM ABI. The code below sets the initial scene for the test chamber at 25 °C. For other temperatures, modify only the single field according to the table. Explicit return of the value 1 forces a single **complete update** for the reference. Allow the BUSY state and confirmation in RRAM to complete. In SPI traffic, both planes must match byte by byte with `old.raw`.

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

3. Release the manual hold and disconnect the probe to let VMAIN fall. Photograph the reference and record the drop of **both** display power rails according to D02. Wait for ≥180 s real time. To capture a controlled wake-up, hold nRESET at GND with a passive contact, then raise VMAIN through normal wake-up; attach the debugger after VMAIN returns and stop at reset prior to releasing nRESET. Recreate the hardware breakpoint for the new power supply. If another update occurred between the two tests, repeat the reference at step 2.
4. At entry into `choose_refresh`, set the same fields for the next scene. **Let the function decide and return normally.** Do not use `return` at this stage. The synthetic time of the first image corresponds to 12:42:59, while that of the second image corresponds to 12:42:00 of the following day. Thus, the displayed clock remains identical, with 86,341 s of logical time between images, and the 24-h policy allows for an additional differential update. This is a data injection for optical verification. The physical cadence of 15 minutes is measured separately at W01 using real time.

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

5. Confirm on analyzer that `0x26` receives `old.raw`, `0x24` receives `new.raw`, `0x22` receives `0xFF`, and `0x20` precedes the BUSY high-to-low transition. `astra_report.mode` must be 2; preserve the photographs and evaluate the four transitions using procedure D02. For D03, interrupt power within the specified window and wait at least 180 s before restoring it. After an unconfirmed journal, the allowed operation must be complete (`mode=1`, `0x22 0xF7`). In the case of interruption **before** writing the intent record, the last confirmed raster remains usable and a partial operation is permitted.
6. Upon completion of tests, set the real UTC, return to BME280 measurement, wait for the allowed interval, and physically synchronize with a full update. Regenerate the digital reference frames with `firmware/tests/make_fixtures.sh verification/firmware/fixture`. During the prototype test, the technician must record the optical results. [Criteria D01–D03](../docs/qualification.en.md)
