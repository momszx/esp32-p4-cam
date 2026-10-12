> ⚠️ Research note (2026-10-09). Where it contradicts 05-architecture.md, 05 prevails. Known outdated points: instead of a separate C6 module, the C6H8 inside the Waveshare module (F-10); P4 USB OTG HS = GPIO20/21 and the SDIO pinout (CMD18/CLK19/D0 20…) are wrong – E18: CLK=18, CMD=19, D0=14, D1=15; GPIO20/21 = ADC (F-9); a single USB-C (GPIO24/25); LiPo/battery and PTC+SY8089 (5.5 V buck) are outdated – PD + eFuse + wide-input buck (E-1, E-2, E-13); C6 programming: C6_EN (GPIO54) + IO9 pad, OTA (05 §10).

# 02 – ESP32-C6 coprocessor, P4 ↔ C6 link, programming and power supply

> **WARNING – state of the sources:** during the research the WebFetch tool was blocked by a local governance hook (wrong node path), and WebSearch returned only generic results (it did not retrieve the pin tables). Therefore the specific numbers below (GPIOs, dimensions, currents) **come from the model's trained knowledge**, and where they were not confirmed by a primary source they are marked **[UNVERIFIED]**. Before finalising the schematic it is MANDATORY to check them against the documents in the "Sources" section (especially the EV-board schematic and the C6 datasheet).

## 1. ESP32-C6 module options

| Module | Size (approx.) | Antenna | Note |
|---|---|---|---|
| ESP32-C6-MINI-1 | ~13.2 x 16.6 x 2.4 mm [UNVERIFIED] | PCB (on-board) | smallest, with antenna; keep-out under/next to the PCB antenna |
| ESP32-C6-MINI-1U | ~13.2 x 12.5 x 2.4 mm [UNVERIFIED] | u.FL | smallest, with external antenna |
| ESP32-C6-WROOM-1 | ~18 x 25.5 x 3.2 mm [UNVERIFIED] | PCB | larger, more flash options |
| ESP32-C6-WROOM-1U | ~18 x 19.2 x 3.2 mm [UNVERIFIED] | u.FL | |
| Bare chip (QFN40) | 5x5 mm | external | RF matching, crystal, flash, 4+ layers recommended; **to be avoided on 2 layers** |

**Keep-out (general Espressif rule):** for a PCB-antenna module, under and around the antenna part (approx. 15 mm from the antenna end laterally, on the antenna side of the module) there must be **no copper, no components, no vias**, and the antenna end of the module should sit at/overhang the board edge. The antenna must not be close to a metal enclosure, battery, camera flex or FPC (min. ~15 mm). [exact values: UNVERIFIED – see the "Placement" figure in the module datasheet]. The ground plane under the module (not under the antenna part) must be continuous.

**Recommendation for a compact camera:** **ESP32-C6-MINI-1** (PCB antenna, smallest footprint, no RF layout), if the keep-out can be ensured at the board edge. If a plastic/metal enclosure or stacked boards interfere with the antenna: **MINI-1U + u.FL pigtail + small FPC/chip antenna on the enclosure**. Module = the RF matching, crystal and flash are done at the factory, so it can be implemented on 2 layers as well.

## 2. P4 <-> C6 link (esp-hosted-mcu)

The ESP32-P4 has no radio; WiFi/BLE is available through the C6 using the `esp-hosted-mcu` + `esp_wifi_remote` components (the C6 runs "slave" firmware).

| Transport | Signals | Note |
|---|---|---|
| **SDIO 4-bit** (recommended, the EV board uses this too) | CLK, CMD, D0-D3 + reset (+ optional handshake/data-ready) | highest speed; the practical throughput easily serves the C6's 2.4 GHz WiFi 6 20 MHz link (~40-60 Mbit/s real) [UNVERIFIED] |
| SDIO 1-bit | CLK, CMD, D0 | fewer wires, lower speed; fewer pins on a stacked connector |
| SPI | CLK, MOSI, MISO, CS, handshake, data-ready, reset | fewer pins, but slower (according to esp-hosted typically 10-30 Mbit/s [UNVERIFIED]) |
| UART | TX, RX (+RTS/CTS), reset | slowest, only for low bandwidth; not recommended for a camera stream |

**C6 SDIO slave fixed pins** (the C6 SDIO slave peripheral is tied to the IOMUX) [UNVERIFIED, check: ESP32-C6 datasheet "SDIO" / TRM]:
- CMD = GPIO18, CLK = GPIO19, D0 = GPIO20, D1 = GPIO21, D2 = GPIO22, D3 = GPIO23.
- These do not coincide with the strapping pins (GPIO4/5/8/9/15), so there is no circuit conflict.

**Espressif EV board (ESP32-P4-Function-EV-Board) – P4 side** [UNVERIFIED, from memory of the esp-hosted documentation]: SDMMC Slot 1: CLK=GPIO18, CMD=GPIO19, D0=GPIO14, D1=GPIO15, D2=GPIO16, D3=GPIO17, the C6 reset (EN) tied to P4 GPIO54. The P4 SDMMC Slot 1 pins can also be assigned freely through the GPIO matrix, but the IOMUX pins (GPIO14-19) are the best for the highest speed/best signal integrity. Slot 0 IOMUX: GPIO39-44 (can be left for the SD card).

**Electrical requirements for SDIO:**
- External **pull-up (10 kohm, typically 10-47 kohm) on the CMD and D0-D3 lines to 3.3 V** (the C6 needs the pull-up in SDIO slave mode; the EV board does it this way too) [UNVERIFIED: exact value].
- Optional small series resistor (22-33 ohm) on CLK, at the source, against overshoot.
- VDDIO = 3.3 V on both sides (the corresponding VDDPST domain of the P4 must be 3.3 V; do not connect the SD-slot supply to the P4 internal LDO unless it is designed for that).
- Short, equal-length (±5-10 mm) traces, ground plane underneath; on 2 layers 4-bit SDIO at 20-40 MHz is feasible if the trace is < ~5-6 cm. On a stacked board, passing through the connector degrades it – initially configure **below 40 MHz**.

**Reset and boot control:** a P4 GPIO drives the C6 EN pin (push-pull or open-collector; on EN a 10 kohm pull-up + 1 uF RC on the C6 side, per the Espressif recommendation). If the P4 should also be able to push the C6 into download mode, the C6 GPIO9 must also be routed out to a P4 GPIO (or to a header pin) – see point 3.

## 3. Programming both chips

### 3.1 C6 strapping pins [UNVERIFIED – check: ESP32-C6 datasheet "Strapping Pins"]
- **GPIO9** (internal pull-up): 1 = SPI boot (normal), **0 = Download boot** (LOW when reset is released).
- **GPIO8**: must be **1** in download mode (without an internal pull-up it may float! add an external pull-up, or keep the module's default wiring). According to some documentation GPIO8 is also "don't care" in normal boot mode. **For us: the C6_IO8 10k pull-up is MANDATORY (05 E6, chapter 5).**
- **GPIO15**: selects the JTAG signal source (USB-Serial-JTAG vs. external pins via eFuse) and/or the ROM log; default value (usually no external drive needed). Do not connect it to a peripheral that drives strongly towards either ground or supply.
- GPIO4/GPIO5: SPI-boot strapping (flash supply / JTAG), avoid strong external driving during reset.
- On the ESP32-C6-MINI/WROOM module the flash-related pins are handled internally; the module datasheet lists the usable GPIOs.

### 3.2 C6 programming options on the end product
| Mode | How | Pro | Con |
|---|---|---|---|
| (a) UART pads | C6 U0TXD=GPIO16, U0RXD=GPIO17, EN, GPIO9 brought out (6 pads: 3V3/GND/TX/RX/EN/IO9) – Tag-Connect TC2030 / pogo / 1.27 mm header | independent of the P4, always works; excellent for the first factory programming | needs pad area and an external USB-UART |
| (b) P4 updates the C6 via esp-hosted OTA | `esp_hosted` slave OTA: the P4 sends an OTA image to the C6 over SDIO | no separate connector for the end user; field update | does not work without a **first** C6 firmware (the C6 is blank/factory state), and the slave firmware must already be running; with faulty C6 firmware, recovery only via (a)/(c) |
| (c) C6 USB-Serial-JTAG | GPIO12 (D-), GPIO13 (D+) to USB (native USB, no separate bridge) | fast, DTR/RTS emulation with the built-in USB-Serial-JTAG (reset + boot automatically) | needs a separate USB connector or a mux; the P4's USB is not the same port |

**Recommendation:** for the C6, **(a) or (c) pads for development + (b) OTA in the end product**. The pads must stay in the design (must not be removed), otherwise a broken slave FW means a "brick". At least TX/RX/EN/IO9/3V3/GND (6 pads).

### 3.3 Auto-reset circuit for UART
Classic 2x NPN (e.g. MMBT3904) with DTR/RTS cross-coupled: DTR->EN, RTS->IO9 (or the combination matching the esptool "classic reset" sequence). If the P4 drives the C6 EN anyway, make sure it does not fight with the bridge (series 1-4.7 kohm protection resistor or diode-OR).

## 4. Programming the P4 [UNVERIFIED: details]

- The P4 **native USB-Serial-JTAG** pins: GPIO24 (D-), GPIO25 (D+) – these are suitable for flashing and debugging (esptool via the built-in ROM bootloader), so **a separate CH340/CP2102 is not needed**.
- The P4 **USB 2.0 OTG HS** PHY is on separate fixed pins (GPIO20/21) [UNVERIFIED] – this is the application USB (UVC/MSC); do not confuse it with the Serial-JTAG. The debug port should be GPIO24/25.
- **UART0**: TX=GPIO37, RX=GPIO38 [UNVERIFIED]; ROM logs and backup programming from pads (3V3/GND/TX/RX/EN/BOOT).
- **Boot strapping**: GPIO35 (Boot, LOW = Download), GPIO36/37/38 further strapping (ROM log, UART/USB download). A separate BOOT+RESET push button (or pads) is recommended, because with USB-Serial-JTAG even auto-reset cannot always force download mode when the flash is blank/corrupt.
- The P4 has no internal flash: **an external SPI/QSPI NOR flash** is required (16 MB or more); the PSRAM (16/32 MB) is in the package. The flash/PSRAM supply rail is the P4's internal LDO – see the datasheet.
- **USB-C connector**: a separate 5.1 kohm pulldown (Rd) to GND on each of the CC1 and CC2 pins (otherwise the host does not supply 5 V over a C-C cable); D+/D- from the two rows in parallel; TVS/ESD on VBUS; shield to GND (RC or 1 Mohm + 4.7 nF). USB D+/D- is 90 ohm differential – on 2 layers use short (<~3 cm), tightly coupled traces with continuous ground underneath.
- **ESD**: USBLC6-2SC6 (or similar, e.g. TPD2EUSB30) on the D+/D- lines, close to the connector; on VBUS an SMF5.0A or similar TVS, plus a polyfuse/PTC or a switched current limit.
- **Smallest programming setup (recommended):**
  1. P4: **native USB-C** (GPIO24/25 Serial-JTAG), BOOT + RESET button.
  2. C6: **6-pad Tag-Connect TC2050/TC2030 or pogo** (TX/RX/EN/IO9/3V3/GND), only for the first factory flashing and for recovery; everyday updates from the P4 via **esp-hosted OTA**.
  3. Alternative: a separate, detachable "programmer board" (CP2102N/CH340C + auto-reset transistors) that mates with the C6/P4 pads via pogo pins; this way the product board has no bridge IC and no USB-C for the C6.

## 5. Power supply – C6

- **VDD**: 3.3 V (3.0-3.6 V range) [UNVERIFIED: exact range]. With a module the decoupling is on the module, but an external **10 uF + 0.1 uF** at the module's 3V3 pin is recommended.
- **Peak current**: WiFi TX peak around ~350 mA (narrow pulse); according to the official design recommendation the supply should provide at least **500 mA** for the module [UNVERIFIED]. Size the whole 3.3 V rail together with the P4 (see 6.).
- **Bulk capacitance**: 22 uF + 100 uF (low-ESR ceramic/tantalum) on the 3.3 V rail near the C6; the capacitor should be placed as close as possible to the module's 3V3 pin.
- **EN pin**: 10 kohm pull-up + 1 uF to GND (RC reset delay); the EN should be driven open-collector by a P4 GPIO.
- **Power-up sequence**: the C6 3.3 V must not lag significantly behind the P4 SDMMC VDDIO, otherwise the CMD/CLK lines back-feed the C6 from the P4 side (through the ESD diodes). Before SDIO, the P4 should hold the C6 EN LOW until the rail is stable.

## 6. Complete power supply – for a compact camera

**P4 power tree on the EV board** [UNVERIFIED, to be checked in the schematic]: 5 V USB -> 3.3 V buck (for several rails); the P4 internal LDOs provide the MIPI PHY (approx. 2.5 V), the flash/PSRAM (1.8 V / 3.3 V) and the core (approx. 1.1 V) voltages – with external components (inductor, capacitors) per the datasheet; the P4 core is supplied by an external DC/DC per the hardware design guideline because of the higher current. **Its exact structure MUST be taken from the "Power Supply" chapter of the ESP32-P4 Hardware Design Guidelines** – this is the biggest risk for the 2-layer board.

**Recommended inputs:**
1. **USB-C 5 V** (main): CC Rd 5.1 kohm; required current ~1-1.5 A (P4 + camera + C6 + LEDs). Ideal diode/load switch at the input (e.g. TPS2113A or diode-OR) if there is also a LiPo.
2. **Optional LiPo + charger**: compact bq24074 (power-path, 1 A) or MCP73831 (simple); the TP4056 is cheap, but has no power-path and runs hot – not recommended long-term. Protection circuit (DW01 + 8205) at the cell, if it does not have one built in.
3. **3.3 V rail**: synchronous buck, ≥ 2 A (e.g. TPS62xxx family, SY8089 2 A, TPS63xxx buck-boost if the battery range falls around 3.3 V). On 2 layers keep the switching loop very small; no break in the ground under the inductor.
4. **Camera rails** (per the camera module datasheet): typically 1.8 V + 2.8 V (AVDD, DVDD, IOVDD) – separate LDOs (e.g. 2x AP7343 / TLV733) close to the camera.
5. Cooling/EMC: ferrite bead on the 3.3 V rail between the camera analog section and the digital section; at the P4 VDD pins 100 nF on every pin + bulk on every rail.

**Summary proposal:** USB-C 5 V -> TVS+PTC -> (optional power-path + LiPo) -> 3.3 V buck (≥ 2 A) -> P4 + C6 module + flash; P4 internal LDOs with the external capacitors specified in the datasheet; camera 1.8/2.8 V with separate LDOs.

## Sources (primary documents to be confirmed; they could NOT be downloaded in this session)
- ESP32-C6 Datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf
- ESP32-C6 Hardware Design Guidelines: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/index.html
- ESP32-C6-MINI-1 datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf
- ESP32-P4 Datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-p4_datasheet_en.pdf
- ESP32-P4 Hardware Design Guidelines: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32p4/index.html
- ESP32-P4-Function-EV-Board user guide + schematic: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html
- esp-hosted-mcu: https://github.com/espressif/esp-hosted-mcu (docs/sdio.md, docs/spi_full_duplex.md, docs/ota.md)
- esp_wifi_remote: https://github.com/espressif/esp-protocols/tree/master/components/esp_wifi_remote
- Component registry (WebSearch hit, only provided example code): https://components.espressif.com/components/espressif/esp_hosted
- ESPHome esp32_hosted (WebSearch hit): https://esphome.io/components/esp32_hosted/

## Open questions / risks
1. **Every specific GPIO, dimension, current [UNVERIFIED]** – check against the datasheets above and the EV-board schematic before the schematic is drawn.
2. **P4 power tree on 2 layers:** the P4 requires several internal LDOs and an external DC/DC; the QFN/BGA breakout (P4 BGA (sic)) on 2 layers is most likely to be problematic (via-in-pad, fanout). Worth considering 4 layers or using a ready-made **P4 module** (if one exists).
3. **SDIO signal integrity through a stacked connector**: initially plan a 1-bit/low-clock fallback (pads for the 0 ohm jumpers).
4. **C6 RF/antenna**: if the C6 module goes above/below the P4 board, the antenna keep-out may be violated by the stacking.
5. **USB-C**: the P4 USB OTG HS (fixed GPIO) and the Serial-JTAG (GPIO24/25) are two separate ports – to be decided whether one or two connectors are needed (or a USB mux).
6. **C6 recovery**: OTA-only updating is unreliable if the slave FW breaks – keeping the pads is mandatory.
7. **P4 silicon revision** (v1.0 vs. v3.x): boot/strap and USB behaviour may be revision-dependent; check the errata.
8. Auto-reset circuit: the P4/C6 DTR/RTS logic is to be confirmed against the current esptool reset sequence.
