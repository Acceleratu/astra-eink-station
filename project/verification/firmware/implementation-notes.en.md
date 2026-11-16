# Firmware implementation log

| Observed problem | Correction and verification |
|---|---|
| The first RTC configuration used RV-3028. The JLCPCB stock check found no units of any variant considered. | The circuit and firmware use the PCF85063AT/AY at 0x51. The H:M:S comparators are programmed and read. The test for every calendar date from 2000 to 2099 includes leap year dates and the transition across midnight. |
| The generic DT `rtc` label has encountered a conflict during compilation with the Nordic check of internal register addresses. | The label has become `external_rtc`. The Nordic verification and full image linking have passed. |
| The regulator can stop the panel between an optical transition and image saving. | A dedicated journal with separate intent and confirmation has been introduced, with writes using RRAMC READY/EMPTY, CRC, confirmation from BUSY high to low, and recovery via full waveform. The host tests interrupt writes at each byte and corrupt each bit of the most recent slot. |
| Setting the clock manually or resetting the RTC could bypass the 180 s limit between refreshes. | A reference is registered without activation. A test shows delay at 179 s and complete recovery at 180 s. |
| The button RC filters can register a press when the always-on domain first receives power. | The capture occurs immediately after GPIO initialization. The code suppresses start key presses if the RTC declares the time invalid and limits the release wait time to 2 s. The physical behavior of the keys remains to be measured. |
| The ADC requires explicit activation of the switch added in the revision of the measurement circuit. | P1.09 starts low, goes high for the measurement, allows 5 ms to settle and a 40 µs acquisition, then goes low with 1 ms for discharge. The pin check traced the connection through the Fusion library to module pad 1. |
| A debugger can hold WAKE_MDRV active after the DONE pulse or after the alarm expires. | The firmware rearms the RTC before shutdown, repeats DONE when the fixture is released and renews the alarm during an extended hold. |
| A first ELF/HEX comparator processed the bytes from the alignment/gaps/TLS as data that should be programmed. | The comparator uses each allocated and initialized ELF section with its physical address from PT_LOAD. It verifies the exact equality of the set of addresses and each byte. In the first compilation, there were 12 alignment/TLS addresses. In the delivered revision, the only gap among the initialized addresses is 0x47C…0x47F. |
| The local USB device list showed no J-Link, CMSIS-DAP, nRF or ST-Link debug hardware. | ELF, HEX, host checks, SWD report, and bench procedure have been delivered. Analog, optical and radio measurements still require a prototype. |

Build log · ELF/HEX verification · [Functional tests](host-tests.txt) · Pinout

## Rechecking the routed board

Comparison of the code against requirement W01 identified accumulation of active duration if each alarm is programmed 15 minutes after the end of the waveform. Firmware programs absolute quarter-hour marks with zero-second alignment. A test for all 86,400 moments throughout the day and 96 variable active durations verifies the absence of phase drift introduced by software. SPI settings have explicit margins for setup/hold and CS inactive periods between transactions. The verifier traverses the library from the schematic and validates both ends against the file's contactref entries in the BRD file. Comparison with circuit documentation · Verification on files identified via SHA-256
