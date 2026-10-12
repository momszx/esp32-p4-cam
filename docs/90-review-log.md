# 90 – Review log

Legend: ✅ accepted → to be fixed in 05 (applied) · ❌ rejected (reason) · ⏳ open / gate (external data or measurement needed) · 👤 owner decision · ⟲ superseded by a later item

## Review round 1 (2026-10-09)

### R1-E: Electrical / power / schematic completeness (Sonnet) — 36 items

| # | Severity | Finding | Fix | St. |
|---|---|---|---|---|
| E-1 | BLOCKER | 5.5 V-rated buck (SY8089/TPS62A02) can be destroyed by a USB-C hot-plug spike (~2× VBUS); SMBJ5.0A clamps at ~9 V | Buck with ≥17 V input (TPS62933 class) **or** eFuse/OVP (~5.8–6 V) in front of it | ✅ |
| E-2 | BLOCKER | VBUS capacitance at attach: USB limit ~10 µF; 100/470 µF directly on VBUS → host OCP | ≤10 µF on the connector side, soft-start eFuse, bulk after it; delete 470 µF from the 04 doc | ✅ |
| E-3 | BLOCKER | SD pins on the VO4 domain (default 1.8 V) → 10k pull-up to 3V3 = overvoltage during boot | Pull-ups to the switched SD_3V3; FW: VO4 → 3.3 V first, then SD power; CD + load switch EN moved off VO4 (GPIO26–33) | ✅ |
| E-4 | BLOCKER | Card back-powering while the load switch is off | Pull-ups + ESD on the switched rail; load switch with discharge (TPS22918); 10 µF + 100 nF | ✅ |
| E-5 | HIGH | VO4 (pad 66) handling missing | 1 µF + TP, external source forbidden; GPIO47/48 are also VO4 | ✅ |
| E-6 | HIGH | Strapping GPIO34–38 incomplete; 34 is in the free list | 34/37/38 left unloaded; debug pad series 1–4.7k; strapping table from datasheet | ✅ |
| E-7 | HIGH | 05 §5 pin numbers conflict with 01 | ❌ 01 = chip QFN pin, 05 = module pad (Waveshare table). Banner added to 01 | ❌ |
| E-8 | HIGH | IR PWM + ICR inputs float during boot | 100k pull-down; preferably GPIO26–33 | ✅ |
| E-9 | HIGH | ICR coil data unknown; H-bridge on MAIN, coil on FRONT | ICR datasheet first; H-bridge to FRONT (DRV8837); no ICR → delete | ✅ |
| E-10 | HIGH | IR LED driver undersized | Fix the LED count; current source/1206 resistor; AO3400; PWM ≥20 kHz (**→ ≥40 kHz, B-30**); 10–22 µF at the LED anode (**→ Cout ≤1 µF, B-15**) | ✅ ⟲ B-15, B-30 |
| E-11 | HIGH | CC directly to GPIO | 1k + BAT54S clamp + 100 nF (**→ 100k + 10 nF + Zener, B-6**); thresholds 0.25–0.61 / 0.70–1.16 / 1.31–2.04 V | ✅ ⟲ B-6 |
| E-12 | HIGH | >500 mA on a default port; boot = peak | Boot order P4+C6 → CC → camera+SD → IR; WiFi TX limit; min. 5 V/1.5 A source | ✅ |
| E-13 | HIGH | PTC 1.5 A is ~1 A when hot | eFuse ~2 A (combined with E-1/E-2) | ✅ |
| E-14 | HIGH | WiFi TX brown-out | 47–100 µF + 10 µF + 100 nF at the module 3V3 pads | ✅ |
| E-15 | HIGH | Buck PFM noise → microphone | forced-PWM, 2.2 µH Isat ≥3.5 A, mic LC filter | ✅ |
| E-16 | HIGH | Mic: 04 I2S vs 05 PDM, no part | PDM (MSM261D3526H1CPM / MP34DT05-A); CLK 33–100 Ω series | ✅ |
| E-17 | HIGH | Camera module I2C level, osc., EN polarity unknown | Select the module first; I2C pull-ups DNP; CAM_IO0 pull-down; 0 Ω in camera 3V3 | ✅ |
| E-18 | HIGH | MIPI PHY supply (VO3) inside the module? | module schematic | ⏳ |
| E-19 | HIGH | J5 2×8 has too few GND | 2×10; IR driver + ICR to FRONT | ✅ |
| E-20 | MEDIUM | ADC1 only on GPIO20–23, all taken | LDR removed → GPIO20 VBUS monitor | ✅ |
| E-21 | MEDIUM | Light sensor sees its own IR | switching based on camera AE/gain; opt. VEML7700, shielded | ✅ |
| E-22 | MEDIUM | Reset RC may be duplicated | module schematic | ⏳ |
| E-23 | MEDIUM | C6_EN pad missing | TP C6_EN (pad 82), C6_IO9; 10k pull-ups on C6_IO8 + IO9 | ✅ |
| E-24 | MEDIUM | USB-C shield, D± duplication, VBUS detect | 1 MΩ ‖ 4.7 nF; VBUS divider | ✅ |
| E-25 | MEDIUM | USB-JTAG is the only recovery path | UART0 pads as backup; BOOT/EN reachable when enclosed | ✅ |
| E-26 | MEDIUM | Camera 3V3 always on | load switch or CAM_IO0 pull-down | ✅ |
| E-27 | MEDIUM | RF 50 Ω under-specified | stackup first, π-network footprint | ✅ |
| E-28 | MEDIUM | PCB thickness conflict | one thickness, everything calculated for it | ✅ |
| E-29 | MEDIUM | Test point list missing | TPs + 0 Ω measurement jumpers | ✅ |
| E-30 | MEDIUM | ESD SD/FPC/header | SD ESD ≤3.5 pF; "no hot-plug" label | ✅ |
| E-31 | MEDIUM | Mic acoustics + noise | LC, distance, sealing | ✅ |
| E-32 | MEDIUM | Thermal | P4 internal temperature sensor + IR throttling | ✅ |
| E-33 | LOW | Camera current may be ~200 mA | measurement | ✅ |
| E-34 | LOW | WS2812 with 3.3 V data | discrete 0603 LED | ✅ |
| E-35 | LOW | Bench supply back-feeding | no 2nd input | ✅ |
| E-36 | LOW | 01/04 outdated statements | banner | ✅ |

### R1-P: PCB / mechanics / manufacturing (Sonnet) — 40 items

| # | Severity | Finding | Fix | St. |
|---|---|---|---|---|
| P-1 | BLOCKER | Camera module not selected → all mechanics depend on it | Procure 2–3 candidates, measure them, freeze one with a STEP model | ✅ |
| P-2 | BLOCKER | Not specified which side of MAIN the module is on; collides with the camera | Module + USB-C + u.FL + buttons on the **back** side; FPC, B2B, buck, SD on the camera-facing side; Z-stack budget | ✅ |
| P-3 | BLOCKER | 38×38 mm unrealistic (6.5 mm ring around the module) | ~45×45 mm double-sided, or 3 boards (POWER+USB / MAIN / FRONT); 1:1 mechanical sketch before the schematic | ✅ |
| P-4 | BLOCKER | 88 pads ≈ 22/side → CSI pads 41–46 wrap around the corner (41–44 side 2, 45–46 side 3); RF pad 2 + EN 87 at a corner; SD 67–72 at a corner | Waveshare footprint → real pad map; module rotation: CSI toward J2, pad 2 toward u.FL, USB pads toward USB-C | ✅ |
| P-5 | HIGH | CSI pad order vs FPC order → lane crossing with vias | Check before rotating; do not rely on lane swap | ✅ |
| P-6 | HIGH | 100 Ω diff on 2 layers: at 1.6 mm only CPW (w≈0.20–0.25 / s≈0.15–0.20 / GND gap 0.2–0.3); at 0.8 mm w≈0.30–0.35 / s≈0.2 [U] | MAIN 0.8–1.0 mm; field solver; lane rate limit (≤800 Mbps/lane, 1080p30) | ✅ |
| P-7 | HIGH | Pad → pair transition, harmonics at 2.4 GHz | ≤1 mm taper, GND pads between pairs, CSI away from RF, no TP on CSI | ✅ |
| P-8 | HIGH | 0.8 mm board: USB-C/SD mechanics, warping | **1.0 mm** + 4 standoffs + enclosure support | ✅ |
| P-9 | HIGH | 50 Ω RF on 2 layers (0.8 mm ≈1.5 mm wide; 1.0 mm ≈1.8 mm) | CPWG (w≈0.5–0.6 / gap 0.2–0.25 @0.8 mm), via fence ≤2 mm, π-network | ✅ |
| P-10 | HIGH | RF path inside the module (what is behind pad 2) undocumented | module schematic | ⏳ |
| P-11 | HIGH | Antenna position in the stack | external FPC antenna on a plastic wall, ≥15 mm from metal; plastic enclosure; early RSSI test | ✅ |
| P-12 | HIGH | u.FL mechanics weak | at the board edge, strain relief | ✅ |
| P-13 | HIGH | FPC ZIF cannot be opened in a closed stack | J2 placed at the edge, assembly order, ≥20 mm slack | ✅ |
| P-14 | HIGH | FPC length/bending | 40–60 mm, S-loop, stiffener, straight cable | ✅ |
| P-15 | HIGH | B2B header current/noise | ≥2× 5 V, ≥3 GND, GND around PDM, PWM not next to the mic; I2C pull-ups in one place | ✅ |
| P-16 | HIGH | Header height tolerance | header with a defined height, the standoff is the structural element | ✅ |
| P-17 | HIGH | IR leakage into the lens (FR4 passes 850 nm) | Cu ring + plated holes, black foam ring, LED ≥10 mm from the axis, separate window aperture | ✅ |
| P-18 | HIGH | ALS sees its own IR → oscillation | = E-21 | ✅ |
| P-19 | HIGH | Microphone acoustics | = E-31 + ≥10 mm from IR LED/ICR | ✅ |
| P-20 | HIGH | Heat 1.5–2 W in a closed box | module on the back side → gap pad to the back wall; GND vias; CC LED driver; throttling | ✅ |
| P-21 | HIGH | Assembly order, module reflow | JLC SMT for everything else, module last by hand/hot-plate | ✅ |
| P-22 | MEDIUM | Footprint mirroring / pin 1 error | Waveshare footprint import, 1:1 paper test | ✅ |
| P-23 | MEDIUM | M2 holes at the module corner pads | 33–34 mm common grid, 2.2 mm NPTH, 3.8 mm keep-out | ✅ |
| P-24 | MEDIUM | Camera mounting to FRONT not defined | 2 NPTH datums, lens hole +0.5 mm | ✅ |
| P-25 | MEDIUM | USB-C mechanics | 4 THT shell legs, held by the enclosure | ✅ |
| P-26 | MEDIUM | SMBJ + 100 µF electrolytic are large | SMAJ/SOD-123 TVS, MLCC/polymer | ✅ |
| P-27 | MEDIUM | Buck layout in a crowded corner | corner opposite the u.FL and mic | ✅ |
| P-28 | MEDIUM | IR LED ring vs lens hole | 3535 LEDs, ≥10 mm radius, back-side Cu heat spreading | ✅ |
| P-29 | MEDIUM | Test access in the stack | pogo pad group on the back side + enclosure window | ✅ |
| P-30 | MEDIUM | C6 UART pads next to the RF pad | on the opposite layer, GND between them; IO9 jumper | ✅ |
| P-31 | MEDIUM | Button/LED enclosure interface | pinhole BOOT/RESET, light pipe | ✅ |
| P-32 | MEDIUM | microSD access | board edge, enclosure slot, away from RF | ✅ |
| P-33 | MEDIUM | VO4 + 3V3 decoupling in the corner | = E-5 | ✅ |
| P-34 | MEDIUM | No panelisation | tab-route + mouse bites, 3 fiducials, boards separate | ✅ |
| P-35 | MEDIUM | JLC DFM + part availability | to be checked (header, FPC, u.FL, USB-C THT) | ✅ |
| P-36 | MEDIUM | 3-board option decision now | = P-3 | ✅ |
| P-37 | LOW | Silkscreen markings | pin 1, FPC contact side | ✅ |
| P-38 | LOW | Enclosure: ventilation, 850 nm window, IR eye safety (IEC 62471) | 06 mechanics doc | ✅ |
| P-39 | LOW | Outdoor/indoor? | indoor v1 (user confirmation) | ⏳ **deferred (enclosure, 05 §18; Q15)** |
| P-40 | LOW | USB cable strain relief | enclosure | ✅ |

### R1-F: Firmware / consistency (Haiku) — 38 items (duplicates reference the E/P items)

| # | Severity | Finding | Fix | St. |
|---|---|---|---|---|
| F-1 | BLOCKER | 01 "pin 54" = chip pin (VDD_HP_1), not GPIO54 | 01 banner; GPIO54 = E18 (esp-hosted) | ✅ |
| F-2 | HIGH | Module chip: NRW32 (v1.x?) vs v3.x for a new design | revision + availability (Q4) | ⏳ |
| F-3 | HIGH | Average 610 mA is already >500 mA in daytime | min. source **5 V / 2 A**; CC policy for every load (**superseded: B-17 FULL/MID/LOW, minimum source per power mode 4.3**) | ✅ ⟲ B-17 |
| F-4 | HIGH | SD on the VO4 domain | = E-3 | ✅ |
| F-5 | BLOCKER | Camera topology: camera on FRONT, J2 on MAIN → FPC path not defined | The camera module's own FPC goes directly into MAIN J2 (in the gap between the two boards); length/route in §6 | ✅ |
| F-6 | HIGH | IR driver location vs header, LED return path | driver to FRONT (= E-19) | ✅ |
| F-7 | MEDIUM | Mic I2S vs PDM | = E-16 (PDM) | ✅ |
| F-8 | MEDIUM | GPIO34 in the free list | = E-6 | ✅ |
| F-9 | MEDIUM | 02/04 state USB HS, 02 OTG GPIO20/21 is wrong | single USB-C → GPIO24/25; 02/04 banner | ✅ |
| F-10 | MEDIUM | 02 outdated (separate C6 module) | banner | ✅ |
| F-11 | MEDIUM | According to 03, OV5640 MIPI is not confirmed | 03 banner → E11 overrides it; pin the esp_cam_sensor version | ✅ |
| F-12 | MEDIUM | Strapping logic stated as fact | datasheet strapping table, test on the real board | ✅ |
| F-13 | MEDIUM | Reset RC 100 nF vs 1 µF | = E-22 | ⏳ |
| F-14 | MEDIUM | Camera power sequence contradictory | the module with its own LDO handles it; CAM_IO0 timing in FW | ✅ |
| F-15 | MEDIUM | Camera I/O level may be 1.8 V | = E-17 | ✅ |
| F-16 | MEDIUM | Module internal DCDC claim taken from the wiki | module schematic (Q3) | ⏳ |
| F-17 | LOW | IR LED count/wavelength/LED type not in 05 | = E-10, E-34; 850 nm | ✅ |
| F-18 | LOW | Current budget/bulk numbers differ | one set in 05 | ✅ |
| F-19 | MEDIUM | Thermal section missing (00 requirement) | = E-32/P-20, new section | ✅ |
| F-20 | MEDIUM | Coverage: stream pipeline + thermal missing; K6/K7/SD/mic/ICR partial | new sections | ✅ |
| F-21 | BLOCKER | C6 download mode not reachable | C6_EN (GPIO54) + IO9 pad with optional pull-down; document the procedure | ✅ |
| F-22 | HIGH | C6 factory firmware unknown | first step: C6 chip ID + FW version via the UART pads | ✅ |
| F-23 | MEDIUM | Is USB-JTAG enabled (eFuse)? | first bring-up | ✅ |
| F-24 | MEDIUM | UART0 pad strapping hazard | = E-6 | ✅ |
| F-25 | LOW | C6 JTAG/strapping pads | C6 JTAG not broken out in v1 | ✅ |
| F-26 | MEDIUM | esp-hosted handshake/reset GPIO for the module | Waveshare example sdkconfig | ⏳ |
| F-27 | HIGH | XCLK: not present on the 15-pin FPC | mandatory: module with its own oscillator (Q5) | ✅ |
| F-28 | HIGH | Stream pipeline not described; 03 2592×1944 vs ISP 1080p | new section: 1080p30 cap, ISP → H.264, MJPEG fallback | ✅ |
| F-29 | HIGH | PCB thickness not fixed | = P-8: 1.0 mm | ✅ |
| F-30..32 | MED/LOW | ADC1 ok, LEDC ≥20 kHz, I2S0 belongs to the mic | recorded (**LEDC → ≥40 kHz, B-30**) | ✅ ⟲ B-30 |
| F-33 | MEDIUM | No factory test plan | new section | ✅ |
| F-34 | MEDIUM | Bring-up order | new section (based on the F-34 proposal) | ✅ |
| F-35..38 | LOW/MED | EMC, footprint import, VDDPST_5/VO4 naming, E5 inference marking | recorded | ✅ |

### Summary round 1
- 114 items, of which BLOCKER: E-1..4, P-1..4, F-1, F-5, F-21 → **11**
- ⏳ external data needed (Waveshare module schematic PDF, camera module): E-18, E-22, P-10, F-2, F-16, F-26, P-39

## Review round 2 (2026-10-09) — on 05 v0.2

### R2-B: Power front-end deep analysis (Sonnet) — 30 items
| # | Severity | Finding | Fix | St. |
|---|---|---|---|---|
| B-1 | BLOCKER | USBLC6-2SC6 VBUS pin is ~5 V rated; destroyed on a 9 V VBUS | pin 5 → 3V3, or a 3.3 V array without a VBUS pin (TPD2E2U06 / PRTR5V0U2X) | ✅ |
| B-2 | HIGH | PD race: boots at 5 V, 9 V only after 0.3–1 s → wrong mode selection | mode decision after ≥1.5 s settle or PG/VBUS>8 V; continuous re-evaluation | ✅ |
| B-3 | HIGH | CC DC level jumps during PD (Rp toggle), bands as close as 90 mV | FULL = VBUS≥8 V; CC only for non-PD 5 V, median + hysteresis | ✅ |
| B-4 | HIGH | CH224K ≠ CH224A (K: no I2C, only PG) | choice: K + PG → GPIO + VBUS ADC, or an I2C sink (CH224A/HUSB238/STUSB4500) | ✅ |
| B-5 | HIGH | CH224 internal 5.1k Rd → external Rd FORBIDDEN | rule into the docs; MCU tap ≥200k (**tap value superseded: B-6 → ≥100k**; "external Rd FORBIDDEN" stays, with the rev A DNP exception: K-1) | ✅ ⟲ B-6 |
| B-6 | HIGH | CC tap 1k + 100 nF = AC load on PD BMC (max 200–600 pF); BAT54S pumps into 3V3 | ≥100k series, 10 nF at the ADC, 3.6 V Zener | ✅ |
| B-7 | HIGH | CH224 DP/DM (BC1.2/QC) conflicts with USB-JTAG D± | NC (if the datasheet allows), otherwise bring-up test | ✅ |
| B-8 | HIGH | PD hard reset → VBUS ~0 V; holdup useless | eFuse auto-retry; power-loss-tolerant NVS/OTA in FW; 20× hard reset test | ✅ |
| B-9 | HIGH | eFuse reverse current → vSafe0V check fails | reverse-blocking eFuse | ✅ |
| B-10 | HIGH | Downstream C × PD slew (30 mV/µs) → 100 µF = 3 A > ILIM | VBUS_SW effective C ≤47 µF, ILIM/timer sized for it | ✅ |
| B-11 | HIGH | VBUS 5–12 V vs OVP 10.8 V vs TVS contradict each other | **max 9 V**; adjustable-OVP eFuse 10.5–11 V | ✅ |
| B-12 | HIGH | TVS clamp vs eFuse abs-max | SMAJ10A; leakage at 9.45 V/85 °C | ✅ |
| B-13 | HIGH | CH224 floating voltage strap → 20 V request | fixed resistor to GND, a 20 V case trips the OVP | ✅ |
| B-14 | HIGH | IR CC at 5 V: 2-LED string ~4.0 V vs 4.5 V Vin → 90% duty | ≥95% duty / LDO-CC, or 3 parallel 1-LED branches | ✅ |
| B-15 | HIGH | 20 kHz PWM vs 10–22 µF on the LED | series NFET dimming, Cout ≤1 µF; large C on the input | ✅ |
| B-16 | HIGH | ICR H-bridge supply (DRV8837 VM ~11 V max) | from 3V3 or an LDO, never from VBUS_SW | ✅ |
| B-17 | MEDIUM | 5 V/1.5 A mode contradiction | three modes: FULL / MID / LOW | ✅ |
| B-18 | MEDIUM | Currents at 5.0 V, η 0.88 is optimistic | recalculation at 4.5 V, η 0.82, daytime peak column | ✅ |
| B-19 | MEDIUM | 500 mA on a PC port is not enough for boot | hard LOW boot (camera off, TX ≤10 dBm, 720p); PC = best effort | ✅ |
| B-20 | MEDIUM | UVLO not defined | eFuse UVLO ~4.4/3.9 V | ✅ |
| B-21 | MEDIUM | No supervisor | TPS3840 class on ESP_EN (after the module RC) | ✅ |
| B-22 | MEDIUM | Camera 3V3 via 0 Ω, not switched | load switch CAM_3V3 | ✅ |
| B-23 | MEDIUM | VBUS divider: TVS clamp → 4.25 V on GPIO20, back-feeding | from VBUS_SW, ≥200k/54k + Zener | ✅ |
| B-24 | MEDIUM | SD pins driven without SD power | FW tri-state before SD_EN off | ✅ |
| B-25 | MEDIUM | Shared ILIM: an IR fault resets everything | separate high-side switch for the IR branch (0.5–0.7 A) | ✅ |
| B-26 | MEDIUM | Heat underestimated (~4.5–4.9 W peak, enclosed) | thermal budget with an ambient condition; NTC (ADC2 GPIO49–53) | ✅ |
| B-27 | MEDIUM | Buck L/Cout range | datasheet check | ⏳ |
| B-28 | LOW | Capacitor DC bias at 9 V | state the effective C, 35–50 V MLCC | ✅ |
| B-29 | LOW | Header IR current step | local 10 µF + 100 nF | ✅ |
| B-30 | LOW | PDM vs 20 kHz PWM alias | LEDC ≥40 kHz | ✅ |

### R2-A: Fix verification + internal contradictions (Haiku) — 38 items
Status correction: P-1, P-4, P-5 → ⏳ (external data: camera sample, Waveshare footprint).

| # | Severity | Finding | Fix (coordinator decision) | St. |
|---|---|---|---|---|
| A-3 | HIGH | E-26: CAM_IO0 pull-down with an active-high PWDN = camera ON; no CAM_3V3 switch | CAM_3V3 load switch mandatory (= B-22) | ✅ |
| A-4 | MEDIUM | C6_IO9 10k pull-up missing | add it | ✅ |
| A-5/6 | MED/LOW | IR parts, PDM part name missing | name them [UNVERIFIED] | ✅ |
| A-7 | MEDIUM | Camera I2C level is not a gate | gate: no pull-up fitted until the camera I/O level is known | ✅ |
| A-8 | HIGH | F-3 (min. 5 V/2 A) missing | FULL/MID/LOW mode table (= B-17) | ✅ |
| A-9 | MEDIUM | No strapping check in the bring-up | §15/§16 step | ✅ |
| A-10..12 | MED/LOW | ICR [UNVER.] marking, TVS package, VEML shielding, FPC/header ESD, stiffener | add | ✅ |
| A-13 | MEDIUM | "06-mechanika" (06 mechanics) reference does not exist; IR eye safety is PCB-dependent | LED current ceiling as a PCB requirement; reference → 06-floorplan | ✅ |
| A-14/15/17/18 | LOW | CAM_IO0 timing, EMC section, "no 2nd input", §19 coverage incomplete | add | ✅ |
| A-19 | HIGH | **CSI: module at the back, J2 at the front → vias needed, but the rule forbids them** | **Decision: symmetric via pair (P+N together), with 2 GND return vias beside them, max 1 layer change per pair; J2 stays at the front (FPC in the gap)** | ✅ |
| A-20/21 | HIGH/MED | VBUS 5–12 V vs OVP vs DRV8837 | max 9 V (= B-11, B-16) | ✅ |
| A-22/23/24 | MEDIUM | CC-sense DNP / 1.5 A row / LOW mode peak >0.5 A | CC-sense + PG mandatory; mode table; LOW peak row with WiFi cap | ✅ |
| A-25 | MEDIUM | TP8 on FRONT is inaccessible | IR current shunt to MAIN (next to the IR high-side switch, = B-25) | ✅ |
| A-26 | MEDIUM | C6 UART pad "next to RF" vs "away from RF" | the module pad is next to RF; trace on the opposite layer, TPs far away | ✅ |
| A-27 | MEDIUM | SD CD pull-up to the main rail vs the rule | the rule applies only to data lines; CD on a non-VO4 GPIO | ✅ |
| A-28 | MEDIUM | VDDPST_5 = VO4 on the module? (Q1 remainder) | gate before the schematic | ⏳ |
| A-29 | MEDIUM | Per-pin strapping load table | table with datasheet ref | ⏳ (the table exists, the **datasheet reference is TODO**, 05 5.1 / Q21) |
| A-30 | MEDIUM | E4 "USB HS (48/49)" are pad numbers, not GPIOs | "P48/P49" notation | ✅ |
| A-31..33 | LOW | C6_IO8 recommended/mandatory; C6 JTAG; pad vs GPIO notation | unified; **pads with a "P" prefix** | ✅ |
| A-34 | MEDIUM | Module rotation: pad 2 (RF) and P50/51 (USB) on opposite sides | edge assignment: u.FL and USB-C on opposite edges | ✅ |
| A-35 | LOW | IR numbers unmarked | [UNVERIFIED] | ✅ |
| A-36 | MEDIUM | K8: C6 OTA not confirmed | bring-up gate + impact of the fallback | ✅ |
| A-37 | MEDIUM | ICR DNP → IR-cut extra not met in v1 | Q: choose a camera module with an ICR lens (mandatory criterion in Q5) | ✅ |
| A-38 | LOW | User button location/pull-up | back side, internal pull-up + 100 nF | ✅ |

## Review round 3 (2026-10-09) — on 05 v0.3 → v0.4, 06 v0.1 → v0.2

### R3-C: Consistency check (31 items)
| # | Finding | Fix (where) | St. |
|---|---|---|---|
| C-1 | 06: USBLC6 still listed (05: 3.3 V ESD array) | 06 2.1 → TPD2E2U06 / PRTR5V0U2X class | ✅ |
| C-2 | 06: CC-sense 1k / BAT54S (05: 100k + 10 nF + Zener) | 06 2.2 PD block; CC tap DNP rev A | ✅ |
| C-3 | 06: gap 6.0 mm (05: 7.0 mm); Z sums | 06 3. recalculated: 14.3 / 29.3 / 17.8 mm | ✅ |
| C-4 | Height limit under the camera: G − 3.2 − 0.5 = 3.3 mm @7 mm | 06 2.2, 3.2; 05 3., 7., Q8 | ✅ |
| C-5 | TP8 location: MAIN front, next to the IR switch (not in the back-side pogo group) | 05 4.2, 12; 06 2.2, 4.2, 4.4 | ✅ |
| C-6 | 06 budget: IR high-side part + shunt missing | 06 2.2 (IR branch row) | ✅ |
| C-7 | 06 budget: CAM_3V3 switch missing | 06 2.2 | ✅ |
| C-8 | 06 budget: supervisor missing | 06 2.1 (DNP rev A) | ✅ |
| C-9 | 06 budget: USER button missing | 06 2.1 (3 tact) | ✅ |
| C-10 | 06 budget: NTC missing | 06 2.2 | ✅ |
| C-11 | 06 budget: VBUS divider (after the eFuse, MAIN front) missing | 06 2.2 | ✅ |
| C-12 | eFuse bulk 35–50 V MLCC (06: ≥25 V) | 06 2.2; 05 4.1 already like this | ✅ |
| C-13 | PDM series R must not be on the MAIN back side | 06 2.1 deleted; FRONT back side (2.4) | ✅ |
| C-14 | Module 3V3 bulk: one value in both docs | 47 µF + 10 µF + 100 nF (05 4.1 power tree, 06 2.1) | ✅ |
| C-15 | TP count: TP1–TP17 in both docs | 05 12; 06 2.1 pogo group (without TP8) | ✅ |
| C-16 | FFC length text → 25–30 mm | 06 0, 3.3, K1 | ✅ |
| C-17 | Lens cutout rationale: an axis-aligned 14×14 fits through 16×16 | 06 2.3, K9; 05 3. | ✅ |
| C-18 | 05: GPIO2, 3, 4 rows missing | 05 5 (P17–P19, free) | ✅ |
| C-19 | GPIO0/1: one function (VEML INT only if J5 gets a pin; 32k XTAL option) | 05 5 | ✅ |
| C-20 | GPIO45 NC, but the sdkconfig overrides the IDF default SD power-reset pin + bring-up check | 05 5, 15/4 | ✅ |
| C-21 | Marking of pad origin (E20, primary source) | 05 E20, banner, 5, 14 | ✅ |
| C-22 | GPIO23 pull = TBD (Q5) | 05 5 | ⏳ Q5 / G3 |
| C-23 | Delete the incorrect "~5 % CC tap load" claim | 05 4.1 CC tap row | ✅ |
| C-24 | Minimum source per power mode | 05 4.3 mode table | ✅ |
| C-25 | Reference prefixes: "00-K8" / "06-K8" | 05 D8, 9, 15, Q16; 06 at the beginning | ✅ |
| C-26 | C6_IO8 pull-up mandatory everywhere | 05 E6, 5, 10; 02 note | ✅ |
| C-27 | VEML shielding note | 05 D7; 06 2.3 | ✅ |
| C-28 | 00: microphone text → PDM | 00 extra functions | ✅ |
| C-29 | Single USB naming: USB-Serial-JTAG (GPIO 24/25) | 05 E4, 5, 13 | ✅ |
| C-30 | To be confirmed: OTG FS is not used | 05 Q23 | ⏳ G0 sdkconfig |
| C-31 | 1.0 mm CPWG numbers derived from the 0.8 mm rows → field solver | 05 13 (CSI, RF) | ✅ |

### R3-K: "Prototype-killer" review (22 items)
| # | Finding | Coordinator decision / fix (where) | St. |
|---|---|---|---|
| K-1 | **BLOCKER** No independent power path (eFuse / CH224K failure = everything stops) | DNP VBUS→VBUS_SW bridge, 2× 5.1k Rd (only without CH224K), TP4 3V3 bench feed, silkscreen "NEVER BOTH" (05 0.1, 4.1) | ✅ |
| K-2 | **BLOCKER** The firmware chain has never run yet | **G0**: dev-kit stream OV5640 → ISP → H.264 → RTSP over esp-hosted C6 WiFi, 24 h soak, current per state, freeze sdkconfig + versions (05 0.2) | ⏳ gate |
| K-3 | TPS22810 has no adjustable ILIM [UNVERIFIED] | 2nd adjustable-ILIM eFuse (≥18 V) for the IR branch, or rev A: fused 0 Ω (05 D9, 4.1, 4.2) | ✅ type ⏳ G4 |
| K-4 | Incorrect sentence: "in the 20 V case the eFuse OVP protects" – the TVS is in front of the eFuse | corrected (05 4.1); G1 CH224K breakout bench test | ✅ text ⏳ G1 |
| K-5 | ICR fallback | rev A: any module with NoIR / fixed lens, ICR block DNP; ICR in rev B (05 D3, 4.2, 7) | ✅ |
| K-6 | RF: module schematic before routing | G2: read the schematic; the module's own IPEX in rev A, if available; u.FL / π / CPWG 0 Ω-DNP; 2 antennas; RSSI on the dev kit (05 3, 0.2) | ⏳ G2 |
| K-7 | Official bring-up configuration | MAIN standalone, standard 50–100 mm FFC; close the stack only after a stable image (05 0, 15) | ✅ |
| K-8 | BOM gate before the schematic | **07-bom-plan.md** skeleton + value calculation sheet; G4 (05 0.2) | ✅ skeleton ⏳ G4 |
| K-9 | Procurement list | 05 0.3 | ✅ list ⏳ procurement |
| K-10 | Module soldering method | iron + flux, external pad ≥1.5 mm, mask / keep-out under the module, USB-C distance ↑ (05 3.1; 06 2.1, K8) | ✅ |
| K-11 | 06 outdated relative to 05 v0.3 (USBLC6, BAT54S, 6 mm gap, missing switches) | 06 v0.2 regenerated | ✅ |
| K-12 | Board size | 45×45 stays; open question: rev A MAIN larger (e.g. 60×50), same M2 grid + J2/J5 coordinates (05 Q22; 06-K15) | 👤 |
| K-13 | Ordering sequence | MAIN first, FRONT later (G6) (05 0, 3) | ✅ |
| K-14 | Supervisor | open-drain variant, 0 Ω into ESP_EN, DNP rev A (05 5) | ✅ |
| K-15 | Rev A mode logic | boot LOW → FULL if VBUS_SW ≥8 V after settling; CC tap DNP (05 4.3 / rule 6) | ✅ |
| K-16 | SD block | DNP rev A, footprint stays (05 0.1, 5, 6) | ✅ |
| K-17 | C6 + UART0 header | DNP 2.54 / 1.27 mm footprint, back-side edge, away from P2 (05 6 J7; 06 2.1) | ✅ |
| K-18 | EDA / process section | 05 3.1: EDA TBD, JLC 2-layer 1.0 mm DRC, no impedance control (±10–20 %), USB-C THT question | ✅ 👤 EDA tool |
| K-19 | Shielding tube / window spacer for the IR test | 05 4.2, 15/9, 0.3 | ✅ |
| K-20 | USB-C 16-pin pin map | 07 §3 (A6/B6, A7/B7 connected; SBU NC; CC1/CC2 → CH224K) | ✅ |
| K-21 | The TBD pads of the GPIO table can be filled from the Waveshare pinout | E20 pad map, all pads filled | ✅ |
| K-22 | Camera switch CT / slew value | 07 §4; inrush measurement in bring-up step 7 | ✅ framework ⏳ G4 value |

### Summary round 3
- New content gates: G0–G6 (05 0.2). The **new ⏳ items**: C-22, C-30, K-2 (G0), K-3 type (G4), K-4 (G1), K-6 (G2), K-8 (G4), K-9 (procurement), K-22 value (G4).
- 👤 owner decision: K-12 (rev A board size), K-18 (EDA tool), Q15 (indoor v1).
- New finding outside the round (while incorporating E20): **CSI pad order differs from J2** (05 6, 06-K14) → ⏳ G2/G3.

## Review round 4 – diagram back-check (2026-10-09) — 05 v0.4 → v0.5, 06 v0.2 → v0.3, 07 v0.1 → v0.2, 08 v0.1 → v0.2

Source: reverse check of the error list (1–23) in `08-diagrams.md`. The reverse check confirmed items 1–8, 10–17 and 19–22; #9 partially (07 #38 was already FIT), #23 partially (only Q26 was missing), #18 was incorrect.

| # | Item | Fix (where) | St. |
|---|---|---|---|
| R4-1 | TP8 FIT vs DNP | 05 §0.1, §12; 07 #33 | ✅ |
| R4-2 | TP4–TP6 side | pads at the back, 0 Ω at the front (05 §12; 06 §2.1, §2.2, §4.2) | ✅ |
| R4-3 | TP9 / TP16 split, pad count | 18 pads (17 signals + TP3 GND) + 2 GND = 20 (05 §12; 06 §2.1) | ✅ |
| R4-4 | "GPIO 54 / C6_EN (P82)" label + Q2 | 05 §5, §6, §10, §12; 07 #32; 08 | ✅ label ⏳ Q2 (G2) |
| R4-5 | CH224K VDD ← raw VBUS | 05 §4.1 | ✅ |
| R4-6 | NTC, VEML7700 on the 3V3 list | 05 §4.1 | ✅ |
| R4-7 | Status LED on the MAIN back side (GPIO 6), J5.17 NC, "LEDs" clarified | 05 §0.1, §4.1, §5, §6; 06 §2.1, §2.3; 07 #30 | ✅ |
| R4-8 | 100k pull-downs on the MAIN back side | 05 §4.2, §5; 06 §2.1, §2.4; 07 #54 | ✅ |
| R4-9 | J2 ESD in §0.1 and in the front budget | 05 §0.1; 06 §2.2 | ✅ (07 #38 was already FIT) |
| R4-10 | §0.1 additions (VO4, strap, I2C, ESD, shield RC, Rd) | 05 §0.1 | ✅ |
| R4-11 | IR branch rev A = DNP, "fused 0 Ω" corrected | 05 D9, §0.1, §4.1, §4.2 | ✅ |
| R4-12 | CC ADC removed from the rev A boot sequence | 05 §4.3, §15 | ✅ |
| R4-13 | J7 = 1×9 | 05 §6; 07 #32 | ✅ |
| R4-14 | 07 passive groups | 07 #53–#60 | ✅ |
| R4-15 | CSI crossing vs 1 layer change | 05 §13 exception proposal [UNVERIFIED] | ✅ rule ⏳ Q24 (G3) |
| R4-16 | G2–G3 circularity | CSI/J2 decision in G3 (05 §0.2, §6, §14, Q24; 06 K12/K14) | ✅ |
| R4-17 | G5b gate | 05 §0.2 | ✅ |
| R4-18 | J5 GND adjacency | the rule is met | ❌ incorrect |
| R4-19 | J3, J4, J6, J7 pin tables | 05 §6 | ✅ |
| R4-20 | Unused pads (P6–P8, P11–P14, P34–P39, GND pads) | 05 §5 | ✅ |
| R4-21 | TVS + ESD on the back side, VBUS ≥2 vias to the front eFuse | 05 §3, §4.1 | ✅ |
| R4-22 | 06-K5 arithmetic (242 vs 295) | 06 K5 | ✅ |
| R4-23 | §0.4: Q26 added, Q15 👤 | 05 §0.4, §17 | ✅ (partially incorrect) |
| R4-D | Diagram errors: D1 TPC6 split (J7 DNP), CSI edge Q24; D2 SDB/TP6 split, IR_SW_EN DNP, LEDs → status LED; missing elements (Rd, shield RC, I2C pull-up) | 08 v0.2 | ✅ |
| R4-E | 06 budget recalculated: back side 429.2 → 558 mm² (50 %), front 819 → 1065 mm² (56 %), FRONT front side 95.7 (8 %), FRONT back side 315 → 410 mm² (32 %) | 06 §2 | ✅ |
| R4-F | 07 BOM rows (shield RC, pull-downs, UART0 R, GPIO 5, CH224K caps, CAM_3V3 0 Ω, FB, eFuse Rs) | 07 #53–#60 | ✅ (values ⏳ G4) |

Remaining open: Q2 (C6_EN on the module), Q24 (CSI order, G3), 07 MPNs / values (G4), the exact pogo pad count in the layout (20 pads: 17 signals + TP3 GND + 2 GND).

## Owner decisions (2026-10-09, after round 4)
| Item | Decision | Affected |
|---|---|---|
| Q22 / K-12 / 06-K15 | **Rev A MAIN 60×50 mm**, FRONT 45×45; common M2 grid + J2/J5 coordinates; final target 45×45 | 05 0, D6, 3; 06 |
| Q26 | **EDA: KiCad** (USB-C THT shell assembly still open) | 05 3.1, Q26; 07 |

## Power sheet wiring (2026-10-09)
| Item | Result |
|---|---|
| CH224K | **Discontinued** at LCSC → owner decision: **CH224A** (C42459160); the CH224D turned out to have no I2C (earlier coordinator error corrected) |
| B-4 (PD voltage readback) | ✅ solved: CH224A I2C 0x22/0x23 (reg 0x09, 0x50) |
| Q13 (eFuse type) | ✅ TPS259470ARPW, values in E22; RPW0010A footprint from the TI land pattern (`kicad/lib`) |
| Q18 (buck) | ✅ TPS62933F, values in E22 |
| `01_tap.kicad_sch` | 35 parts, ERC 0 errors on the sheet; R4/R5 DNP; JP1 open bypass |
| MCP tool bug | `batch_add_and_connect` with 38 parts timed out → **0-byte sheet file**; restored, ≤8 parts/call |

## P4 module sheet wiring (2026-10-09)
| Item | Result |
|---|---|
| `02_p4_modul.kicad_sch` | U1 88/88 pins handled (57 global labels + 31 NC); 33 passives: 3V3 decoupling (47 µF + 10 µF + 2×100 nF), VO4 1 µF, GPIO36/C6_IO9/C6_IO8 10k pull-ups, 100k pull-downs (IR_PWM, ICR_IN1/2, SD_EN, CAM_3V3_EN; IR_SW_EN DNP), status LED + 1k, NTC 10k divider, u.FL + π (0R series, 2× DNP shunt), I2C pull-ups 4.7k DNP, ESP_EN RC DNP (Q3), CC ADC tap DNP |
| New assignment | **GPIO2 (P17) = EFUSE_FLT** – it had no GPIO on the power sheet (05 §5 updated) |
| ERC | 0 errors; 23 warnings = labels of the sheets not yet drawn (camera, prog/TP, SD, B2B) |

## Programming / buttons / TP sheet (2026-10-09)
| Item | Result |
|---|---|
| `04_prog_tp.kicad_sch` | SW1 BOOT (GPIO35→GND), SW2 RESET (ESP_EN→GND), SW3 USER (GPIO5→GND, +100 nF C40); R40/R41 1k UART0 series (U0TXD/RXD → _TP); J7 1×9 1.27 mm (GND, C6_TXD, C6_RXD, C6_IO9, C6_IO8, C6_EN, U0TXD_TP, U0RXD_TP, +3V3) **DNP**; 20 pogo pads Ø1.5: TP1–TP7, TP9A/B, TP10–TP15, TP16A/B, TP17, TP18/TP19 GND |
| Supervisor (K-14) | **not drawn in rev A** (DNP; no verified KiCad symbol / pinout) – TODO text on the sheet |
| ERC | 0 errors; 18 warnings = labels of the camera / SD / B2B sheets |

## Camera sheet (2026-10-09)
| Item | Result |
|---|---|
| `03_kamera.kicad_sch` | J2 15p 1.0 mm FPC (RPi pinout, MP→GND, pin 12 NC); U6 **TPS22917DBV** CAM_3V3 switch (EN = CAM_3V3_EN, CT 1 nF, QOD → R53 0R → VOUT); R50 0R measurement jumper → CAM_3V3 (TP5); C50/C51 1 µF; CAM_PWDN: R51 pull-down / R52 pull-up **both DNP** (Q5: only one of them may be fitted) |
| TPS22918 → TPS22917 | same class; the TPS22917 pinout was checked against the KiCad library; I did not read the TPS22918 datasheet because of the cookie dialog on the TI site |
| Open (TODO text on the sheet) | Q24 CSI order, Q5 PWDN polarity, Q6 FPC contact side (the TE 1-84953-5 footprint is a placeholder), I2C pull-ups DNP, 07 #38 control-signal ESD not drawn yet |
| MCP tool bug | `batch_connect replace=true` did not delete the old global label on U6 pin 5 → deleted manually |
| ERC | 0 errors; 10 warnings = labels of the SD and B2B sheets |

## B2B J5 + IR branch and microSD sheet (2026-10-09) – first complete version of the MAIN schematic
| Item | Result |
|---|---|
| `05_b2b_front.kicad_sch` | J5 2×10 1.27 mm (05 §6 pinout; J5.17 NC), R70 47 Ω PDM_CLK series at the source (FIT). **IR branch DNP**: U7 TPS259470ARPW (EN = IR_SW_EN, OVLO → GND, RILM 6.65k = 0.5 A, CdVdt 1 nF), R72 0.1 Ω shunt + TP8A/B, R73 0R bypass, C71 10 µF → IR_VIN (J5.1/2) |
| `06_sd.kicad_sch` | **entire sheet DNP**: J3 Hirose DM3AT (DET_A → SD_CD, DET_B → GND), U8 TPS22917DBV (SD_EN), 5× 10k pull-ups to SD_3V3, CD 10k to the main 3V3, 10 µF + 100 nF; TODO: SD ESD (E-30) |
| K-3 (IR eFuse type) | ✅ TPS259470A, 0.5 A ILIM (the TPS22810 has no adjustable ILIM) |
| **Complete MAIN schematic** | 6 sheets, **131 parts (92 FIT / 39 DNP), 122 nets, ERC 0 errors / 0 warnings** |
| Open (TODO on the schematic) | Q24 CSI order, Q5 PWDN, Q6 FPC side, Q2 C6_EN, Q3 EN RC, I2C pull-up level, control-signal and SD ESD, supervisor (rev B), L1 / CH224A EP / TPD2E2U06 pinout check, B2B 7 mm type (Q17) |

## MAIN PCB placement (2026-10-09)
| Item | Result |
|---|---|
| Netlist → PCB | `kicad/MAIN/scripts/place.py` (pcbnew; the MCP does not resolve the `${KIPRJMOD}` library): 131 footprints + 4 M2 holes, 123 nets, DNP attribute + BOM/pos exclusion for the DNP parts |
| Placement | back side: U1 (22.5;25), J1 USB-C right edge y=20 (270°, opening at the board edge), D1/U5, SW1/SW2 at the top, SW3 + J7 at the bottom, pogo TPs 4×5 / 2.6 mm (x 46.5–54.3, y 29.6–40), pull-down column x=40.5, 3V3 decoupling under P84–86, RF/u.FL at P2. Front side: power chain in the extra strip (CH224A at the top, eFuse between the J1 holes, VBUS monitor, buck + L1 at the bottom), J2 between the two M2 holes on the top edge, J5 x=40.5, J3 (DNP) left edge, U6 group top-left, SD and IR (DNP) at the bottom |
| DRC | **0 courtyard / clearance / short errors**; remaining: label (silk) overlaps, 4 hole lib mismatches (cosmetic); 317 unconnected = routing missing |
| Images | `docs/img/main_revA_front_placement.png`, `docs/img/main_revA_back_placement.png` |
| Open | J2 orientation (rev A: cable toward the board edge – good for bring-up; stack variant G3), label tidy-up, routing (CSI, RF, USB, power) |

## CSI routing (2026-10-09)
| Item | Result |
|---|---|
| Script | `kicad/MAIN/scripts/route_csi.py` (idempotent: deletes and redraws the CSI copper) |
| Topology | D0 + CLK: back-side tracks above the module (y 3.6–7.5) → via pair under the J2 body → front-side stub into the J2 pad from above. D1: right-side pads → via (x 37.0 / 37.7) → front-side track under J2 (y 10.9 / 11.45) → into the J2 pad from below. **Exactly 1 layer change** per signal (05 §13) |
| **Q24 solved in layout** | D0 and D1 order is correct thanks to the turns; **CLK P/N swap at the layer change** (vias at different x), without crossing; the CLK × D1 crossing is between layers (D1 front side, CLK back side) |
| Lengths | D0 11.72/11.72, CLK 24.72/24.72, D1 20.32/20.32 mm → **0.0 mm within pairs** (D0N U-meander +3.8, CLKP bump +1.8, D1N jog +0.6). Between pairs max. ~13 mm (≈85 ps ≈ 0.07 UI @ 800 Mbps) [UNVERIFIED tolerance] |
| Geometry | 0.3 mm track, via 0.6/0.3; intra-pair coupling is loose (0.6–0.7 mm gap) → rather single-ended ~50–60 Ω behaviour with a GND pour; **GND pour + return GND vias next to the via pairs still to be done**; field solver check TODO |
| DRC | 0 errors, 0 CSI unconnected |
| Image | `docs/img/main_revA_csi_routing.png` |

## RF routing (2026-10-09)
| Item | Result |
|---|---|
| Script | `kicad/MAIN/scripts/route_rf.py` (idempotent; selects the rotation from the real pad geometry, because of the back-side mirroring) |
| Topology | back side, straight 0.7 mm line at y = 34.5: **P2 (LNA_OUT) → C27 shunt (DNP) → R34 0R series → C28 shunt (DNP)** → one 90° turn down → **J4 u.FL** (270°, centre pin up; the track does not run under the u.FL body) |
| Fix | 1st placement: R34 reversed (mirroring), J4 GND pin in the line, courtyard collision of the 0402s (3.97 mm needed in a 3.47 mm space) → rearranged |
| Length | ~5 mm + 1.8 mm ≪ λ/10 (~7 mm in FR4 at 2.4 GHz [UNVERIFIED estimate]) |
| DRC | 0 errors (1 cosmetic: J4 label at the board edge) |
| Still to do | GND pour + via fence (≤2 mm) on both sides of the line, connection of the shunt and u.FL GND pads; 0.7 mm / gap with a field solver; G2: the module's own IPEX path (K-6) |
| Image | `docs/img/main_revA_rf_routing.png` |

## USB D+/D− routing (2026-10-09)
| Item | Result |
|---|---|
| Script | `kicad/MAIN/scripts/route_usb.py` (idempotent; U5 placement based on pad geometry) |
| Topology | back side, 0.25 mm, **no via on the data lines**: P50 DM / P51 DP → **U5 ESD on the track** (IO pads on the lines, x 45.5) → J1. DM: main line → B7, A7 → L-stub in front of the pads (x 50.1). DP: main line → B6, **A6↔B6 behind the pads** (x 52.6, under the connector body, 0.3 mm from A7). U5 GND → stub + GND via (46.5; 20.0) between the two lines |
| Fixes | 1. GND via on the front-side R9 pad → moved; a stub left behind because of a parenthesisation bug in the delete condition → bounding-box-filtered cleanup |
| DRC | 0 errors; 1 "dangling via" (GND, goes away with the pour); TP9A/TP9B still unconnected (in the pogo field, during general routing) |
| Image | `docs/img/main_revA_usb_routing.png` |

## MAIN rev A – power routing (2026-10-09)
| Item | Status |
|---|---|
| Script | `kicad/MAIN/scripts/route_pwr.py` (idempotent; deletes the copper of the power nets + GND, except the USB ESD GND stub) |
| Netclass | `.kicad_pro` netclass_patterns filled in (it was empty until now): PWR = VBUS, VBUS_SW, 3V3_BUCK, BK_SW, +3V3, IR_VIN(_SH), CAM_3V3(_SW), SD_3V3; CSI_*, USB_D*, RF* |
| VBUS | J1 A4/B9 (B) → D1 TVS → 2× via (46.6, 17.2/18.2) → F trunk y 14.35 → C3 → U3.5 (0.28 mm neck, 0.2 mm pad gap). A9/B4: B → via (49.3, 23.4) → F on the west side of the R column. JP1.1, C2 (VHV), U2.8, U2.1 (VHV, B jump under the SW1/SW2 gap) |
| VBUS_SW | U3.6 at the bottom → C6 → y 27.3 → C5 → x 45.2 column → C8/C9 → U4.3. JP1.2 → B x 58.8 column. IR eFuse: B above MH4 (y 39.55) → via → U7.5. R73.1 (DNP bypass) thin F branch |
| Buck | BK_SW U4.5 → L1.1; 3V3_BUCK L1.2 → C12 → R16.1, C13; FB sense L1.2 → R14.1 (0.25) |
| +3V3 | R16.2 → 2× via (42.6, 43.6/44.6) → B y 44.06 (under MH4) → C20/C21 → module P84–86 (y 38.9 link) → C22/C23 |
| IR_VIN | C71 → F diagonal → between the J5 columns x 40.5 → J5.1/J5.2 inner end; TP8B/R72.2 at the edge (y 49.2). IR_VIN_SH: U7.6 → R72.1/TP8A, R73.2 with a B jump |
| Placement change | R16 → (44.0, 42.5) rot 270; R11 rot 180 (FLT to the right); R3 ↔ C2 swap (PG/CFG1/VHV without crossing) |
| GND | vias: C5, C6, C8, C9, C12, C13, C3/R10, R15/C10, U2 EP; U4 GND1→C8, GND4→via |
| DRC | 0 errors; 13 via_dangling (GND + R11 +3V3 via) → resolved by the pour / general routing |
| Open (general routing) | +3V3 branches: U6 (CAM switch), U8 (SD switch), C61, J5.10/11, J7.9, pull-ups (R3, R11, R20–23, R31–33, R66), TP4; TP1/TP2; BK_BST (C11), BK_FB/BK_SS, eFuse control nets, CC1/CC2, PD_PG, I2C |
| Image | `docs/img/main_revA_power_routing.png` |

## MAIN rev A – general routing, Freerouting (2026-10-09)
| Item | Status |
|---|---|
| Tool | Freerouting 2.4.1 (`~/.kicad-mcp/freerouting.jar`, GitHub release, 64 076 787 B), Java 27 |
| Preparation | `kicad/MAIN/scripts/autoroute_prep.py`: all existing copper locked (DSN `type fix`), `RF_F_KEEPOUT` rule area F.Cu (1.0–8.9 × 33.2–37.6) under the RF CPWG, GND removed from the DSN netlist (GND = pour + stitching) |
| Runs | 1st round: 60 passes, 834 new segments; 2nd round (1st round locked + re-run): +55 segments |
| Result | 1098 tracks/vias, 113 vias; **28 non-GND connections missing**, 104 GND (resolved by the pour) |
| DRC | 1 error: `solder_mask_bridge` BOOT track ↔ MH2 NPTH (37.6; 12.2); 12 via_dangling (GND) |
| Missing (28) | VBUS_MON, BK_SW→C11, SD_3V3 (2), +3V3 J5.10↔11, CAM_3V3→TP5, CAM_3V3_SW, CC2, CC2_ADC, PD_PG, NTC_ADC, SD_EN, SD_CD, SD_D3, PDM_DATA, ESP_EN (2), BOOT→TP16B, USB_DP/DM→TP9A/B, C6_TXD (2), C6_IO9 (2), C6_EN, U0RXD_TP, USER_BTN, USB_SHIELD |
| Observation | 38 B.Cu segments under the module (inside the pad ring). According to the DXF there is no centre pad → OK with mask, but the **vias must be tented**; the module underside must be checked at G3. Bottleneck: B right-side pogo/TP grid + J7 corner; many long, board-spanning nets run here (C6_*, ESP_EN, BOOT, USER_BTN) |
| Image | `docs/img/main_revA_autoroute.png` |

## MAIN rev A – TP thinning, GPIO swap v0.6, J7 relocation, routing v2 (2026-10-09)
| Item | Status |
|---|---|
| TP thinning (owner decision: option 1) | deleted: TP9A/B (USB), TP10, TP11, TP12, TP13 (C6 – duplicated by J7), TP14, TP15 (UART0 – duplicated by J7). Remaining: TP1–TP7, TP16A/B, TP17–TP19 + TP8A/B (IR). ERC 0 |
| GPIO swap v0.6 (owner decision) | SD_EN 29→53 (P81), SD_CD 30→52 (P80), CAM_3V3_EN 33→4 (P19), USER_BTN 5→33 (P60), EFUSE_FLT 2→29 (P56), PDM_DATA 13→30 (P57); freed: GPIO 2, 5, 13. ADCs unchanged. `05` §5, §0.1, §6, J3; `06`, `07` updated. **`08-diagrams.md` still shows the old assignment → regeneration + back-check needed** |
| J7 | top-left board edge, vertical (x 2.0; pin1 y 11.2 → pin9 y 1.04), above the C6 pads, away from RF |
| R27 / R28 | 100k pull-downs moved to the front side, next to U8 / U6 |
| Netclass | new `PWR_LIGHT` (0.3 mm): +3V3, SD_3V3, CAM_3V3, CAM_3V3_SW (so that the autorouter does not route the side branches at 0.6 mm); manual power spines unchanged |
| Tools | `scripts/autoroute_prep.py` (locking, RF + MH keepout r1.75, TP deletion, DSN without GND), `scripts/gpio_swap_pcb.py`, `scripts/maze/` (own A* grid router 0.05 mm, 2 layers + rip-up driver; DRC-clean result). Freerouting 2.4.1: writes an empty SES above 25 passes → `-mp 25` |
| Result | 1286 tracks, 142 vias; DRC **0 errors**; non-GND missing: **6** (LED_STAT_A, CAM_3V3_EN, I2C_SDA, C6_IO8 – top-left corner; SD_QOD at U8; +3V3 J5.10↔J5.11) |
| Image | `docs/img/main_revA_autoroute.png` |

## MAIN rev A – routing completed (non-GND) (2026-10-09)
| Item | Status |
|---|---|
| Result | **all non-GND connections done**; DRC 0 errors; schematic parity: no net mismatch; 1564 tracks, 159 vias; only the 104 GND connections (pour) + 12 GND via_dangling remain |
| Placement change | R31/R32 (I2C pull-ups, DNP) → front side (23.0; 12.5 / 14.2) next to J2 (the +3V3 wall in the top-left corner is gone); C60 ↔ C61 swap (U8 right-side pin order: SD_3V3 / QOD / CT – without crossing); **TP5 (CAM_3V3) → back side (11.6; 9.0)**, near the CAM_3V3 source – removed from the pogo group (to be taken into account in the fixture design) |
| Method | regional rip-up + Freerouting (`-mp ≤ 25`) + own A* router for the remainder (`scripts/maze/`: `kgeom.py`, `maze.py`, `ripup.py`, `cleanup.py` (DRC-UUID-based stub cleanup), `region_reroute.sh` (best-of-N, overwrites only on improvement)) |
| Quality to-dos (G-review) | (1) a few long, detouring thin (0.2 mm) tracks: +3V3 branches J5.10/11 (~67–86 mm), CAM_3V3 → TP5 (~47 mm) – low current, but can be shortened with manual push-and-shove; (2) many B.Cu tracks under the module (inside the pad ring) → via tenting mandatory, check the module underside at G3; (3) the B.Cu GND pour is fragmented by the tracks under the module → denser stitching vias needed; (4) `08-diagrams.md` GPIO v0.6 update |
| Image | `docs/img/main_revA_routed.png` |

## MAIN rev A – GND pour (2026-10-09)
| Item | Status |
|---|---|
| Zones | `scripts/gnd_pour.py`: GND_F + GND_B over the whole board, 0.2 mm clearance, thermal relief (gap 0.3 / spoke 0.35), islands removed; `ESP32-P4-CAM-MAIN.kicad_dru`: `min_resolved_spokes 1` (dense small passives) |
| Stitching vias | `scripts/maze/stitch.py`: RF fence 10 pcs (±1.05 mm from the B.Cu RF line, ≤1 mm pitch), CSI return 4/6 vias, 2 mm grid 232 pcs; `island_stitch.py` (raster-based GND component analysis → via where the island lies above the main GND on the other layer) + `gnd_fix.sh` (rip-up + GND link). Total 283 GND vias |
| RF_F_KEEPOUT | now forbids only tracks, allows vias (GND fence) |
| Status | DRC **0 errors**; open: **9 signals** (CC1, IR_ILM, PDM_CLK_J5, SD_D0, SD_D1, EFUSE_FLT, U0TXD_TP, C6_EN, LED_STAT) + **2 GND zone islands**. The rip-ups of the GND island fix broke signals; re-routing does not fully converge (Freerouting ~10–14 open, own router connects 3–5 of the remainder) |
| Recommendation | finish the remaining 9+2 manually with the KiCad interactive router (push-and-shove), then `gnd_pour.py fill` + DRC; or loosen the placement (the SD block / J3 area is the densest) |
| Image | `docs/img/main_revA_pour.png` |
| Fixed bugs | `region_reroute.sh` overwrites only on improvement + starved_thermal does not count as an error; maze: via-to-board-edge distance 0.85 mm (previously 0.65 → copper_edge error); bash 3.2 compatibility (`gnd_fix.sh`) |

## MAIN rev A – SD block loosening + GND/signal completion attempt (2026-10-09)
| Item | Status |
|---|---|
| SD loosening (owner decision) | SD pull-ups next to the J3 pins, in two columns: R62 (D1) / R65 (CMD) / R63 (D2) x 19.4; R61 (D0) / C63 / R64 (D3) x 22.4 (courtyard-collision-free); the old y≈40 loop is gone |
| Via-in-pad bug (own router) | 21 vias in SMD pads (maze layer change in the middle of the pad + island via on the pad copper) → **all removed**; from now on the router does not put a via into any SMD pad (`maze.py` V-mask). Remaining: U2 EP 2 thermal vias (intentional) |
| Stitching vias | grid vias removed → signals → re-stitching (`stitch.py`), deletion of isolated vias (not reaching the main GND) (`island_stitch.py .useless`); 309 GND vias |
| Tools | `scripts/maze/`: `guarded.sh` (per-route DRC guard, reverts), `ripall.sh`, `finish.sh`, `errs.py`, `GRID_MARGIN` env (tight pin escape) |
| Status | DRC **0 errors**, schematic parity clean, via-in-pad 0; open: **6 signals** (CAM_QOD, CC1, LED_STAT, PDM_CLK_J5, PDM_DATA, U0TXD_TP) + **14 GND** (mainly J5 GND pins / R24–R29 back-side pull-downs, J1 A12, U1 P15, U7 GND, C24) |
| Assessment | automatic rip-up/reroute stagnates here (every fix breaks something elsewhere); the 2-layer 60×50 board is saturated in the zone under the module and around J5 |
| Image | `docs/img/main_revA_pour.png` |

## MAIN rev A – J5 area rearrangement (2026-10-09)
| Item | Status |
|---|---|
| Pull-downs (owner decision, option 2) | R24 (IR_PWM), R25 (ICR_IN1), R26 (ICR_IN2), R29 (IR_SW_EN) from under J5 (B) → **front side, under the module, x 31.5 / y 22.5–27.3** (GND pin into the main F pour). `05` §5 "pull-down location: MAIN back side" → now MAIN front side under the module (K-7 is still met) |
| J5 GND | right-column GND pins (6, 12, 14, 18) locked F stub + via x 44.35 → B pour; pin 4 tied to pin 6 (USB D+ runs under it on B). Result: of the J5 GND pins only pin 15 remained open |
| Status | DRC **0 errors**, parity clean, via-in-pad 0; open: **7 signals** (CC1, EFUSE_FLT ×2, LED_STAT, PDM_CLK_J5, PDM_DATA, VBUS_MON) + **~10 GND** (mainly zone fragments; specific pads: U1 P15, J5.15, U7.2) |
| Assessment | the J5 rearrangement improved GND, signal count 6 → 7 (the regional re-route broke something else). Automation has plateaued here |
| Image | `docs/img/main_revA_pour.png` |

## Decision: MAIN 4 layers, 45×45 mm (2026-10-09)
| Item | Status |
|---|---|
| Owner decision | "the goal is a compact camera" → **4 layers, 45×45 (option A)**; K4 modified (`00`) |
| Stackup | JLC04101H-3313A (verified with a browser, JLC impedance + calculator): L1 signal / L2 GND / L3 power+GND / L4 signal; 50 Ω 0.302 mm, CSI 100 Ω 0.204/0.203, USB 90 Ω 0.262/0.203 (`05` §3.2) |
| Area requirement | 2433 mm² courtyard / ~3800 mm² → ~64 % (`06`) |
| Archive | the 2-layer 60×50 state: `kicad/archive/MAIN_2L_60x50_2026-10-09/` (not fully routed: 7 signals + ~10 GND open) |
| Next | small-part decisions (switch size, J7), then 45×45 placement on 4 layers, critical signals (CSI/RF/USB/power) by hand, the rest with Freerouting |

## MAIN v0.6 – 45×45 / 4-layer placement (2026-10-09)
| Item | Status |
|---|---|
| Part change (owner decision) | SW1–SW3 → **Omron B3U-1000P** (3.0×2.5 mm, LCSC C231329, in stock, ~0.19 USD, stock KiCad footprint; verified with a browser). Alternative: XKB TS-1088-AR02016 (4×3 mm, C720477, ~0.05 USD) – would need a footprint drawing. J7 → `ESP32-P4-CAM:PadRow_1x09_P1.27mm_SMD` (custom, 9 SMD pads). ERC 0 |
| Floorplan (owner decision) | U1 module x 20.5 (−2 mm); J1 USB-C back side right edge (40.8; 22.5); **J5 to the bottom of the front side, horizontal** (22.5; 40.2) – the FRONT board follows this |
| Scripts | `scripts/place45.py` (copper stripping, 4 layers, 45×45 R1 outline, footprint swap, block placement), `scripts/legalize.py` (courtyard spreader: fixed large parts, M2 keepout, J1 shell-leg keepout on both sides), positions: `scripts/pos_v06_45x45.json` |
| Result | DRC: **0 errors**, courtyard overlap 0, schematic parity clean |
| Image | `docs/img/main_v06_45x45_placement.png` |
| Next | layer types (In1 = GND plane, In2 = power/mixed), netclass widths per 3313A, critical routing (CSI, RF, USB, power) by hand, the rest with Freerouting (In1 excluded), GND pours |

## MAIN v0.6 – 4-layer routing, round 1 (2026-10-09)
| Item | Status |
|---|---|
| Setup | In1 = `LT_POWER` + `GND_In1` zone → DSN `plane` (Freerouting fans GND out to the plane); In2 mixed; netclasses per 3313A (CSI 0.204/0.203, USB 0.262/0.203, RF 0.302, PWR 0.4, PWR_LIGHT 0.3, Default 0.15); JLC 4-layer minimums: track 0.09, drill 0.2, via 0.45 (verified with a browser) |
| ⚠ Project file overwrite | the `.kicad_pro` was reverted twice to old settings (netclass patterns were deleted) – probably saved by the open KiCad GUI / MCP server; fix: `scripts/project_rules.py` (single source, re-applied before every DRC) |
| Tools | `scripts/prep4.py`, maze router extended to 3 layers (F/B/In2, via only if all three are free), `gnd_fanout.sh` (GND pad/island → stub + via to the In1 plane) |
| Result | 1696 tracks, 191 vias; DRC: 6 clearance (CSI vias placed with Default 0.15); **11 open**: GND 6 (C51, U7 (DNP), C10, R7, J1 A12), VBUS 2, VBUS_SW 1, CC1 1, IR_VIN_SH 1 – all around the J1/U2/U3 power block |
| ⚠ CSI quality | with the autorouter: length mismatch D0 **8.3 mm**, D1 2.6 mm, CLK 0.4 mm, no coupled pair → **not acceptable**, manual parallel, length-matched CSI routing needed (module P41–P46 → J2) |
| Image | `docs/img/main_v06_routing.png` (F / In2 / B) |

## MAIN v0.6 – manual CSI routing + round 2 (2026-10-09)
| Item | Status |
|---|---|
| CSI (`scripts/route_csi4.py`) | module P41–P46 (B) → 1 via/conductor under the module body → **F.Cu (ref. In1 GND)** → J2 pins from below; "onion": D0 inside (straight up, P/N swap using the via positions), D1 in the middle (y 15.4/15.81), CLK outside (y 16.6/17.01); width 0.204, gap ~0.203 on the coupled sections; **length: D0 9.28 / D1 14.98 / CLK 21.12 mm, pair skew 0.000** (serpentine on the shorter leg); locked |
| Corridor clearing | R24, R25, R26, R29, D2, JP1, R9, R11 moved (5–11 mm) out of the CSI corridor (F x 20.8–34.2 / y 9–18.4) |
| Finishing round | `scripts/maze/finish4.sh` (Freerouting with locked copper → GND fan-out → guarded maze), `ripall.sh`, `gnd_fanout.sh` |
| Status | DRC: 1 clearance; **14 open**: GND 5 (C51, C10, U7×2 DNP), VBUS, VBUS_SW×2, VBUS_MON, CC1, +3V3, EF_ILM, IR_VIN_SH (DNP), I2C_SCL, ESP_EN – mostly around the power block (U2/U3/U4) |
| Image | `docs/img/main_v06_routing.png` (F / In2 / B) |

## MAIN v0.6 – power block rearrangement + In2 power zones (2026-10-10)
| Item | Status |
|---|---|
| Placement (`scripts/power_place.py` + `legalize.py ONLY`) | eFuse block top-right (U3 + C3/C4/R6–R10), CH224A below J1 (U2 + C2/R2/R3), buck in one block under the module (U4, L1, C5/C6, C8–C13, R14–R16), VBUS_MON divider + NTC next to it; the legalizer now also treats locked copper (CSI) as an obstacle; `scripts/freespot.py` |
| In2 power zones | `PWR_VBUS_In2` (right strip, 171 mm²) and `PWR_VBUSSW_In2` (buck block + strip up to the eFuse output, 264 mm², not under the CSI B stubs) priority 2; `scripts/maze/zone_drop.py`: power pads get a short stub + via into their own zone (VBUS 14/14, VBUS_SW 6/11); `J1_BODY_NOVIA` rule area (no via under the metal shell); NPTH hole clearance in the router 0.3 |
| Status | DRC **0 errors**; **16 open**: GND 4, VBUS_SW 2 (U3.6 output, U7 DNP), CC1 2, PD_PG 2, PD_CFG1, EFUSE_FLT, NTC_ADC, PDM_CLK, IR_SW_EN (DNP branch), IR_VIN_SH (DNP) |
| Remaining | the remaining 16 (manual / interactive router recommended), F/B/In2 GND pour + stitching, GND vias next to the CSI vias, final DRC, `08` diagram update |
| Image | `docs/img/main_v06_routing.png` |

## MAIN v0.6 – loosening around U2 (CH224A) + U3 output (2026-10-10)
| Item | Status |
|---|---|
| U2 | rotated by 180°, (40.75; 31.05); CC/CFG1/PG pins toward J1; R2 (39.75; 35.55), R3 (37.3; 35.5), C2 (42.6; 36.4) |
| PD nets | CC1 J1 A5 → manual B stub + 0.5/0.25 via (35.56; 21.25) → U2.7; CC2 → J1 B5, PD_CFG1, PD_PG at U2 done, locked; the redundant +3V3 loop (R11 → via → back) blocking the CC1 exit deleted |
| U3 eFuse output | VBUS_SW (pad 6, 0.3×2.4 strip) **connected for the first time**: south end → 0.6/0.3 via (41.05; 15.0) → In2 0.5 mm y 14.9 → VBUS_SW zone (36.71); redundant VBUS In2 tracks inside the zone deleted |
| VBUS zone | `KO_VBUS_In2` rule area (In2, tracks forbidden, vias allowed), leaving out the corridor of the VBUS_SW feed-through; the IR_SW_EN/CAM_3V3/I2C In2 tracks cutting up the zone re-routed → **VBUS In2 zone = 1 island** (north U3 ↔ south J1/U2 over the eastern ~1.9 mm neck) |
| USB shield RC | R1/C1 moved from the B top-right corner to the F side next to the J1 shell tab (43.6; 20.6 / 23.6); the 10 mm In2 shield track is gone |
| Tool fix | `maze/kgeom.py` CLR table set to 4-layer values (Default 0.15, USB/CSI/PWR 0.2) – until now it calculated with the 2-layer 0.2/0.25 values, so it found no escape from tight pin rows; `prep4.py` `FR_RESPECT_LOCKS=1` option |
| Freerouting | no longer usable: it sees 102 rule violations of its own on the existing copper → 0 progress |
| Status | DRC **0 errors**; **21 open** (GND 6, I2C_SCL 2, VBUS (TP1), VBUS_SW (U7 DNP), SD_3V3 (TP6), +3V3 (R11), CAM_3V3 (TP5), CC2 long branch → R36, PD_PG (TP17), EF_ILM, NTC_ADC, IR_SW_EN, I2C_SDA (missing via, the spot collides with the PD_PG via), EFUSE_FLT, PDM_CLK) |
| ⚠ Observations | maze places 0.2 mm VBUS stubs (instead of PWR 0.4) – full-current stubs must be widened; USB_DM goes from J1 to the module via a northern detour (~10 mm), DP goes west → intra-pair length mismatch to be checked; the B-side TP grid (under U2) causes many long branches (TP1/5/6/17) |

## MAIN v0.6 – TP relocation + maze fixes (2026-10-10, round 2)
| Item | Status |
|---|---|
| Relocation | TP1 (VBUS) → (40.35; 32.25) next to the VBUS via; TP5 (CAM_3V3) → B (12.6; 6.6) to the CAM_3V3 net; TP6 (SD_3V3) → B (23.4; 41.6); R10 (EF_ILM) → east side of U3 (43.4; 15.6), C4 → (43.4; 18.65), R1/C1 → (43.6; 21.7 / 24.8); the 2.75 mm TP grid is thereby gone (owner decision: option 1) |
| maze fix | (1) the raster inflates by the DRC max(own, obstacle) clearance – until now PWR/PWR_LIGHT/USB nets next to a Default obstacle ended up with DRC errors and were reverted; (2) Default nets get 0.5/0.25 vias (until now all 0.6/0.3); `ripall.sh` `RIPM` box margin |
| New tool | `maze/route_all.py` (global rip-up + ordered re-routing) – tried: **worse** (48 open) → discarded, d16 state restored |
| Status | DRC **0 errors**; **20 open** (GND 9; non-GND 11: +3V3 ×2 (R11), EFUSE_FLT, I2C_SCL, I2C_SDA, PDM_CLK, U0TXD_TP, SD_3V3 (TP6), and to DNP parts only: CC2 → R5/R36, VBUS_SW → U7, IR_SW_EN → R29) |
| Done in this round | all VBUS (J1 southern pin pair, TP1), CAM_3V3 (TP5), EF_ILM, PD_PG, NTC_ADC, PDM_CLK_J5 |

## MAIN v0.6 – targeted rip-up, GND pour, loop pruning (2026-10-10, round 3)
| Item | Status |
|---|---|
| New tools | `maze/ripthru.py` (soft-obstacle maze → rips up only the tracks it cuts through, routes the target locked, re-routes the victims recursively; keeps only improvements); `maze/prune.py` (per-net spanning tree + dead-end trimming, except zoned nets) – **452 redundant elements** (maze loops) deleted, open/errors unchanged; maze `SOFT`/`SOFT_COST` mode |
| GND pour | `gnd_pour.py` fixed (until now, called without an argument it would also have deleted the GND_In1 plane!): GND_F, GND_B, GND_In2 (priority 0, the VBUS/VBUS_SW In2 zones win with priority 2) |
| Relocation | TP3 (GND) → (43.1; 40.5) |
| Done in this round | PDM_CLK, +3V3 ×2 (R11), EFUSE_FLT, I2C_SDA, IR_SW_EN (DNP branch) |
| Status | DRC **0 errors**; **13 open**: functional 4 – I2C_SCL U2.2 (CH224A I2C, B-4), I2C_SCL J2.13 (camera SCCB), U0TXD_TP (J7.7 ↔ R40.2), SD_3V3 (TP6); DNP 2 – VBUS_SW → U7, CC2 → R5/R36; GND 7 (zone islands/stitching) |
| Observation | the eastern EP–pin channel of U2 (0.75 mm) allows one track; both branches of SDA occupy it; the southern exit of SCL is blocked by locked VBUS vias (TP1, U2.1) and TP pads. In the corner under J2, the C6 bundle (In2), CAM_PWDN (F, y 8.0) and the R70/R31/R32 column block the way |

## MAIN v0.6 – remaining functional nets (2026-10-10, round 4)
| Item | Status |
|---|---|
| Board size increase | **rejected** (it would help only 1–2 of the remaining 4; a full re-route of J1/USB/CC/VBUS would be needed) – the owner allowed it on an "if it helps" condition |
| I2C_SCL (U2, CH224A) | southern branch of SDA removed (B eastern edge track x 44.12 straight), TP1 → (42.95; 32.25) next to the U2.1 VBUS via, SCL F stub in the 0.75 mm EP–pin channel → via (41.95; 33.3) → In2 westward (KO_VBUS_In2 notch y 30.2–33.75) → SCL via (30.35; 32.04); VBUS zone 1 island ✅ |
| I2C_SCL (J2, camera SCCB) | R70 (47R PDM CLK series) → **B (17.0; 8.0)** under J2 (legal-spot search + maze test); SCL on F straight down between the R31 pins ✅; PDM_CLK, PDM_CLK_J5 re-routed ✅ |
| SD_3V3 | TP6 → **B (36.3; 10.4)** ✅ |
| U3.8 GND | GND via (42.4; 13.7) → In1; EF_ILM re-routed ✅ |
| Status | DRC **0 errors**; **9 open**: U0TXD_TP (J7.7 ↔ R40.2), J1 A1 + A12 GND, GND islands (F/B pour, C24, U7 DNP), DNP: VBUS_SW → U7, CC2 → R5/R36 |
| ⚠ Critical | **J1 A1/A12 (USB-C GND) boxed in**: N the shell-tab hole, W the locked USB_DP (x 35.58) or R11/EFUSE_FLT respectively, E the J1 body (via forbidden) → the J1 breakout (USB DP/DM pair + CC + GND) must be redesigned |
| U0TXD_TP | R40/R41 in the J5 "pocket" (B2B node; enclosed by the PDM_CLK_J5, IR_VIN, SCL, U0RXD_TP lines) – a passage has to be opened, or R40/R41 + the UART route redesigned |

## MAIN v0.6 – J1 breakout redesign (2026-10-10, round 5)
| Item | Status |
|---|---|
| J1 A1 GND | the redundant northern detour of USB_DP (In2 x 35.58 → via (35.54; 18.8) → back to B) deleted, new USB_DP via (35.3; 20.5) → B to module pad 51 (DP became shorter); GND via (35.62; 19.15) + B stub to A1 ✅ |
| J1 A12 GND | R11 (EFUSE_FLT pull-up) → **B (36.0; 15.5)** (legal-spot search + maze test, modelled on `scratchpad/spotsearch.py`); CC2 B breakout redone (B5 → straight W y 24.25 → diagonal → via (37.12; 27.98)); EFUSE_FLT In2 end re-routed up to module pad 56; GND via (35.78; 26.33) to A12 ✅ |
| GND pour islands | 4-layer island stitcher (`scratchpad/stitch4.py`): 1 via; **the F islands of C2.2 (CH224A VBUS cap GND) and TH1.2 (NTC GND) are still without a via** – the soft path finder's attempt produced a short, reverted |
| Status | DRC **0 errors**; **7 open**: U0TXD_TP; GND: C2.2 and TH1.2 islands, C24, U7 (DNP); DNP: VBUS_SW → U7, CC2 → R5/R36 |
| ⚠ USB | the DM runs under the J1 body with a northern detour (~10 mm longer than the DP) – at HS the intra-pair mismatch must be checked/fixed |

## MAIN v0.6 – routing closed (2026-10-10, round 6)
| Item | Status |
|---|---|
| C2.2 GND | C2 (CH224A VBUS cap) rotated by 180° → GND pin next to the existing GND vias; VBUS to the U2.1 VBUS via ✅ |
| TH1.2 GND (NTC) | GND via (22.75; 28.15) + stub; SD_D3 and SD_CLK re-routed locally (longer, negligible at SD default speed) ✅ |
| C24 GND (VO4 cap) | GND via (31.5; 40.6) + B stub (spot search with an exact collision check; the maze raster was too conservative) ✅ |
| U0TXD_TP | U0RXD_TP thinned to 0.1 mm (on the same route), +3V3 via (18.48; 15.69) → (18.3; 15.85), U0TXD_TP with a 0.1 mm track (`TRACK_W=0.1`, GRID_MARGIN 0.01), ~56 mm, 6 vias ✅ |
| Power widening | 118 PWR/PWR_LIGHT segments → 0.4 / 0.3 mm (DRC-driven; where it did not fit, left as is) |
| USB | P50/P51 is FS USB-Serial-JTAG (12 Mbps) → the ~10 mm excess on DM is **not a problem** |
| **Final DRC** | **0 errors**; warnings: silkscreen 198 (cosmetic, refdes tidy-up before rev A), 12 dangling tracks + 2 dangling vias (T-junction bridges – deleting them causes opens, they stay), 4 lib mismatches |
| Open (DNP, rev B) | **3**: CC2 → R5/R36 (Rd / CC-ADC tap), U7 GND, VBUS_SW → U7 (IR eFuse) – parts not fitted in rev A; must be connected before they are fitted |
| Statistics | 2404 track segments, 233 vias (141 × 0.5/0.25, 91 × 0.6/0.3), 3.1 m; smallest track 0.1 mm (JLC 4L min. 0.09) |
| Image | `docs/img/main_v06_routing.png` (F / In2 / B, with pour) |
| Remaining | silkscreen tidy-up, manufacturing export (Gerber/drill/BOM/CPL), FRONT board (J5 on the bottom edge), G0–G6 gates, `08` diagrams to GPIO v0.6 |

## MAIN v0.6 – multi-agent PCB review (2026-10-10, round 7)
7 independent expert agents (power, SI, GND/EMC, RF, DFM, mechanics, electrical) + 1 sceptical re-measurer per dimension + 1 gap finder/summariser (15 agents, ~790 tool calls). They worked on a copy; the project file is untouched.

**Verdict: NO-GO for manufacturing in the current state; GO after one targeted layout round + BOM decisions + targeted re-measurement.** No fatal error (DRC 0, schematic↔PCB net parity clean, U1/U3/U4/CH224A land patterns match the datasheet/DXF, values: UVLO 4.40/4.00 V, OVLO 10.87 V, ILIM 2.03 A, FB 3.328 V, SS 1.45 ms) – the board would very likely start up, but it violates rules that cannot be fixed after manufacturing.

| Severity | Mandatory | Item | Fix |
|---|---|---|---|
| high | ✔ | **U4 buck layout**: no cap at the VIN/GND pins, loop 16 mm² with 4 via transitions, input caps' GND on a separate F island, BST/SW branch on B under the module, FB between the BST/SW pads, In1 antipad gaps (x≈31.5; y≈28) | 100 nF + 10 µF directly on pin 3/4, C11 to F on pin 5/6, R14/R15 to the FB pin, C10 to pin 7, 2–3 GND vias at the pins, break up the via columns |
| high | ✔ | **RF path (U1 P2 → R34 → J4 u.FL, FIT in rev A)**: In2 reference cut by the +3V3 and CC1_ADC tracks (19%), floating In2 island, no GND fence | +3V3/CC1_ADC out of the x 0.5–9.5 / y 33–40.5 range, In2 keep-out area, GND vias at J4 + fence with ≤2 mm pitch |
| high | ✔ | **GND stitching**: only 44 GND vias (283–309 in 2L), 25% of the F pour is >6 mm from a via (max 12.3 mm), 0 vias at the edge, GND_In2 30 islands (23 with a single via) | ~60–100 vias: edge fence 3–4 mm, grid ≤5 mm, ≥2 vias per island; target: max 6 mm via distance |
| high | ✔ | **G4 BOM gate open**: 0 MPN/LCSC fields, 73 TBDs in 07; J2 (FPC) footprint is a placeholder, contact side (Q6) open → wrong side = 3V3/GND swap at the camera; J5, L1 placeholders | MPNs; fix the J2 part + side based on the real FFC/camera |
| high | ✔ | **ESP_EN**: R23 (10k) and C25 (1 µF) DNP → nothing pulls EN up (Q3 open) | R23 + C25 FIT (BOM change only) |
| medium | ✔ | CPL/BOM: U3 footprint without `attr smd` (drops out of the CPL), U1 + MH1–4 not excluded; 51 DNP attribute mismatches | lib + board attributes, DNP sync, check CPL = 70 rows |
| medium | ✔ | U3 eFuse: 0.2 mm gaps with 100% paste (TI: 82/93%); JP1 without a solder mask dam (VBUS↔VBUS_SW bridge risk) | paste reduction, ENIG, resistance measurement before the first power-up |
| medium | ✔ | C4 (EF_DVDT) 0.28 mm from the J1 shell-tab pad (the DRC does not see it: J1 courtyard only on B) | move C4 (R9/R10) ≥1 mm, F.CrtYd ring |
| medium | ✔ | CSI return path: no via at the J2 GND pins (≥5 mm), 1 return via per pair, CSI_D0P stub above the +3V3 In2 track | via to the J2 GND pins, 2nd return via, In2 tracks out from under the CSI |
| medium | ✔ | Manufacturing specification missing: no stackup in the board (gbrjob = KiCad default), no surface finish, no rev text; 32–40 parts <5 mm from the edge | JLC04101H-3313A + impedance, ENIG, rails + fiducials, rev text |
| medium | – | CSI length: D0 9.6 / D1 15.3 / CLK 21.4 mm (data–clock 6–12 mm ≈ 0.03–0.05 UI); the "pair skew 0.000" claim is **false** (actual 1.2–1.4 mm), the zigzag tuning is ineffective | real meander or accepted deviation + G3 eye-diagram test; DRU rules |
| medium | – | 3V3 trunk: 0.15 mm neck next to the SW pad, 0.3 mm inner (0.5 oz) track, single 0.25 vias (~64 mΩ); netclass width not enforced in the DRU | ≥0.6 mm / 0.8–1.0 mm trunk, 2× 0.3 via, DRU track_width rule |
| medium | – | USB DM: ESD (U5) after the module branch; U5 GND shared with the buck input GND; DM on B above the VBUS plane | J1 → U5 → U1 order, separate GND via |
| medium | – | USB-C power input: J1 GND 2 small vias, TVS 13 mm away, VBUS neck 0.2–0.3 mm, VBUS_SW plane falls apart, no cap on the U3 output | vias, neck widening, 1 µF on U3 OUT |
| medium | – | Long open stubs to DNP parts: CC1 ~97 mm, CC1_ADC 85 mm, VBUS_SW edge stub 44.5 mm | shorten the DNP branches / 0R at the branch point |
| medium | – | Camera control ESD (05 §0.1 FIT) not in the schematic; SD ESD footprint missing; no CC protection | 3-channel ESD for J2, or formal deferral to rev B |
| medium | – | VBUS_MON: D2 Zener leakage at the 43 kΩ node can skew the 9 V / LOW decision | D2 DNP or a low-leakage clamp |
| medium | – | Shared I2C (CH224A + camera + FRONT): only the CH224A internal pull-ups; CH224A reg 0x0A can request 20/28 V | FW: CH224A read-only; preferably a separate I2C pin |
| medium | – | Mounting hole centre (22.5; 25.0) ≠ board centre; MH footprints without courtyard/keep-out, track under a screw head | record the as-built coordinates in 05/06 before the FRONT |
| low | – | CAM_3V3_EN GPIO4 during reset; paste on U1 and on the DNPs; via in the D1 pad; silkscreen 198 + no name/rev | R28 10k; paste; silkscreen |
| info | – | 312 duplicated track copies (GND 287); of the 12 "dangling" tracks only 4 are real T-bridges; incorrect claims in the 90 log: pair skew 0.000, U2 EP 2 vias, 1.9 mm VBUS neck, 10-via RF fence | cleanup on a copy; as-built update of the documents |

Refuted: electrical-14 (D1 TVS polarity is correct). Uncertain: J1 plug mating (mech-02), GPIO4 reset state (electrical-06).
Not verifiable offline: Waveshare module schematic (EN RC, RF 0R direction), ESP32-P4 datasheet (reset pulls), TPS22917/TPD2E2U06/J2/J5/L1 datasheets, JLC live capabilities/stock.
**Lesson:** "DRC 0 errors" does not mean a good layout – the round 6 "routing closed" was an overstatement; the DRC does not check the quality rules of the buck, the stitching and the RF reference.

### Corrections to earlier entries (based on the round 7 review)
Earlier entries are not rewritten. The round 7 re-measurement (the review `result.json`, confirmed by a sceptical re-measurer per dimension) found the claims below **incorrect or outdated** on the 2026-10-10 snapshot of the MAIN v0.6 board. Claims made for the 2-layer (60×50) state may have been true at the time, but they do not apply to the v0.6 board.

| Original claim (entry) | Actual, measured state (v0.6) | Source |
|---|---|---|
| "length: D0 9.28 / D1 14.98 / CLK 21.12 mm, **pair skew 0.000**" (*manual CSI routing + round 2*, 2026-10-09) | Measured length (tracks only, without duplicates): D0 9.580 / 9.580, D1 15.280 / 15.285, CLK 21.415 / 21.415 mm. The amplitude of D1N (8 zigzags, 0.145 mm) and CLKN (12 zigzags, 0.114 mm) is smaller than the 0.204 mm track width → the +1.16 / +1.37 mm centre-line excess practically **adds no delay** (the copper is just a widened ribbon). **Actual intra-pair mismatch ≈1.2–1.4 mm** (D1 ≈1.16 mm ≈7 ps, CLK ≈1.37 mm ≈8 ps; ≈0.006 UI) – functionally negligible, but the "0.000" is false. The D0N meander (0.727 mm amplitude) is real. Data–clock mismatch: D0 11.8 mm, D1 6.1 mm (≈66–70 / 36 ps; 0.053 / 0.029 UI @ 800 Mbps); CLK (21.4 mm) and D1 (15.3 mm) exceed the `05` §13 "<15 mm" rule | si-05, si-04 |
| "width 0.204, gap ~0.203 on the coupled sections" (ibid.) | the coupled section with a 0.203 mm gap is short: D0 0 / 9.58 mm, D1 5.0–5.3 / 15.3 mm, CLK 7.0 / 21.4 mm; the rest has a 0.6–0.8 mm gap (estimated Zdiff ≈115–117 Ω; within the D-PHY window, outside the 100 Ω ±10 % target) | si-06 |
| "Remaining: **U2 EP 2 thermal vias** (intentional)" (*SD block loosening*, 2026-10-09, 2-layer) | on the v0.6 board there is **no via** inside the EP (39.7–41.8 × 29.4–32.7); the only GND of the CH224A (pin 0 = EP) connects to the plane through **1 via, outside the pad** (41.175; 28.525); C2.2 (VHV cap GND) is on another F island. Low risk at ~0.11 W; check the soldering (X-ray / continuity) | power-10 |
| "VBUS In2 zone = 1 island (north U3 ↔ south J1/U2 over the eastern **~1.9 mm neck**)" (*loosening around U2 (CH224A)*, 2026-10-10) | the two halves are connected **only through a ~0.2–0.3 mm neck**: **x 41.6–42.0, y 14.8–15.2** (between the VBUS_SW via (41.05; 15.0) and the GND vias (42.42; 14.88) / (42.83; 15.62)); the eastern finger (x 43.0–43.4) is a dead end at y 15.2 because of the (42.825; 15.625) GND via. At ≤1 A the resistance and heating are negligible, but there is no margin, and the neck lies on the J1 → TVS path | power-06, power-07 |
| `PWR_VBUSSW_In2` "264 mm²" power zone (*power block rearrangement + In2 power zones*, 2026-10-10) | the zone fills as **3 islands** (80.07 / 25.08 / 15.47 mm²), connected by a 0.4 mm In2 track and single vias (U3.6 → U4.3 ≈45 mΩ, every transition 1 via – violates the `05` §4.1 "≥2 vias" rule) – it does not work as a plane | power-05 |
| "RF fence **10 pcs** (±1.05 mm from the B.Cu RF line, ≤1 mm pitch)" (*GND pour*, 2026-10-09, 2-layer) | on the v0.6 board there is **no RF fence**: 0 GND vias within 2 mm of the RF centre line; the nearest (5.742; 37.033) is at 2.01 mm, the next (7.975; 37.475) at 2.83 mm, the rest >9 mm. 44 GND vias on the whole board (out of 233; 283–309 in the 2-layer version) – lost during the 4-layer rework | si-01, rf-02, gnd_emc-01 |
| "U5 ESD on the track (IO pads on the lines)" (*USB D+/D− routing*, 2026-10-09, 2-layer) | on the v0.6 board the D− clamp sits **after the module branch**: J1.A7 → U1.50 18.78 mm, → U5.2 20.13 mm (the transient reaches the P4 pin first); the U5.3 GND shares a track and a via with the return path of the buck input cap (violates `05` §13.1). D+ is fine (J1.A6 → U5.1 3.95 mm, → U1.51 6.60 mm) | gnd_emc-04 |
| "12 dangling tracks + 2 dangling vias (**T-junction bridges** – deleting them causes opens, they stay)" (*routing closed*, round 6) | of the 12 dangling tracks **only 4 are real T-bridges** (SD_3V3 In2 0.106 mm, +3V3 In2 0.071, PD_PG F 0.224, I2C_SDA B 0.112 mm); **8 dead-end stubs** (VBUS_SW F 2.75 → DNP U7; +3V3 F 1.48; CAM_3V3 In2 4.35; CC2 B 0.78; ICR_IN2 In2 2.69; I2C_SDA F 1.85; SD_D3 B 2.11; SD_CLK B 2.60 mm) – all ≤4.35 mm, harmless, the 8 stubs can be deleted | gnd_emc-17 |
| "Statistics: **2404 track segments**" (round 6) | of these, **312 are exact duplicates** (GND 287, VBUS 23, PDM_CLK_J5 1, EFUSE_FLT 1; one segment up to 19×) → 2092 unique; this can distort the length/skew reports | gnd_emc-16, power-13 |
| "**routing closed**", "Final DRC 0 errors" (round 6 title and summary) | **overstatement**: electrically every FIT pad is connected (DRC 0, schematic ↔ PCB parity clean), but the round 7 verdict is **NO-GO**: buck input loop (no cap at the VIN/GND pins, BST/SW under the module on B), RF reference (In2 cut, no fence), GND stitching (44 vias, 30 In2 islands, 23 of them with a single via), missing J2/CSI return vias – the DRC does not check these. Correct wording: "**connected (DRC 0), a quality layout round is still to be done**" | round 7 verdict |

Documentation side: `05` (v0.6 as-built: §0.1 decisions, §3.1a frozen interface, §5, §6, §12), `06` ("As-built placement"), `07` (v0.3) and `08` (v0.3, GPIO v0.6) updated according to these corrections and the delegated decisions of 2026-10-10. The result of the layout fix passes (round 8) is recorded in a separate entry.

## MAIN v0.6 – fix passes based on the round 7 review (2026-10-10/11, round 8)
Parallel, region-fenced fixing: a full project copy + its own board region per agent, UUID-based merge-back (`kicad/MAIN/scripts/pcbmerge.py`, region guard `regioncheck.py`); every fix was re-measured by an independent verifier agent, followed by a further fix pass if anything was missing.

| Pass | Area | Result (measured) |
|---|---|---|
| pre-step | DNP stubs | CC1 (96.5 mm), CC1_ADC (85.4 mm), CC2_ADC (57.9 mm), VBUS_SW edge stub (47.2 mm) deleted – must be re-routed before rev B fitting; 255 duplicated track copies deleted; MH1–4 → stock `MountingHole_2.2mm_M2` (board-only) |
| 1 / buck | U4 TPS62933F | input loop 16.3 → ~1.4 mm² (C9 0.59 mm from the pins, without via); SW only on F (B jumper deleted); FB node 8.7 → 2.8 mm; SS 15.6 → 3.4 mm; In1 under the loop 22–41% → 92–97%; 3V3_BUCK 0.15 → 0.8 mm + F zone; U5 own GND via |
| 1 / USB-C | J1, U3, D1, C4 | C4 ≥1 mm from the J1 shell holes; J1 GND vias; VBUS neck widened; via removed from the D1 pad; CH224A EP 2nd GND via; C1 next to the shell tab |
| 1 / CSI | J2 | GND via at every J2 GND pin; 2nd return via at every CSI via pair; In2 GND under the CSI stubs + In2 keep-out area; fake zigzag → real detour (D0 9.6 → 10.4 mm); data–clock mismatch **accepted** (≈0.05 UI), to be measured at G3 |
| 1 / RF | U1.2 → R34 → J4 | +3V3 moved out from under the RF, In2 keep-out area → GND_In2 continuous under the RF line; GND fence + J4 GND vias |
| 1 / meta | schematic, lib, DRU, attrib. | R23/C25 FIT, D2 DNP, R28 10k; DNP/BOM/pos flags; U3/U7 `attr smd` + paste reduction (TI), U1 without paste; stackup JLC04101H-3313A + ENIG + impedance in the board file; DRU: PWR ≥0.4 / PWR_LIGHT ≥0.3 warning rule, PWR zones ≥1 mm from the edge |
| 2 / A (SW) | module power | +3V3 R16 → U1.84-86: 40.0 → 28.4 mΩ, 0.8 mm rail on P84-86; C21/C22/C23 under P84-86 (C22/C23 0.2 mΩ); SD_EN out of the RF box; parts around MH3 moved away |
| 2 / B (E) | USB, eFuse | USB D− clamp-first; VBUS_SW In2 plane in one piece; J1 A12/B1 2nd GND via; **C14 1 µF/25 V on U3 OUT (new part, schematic + board)** |
| 2 / C (SE) | J5 E, TP field | DNPs around MH4 moved away; PD_PG 22.8 mm detour → 2.3 mm; GND fence + island vias (max. via distance ≤5 mm) |
| 2 / D (N+W) | J2, U6, SD | MH1/C50; dangling stubs; GND stitching |
| 2 / BOM | G4 | 72 fitted items with LCSC numbers (16 Basic, 24 Extended), `fields_apply.py` → LCSC/MPN/Manufacturer fields in the schematic and on the board; J2 = TE 1-84953-5 (available, low stock) |
| **Status (05:20)** | | DRC **0 errors**, ERC 0, schematic↔board parity **0** (was 178); 12 unconnected, all DNP; track_width warnings 125 → 37; dangling 14 → 1 |

## MAIN v0.6 – final multi-agent review (2026-10-11, round 9)
**Method:** 7 dimensions (power, SI, GND/EMC, RF, DFM, mechanics, electrical) – 1 expert + 1 sceptical re-measurer per dimension, 1 critic/summariser, + the parallel silkscreen agent (**16 agents**). On the post-round-8 snapshot (md5-identical with the `kicad/MAIN` board) every round 7 item was re-measured (fixed / partially / accepted / not fixed), the new items with a sceptical check; the critic reproduced the main defect and verified the fix on a copy. The project file was not touched.

**Verdict: conditional GO for the rev A order (JLC 4-layer + double-sided PCBA)** – the design is fine, no layout change needed; **order only from a board file that has been refilled and saved in the project folder.** The only critical item is process-level: the **zone fills saved in the board file are stale** – plotted without a refill, +3V3, VBUS, VBUS_SW and ~10 signal nets would be shorted to GND (DRC without refill **173 errors**: 133 clearance, 27 hole_clearance, 13 solder_mask_bridge; 0 with refill). Verified on a copy: `kicad-cli pcb drc --refill-zones --save-board` in the project folder → DRC without refill **0 errors / 12 unconnected (all DNP) / parity 0**; the gbrjob ENIG / ImpedanceControlled / Rev A / 0.9872 mm; CPL 72 rows (47 F / 25 B). A refill **outside** the project folder produces different copper (the 1 mm edge rule of the `.kicad_dru` is lost: PWR_VBUS_In2 152.5 vs 138.6 mm²) → forbidden. The U1 module copper is the footprint verified against the DXF (only B.Paste deleted). The silkscreen agent's board has **0 copper differences** relative to the snapshot (silk DRC 214 → 0), but carries the same stale fills.

**Pre-order gate (the owner should watch it run, after the silkscreen merge, on the `kicad/MAIN` file to be ordered, with the `.kicad_pro` + `.kicad_dru` next to it):** (1) refill + save (`kicad-cli pcb drc --refill-zones --save-board …` or GUI: Fill All Zones + Save); (2) DRC without refill: 0 errors / 12 unconnected / parity 0; (3) `copper_diff.py` (review work script, not in this repository) against the review snapshot: 0 copper differences, 0 stale fills; (4) Gerber `--check-zones` + drill, the In2 layer in a Gerber viewer; (5) updated ordering note. Ordering from any Gerber older than this is forbidden.

**Round 7 items – final status** (✔ = mandatory in round 7)
| | Item | Status | Measured (round 9) |
|---|---|---|---|
| ✔ | U4 buck layout | ✅ fixed | hot loop 16.3 → **1.44 mm²** (through C9, without via); SW only on F (3.0 mm, 0 vias); FB 2.77 mm; SS 3.42 mm; In1 100 % under SW/BST/FB; 12 GND vias on the buck F-GND island |
| ✔ | RF path U1 P2 → R34 → J4 | ✅ fixed | In2 **100 % GND** under the RF (one 325.6 mm² island, 44 vias); GND vias within 1.0 / 1.5 mm: **10 / 14** (was 0 / 0); 0.302 mm all the way, path 7.96 mm; KO_RF_In2 keep-out area |
| ✔ | GND stitching | ◐ mostly | GND vias 44 → **148**; pour >6 mm from a via 235 → **0 mm²**; near-edge (≤1.5 mm) vias 0 → 38; remaining: edge fence gaps (bottom 15.4, right 18.9 / 10.75 mm), In2 32 islands, max. geodesic 12.9 mm |
| ✔ | G4 BOM gate | ◐ data complete | 72/72 FIT items with LCSC / MPN / Manufacturer fields (schematic = PCB = `BOM_jlc.csv` = CPL); open: Q6, Q17; documents updated in this round |
| ✔ | ESP_EN RC | ✅ | R23 10k (C25804) + C25 1 µF (C15849) FIT, τ = 10 ms |
| ✔ | CPL/BOM attributes | ✅ | CPL 72 rows (47 / 25); U3 `attr smd`; U1, MH, TP, JP1, DNP excluded; paste F 159 / B 65 apertures = exactly the CPL set |
| ✔ | U3 paste + JP1 | ✅ | U3 paste 82 % (pad 5/6) / 93 % (corner), per the TI RPW0010A stencil; ENIG in the board file; JP1: VBUS ↔ VBUS_SW measurement before the first power-up |
| ✔ | C4 ↔ J1 shell leg | ✅ | C4 → B (42.9; 16.2): 0.279 → **1.005 mm**; on F the nearest foreign pad is C1.2 (GND) at 0.757 mm |
| ✔ | CSI return path | ✅ | 2 GND vias per pair within ≤1 mm; J2 GND pin vias 5.05–6.13 → **0.68–1.49 mm**; In2 100 % GND under the CSI B stubs |
| ✔ | Manufacturing specification | ✅ (board file) | stackup JLC04101H-3313A, ENIG, impedance, Rev A in the board file and the gbrjob; the ordering note is outdated → owner item |
| – | CSI length / skew | accepted | D0 10.446 / D1 15.280 / CLK 21.415 mm; within pair ≤0.003 mm; data–clock 10.97 / 6.14 mm ≈ 64 / 36 ps ≈ **0.05 / 0.03 UI** @800 Mbps; G5b soak test (`05` §13, §15) |
| – | 3V3 trunk | partially | the 0.15 mm neck is gone (0.8 mm + F zone); R16.2 → U1.84–86 **21.2 mΩ** (was ~43); remaining: 2 single 0.5/0.25 vias in series |
| – | USB D− / U5 | partially, accepted for rev A | D− clamp-first (J1 → U5.2 1.85 mm); D+ on a 2.6 mm T-stub; no own via at U5.3 (nearest GND via 1.96 mm); USB is FS only |
| – | USB-C power input | partially | J1 GND 2 vias per pin pair; J1 → U3.5 7.1 mΩ; U3 IN 3 / OUT 2 vias; **C14 1 µF on U3 OUT**; VBUS In2 neck 1.05 / 0.55 mm (parallel B path); D1 position: accepted deviation |
| – | DNP stubs | ✅ | CC1 107.4 → 10.97 mm; CC1_ADC / CC2_ADC 0 mm; VBUS_SW edge stub deleted; 1 dangling +3V3 In2 stub remains (4.54 mm) |
| – | Camera / SD / CC ESD | accepted → rev B | J2 control-signal ESD, SD ESD in rev B; no CC clamp (CH224A CC abs max 32 V) → onto the rev B list |
| – | VBUS_MON D2 | ✅ | D2 DNP |
| – | Shared I2C (CH224A + camera + J5) | not fixed → FW rule | R31/R32 DNP; SDA 112.9 / SCL 63.9 mm; rise time ~0.2–0.45 µs with 10–15k / 25–35 pF → **100 kHz** |
| – | Mounting holes | accepted | stock `MountingHole_2.2mm_M2` (mask = hole, courtyard only on F); coordinates frozen; washer rule (`05` §3) |

**Corrections to the round 8 entry:** "U5 own GND via" → there is no via at the U5.3 pad: the nearest GND via is 1.96 mm away (through thermal spokes), plus a 0.25 × 2.62 mm track to a via 2.47 mm away (gnd_emc-04 dispute); "VBUS_SW In2 plane in one piece" → 1 island (147.5 mm²), but cut by 12 foreign In2 nets; between the feed and the U4 VIN vias there is only a ~0.24–0.30 mm zone connection – the current flows through the 0.5 mm In2 track and F/B links (U3.6 → U4.3 22.95 mΩ); "+3V3 … 28.4 mΩ" → 21.2 mΩ (raster DC solver; the 28.4 was calculated for tracks only); BOM note "F 48 / B 24" → **F 47 / B 25** (C4 moved to the B side).

**Remaining items (medium / low) – decision**
| Severity | Item | Decision |
|---|---|---|
| medium | Ordering package outdated; the tab range specified for the right edge falls on C3 (C3/R10/C1 0.7–0.8 mm from the right edge) | **before ordering**: JLC rails only top / bottom; no tab on the right edge for y > 5.8 and on the top edge for x 10–35; BOM + 72-row CPL (owner items) |
| medium | J1 USB-C shell legs: without paste, `attr smd` → JLC reflow will probably leave the 4 legs unsoldered | **decision before ordering**: JLC manual / selective soldering, or the owner solders them before the first cable insertion (`05` §15) |
| medium | U1 hand soldering: C23.1 (+3V3) 0.525 mm from the P87 (ESP_EN) pad tip; C21–C23 0.5 mm from the P83–86 tips – a bridge = no EN delay, SW2 3V3–GND short | **accepted for rev A + bring-up check**: fine conical tip, inspection of P87/C23; TP16A ↔ TP4 ≈ 10k (0 Ω = bridge) |
| medium | Shared I2C only with the CH224A internal pull-ups; the QOD holds CAM_3V3 at 0 V → the camera's clamp diodes can pull the bus down | **FW rule + bring-up**: 100 kHz; PD mode from PG + ADC; CH224A read-only, only after CAM_3V3; at G1 CFG2/CFG3 open-circuit voltage ≤3.3 V; R31/R32 after G3; rev B: separate I2C pin |
| low | Via drill protruding 0.03 / 0.07 mm into the R14.1 and R27.2 pads (R14 open → FB 0 V → the 3V3 may run up toward VBUS_SW) | **bring-up check**: 3V3_BUCK ↔ GND 5k–16k (>16k → R14/R15/R33); rev B: move the via |
| low | U5 = TECH PUBLIC clone (C5350871), pinout not verified | **before ordering**: LCSC datasheet, pin 3 = GND; otherwise TI C1855726; bring-up: D+/D− ↔ GND |
| low | J5 Hong Cheng pair (5.3 mm mated): ~2.3 mm engagement at 7.0 mm, generic land (Q17) | **owner decision** (Q17); rev A bring-up with the MAIN standalone |
| low | J2 contact side (Q6), JLC stock 31 pcs | stock reservation; Q6 before the camera's first power-up (does not block manufacturing) |
| low | Dangling +3V3 In2 stub (4.54 mm, via_dangling 1) | accepted for rev A (optionally deletable + re-run of the gate) |
| low | R28 10k: with the GPIO 4 pull-up during reset, the TPS22917 ON pin may sit at 0.60–0.83 V [UNVERIFIED] | **bring-up check**: TP5 = 0 V during reset; optional BOM swap 4.7k |
| low | CSI data–clock skew ≈0.05 / 0.03 UI, CLK / D1 > 15 mm | accepted for rev A; **G5b soak test with CSI error counters** |
| low | USB FS: D± B sections above VBUS_SW / void, D+ T-stub, long U5 GND return path | accepted for rev A (**FS only, never the HS PHY**); rev B: GND via ≤0.5 mm to U5.3, D+ in-line |
| low | Power distribution leftovers (+3V3 single vias, VBUS_SW zone cut by 12 nets, VBUS neck, C14 DC bias, no 100 nF on U3 IN, C24 6.26 mm, C2 2.79 mm) | accepted for rev A; optional BOM swap C14 → 2.2 µF / 25 V X7R; rev B: 2× via per layer change, 100 nF on U3.5/U3.8 |
| low | Edge stitching gaps, SDA / +3V3 0.52 mm from the edge, 0.24 mm GND_In2 ribbon | accepted for rev A; rev B: ≥0.75 mm further in, ≤4 mm fence, In2 keep-out x ≥ 43.9 |
| low | Hole spacing: different nets 0.408 mm, same net 0.253 mm (rule 0.25 ✓) | accepted for rev A, unless JLC DFM objects |
| low | Mounting holes: signal copper under the screw head (MH1/MH2 SDA 1.95 / 1.93 mm, MH4 SDA via 2.18 mm), B side without DRC | rev A: mechanical rule (nylon, `05` §3); rev B: copper keep-out ring |
| low | RF leftovers: KO_RF_In2 does not forbid non-GND vias, the tracks / fence are not locked, R34/J4 inspection was missing | **bring-up check**: R34/J4 GND fillet inspection after U1; rev B: DRU rule + locking |
| low | EMC/ESD leftovers: ESP_EN RC 13.2 mm from P87; SDA / VBUS / USB_DM under the J1 shell on B; C1 200 V (8 kV / 150 pF → ~247 V); no clamp on CC | accepted for rev A; rev B: C25 ≤2 mm from P87, no signal under J1, 1206 / 1 kV C1, CC clamp |
| low | Outdated statements in the documents | **closed in this round** (`05` §0.1, §3, §3.1, §3.1a, §4.1, §6, §13, §15; `06`; `07`; `08`) |
| info | Schematic Value fields below the ordered rated voltage (C1 "50V" → 200 V part, C9/C11/C12/C13/C20/C21); TH1 B = 3987 K | accepted for rev A (the `BOM_jlc.csv` is correct per LCSC number); FW NTC model: B = 3987 K; rev B: field sync |
| info | L1 land pattern (generic NR-50xx) vs NRS5024 drawing | JLC DFM / 3D preview at ordering |
| info | Cosmetics: acute-angle / micro segments, In1 antipad 3.39 mm², MH lib name, TP8A/TP16A annotation, D20 ~0.5 mA (dim) | rev B; optional R30 → 470 Ω |

**Owner items**
1. **Pre-order gate** (the 5 steps above) – an agent may run it, but the owner should see the successful result; we do not order from any Gerber older than that.
2. **JLC order form:** 4 layers, 45 × 45 mm (not the 45.1 of the gbrjob), 1.0 mm, stackup JLC04101H-3313A, impedance control on, ENIG, tented vias, PCBA on both sides; rails only top / bottom, no tab on the right edge (C3/R10/C1 at 0.7 mm); upload `BOM_jlc.csv` + the 72-row CPL.
3. **JLC placement preview:** check rotation and pin 1: U2, U3, U4, U5, U6, D1 (cathode = VBUS), D20, J1, J2, J4, J5 and all 25 B-side parts (cannot be verified offline).
4. **J1 shell legs:** order JLC manual / selective soldering, or solder them yourself before the first cable insertion.
5. **U5 (TECH PUBLIC C5350871):** check pin 3 = GND on LCSC; if it cannot be verified → TI C1855726.
6. **Stock reservation:** J2 C5164008 (31 pcs), U3 C3662799 (~300), R6 C22963 (180); Extended fees expected.
7. **Q6** (J2 contact side + FFC): with the real camera and cable, before the camera's first power-up – does not block PCB manufacturing.
8. **Q17** (J5 height): the Hong Cheng pair stays (MAIN unchanged; the FRONT socket height compensates, ~2.3 mm engagement at 7.0 mm) or Samtec 7.47 mm (MAIN footprint swap before ordering + 7.5 mm standoff).
9. **Optional BOM swaps on the same footprint:** R28 → 4.7k, C14 → 2.2 µF / 25 V X7R, R30 → 470 Ω.
10. **U1 hand soldering:** fine conical tip on P83–P88, then inspection of the P87/C23 gap and the R34/J4 soldering.
11. **Measurements before the first power-up:** TP16A (ESP_EN) ↔ TP4 (+3V3) ≈ 10k (0 Ω = bridge); 3V3_BUCK ↔ GND 5k–16k (with an open R14 the buck may run up to ~9 V); VBUS ↔ VBUS_SW ≈ 300k (JP1 open); VBUS / D+ / D− ↔ GND not shorted.
12. **Rev A firmware rules:** I2C 100 kHz; PD mode from PG + ADC; read the CH224A only after CAM_3V3 has been switched on, never write it; IR_SW_EN low; never enable the USB HS PHY on this layout.
13. **Mechanics:** nylon standoff or nylon washer on MH1/2/4; no washer on MH3, screw head max. Ø4.0 mm, the u.FL cable exits toward W/N.
14. **Accepted rev A deviations (sign-off):** D1 TVS at the eFuse, not at J1; CSI skew ≈0.05 UI, CLK 21.4 mm; USB FS on a VBUS_SW / void reference; single vias on the +3V3 trunk; edge fence gaps; J2 / SD / CC ESD in rev B.
15. **After ordering:** as-built update of the documents (`05` / `06` / `07` / `90`) and the CSI soak test with error counters in `05` §15 – **done 2026-10-11** (this entry and the related doc update).

Not measured: thermal conditions, buck loop stability, the real current budget, JLC live capabilities, stock and CPL rotations, the module underside, the clone / connector datasheets (not available offline).
