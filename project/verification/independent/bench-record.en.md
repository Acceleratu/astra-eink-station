# Bench record: one copy per prototype

**Initial status: not run.** Mark a test as passed only after recording its measurements. Follow the thresholds and sequence in the [test procedure](../../docs/qualification.en.md). If a result falls outside its limits, record the conditions, isolate the fault and repeat the affected tests after the fix.

| Identification | To be completed |
|---|---|
| Board, batch, date, operator | |
| Schematic / PCB / firmware SHA-256 | |
| U201 marking, FICR.PART/PACKAGE, display V2 marking / FPC lot | |
| Pack, lot, 1/2/3 cavities measured, polarity, V, Ω, and °C | |
| PV, polarity, cold Voc, Vmp/Imp at STC and irradiance measurement method | |
| USB supply / PV emulator / battery simulator and their serial numbers | |
| Current analyzer / shunt, bandwidth, offset, burden voltage and calibration | |
| Temperature / RH / reference / cables / metal and glass position | |
| Location of raw data, photographs, and oscilloscope traces | |

| Test | Values, conditions, repetitions, raw file | Pass / fail / not run |
|---|---|---|
| M01 — polarity, AOI, X-ray, height and mechanical fit | | Not run |
| P01 — VAON/VMAIN and sleep with battery | | Not run |
| P02 — USB in both orientations, CC/CV/precharge | | Not run |
| P03 — thermal window, CE for NTC fault and UVLO | | Not run |
| P04 — the 8 states and 24 source transitions | | Not run |
| P05 — MPPT, STC and shading | | Not run |
| P06 — temperatures and thermal effects on BME | | Not run |
| W01 — RTC, stuck key, timeout and recovery | | Not run |
| W02 — 7 pogo contacts, SWD, two programming passes and 100 power-on cycles | | Not run |
| D01 — boost converter, polarity, raster and full-refresh contrast | | Not run |
| D02 — five differential refreshes after a real power cut; optical drift | | Not run |
| D03 — brownout in four phases, CRC and renderer version | | Not run |
| S01 — ID / T / RH / P / BAT voltage, interlock | | Not run |
| R01 — BLE by channel / RSSI in free space and in the enclosure | | Not run |
| E01 — 24 h recording, integrated energy and peaks | | Not run |

**For P04:** copy [the matrix of the 24 transitions and their thresholds](source-transitions.csv) for each unit and lighting condition. Each row `(USB, PV, pack) before→after` includes fields for minimum voltages `CHG_IN/SYS_AON/VMAIN/VAON`, return current, RTC reset, display result, oscilloscope trace name, and conclusion. For example, `111→011` disables only USB. Separate sudden removal from gradual ramp. For PV, record the voltage on both sides of R126, the shunt value introduced, current, and voltage drop. For final acceptance, repeat the test with R126 set to 0 Ω. Add rows for simultaneous removal of USB + PV, with and without pack.

**For E01:** Attach synchronized CSV file, JSON reduction results and raw data with high-bandwidth signals during boot interval. Save the analysis prior to conversion for plotting. Synthetic recordings and simulations are stored separately from physical board case files.
