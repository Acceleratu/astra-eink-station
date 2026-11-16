# Board bring-up firmware

The E73-2G4M08S1F module contains an nRF54L15-QFAA with a Cortex-M33 core. Use SWD to flash `artifacts/astra.hex`. `artifacts/astra.elf` contains symbols for the debugger. Execution results are in `artifacts/build.log`, `artifacts/image-check.txt`, and `../verification/firmware/`. The board probes are described below and in the qualification report. [Station procedure](../docs/qualification.en.md)

## What runs on wake-up

1. The code captures the level of the three buttons immediately after GPIO initialization, issuing DONE and VBAT_MEAS_EN commands to low level, then rereads the buttons at the start of the application. In case of RTC integrity loss, it ignores transient indications produced by the key capacitors. Holding a button during power-up facilitates bench testing.
2. Firmware reads the PCF85063A at `0x51`, disables CLKOUT, confirms or initializes the calendar and programs the next alarm on the quarter-hour grid at minutes 00, 15, 30, and 45, with second 00. The first wake-up after initialization occurs at the next quarter-hour. If a manual wake-up or fixture release occurs at most 2 s before a threshold, the ongoing read covers that threshold and schedules the next one. The time required for the waveform and debugging preserves the grid phase. The second/minute/hour comparators are enabled, while day/week comparisons are masked. After first power-up, the clock starts with a local origin marked `REL`; civil date and time become `UTC` after debugger configuration. Seconds with OS flag and invalid BCD dates trigger recovery. The time base is qualified for the 2000–2099 range. [NXP PCF85063A](https://www.nxp.com/docs/en/data-sheet/PCF85063A.pdf)
3. SAADC measures P1.04/AIN0 after activation of P1.09 and 5 ms stabilization. Resolution is 12 bits, internal reference at 900 mV, gain of 1/3, acquisition time of 40 µs. The input sees half of the terminal voltage from VBAT. The measurement command returns low, followed by a minimum of 1 ms until DONE. The terminal voltage may exist even without battery, when USB is present. BME280 at `0x76` must respond with ID `0x60`; the Zephyr driver measures temperature, pressure, and humidity in forced mode with oversampling ×1. [SAADC Driver](https://github.com/zephyrproject-rtos/zephyr/blob/v4.3.0/drivers/adc/adc_nrfx_saadc.c) · [BME280 Driver](https://github.com/zephyrproject-rtos/zephyr/tree/v4.3.0/drivers/sensor/bosch/bme280)
4. A valid measurement can update the Waveshare 13186 B/W V2 400 × 300 px display panel. Firmware prevents waveform display outside the 0–50 °C range or if the VBAT terminal measured is outside the 3.30–4.35 V range. The conservative temperature range for differential refresh is 15–35 °C. A full update is required on the first image, after at most five partial updates, after ≥24 h since the last full update, upon BTN1 press, or upon an unreliable log. A minimum of ≥180 s is maintained between activations for continuous operation. After clock discontinuities, a new reference is first written without activating the panel. BTN2 appears in the button bitmask. BTN3 also requests a BLE test. [V2 Panel Manual](https://files.waveshare.com/upload/9/97/4.2-inch-e-Paper-V2-user-manual.pdf) · [Waveshare Reference Driver](https://github.com/waveshareteam/e-Paper/blob/master/Arduino/epd4in2_V2/epd4in2_V2.cpp)
5. On BTN3 and with allowed voltage, the BLE stack transmits nonconnectable advertisements for 2 s with the name `Astra weather`, then stops advertising. SWD programming remains available. HF/LF uses crystals from the module with internal loads of 15,000/17,000 fF as specified in the evaluation firmware by Ebyte. The SSD1683 interface writes SPI mode 0 at 2 MHz, with 1 µs configured before the first edge and after the last edge under active CS. After each synchronized transfer, an additional 1 µs is enforced with CS inactive. The Nordic SPIM driver implements the solution for erratum 8 in mode 0 and prescaler >2. The CLOCK driver handles erratum 39, while the BLE controller requests constant latency during radio activity. Module configuration · [Erratum nRF54L15](https://docs.nordicsemi.com/r/bundle/errata_nrf54l15_rev2/page/err/nrf54l15/rev2/latest/err_l15_new.html) · [SPIM nrfx fixed in compiled revision](https://github.com/zephyrproject-rtos/hal_nordic/blob/7858281d843468fe53c829995fb63f45a227387a/nrfx/drivers/src/nrfx_spim.c)
6. Before asserting DONE, the firmware reads the RTC and rearms the next quarter-hour alarm, even if a long debugger pause let the previous alarm expire. P0.00 generates a positive pulse of 10 ms. If the domain remains powered, repeat the pulse at ~100 ms for the first ten attempts, then at 1 s. During an extended manual hold on the bench, the firmware rearms the alarm after 14 minutes. If I²C fails, it makes three initial bus-recovery attempts, then allows shutdown to protect the battery. A button press can retrigger the one-shot circuit.

## Display state after VMAIN is switched off

The reserved RRAM region spans `0x15D000…0x164FFF`, a ring of 512 records, each consisting of 64 bytes. Each record includes temperature, humidity, pressure, voltage, time, button bitmask, and the exact version of the rasterizer. Before the panel starts, the confirmation from the reused position is invalidated, then the intent is written and verified using CRC32. After each write, the code waits for `READY` and `WRITEBUFEMPTY` signals from RRAMC and then re-reads the data. Each update uses four 128-bit RRAM lines, and the confirmation line supports two writes per rotation. At 96 updates per day and 10,000 cycles per location, the arithmetic lifetime for this line is approximately 73 years. The actual service life of the entire assembly is determined separately. [Memory specifications Nordic](https://docs.nordicsemi.com/r/bundle/ps_nrf54l15/page/chapters/abs_max_ratings/doc/abs_max_ratings.html) · [RRAM Zephyr driver](https://github.com/zephyrproject-rtos/zephyr/blob/v4.3.0/drivers/flash/soc_flash_nrf_rram.c)

SSD1683 loses its reference memory upon power supply interruption. On the next partial update, the controller is reinitialized, the XY address is reset, and all 15,000 bytes of the old raster are written with `0x26`, and all 15,000 bytes of the new raster are written with `0x24`. The differential waveform is selected with `0x22 0xFF`, followed by `0x20`. During a full update, both memories receive the new raster and use `0x22 0xF7`. Confirmation in RRAM follows detection of BUSY high and returning to low level. The brownout-induced intention marker mandates the next permitted full update. A blocked BUSY or an SPI error maintains the unconfirmed state. Render implementation changes require updating the constant `ASTRA_RENDERER`. SSD1683 controller and panel used

File `../verification/firmware/reference-frame.png` is the raster reference generated on the computer for synthetic data. The optical quality of transitions, temperature effects, and ghosting still need to be measured on a physical panel. [Reference image](../verification/firmware/reference-frame.png)

## Rebuilding the firmware

Zephyr 4.3.0, commit `3568e1b6d5cdd51a6b964a2a1d6d29200fea2056`, Zephyr SDK 0.17.4 with `arm-zephyr-eabi-gcc 12.2.0`, Python 3.12.13, west 1.5.0, CMake 3.31.10, Ninja 1.13.2 and DTC 1.8.1. The official SDK is installed with the corresponding host system toolchain `arm-zephyr-eabi`. [Zephyr SDK 0.17.4](https://github.com/zephyrproject-rtos/sdk-ng/releases/tag/v0.17.4)

Example for a new clone. `ZEPHYR_SDK_INSTALL_DIR` is set to the actual installed SDK directory. The local project copy remains the source of the custom firmware.

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

`build.sh` compiles into a temporary directory, copies the ELF, HEX, configuration, and resolved DTS into `firmware/artifacts/`, verifies each emitted byte in HEX against the initial ELF sections, partition boundaries, and reset vector. The variable `ASTRA_OUTPUT_DIR` changes the destination. The pin verification script accepts `--board path/to/astra.brd` to verify physical references to contacts on the Fusion board. For C tests on the host machine, a compiler with AddressSanitizer/UndefinedBehaviorSanitizer is used. The module manifest used

## Programming and inspection over SWD

Use a J-Link/Debug Out probe with nRF54L15‑M33 support. J201 has pads: 1 GND, 2 VMAIN as the probe's voltage reference, 3 SWCLK, 4 SWDIO, 5 nRESET, 6 WAKE_MDRV, and 7 VAON. Power the board through the designed power sources. Leave the contact between pins 6 and 7 open at startup. After the first rise of VMAIN, or after 500 ms of stable VAON, close this dry contact to keep the domain active. The USB-C port powers the charging circuit. [Test connector and fixture preparation](../docs/radio.en.md) · [J-Link Commander](https://kb.segger.com/J-Link_Commander)

From the `firmware/artifacts` directory, start J-Link Commander with `JLinkExe -device nRF54L15_M33 -if SWD -speed 1000 -autoconnect 1`. In the programming console, execute the following commands and retain the result of the programmer verification.

```text
h
loadfile astra.hex
r
g
exit
```

For reporting, open `astra.elf` in GDB via J-Link GDB Server. Set a breakpoint on `astra_done_hook` prior to the DONE cycle, and `p astra_report` displays the FICR identity, RTC/sensor/ADC/panel/radio codes, voltage, time, and RRAM sequence number. The expected value of `part` is `0x00054B15`. The `variant` and `package` values are retained together with the module lot. Code 0 indicates a successful operation; `-ENODATA` for conditional operations indicates that the current loop did not execute them. `mode` takes values 0 (preserve image), 1 (full), 2 (differential), 3 (time reference, without panel activation). The binary verification report

For UTC setup, halt execution at `astra_fixture_hook`, fill in the fields with the current UTC time, then write the cookie **last** and continue. The example shows the data format.

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

After the release of contacts 6–7, verify that the first accepted DONE stops VMAIN and that the time remains valid on VAON. For the radio test, hold BTN3 until a subsequent wake-up, start scanning prior to the wake-up, and confirm the advertisement `Astra weather`. Measure RF/emissions using the methods specified in the qualification plan.

## Verification records and bench tests

| Check | Result |
|---|---|
| Three clean builds from the same source | Byte-for-byte comparison of HEX image files and hashes in `../verification/firmware/rebuild.txt`. ELF contains directory compilation paths within DWARF information. |
| Write faults / corrupted data | The test covered 81 power-cut positions in a write cycle to a reused slot and all 512 individual bit flips in the latest slot. Recovery, consumption of the intermediate marker and sequence-number wraparound through zero all passed. |
| SSD1683 Commands | The SPI test receiver verified the content of both planes, addresses, and order. 30 injected errors at transfer for each mode, BUSY held low/high and held prior to initialization. |
| RTC and cabling | Round-trip date conversion for all 36,525 calendar dates from 2000 to 2099. Separate validations for BCD invalid cases, all 86,400 seconds as programming moments, and 96 rearmings with variable active times, including crossing over the midnight boundary. GPIO and terminal pads at both ends were cross-checked against the schematic, routed Fusion PCB, and Ebyte pinout. |
| Physical tests still to run | Physical tests outstanding: programming through the pogo pins, ADC accuracy, BME280 readings in a reference environment, sleep and refresh currents, the actual RTC interval, optical transitions after power loss, radio operation and RF compliance. |

The acceptance plan sets the physical thresholds and test sequences, including power cuts during BUSY. C test output · Pin mapping · [First-article qualification](../docs/qualification.en.md)

In D02, the three pairs of images and the GDB commands allow a controlled change to just the large temperature digits. Compare all 15,000 captured bytes for each image plane as well. D01–D03 protocol and digital reference images
