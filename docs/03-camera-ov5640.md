> ⚠️ Research note (2026-10-09). Where it contradicts 05-architecture.md, 05 prevails. Known outdated points: the remark that OV5640 MIPI support is "not confirmed" is superseded: E11 confirms it (F-11); instead of the 2592×1944 resolution, a 1080p30 cap applies (ISP max 1920×1080, F-28); the camera module must have an onboard oscillator + LDOs + 3V3 input (F-27, E-17); MIPI lane rate ≤800 Mbps/lane; "from memory" claims made because of the WebFetch block are unverified; the "max. 2 layers" task constraint no longer applies – MAIN v0.6 is 4-layer (00 K4; CSI 100 Ω: 0.204/0.203 mm, 05 §3.2), the 2-layer considerations of section 5 are outdated for MAIN; the camera connector on the PCB is for now a placeholder footprint (TE 1-84953-5, 05 §6, Q6).

# 03 – Camera: OV5640 and alternatives for the ESP32-P4

> **Reliability note (important).** During the research, direct page download (WebFetch and quarantine-reader) **was blocked** (hook error, and the domain not being on the allowlist, respectively). Only WebSearch summaries were available. What I confirmed from these is marked **[VERIFIED – source]**; what comes only from prior knowledge is marked **[UNVERIFIED]**. Before manufacturing, the datasheets and the EV-board schematic must be checked manually.

## 1. OV5640 interfaces and ESP32-P4 support

### 1.1 OV5640 side
- 5 MP sensor; it has both DVP 8/10-bit parallel and MIPI CSI-2 (1 or 2 lane) output. [UNVERIFIED – general knowledge, the datasheet was not readable]
- SCCB (I2C-like) address: 0x78 (write) / 0x79 (read), i.e. 7-bit **0x3C**. [UNVERIFIED]

### 1.2 ESP32-P4 side
- The Espressif ESP-IDF camera documentation lists three hardware paths: **MIPI-CSI**, **DVP via the ISP module** and **DVP via the LCD_CAM module**. So the P4 also has DVP. [VERIFIED – ESP-IDF Camera Controller Driver page (search summary)]
- MIPI-CSI: the example code works with 2 data lanes; when the ISP is used, the camera system's max. output is 1920x1080; MIPI-CSI max. 1.5 Gbps/lane. [VERIFIED – esp_cam_sensor readme]
- A documented example: 2592x1944 (OV5645) can be received within the P4's bandwidth. [VERIFIED – esp_cam_sensor readme]

### 1.3 Which is better for the P4: DVP or MIPI?
| Aspect | MIPI CSI-2 (2 lane) | DVP (8 bit) |
|---|---|---|
| Signal count | 5 diff. pairs/pins (sic) (CLK, D0, D1) + I2C | ~8 data + PCLK + VSYNC + HREF + XCLK + I2C = 14+ GPIO |
| ISP (Bayer→RGB/YUV, AE/AWB) | Through the hardware ISP | Possible via the ISP-DVP path, but the OV5640 DVP typically already outputs YUV/RGB (the sensor's own ISP does the work) |
| Bandwidth | High, high resolution/fps | PCLK-limited; weak for 5 MP |
| 2-layer PCB | The diff. pair is critical (see 5.) | Easier with no impedance concerns, but many wires, hard on the compact stacked board |
| Software support | esp-video + esp_cam_sensor (primary path) | LCD_CAM/ISP-DVP, fewer examples for the P4 |

**Summary:** the P4's "native" and best-supported path is MIPI-CSI + ISP. DVP is a fallback/simplifying solution, but it occupies many GPIOs.

### 1.4 OV5640 support over MIPI
- In the esp_cam_sensor README, the OV5640 is mentioned only in connection with the ESP32-S3 (JPEG output, 2 MP); **I found no confirmation for P4 MIPI**. [VERIFIED that it is not mentioned in the excerpts received; the full table was NOT readable]
- The component definitely includes the **SC2336** (1920x1080, MIPI and DVP, 8/10-bit RAW). [VERIFIED – readme excerpt]
- Official P4 support for **OV5647, OV02C10, SC202CS** etc.: to my knowledge they exist in the component, but this is **[UNVERIFIED]** (the search did not return the table). The version/list changes – check the current one on the docs.espressif.com/projects/esp-video-components page.
- **Conclusion:** OV5640 over MIPI has weak/unverified support on the P4 → a custom register table and ISP tuning may be needed. If MIPI is needed, the SC2336 or OV5647 is a safer choice.

## 2. Module connectors and pinouts

### 2.1 Espressif ESP32-P4-Function-EV-Board
- Camera connector: **1.0K-GT-15PB, 15-pin, 1.0 mm pitch**, for an external camera module; adapter board + forward-direction ribbon cable. [VERIFIED – EV-board user guide (search summary)]
- Pinout (signal/GPIO): **was not readable** → must be read from the schematic. [UNVERIFIED] Probably similar to the Raspberry Pi 15-pin pinout, but **do not assume it**.

### 2.2 Raspberry Pi 15-pin CSI (1.0 mm) – common MIPI module form factor
| Pin | Signal |
|---|---|
| 1 | GND |
| 2 / 3 | CAM_D0_N / CAM_D0_P |
| 4 | GND |
| 5 / 6 | CAM_D1_N / CAM_D1_P |
| 7 | GND |
| 8 / 9 | CAM_CK_N / CAM_CK_P |
| 10 | GND |
| 11 / 12 | CAM_IO0 / CAM_IO1 (LED/PWDN-like GPIO) |
| 13 / 14 | CAM_SCL / CAM_SDA |
| 15 | CAM_3V3 |

Pins 1–12 [VERIFIED – Arducam pinout], pins 13–15 [UNVERIFIED – from prior knowledge]. According to Arducam, the pinout is the same regardless of variant. Connector (camera side): Amphenol SFW15R-2STE1LF (1 mm, right-angle) [VERIFIED – Arducam]; host side: e.g. TE 1-1734248-5 (reportedly used on RPi boards) [VERIFIED – Arducam].

### 2.3 Raspberry Pi Zero/CM/5 22-pin (0.5 mm)
To my knowledge: 1 GND, 2/3 D0 N/P, 4 GND, 5/6 D1 N/P, 7 GND, 8/9 CLK N/P, 10 GND, 11/12 D2 N/P, 13 GND, 14/15 D3 N/P, 16 GND, 17 CAM_GPIO, 18 CAM_CLK, 19 GND, 20 SCL, 21 SDA, 22 3V3. **[UNVERIFIED]** – a 4-lane form factor; the P4 has only 2 lanes, so the D2/D3 pins stay unused.

### 2.4 24-pin, 0.5 mm DVP FPC (ESP32-CAM-style OV5640 modules)
- The pinout **differs by manufacturer**, so I do not give a general table; the specific module's datasheet is needed. The beginning of the DVP list seen on the Element14 forum: VCC 3.3V, GND, SCL, SDA, VSYNC, HREF, PCLK… [VERIFIED, partial]
- Typical signal set: AVDD/DOVDD/DVDD (or 3V3), GND, SCL, SDA, VSYNC, HREF, PCLK, XCLK, D2–D9, PWDN, RESET, (AF_VDD on AF modules). [UNVERIFIED]
- E.g. the Kurokesu 687.5640A MIPI 24-pin 0.5 mm module uses a Würth 68712414522 connector (pin 22: power-down). [VERIFIED – Kurokesu wiki] – this is a MIPI pinout, not DVP.

### 2.5 Connector recommendation
- **15-pin, 1.0 mm:** Hirose FH12-15S-1SH(55) or an LCSC alternative with the same pitch. The contact side (top/bottom) and the LCSC part number are **[UNVERIFIED]** – they must be chosen based on the manufacturer's datasheet and the cable/module orientation (the "forward/reverse" ribbon cable question is a classic mistake).
- **0.5 mm, 22/24-pin:** Würth 68712414522 (24 p.) mentioned above; 22-p. version Hirose FH12-22S-0.5SH [UNVERIFIED].
- Always check: contacts top/bottom, locking actuator, FPC thickness (0.3 mm).

## 3. Power and control

| Rail | Value | Note |
|---|---|---|
| AVDD | 2.6–3.0 V (typ. 2.8 V) | analog, noise-sensitive, separate LDO |
| DOVDD | 1.8 V or 2.8 V | I/O level |
| DVDD | 1.5 V | also works with the internal regulator (external capacitor) |

Values [UNVERIFIED – general knowledge, the datasheet was not readable]. Estimated consumption: AVDD ~20–30 mA, DVDD/DOVDD ~50–100 mA, total ~100–150 mA in active mode [UNVERIFIED].

- **Modules:** most ready-made OV5640 modules (RPi-style or 24-pin) contain their own LDOs fed from a single 3.3 V input (CAM_3V3 on the RPi connector), but this is module-dependent. If we solder our own sensor, 2.8 V + 1.8 V (+ 1.5 V) LDOs are needed.
- **Power-up sequence** (per datasheet 2.7, as quoted in Linux driver patches): DOVDD stable → ≥5 ms → PWDN low → ≥1 ms → RESETB high → ≥20 ms → first SCCB access. [VERIFIED – linuxtv patch]. A hardware reset at power-up is recommended/required. [VERIFIED]
- **RESETB** is internally pulled up to DOVDD; do not drive 2.8 V onto RESETB when DOVDD is 1.8 V. SCL/SDA tolerate a higher pull-up voltage. [VERIFIED – Allwinner app note]
- Some modules do not bring out PWDN/RESETB. [VERIFIED]
- **XCLK:** 6–27 MHz, typically 24 MHz [UNVERIFIED]. The P4's LEDC can be used in low-speed mode, and the timers share a common clock; whether 24 MHz can be generated, and its jitter, are **not confirmed** (the documentation does not mention XCLK). [VERIFIED for the LEDC limitations, the rest NOT] Safer: a standalone 24 MHz oscillator on the board, or a module that has its own oscillator (many RPi cameras do).
- **SCCB pull-up:** 2.2–4.7 kΩ to a level matching DOVDD; attention must be paid to level matching between the P4 GPIO level and the sensor I/O level (3.3 V ↔ 1.8 V). [UNVERIFIED]
- The P4 MIPI D-PHY requires a separate supply (from an internal LDO channel). [UNVERIFIED – to be checked against the P4 hardware reference]

## 4. Autofocus (AF) variant
- AF OV5640 modules contain a VCM; the OV5640 supports AF operated through an embedded controller and a firmware download (over SCCB). [UNVERIFIED]
- Additional questions: VCM supply (typ. 2.8 V), a separate AF_VDD pin on 24-pin modules, downloading the firmware (~4 KB) at boot, extra software work in esp_cam_sensor (ready-made support may not exist). Simpler with a fixed-focus variant.

## 5. Layout on a 2-layer PCB
- **Feasible, but risky.** MIPI D-PHY uses 100 Ω diff. pairs; on 2 layers the reference plane is on the other side, so on a 1.6 mm board a 100 Ω diff. impedance becomes a matter of a narrow pair + wide spacing (a short section, under a few cm, can be tolerated). [UNVERIFIED – general good practice]
- Tips: place the FPC connector directly next to the P4; route the diff. pair along the shortest path, with a solid GND plane beneath it, without vias; intra-pair length match ±0.1–0.2 mm (the two members of a pair), looser between lanes; do not cross a gap in the GND plane; supply decoupling at the PHY pins. Above 1.5 Gbps/lane it is loss-sensitive; choosing a mode with a lower lane rate (e.g. 720p30) reduces the risk.
- If the manufacturer (e.g. JLC) provides an impedance calculator for 2 layers, use it; a 4-layer board is strongly recommended if possible. The task allows max. 2 layers → DVP as a fallback.

## 6. Recommendation for the project
1. **Primary:** MIPI-CSI 2 lane, **RPi-compatible 15-pin 1.0 mm FPC** connector directly next to the P4 (EV-board compatible), with an **SC2336 or OV5647** module (Espressif support in the component is better/more confirmed; the SC2336 is [VERIFIED]).
2. **OV5640 over MIPI:** only if 5 MP / AF is needed; support is unverified → risk, custom driver work may be needed.
3. **OV5640 DVP (LCD_CAM):** a safe fallback, but ~14 GPIOs + longer wires on the compact stacked board; 24-pin 0.5 mm FPC.
4. XCLK is best taken from a separate 24 MHz oscillator or from the module; from LEDC only after testing.
5. Plan jumper/0 Ω options on the board for the supply rails and for PWDN/RESET.

Trade-off: MIPI = fewer signals, better support, but a sensitive layout on 2 layers; DVP = simple impedance, but many GPIOs and lower bandwidth.

## Sources
- https://components.espressif.com/components/espressif/esp_cam_sensor (and /versions/2.6.0/readme) – search summary
- https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32p4/api-reference/peripherals/camera_driver.html
- https://docs.espressif.com/projects/esp-idf/en/v5.3/esp32p4/api-reference/peripherals/ledc.html
- https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html
- https://docs.espressif.com/projects/esp-faq/en/latest/application-solution/camera-application.html
- https://docs.arducam.com/Raspberry-Pi-Camera/raspberry-pi-camera-pinout/
- https://wiki.kurokesu.com/books/6875640-camera-module/export/html
- https://patchwork.linuxtv.org/project/linux-media/patch/20221219143056.4070-2-j-luthra@ti.com/mbox
- https://wiki.linux-sunxi.org/A31s/HDK/A31s_HDK-20140222/device_data/camera/OV5640_Camera_Module_Hardware_Application_Notes_R1.0_Allwinnertech.pdf
- https://www.mouser.lt/datasheet/3/902/1/LI_OV5640_MIPI_AF_SPEC.pdf (not readable)
- OV5640 datasheet (cdn.sparkfun.com/datasheets/Sensors/LightImaging/OV5640_datasheet.pdf) – could not be opened

## Open questions / risks
- Official MIPI support of the OV5640 on the P4 (esp_cam_sensor list) – to be checked.
- Exact pinout and GPIOs (I2C, XCLK, RESET) of the EV-board camera connector – from the schematic.
- Pins 13–15 of the 15-pin RPi connector and the 22-pin pinout to be checked against official RPi documentation.
- 24 MHz XCLK from LEDC: jitter, feasibility.
- Supply voltages, currents, DVDD internal regulator – from the OV5640 datasheet.
- Level matching P4 GPIO (3.3 V) ↔ sensor I/O (1.8/2.8 V).
- 2-layer MIPI impedance and the manufacturer's stackup.
- AF firmware and VCM support in software.
- Connector contact side and LCSC part numbers.
