> ⚠️ Research note (2026-10-09). Where it contradicts 05-architecture.md, 05 prevails. Known outdated points: PDM MEMS instead of I2S microphone (E-16, F-7); 470 µF VBUS capacitance removed – ≤10 µF at the connector + eFuse soft start (E-2); VDDPST_5 from VO4 → 3.3 V set from firmware instead of external 3.3 V, with switched SD_3V3 pull-ups (E-3, E-4); SD slot0 pins "from memory" – confirmed by E17; SY8089/PTC/SMBJ5.0A outdated (E-1, E-13, P-26); camera AE instead of LDR/light sensor (E-21); discrete LED instead of WS2812 (E-34); reset RC open (E-22); PD sink 9 V instead of USB-C 5 V only (K7); I2S/USB statements outdated (E-36); the "2-layer board" constraints are outdated for the MAIN (MAIN v0.6: 4 layers, 45×45, 00 K4); the actual assignment of buttons/LED/SD control is per 05 §5 / §3.1a (e.g. SD_EN = GPIO 53, USER = GPIO 33, status LED = GPIO 6).

# 04 – Peripherals: microSD, microphone, IR night vision, buttons/LED, power supply

Status: research draft. Markings: **[VERIFIED]** = based on a primary web source (from the search results); **[UNVERIFIED]** = from memory / typical value, to be checked before the schematic.

WebSearch worked (ESP-IDF docs hits), but WebFetch was blocked by a local hook error (hook interpreter not found), so the EV board schematic, the manufacturer datasheets and the LCSC stock could NOT be opened. Because of this every part number and current value is [UNVERIFIED], except where marked.

---

## 1. microSD

### 1.1 SDMMC host slots
- The P4 has 2 SDMMC slots. According to the ESP-IDF v5.4/5.5 documentation, slot 1 is for non-UHS-I use, slot 0 is reserved for UHS-I (the driver does not support UHS-I yet) **[VERIFIED – search excerpt]**.
- Divergent sources: according to the search hits, the newer documentation mentions the GPIO matrix for both slots, while an older documentation version states a fixed IO_MUX assignment. According to community/Arduino PR sources, on the EV board **slot 0 is the SD card, slot 1 is the C6 SDIO** link **[partially verified – third party]**.
- From memory (**[UNVERIFIED]**): the fixed IO_MUX pins of slot 0 are GPIO39–44 (D0=39, D1=40, D2=41, D3=42, CLK=43, CMD=44), in the VDDPST_5 (VDD_IO_5) power domain; this is the domain that the on-chip LDO (LDO_VO4 – exact number to be checked) can supply at 3.3 V / 1.8 V for UHS-I. Slot 1 can be placed on any pin via the GPIO matrix; on the EV board the C6 SDIO runs there (CLK=18, CMD=19, D0–D3=14–17, C6 reset=54 – **[UNVERIFIED]**, cross-check against the P4-pinout agent's material).
- Consequence for the project: if the C6's SDIO is slot 1 (GPIO matrix), then the SD card goes to **slot 0** (fixed pins, simple routing even on a 2-layer board, because the pins are next to each other). This does not conflict. If we put the C6 on SPI, slot 1 would be free, but SDIO is faster (recommended for esp-hosted).

### 1.2 IO voltage
- The P4 must be given an external supply on the VDDPST_5 (SD_VREF) pin if it is not supplied from the LDO; without UHS-I it can be tied to 3.3 V **[VERIFIED – search excerpt]**.
- Proposal: 3.3 V card, no 1.8 V switching (no UHS-I) → VDDPST_5 = 3.3 V fixed. Simpler, and the throughput in 4-bit High-Speed mode (50 MHz, ~20–25 MB/s theoretical) is plenty for 1080p MJPEG/H.264 recording. The on-chip LDO 1.8 V option would only be needed for UHS-I.
- Card supply: from 3.3 V through a **load switch** (see 1.4), so that a faulty card state can be recovered by removing power (power-cycle).

### 1.3 4-bit vs SPI
- **4-bit SDMMC recommended** (slot 0, fixed pins). SPI mode is slower and there is no useful gain from the P4 SDMMC hardware. SD mode needs pull-ups on CMD and D0–D3: **10 kΩ** (external, not only the internal ~45 kΩ). CLK needs no pull-up; a series 22–33 Ω on CLK is optional (EMI, useful on 2 layers).
- Boot-strapping caution: check that none of GPIO39–44 is a strapping pin **[UNVERIFIED]**.

### 1.4 Components (all [UNVERIFIED] for LCSC stock)
| Function | Proposal | Note |
|---|---|---|
| microSD socket, push-push, SMD, with card-detect (CD) switch | TF-01A (HRO / Korean Hroparts) or "TF-015" category (several on LCSC, ~C91145-like) | The exact C number is to be checked; there are several push-push types among the JLCPCB extended parts. Hand-solder: for hand soldering the pins are on the side, at 1.0 mm pitch |
| Load switch | TPS22918 (SOT-23-5) or SY6280 / "AP2552" | 3.3 V, ≥300 mA, GPIO control; 10 µs–ms soft start at ON. SD card peak ~100–200 mA during write |
| ESD | USBLC6-4SC6 (SOT-23-6) or 4-5 channel TVS array (e.g. IP4234CZ6 / "ESDA6V1") on the CMD/CLK/D0–D3 lines | Max capacitance <~10 pF, so as not to degrade the 50 MHz signal |
| Pull-ups | 6× 10 kΩ 0402 | CMD, D0–D3; CD separate pull-up |
| Supply buffering | 10 µF + 100 nF at the card VDD | Because of write spikes |

- Card detect: the socket's CD switch → GPIO, with 10 kΩ pull-up (active low); any GPIO on the P4 side.
- Location of the card socket: at the board edge, with the card removable/accessible through the enclosure wall.

---

## 2. Microphone

### 2.1 Interface choice
- According to the ESP-IDF I2S documentation, on the P4 **PDM RX is available on I2S0** (the standard and TDM modes on all of I2S0–2), and only on 1 controller **[VERIFIED – search excerpt, v5.4.x]**. The PDM bus: CLK + DIN (1 data line). Note: the v5.2/5.3 docs mention 1 I2S peripheral, v5.4+ mention three – for the P4, 3 I2S is correct (newer IDF) **[contradiction in the sources]**.
- Two paths:
  1. **PDM MEMS** (e.g. MSM261D3526H1CPM – PDM, 2.7 mm × 1.9 mm × 0.9 mm → rather the MSM261S4030H0 I2S variant; or SPH0641LU4H-1, or MP34DT05): 2 wires (CLK, DAT), 1.8–3.3 V, very cheap. Drawback: PDM→PCM filtering in the P4 hardware (I2S0 PDM RX); in the P4, using I2S0 PDM RX may block other I2S needs (see below). Typically 1.6–3.6 V.
  2. **I2S MEMS** (INMP441 – 3.3 V, 24-bit I2S, LGA-14, hard to hand-solder; ICS-43434; MSM261S4030H0 – PCM/I2S output, common at JLCPCB): 3 wires (BCLK, WS, SD) + L/R select pin. Standard I2S RX → no PDM filter question.
- **Proposal:** I2S MEMS, because (a) standard I2S RX driver, both peripherals usable, (b) no PDM aliasing/filtering in firmware, (c) simpler routing even on a noisy 2-layer board. Specific type: **MSM261S4030H0R** (LCSC-type, cheap, "bottom-port" 4.72×3.76 mm) – [UNVERIFIED], or ICS-43434 (TDK, more expensive, better SNR). I would avoid the INMP441 (LGA-14, difficult hand soldering, near EOL).
- If PDM after all: a PDM MEMS can also run from the 1.8 V domain, but the P4 signal level is 3.3 V on most GPIOs; the MSM261D3526 also works at 3.3 V **[UNVERIFIED]**.

### 2.2 P4 pins
- I2S RX: BCLK, WS, DIN = 3 GPIOs (freely selectable on the GPIO matrix – to be checked in the P4-pinout material whether the I2S pins are also on IO_MUX). For PDM, 2 GPIOs (CLK, DAT). MCLK is not needed for a MEMS microphone.
- If audio output (speaker) is not needed, RX only.

### 2.3 Acoustic port
- Bottom-port MEMS: a hole in the PCB (0.5–1.0 mm, per the manufacturer's recommendation) under the microphone, an acoustic opening in the front or side wall of the enclosure; a gasket (rubber ring/adhesive ring) between the enclosure and the PCB against sound leakage.
- For a top-port MEMS the hole is in the enclosure, there is no cutout in the PCB. Minimum 3–4 mm distance from the fan/DC-DC inductor; the microphone supply separately LC/ferrite filtered (10 µF + 100 nF + ferrite), because of the WiFi TX burst (217 Hz GSM-like "TDMA noise" is not relevant, but the buck switching noise is).
- On 2 layers: no digital signal trace should run above/below the microphone, the I2S lines should be short, the ground plane continuous.

---

## 3. IR night vision

### 3.1 IR-cut filter (ICR) control
- The mechanical IR-cut filter of camera modules (ICR variants of the OV5640, or M12-lens modules) is usually a **two-wire bistable coil**: a pulse of +/− polarity (~50–100 ms, ~5 V / 60–120 mA) pulls in the IR-cut filter (day), a pulse of opposite polarity removes it (night). The switched state does not need to be held.
- Required: **H-bridge** (two half-bridges), 2 GPIOs from the P4. Options **[UNVERIFIED]**:
  - **DRV8833** (HTSSOP-16/WQFN, small dual H-bridge, 1.5 A/channel): oversized, but widespread, available at LCSC.
  - **BA6208** (SOP-8): ICR driver typically used in IP cameras; cheap, but the available stock is uncertain.
  - **DRV8837 / DRV8838** (WSON-6/ SOT) smaller; or
  - **discrete solution**: 2× complementary MOSFET pair (e.g. 2× AO3401 + 2× AO3400 driven, or 2 pcs "CJ3134K" half-bridge) + 4 protection diodes – many parts; a dual half-bridge IC takes less space.
  - **Simplest:** 2 pcs ULN-like or 1× "FM116B"-type IC; or an `SGM2xx`-like "motor driver". Let's choose the exact part in the next iteration based on LCSC stock.
- The coil is inductive: **freewheeling/TVS diodes** (SS14 or the built-in protection of the H-bridge IC).
- During the pulse the load on the 5 V rail jumps by ~100 mA; a 100 µF bulk (reservoir) capacitor is recommended.
- Project question: is there an ICR on the selected camera module? Coordinate with the camera agent's material (many OV5640 modules have no mechanical ICR; in that case an "IR-sensitive / no-IR-cut" module + IR LEDs are sufficient, with a colour shift in daytime).

### 3.2 IR LED wavelength
- **850 nm**: a faint red glow is visible (the LEDs glow slightly), but ~2–3× better sensitivity on CMOS sensors (OV5640 QE is better at 850 nm than at 940). A good choice for longer-range illumination.
- **940 nm**: invisible, but the sensor sensitivity at 940 nm is much lower (approx. 1/3–1/2 compared with 850 nm) → more LEDs/current are needed for the same light.
- **Proposal:** 850 nm, 3–6 pcs 5 mm / 3535 SMD LEDs (e.g. OSRAM SFH 4235 / "Everlight IR333"), or LCSC 850 nm 3535 SMD types; max ~20 cm–3 m range for room monitoring. [UNVERIFIED – specific part number]

### 3.3 Drive and PWM
- 850 nm IR LED Vf ≈ 1.4–1.6 V @ 100 mA. From 5 V: **2 LEDs in series + series resistor** (Vf ≈ 3 V → 2 V drops across the resistor, ~20 Ω for 100 mA) or 3 LEDs in series (4.5 V – little voltage headroom, not recommended because of USB voltage drop).
- **Simple:** 2 × (2 LEDs + resistor) parallel branches, **low-side N-MOSFET** (e.g. AO3400/ 2N7002 / SI2302), the gate driven by a P4 GPIO with PWM (LEDC); the resistor limits the current. Current stability is poor (Vf temperature dependence, 5 V fluctuation), but this is acceptable for IR auxiliary light.
- **Better:** constant-current LED driver, e.g. **AL8860** (buck, 1 A, SOT-89/SOT-23-5 variant), **AP3012**, **PT4115**; or a linear CC driver (e.g. **AL5809 / AL8805**). Advantage: PWM dimming pin (DIM/ADJ) directly from the GPIO, current independent of the supply voltage. The buck IC needs an inductor, which means noise and space on a small 2-layer board – therefore the simple resistor/MOSFET solution for the first prototype.
- PWM frequency: ≥ 1 kHz, to avoid camera rolling-shutter banding: either DC (no PWM) or 20 kHz+ PWM. Against stripes related to the camera exposure, the LED should be continuously on (no unsynchronised PWM <1 kHz).
- Light/dark detection: a) **LTR-303ALS / VEML7700 / BH1750** I2C light sensor (the P4 I2C already carries SCCB for the camera – a separate I2C bus is recommended for the sensor, or it can be shared thanks to the 7-bit addresses); b) **LDR + divider → ADC** (cheap, but needs calibration, the P4 ADC pins are to be checked). c) **Alternative:** no separate sensor – the firmware decides from the camera auto-exposure/AGC value (OV5640 registers) or from the average frame brightness. This is the least hardware, the recommended starting point; the ambient sensor is optional. [UNVERIFIED]
- Watch out: the IR LED light reflects behind the sensor window (glare) – the LEDs must be optically isolated from the lens (black ring/dark partition).

### 3.4 Current budget on USB-C 5 V
- With only 2× 5.1 kΩ Rd the source **does not know how much we may draw**: a USB-C port has a baseline of at least **500 mA (USB 2.0) / 900 mA (USB 3.x)**; **with Rd the source stays in "Default USB power" mode**, i.e. typically 500 mA (old USB-A–C cable, USB-A host). If the source advertises 1.5 A or 3 A with Rp, the voltage level on the Rd indicates this, but the sink (us) does not read the current from the CC voltage, it only assumes it. So the DESIGN-SAFE limit = **500 mA** (USB 2.0 default), 900 mA–1.5 A–3 A only "if the charger is capable" – common in similar simple Rd-based cameras, but disconnection from the supply (brown-out) is a risk. [Source: USB-C specification, from memory – UNVERIFIED.]
- Consequence: the average current of the IR LEDs in the budget should be ~ **100–200 mA**; peak max 300 mA (briefly). If the total system peak goes above 500 mA, USB-C PD/CC detection (e.g. a "CC logic IC", FUSB302/STUSB4500 – requests/checks 5 V/1.5 A) or a soft current limit (reducing the LED during WiFi TX) is needed.
- Thermal: 2–4 LEDs × 100 mA × 1.5 V = 0.3–0.6 W on the LEDs + 0.4–0.5 W on the resistors (if from 5 V with a resistor). Total ~1 W, a 10–15 °C rise in a small closed enclosure. P4 + C6 + camera together ~1–2 W: **the enclosure temperature (OV5640 noise increases)** and the LED lifetime are concerns. The efficiency of the buck CC driver is better (~85–90%), the resistive one ~60%. Thermal vias and copper area for heat dissipation.

---

## 4. Buttons and status LED

| Item | Proposal | Note |
|---|---|---|
| BOOT (GPIO35, strapping – P4: boot mode) | Tact switch 3×4×2 mm SMD (e.g. "TS-1187A"-like) | On the P4 the download-boot strapping pin is **GPIO35** [UNVERIFIED – to be checked with the P4-pinout agent]; 10 kΩ pull-up + button to GND |
| RESET (CHIP_PU/EN) | Tact switch + 100 nF cap + 10 kΩ pull-up (RC) | Auto-reset; for USB programming the serial USB-JTAG/Serial (the P4 has native USB 2.0 OTG HS and USB-Serial-JTAG [UNVERIFIED]) |
| User button | Tact switch → GPIO, internal pull-up or 10 kΩ, 100 nF debounce | E.g. WiFi provisioning / factory reset (long press) |
| Status LED | **Simple 0603 LEDs** (green/red, 1 kΩ series resistor) or **WS2812B-2020 / SK6812 mini** | WS2812: 1 GPIO, but needs a 5 V data signal level (from a 3.3 V GPIO most WS2812B are not reliable; SK6812 mini-e or WS2812B-2020 may also accept 3.3 V data if the supply is 4–5 V – [UNVERIFIED]); alternative: 74LVC1T45 level shifter. RGB LED current ~5–10 mA each → 20–30 mA in the budget |

- Proposal: **1 simple single-colour/RGB LED** (3 GPIOs with PWM, or 1 two-colour LED), or a WS2812-2020 with one GPIO; the discrete 0603 LEDs are the lower complexity. If 2-layer with few pins, the WS2812 saves GPIOs.
- BOOT/RESET buttons at the board edge, with an enclosure opening; a "pinhole" reset is recommended against accidental resets.

---

## 5. Power tree (USB-C 5 V)

### 5.1 Input
- **USB-C receptacle, 16-pin** (USB 2.0-only, e.g. HRO TYPE-C-31-M-12 / "TYPE-C 16P" – common at LCSC, JLCPCB extended), 2× **5.1 kΩ** CC1/CC2 → GND (Rd). 5 V only, no PD. D+/D− routed to the ESP32-P4 USB 2.0 HS (OTG) PHY / for programming (coordinated with the P4-pinout agent); a 22 Ω series resistor is not needed, but ESD is.
- **Protection:**
  - Polyfuse (PTC) 1.1–1.5 A hold (e.g. 1206L110) **or** eFuse (e.g. TPS2553/TPS259xx, or a cheaper "SY6280"-style current-limiting load switch) → the eFuse gives an exact current limit (e.g. 1.0 A), plus overvoltage/reverse-current protection. Because of the 500 mA default, even a 700 mA current limit could be considered.
  - **TVS:** SMBJ5.0A (large, 600 W – oversized, but strong against surges) or the smaller SMAJ5.0A / ESD9B5.0 / "PESD5V0" on VBUS; ESD array (USBLC6-2SC6) on D+/D− and on the CC pins.
  - Input capacitance: 10–22 µF ceramic + 100 µF bulk (series ferrite/RC to damp the hot-plug spike, because of USB-C hot-plug ringing).
  - Reverse polarity: not needed for USB-C.

### 5.2 3.3 V rail (main)
- Buck 5 V → 3.3 V, ≥2 A (because of the WiFi TX peak, ~1.5–2 A nominal headroom). Options **[UNVERIFIED – LCSC stock]**:
  - **SY8089** (SOT-23-5, 2 A, 2.7–5.5 V in, simple, common at JLCPCB, cheap). A good first choice.
  - **TPS62A02** (SOT-583/ 2 A, 6-pin, very small, but more expensive, smaller inductor 1 µH).
  - **MP2143 / MP2161** (2 A, 3-pin small) – same class.
  - Inductor 2.2 µH, ≥3 A saturation, shielded (e.g. 4×4 mm); output 22 µF ×2.
- On 2 layers: the buck loop (input C, IC, inductor) in one corner of the board, with a short loop, far from the microphone and the camera; the ground plane uninterrupted.

### 5.3 The P4's own supply rails (cross-check with the P4-pinout agent!)
- Is the ESP32-P4 **VDD_HP/core** voltage generated by **the chip's internal (integrated) regulator**? According to the official P4 hardware design guidelines the chip requires **external 3.3 V** (VDDA, VDD_DIG-IO, VDD_FLASH), and the core voltage comes from the internal DCDC/LDO – the **P4 internal DCDC** (for VDD_HP) may require an external inductor [UNVERIFIED – critical, the hardware design guide must be read!]. Note: on the ESP32-P4-Function-EV-Board schematic a separate PMIC/DCDC ('VDD_HP' supply) and the chip's LDOs (e.g. VDD_PSRAM/VDD_MIPI 1.8 V / 2.5 V) are visible – this schematic must be opened before the power tree is finalised.
- Internal LDOs (from memory, [UNVERIFIED]): LDO_VO1..4 – one is the analog supply of the MIPI-DSI/CSI PHY (VDD_MIPI_DPHY 2.5 V from the internal LDO), another the VDDPST_5 (SD) 1.8 V/3.3 V, one for the PSRAM/flash. These internal LDOs require external capacitors.
- Built-in PSRAM/flash: the P4 module (ESP32-P4 "Function" chip) contains PSRAM in package (16/32 MB); external SPI flash 3.3 V or 1.8 V (version-dependent) – see the P4-pinout agent.

### 5.4 Camera rails (OV5640)
- Typical OV5640: **AVDD 2.8 V** (analog, noise-sensitive), **DVDD 1.5 V** (core; built-in LDO on many modules), **DOVDD 1.8 V** (IO) or 2.8 V. MIPI CSI on the P4: the IO level is ~1.8 V.
- LDOs: **ME6211C28** (2.8 V, 500 mA, SOT-23-5) and **ME6211C18** (1.8 V); DVDD 1.5 V: **ME6211C15** or RT9013-15; all three are available at LCSC (ME6211 series JLCPCB basic/extended). **Fixed-voltage variants**, 1 µF–2.2 µF input/output ceramic. A separate LDO (low noise) and ferrite for AVDD. Coordinate with the camera agent's material: if there is a ready-made, connectorised **camera module** (FPC), the module typically requires 3.3 V or 2.8 V and contains LDOs.
- Order (power-up sequencing): OV5640 datasheet: AVDD → DVDD → DOVDD order / PWDN/RESET pins – the EN pins of the SOT-23-5 LDOs from a P4 GPIO or RC-delayed; [UNVERIFIED – the camera agent's material].

### 5.5 Current budget (ESTIMATE – all [UNVERIFIED])
| Consumer | Average (mA referred to 5 V, ~85% efficiency) | Peak | Note |
|---|---|---|---|
| ESP32-P4 (streaming, 1080p encoding, 2×400 MHz + PSRAM) | ~250–350 | ~450 | Estimated; measurement needed. The P4's own figures are in the official datasheet (TX/RX/active mode) – to be checked |
| ESP32-C6 (WiFi 6 TX average/peak) | ~80–120 | ~350 (TX peak, 3.3 V) | The 350 mA is the TX peak given in the task; ~230 mA on the 5 V side |
| Camera module (OV5640 + MIPI) | ~120–150 (~150 mA at 3.3 V) | ~180 | Estimated |
| microSD (write) | ~50–100 (at 3.3 V) | ~150–200 | Estimated; 4-bit write peak |
| Microphone, buttons, LED | ~5–30 | ~40 | WS2812 RGB: +20–30 mA |
| IR LEDs (850 nm, 2–4 LEDs) | 0 (day) / 100–200 (night) | 300 | The main variable; see 3.4 |
| Buck loss, ICR pulse | included | +100 mA (<100 ms) | |
| **Total (day)** | **~450–650 mA @ 5 V** | ~800–900 mA | **We may exceed the 500 mA default USB limit!** |
| **Total (night, with IR)** | **~600–850 mA** | ~1.1 A | A 1.5 A charger is needed |

- Consequence: the system **typically goes above 500 mA** from a USB 2.0 port. Recommended: (1) operate from a USB-C charger (5 V/≥1.5 A), (2) record the minimum charger in the documentation (5 V/2 A), (3) limit the IR LED in firmware during WiFi TX load, (4) ≥470 µF/low-ESR bulk at the input for the TX bursts and for hot-plug.

---

## Sources
- SDMMC Host Driver, ESP32-P4 (v5.5.x): https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32p4/api-reference/peripherals/sdmmc_host.html (search excerpt; the page content was not opened)
- SDMMC Host Driver, ESP32-P4 (v5.4): https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32p4/api-reference/peripherals/sdmmc_host.html
- Older sdmmc_host.rst (GitHub, variant with a different fixed IO_MUX assignment): https://github.com/espressif/esp-idf/blob/636ff35b/docs/en/api-reference/peripherals/sdmmc_host.rst
- Arduino-ESP32 PR (P4 EV board, SD = slot 0, C6 SDIO = slot 1): https://github.com/espressif/arduino-esp32/pull/10460
- I2S driver, ESP32-P4 (v5.4.x, PDM RX only on I2S0): https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32p4/api-reference/peripherals/i2s.html
- Could not be opened (WebFetch hook error): ESP32-P4 datasheet / hardware design guide, ESP32-P4-Function-EV-Board schematic, LCSC/JLCPCB stock, manufacturer datasheets (SY8089, TPS62A02, ME6211, DRV8833, AL8860, MSM261S4030H0).

## Open questions / risks
1. Open the **EV board schematic** (ESP32-P4-Function-EV-Board): exact pins of SD slot 0, VDDPST_5 supply (on-chip LDO vs external 3.3 V), C6 SDIO pin assignment – every GPIO number given here is [UNVERIFIED].
2. **P4 core supply**: is an external inductor / DCDC (VDD_HP) needed? Must be checked against the hardware design guide before the power tree is finalised (with the P4-pinout agent).
3. **USB-C current limit**: Rd-only → 500 mA default; the estimated consumption may exceed this. A decision is needed: usable only with a ≥1.5 A charger, or a CC-detecting/PD-sink IC.
4. **Measurement data missing**: P4 streaming current, C6 average/TX peak, camera current, SD current – the table is an estimate.
5. **Presence of an ICR** on the chosen camera module (many OV5640 modules have no mechanical ICR). If there is none, the H-bridge can be omitted.
6. **PDM vs I2S**: on the P4, PDM RX is only on I2S0 (per the v5.4 docs); I2S MEMS recommended. Contradicting I2S count between IDF versions (1 vs 3) – to be checked in the current IDF.
7. **WS2812 3.3 V data signal level**: unreliable from a 3.3 V GPIO; level shifter or a 3.3 V-compatible LED.
8. **Thermal**: in a closed enclosure P4 + IR LED + buck ~1.5–2 W; the OV5640 noise level and the LED lifetime; heat dissipation on 2 layers is limited.
9. **2-layer PCB**: routing of SD 4-bit 50 MHz, I2S and buck noise; the microphone and the camera AVDD are noise-sensitive near the buck.
10. **LCSC/JLCPCB stock and C numbers** not checked: every part number must be checked before the final BOM.
