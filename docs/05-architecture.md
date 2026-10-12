# 05 – System architecture (v0.6 as-built)

Date: 2026-10-09 · as-built update: 2026-10-10 · **final rev A as-built: 2026-10-11** · Status: **v0.6 final as-built – §0.1, §0.2, §3, §3.1, §3.1a, §4.1, §6, §13, §15 aligned to the measured state of round 8 (fix passes) and round 9 (final multi-agent review, conditional GO)**; before that: **v0.6 as-built – §0.1, §3, §3.1, §5, §6, §12 aligned to the MAIN v0.6 board (45×45, 4 layers) based on the round-7 PCB review**; before that **v0.5 – the items of review rounds 1–3 and round 4 (R4: diagram re-check, `08` defect list) incorporated; the Rev A plan is in §0** (`90-review-log.md`); floorplan source: `06-floorplan.md` (v0.3); BOM / gate sheet: `07-bom-plan.md`
This document **overrides** the recommendations of documents 01–04 wherever they conflict.
Legend: **[UNVERIFIED]** = own knowledge / estimate, not yet confirmed by a primary source. Anything that is not marked and is not an E-fact is a design decision. **Notation:** module pad = **"P" prefix** (P2, P41–P46, P50/P51, P66, P82); processor pin = **"GPIO n"**. (The pad numbers come from the Waveshare pinout table – **E20, primary source**; the *spatial* pad map, i.e. which pad sits on which edge/corner, is an assumption, see 14.)

Changes v0.1 → v0.2: USB-C PD input with eFuse/OVP, wide-input buck; MAIN double-sided 45×45 mm, 1.0 mm; module on the back side; IR driver + ICR on the FRONT board; SD domain fix (VO4); GPIO reallocation; OTA; new sections (power tree, thermal, stream, FW/OTA, recovery, test points, bring-up, factory test, layout, pad map). Enclosure: deferred.
Changes v0.2 → v0.3 in short: **VBUS max 9 V** (PD 9 V, 5 V fallback; "5–12 V" removed); eFuse parameters (OVP/UVLO/ILIM/reverse-blocking/auto-retry) and capacitance budget; **CH224A + PG → GPIO + VBUS_SW ADC**, external Rd forbidden; CC-tap resized; **FULL/MID/LOW power modes** (boot always LOW, ≥1.5 s settle); power budget recalculated (4.5 V, η 0.82, daytime peak, LOW peak); USB ESD 3.3 V array; **IR separate high-side switch** + driver Vin 4.5–9.45 V criterion, series NFET dimming, LEDC ≥40 kHz; ICR H-bridge from 3V3; CAM_3V3 load switch mandatory; supervisor; CSI layer-change rule (symmetric via pair); GND pour rule; **stack gap 7 mm**, square 16×16 lens cutout; strapping table + check; EMC subsection; NTC + thermal envelope; PD hard-reset and power-outage tolerance tests; C6 OTA bring-up gate; §17/§19 updated.
Changes v0.3 → v0.4 in short: **new §0 Rev A plan** (goal, Fit/DNP table, gates G0–G6, procurement list); **E20** full pad map → every TBD pad filled in, the deviation of the CSI pad order from J2 flagged (CLK P/N reversed, pair order D0–CLK–D1 vs D0–D1–CLK); independent power path (DNP bypasses, TP4 feed-in; K-1); IR branch: 2nd eFuse / fused 0 Ω (K-3); the wrong sentence "in the 20 V case the eFuse OVP protects" corrected, the TVS sits before the eFuse (K-4); ICR only in rev B (K-5); RF/antenna decision after the module schematic (K-6); official bring-up = MAIN standalone with a standard FFC (K-7); module soldering and EDA/process (§3.1; K-10, K-18); DNP blocks: supervisor, CC-tap, SD, C6/UART0 header (K-14..K-17); height limit under the camera **G − 3.2 − 0.5 = 3.3 mm** (G = 7); the "CC-tap ~5 %" claim removed; minimum source per power mode (4.3); `00-K8` / `06-K8` reference prefixes; C6_IO8 pull-up mandatory everywhere; the 1.0 mm CPWG numbers derived from the 0.8 mm rows → field solver; **new `07-bom-plan.md`**.
Changes v0.4 → v0.5 in short (R4, `08` defect list): **IR branch fully DNP in rev A** (the "fused 0 Ω" text corrected); **TP plan**: back-side pogo group TP1–TP7, TP9–TP17, TP9 and TP16 split in two (18 pads, of which TP3 = GND, + 2 GND pads), TP8 front/DNP; **every 100k pull-down on the MAIN back side** (K-7); **status LED on the MAIN back side** (GPIO 6), J5.17 spare; **CC ADC removed from the rev A boot sequence**; power tree: raw VBUS → CH224A VDD, NTC divider, VEML7700, TVS + ESD on the back side (VBUS on ≥2 vias to the front eFuse); §0.1 extended (VO4, strap, I2C, ESD, shield RC, Rd); **J7 = 1×9**; the label "GPIO 54 / C6_EN (P82)" (Q2) everywhere; **new gate G5b**; the **CSI/J2 decision moved to G3** (the G2–G3 circularity eliminated); §5: unused pads; §6: J3, J4, J6, J7 pin tables; §0.4: Q26, Q15 👤.
Changes v0.5 → v0.6 as-built (2026-10-09/10; measured from the PCB, `90-review-log.md` round 7): **MAIN 45×45 mm, 4 layers** (the 60×50 / 2-layer rev A overridden, 00 K4); **new §3.1a: frozen mechanical interface** (M2 grid centre (22.5; 25.0) – 2.5 mm below the board centre; J2, J5, J1, J4, J7, SW1–3, D20 coordinates); §5 GPIO v0.6 verified against the module pads; §0.1: delegated decisions of 2026-10-10 (R23/C25 FIT, D2 DNP, R28 10k, camera control ESD and SD ESD → rev B, DNP stubs removed); §12: as-built TP list (12 pads); §6 J7 / J2 / J4 as-built.
Changes v0.6 → v0.6 final as-built (2026-10-11; `90-review-log.md` rounds 8–9): **C14 1 µF / 25 V on U3 OUT (new FIT)**; R23/C25 FIT, D2 DNP, R28 10k propagated into both the schematic and the board; **G4 closed for rev A** (72 FIT items with LCSC numbers, `07`); J2 = TE 1-84953-5 (ordered part), J5 = Hong Cheng pair (Q17 open); MH = stock `MountingHole_2.2mm_M2` + washer rule; stackup / ENIG / impedance in the board file; D1 TVS location is an accepted deviation; **USB FS only**; CSI as-built lengths and accepted skew (§13); **pre-order gate** (refill + DRC + `--check-zones`, §3.1); bring-up: measurements before first power, U1 / J1 hand soldering, rev A FW rules, G5b CSI soak test (§15).

## 0. Rev A plan (v0.5) – proof-of-concept prototype

**Goal:** **prove the core path**: USB-C PD (9 V) → eFuse → buck 3V3 → P4 module → OV5640 MIPI → ISP → H.264 → RTSP → esp-hosted C6 WiFi, with 24 hours of continuous operation. **Success criterion:** stable stream (the best resolution/fps measured at G0, target 1080p30), 24 h without reset, 9 V PD negotiation + PG correct, surviving PD hard reset ×20. **Not a goal in rev A:** night vision (IR/ICR), microSD, MID mode, closed-enclosure thermal tolerance, final mechanics. Anything not needed for the core path is **present with its footprint but DNP** (can be fitted in rev B without a redesign).

- **Official bring-up configuration (K-7):** the **MAIN standalone**, the camera on a **standard 50–100 mm FFC**, open (not closed) stack. The stack (FRONT + 25–30 mm FFC) is closed only **after a stable image**.
- **Order sequence (K-13):** **MAIN first**; the FRONT later (G6), because it depends on the camera STEP (cutout, datums, gap).
- **Board size (K-12):** ~~rev A MAIN = 60×50 mm, 2 layers (Q22)~~ → **overridden (owner decision 2026-10-09, 00 K4): the rev A MAIN = 45×45 mm, 4 layers** (JLC04101H-3313A, 0.97 mm; §3.2). The 60×50 / 2-layer variant is archived (`kicad/archive/MAIN_2L_60x50_2026-10-09/`, not fully routed). The FRONT is 45×45. **The frozen interface towards the FRONT and the enclosure is the as-built table of §3.1a** – the mounting-hole grid is **not** symmetric about the board centre (its centre is (22.5; 25.0), the board centre is (22.5; 22.5)).
- **Mode logic (K-15):** boot always LOW; **FULL** only if, after a ≥1.5 s settle, VBUS_SW ≥ 8 V (ADC + PG), otherwise LOW. There is no MID (the CC-tap is DNP): on a 5 V/1.5 A source it runs in LOW.
- Every estimate is **[UNVERIFIED]** until the G0 measurements replace it.

### 0.1 Fit vs DNP (rev A)
| Block | Rev A | Note |
|---|---|---|
| USB-C J1 (16 pin) + 3.3 V ESD array + TVS (SMAJ10A class) | **FIT** | pin map: `07` §3; ~~plan: the TVS + ESD on the MAIN back side, next to J1~~. **As-built (final, round 9): the D1 TVS (SMAJ10A-13-F) on the B side at / under the eFuse (U3) input (40.5; 13.5), 6.8 mm in a straight line from J1 – accepted deviation (owner sign-off, `90` round 9)**; D1.1 has its own B-side path to J1 A4/B9 (~8 mm); the **U5 USB ESD (F, (34.0; 21.2))** and the R1/C1 shield RC (F) next to J1. Soldering of the J1 shell legs: §3.1, §15 |
| J1 shield: 1 MΩ ‖ 4.7 nF → GND | **FIT** | `07` #53; C1 is a **200 V** part (YAGEO C596328; the schematic Value field still says "50V") |
| CH224A + voltage strap + PG → GPIO 31 | **FIT** | strap; PG: open-drain, active low (E22) – to be confirmed by the G1 measurement |
| eFuse (adjustable OVP/UVLO/ILIM, reverse-blocking, auto-retry) | **FIT** | **TPS259470ARPWR (C3662799)** – `07` §0 |
| **C14 1 µF / 25 V X7R 0603 on U3 OUT (VBUS_SW → GND)** | **FIT** (2026-10-11, new) | TI 8.4.1 (≥1 µF on the eFuse output); F (42.675; 16.0), 1.14 mm from U3.6; effective <1 µF at 9 V – optional BOM swap to 2.2 µF / 25 V X7R on the same footprint |
| VBUS → VBUS_SW 0 Ω / solder bridge around the eFuse | DNP | bring-up / eFuse-failure bypass (K-1) |
| 2× 5.1k Rd footprint | DNP | **only if the CH224A is not fitted – never both at once** (K-1) |
| Buck 3V3 + output 0 Ω + TP4 | **FIT** | after removing the 0 Ω, bench feed-in on TP4; **never at the same time as USB** (K-1) |
| P4 module + 3V3 bulk (47 µF + 10 µF + 100 nF) | **FIT** | hand soldering, 3.1 |
| CAM_3V3 load switch + 0 Ω measurement jumper | **FIT** | CT / slew: `07` §4 |
| J2 FPC 15 pin, J5 B2B | **FIT** | the MAIN also works without the FRONT (K-7). ~~J2 footprint = placeholder~~ → **J2 = TE 1-84953-5 (C5164008, TOP contact) – the footprint is the ordered part itself**; contact side **Q6**: decided before the first camera power-up (the bottom-contact 1-84952-5 has the same footprint → part / cable swap, not a redesign); **J5 = Hong Cheng HC-PZ127-7.2L-2x10PS (C41375929)**, generic land, **Q17 open** (`07` §0) |
| VBUS_SW ADC divider (R12 200k / R13 54.9k + C7 100 nF), NTC (ADC2), PG pull-up | **FIT** | **D2 (BZT52C3V6, VBUS_MON clamp Zener): DNP** (2026-10-10) |
| BOOT / RESET / USER button (SW1–SW3, B side); back-side TPs **as-built: TP1–TP7, TP16A/B, TP17–TP19 = 12 pads** (TP16A = ESP_EN, TP16B = GPIO 35; GND: TP3, TP18, TP19). ~~TP9a/b, TP10–TP15~~ deleted (2026-10-09): C6 / UART0 access only via the J7 pad row | **FIT** | TP8A/B is a separate row (front side, DNP); list + coordinates: §12 |
| Status LED (0603 + series R, GPIO 6) | **FIT** | MAIN back side, near the module; J5.17 spare (NC) |
| VO4: 1 µF + TP7 | **FIT** | external source forbidden |
| Strap pull-ups: GPIO 36 10k, C6_IO9 10k, C6_IO8 10k | **FIT** | §5.1; `07` #28 |
| Pull-downs: **100k** – GPIO 26, 27, 28 (R24–R26), 53 (SD_EN, R27); **10k – GPIO 4 (CAM_3V3_EN, R28; 2026-10-10, previously 100k)** | **FIT** | as-built: **MAIN front side (F)**, under the module / next to the target IC (K-7 satisfied: the MAIN works standalone); the GPIO 32 (IR_SW_EN, R29) pull-down is DNP together with the IR branch |
| UART0 series R 1–4.7k ×2 (GPIO 37/38; as-built R40/R41 1k → J7.7/J7.8) + GPIO 33 (USER, v0.6) 100 nF (C40) | **FIT** | §5, §5.1 |
| I2C pull-up (SDA/SCL, MAIN) | **DNP** | until the camera I/O level is known (G3); until then only the CH224A internal pull-ups → **rev A FW: I2C 100 kHz** (§15) |
| J2 control-signal ESD (CAM_PWDN = CAM_IO0, SCL, SDA) | ~~FIT~~ → **rev B (formally deferred, 2026-10-10)** | not in the schematic; the J2 contact side (Q6) is open, the J2 area is crowded; the lines stay inside the FFC – during bring-up, ESD care when plugging in the FFC by hand. `07` #38 |
| CC1/CC2 ESD clamp | **rev B** (2026-10-11) | not in the schematic; CH224A CC abs max 32 V; in rev A the CC goes only J1 → U2 (CC1 10.97 / CC2 7.8 mm) |
| Supervisor (open-drain variant) + 0 Ω → ESP_EN | ~~DNP~~ → **not drawn (rev B)** | K-14; only a TODO text in the schematic (no verified symbol / footprint) |
| **ESP_EN RC: R23 10k → 3V3 + C25 1 µF → GND** | **FIT** (2026-10-10; previously DNP) | Q3 (whether the module has an EN RC) is open; a double RC only slightly changes the time constant, whereas a missing pull-up means a board that does not start (nothing else pulls ESP_EN up); B side (3.2; 29.55) / (3.2; 31.25) |
| CC-tap (100k + 10 nF + 3.6 V Zener ×2) | **DNP** | K-15 |
| u.FL + π-network + CPWG | footprint FIT, every element 0 Ω / DNP-capable | K-6; G2 decides: the module's own IPEX or u.FL. **As-built: J4 + R34 (0R) FIT, C27/C28 DNP**; 0.302 mm microstrip on the B layer (ref. In2), ~7 mm track (U1 P2 → J4.1 path 7.96 mm), without vias; **round 9: In2 100 % GND underneath, GND fence 10 / 14 vias within 1.0 / 1.5 mm** |
| C6 UART/EN/IO9 + UART0 header J7 | **J7 = 9-pad SMD row, 1.27 mm (pad 0.85×1.6), DNP** (header not fitted); the C6 pogo pads (TP10–TP13) deleted | K-17; as-built: B side, top edge (22.5; 2.0), horizontal (§3.1a) |
| microSD block (J3, SD_3V3 switch U8, pull-ups) | **DNP** (footprint stays) | K-16; enabled later. **SD ESD: footprint not in the schematic → rev B** (2026-10-10). R27 (SD_EN 100k pull-down) is FIT |
| IR branch: 2nd eFuse / high-side switch (or fused 0 Ω) + shunt + TP8 + IR_SW_EN pull-down (GPIO 32) | **DNP** – the footprint stays | rev A: IR_VIN unpowered, together with the FRONT (G6); TP8 on the front side |
| FRONT board: IR LED + driver + NFET, microphone, VEML7700 (DNP) | **later (G6)** | separate board, after the camera STEP; the status LED is on the MAIN |
| ICR (DRV8837, J6) | **DNP / none** | rev B (K-5) |
| Camera | any module meeting the requirements of section 7, **NoIR or fixed lens** | K-5 |

**Delegated owner decisions – 2026-10-10 (round-7 review, `90-review-log.md`):**
1. **R23 10k + C25 1 µF (ESP_EN RC) → FIT** (electrical-02; Q3 remains open independently of this).
2. **D2 (VBUS_MON Zener) → DNP**: at the 43.1 kΩ (200k ‖ 54.9k) node, a BZT52C3V6 leakage of only ~2.7 µA already eats up the margin of the 8 V FULL/LOW threshold (~0.12 V on the ADC at the 8.55 V PDO lower limit) [leakage data UNVERIFIED]; the P4 pin is already limited by the 43 kΩ source resistance. ADC calibration at G5b.
3. **R28 100k → 10k** (CAM_3V3_EN pull-down): if GPIO 4 (MTMS) starts with an internal pull-up during reset (~45 kΩ, [UNVERIFIED]), with 100k ~2.3 V would reach the TPS22917 ON pin (the camera would switch on during reset, violating "boot always LOW"); with 10k ~0.6 V. Check at G5b: CAM_3V3 on TP5 during reset.
4. **Camera control-signal ESD (CAM_PWDN / SCL / SDA) → formally rev B**: not in the schematic; the J2 contact side (Q6) is open, the area is crowded.
5. **SD ESD footprints → rev B** (the SD block is DNP in rev A anyway).
6. **DNP stubs removed from the rev A layout (EMC):** **CC1 → R4/R35** (~97 mm edge-running branch), **CC1_ADC → C29/R35/D21** (the net – from the GPIO 21 / P30 pad – has no copper), **VBUS_SW edge stub → R73** (~44.5 mm, In2). **These parts must be reconnected before fitting**, together with the earlier 3 DNP breaks (**CC2 → R5/R36, U7 GND, VBUS_SW → U7**). ~~This leaves 9 unconnected ratsnest items on the PCB~~ → **on the final board 12 unconnected items (kicad-cli DRC, 2026-10-11), all on DNP pads** (the CC2_ADC branch belongs here too). The K-1 Rd fallback (R4/R5) only works once both CC branches are connected (otherwise it is not guaranteed in either plug orientation).

~~**Propagation:** in the schematic (2026-10-10) R23/C25 are still DNP, D2 is FIT, R28 has the value 100k – …~~ **Propagated (round 8, 2026-10-11):** schematic, PCB attributes and BOM per the above decisions (R23/C25 FIT, D2 DNP, R28 10k), + the new C14; ERC 0, DRC 0 errors (with refill), schematic ↔ board parity 0.

### 0.2 Gates (in order; the next one only after the previous one is closed)
| Gate | Content | Exit criterion |
|---|---|---|
| **G0** | **Dev-kit stream + current (K-2):** Waveshare ESP32-P4-Module dev board or ESP32-P4X-Function-EV-Board + candidate camera: OV5640 MIPI → ISP → H.264 → RTSP **over esp-hosted C6 WiFi**; **24 h soak**; current draw measured per state (idle, stream, WiFi TX peak, camera on/off); RSSI test with the candidate antennas; **freeze sdkconfig + component versions** (IDF, esp_cam_sensor, esp-hosted, esp-video) | stable stream for 24 h; the measured table **replaces the estimates of 4.3**; the chain **has never run yet** in the design so far – this is the first evidence |
| **G1** | **CH224A breakout bench test (K-4):** MacBook, cheap PD charger, USB-A→C cable; 9 V PDO negotiation, voltage strap, PG polarity / level, DP/DM NC behaviour alongside USB-Serial-JTAG | 9 V stable, PG level known, no 20 V; strap table confirmed from the datasheet (Q13) |
| **G2** | **Module schematic + footprint + antenna decision:** read the Waveshare module schematic before the MAIN routing (Q1–Q3, Q9–Q11: VDDPST_5/VO4, EN RC, C6_EN, MIPI PHY supply, RF path, esp-hosted reset); footprint import (G2 delivers **only** the module footprint / schematic; the spatial CSI pad order is known from here, but the J2 decision is in **G3**); **antenna: if the module's own IPEX is usable (module on the back side, accessible), we use it in rev A** (K-6) | footprint + 1:1 paper test; antenna decision; supervisor fitting decision |
| **G3** | **Camera module frozen:** NoIR / fixed lens, 15 pin, onboard osc + LDO, CAM_IO0 polarity, I/O level, **STEP**, FFC lengths (bring-up 50–100 mm; closed 25–30 mm) | one module selected; GPIO 23 pull (Q5) decided; **the final CSI pad order / J2 pinout decision (Q24)**: order of the selected camera / FFC + spatial order of the G2 footprint + TRM check of the lane / polarity swap + via crossing (§6, §13) |
| **G4** | **BOM sheet done** (`07`): MPN / LCSC# / footprint source for every part class + resistor calculations (buck FB/L/Cout, eFuse OVP/UVLO/ILIM, IR current/shunt, PG pull-up rail, CH224A strap) **before the schematic** (K-8) | no TBD in the rev A FIT rows – **✅ closed for rev A 2026-10-11** (72/72 LCSC; open owner decisions: Q6, Q17 – `07` §0) |
| **G5** | **MAIN schematic → layout → DRC → 1:1 print → order** (JLC; module last, by hand) | MAIN ordered – **only after the pre-order gate** (refill + save in the project folder, DRC without refill 0 errors, `--check-zones` Gerber; §3.1, `90` round 9) |
| **G5b** | **Bring-up – MAIN standalone, camera on a 50–100 mm FFC (§15)**: steps 0–7 of section 15, open stack; **+ CSI soak test with error counters (§15 7a)** | the §0 success criterion: stable stream (best resolution/fps measured at G0), 24 h without reset, 9 V PD + PG correct, PD hard reset ×20 survived; CSI error / CRC / ECC counters 0 over ≥1 h |
| **G6** | **FRONT** (IR, microphone; ICR rev B): after closing **G5b** (stable image from the MAIN), with the camera STEP; IR bench test with a shielding tube (K-19) | FRONT ordered |

### 0.3 Procurement list (K-9, K-2, K-4, K-6)
| Item | Qty | Purpose | Gate |
|---|---|---|---|
| Dev kit (Waveshare ESP32-P4-Module dev board **or** ESP32-P4X-Function-EV-Board) + candidate camera | 1 | stream chain, current, RSSI | G0 |
| ESP32-P4 module (Waveshare, 88 pad) | 3–4 | MAIN + soldering trial + spare | G2/G5 |
| Camera module candidates (15 pin MIPI, onboard osc/LDO, NoIR or fixed lens) | 2–3 | measurement, STEP, freezing one | G3 |
| FFC samples: standard 50 and 100 mm (15 pin, 1.0 mm, straight) + 25–30 mm custom / short flex | 3 + 2 | bring-up / closed stack | G3 |
| B2B 2×10 1.27 mm mated pair, 7 mm height (**2026-10-11: in the BOM Hong Cheng C41375929 + C27985222, 5.3 mm; Samtec 7.47 mm alternative – Q17**) | 2–3 pairs | stack, tolerance, wipe (Q17) | G3/G4 |
| USB-C 16 pin receptacle (THT shell) samples | 3–5 | footprint, soldering | G4 |
| microSD card (branded) | 2 | rev B SD | – |
| IR LED 850 nm 3535 | 8–10 | rev B / FRONT | G6 |
| PD trigger / analyser that **can force a hard reset** | 1 | PD hard reset ×20 (4.1, 15.) | G1 |
| USB power meter (V/A) | 1 | current, UVLO | G1 |
| USB-UART (3.3 V logic) | 1–2 | C6 UART flash | G5 |
| CH224A breakout (+ MacBook, cheap PD charger, USB-A→C cable) | 2 | strap / PG / DP-DM test | G1 |
| Soldering iron + flux, hot-air / preheater, solder wick | 1 | module hand soldering (3.1) | G5 |
| 1:1 3D print (stack mock-up: 2 boards, 4 standoffs, camera) | 1 | mechanics, pin 1 | G3 |
| Antenna (2.4 GHz, IPEX Gen1 / u.FL) | 2 | RSSI comparison | G0/G2 |
| Shielding tube / window spacer (black) | 1 | IR bench test (K-19) | G6 |

### 0.4 Open owner decisions
- ~~**Q22:**~~ ✅ **closed: rev A MAIN 60×50 mm** – **overridden 2026-10-09: MAIN 45×45 mm, 4 layers (00 K4; §3.1a)**. Original question: should the rev A MAIN be larger (e.g. 60×50 mm), **with the same M2 grid and J2/J5 coordinates**? (45×45 remains the target; the larger board would improve access for bring-up and soldering)
- **Q26:** EDA = **KiCad** ✅ (2026-10-09); open remainder: JLC assembly of the USB-C THT shell → **2026-10-11: the J1 shell legs have no paste (`attr smd`), so JLC reflow leaves them unsoldered → decision at order time: JLC hand / selective soldering, or the owner solders them before the first cable insertion (§15).**
- **Q6, Q17** (J2 contact side, J5 height) and the **U5 clone pinout**: `07` §0; the full list of owner items: `90-review-log.md` round 9.
- **Q15:** 👤 indoor v1 (affects the T_amb of the thermal envelope and the LED choice).

## 1. Browser-verified facts (primary source, 2026-10-09)

| # | Fact | Source |
|---|---|---|
| E1 | Waveshare **ESP32-P4-Module**: ESP32-P4NRW32 (32 MB PSRAM in-package) + 16 MB flash + **ESP32-C6H8 inside the module, over SDIO** | waveshare.com/wiki/ESP32-P4-Module |
| E2 | Module size **25 × 25 × 3.3 mm**, 88 castellated pads, **1.0 mm** pitch (bottom pads: check the land pattern in the zip) | ibid. (size.jpg) |
| E3 | Module supply: **ESP_3V3 (P85, P86)** + **VBAT (P84)** → 3.3 V. Internal DCDC/LDO on the module → we only need 3.3 V | ibid. pinout |
| E4 | Broken out: MIPI-CSI 2 lane (P41–P46), MIPI-DSI, USB HS (P48/P49), USB-Serial-JTAG / FS PHY GPIO24/25 (P50/P51), GPIO0–13, 20–23, 26–54, ESP_EN (P87), ESP_LDO_VO4 (P66) | ibid. |
| E5 | **Not broken out:** GPIO14–19 → internally occupied by the C6 SDIO link (**inference**, not a direct statement) | ibid. (inference) |
| E6 | C6 programming pins broken out: C6_U0RXD (P4), C6_U0TXD (P5), C6_IO9 (P9, BOOT), C6_IO8 (P10; the wiki recommends a 10k pull-up → **mandatory for us**), C6 JTAG IO4–7 | ibid. |
| E7 | C6 antenna: connected to the **LNA_OUT (P2)** pad by default; IPEX Gen1 only by re-soldering a 0 Ω (→ rev A: if the module is on the back side and the IPEX is accessible, we use it, §0 G2) | ibid. |
| E8 | P4 BOOT: **GPIO35** low at power-up = download (if GPIO36 is pulled up); **GPIO36 10k pull-up to 3.3 V** recommended | ibid. |
| E9 | The IO supply of GPIO39–48 is **ESP_LDO_VO4** (default 1.8 V, adjustable from software) | ibid. |
| E10 | P4 USB-Serial-JTAG: **GPIO24 (D−) / GPIO25 (D+)** (alternative 26/27); flash + console + JTAG, auto download mode → **no USB-UART chip needed** | IDF docs usb-serial-jtag-console (esp32p4) |
| E11 | esp_cam_sensor: **OV5640 supported in both MIPI and DVP** mode on the P4 (RGB565/YUV422 output). Also SC2336, OV5647, OV5645, GC2145 etc. | github espressif/esp-video-components esp_cam_sensor/README; esp_cam_sensor README, master branch, 2026-10 |
| E12 | P4 ISP max input 1920×1080; MIPI-CSI max **1.5 Gbps/lane** | ibid. |
| E13 | Espressif EV board camera connector: **1.0K-GT-15PB** (15 pin, 1.0 mm FPC), straight ("forward") cable | esp-dev-kits P4-Function-EV-Board v1.5.2 user guide |
| E14 | EV board v1.5.2 **EOL**; current: ESP32-P4X-Function-EV-Board (chip rev v3.x) | ibid. |
| E15 | EV board: microSD 4-bit, I2C on GPIO7/8 (J1 header), UART0 = GPIO37 TX / 38 RX | ibid. |
| E16 | P4 SDMMC: **slot1 = GPIO matrix** (non-UHS), **slot0 = UHS-I, IO_MUX fixed pins**; the IO voltage is supplied externally on the **VDDPST_5 (SD_VREF)** pin. For non-UHS it can go to a fixed 3.3 V, or come from the on-chip LDO (`sd_pwr_ctrl_new_on_chip_ldo`) | IDF docs sdmmc_host (esp32p4) |
| E17 | SD slot0 pins on the P4: **CLK=43, CMD=44, D0=39, D1=40, D2=41, D3=42**; IDF example: on-chip **LDO ID 4** (= VO4), card power-reset default **GPIO45** | esp-idf examples/storage/sd_card/sdmmc Kconfig + esp-hosted-mcu Kconfig.host.sdio |
| E18 | esp-hosted P4 + C6 (EV board): SDIO **slot1**, CLK=18, CMD=19, D0=14, D1=15 (D2/D3=16/17), **C6 reset = GPIO54** (P4 default) | esp-hosted-mcu host/mcu/.../Kconfig.host.sdio |
| E19 | esp-hosted has an `mcu_hosted_sdio_sdmmc_combined` example → SD card + C6 SDIO together on one host is supported | esp-hosted-mcu repo tree |
| E20 | **Full module pad map** (88 pads): P1 GND, P2 LNA_OUT, P3 GND, P4 C6_U0RXD, P5 C6_U0TXD, P6 C6_IO15, P7 C6_IO14, P8 C6_IO13, P9 C6_IO9, P10 C6_IO8, P11–P14 C6_IO7..IO4 (JTAG), P15 GND, P16 GPIO1, P17–P28 GPIO2..GPIO13, P29–P32 GPIO20..GPIO23, P33 GND, P34–P39 DSI, P40 GND, P41 CSI_D0N, P42 CSI_D0P, P43 CSI_CLKP, P44 CSI_CLKN, P45 CSI_D1N, P46 CSI_D1P, P47 GND, P48 USB_DM(HS), P49 USB_DP(HS), P50 GPIO24, P51 GPIO25, P52 GND, P53–P61 GPIO26..GPIO34, P62 GPIO35, P63 GPIO36, P64 GPIO37, P65 GPIO38, P66 ESP_LDO_VO4, P67–P82 GPIO39..GPIO54, P83 GND, P84 VBAT, P85 ESP_3V3, P86 ESP_3V3, P87 ESP_EN, P88 GPIO0. **Note:** the CSI pad order is D0N, D0P, **CLKP, CLKN**, D1N, D1P – the P/N order of the CLK pair is reversed relative to the D pairs (see 6. J2 note, 14.) | waveshare.com/wiki/ESP32-P4-Module, pinout table (primary source) |

## 2. Main decisions

| ID | Decision | Rationale |
|---|---|---|
| D1 | **Waveshare ESP32-P4-Module** instead of a bare QFN104 | on 2 layers the QFN104 + VDD_HP DCDC + flash + crystal + C6 + RF is too risky (01 doc) |
| D2 | C6 = the C6H8 inside the module | E1. No SDIO routing on our PCB |
| D3 | Camera: **OV5640 MIPI 2-lane**, 15 pin 1.0 mm FPC; the module **must** have its own oscillator + LDOs + 3V3 input (there is no XCLK on the FPC). **Lens with ICR (IR-cut): mandatory in rev B; in rev A a NoIR or fixed-lens module is fine too** (K-5, Q5) | E11, E13, F-27, A-37, K-5 |
| D4 | Programming: USB-C → GPIO 24/25 USB-Serial-JTAG (first flash only); then OTA (D8) | E10 |
| D5 | Power: **USB-C PD sink, VBUS max 9 V**: CH224A (+PG pin → GPIO, mandatory; 9 V request, 5 V fallback on a PC/legacy port) → ESD/TVS (SMAJ10A class) → adjustable-OVP, reverse-blocking, auto-retry eFuse → wide-input forced-PWM buck 3V3 ≥2 A (TPS62933F class) [parts **UNVERIFIED**]. **No 2nd (product) power input**; in rev A only DNP debug paths (§0, 4.1) | E-1, E-2, E-13, E-35, B-4, B-11, K-1 |
| D6 | **2 pcs, ~1.0 mm FR4**: FRONT 45×45 (2 layers, if sufficient) + **MAIN 45×45, 4 layers** (JLC04101H-3313A, 0.97 mm; §3.2) – the earlier "rev A: 60×50, 2 layers" overridden (00 K4). Common interface (M2 grid, J5, J2): **§3.1a as-built**. MAIN double-sided (see 3.) | P-2, P-3, P-8, 00 K4 |
| D7 | Microphone: PDM MEMS on the FRONT (right strip); light sensing: no LDR, day/night based on the camera AE/gain; optional VEML7700 footprint (DNP), **shielded from our own 850 nm IR LEDs** (Cu ring + black foam / window aperture) | E-16, E-21 |
| D8 | **OTA**: P4 app with 2 OTA partitions (16 MB flash); C6 slave FW via esp-hosted OTA from the P4. USB only for the first flash. **C6 OTA = bring-up gate** (9., 15.) | 00-K8, A-36 |
| D9 | IR: 850 nm, 4× 3535 LED, per-branch CC driver on the FRONT, **a separate, second adjustable-ILIM eFuse (≥18 V rating, ILIM 0.5–0.7 A) on the MAIN** – the TPS22810 class has no adjustable current limit [UNVERIFIED], hence rejected; **rev A: the whole IR branch DNP, the footprint stays** (IR_VIN unpowered until G6; the fused 0 Ω is only a rev B alternative); series NFET dimming; ICR H-bridge (DRV8837 class) on the FRONT **from 3V3**, **DNP in rev A (ICR: rev B)**. Branch topology per the 4.2 criterion | E-9, E-10, E-19, B-14..16, B-25, K-3, K-5 |
| D10 | Enclosure: **later** – PCB only for now. See 18. | |
| D11 | Firmware power modes: **FULL / MID / LOW**, boot always LOW (4.3) | B-2, B-3, B-17, B-19 |
| D12 | **Rev A = proof-of-concept prototype**: MAIN first, gates G0–G6, DNP blocks (§0) | K-2, K-7, K-13 |

## 3. PCB stack (mechanics)

Floorplan source: **`06-floorplan.md`** (area and height budget, ASCII floorplan, K1–K13). The pad numbering there is an **assumption [F]** and must be treated as such until the Waveshare footprint is imported (14.).

```
 forward (lens direction) ↑
 ┌──────────────────────────────────────────────┐
 │ FRONT  45×45, 1.0 mm, 2 layers                 │ front: lens cutout ~16×16 mm square (R1), IR LED ×4 (3535),
 │                                                │       PDM microphone (right strip), (VEML7700 DNP)
 │                                                │ rear: camera module, IR CC drivers (+NFET), DRV8837 + ICR conn. (DNP),
 │                                                │       B2B header
 └──────────────┬─────────────────────────────────┘
        B2B 2×10 1.27 mm mated height 7 mm [UNVERIFIED: availability]  +  4× M2 standoff 7 mm (structural element)
        camera FPC: short flex or 25–30 mm custom cable (gate: Q5/Q6), from the module's own FPC socket into MAIN J2
 ┌──────────────┴─────────────────────────────────┐
 │ MAIN   45×45, 4 layers, 0.97 mm, DOUBLE-SIDED  │ front side (F): J2 FPC (top edge; control-signal ESD: rev B), J5 B2B (bottom edge), buck + eFuse + PD IC, IR branch (2nd eFuse; rev A: DNP) + shunt + TP8,
 │                                                │       CAM_3V3 switch, microSD (left edge, DNP), NTC, VBUS divider (after the eFuse), GPIO pull-downs; components under the camera ≤3.3 mm
 │                                                │ back side (REAR, B): P4 module, USB-C (right edge) + TVS, u.FL (left edge), BOOT/RESET/USER button (top edge),
 │                                                │       status LED (GPIO 6), TPs (TP1–TP7, TP16A/B, TP17–TP19), C6/UART0 DNP pad row (J7, top edge); supervisor: rev B
 └────────────────────────────────────────────────┘
 as-built coordinates and sides: §3.1a (the v0.5 60×50 / 2-layer plan overridden)
 backward ↓
```

| Rule | Value / decision | Ref |
|---|---|---|
| Board thickness | **1.0 mm** for both boards, every calculation is based on this; **MAIN as-built: 0.97 ± 0.10 mm** (4 layers, JLC04101H-3313A, §3.2) | P-8, E-28, F-29 |
| Assembly sequence | 1. camera FPC → J2 (ZIF at the board edge, ≥20 mm slack) → 2. check (continuity/image) → 3. close the stack. **Rev A: bring-up with the MAIN standalone, with a standard 50–100 mm FFC; closing only after a stable image** | P-13, K-7 |
| Manufacturing | JLC SMT for everything else; P4 module **last**, by hand (3.1); **MAIN first, FRONT later** (depends on the camera STEP) | P-21, K-13 |
| **Gap (stack gap)** | **G = 7 mm**: B2B 2×10 1.27 mm header pair, mated height 7 mm [UNVERIFIED: whether such a part exists, tolerance ±0.2–0.3 mm, wipe]. The MAIN front-side components **under the camera ≤3.3 mm** (= G − 3.2 − 0.5; 3.2 = camera PCB 1.2 + back-side components 2.0); FRONT back-side S strip (IR driver) + MAIN J2 actuator zone: 06-K13 (4.6 < 7). The module (3.3 mm, E2) is on the back side | P-2, 06 §3/K13 |
| **Camera FPC** | Length **gated by Q5/Q6**: short flex (the module's own FPC) or **25–30 mm custom cable**; the earlier "40–60 mm S-loop" **removed** (06-K1: ~25–33 mm of excess cannot be held in a 7 mm gap). Straight ("forward") cable, bend R ≥2 mm. **Rev A bring-up: standard 50–100 mm FFC, open stack** (§0); closed stack: 25–30 mm | P-14, 06-K1, K-7 |
| Lens cutout | **~16×16 mm square** (R1 corners), milled, **not a Ø hole**; the camera holder reaches forward through the cutout (06 variant "A"); an **axis-aligned** 14×14 mm holder fits through with 1 mm/side clearance (the 19.8 mm diagonal only matters for a rotated holder; the R1 corner does not narrow it); final size with the camera module STEP | P-24, 06-K9 |
| Fixing | 4× M2 standoff, **33.5 mm common grid**, 2.2 mm NPTH, 3.8 mm keep-out; **the standoff is the structural element, not the header**. **As-built (MAIN v0.6):** MH1–MH4 = (5.75; 8.25), (39.25; 8.25), (5.75; 41.75), (39.25; 41.75), Ø2.2 NPTH – the grid centre is **(22.5; 25.0), 2.5 mm below the board centre** → frozen, §3.1a. Moving the holes to symmetric positions would collide (J4, TP17/TP18, JP1). ~~mask opening Ø3.2 (exposed GND ring)~~ → **final: stock `MountingHole_2.2mm_M2`** (board-only, excluded from BOM/CPL): mask opening = hole (Ø2.2), GND copper from r 1.36 mm under mask → **no exposed GND ring, the screw / standoff floats electrically**; courtyard r 2.45 only on the F side (DRC does not check the B side). Signal copper under the screw head / standoff (insulated only by the mask): MH1 / MH2 I2C_SDA (B) 1.95 / 1.93 mm, MH2 EF_UVLO (F) 2.40 mm, MH4 I2C_SDA via 2.18 mm from the hole centre. **Assembly rule (round 9): nylon standoff or nylon washer on MH1 / MH2 / MH4; no washer on MH3 (the J4 GND pad is 2.54 mm away), screw head max. Ø4.0 mm, the u.FL cable exits towards W / N** | P-16, P-23, mech-01, mech-04, mech-10 |
| Camera fixing | 2 NPTH datums on the FRONT | P-24 |
| IR → lens | Cu ring (IR baffle) around the cutout on both layers + plated edge; LEDs at ≥10 mm radius from the lens axis; LED heat spreading on the back-side Cu | P-17, P-28 |
| Microphone | FRONT **right strip** (product frame), away from the MAIN buck/inductor (under the left strip) (06-K7); ≥10 mm from the IR LEDs / ICR; acoustic port on the FRONT | P-19, P-27 |
| USB-C and u.FL | **on opposite edges** (module rotation constraint, see 14.); USB-C 4 THT shell legs; **module ↔ USB-C clearance ≥2 mm** after the extended solder pads (module shifted 1 mm towards the edge opposite the USB-C, 3.1; 06-K8). ~~The TVS + USB ESD + shield RC sit on the MAIN back side, next to J1~~; VBUS goes on ≥2 vias to the front-side eFuse (4.1). **As-built (final):** J1 on the right edge (B), J4 on the left edge (B) – opposite edges ✅; module pad ↔ J1 copper clearance **1.53 mm** (< 2 mm, dfm-08, accepted); the J1 front face is 0.55 mm behind the edge (plug fit to be checked with the G3 mock-up); **the D1 TVS on the B side under the eFuse (U3), 6.8 mm from J1 (accepted deviation, §0.1); the U5 USB ESD and the R1 / C1 shield RC on the F side, next to J1**; 3 VBUS vias to U3 IN (J1 → U3.5 7.1 mΩ) | P-25, A-34, K-10, R4-21 |
| u.FL | at the board edge, strain relief; antenna: external FPC antenna, ≥15 mm from metal, early RSSI test. **Rev A: if the module's own IPEX is usable, we use it; every element of the u.FL / π-network / CPWG footprints is 0 Ω / DNP-capable; 2 antennas, RSSI on the dev kit** (G0/G2) | P-11, P-12, K-6 |
| microSD | at the board edge, away from RF; **rev A: DNP (footprint stays)** | P-32, K-16 |
| Buck | in the corner opposite the u.FL and the microphone | P-27 |
| Panelisation | tab-route + mouse bites, 3 fiducials, boards separate. **As-built (round 9):** there are no fiducials on the board → single board **with JLC rails only on the top and bottom edges** (the rails carry the fiducials); **no tab / V-cut on the right edge at y > 5.8 mm and on the top edge between x 10–35 mm** (C3 / R10 / C1 are 0.7–0.8 mm from the right edge); mouse bites outside the outline, ≥1 mm from via rings | P-34, dfm2-02 |
| Silkscreen | pin 1, FPC contact side, "no hot-plug" label (SD/FPC/B2B), test point names. **As-built (2026-10-11):** silk DRC 0; B: "ESP32-P4-CAM MAIN", "rev A 2026-10", "USB-C PD 9V", "no hot-plug of FRONT", TP net names, BOOT / RESET / USER; F: J2 / J5 pin-1 "1", "R16→", JLC order-number placeholder (x 22.3–32.5, y 13.8–15.0 – at order time "specify location" or delete) | P-37, E-30 |
| JLC DFM | availability of header (7 mm), FPC connector, u.FL, USB-C THT to be checked. **2026-10-11: all can be assembled at JLC (`07` §0); J2 stock is 31 pcs (reserve them); there is no 7.00 mm B2B pair (Q17); the J1 shell legs need hand / selective soldering (§3.1)** | P-35 |
| First prototype | 1:1 paper/3D-print mechanical mock-up **before** the schematic (footprint mirroring, pin 1) | P-3, P-22 |

### 3.1 EDA, manufacturing process and module soldering (K-10, K-18)
| Topic | Decision / requirement |
|---|---|
| EDA tool | **KiCad** (owner decision, 2026-10-09). To do: JLC ~~2-layer 1.0 mm~~ **4-layer (v0.6: `scripts/project_rules.py` + `.kicad_dru`)** DRC rules, import the Waveshare footprint + 3D STEP into our own library, LCSC fields in the symbols (BOM → 07), field solver: KiCad PCB Calculator. Requirement: JLC/LCSC part import, own footprint (Waveshare module), 3D STEP export for the mechanical check (06) |
| KiCad project (2026-10-09) | `kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pro`; shared library `kicad/lib/ESP32-P4-CAM.{pretty,kicad_sym}` (`${KIPRJMOD}/../lib`). Sheets: 01_tap, 02_p4_modul (U1), 03_kamera, 04_prog_tp, 05_b2b_front, 06_sd. PCB **(v0.6 as-built): 45×45 mm, R1 corners, 4 layers, 0.97 mm** (JLC04101H-3313A); netclasses per 3313A: CSI 0.204/0.203, USB 0.262/0.203, RF 0.302, PWR 0.4, PWR_LIGHT 0.3, Default 0.15; JLC 4L minimums (track 0.09, drill 0.2, via 0.45) – §3.2. ~~60×50 mm, 1.0 mm, 2 layers, CSI_DIFF 0.30/0.20, RF_50 0.70, PWR 0.60~~ (archived). ~~The netclass width is not enforced in the DRU (round 7)~~ → **round 8: `.kicad_dru`: PWR ≥0.4 / PWR_LIGHT ≥0.3 mm warning rule (37 hits, accepted), CSI intra-pair skew ≤0.1 mm, PWR zones ≥1 mm from the board edge**; no CSI length, RF or USB geometry rule (rev B) |
| MAIN coordinates | **→ §3.1a (as-built, frozen).** ~~45×45 "core" = x 0–45, y 2.5–47.5 (centre 22.5; 25); extra strip x 45–60; "the FRONT uses the same core"~~ – the outline of the 45×45 board is x 0–45, **y 0–45**; the M2 holes stayed at the old 60×50 coordinates (`place45.py` skipped them), so the grid is asymmetric by 2.5 mm. **The FRONT copies the MAIN outline and hole coordinates 1:1**, not a symmetric "core" |
| Power ICs locked (E22, 2026-10-09, from the datasheets) | **PD: CH224A** (LCSC C42459160, ESSOP10; the CH224K is *Discontinued* at LCSC; the CH224D has no I2C). Rset CFG1→GND **6.8 kΩ = 9 V**; VBUS pin ↔ VHV; VHV 1 µF; **I2C 0x22/0x23** (CFG2=SCL, CFG3=SDA, internal 10k pull-up, VIH 1.5–3.3 V) → reg 0x09 protocol status, 0x50 current (×50 mA) → **B-4 solved**; PG open-drain, active low; DP/DM NC; abs max DP/DM/CFG1 3.8 V. **eFuse: TPS259470ARPW** (adj. OVLO, active ILIM, auto-retry, FLT; 2.7–23 V, abs 28 V; reverse blocking): UVLO/OVLO threshold 1.20 V↑ / 1.09 V↓ → R6/R7 = 267k/100k → **4.40 / 4.00 V**; R8/R9 = 80.6k/10k → **OVLO 10.87 / 9.88 V**; R10 RILM 1.65k → **2.03 A** (min 1.80); CdVdt = 2000/SR[V/ms] → 1 nF = 2 V/ms. **Buck: TPS62933F** (FCCM, 3.8–30 V, 3 A, SOT583): RT→GND 1.2 MHz, Vref 0.8 V → R14/R15 = 31.6k/10k = **3.33 V**, CSS 10 nF (min 6.8 nF), BST 100 nF, L 2.2 µH, COUT TI recommendation 30 µF eff. (min 10). Source: `ref/datasheets/` |
| Module footprint (E21) | `Waveshare_ESP32-P4-Module`: **from the Waveshare land pattern DXF** (`ref/waveshare-land-pattern/`): 88 pads **1.5×0.7 mm**, mask 1.6×0.8 (+0.05), paste = pad, 1.0 mm pitch, pad-centre frame 25.0 mm, outer 26.5 mm. Numbering verified against the Waveshare pinout image (top view, CCW: P1 top-left → P22 bottom-left → P23–P44 along the bottom → P45–P66 right side upwards → P67–P88 along the top). **Hand-soldering variant (K-10) done:** `Waveshare_ESP32-P4-Module_HandSolder` – copper+mask pad extended +1.5 mm beyond the module edge (2.25×0.7 mm), paste the original 1.5×0.7; courtyard ±14.25. **Placed (v0.6 as-built): U1, B.Cu, (20.5; 25.0), 0°** (2 mm to the left of the 60×50 position (22.5; 25)) → USB P50/P51 towards the right edge (J1), CSI P41–P46 towards the top-right corner (J2), RF P2 (7.625; 34.5) towards the bottom-left (J4). Round 7: all 88 pads of the lib match the DXF within 0.0002 mm, pin 1 correct |
| JLC process | **v0.6: 4-layer, JLC04101H-3313A, 0.97 mm** (§3.2); the JLC 4L minimums are met (round 7: track ≥0.10, clearance ≥0.15, annular ring ≥0.125 mm). ~~The board file has no stackup block, the gbrjob carries the KiCad default~~ → **round 8: stackup block in the board file (3313 0.107 + 1080 0.0764 / core 0.5, Cu 35 / 15.2 / 15.2 / 35 µm), ENIG, dielectric_constraints, Rev A; the gbrjob: ENIG, ImpedanceControlled, Rev A, 0.9872 mm**; nevertheless, specify on the order form by name: JLC04101H-3313A, impedance control, ENIG, 45 × 45 mm (not the 45.1 of the gbrjob). Hole spacing: different net min. 0.408 mm, same net 0.253 mm (rule 0.25 ✓; JLC DFM may flag it). **Pre-order gate (round 9, mandatory; the saved zone fills are stale → plotting without a refill gives GND shorts):** (1) on the `kicad/MAIN` board to be ordered, with the `.kicad_pro` + `.kicad_dru` next to it: `kicad-cli pcb drc --refill-zones --save-board --schematic-parity --severity-all` (or GUI: Fill All Zones + Save); (2) DRC without refill: **0 errors / 12 unconnected (DNP) / parity 0**; (3) `copper_diff.py` (review work script, not in this repository) against the review snapshot: 0 copper differences, 0 stale fills; (4) `kicad-cli pcb export gerbers --check-zones …` + `export drill --excellon-separate-th`, In2 in a Gerber viewer; (5) update the order package (`kicad/MAIN/fab/`). **Refilling / saving outside the project folder is forbidden** (the 1 mm edge rule of the DRU is lost). ~~2-layer, 1.0 mm~~ (archived) |
| Impedance | v0.6: the 3313A stackup with widths per the JLC calculator (§3.2); impedance control as an order option. ~~JLC 2-layer manufacturing has no impedance control, ±10–20 %~~ (applied to the 2-layer design); in rev A, RSSI + image stability validate it |
| Double-sided SMT | JLC assembles both sides (cost ↑; **Standard PCBA**); the P4 module by hand. **As-built: 72 fitted items, F 47 / B 25 (CPL 72 rows)**; U1, MH1–4, TPs, JP1 and every DNP excluded. ~~Fitting the USB-C THT shell legs (JLC vs hand) is an open question~~ → **the 4 shell legs of J1 (plated slots, (37.67 / 41.85; 18.18 / 26.82)) have no paste and J1 is `attr smd` → probably unsoldered after reflow; the power input would be held only by the 16 SMD pads (~10.2 mm²)** → at order time: JLC hand / selective soldering, **or** the owner solders them from the F side before the first cable insertion (fine tip, little solder; afterwards check the 0.757 mm gap to the C1.2 GND pad) – §15 |
| **Module soldering (K-10)** | castellated module, **soldering iron + flux** (+ preheater / hot-air); on the MAIN the module pads are **extended outwards by ≥1.5 mm** (the fillet is accessible); **mask / keep-out under the module**: no exposed Cu / via under the module (except an intentional GND pad), solder-mask dam between the pads; the module footprint is therefore **28×28 mm** (06); the **module ↔ USB-C distance increases** (≥2 mm from the pad extension; module 1 mm offset). **As-built deviation (final):** 105 vias (33 GND, 72 signal) and 290 B segments run under the module body (all tented; per the DXF there is no centre pad – low risk, dfm-14); module ↔ J1 1.53 mm. **Hand-soldering risk (since round 8):** the pads of C21–C23 (B) are 0.5 mm from the P83–P86 pad tips, **C23.1 (+3V3) is 0.525 mm from the tip of P87 (ESP_EN)** – a bridge means no EN delay and SW2 (RESET) becomes a 3V3–GND short; the tip of RF P2 is 1.82 mm from R34.1 → **fine conical tip on P83–P88, then inspect P87/C23 and R34/J4 + TP16A ↔ TP4 measurement (§15)** |
| Trial soldering | at least one of the 3–4 modules goes to a soldering trial (§0.3) |

### 3.1a MAIN as-built mechanical interface (v0.6, measured from the PCB, 2026-10-10) – **FROZEN towards the FRONT and the enclosure**
Coordinates: KiCad frame, mm – origin at the top-left corner of the board, X to the right, Y **downwards**, viewed from the F (camera / FRONT) side; the B-side components are also given in this frame (transparent view). Conversion to the product frame of 06 (front view, Y up): x unchanged, y₀₆ = 45 − y.

| Element | Side | Position / rotation | Note |
|---|---|---|---|
| Board outline | – | (0; 0)–(45; 45), R1 corners; 4 layers, 0.97 mm | board centre (22.5; 22.5) |
| MH1–MH4 (M2 standoff) | NPTH | (5.75; 8.25), (39.25; 8.25), (5.75; 41.75), (39.25; 41.75); Ø2.2; ~~mask opening Ø3.2~~ → stock `MountingHole_2.2mm_M2`, mask opening = hole (Ø2.2) | grid 33.5 × 33.5, **centre (22.5; 25.0) – 2.5 mm below the board centre** (8.25 to the top edge, 3.25 mm to the bottom edge; the hole edge is 2.15 mm from the bottom edge). Keep-out rule area r 1.75 (tracks/vias forbidden, components not); ~~the hole footprint has no courtyard (dfm-09)~~ → courtyard r 2.45 (F only; DRC 0 courtyard overlaps); on F the nearest fitted component is ≥2.87 mm away (a 4 mm hex standoff, r 2.31, fits). **Washer: nylon on MH1 / MH2 / MH4, none on MH3 (screw head max. Ø4.0)** – §3 |
| J5 B2B 2×10, 1.27 mm | F | (22.5; 40.2), 90° – horizontal, along the **bottom edge**; pin 1 (16.785; 42.15), pin 2 (16.785; 38.25), pin 19 (28.215; 42.15), pin 20 (28.215; 38.25) | odd row towards the edge (y 42.15), even row y 38.25; courtyard x 15.6–29.4, y 35.9–44.5. The FRONT mate sits at the same X/Y on the FRONT B side – mirroring / pin 1 on a paper test (P-22). ~~Footprint generic, no type (Q17)~~ → **BOM: Hong Cheng HC-PZ127-7.2L-2x10PS (C41375929)**, FRONT socket: HC-PM127-4.3H-2x10PS (C27985222) – 5.3 mm mated height → ~2.3 mm engagement at a 7.0 mm gap [UNVERIFIED]; the land is generic (`PinHeader_2x10_P1.27mm_Vertical_SMD`); **Q17 open** (with Samtec 7.47 mm: MAIN footprint swap + 7.5 mm standoff before ordering) |
| J2 camera FPC 15 pin, 1.0 mm | F | (22.5; 7.5), 180° – **top edge**; contact row y 9.3: pin 1 (29.5; 9.3) → pin 15 (15.5; 9.3); retention pads (12.51 / 32.49; 6.5) | actuator and cable entry from the top edge (courtyard y 0.46–10.85, x 10.5–34.5) → the FFC exits at the top edge, through the ~28.9 mm window between MH1–MH2; in a closed stack a ~180° fold-back, ~4–5 mm outside the outline (estimate, G3). ~~Footprint placeholder~~ → **part = footprint: TE 1-84953-5 (C5164008, TOP contact, slide lock; JLC stock 31 pcs – reserve them)**; contact side **Q6** before the first camera power-up (wrong side = 3V3/GND swap at the camera) |
| J1 USB-C 16 pin (HRO TYPE-C-31-M-12) | B | (40.8; 22.5), −90° – **right edge**, opening towards +X | signal pads x 36.755; THT shell legs (37.67 / 41.85; 18.18 / 26.82) – they also occupy space on the F side; front face x ≈ 44.45 (0.55 mm behind the edge); courtyard x 35.5–45.0, y 17.1–27.9 |
| J4 u.FL | B | (3.0; 38.3), −90° – **left edge**; centre pin (3.0; 36.775) | immediate neighbour of the MH3 screw head (no room for a washer, mech-10: the J4 GND pad is 2.54 mm and its courtyard 1.87 mm from the MH3 centre) → **MH3: no washer, screw head max. Ø4.0 mm, the u.FL cable exits towards W / N**; RF: U1 P2 (7.625; 34.5) → R34 (3.9; 34.5) → J4 |
| J7 C6/UART0 pad row 1×9, 1.27 mm (DNP) | B | (22.5; 2.0), 0° – **top edge**, horizontal; pin 1 (17.42; 2.0) → pin 9 (27.58; 2.0) | pad 0.85×1.6; pinout: §6 J7 table |
| SW1 BOOT / SW2 RESET / SW3 USER (Omron B3U-1000P) | B | (11.5; 3.0) / (33.5; 3.0) / (33.5; 7.4) | top edge; the enclosure pinholes follow these (§18) |
| D20 status LED (0603, green) + R30 1k | B | D20 (3.2; 14.35), R30 (3.2; 16.05) | left edge; light pipe in the enclosure (§18) |
| U1 P4 module | B | (20.5; 25.0), 0° | courtyard x 6.2–34.8, y 10.7–39.3 |
| J3 microSD (DNP) | F | (9.0; 25.0), −90° – left edge | rev A DNP; an inserted card protrudes ~4.8 mm (mech-14) |
| Test points | B | §12 | the pogo jig is built from the coordinates in §12 |

**Change compared with the earlier plan:** 60×50 / 2 layers → **45×45 / 4 layers**; the symmetric "45×45 core (y 2.5–47.5)" is gone, the holes stayed at the old coordinates → grid centre (22.5; 25.0); U1 (22.5; 25) → (20.5; 25.0); J5 **horizontal along the F bottom edge** instead of vertical (x 40.5) (the FRONT follows this); J1 on the right edge of the 45×45 instead of the extra strip; J7 a **horizontal SMD pad row on the top edge** instead of the vertical header at the top-left; pogo group 20 → 12 pads; SW1–3 → B3U-1000P (3.0×2.5 mm). **This interface is the input for the FRONT (G6) and the enclosure; it can only be changed together with the FRONT.** Check: 1:1 printed stack mock-up (G3).

**Final as-built (2026-10-11, review snapshot):** round 8 moved none of the interface elements above (outline, MH, J1, J2, J4, J5, J7, SW1–3, D20/R30, U1, J3 – re-measured, they match). Moved (not interface): **C4 → B (42.9; 16.2)**, **C14 new, F (42.675; 16.0)**, C3 (43.5; 9.45), R10 (43.8; 12.75), C1 (43.8; 26.75) −90°, U4 (29.4; 25.74), L1 (31.4; 30.02) −90°, the buck caps / R14–R16, **C20–C23 under P84–P86** (B, y 40.75–42.4), R27 (7.3; 37.93), C50 (2.75; 11.0) and DNPs (R4, R36, C29, C30, C71, R73) – full list: `06` "As-built placement". 128 footprints (124 components + MH1–4), 38 DNP; 72 fitted (F 47 / B 25).


## 3.2 MAIN 4-layer build-up (v0.6, 2026-10-09 – owner decision, browser-verified)
Source: jlcpcb.com/impedance and jlcpcb.com/pcb-impedance-calculator (4 layers, 1.0 mm, outer 1 oz, inner 0.5 oz; the calculator's first, "cheapest, fastest" offer).

| Layer | Material | Thickness | Role |
|---|---|---|---|
| L1 (F.Cu) | Cu 1 oz | 0.035 | signals + components (front side) |
| prepreg | 3313 (0.107) + 1080 (0.0764) | 0.183 | |
| L2 (In1.Cu) | Cu 0.5 oz | 0.0152 | **continuous GND plane** (no cuts) |
| core | | 0.5 | |
| L3 (In2.Cu) | Cu 0.5 oz | 0.0152 | power (VBUS / VBUS_SW / 3V3 islands) + slow signals, remaining GND pour |
| prepreg | 1080 + 3313 | 0.183 | |
| L4 (B.Cu) | Cu 1 oz | 0.035 | module (back side) + signals |

Finished thickness 0.97 ± 0.10 mm (JLC04101H-3313A).

| Impedance (L1, ref. L2) | Width | Gap |
|---|---|---|
| 50 Ω single-ended (RF, if on F.Cu) | 0.302 mm | – |
| 100 Ω diff. (MIPI-CSI) | 0.204 mm | 0.203 mm |
| 90 Ω diff. (USB FS) | 0.262 mm | 0.203 mm |

The reference of the L4 (B.Cu) signals is L3: under CSI / RF / USB a **GND pour** on L3 is mandatory (no power island underneath), otherwise the impedance does not hold. At layer changes, a GND via next to the signal via. **MAIN size: 45×45 mm** (common interface with the FRONT – M2 grid, J5, J2 – as-built: **§3.1a**; the grid is not symmetric about the board centre). Price: **[UNVERIFIED]** (the surcharge for a small 4-layer board is expected to be a few USD).

## 4. Power tree + current budget

### 4.1 Power tree
```
USB-C VBUS (max 9 V) ─ TVS (SMAJ10A; as-built D1: B side, at the eFuse input, 6.8 mm from J1) + USB ESD (as-built U5: F, next to J1) ; 3 vias to U3 IN ─ ≤10 µF EFFECTIVE (CH224 caps + TVS Cj count too) ─ eFuse (adjustable OVP ~10.5–11 V,
        │                reverse-blocking, auto-retry, UVLO ~4.4 V rising / ~3.9 V falling, ILIM ~2 A, soft-start) ─ VBUS_SW ─┬─ C14 1 µF/25 V on U3 OUT + bulk ≤47 µF eff. (plan: 35–50 V MLCC; as-built 25 V: C5/C6 22 µF, C8 10 µF)
        │                (around the eFuse: 0 Ω / solder bridge VBUS→VBUS_SW, DNP – bypass, K-1)                              ├─ BUCK 3V3 (forced-PWM, ≥2 A, 2.2 µH Isat ≥3.5 A) ─ 0 Ω ─ 3V3 rail (TP4 = bench feed-in, if the 0 Ω is open)
        │                                                                                                                     │     ├─ P4 module ESP_3V3 + VBAT (47 µF + 10 µF + 100 nF at the P84–P86 pads)
        │                                                                                                                     │     ├─ CAM_3V3 ← load switch (TPS22918 class, mandatory) → camera module
        │                                                                                                                     │     ├─ SD_3V3 ← load switch (with discharge) (rev A: DNP)
        │                                                                                                                     │     ├─ ICR H-bridge (FRONT, from 3V3, never from VBUS_SW; rev A: DNP) + microphone (LC, FRONT)
        │                                                                                                                     │     ├─ VEML7700 (FRONT, via the J5 3V3 pin; rev A: DNP) + NTC divider (MAIN, ADC2, GPIO 49)
        │                                                                                                                     │     ├─ status LED (MAIN back side, driven by GPIO 6, series R; not on J5)
        │                                                                                                                     │     └─ supervisor (TPS3840 class, open-drain) → 0 Ω → ESP_EN (rev A: DNP)
        │                                                                                                                     ├─ VBUS_SW ADC divider (200k/54.9k + 100 nF; 3.6 V Zener D2: DNP) → GPIO 20
        │                                                                                                                     └─ IR branch: 2nd eFuse (≥18 V, adjustable ILIM 0.5–0.7 A) + shunt (TP8) – rev A: DNP, footprint stays → IR_VIN → B2B → FRONT IR drivers
        ├─ raw VBUS (after the TVS, BEFORE the eFuse) ─ CH224A VDD (+ CH224 caps, within the ≤10 µF effective budget)
        └─ CC1/CC2 ─ CH224A (internal Rd; NO external Rd – the 2× 5.1k footprint is DNP, only without CH224A, never both at once) ; PG → GPIO 31 ; CC-tap ≥100k series → GPIO 21/22 (rev A: DNP)
```
**VBUS transfer back side → front side:** between J1 / TVS (back side) and the eFuse (front side) VBUS goes through **≥2 vias** (3–4 recommended; ILIM ~2 A → ≤1 A/via, Ø0.3 mm via ≈ 1 A [UNVERIFIED]); the GND return through the same number of vias, the TVS + ESD ground on the J1 GND (13.1). The CH224A VDD is powered from the raw VBUS (after the TVS); VDD range / 9 V capability from the datasheet [UNVERIFIED – Q13].
**As-built (final, round-9 measurement):** J1 A4/B9 → 2 vias + a direct 0.8 mm B-side connection to D1.1; A9/B4 → 2 vias; **3 vias (0.6/0.3) on U3.5 IN**, 2 vias on U3.6 OUT; DC J1 → U3.5 **7.1 mΩ**, U3.6 → U4.3 **22.95 mΩ**. The VBUS In2 zone is a single island (138.6 mm²), but its N–S neck is 1.05 mm, then ~0.55 mm next to a GND via (parallel B-side path – electrically negligible). The VBUS_SW In2 zone is a single island (147.5 mm²), but 12 foreign In2 nets cut through it → it only partly works as a plane (the current flows on the 0.5 mm In2 track and F/B links). J1 GND: 2 vias per pin pair. **The D1 TVS is not at J1 but at the eFuse input (6.8 mm; TI TPS25947 8.4.1: protection next to the protected device) – accepted rev A deviation.** The U5.3 (USB ESD GND) pad has no via of its own (nearest GND via 1.96 mm; rev B: ≤0.5 mm). **C14 1 µF / 25 V** on U3 OUT (1.14 mm from U3.6, its GND on the same F island as U3.8); there is no 100 nF on U3 IN (C3 4.7 µF is 2.9 mm away, on another F GND island) – rev B.

**No 2nd power input** (no bench supply / 5 V pin / PoE: avoiding back-feeding and conflicts; E-35). The only power path is USB-C.

| Rule | Value / decision | Ref |
|---|---|---|
| VBUS max | **9 V** (PD 9 V request, 5 V fallback). "5–12 V" **removed** from every section; there is no 12 V profile | B-11, A-20 |
| CH224A voltage strap | **with a fixed resistor to GND/the appropriate config pin, never floating** (floating strap → may request 20 V); **with a wrong / floating strap a 20 V PDO may also arrive – the eFuse OVP does not catch this: the TVS (SMAJ10A) sits *before* the eFuse, it is the first element of the chain, and it is the one that fails first** → the correctness of the strap is confirmed by the G1 bench test (MacBook, cheap PD charger, USB-A→C cable; 9 V PDO, PG polarity / level, DP/DM NC alongside USB-JTAG). Strap table from the CH224A datasheet **[UNVERIFIED – Q: CH224A datasheet]** | B-13 |
| CH224A readout | **I2C (0x22/0x23)**: reg 0x09 = protocol status (PD/QC/BC/EPR active bits), reg 0x50 = max. current of the current PD profile ×50 mA ~~→ the FULL/MID/LOW mode can be read directly; PG → GPIO 31 remains as a fallback~~ (E22; B-4 ✅). **Rev A FW rule (round 9, electrical2-02): the PD mode is given by PG (GPIO 31) + VBUS_SW ADC (GPIO 20); the CH224A is read only after CAM_3V3 is switched on (or not at all), and never written; I2C 100 kHz.** Reason: the shared bus only has the CH224A internal pull-ups (R31/R32 DNP), and the switched-off camera (CAM_3V3 ≈ 0 V because of QOD) can pull the bus down through its clamp diodes; in TP4 bench mode (no VBUS) the CH224A is unpowered → no pull-up. G1: the open-circuit voltage of CFG2/CFG3 must be ≤3.3 V |
| **External Rd FORBIDDEN** | Per the WCH reference circuit the CH224A works without an external Rd, connected directly to CC (E22; internal Rd) → **we do not add an external 5.1k** on CC (double Rd = wrong Rp level, PD negotiation). **Exception (K-1, rev A debug only):** 2× 5.1k Rd footprint, DNP – **may be fitted only if the CH224A is not fitted; never both at once** (silkscreen: "NEVER BOTH") | B-5, K-1 |
| CC-tap (ADC) | **≥100k series** → 10 nF at the ADC pin → 3.6 V Zener clamp (not BAT54S to 3V3: no pumping). The 10 nF and the 100k do not load the PD BMC (the old 1k + 100 nF AC load **removed**). The CC-tap is **only for non-PD 5 V current sensing** (Rp level); during PD the CC toggles → not used for mode selection. The series tap draws no DC current from CC (the ADC input is high-impedance); the error comes from ADC and Zener leakage × 100k, to be checked [UNVERIFIED]. **Rev A: the CC-tap parts are DNP** (K-15) | B-3, B-6, K-15 |
| CH224 DP/DM | **NC** (E22: DP/DM are needed for BC1.2; left NC, only the BC1.2 detection is lost; this way it does not conflict with the USB-JTAG D±); bring-up test (15. step 1) **[ – Q: CH224A datasheet]** | B-7 |
| VBUS monitor | divider **from VBUS_SW (after the eFuse)**, ≥200k/54k (9.45 V → ~2.0 V), 3.6 V Zener + 100 nF; not from the raw VBUS with the TVS (back-feeding, 4.25 V clamp). **As-built: R12 200k / R13 54.9k / C7 100 nF; the Zener (D2) is DNP (2026-10-10)** – its leakage at the 43 kΩ node would distort the 8 V mode threshold (§0.1) | B-23 |
| TVS | **SMAJ10A class**: standoff 10 V; leakage at 9.45 V/85 °C to be checked; clamp vs eFuse abs-max reconciled [UNVERIFIED – datasheet]. **With a 20 V PDO (strap fault) the TVS fails first** (G1). **As-built: D1 = Diodes SMAJ10A-13-F (C134939), B side, under U3 (40.5; 13.5) – 6.8 mm from J1 (accepted deviation); pad 1 = cathode = VBUS (check in the JLC preview)** | B-12, K-4 |
| eFuse | **adjustable OVP ~10.5–11 V**, **reverse-blocking** (after a hard reset VBUS_SW must drop to 0 without back-flow, vSafe0V check), **auto-retry**, **UVLO ~4.4 V (↑) / ~3.9 V (↓)**, **ILIM ~2 A**, soft-start; ~~TPS25947 / TPS2595x class [UNVERIFIED: specific type, Q13]~~ → **TPS259470ARPWR (C3662799)**: UVLO 4.40 / 4.00 V, OVLO 10.87 V, ILIM 2.03 A (§3.1) | B-9, B-11, B-20 |
| **Capacitance budget** | **≤10 µF effective before the eFuse** (CH224 caps, TVS Cj, ESD Cj count too). **VBUS_SW total effective C ≤47 µF** (PD slew ~30 mV/µs × C → stays below ILIM: 47 µF ≈ 1.4 A [UNVERIFIED]; the 100 µF = 3 A > ILIM **removed**). Counted in: buck input, IR switch/driver inputs, B2B local 10 µF + 100 nF. **35–50 V MLCC** on the VBUS side, effective C to be specified under DC bias (9.45 V) (e.g. 10 µF/50 V 1206 → ~3–5 µF [UNVERIFIED]). **As-built: 25 V MLCC on the VBUS_SW side** (C5/C6 22 µF 1210, C8 10 µF 0805, C14 1 µF 0603; nominally ~55 µF, less after DC bias at 9 V [UNVERIFIED] – confirmed by the attach-current measurement of bring-up step 1) – accepted deviation from the 35–50 V rule given the 10.87 V OVLO; before the eFuse C3 4.7 µF / 50 V and C2 1 µF / 50 V | B-10, B-28, B-29, E-2 |
| Buck L/Cout | range check against the datasheet of the selected buck (calculation: `07` §2) | B-27 ⏳ |
| **Bring-up / debug power path (rev A, K-1)** | (1) **VBUS→VBUS_SW 0 Ω / solder bridge** around the eFuse (DNP): if the eFuse fails, the rest of the chain can still be tested; (2) **2× 5.1k Rd** (DNP, only without CH224A); (3) **TP4 = 3V3 bench feed-in**: with the buck output 0 Ω removed, the 3V3 rail can be powered from the lab (**never at the same time as USB**). Silkscreen: "NEVER BOTH". Not present in the product (rev B) | K-1 |

### 4.2 IR branch (D9)
| Element | Requirement |
|---|---|
| Supply | **a separate, second adjustable-ILIM eFuse (≥18 V rating, TPS2595x class [UNVERIFIED]) on the MAIN, ILIM 0.5–0.7 A**: an IR short/overcurrent does not reset the system (instead of a shared ILIM). The TPS22810 class **has no adjustable ILIM [UNVERIFIED]** → rejected. **Rev A: the whole IR branch is DNP** (2nd eFuse / high-side switch, shunt, TP8, IR_SW_EN pull-down; the footprint stays, IR_VIN unpowered until G6). Alternative (may be considered until rev B): fused 0 Ω (fused 0 Ω / PTC footprint). **Current shunt + TP8 on the MAIN *front* side, next to the IR eFuse** (a TP on the FRONT would be inaccessible; outside the back-side pogo group) |
| Driver input range | the IR driver on the FRONT must operate at **Vin = 4.5 … 9.45 V** |
| Headroom criterion | **Vin_min − Vsense ≥ Vf_max(−20 °C) + 0.3 V** (for series LEDs Σ Vf). If it is not met at 4.5 V for 2 LEDs in series (≈4.0 V load) → **single (1-LED) branches** with buck-CC, or **low-dropout CC** (≥95% duty / LDO mode). The "2×2 LED series" stays only if the criterion is met [Vf_max UNVERIFIED – LED datasheet] |
| Dimming | **series NFET (AO3400 class)** with PWM, **Cout ≤1 µF** at the LEDs (the 10–22 µF at the LED anode **removed**: switched at 20 kHz it causes a current-buffer error); the large caps go to the **driver input** (within the 47 µF VBUS_SW budget) |
| PWM frequency | **LEDC ≥40 kHz** (avoiding PDM microphone aliasing); IR_PWM and PDM CLK separated by GND on the B2B |
| Pull | IR_PWM, ICR_IN1/2 (and SD_EN, CAM_3V3_EN, IR_SW_EN): **100k pull-down (CAM_3V3_EN: 10k, 2026-10-10) on the MAIN – as-built on the front side, under the module / next to the target IC** (against floating during boot; K-7: the MAIN also works without the FRONT, hence not on the FRONT) |
| Eye safety | **LED current ceiling = PCB-level requirement** (limited in hardware by the shunt/ILIM/driver, not only in FW); IEC 62471 at enclosure level (18.) |
| Components | LED: 850 nm 3535 [UNVERIFIED – specific type Q13/BOM]; driver: buck-CC class [UNVERIFIED]; NFET: AO3400 class |
| Bench test (K-19) | the IR test needs a **shielding tube / window spacer** on the bench (so that the LED light does not shine into the lens / the eye; to avoid image and AE oscillation); eye safety: the LED current ceiling is in hardware |
| ICR | H-bridge (DRV8837 class) **from 3V3 (or an LDO), never from VBUS_SW** (VM max ~11 V, but 9.45 V + spikes are not wanted) [UNVERIFIED]; **FW pulse limit 50–100 ms** + **series current limit** (resistor) to protect the coil; coil data from the ICR lens datasheet (Q5) | **Rev A: DNP** (K-5; ICR rev B) |

### 4.3 Current budget and power modes (one set; estimate **[UNVERIFIED]**, to be refined by measurement – E-33, F-18; **replaced by the G0 measurements**)

Calculation basis: **VBUS 4.5 V** (worst case: cable drop + above UVLO), **buck η = 0.82**, IR branch input power 1.2 W (2 branches × 150 mA, ~3.4 V/branch, CC η≈0.85).

| Consumer | Rail | Typical | Peak |
|---|---|---|---|
| P4 (stream + H.264) | 3V3 | 250 mA | 400 mA |
| C6 WiFi TX | 3V3 | 100 mA | 350 mA |
| Camera module (own LDOs) | 3V3 | 120 mA | 200 mA |
| microSD write | 3V3 | 50 mA | 100 mA |
| other (mic, LED) | 3V3 | 20 mA | 30 mA |
| **3V3 total** | | **540 mA = 1.8 W** | **1080 mA = 3.6 W** |
| Buck input (η=0.82) | VBUS_SW | 2.20 W | 4.39 W |

| Operating state | Power (VBUS_SW) | I @ 4.5 V | I @ 9 V | Note |
|---|---|---|---|---|
| **Day, typical** (IR off) | 2.20 W | 0.49 A | 0.24 A | |
| **Day, peak** (WiFi TX peak, SD write, IR off) | 4.39 W | **0.98 A** | 0.49 A | daytime peak column |
| **Night, typical** (IR on) | 3.40 W | 0.76 A | 0.38 A | |
| **Night, peak** | 5.59 W | **1.24 A** | 0.62 A | |
| **MID** (5 V/1.5 A source): IR ≤50% (0.6 W), WiFi TX cap (~200 mA) | ~3.9 W | 0.87 A | – | from the source 4.5 V × 1.5 A = 6.75 W; tight margin |
| **LOW boot** (camera off, SD off, IR off, TX ≤10 dBm) | 1.49 W (370 mA 3V3) | **0.33 A** | – | ≤0.5 A (USB 2.0 unit load) → boots on a PC port |
| **LOW peak** (camera 720p on, WiFi cap TX ≤10 dBm ~180 mA, no SD/IR) | 2.82 W (700 mA 3V3) | **0.63 A** | – | > 0.5 A → **PC = best effort** (OK on USB 3.x/BC1.2 hosts; brown-out possible on USB 2.0 hosts) |

For the thermal calculation: input peak 5.6 W → heat load in a closed enclosure **~4.5–4.9 W** (11.).

**Firmware power modes (B-2, B-3, B-17, B-19, E-11, E-12, F-3)**
| Mode | Condition | Behaviour | Minimum source |
|---|---|---|---|
| **FULL** | **VBUS_SW ≥ 8 V** (PD 9 V) **or** non-PD Rp = 3 A (CC ADC 1.31–2.04 V) | all functions, IR at full (up to the thermal limit) | **PD 9 V / ≥1.0 A** (night peak 0.62 A @9 V + margin; recommended 9 V/2 A) **or** non-PD **5 V / 3 A** (night peak 1.24 A @4.5 V) [UNVERIFIED; G0] |
| **MID** | non-PD Rp = 1.5 A (CC ADC 0.70–1.16 V) | **IR ≤50%**, WiFi TX cap, 1080p30 kept if thermals allow | **5 V / 1.5 A** (non-PD); peak ~0.87 A @4.5 V; **not in rev A** (CC-tap DNP) |
| **LOW** | default: USB/PC (Rp default, CC 0.25–0.61 V), unknown or during PD negotiation | **camera off at boot**, WiFi **TX ≤10 dBm**, **720p**, **SD off, IR off**; enough for programming/debugging; **PC = best effort** | **5 V / 0.5 A** (USB 2.0 unit load): LOW boot 0.33 A is enough; the LOW peak of 0.63 A needs ≥0.9 A (USB 3.x / BC1.2), otherwise best effort |

Rules:
1. **Boot always starts in LOW.** The mode is decided **only after a ≥1.5 s VBUS settle** (PD negotiation takes 0.3–1 s; boot starts at 5 V, 9 V comes later).
2. The decision is **continuously re-evaluated**; on CC **median (≥8 samples) + hysteresis** (the Rp toggle during PD must not cause mode hopping). While PD is active the CC is not used, **FULL = VBUS_SW ≥ 8 V** (ADC) / PG.
3. Stepping down (FULL→LOW): VBUS ≤ 7.5 V or PG lost → IR off immediately, WiFi TX cap; stepping up only after the settle.
4. Boot sequence: P4 + C6 → VBUS/PG measurement (GPIO 20, 31; the CC ADC GPIO 21/22 **rev B / if the CC-tap is fitted**) → ≥1.5 s settle → mode → CAM_3V3 → SD (tri-state rule, 5.) → IR.
5. PD hard reset (VBUS ~0 V): the bulk does not hold through; the eFuse **auto-retries**, the system cold-starts into LOW (9. power-outage tolerance).
6. **Rev A mode logic (K-15):** boot LOW → **FULL** only if after a ≥1.5 s settle VBUS_SW ≥ 8 V (ADC + PG), otherwise LOW; the CC-tap parts are DNP, so there is no MID and the non-PD Rp branches cannot be used.

## 5. GPIO allocation (P4 module)

The "module pad" column comes from the Waveshare pinout table (**E20, primary source**; every pad filled in). Distinction: **P49 = module pad, GPIO 49 = processor pin** (different things).
**As-built check (2026-10-10):** every row compared with the nets of the PCB U1 pads and with the pin names of the schematic symbol (U1 pad n ↔ "GPIOx" pin name, per E20) – the GPIO ↔ pad ↔ net assignment **matches everywhere** (v0.6 swap: SD_EN P81, SD_CD P80, CAM_3V3_EN P19, USER_BTN P60, EFUSE_FLT P56, PDM_DATA P57). The corrections only affected the text columns (GPIO 45 row, GPIO 54 TP, ESP_EN RC, GPIO 4 pull-down, GPIO 7/8 CH224A, side of the pull-downs, UART0 / C6 TPs).

| GPIO | Module pad | Function | Pull / protection | Note |
|---|---|---|---|---|
| GPIO 24 / 25 | P50 / P51 | **USB-Serial-JTAG** D− / D+ (the only USB designation; the P48/P49 HS PHY is **not used, NC – never enabled on this layout, FS only (§6)**; the OTG FS function is not used – check in sdkconfig, Q23) | ESD **TPD2E2U06 / PRTR5V0U2X class** (3.3 V array, **no VBUS pin**; USBLC6-2SC6 removed – its VBUS pin is ~5 V rated, it fails at 9 V); shield 1 MΩ ‖ 4.7 nF | E10, E20; single USB-C; CH224 DP/DM NC |
| GPIO 35 | P62 | BOOT button | button to GND | strapping, E8 |
| GPIO 36 | P63 | BOOT_EN pull-up | 10k → 3V3 | E8 |
| GPIO 34, 37, 38 | P61 / P64 / P65 | strapping / UART0 TX,RX | **no load**; UART0 only on the **J7.7 / J7.8** pads (DNP pad row), series **R40 / R41 1k** (TP14/TP15 deleted) | E-6, E20; detailed table: 5.1 |
| ESP_EN | P87 | RESET button (SW2) **OR** supervisor output; TP16A | **R23 10k → 3V3 + C25 1 µF → GND: FIT (2026-10-10)** – the module's RC (Q3 ⏳) is unknown, a double RC only modifies the time constant; the ESP_EN route is ~95 mm (button + TP). Supervisor TPS3840 class, open-drain, through 0 Ω, wired-OR with the RESET button: **not drawn → rev B** | E-22 ⏳, B-21, K-14 |
| GPIO 7 / 8 | P22 / P23 | I2C SDA / SCL – **shared bus: camera SCCB (J2.14/13) + CH224A (CFG3/CFG2, 0x22/0x23) + FRONT (J5.19/20, VEML7700)** | pull-up in one place (MAIN, R31/R32 4.7k); **the pull-up may only be fitted once the camera I/O level is known** (1.8 V module?) – until then DNP (until then only the CH224A internal 10k pulls up); the module's own pull-up to be checked. **FW: the CH224A is only read** (a wrong write may request 20/28 V – the TVS cannot take it; electrical-05); **rev A: I2C 100 kHz, the CH224A is read only after CAM_3V3 is switched on (§4.1, §15)** | E15, E22, A-7 |
| GPIO 23 | P32 | Camera PWDN/EN (FPC CAM_IO0) | **Pull = TBD (Q5)** – depends on the PWDN/EN polarity of the selected module: with an active-high PWDN the 100k pull-down = *switched on* → in that case pull-up / GPIO control; default state = camera off, also because of the **CAM_3V3 load switch** | E-17, E-26, A-3 |
| GPIO 4 | P19 | **CAM_3V3_EN** (load switch, TPS22917) **(v0.6 GPIO swap, PCB routability)** | pull-down **10k (R28, 2026-10-10; previously 100k)** – GPIO 4 = pad-JTAG MTMS, its internal pull-up during reset [UNVERIFIED]; check: CAM_3V3 (TP5) 0 V during reset | B-22, E20, electrical-06 |
| GPIO 12 / 30 | P27 / P57 | PDM mic CLK / DATA (DATA: GPIO 13 → 30 **(v0.6 GPIO swap, PCB routability)**) → J5.13 (PDM_CLK_J5) / J5.16 | CLK series R70 47 Ω at the source (B); I2S0 PDM RX | E-16 |
| GPIO 33 | P60 | User button **(v0.6 GPIO swap, PCB routability)** | **MAIN back side**; internal pull-up + 100 nF on the pin | A-38 |
| GPIO 6 | P21 | Status LED (discrete 0603 + series R, **MAIN back side**, near the module; FIT) | series R (LED current ≤~2 mA, value: `07`) | E-34; J5.17 spare (NC) |
| GPIO 20 | P29 | **VBUS_SW monitor ADC** (200k/54.9k + 100 nF; the 3.6 V Zener D2 **DNP**, 2026-10-10) | – | ADC1; replaces the LDR |
| GPIO 21 / 22 | P30 / P31 | CC1 / CC2 ADC (non-PD 5 V current sensing only) | ≥100k series + 10 nF + 3.6 V Zener (rev A: all DNP) | ADC1; B-6. **Rev A as-built: the CC1_ADC net has no copper** (the P30 → C29/R35/D21 stub removed, §0.1) – to be connected before fitting |
| GPIO 26 | P53 | IR PWM (LEDC **≥40 kHz**) | **100k pull-down** | E-8, B-30, E20 |
| GPIO 27 / 28 | P54 / P55 | ICR IN1 / IN2 | **100k pull-down** (R25 / R26, MAIN **front side** (as-built), FIT; the ICR block is **DNP in rev A**) | E-8, E-9, E20 |
| GPIO 53 | P81 | SD_EN **(v0.6 GPIO swap, PCB routability)** (U8 TPS22917, TPS22918 class; rev A: SD DNP) | 100k pull-down (R27, front side, FIT) | E-3 – not in the VO4 domain; E20 |
| GPIO 52 | P80 | SD_CD **(v0.6 GPIO swap, PCB routability)** | pull-up to the main 3V3 (**CD only**, non-VO4 GPIO; the data-line pull-ups go to SD_3V3) | E-3, A-27, E20 |
| GPIO 31 | P58 | **PD PG** (CH224A Power-Good) – mandatory; TP17 | pull-up R3 10k to 3V3 (open-drain, active low – E22; to be confirmed by the G1 measurement) | B-4, E20 |
| GPIO 32 | P59 | **IR_SW_EN** (enable for the IR eFuse / switch; rev A: DNP) | **100k pull-down** (R29, MAIN front side (as-built); rev A: DNP with the IR branch) | B-25, E20 |
| GPIO 0 | P88 | **free** (VEML7700 INT only if J5 gets a pin for it – currently there is no free J5 pin → NC) | – | E20 |
| GPIO 1 | P16 | **free** (32k XTAL option: if used, GPIO 0 + GPIO 1 together, and then the VEML INT is lost [UNVERIFIED]) | – | E20 |
| GPIO 29 | P56 | **EFUSE_FLT** **(v0.6 GPIO swap, PCB routability)** (TPS259470A ~FLT, open-drain, active low; 10k pull-up on the power sheet, R11 – as-built B side) | – | 2026-10-09, added during schematic wiring |
| GPIO 2, 3, 5, 13 | P17 / P18 / P20 / P28 | **free** (spare; after the v0.6 swap) | – | E20 |
| GPIO 49 | P77 | **NTC ADC2** (near the buck/IR) | NTC + divider, 100 nF | B-26, E20; ADC2: GPIO 49–53 |
| GPIO 39–44 | P67–P72 | microSD D0 D1 D2 D3 / CLK CMD (**rev A: DNP**) | pull-up to the **switched SD_3V3**, ESD ≤3.5 pF | E17, E20; SDMMC slot0 IO_MUX |
| GPIO 45, 46 | P73, P74 | – (not used, VO4 domain) | NC | the default power-reset pin of the IDF SD example is GPIO 45 → **must be overridden / disabled in sdkconfig** (SD_EN = **GPIO 53**, v0.6; the earlier "GPIO 29" is obsolete); bring-up check: step 15/4 |
| GPIO 47, 48 | P75 / P76 | VO4 domain, not used | NC | E-5, E20 |
| GPIO 14–19 | – | C6 SDIO (inside the module) | – | E5 (inference), E18 |
| GPIO 54 / C6_EN (P82) | P82 | C6_EN (**reserved**; E20 has no separate C6_EN pad, P82 = GPIO 54) | **J7.6** pad (DNP pad row; TP13 deleted) | E18; **Q2**: is it also connected to C6_EN inside the module? |
| C6_IO9 | P9 | C6 BOOT | **10k pull-up to 3V3** (R21) (+ J7.4 pad: jumper/pogo pull-down for download) | E6, A-4 |
| C6_IO8 | P10 | C6 strapping | **10k pull-up mandatory** (R22; in every document); J7.5 | E6, A-31 |
| GPIO 9–11, 50–51 | P24–P26, P78–P79 | free | – | E20 |
| C6_IO13–15 | P8 / P7 / P6 | **NC** (not used) | – | E20 |
| C6 JTAG IO7..IO4 | P11–P14 | **NC** (not broken out in rev A, F-25) | – | E20 |
| DSI | P34–P39 | **NC** (not used) | – | E20 |
| GND pads | P1, P3, P15, P33, P40, P47, P52, P83 | **connect to GND** (all; verified on the PCB) | – | E20 |
| VO4 | P66 | ESP_LDO_VO4 | C24 1 µF + TP7, **external source forbidden** | E-5 |

**v0.6 GPIO swap (2026-10-09, MAIN rev A routing):** Freerouting could not complete 27–34 connections because several functions ran to a component on the opposite side of the module. Swap: SD_EN 29→53, SD_CD 30→52, CAM_3V3_EN 33→4, USER_BTN 5→33, EFUSE_FLT 2→29, PDM_DATA 13→30. The ADC functions (GPIO 20–22, 49) are unchanged (ADC-capable pins are only GPIO 20–23 / 49–53). The pull-downs (R27 SD_EN 100k, R28 CAM_3V3_EN – 10k since 2026-10-10) moved next to the target IC, onto the front side. **Firmware: pin definitions must be updated; on GPIO 33 (USER) the 100k pull-down is gone, internal pull-up + C40.** The swap was made for routability, without checking the reset/strap states → the reset state of GPIO 4 (MTMS) must be checked in the P4 datasheet [UNVERIFIED].

**Location of the pull-downs (as-built, 2026-10-10):** all on the **MAIN front side (F)**: R24 IR_PWM (19.8; 13.6), R25 ICR_IN1 (24.05; 19.45), R26 ICR_IN2 (19.75; 16.8), R29 IR_SW_EN (35.45; 8.7; DNP), R27 SD_EN (7.0; 38.15), R28 CAM_3V3_EN (3.0; 16.3) – KiCad coordinates (§3.1a). ~~x 31.5, under the module~~ and ~~MAIN back side~~ are obsolete (they moved when the CSI corridor was cleared). Not on the FRONT (K-7: the MAIN works standalone).

### 5.1 Strapping table (GPIO 34–38) – **datasheet ref: TODO**
Known only from the Waveshare wiki (E8) and the EV board documentation; the ROM/strap function of each pin is to be filled in from the P4 datasheet **[UNVERIFIED]**.
| GPIO | Pad | Planned load | Expected boot state | Datasheet ref |
|---|---|---|---|---|
| GPIO 34 | P61 | **none** (NC, no external component) | default state | TODO |
| GPIO 35 | P62 | BOOT button to GND; **no other load** | high = normal, low = download (if GPIO 36 is high) | E8; TODO |
| GPIO 36 | P63 | 10k pull-up to 3V3 | high | E8; TODO |
| GPIO 37 | P64 | UART0 TX → R40 1k → J7.7 pad; **no pull-up/pull-down** | the test adapter must not hold it low | TODO |
| GPIO 38 | P65 | UART0 RX → R41 1k → J7.8 pad; **no pull-up/pull-down** | same | TODO |
Check: bring-up step 4 (15.) and factory test (16.): measurement on the strapping pins during boot (no external load beyond the documented values).

**SD rules (E-3/E-4/E-5/B-24; rev A: the block is DNP, the footprint stays – K-16):**
1. Firmware: set VO4 to **3.3 V** (`sd_pwr_ctrl` on-chip LDO ID 4), **then** SD_EN (GPIO 53, v0.6).
2. Pull-ups (CMD, D0–D3) to the **switched SD_3V3**, not to the main 3V3 (VO4 = 1.8 V during boot → overvoltage).
3. Load switch with discharge (TPS22918 class [UNVERIFIED]); SD_3V3 10 µF + 100 nF; ESD on the SD lines.
4. No back-feeding when the switch is off: no pull-up to the main rail (CD is the exception, A-27).
5. **FW: the SD lines must be put into tri-state (GPIO input) before SD_EN switches off** (otherwise the driven pins power the card).

## 6. Connectors

| Ref | Type | Where | Note |
|---|---|---|---|
| J1 | USB-C 16 pin (USB 2.0; HRO TYPE-C-31-M-12, C165948) | MAIN back side, **right edge** (40.8; 22.5) | D+/D−, CC1/CC2 → CH224A; shield 1 MΩ ‖ 4.7 nF (R1/C1, F). **USB FS only (12 Mbps, USB-Serial-JTAG P50/P51): the P48/P49 HS PHY is never enabled on this layout** – under the B-side sections of D+/D− In2 is not GND (DP 5.05 / DM 5.90 mm over VBUS_SW / void), the D+ clamp is on a 2.6 mm T-stub, the GND return path of U5 (F) is long (no via at U5.3) – no SI impact at FS, accepted in rev A (rev B: GND via ≤0.5 mm to U5.3, D+ in-line). **Soldering the 4 shell legs: §3.1 / §15**; pin map: `07` §3 |
| J2 | FPC 15 pin 1.0 mm – ~~candidate: 1.0K-GT-15PB or Hirose FH12-15S-1SH; the footprint on the PCB is a placeholder~~ → **TE 1-84953-5 (C5164008, TOP contact; the footprint is the ordered part itself; JLC stock 31 pcs)** | MAIN front side, **top edge** (22.5; 7.5), 180°, cable entry from the top edge | **contact side (Q6) + cable direction** to be checked with the camera module (before the first camera power-up) – wrong side = 3V3/GND swap at the camera; the 1-84952-5 (bottom contact) has the same footprint; straight cable; stiffener; control-signal ESD: **rev B** (A-10..12; §0.1) |
| J3 | microSD (the footprint is Hirose DM3AT – described as push-pull, "push-push" to be checked, mech-14) | MAIN front side, left edge | **DNP rev A** (footprint, K-16) |
| J4 | u.FL / IPEX | MAIN back side, **left edge** (3.0; 38.3) (the edge opposite the USB-C) | LNA_OUT (P2) → π-network (DNP elements) → 50 Ω line → u.FL | rev A: every element 0 Ω / DNP-capable; if the module's own IPEX is usable (G2), J4 can be DNP. **As-built: J4 + R34 0R FIT** (the G2 / K-6 / Q25 decision is open) |
| J5 | B2B 2×10, 1.27 mm, **mated height 7 mm** ~~[UNVERIFIED: part/availability]~~ → **BOM: Hong Cheng HC-PZ127-7.2L-2x10PS (C41375929)** + FRONT: HC-PM127-4.3H-2x10PS (C27985222); there is no ready-made 7.00 mm pair (5.3 mm pair → ~2.3 mm engagement; Samtec FTSH/FLE 7.47 mm → 7.5 mm standoff + footprint swap) – **Q17** | MAIN front ↔ FRONT | below; `07` §0 |
| J6 | ICR 2 pin JST-SH 1.0 mm | FRONT | DNP rev A (ICR: rev B); pin table below |
| J7 | 1×9 **SMD pad row, 1.27 mm** (`PadRow_1x09_P1.27mm_SMD`, pad 0.85×1.6) **(as-built: top edge, horizontal, (22.5; 2.0); pin 1 (17.42; 2.0) → pin 9 (27.58; 2.0); away from RF P2)**; ~~top-left board edge, vertical, x = 2.0~~ (60×50 state, obsolete) (GND, C6_TXD, C6_RXD, C6_IO9, C6_IO8, GPIO 54 / C6_EN (P82; Q2), UART0 TX, UART0 RX, 3V3-ref) | MAIN back side, on the edge **far** from the P2 (RF) pad | **DNP** (K-17); the only C6 / UART0 access (TP10–TP15 deleted); the RF trace does not run next to it; pin table below |
| SW1/SW2/SW3 | BOOT / RESET / USER – **Omron B3U-1000P** | MAIN back side, top edge: (11.5; 3.0) / (33.5; 3.0) / (33.5; 7.4) | at the board edge, accessible with a pin/pogo; USER (GPIO 33, v0.6) on the back side |
| TP | test points (12 pads) | MAIN back side | see 12. |

### J5 – 2×10 B2B (proposal; logic + power only, GND around PDM CLK and IR PWM, ≥2 pins per rail)
| Row | Odd | Even |
|---|---|---|
| 1–2 | **IR_VIN** (after the IR eFuse / fused 0 Ω) | **IR_VIN** |
| 3–4 | GND | GND |
| 5–6 | IR_PWM | GND |
| 7–8 | ICR_IN1 | ICR_IN2 |
| 9–10 | GND | 3V3 |
| 11–12 | 3V3 (also the ICR H-bridge supply) | GND |
| 13–14 | PDM_CLK | GND |
| 15–16 | GND | PDM_DAT |
| 17–18 | spare (NC; the status LED is on the MAIN back side, GPIO 6) | GND |
| 19–20 | SDA | SCL |
J5.17 is **spare (NC)**; GPIO 6 does not go to the B2B. Mirror/pin 1 check on a paper test (P-22). I2C pull-up in one place only (MAIN). Header current: IR_VIN 2 pins ≥ 0.6 A (estimated ~0.3 A at 4.5 V) **[UNVERIFIED: pin current rating]**; because of the IR current step, **local 10 µF + 100 nF on the FRONT** next to the header (within the 47 µF VBUS_SW budget, 4.1).

### J3 – microSD (push-push; DNP rev A) – pin table [UNVERIFIED: the pin numbering must be checked in the datasheet of the specific MPN; below is the standard microSD card pin order]
| Card pin | Signal | Connection |
|---|---|---|
| 1 | DAT2 | GPIO 41 (P69); pull-up to SD_3V3 |
| 2 | DAT3 / CD | GPIO 42 (P70); pull-up to SD_3V3 |
| 3 | CMD | GPIO 44 (P72); pull-up to SD_3V3 |
| 4 | VDD | **SD_3V3** (switched; 10 µF + 100 nF) |
| 5 | CLK | GPIO 43 (P71) |
| 6 | VSS | GND |
| 7 | DAT0 | GPIO 39 (P67); pull-up to SD_3V3 |
| 8 | DAT1 | GPIO 40 (P68); pull-up to SD_3V3 |
| CD switch | card detect | GPIO 52 (P80, v0.6), pull-up to the **main** 3V3 (CD is the exception, SD rule 4 in 5.); the other leg of the switch to GND |
| Shield | | GND |
ESD ≤3.5 pF on the SD lines; SD_EN = GPIO 53 (P81, v0.6) → SD_3V3 load switch (E17, SD rules in 5.).

### J4 – u.FL (rev A: DNP if the module's own IPEX is usable, G2)
| Pin | Signal | Connection |
|---|---|---|
| 1 (centre) | RF | LNA_OUT (P2) → π-network (DNP-capable) → 50 Ω line → u.FL (as-built: 0.302 mm microstrip on the B layer, In2 reference, ~7 mm track, U1 P2 → J4.1 path 7.96 mm; R34 0R FIT, C27/C28 DNP) |
| 2 (outer, shield) | GND | GND (via fence ≤2 mm, 13.) – ~~as-built (round 7): no fence, 0 GND vias within 2 mm; the In2 reference is cut by the +3V3 track → to be fixed (rf-01/rf-02)~~ → **fixed (round 8, round-9 measurement): GND vias within 1.0 / 1.5 / 2.0 / 3.0 mm of the RF centreline: 10 / 14 / 14 / 18, on both sides (largest spacing 1.31 mm); vias 0.10 mm from the J4 GND pads; In2 underneath 100 % GND (one 325.6 mm² island, 44 vias), KO_RF_In2 keep-out area (forbids tracks, but not non-GND vias – rev B: DRU rule)** |

### J6 – ICR 2 pin JST-SH 1.0 mm (FRONT; DNP rev A)
| Pin | Signal | Connection |
|---|---|---|
| 1 | ICR_A | DRV8837 OUT1 (IN1 = GPIO 27 → J5.7) |
| 2 | ICR_B | DRV8837 OUT2 (IN2 = GPIO 28 → J5.8) |
Coil polarity / day–night direction from the ICR lens datasheet (Q5) [UNVERIFIED]; FW pulse limit 50–100 ms, series current limit (4.2).

### J7 – C6 / UART0 header 1×9 (MAIN back side; DNP rev A, K-17)
| Pin | Signal | Module pad / note |
|---|---|---|
| 1 | GND | |
| 2 | C6_TXD (C6_U0TXD) | P5 (TP10 deleted) |
| 3 | C6_RXD (C6_U0RXD) | P4 (TP11 deleted) |
| 4 | C6_IO9 | P9 (BOOT; 10k pull-up R21; TP12 deleted) |
| 5 | C6_IO8 | P10 (10k pull-up R22, mandatory) |
| 6 | GPIO 54 / C6_EN (P82) | P82 (TP13 deleted); Q2 open (the connection to C6_EN inside the module is not confirmed) |
| 7 | UART0 TX (U0TXD_TP) | GPIO 37 (P64), after R40 1k (TP14 deleted) |
| 8 | UART0 RX (U0RXD_TP) | GPIO 38 (P65), after R41 1k (TP15 deleted) |
| 9 | 3V3 (level reference only) | the USB-UART adapter **must not power** the board (no 2nd power input, 4.1) |

### J2 – 15 pin MIPI FPC (RPi standard; **to be checked against the EV adapter schematic / the camera module**)
| Pin | Signal | Pin | Signal |
|---|---|---|---|
| 1 | GND | 9 | CLK_P |
| 2 | D0_N | 10 | GND |
| 3 | D0_P | 11 | CAM_IO0 (PWDN/EN) |
| 4 | GND | 12 | CAM_IO1 (LED, NC) |
| 5 | D1_N | 13 | SCL |
| 6 | D1_P | 14 | SDA |
| 7 | GND | 15 | 3V3 (CAM_3V3) |
| 8 | CLK_N | | |

**CSI pad order vs J2 (E20, R3-C):** the module pad order is P41 D0N, P42 D0P, P43 **CLKP**, P44 **CLKN**, P45 D1N, P46 D1P; the J2 (RPi) order is D0_N, D0_P, D1_N, D1_P, CLK_N, CLK_P. Consequences: (1) the **P/N order of the CLK pair is reversed** relative to the D pairs (P,N on the module; N,P on J2); (2) the **pair order also differs** (module: D0–CLK–D1; J2: D0–D1–CLK) → on a planar, 2-layer route at least one **pair crossing / P-N twist** is to be expected, which conflicts with the rule of 13. "max 1 layer change per signal". **⏳ G3** (the final decision depends on the camera selection; G2 only gives the spatial order from the footprint): options: (a) a camera module / FFC adapter whose order matches the module; (b) CSI lane / polarity swap in the P4 (TRM) [UNVERIFIED]; (c) symmetric via crossing at the J2 pads (measurement in rev A). We do not rely on a lane swap until the TRM confirms it (14.).

## 7. Camera module requirements (P-1, E-17, F-27, A-37)
| Requirement | Value |
|---|---|
| Oscillator, LDOs | **mandatory on the module** (no XCLK on the FPC) |
| **ICR (IR-cut) lens** | **mandatory in rev B; not in rev A**: any module meeting the electrical requirements (NoIR or fixed lens), the ICR block is DNP (K-5). The night-time IR image is not achieved without ICR (A-37) → rev B |
| Supply | 3V3 input from the **CAM_3V3 load switch (mandatory, TPS22918 class)**; 0 Ω measurement jumper after the switch; **CT / slew value: `07` §4, inrush to be measured** (K-22) |
| I2C | the pull-up on the module to be checked; DNP on the MAIN; **gate for fitting the pull-up: knowing the camera I/O level** |
| CAM_IO0 | polarity from the selected module's schematic (table in 5.); CAM_3V3 off → the camera definitely does not run, CAM_IO0 timing in FW (power sequence: 3V3 → CAM_IO0 → I2C) |
| Mechanics | **FPC length gate (Q5/Q6)**: short flex or 25–30 mm custom cable; the module PCB + holder fits into the **16×16 mm** cutout; MAIN components under the camera ≤3.3 mm; STEP required (G3) |
| MIPI speed | target ≤800 Mbps/lane; stream cap **1080p30** |
| Synchronous I/O level | may be 1.8 V on the module; to be checked (I2C level) |
| Procurement | buy 2–3 candidate modules, measure them, **freeze one with its STEP** → this precedes the mechanical finalisation (P-1 ⏳, Q5) |
| Software | `esp_cam_sensor` version to be pinned (E11) |

## 8. Stream pipeline
```
OV5640 (MIPI 2-lane, ≤800 Mbps/lane) → CSI host → ISP (max 1920×1080, E12) → [PPA: scaling/colour] → H.264 HW encoder → RTSP server → esp-hosted (SDIO) → C6 WiFi
                                                                                  └─ fallback: JPEG/MJPEG HTTP
```
| Step | Note |
|---|---|
| Sensor output | RAW/YUV422/RGB565 (E11); 2592×1944 is the sensor max, the pipeline is **capped at 1080p30** (720p in LOW mode) |
| Colour conversion | ISP output → H.264 input format (e.g. YUV420): where the conversion happens (ISP vs PPA), supported formats **[UNVERIFIED]** |
| H.264 encoder | P4 HW encoder, max resolution/fps/profile **[UNVERIFIED]** |
| RTSP | choice of library/component is open (Q12) |
| Fallback | MJPEG (HW JPEG) at a lower fps; the bitrate depends on WiFi + power mode |
| Bandwidth | 1080p30 H.264 ~2–6 Mbps target **[UNVERIFIED]**; SDIO is not a bottleneck |
| Day/night | switching based on camera AE/gain (no LDR); IR on → the ICR (if present) switches (pulse ≤50–100 ms) |

## 9. Firmware / OTA / partitions / power-outage tolerance
| Element | Plan |
|---|---|
| Partition table (16 MB) | bootloader · nvs (32K) · otadata (8K) · phy_init (4K) · coredump (64K) · `c6fw` data (~2 MB, C6 slave image storage/staging) · **ota_0 (4 MB)** · **ota_1 (4 MB)** · config (1 MB); remainder spare. Sizes **[UNVERIFIED]**, to be refined based on the real app size |
| P4 OTA | HTTPS download → inactive OTA partition → rollback (app rollback + diag. self-check) [UNVERIFIED: exact Kconfig] |
| C6 OTA | esp-hosted slave OTA from the P4 (from the `c6fw` partition/HTTPS) [UNVERIFIED: the API is version-dependent] |
| **C6 OTA = bring-up gate (00-K8, A-36)** | If the C6 factory FW is **not** OTA-capable: one-time UART flash with a known slave FW (10.); afterwards the C6 FW **cannot be updated in the field** without USB/UART → we pin the C6 FW version, the P4 app runs only with a compatible C6 version; the impact goes onto the risk list. If OTA-capable: closed by step 11 of section 15. |
| Rollback protection | the P4 app checks C6 version compatibility at start-up |
| **Power-outage tolerance (B-8)** | A PD hard reset takes VBUS to ~0 V and holdup does not help → the firmware **tolerates a power outage at any point**: NVS/config writes are atomic (journal/CRC, double copy), OTA only to the inactive partition, the `otadata` switch is the last step, a half-finished C6 staging is invalidated, SD file-system check at start-up; watchdog + rollback |
| Secure boot / flash enc. | **open** (Q14); eFuse is irreversible – to be decided after bring-up |
| Power mode logic | 4.3; mode decision after a ≥1.5 s settle, boot always LOW |

## 10. Programming and recovery
| Case | Path |
|---|---|
| P4 first flash | USB-C (GPIO 24/25 USB-Serial-JTAG); if the eFuse disables it, or USB does not enumerate: BOOT (GPIO 35 low) + RESET, or the UART0 pad (GPIO 37/38, E-25) |
| P4 recovery | BOOT/RESET buttons accessible on the back side (also when enclosed); UART0 spare pad |
| C6 first flash | UART pad (C6_U0TXD P5 / C6_U0RXD P4) + **GPIO 54 / C6_EN (P82; Q2)** + **C6_IO9 (P9)** pad |
| C6 later update | OTA from the P4 (D8) – **gate**, see 9. |

**C6 UART flash procedure** (F-21/F-22/E-23):
1. Hold the P4 in reset (ESP_EN pulled low) → GPIO 54 does not drive C6_EN. Q2: the C6_EN pull-up situation on the module is unknown.
2. USB-UART adapter (3.3 V logic) on the C6 TX/RX/GND pads – **as-built: J7 pad row J7.2 / J7.3 / J7.1** (DNP pad row, 1.27 mm; K-17; C6_EN = J7.6 = GPIO 54 / P82, Q2; TP10–TP13 deleted). **The module pad is close to the RF pad (P2)** (K6): the trace on the opposite layer, GND between them (P-30); **J7 is on the (top) edge far from the RF** (A-26).
3. C6_IO9 → GND (jumper/pogo), short pull-down of C6_EN → release (download mode). C6_IO9 **10k pull-up** to 3V3; C6_IO8: 10k pull-up mandatory (E6).
4. `esptool` chip-id + flash-id read → **F-22: query/save the factory FW version before flashing**.
5. Write the slave FW, remove the IO9 jumper, reset. JTAG (IO4–7) is not broken out in v1 (F-25).

## 11. Thermal management (PCB level)
| Element | Plan |
|---|---|
| Heat sources | P4+C6 ~1.5 W; buck loss ~0.8 W at peak (4.39 W × 0.18); IR drivers + LEDs ~0.5–1 W; camera ~0.7 W |
| **Thermal envelope** | in a closed (sealed) enclosure, at peak operation **~4.5–4.9 W** of heat (4.3: 5.6 W input − optical/RF output) **[UNVERIFIED]**; assumed **ambient temperature: 25–35 °C indoors** – the allowed T_amb and the required heat conduction (gap pad/enclosure heat path) to be finalised at the enclosure decision (18.); to be recalculated for outdoor use (P-39 ⏳) |
| Module | on the back side (towards the enclosure): Cu pour + GND vias under the module; whether there is a GND pad under the module: from the land pattern zip **[UNVERIFIED]** |
| IR LED | thermal vias under the 3535 pad + back-side Cu spreading; CC driver (not linear) → little dissipation |
| Buck | GND pour on the opposite layer, heat spreading around PGND |
| **NTC** | NTC **on an ADC2 pin (GPIO 49, range 49–53)** near the buck/IR zone; the P4 internal thermometer measures the core temperature, the NTC the board temperature |
| Firmware | P4 internal thermometer + NTC (E-32); thresholds (initial, **[UNVERIFIED]**): reduce IR power → reduce fps/bitrate → alarm; thresholds from the measurements |
| Measurement | bring-up step 10: closed-stack thermal camera/thermocouple measurement at the assumed T_amb |
| Enclosure/gap pad | deferred (18.) |

## 12. Test points (E-29, P-29)
**As-built (MAIN v0.6, 2026-10-10):** every TP is `TestPoint_Pad_D1.5mm` (Ø1.5 pad, excluded from BOM/CPL); coordinates in the KiCad frame (§3.1a).

| TP | Net | Side / position | Note |
|---|---|---|---|
| TP1 | VBUS | B (42.95; 32.25) | pogo group (0.15 mm off the 2.75 mm grid) |
| TP2 | VBUS_SW | B (40.35; 29.5) | pogo group |
| TP3 | GND | B (43.1; 40.5) | pogo group |
| TP4 | +3V3 | B (37.6; 32.25) | pogo group; with R16 0R (F, K-1) removed → 3V3 bench feed-in (never at the same time as USB). Round 7: the TP4 → 3V3 path is ~34 mm of thin In2 copper (~0.17 Ω) → round 9: TP4 → U1.84–86 **72.9 mΩ** (~39 / 79 mV at 0.54 / 1.08 A) – acceptable for debugging; for high current the bench feed-in is better applied at R16.2 / C20 |
| TP5 | CAM_3V3 | B (12.6; 6.6) | **separate, outside the group**, next to the CAM_3V3 net (after the R50 0R measurement jumper) |
| TP6 | SD_3V3 | B (36.3; 10.4) | **separate, outside the group**; FIT pad, even if the SD block is DNP |
| TP7 | VO4 | B (37.6; 35.0) | pogo group; next to C24 1 µF; external source forbidden |
| TP8A / TP8B | IR_VIN_SH / IR_VIN (both ends of shunt R72) | F (36.85; 38.45) / (31.0; 39.15) | **DNP rev A** (with the IR branch); not in the back-side group (A-25) |
| TP16A | ESP_EN | B (40.35; 35.0) | pogo group |
| TP16B | BOOT (GPIO 35) | B (43.1; 35.0) | pogo group |
| TP17 | PD_PG (CH224A) | B (37.6; 37.75) | pogo group |
| TP18 | GND | B (40.35; 37.75) | pogo group |
| TP19 | GND | B (43.1; 37.75) | pogo group |
| ~~TP9a/b, TP10–TP13, TP14–TP15~~ | ~~USB D±; C6 TX/RX/IO9/EN; UART0~~ | – | **deleted** (owner decision 2026-10-09, "TP thinning"): C6 and UART0 only via the J7 pad row (§6), USB D± can be measured on J1/U5 |
| – | **no TP on the CSI lines** | – | P-7 |

**Pad count (as-built):** **12 TP pads** on the B side (9 signal + 3 GND: TP3, TP18, TP19); of these **10 are in one pogo group, on a 2.75 mm grid** (x 37.6–43.1, y 29.5–40.5; TP1 offset by 0.15 mm), **TP5 and TP6 stand separately**. TP8A/B (F, DNP) do not belong to the group. ~~20 pads, 2.0 mm grid (R4 plan)~~ – the pogo jig must be designed from the coordinates above; C6 programming on the 1.27 mm pads of J7 (0.85×1.6) with pogos or a soldered header.

## 13. 2-layer layout rules
> **v0.6 note:** the MAIN is 4-layer (§3.2) – the initial width/gap values are overridden by §3.2 (3313A, L2 = continuous GND); the 2-layer CPWG numbers below apply only to the FRONT (and as an archived reference). The rule principles (CSI layer change + return GND via, RF fence / GND reference, small buck loop, ESD at the connector) are mandatory for the MAIN too – ~~according to round 7, several of them are violated~~ → **met after round 8 (round-9 measurement, `90-review-log.md`): 2 GND return vias per CSI pair ≤1 mm, In2 100 % GND under the CSI stubs and the RF, RF fence, buck hot loop 1.44 mm²**; accepted rev A deviations: CSI length / skew (below), USB FS only (§6), D1 TVS at the eFuse (§4.1).

For everything: 1.0 mm FR4, Cu 35 µm [UNVERIFIED]. **Every geometry "to be checked with a field solver" against the final stackup** (JLC 2-layer; εr ~4.2–4.6 [UNVERIFIED]).

| Area | Rule / initial value |
|---|---|
| MIPI-CSI (100 Ω diff) | CPW diff pair with GND; initial: **w≈0.30 / s≈0.20 / GND gap 0.2–0.3 mm** (P-6: **derived / interpolated from the 0.8 mm rows, there is no independent source for 1.0 mm** → field solver) – *to be checked with a field solver*. **Layer-change rule (A-19, 06-K2; replacing the old "no via in the pair"):** the module is on the MAIN back side, J2 on the front side → the pair crosses over with **a single symmetric layer change**: **P and N vias side by side, with 2 GND return vias per pair next to them**; **max 1 layer change per signal**, preferably **at the J2 pads (≤1 mm)**; the rest of the pair on the back side. Length module pad → J2 **<15 mm**, ±0.1 mm matching, ≤1 mm taper at the pad, GND pads between the pairs, CSI away from the RF, **≤800 Mbps/lane**, no TP. **Pad order (E20): D0N, D0P, CLKP, CLKN, D1N, D1P vs J2 D0, D1, CLK → a pair crossing / P-N twist is to be expected, see the 6. J2 note (⏳ G3). Proposed exception to "max 1 layer change per signal" (Q24, decided at G3): if the camera / FFC order does not match, the crossing happens at the J2 pads (≤1 mm), and for this at most **one additional symmetric via pair** is allowed [UNVERIFIED; measurement in rev A]**. **As-built (MAIN rev A, round-9 measurement): length D0 10.446 / D1 15.280 / CLK 21.415 mm (P/N), intra-pair ≤0.003 mm; data–clock mismatch D0 10.97 / D1 6.14 mm ≈ 64 / 36 ps ≈ 0.05 / 0.03 UI @800 Mbps → the "<15 mm" rule (CLK, D1) and the data–clock matching are violated – accepted rev A deviation, to be confirmed by the G5b soak test (§15 7a); coupled (≤0.25 mm gap) section only D1 ~5 / CLK ~7 mm, the rest has a 0.45–0.85 mm gap (estimated Zdiff ≈115–117 Ω); 2 GND return vias per pair within ≤1 mm; the 6 CSI vias under the module (tented)** |
| GND reference | Since the MAIN is **assembled on both sides, there is no "solid bottom GND plane"**: a **continuous GND pour on the opposite layer under the CSI and RF traces is mandatory, with a component ban** there (06-K3: behind the RF zone and behind the CSI strip on the front side only GND) |
| RF (50 Ω) | LNA_OUT (P2) → u.FL **CPWG**, <10 mm, via fence ≤2 mm; initial: **w≈0.6–0.8 / gap 0.2–0.25** (estimate – derived from the **0.8 mm** CPWG row of P-9 [w≈0.5–0.6], no independent data for 1.0 mm) – *field solver mandatory*; JLC 2-layer: no impedance control, ±10–20 % [UNVERIFIED] (3.1); π-network footprint (DNP); GND pour underneath, component ban. **As-built (MAIN, 4 layers): 0.302 mm microstrip on B, In2 100 % GND reference, path 7.96 mm (0.111 λg), fence on both sides 0.70–1.48 mm from the centreline, max. spacing 1.31 mm (§6 J4)** |
| USB-Serial-JTAG (12 Mbps) | short, ESD (3.3 V array) at the connector, 90 Ω is not critical at 12 Mbps. **As-built: FS only; the HS PHY (P48/P49) must never be enabled on this layout (§6 J1)** |
| Buck | small loop, input MLCC directly VIN–GND, forced-PWM, 2.2 µH Isat ≥3.5 A. **As-built: C9 100 nF 0.6 mm from the U4 pins, hot loop 1.44 mm² (without vias), SW only on F (3.0 mm), FB 2.77 mm, SS 3.42 mm, In1 100 % underneath; L1 = Taiyo NRS5024T2R2NMGJ (Isat 4.1 A, 2.4 mm high)** |
| Microphone | LC supply filter, series R on CLK, GND around it, no digital trace runs above it |
| SD | 4-bit, short, ESD ≤3.5 pF, pull-ups to SD_3V3 |

### 13.1 EMC (A-15, F-35)
| Source | Measure |
|---|---|
| IR LED loop (40 kHz+ PWM, 0.3 A) | small-loop power return (driver input cap ↔ NFET ↔ LED ↔ GND), IR_PWM/IR_VIN flanked by GND on the B2B, LEDC ≥40 kHz (avoiding PDM aliasing), the LED loop away from the microphone and the CSI |
| Buck (forced-PWM) | small switching loop, shielding GND pour, in the left strip (away from the u.FL and the microphone), measurement at bring-up step 2 (ripple) |
| USB ESD | TPD2E2U06 / PRTR5V0U2X class on D± at the connector, shield 1 MΩ ‖ 4.7 nF; TVS+ESD ground directly to the connector GND, not through the buck GND current path |
| WiFi (2.4 GHz) | RF path short and GND-fenced; away from CSI and PDM CLK; the C6 UART TPs away from RF; local 3V3 bulk for the TX spikes (E-14); early RSSI test |
| General | header GND per pair; "no hot-plug" label; ESD diodes on the FPC control signals (A-10..12); preliminary radiated/conducted pre-measurement without and with the enclosure (18.) |

## 14. Pad map (P-4, P-5, P-22) – E20 incorporated
- **Signal ↔ pad assignment: done, primary source (E20).** Every pad column of the GPIO table in chapter 5 is filled in (the earlier TBDs: GPIO 26–33 → P53–P60, GPIO 47–53 → P75–P81 etc.).
- **The spatial arrangement is still an assumption [F]:** counter-clockwise, 22 pads/side, ~2 mm empty at the corners (06 §1). The E20 order gives groups consistent with this (side 1 P1–P22: RF + C6 + GPIO1–7; side 2 P23–P44: GPIO8–13/20–23, DSI, CSI D0 + CLK; side 3 P45–P66: CSI D1, USB, GPIO24–38, VO4; side 4 P67–P88: SD GPIOs, 3V3, EN), but the edges / corners remain [F] until the Waveshare footprint is imported (06-K12).
- The CSI pads P41–P46 probably break across a corner (D0 + CLK on one side, D1 on the next) [inference, UNVERIFIED]; RF P2, ESP_EN P87, SD P67–P72 may also be near a corner.
- **Module rotation/placement can only be decided after the footprint import**: CSI → towards J2, P2 → towards the u.FL (or the module's IPEX), P50/P51 (USB) → towards the USB-C; **u.FL and USB-C on opposite edges** (A-34; 06: USB-C W edge, u.FL NE corner).
- **CSI pad order vs J2: checked, there is a deviation** (CLK P/N reversed; pair order D0–CLK–D1 vs D0–D1–CLK) – see the 6. J2 note and the 13. CSI row; we do not rely on a lane swap. **The final decision is at G3** (selected camera / FFC); G2 only gives the spatial order from the footprint.
- Footprint import + 1:1 paper test (mirroring, pin 1). After that, chapter 4 of 06 is to be redrawn.

## 15. Bring-up sequence (based on F-34)
**Configuration (K-7):** the MAIN standalone, the camera on a standard 50–100 mm FFC; the stack is closed only after a stable image. **Prerequisite:** G0 (dev-kit stream), G1 (CH224A). DNP in rev A: SD, IR, ICR, CC-tap, supervisor.
| Step | What | Success |
|---|---|---|
| 0 | Visual inspection (U3, J1, U4 under a microscope), short-circuit measurement VBUS/VBUS_SW/3V3/GND; **VBUS ↔ VBUS_SW resistance (JP1 0.3 mm open solder bridge – no mask dam, bridging it would bypass the eFuse; round 7)**. **Measurements before first power (round 9; DMM, without U1; 15–30 s settling because of the ~54 µF on VBUS_SW):** (a) VBUS ↔ GND (TP1–TP3) ≈ 70–73 kΩ, VBUS_SW ↔ GND (TP2–TP3) ≈ 230–255 kΩ; (b) **VBUS ↔ VBUS_SW (TP1–TP2) ≈ 300–330 kΩ** (≈ the sum of the previous two; <1 kΩ = JP1 or U3 IN–OUT bridge → STOP); (c) **3V3_BUCK ↔ GND (TP4–TP3, R16 fitted) ≈ 13.5 kΩ – investigate if <5 kΩ or >16 kΩ** (>16 kΩ: R14 / R15 / R33 open; an open R14 → FB 0 V → the buck may run up towards VBUS_SW (9 V); a via hole intrudes into the R14.1 pad); (d) **VBUS, D+, D− ↔ GND not shorted** (the D± check also verifies the pinout of the U5 clone: pin 3 = GND); (e) with reversed leads in diode mode 0.000 V = short | no short, JP1 open, every value within range |
| 0a | **J1 shell legs** (if JLC did not solder them, §3.1): solder the 4 legs from the F side **before the first cable insertion** (fine tip, little solder), then inspect the leg ↔ C1.2 (GND, 0.757 mm) gap | 4 legs soldered, no bridge |
| 1 | Current-limited USB (5 V): CH224A, eFuse, soft start (measure the UVLO and OVP thresholds); then 9 V PD; **VBUS_SW effective C and attach-current measurement**; PG and VBUS ADC; **CH224 DP/DM NC behaviour / USB-JTAG D± conflict test**; **PD hard reset ≥20×** (eFuse auto-retry, vSafe0V) | VBUS_SW stable, OVP/UVLO behaviour, no host OCP | bypasses (K-1) only in case of failure; CH224A + Rd never at the same time |
| 2 | Buck 3V3 without the module (0 Ω open) | 3V3 correct, ripple |
| 3 | P4 module fitted (last; **fine conical tip on P83–P88**, flux – C21–C23 are 0.5 mm from the P83–P86 tips, C23.1 (+3V3) is 0.525 mm from the tip of P87 (ESP_EN)); **inspection: P87/C23 gap, R34 / J4 GND fillet** (the tip of P2 is 1.82 mm from R34.1); before power **TP16A (ESP_EN) ↔ TP4 (+3V3) ≈ 10 kΩ** (R23; **0 Ω = bridge** → no EN delay, and SW2 would be a 3V3–GND short) and 3V3 ↔ GND > 1 kΩ; then current draw; **ESP_EN behaviour** (rev A: supervisor DNP; R23/C25 FIT + the module's RC, Q3) | no bridge, no overcurrent |
| 4 | USB enumeration; USB-JTAG eFuse state (F-23); P4 flash; **strapping check: GPIO 34–38 levels during boot, per table 5.1; level of GPIO 45 (NC); check that the sdkconfig SD power-reset (GPIO 45) is overridden** | `esptool` connects; strap values match |
| 5 | C6 chip-id, factory FW (UART pads, F-22); esp-hosted SDIO; WiFi scan | C6 visible |
| 6 | VBUS/PG ADC (the CC ADC: rev B / if the CC-tap is fitted), **power mode logic (rev A: LOW/FULL; ≥1.5 s settle, hysteresis); LOW boot on a PC port** | thresholds match, no mode hopping |
| 7 | CAM_3V3 switch (**inrush measurement**, K-22; **TP5 (CAM_3V3) at 0 V during reset** – R28 10k), camera **on a standard 50–100 mm FFC, MAIN standalone**, **after checking the J2 contact side (Q6)**: I2C identification (100 kHz) → MIPI image → H.264 | 1080p30 stream |
| 7a | **CSI soak test (G5b, round 9):** 1080p30 at the driver's actual lane rate (≤800 Mbps/lane) for **≥1 h**, logging the CSI error, CRC and ECC counters; repeat with the long (100 mm) FFC – confirms the as-built skew (≈0.05 / 0.03 UI) and the 21.4 mm CLK (§13) | 0 CSI / CRC / ECC errors, no frame loss |
| 8 | SD (**rev A: DNP**; later: VO4 → 3.3 V, then SD_EN; tri-state before SD_EN), PDM mic (FRONT, G6) | SD r/w, mic signal |
| 9 | (**G6, FRONT**; bench: **shielding tube / window spacer**, K-19) IR eFuse #2 + drivers (ILIM, shunt current, headroom at Vin 4.5 V), ICR pulse (if present) | current as calculated; no reset on an IR short |
| 10 | Thermal (NTC + internal) + WiFi TX brown-out test in a closed stack | no reset |
| 11 | **OTA (P4 + C6)**, rollback; **C6 OTA gate (00-K8)**; **PD hard reset during OTA** | successful update without USB; the system recovers |

**Rev A firmware rules (round 9; mandatory throughout bring-up):** (1) **I2C 100 kHz** (the bus only has the CH224A internal pull-ups, R31/R32 DNP; SDA 112.9 mm); (2) the PD mode is given by **PG (GPIO 31) + VBUS_SW ADC (GPIO 20)**; the CH224A is **only read, and only after CAM_3V3 is switched on** (or not at all) – **never written** (a 20 / 28 V request → the TVS fails); (3) **IR_SW_EN (GPIO 32) always low** (the R29 pull-down is DNP); (4) **the USB HS PHY (P48/P49) is never enabled on this layout** – USB-Serial-JTAG FS only (§6); (5) NTC model: B = 3987 K (TH1, LCSC data; the type name says "B3950"), calibration at G5b.

## 16. Factory / first test plan (F-33)
Pogo jig on the back-side pad group; test sequence: (1) current/short circuit, (2) 3V3/VO4/SD_3V3/CAM_3V3 measurement, (3) USB enumeration + flash (test FW), **(3a) strapping level check (GPIO 34–38)**, (4) C6 UART chip-id + FW upload, (5) WiFi ping/RSSI (u.FL antenna), (6) camera image, (7) SD r/w, (8) mic RMS, (9) IR current, (10) ICR click (if present), (11) button/LED, **(11a) PD 9 V negotiation + PG + hard reset 20×**, (12) logging: MAC, chip rev, FW versions.

## 17. Open questions
| # | Question | How we close it |
|---|---|---|
| Q1 | ~~SD VDDPST_5~~ ✅ E16/E17; remainder: whether VDDPST_5 is connected to VO4 inside the module (**A-28 ⏳**) | module schematic |
| Q2 | GPIO 54 = C6_EN on the module too? C6_EN pull-up? | Waveshare module schematic |
| Q3 | Does the module have an EN RC, 40 MHz XTAL, pull-ups, C6_IO9 pull-up (**E-22 ⏳, F-16 ⏳**) – the supervisor (B-21) fitting decision comes after this | module schematic |
| Q4 | Module P4 chip revision (v1.x vs v3.x), long-term availability (**F-2 ⏳**) | Waveshare / LCSC |
| Q5 | Camera module: 15 pin, 3V3, **onboard osc**, CAM_IO0 polarity (→ GPIO 23 pull), I/O level, **short flex / 25–30 mm FPC**; rev A: NoIR or fixed lens (ICR mandatory in rev B) (**P-1 ⏳**) | market search + samples (G3) |
| Q6 | FPC contact side + cable (forward/reverse), FPC length gate. ~~The J2 footprint on the PCB is a placeholder (TE 1-84953-5)~~ → **J2 is the ordered TE 1-84953-5 (TOP contact, C5164008); the bottom-contact 1-84952-5 has the same footprint. Wrong contact side = 3V3/GND swap at the camera** – ~~to be closed before ordering~~ → **to be closed before the first camera power-up (it does not block PCB manufacturing, round 9)** | real camera module + FFC (G3) |
| Q7 | Actual current draw of the module | Waveshare datasheet, then measurement |
| Q8 | Z-stack budget: G = 7 mm, ≤3.3 mm under the camera; recalculate with the actual camera module | 06 + Q5 STEP |
| Q9 | Is the MIPI PHY supply (VO3) handled inside the module (**E-18 ⏳**) | module schematic |
| Q10 | RF path behind P2 on the module (**P-10 ⏳**) | module schematic |
| Q11 | esp-hosted handshake/reset GPIO for the module (**F-26 ⏳**) | Waveshare example sdkconfig |
| Q12 | RTSP component, H.264 HW encoder limits, where the format conversion happens | IDF/esp-video docs |
| Q13 | **CH224A datasheet**: voltage strap table, PG polarity, internal Rd, DP/DM handling, capacitor requirement; **specific eFuse type** (adjustable OVP, reverse-blocking, auto-retry, UVLO, ILIM); TVS SMAJ10A datasheet; **IR eFuse #2 type** (≥18 V, adjustable ILIM) | datasheets (currently [UNVERIFIED]) |
| Q14 | Secure boot / flash encryption | after bring-up |
| Q15 | 👤 Indoor v1? (**P-39 ⏳**; affects the T_amb of the thermal envelope and the LED choice) | owner |
| Q16 | Is the C6 factory FW OTA-capable (**00-K8 gate**) | bring-up steps 5 and 11 |
| Q17 | **B2B 2×10 1.27 mm header pair, 7 mm mated height**: existing part, availability, tolerance, current rating. **2026-10-11: there is no ready-made 7.00 mm pair; in the BOM the Hong Cheng pair (C41375929 + C27985222, 5.3 mm → ~2.3 mm engagement at 7.0 mm, MAIN unchanged) – alternative Samtec FTSH-110 / FLE-110 (7.47 mm; 7.5 mm standoff + MAIN footprint swap before ordering)** | 👤 owner decision (`07` §0) |
| Q18 | Buck L/Cout range for the selected type (**B-27 ⏳**) | buck datasheet |
| Q19 | IR LED type: Vf_max(−20 °C), 2-LED series vs single-branch decision (4.2 criterion) | LED datasheet |
| Q20 | PDM microphone type: MSM261D3526H1CPM / MP34DT05-A [UNVERIFIED], availability | datasheet |
| Q21 | Functions of the P4 strapping table (GPIO 34–38) | P4 datasheet (5.1 TODO) |
| Q22 | ✅ **Closed: rev A MAIN 60×50 mm** – **overridden (2026-10-09): MAIN 45×45, 4 layers (00 K4); as-built interface §3.1a**. Original: should the Rev A MAIN be larger (e.g. 60×50 mm) with the same M2 grid and J2/J5 coordinates? (45×45 remains the target, K-12) | owner |
| Q23 | USB designation: USB-Serial-JTAG GPIO 24/25; OTG FS not used (sdkconfig, P4 datasheet) [UNVERIFIED] | G0 sdkconfig |
| Q24 | Handling of the CSI pad order / CLK P/N deviation: lane / polarity swap in the P4, camera / FFC order, via crossing (6. J2 note) | TRM, G3 (spatial order of the footprint: G2) |
| Q25 | Antenna: is the module's own IPEX usable (back side, accessible)? RSSI with two antennas | G0 / G2 |
| Q26 | EDA = **KiCad** ✅; open: JLC assembly of the USB-C THT shell (3.1) → **the shell legs have no paste: JLC hand / selective soldering or own soldering before the first insertion (§0.4, §15 0a)** | at order time |

## 18. Deferred (enclosure)
The enclosure-level items have been moved here: enclosure material, window 850 nm transmission, IR eye safety (IEC 62471, P-38; the LED current ceiling is a PCB requirement, 4.2), outdoor/indoor protection (P-39), ventilation/heat conduction for the T_amb condition (11.), gap pad to the rear wall (P-20), black foam ring against IR leakage (P-17 enclosure side), microphone sealing, pinhole BOOT/RESET and light pipe (P-31), microSD slot from the side (06-K10), pogo window (P-29), USB cable strain relief (P-40), antenna cable fixing. **Remains at PCB level:** holes/standoffs, FPC access, IR baffle Cu ring, accessibility of buttons/TPs.

## 19. Review coverage (✅ items → section)

**R1 (round 1):** E-1,2,13 → 4.1 · E-3,4,5 → 5 · E-6,8 → 5/5.1 · E-9,10,19 → 2/D9, 4.2, 6 · E-11,12 → 4.1/4.3 · E-14,15 → 4.1/13 · E-16,31 → 5/13 · E-17,26,F-27 → 7/5 · E-20,21 → 5/D7 · E-23,F-21,22 → 10 · E-24,25 → 5/6/10 · E-27 → 13 · E-28 → 3 · E-29 → 12 · E-30,P-37 → 3 · E-32,P-20 → 11 · E-33,F-18 → 4.3 · E-34 → 5 · E-35 → 2/D5, 4.1 (no 2nd input) · E-36,F-1,9,10,11 → banner 01–04 · P-1 → 7 (⏳) · P-2,3,8,13,14,16,21,23,24,34,35 → 3 · P-4,5,22 → 14 (⏳ footprint) · P-6,7,9 → 13 · P-11,12 → 3 · P-15 → 6 · P-17,28 → 3 · P-19 → 3 · P-25,26,27,29,30,31,32,33,36 → 3/4.1/10/12 · P-38,40 → 18 · F-3 → 4.3 · F-4 → 5 · F-5 → 3/6 · F-6 → D9 · F-7,30..32 → 5 · F-8 → 5.1 · F-12,24 → 5.1/15 · F-14,15 → 7 · F-17 → 4.2 · F-19,20 → 8/11/16 · F-23,25 → 10/15 · F-28 → 8 · F-29 → 3 · F-33 → 16 · F-34 → 15 · F-35..38 → 13.1/14/5.
**R2-B (round 2):** B-1 → 5 (GPIO 24/25), 6, 13 · B-2 → 4.3 (rule 1) · B-3 → 4.1 (CC-tap), 4.3 · B-4 → 2/D5, 4.1 · B-5 → 4.1 (external Rd forbidden) · B-6 → 4.1, 5 · B-7 → 4.1, 15/1 · B-8 → 4.3 (rule 5), 9, 15/1, 15/11, 16 · B-9 → 4.1 (eFuse) · B-10 → 4.1 (capacitance) · B-11 → 2/D5, 4.1 (9 V) · B-12 → 4.1 (TVS) · B-13 → 4.1 (strap) · B-14 → 4.2 (criterion) · B-15 → 4.2 (NFET, Cout) · B-16 → 4.2 (ICR 3V3) · B-17 → 4.3 (mode table) · B-18 → 4.3 (recalculation) · B-19 → 4.3 (LOW) · B-20 → 4.1 (UVLO) · B-21 → 5 (ESP_EN supervisor; after Q3 ⏳) · B-22 → 4.1, 5 (GPIO 33), 7 · B-23 → 4.1 (VBUS divider), 5 · B-24 → 5 (SD rule 5) · B-25 → 4.1, 4.2, 5 (GPIO 32) · B-26 → 11 (NTC, thermal envelope), 5 · B-27 → Q18 ⏳ · B-28 → 4.1 (effective C) · B-29 → 4.2, 6 (J5) · B-30 → 4.2, 5 (LEDC ≥40 kHz).
**R2-A (round 2):** A-3 → 5, 7 · A-4 → 5, 10 (C6_IO9 pull-up) · A-5/6 → 4.2, Q19–Q20 (IR, PDM flagged) · A-7 → 5, 7 (I2C gate) · A-8 → 4.3 · A-9 → 5.1, 15/4, 16/3a · A-10..12 → 6, 13.1 · A-13 → 4.2 (eye safety), 3 (06 reference) · A-14 → 7 (CAM_IO0 timing) · A-15 → 13.1 · A-17 → 4.1 (no 2nd input) · A-18 → 19 · A-19 → 13 (CSI layer change), 3 · A-20/21 → 4.1 · A-22/23/24 → 4.1, 4.3 · A-25 → 4.1, 4.2, 12 (TP8) · A-26 → 10, 12 · A-27 → 5 · A-28 → Q1 ⏳ · A-29 → 5.1 · A-30 → 1 (P48/P49), 5 · A-31..33 → 1, 5, 10 (P notation, C6_IO8) · A-34 → 3, 14 · A-35 → 4.2 · A-36 → 9, 15/11 (C6 OTA gate) · A-37 → 2/D3, 7 · A-38 → 5, 6 (user button).
**Coordinator decisions (v0.3):** VBUS 9 V → 4.1 · CH224A+PG → 4.1 · power modes → 4.3 · recalculation → 4.3 · ESD → 5 · IR → 4.2 · ICR/Q5 → 4.2, 7 · CAM_3V3 → 4.1, 7 · supervisor → 5 · CSI/GND → 13 · stack 7 mm → 3 · P notation → 1, 5, 10, 14 · strapping/EMC/NTC/PD hard reset/C6 OTA → 5.1, 13.1, 11, 9, 15, 16.
**R3-C (round 3):** 06 consistency (ESD, CC-tap, 7 mm gap, TP8, budget, bulk, TP count, FFC, lens) → 06 v0.2 · GPIO2–4, GPIO0/1, GPIO45, pad origin, GPIO23 → 5 · CC-tap claim → 4.1 · source per power mode → 4.3 · reference prefixes → D8, 9, 15, Q16 · C6_IO8 → E6, 5 · VEML → D7 · 00 mic → 00 · USB designation → E4, 5, 13, Q23 · CPWG → 13.
**R3-K (round 3):** K-1 → 0.1, 4.1 · K-2 → 0.2 (G0) · K-3 → D9, 4.1, 4.2 · K-4 → 4.1, 0.2 (G1) · K-5 → D3, 4.2, 7 · K-6 → E7, 3, 0.2 (G2) · K-7 → 0, 3, 15 · K-8 → 0.2 (G4), `07` · K-9 → 0.3 · K-10 → 3, 3.1 · K-12 → 0, Q22 · K-13 → 0, 3 · K-14..K-17 → 0.1, 5, 6 · K-18 → 3.1 · K-19 → 4.2, 15 · K-20, K-22 → `07` §3–§4, 7.
**R4 (round 4, `08` defect list 1–23):** 1 → 0.1 · 2, 3 → 12 · 4 → 5, 6, 10, 12 · 5, 6 → 4.1 · 7 → 4.1, 5, 6 · 8 → 4.2, 5 · 9 → 0.1 · 10 → 0.1 · 11 → D9, 4.1, 4.2 · 12 → 4.3, 15 · 13 → 6 (J7) · 14 → `07` · 15, 16 → 0.2 (G3), 6, 13, 14, Q24 · 17 → 0.2 (G5b) · 18 → invalid · 19 → 6 · 20 → 5 · 21 → 3, 4.1 · 22 → 06-K5 · 23 → 0.4.
**R9 (round 9, final multi-agent review, 2026-10-11, `90-review-log.md`):** C14 → 0.1, 4.1 · D1 location → 0.1, 3, 4.1 · J2 / J5 / Q6 / Q17 → 0.1, 3.1a, 6, 17 · MH + washer → 3, 3.1a · stackup / pre-order gate / panel → 3, 3.1 · J1 shell legs → 3.1, 0.4, 15 · USB FS → 5, 6, 13 · CSI as-built + soak → 13, 15 · bring-up measurements, U1 hand soldering, FW rules → 15 · BOM → `07` §0 · as-built placement → `06`.
**⏳ open (not incorporated):** E-18, E-22, P-1, P-4, P-5, P-10, P-39, F-2, F-16, F-26, B-27, A-28 → 17.
