# 06 – Floorplan sketch: area and height budget (v0.3; as-built addendum 2026-10-10, final rev A as-built 2026-10-11)

Date: 2026-10-09 · Status: **designer's draft, for review** · Basis: `05-architecture.md` **v0.5** (Rev A plan: §0), `07-bom-plan.md`, `90-review-log.md`
Notation: **[F]** = assumption (the letter comes from the Hungarian original; not measured, not from a primary source) – to be revisited after Q5 (camera module) and the Waveshare footprint/STEP. All dimensions in mm. Reference prefix: **06-Kn** = conflict Kn of this document, **00-Kn** = requirement.
Change v0.1 → v0.2: **G = 7.0 mm** (Z sums recalculated, limit under the camera **3.3 mm**); ESD = 3.3 V array; CC tap = 100k + 10 nF + Zener (DNP rev A); TP8 on the MAIN front side; budget extended (IR eFuse #2 + shunt, CAM_3V3 switch, supervisor, USER button, NTC, VBUS divider, DNP header, bypass caps); eFuse bulk 35–50 V; PDM series R moved to the FRONT; module 3V3 bulk a single value; TP1–TP17; FFC 25–30 mm; lens cut-out rationale corrected; module footprint 28×28 (K-10); new K14 (CSI pad order), K15 (board size).
> ⚠️ **Superseded (as-built, 2026-10-10):** §0–§6 are based on the **60×50 mm / 2-layer** rev A design and a symmetric 45×45 "core" – this is **obsolete**. MAIN v0.6 is **45×45 mm, 4 layers**; the centre of the M2 hole pattern is **(22.5; 25.0)**, not the board centre (the §1 "5.75 mm from the corners" holds only in X: in Y it is 8.25 / 3.25 mm). Valid: the v0.6 sections at the end of the document, the **"As-built placement"** table and the frozen interface in `05` §3.1a. The numbers of the Z-stack (§3) and of the FRONT budget (§2.3–§2.4) remain authoritative.

Change v0.2 → v0.3 (R4): **TP plan per 05 §12** (back-side pogo group TP1–TP7, TP9–TP17 = 18 pads + 2 GND; the TP4–TP6 pads are also on the back, the 0 Ω jumpers on the front; TP8 front, DNP); **all 100k pull-downs on the MAIN back side** (removed from the FRONT); **status LED on the MAIN back side** (removed from the FRONT); J2 control-signal ESD in the front budget; USB shield RC and UART0/GPIO 5 passives on the back side; K5 arithmetic refined; the CSI decision in G3 (K14, K12).

## 0. Verdict in brief

| Question | Verdict |
|---|---|
| Area, MAIN back side (module side) | **fits** (utilisation ~50 %) |
| Area, MAIN front side (camera-facing) | **fits** (~56 % overall, ~82 % relative to the ring); at G = 7, components ≤3.3 mm may sit in the camera shadow → the overload of the W ring (06-K5) can be resolved |
| Area, FRONT both sides | **fits easily** (front ~8 %, back ~32 %); the limit is not the area but the IR LED/lens/microphone distances |
| Z-stack | **G = 7.0 mm**: ≤3.3 mm under the camera (G − 3.2 − 0.5); 6.0 mm rejected |
| Camera FFC in the gap | bring-up: **50–100 mm standard FFC, open stack, MAIN standalone**; closed stack: **25–30 mm custom cable** (06-K1) |
| CSI route module (back side) → J2 (front) | symmetric via pair (05 §13); **the pad order differs from J2** (E20) → pair crossing expected, ⏳ G3 (06-K14) |

Main reason: the area is not the bottleneck. The bottlenecks are the **edge ring** (10 mm around the 25×25 module, ~8.5 after the solder pad extension), the **Z height** and the **FFC length**.

## 1. Assumptions

**Pad numbering:** the **signal ↔ pad assignment comes from a primary source (05 E20)**; the **spatial arrangement is [F]**: module seen from the top (from the back side, looking at the module side), pad 1 in the top-left corner, numbering **counter-clockwise**, 22 pads/side, 1.0 mm pitch, centred on the side (~2 mm empty at the corners). Thus: left side 1–22 (top to bottom), bottom side 23–44 (left to right), right side 45–66 (bottom to top), top side 67–88 (right to left). Consequences (in module top-view coordinates, module 25×25, origin at the bottom-left corner of the module):

| Signal | Pad (E20) | Side / location [F] |
|---|---|---|
| RF (LNA_OUT) | P2 | left side, top (v≈32.5) |
| C6 UART/IO9/IO8 | P4, P5, P9, P10 | left side, upper third |
| CSI | P41 D0N, P42 D0P, P43 CLKP, P44 CLKN / P45 D1N, P46 D1P | right end of the bottom side / bottom of the right side → **bottom-right corner** |
| USB-Serial-JTAG D−/D+ | P50, P51 (P48/P49 HS PHY NC) | right side, 6th–7th pad from the bottom (v≈17.5–18.5) |
| BOOT/strapping/UART0 | P62 / P63, P64, P65 | upper half of the right side |
| VO4 | P66 | top-right corner |
| SD | P67–P72 | right end of the top side |
| VBAT / ESP_3V3 / EN | P84 / P85–P86 / P87 | left half of the top side |

If the actual footprint is different (e.g. CW, or the corner pads are counted), the whole assignment has to be rotated; the area and height numbers do not change.

**Coordinate system:** *product frame*: viewed from the front (lens side), X to the right, Y up; the board is 0..45 × 0..45. I draw the MAIN back side (module) **viewed from the back** (module top view); there left and right are mirrored relative to the product frame: view u = 45 − x. The module is in the centre of the board (10..35 × 10..35); **because of the solder pad extension (K-10: outward ≥1.5 mm) the footprint is 28×28**; the module is shifted 1 mm towards the edge opposite the USB-C. Rotation 0° with the numbering above → **in the product frame** CSI/J2 are in the bottom-left corner (SW), the USB-C on the left edge (W), RF/u.FL in the top-right corner (NE), SD on the left half of the top edge, the 3V3 pads on the right half of the top edge.

**Camera module [F]:** OV5640 MIPI, 25×24 mm PCB, 1.2 mm thick; on its back an FPC socket + oscillator/LDO, together max. 2.0 mm high; on the front a 14×14 square holder + M12 barrel, optics height above the PCB front plane ~18 mm (M12) or ~7 mm (Ø8 barrel AF variant). **Rev A: NoIR or fixed lens**, ICR in rev B. **Mounting variant "A"**: the module PCB lies against the rear plane of the FRONT, the holder + barrel protrude forward through a **16×16 mm** (R1 corners) cut-out. (Variant "B": the holder stays behind the FRONT, only the barrel goes through the hole → the gap would have to be ≥10 mm; not recommended.) The "lens hole +0.5 mm" of 05 is therefore a square cut-out, not a Ø hole.

**Other [F]:** B2B 2×10, 1.27 mm, SMT: ~15×6 mm, mated height **G = 7.0 mm** (availability of a 7 mm 1.27 mm-pitch B2B [UNVERIFIED], 05 Q17); board 1.0 mm; M2 holes on a 33.5 mm pattern (±16.75 from the centre → 5.75 mm from the corners), keep-out Ø3.8; edge keep-out 0.5 mm; the "+30 %" is the land/routing/keep-out allowance.

## 2. Area and height budget

> **Rev A:** the MAIN is 60×50 mm (05 0, Q22). The numbers below refer to the **45×45 final target**; in rev A there is +975 mm² of board area in the extra strip.

Available area per board: 45×45 = 2025; −edge keep-out (44×44) = 1936; −4 hole keep-outs (4×11.3) = 45.

### 2.1 MAIN – back side (module side)

Deduction: module + hand-soldering pad extension = **28×28 = 784**. **Available: 1936 − 784 − 45 = 1107 mm².**

| Component | W×H | Area | Height | Note |
|---|---|---|---|---|
| USB-C 16 pin (top/mid-mount, THT shell) | 9.4×7.5 | 70.5 | 3.2 | with the 1 mm module shift, ≥2 mm clearance from the pad extension (06-K8) |
| TVS (SMA/SMAJ10A class) | 6.8×3.0 | 20.4 | 2.4 | next to the USB-C |
| USB ESD **3.3 V array** (TPD2E2U06 / PRTR5V0U2X class, no VBUS pin) | 2.9×2.4 | 7 | 1.1 | USBLC6-2SC6 removed (05 B-1) |
| u.FL + π network (3×0603) – every element 0 Ω / DNP-capable | 3.4×3.0 + 6×2 | 22 | 1.25 | rev A: the module's own IPEX is an alternative (05 G2) |
| BOOT + RESET + **USER** (3× SMD tact) | 3× 4.5×3.8 | 51.3 | 2.0 | at the board edge |
| **Supervisor** (open-drain) + 0 Ω → ESP_EN + 100 nF (**DNP rev A**) | – | 12 | 1.0 | near EN (P87) |
| Module 3V3 bulk (**47 µF 1210 + 10 µF 0805 + 100 nF**) | – | 22 | 2.5 | at pads P84–P86; a single value, identical to 05 |
| VO4 1 µF + TP, strapping/pull-ups (6×0603) | – | 33 | 0.5 | C6_IO8/IO9 10k pull-up, GPIO36 10k |
| Pogo TP group **TP1–TP7, TP9–TP17** (TP9a/b, TP16a/b split in two) = **18 pads** (17 signals + TP3 GND) **+ 2 GND pads = 20 pads**, 2.0 mm grid, Ø1.5 pad | ~22×5 | 95 | 0 | the C6 TPs (TP10–13) separate, left ring; the TP4–TP6 pads are also here (the 0 Ω jumpers on the front, brought out by via, 05 §12); TP8 on the front side |
| **C6 + UART0 DNP header footprint** (1.27 / 2.54 mm) | ~12×3 | 36 | 0 (DNP) | on the edge far from pad P2 (RF) (05 K-17) |
| Status LED 0603 + series R (GPIO 6) | – | 9 | 0.6 | near the module (moved here from the FRONT, 05 §5) |
| USB shield RC (1 MΩ ‖ 4.7 nF, 2×0603) | – | 6 | 0.5 | next to the J1 THT shield legs |
| Small parts: **100k pull-downs (GPIO 26–28, 32 back side; GPIO 53, 4 front side next to the target IC – v0.6)**, UART0 series R ×2, GPIO 33 (USER) 100 nF, I2C pull-up (DNP) | – | 45 | 0.5 | the pull-downs near the module (05 K-7); the PDM series R is on the FRONT (not here); the VBUS divider on the front side |
| **Sum** | | **429.2** | | |
| **+30 %** | | **558** | | |
| **Utilization** | | **558 / 1107 = 50 %** | | |

Tallest: module 3.3 mm; USB-C 3.2 mm.

### 2.2 MAIN – front side (camera-facing)

Deduction: holes only. **Available: 1936 − 45 = 1891 mm²**; of which the ring (outside the camera shadow) ≈ 1891 − 600 = 1291 mm².

| Component | W×H | Area | Height | Note |
|---|---|---|---|---|
| J2 FPC 15 pin, 1.0 mm (ZIF) | 19×5.5 | 105 | 1.0–2.5 [F] | at the board edge, open actuator ≥ +2.5 |
| J5 B2B 2×10 receptacle | 15×6 | 90 | G/2 = 3.5 | |
| microSD push-push (**DNP rev A**) | 14.5×14 | 203 | 1.85 | at the board edge; may overhang the board edge by 1–1.5 mm |
| PD block (CH224A ESSOP10 + strap R + PG pull-up + 2× Rd **DNP** + CC tap 2×(100k, 10 nF, 3.6 V Zener) **DNP**) | – | 80 | 1.5 | the old 1k + BAT54S CC sense **removed** |
| eFuse block (TPS2595x 3×3 + 6 R/C + **2×1210 bulk 35–50 V** + 4.7 µF + VBUS→VBUS_SW 0 Ω bridge **DNP**) | – | 76 | 2.5 (1210) | |
| Buck block (TPS62933F SOT583 + L 5×5×2.8 + 2×1210 CIN + 2×0805 COUT + 5 passives + output 0 Ω/TP4) | – | 86 | **2.8 (L)** | ~75 with a 4×4×2.1 inductor |
| SD block (TPS22918 + 5 pull-ups + ESD arrays + caps; **DNP rev A**) | – | 55 | 1.1 | |
| **IR branch:** 2nd eFuse (≥18 V, ILIM 0.5–0.7 A) + ~10 passives + shunt + **TP8** + fused 0 Ω footprint (**DNP rev A**) | – | 52 | 1.1 | the TPS22810 class rejected (no adjustable ILIM) |
| **CAM_3V3 load switch** (TPS22918 + CT + C + 0 Ω measurement jumper) | – | 20 | 1.1 | |
| **VBUS_SW divider** (≥200k/54k + 3.6 V Zener + 100 nF; after the eFuse) | – | 14 | 0.6 | |
| **J2 control-signal ESD** (low-C array: CAM_IO0, SCL, SDA; `07` #38) | 3×3 + pad | 8 | 1.1 | next to J2 (FIT) |
| **NTC + divider + 100 nF** (ADC2, GPIO 49) | – | 10 | 0.6 | near the buck/IR |
| Other (0 Ω measurement jumpers for TP4–TP6; the TP pads are in the back-side pogo group, brought out by via; TP8 front) | – | 20 | 0.5 | |
| **Sum** | | **819** | | |
| **+30 %** | | **1065** | | |
| **Utilization** | | **1065 / 1891 = 56 %** (relative to the ring 1065 / 1291 = 82 %) | | |

Height rule: in the camera shadow (25×24, see chapter 3), **at G = 7.0, components ≤ 3.3 mm** high may sit → the inductor (2.8), the 1210 caps (2.5) and the microSD (1.85) can also be placed in the shadow; J5 (3.5) and J2 (open actuator) go into the ring or to the edge.

### 2.3 FRONT – front side

Deduction: holes + lens cut-out 16×16 = 256. **Available: 1936 − 45 − 256 = 1635 mm².**

| Component | W×H | Area | Height |
|---|---|---|---|
| IR LED 3535 ×4 (pad + heat-spreading vias) | 4× 4.2×4.2 | 70.6 | 2.0 [F] |
| PDM microphone (+ acoustic port Ø~1) | 4.3×3.4 | 14.6 | 1.0 |
| VEML7700 (DNP) + IR shielding ring | 3.5×3.0 | 10.5 | 0.9 |
| **Sum** | | **95.7** | |
| **+30 %** | | **124** | |
| **Utilization** | | **124 / 1635 = 8 %** | |

The status LED is on the MAIN back side (2.1). VEML7700: shielded from the board's own 850 nm IR LEDs and from light leaking through the FR4 (Cu ring + black foam / window aperture), otherwise the day/night measurement oscillates (05 D7).

**Lens cut-out: 16×16 mm.** The square holder is **14×14 mm, aligned to the axes** (not rotated) – therefore it passes through the 16×16 cut-out with 1 mm/side clearance; the R1 corner rounding moves the corner of the cut-out inward by only 0.3 mm, which does not touch the corner of the holder. The 19.8 mm diagonal would only be relevant for a rotated holder (in that case 18×18 or Ø20 would be needed). The final size is to be checked against the STEP of the actual camera module [F].

### 2.4 FRONT – back side

Deduction: camera module 25×24 = 600 + holes 45. **Available: 1936 − 600 − 45 = 1291 mm².**

| Component | W×H | Area | Height |
|---|---|---|---|
| B2B 2×10 header + local 10 µF + 100 nF | 15×6 + 12 | 102 | G/2 = 3.5 |
| IR CC driver ×2 (IC SOT-23-6, inductor 4×4×1.8, Schottky, CIN/COUT 1206, Rsense, 3 small passives) | 2× 69 | 138 | 2.1 (L) |
| AO3400 ×2 (IR PWM) | 2× 9 | 18 | 1.1 |
| ICR: DRV8837 + 2 caps + J6 JST-SH 2p (**DNP rev A**; the ICR_IN pull-downs on the MAIN) | – | 37 | 1.5 |
| Microphone LC + CLK series R (33–100 Ω) | – | 10 | 0.5 |
| IR LED anode caps (Cout ≤1 µF); **the 100k pull-downs are not here but on the MAIN back side** (05 K-7) | – | 10 | 1.0 |
| **Sum** | | **315** | |
| **+30 %** | | **410** | |
| **Utilization** | | **410 / 1291 = 32 %** | |

The TP8 shunt/jumper is **not here**: it is on the MAIN front side (2.2), because on the FRONT the TP would be inaccessible in the closed stack.

Edge strips (the 9.5 mm around the camera): N and S strips ~29.7×9.5 = 282 mm² (one IR driver each, ~108 mm² with +30 %), E strip B2B, W strip ICR – it fits.

## 3. Z-stack

### 3.1 Layers (front to back, for the "G = 7.0" design point)

| Element | Thickness / height |
|---|---|
| Lens/barrel protrusion in front of the FRONT front plane | **M12: ≈ 17.0** (18 − 1.0 board) · Ø8 AF: ≈ 5.5 [F] |
| FRONT front-side component (IR LED 3535 with lens) | 2.0 [F] (behind the barrel) |
| FRONT PCB | 1.0 |
| **Gap G** (B2B mated height = M2 standoff length) | **7.0** |
| – of which the camera module PCB | 1.2 |
| – of which the module back-side components (FPC socket/osc.) | 2.0 |
| – of which free above the MAIN front side in the camera shadow | 7.0 − 3.2 = **3.8** (component limit with 0.5 air gap: **3.3**) |
| MAIN PCB | 1.0 |
| MAIN back side: P4 module (tallest) | 3.3 (USB-C 3.2, tact 2.0) |
| **Total thickness – without lens** | 2.0 + 1.0 + 7.0 + 1.0 + 3.3 = **14.3** |
| **Total – with M12 lens** | 17.0 + 1.0 + 7.0 + 1.0 + 3.3 = **29.3** |
| **Total – with Ø8 AF barrel** | 5.5 + 1.0 + 7.0 + 1.0 + 3.3 = **17.8** |

### 3.2 Gap (G) conditions

Lower bounds: G ≥ 3.2 (module) + h_max(MAIN front in the camera shadow) + 0.5 mm air gap, i.e. **h_max = G − 3.2 − 0.5**.

| G (B2B + standoff) | Max. height under the camera | Assessment |
|---|---|---|
| 5.0 | 1.3 | only 0603/0805 + ICs; **rejected** |
| 6.0 | 2.3 | the v0.1 minimum; inductor (2.8) and 1210 (2.5) only in the ring; **rejected** (05 v0.3) |
| **7.0** | **3.3** | **chosen** (05 v0.4); inductor, 1210 and microSD can also be in the shadow |
| 8.0 | 4.3 | not needed even for the FFC loop (K1): the closed stack uses a 25–30 mm cable |

Ring overlap: FRONT back-side ring components (≤ 2.1) + MAIN front ring components (≤ 2.8) = 4.9 < 7.0 − 0.5 = 6.5 → passes. The open J2 actuator (approx. +2.5 above the connector = 4.5–5.0) is opened only **before the stack is closed**, so it does not collide with the IR driver in the S strip of the FRONT back side (assembly order, 05 chapter 3).

B2B tolerance: mated height ±0.2–0.3 mm [F]; the 4 standoffs are the structural element (05 3.) → choose a 2×10 1.27 mm header with a short contact wipe path, so that it can absorb the tolerance.

### 3.3 FFC bending and J2 height

- Starting FFC lengths: the shortest stock 15 pin 1.0 mm FFC is typically ~50 mm [F]. **Rev A bring-up:** standard **50–100 mm FFC, open stack, MAIN standalone** (05 §0, K-7) – the length is not a problem here.
- Between the module FPC socket and J2 there are ~8–20 mm horizontally and ~2–3 mm vertically. From a 50 mm cable (free length ~43) **~25–33 mm excess** remains → an Ω loop, which **cannot be accommodated even in a 7 mm gap** next to the B2B and the components. Hence the **closed stack: 25–30 mm custom cable / short flex** (05 v0.3 decision, Q5/Q6 gate).
- Bend radius: for a 0.1–0.2 mm FFC, R ≥ 2 mm is recommended → an S bend needs ≥ 4 mm vertical + ≥ 4 mm horizontal space; at J2 the cable needs a ≥ 3 mm straight section outside the actuator.

## 4. Floorplan sketch (ASCII)

Drawing scale: 1 character = 1 mm horizontally, 1 line = 2 mm vertically. `O` = M2 hole (Ø3.8 keep-out). The ASCII sketch is indicative; the exact location is decided after importing the Waveshare footprint. (Pad numbers from E20, edges [F].)

### 4.1 MAIN back side (module side) – viewed from the back (mirrored X)

Module top view; pad 1 top-left. In the product frame the left side is the right side (mirroring).

```
+---------------------------------------------+
|                 SUP   rrrrr                 |   SUP: supervisor + 0 ohm (DNP) next to EN (P87)
|            ddddddddddd RSTrr                |   RST: RESET button on the top edge
|    OOO     3V3-DECdddd rrrrr         OO     |   3V3-DEC: 47 uF + 10 uF + 100 nF at pads P84-P86
|    OOO     ddddddddddd     SDvias    OO     |   SDvia: P67-P72 -> via to the front-side uSD (DNP)
|            ddddddddddd     ssssss  VO4v     |   VO4: P66, 1 uF + TP
|uuuu      ######################### vvvv     |
|uFLu      #########################          |   uFL next to P2 (DNP-capable; the module's IPEX is an alternative)
|uuuu      #########################     BOOT |   BOOT button (at the height of P62/P63)
| ccccc    #########################     bbbb |
| ccccc    #########################   tttttt |   TVS
| C6TPc    #########################   TVSttt |
| ccccc    P4 MODULE 25x25##########   UUUUUUU|   (28x28 with the pad extension)
| ccccc    #########################   UUUUUUU|   USB-C on the right edge (at the height of P50/P51), >=2 mm from the pad extension
|          #########################   USB-CUU|
|          #########################   UUUUUUU|
|          #########################   UUUUUUU|
|          #########################   eeeeee |   ESD (3.3 V array)
|          #########################   ESDeee |
|            smallpartspp  CSIviaxxxx  eeeeee |   CSIvia: P41-P46 -> via to J2 (front)
|    OOO     pppppppppppp  xxxxxxxxxx  OO  USR|   USR: USER button (GPIO5)
|    OOO  POGO TP1-7,9-17PPPPP        OO      |   POGO: TP1-TP7, TP9-TP17 (18 pads + 2 GND; TP8 front)
|  HDR(DNP)  PPPPPPPPPPPPPPPPPPPPP   LED      |   HDR: C6/UART0 header J7 (DNP), far from P2; LED: status LED (GPIO 6)
|                                             |
+---------------------------------------------+
```

- The 100k pull-downs (GPIO 26–28, 32) near the module; GPIO 53 / 4 (SD_EN / CAM_3V3_EN, v0.6) next to U8 / U6, on the back side (sic) (not shown separately in the drawing); the USB shield RC next to J1.
- The C6 TP group (`C6TP`, TP10–13) on the left edge, at the height of P4/P5/P9/P10 (v 19–28); the RF trace (P2 → u.FL) above it, ~4–5 mm away. The DNP header (`HDR`) at the bottom of the board, as far as possible from the RF pad.
- The USB-C on the right edge at v≈13–22; the TVS and the ESD directly above/below it.

### 4.2 MAIN front side (camera-facing) – product frame, viewed from the front

```
+---------------------------------------------+
|          SSSSSSSSSSSSSS                     |
|          SSSSSSSSSSSSSS  wwwwwwwww          |   uSD (DNP rev A): top edge, left half (below P67-P72, via)
|    OOO   SSSSSSSSSSSSSS  SD-SWwwww   OO     |   SD-SW: load switch, pull-ups, ESD (DNP rev A)
|    OOO   uSDSSSSSSSSSSS  wwwwwwwww   OO     |
|          SSSSSSSSSSSSSS                     |
|          SSSSSSSSSSSSSS...........          |
|          SSSSSSSSSSSSSS...........          |
|BBBBBBBBBB.........................          |
|BBBBBBBBBB.........................   555555 |   J5: B2B 2x10 on the right edge (mirror pair with the FRONT)
|BUCK+LBBBB.........................   555555 |   (L 2.8 mm: may also be in the camera shadow, <=3.3 mm)
|BBBBBBBBBB.........................   555555 |
|BBBBBBBBBBCAMERA-SHADOW (<=3.3mm)..   J55555 |   '.' = camera module shadow: only <=3.3 mm
|BBBBBBBBBB.........................   555555 |
|PD+CCDDDDD.........................   555555 |   PD: CH224A, strap, PG; CC tap + Rd DNP
|DDDDDDDDDD.........................   555555 |
|DDDDDDDDDD.........................   555555 |
|eFuse+BRG..........................  IRsw    |   BRG: VBUS->VBUS_SW bridge (DNP); IRsw: 2nd eFuse/fused 0R (DNP)
|EEEEEEEEEEFFC-stripffffff.........   TP8     |   TP8: IR shunt TP, on the MAIN front side
|EEEEEEEEEEfffffffffffffff   NTC VBUSdiv      |   NTC, VBUS divider (after the eFuse)
|    OOO JJJJJJJJJJJJJJJJJJJ  CAMsw 0R4 OO    |   J2: bottom edge, left third; CAMsw: CAM_3V3 switch; 0R4: buck output 0 ohm (the TP4 pad is in the back-side pogo group)
|    OOO J2 FPCJJJJJJJJJJJJJ  miscmmmm OO     |
|        JJJJJJJJJJJJJJJJJJJ  mmmmmmmm        |
|                                             |
+---------------------------------------------+
```

- The left ring (x 0.5–9.5) is the USB-C incoming power path: eFuse → PD+CC → buck; the 3V3 runs along the top edge / on the back-side layer to pads P84–P86 in the NE corner (06-K6).
- The buck is on the left edge, i.e. as far as possible from the u.FL (NE); at G = 7 the inductor and the eFuse bulk can also be pulled into the camera shadow (≤3.3 mm).

### 4.3 FRONT front side – product frame

```
+---------------------------------------------+
|                                             |
|                                             |
|    OOO                               OO     |
|    OOO        IIIII     IIIII        OO     |   IR LED pair (N branch, 2 LEDs in series)
|               IRIII     IRIII               |
|               IIIII     IIIII         mmm   |
|                                       MIC   |   PDM mic on the right edge (>=10 mm from the IR LEDs, ~13 mm)
|              LLLLLLLLLLLLLLLL         mmm   |
|              LLLLLLLLLLLLLLLL               |
|              LLLLLLLLLLLLLLLL               |
|              LLLLLLLLLLLLLLLL               |
|              LENS 16x16LLLLLL         ALS   |   VEML7700 (DNP) + IR shielding ring
|              LLLLLLLLLLLLLLLL         vvv   |
|              LLLLLLLLLLLLLLLL               |
|              LLLLLLLLLLLLLLLL               |
|                                             |
|               IIIII     IIIII               |   IR LED pair (S branch)
|               IRIII     IRIII               |
|    OOO        IIIII     IIIII        OO     |
|    OOO                               OO     |
|                                             |
|                                             |
+---------------------------------------------+
```

- LEDs ~14.9 mm from the lens axis (≥ 10 mm satisfied), ~4.25 mm to the edge of the cut-out → the Cu baffle ring can be ≤ 3 mm wide.

### 4.4 FRONT back side – see-through view (product frame)

```
+---------------------------------------------+
|        DDDDDDDDDDDDDD qqqq                  |   DRV-N: N branch IR CC driver + AO3400 (Q)
|        DRV-NDDDDDDDDD Qqqq                  |
|    OOO DDDDDDDDDDDDDD qqqq           OO     |
|    OOO                               lllll  |   mic LC + CLK series R behind the microphone
|                                      micll  |
|          CCCCCCCCCCCCCCCCCCCCCCCCC   lllll  |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|          CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |   B2B: same product-frame location as the MAIN J5
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
| ICRiiii  CAMERA MODULE 25x24CCCCCC   B2BBBB |   ICR (DNP rev A) in the left strip
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|                                             |
|    OOO                               OO     |
|    OOO DDDDDDDDDDDDDD Qqqq   ppp     OO     |   DRV-S: S branch driver; ppp: LED anode caps
|        DRV-SDDDDDDDDD qqqq                  |
|        DDDDDDDDDDDDDD                       |
+---------------------------------------------+
```

- The ASCII shows the 25×24 footprint of the camera module; the lens cut-out is in its centre (4.3). In the product frame the B2B sits exactly above the MAIN J5; pin 1 and mirroring are to be checked with the paper test (P-22).
- The microphone is deliberately on the right edge (not the left edge), because the MAIN buck/inductor is on the left edge, directly below the left strip of the FRONT (06-K7). **TP8 is not on the FRONT** (MAIN front side, 4.2).

### 4.5 Module rotation – the three requirements

| Requirement | Met at 0°? [F numbering] | Note |
|---|---|---|
| CSI P41–P46 → J2 | **yes**: CSI in the bottom-right corner (from the back) = SW (product frame), J2 in the left third of the bottom edge | P41–P44 on the bottom side, P45–P46 on the left side (product frame) – the P45/P46 pair goes around the corner, ~2–3 mm extra. **The pad order differs from J2 (06-K14)** |
| P2 (RF) → u.FL | **yes**: P2 = NE corner | u.FL on the upper part of the right edge, RF < 6 mm; or the module's own IPEX (rev A, G2) |
| P50/P51 → USB-C | **yes**: left edge (product frame), 6th–7th pad from the bottom | USB-C on the left edge at v≈13–22, D± with ≥2 mm clearance from the module because of the pad extension |

Side effect: the RF (P2) and the 3V3/EN pads (P84–P87) are in the same corner (NE), and the CSI and the USB in the same quadrant (SW) → both corners are crowded.

## 5. Conflicts and risks

| # | Severity | Conflict | Proposal / status |
|---|---|---|---|
| K1 | **HIGH** | Camera FFC: a 40–60 mm cable gives approx. 25–33 mm excess for the ~8–20 mm module→J2 distance; a loop cannot be made even in a 7 mm gap | **Decision (05 v0.3/v0.4):** closed stack **25–30 mm custom cable / short flex**; rev A bring-up **50–100 mm FFC, open stack**, MAIN standalone. The actual length: Q5/Q6 (G3) |
| K2 | **HIGH** | The CSI pairs go from the back-side module pad to the front-side J2 → board layer change | ✅ 05 §13: a single symmetric layer change (P+N together, 2 GND return vias), ≤1 mm at the J2 pads; the front-side GND strip remains. **Because of the pair order more may be needed → 06-K14** |
| K3 | **HIGH** | With 2 layers and double-sided assembly there is no solid bottom GND | Under the back-layer CSI/RF, a GND pour on the front layer; behind the NE corner (RF) and behind the S strip (CSI) a component keep-out on the front side (GND only). J5 (E ring, y 14–29) does not collide with the RF trace (y≈33–37) |
| K4 | MED | The 3V3 pads (P84–P86) are on the NE top edge, the buck on the W ring (~35 mm) → long 3V3 trace; the N ring is occupied by the SD on the front side (rev A: SD DNP) | 3V3 on the back-side layer in the top ring, ≥1.2 mm wide; local bulk at the pads (47 µF + 10 µF + 100 nF) |
| K5 | MED | MAIN front W ring utilisation ~100 %: the **net** PD (80) + eFuse (76) + buck (86) = **242 mm²** (without the +30 % allowance, per the rows of 2.2); **together with the 52 mm² of the IR branch (DNP rev A) ≈ 294 ≈ 295 mm²**; 282 mm² is the estimated net area of the ring | ✅ in rev A the 242 mm² (approx. 86 %) is authoritative (the IR branch is DNP, but its footprint takes up space → ~104 %); at G = 7 the inductor and the eFuse bulk (≤3.3 mm) can be pulled into the camera shadow; the CC tap is DNP |
| K6 | MED | RF pad P2, 3V3, EN, VO4 and the SD pads are all in the NE/N corner; the C6 TX/RX pads are 2 mm from P2 | Pogo/TPs moved back to the left edge, GND via fence next to the RF trace (P-30), the C6 TPs on the back side; the DNP header far from the RF pad (K-17) |
| K7 | MED | The buck/inductor is below the left strip of the FRONT; if the microphone were also in the left strip, P-27 would be violated | The microphone moved to the right edge (4.3); route the PDM CLK in the right strip, between the B2B GNDs |
| K8 | MED | USB-C depth 7.5 mm vs the 8.75 mm ring; **after the ≥1.5 mm pad extension (K-10) ~1.0 mm remains**; THT shell legs at the module footprint extension | The module shifted **1 mm towards the edge opposite the USB-C** → ≥2 mm clearance (asymmetric ring), or a mid-mount connector (board edge cut out) |
| K9 | MED | Lens cut-out: the 05 "hole +0.5 mm" is not enough for a square holder; plated square + IR baffle Cu ring | Milled square cut-out with R1 corners; the **axis-aligned 14×14 holder passes through 16×16 with 1 mm/side clearance** (the diagonal is not relevant if it is not rotated); the baffle ring Cu on both sides + black foam; check with the actual module |
| K10 | MED | microSD in the gap: the FRONT is 7 mm above it, the card can only be exchanged from the side | Fine without an enclosure (rev A: SD DNP); in an enclosure a side opening at the gap is needed (05 18.) |
| K11 | LOW | M2 holes on the 33.5 mm pattern vs J2 (x≥8.3), SD (x≥9.9), USB-C (y≥13): the keep-outs do not collide, but the corners are unusable (~45 mm² per side) | – |
| K12 | LOW | The spatial numbering assumption [F]: if the footprint is different, the corner assignments (CSI/RF/USB/SD) rotate | After the footprint import (G2) chapter 4 has to be redrawn; the CSI/J2 decision in G3 |
| K13 | LOW | IR driver S strip on the FRONT back side above the MAIN J2: 2.1 + 2.5 = 4.6 < 7.0 − 0.5 | OK at G = 7; in the closed stack the actuator is already folded down |
| K14 | **HIGH** | **CSI pad order (E20): D0N, D0P, CLKP, CLKN, D1N, D1P vs J2: D0, D1, CLK (CLK_N, CLK_P)** – the P/N order of the CLK pair is reversed, and the pair order also differs (D0–CLK–D1 vs D0–D1–CLK) → in a planar 2-layer layout at least one pair crossing / P-N twist | ⏳ **G3** (after the camera selection; G2 only gives the spatial order of the footprint): options: camera / FFC adapter order, CSI lane/polarity swap (TRM [UNVERIFIED]), via crossing at the J2 pads (rev A measurement); we do not rely on a lane swap |
| K15 | ✅ | **Board size:** rev A MAIN **60×50 mm** (decision 2026-10-09), same M2 pattern + J2/J5 coordinates; the 45×45 calculation applies to the rev B target. In rev A the W ring (100 %) and the 1.25 mm USB-C gap (K8) are resolved: USB-C, microSD, J7, pogo group into the extra strip. | closed |

## 6. Status relative to 05

The v0.1 proposals have been incorporated into **05 v0.3/v0.4**: G = 7.0 mm; square 16×16 cut-out (variant A); a symmetric via pair instead of the CSI "no via" rule; instead of the 40–60 mm FFC S loop, a 25–30 mm cable (closed stack) and a 50–100 mm FFC (rev A bring-up); the pad map assumption in 05 §14, with the E20 primary pad assignment. Q8 (Z-stack budget) is closed at G = 7 by this document; it has to be recalculated after the actual camera module (Q5/G3). Open: 06-K14 (CSI order, G3), 06-K15 (board size), the redraw after the footprint import (06-K12).


> **2026-10-09 (routing):** TP9A/B, TP10–TP15 removed (J7/USB duplicates); TP5 (CAM_3V3) moved to the upper-left part of the back side (11.6; 9.0); R31/R32 to the front side next to J2; R27/R28 to the front side next to U8/U6; J7 to the upper-left board edge (60×50 state – in v0.6 J7 is on the top edge, TP5 (12.6; 6.6): see below, "As-built placement"). Details: `90-review-log.md`.


## 45×45 mm, 4 layers – space requirement (v0.6, 2026-10-09)
Measured from the current footprints (courtyard area): front side 1134 mm², back side 1299 mm², total 2433 mm² (123 components, of which 39 DNP). Available area: ~1900 mm²/side (without the hole keep-outs and the 0.5 mm board edge) → **~64 % utilisation** (B: ~68 %, F: ~60 %). Feasible on 4 layers, with little margin.
Largest items: U1 module 812 (B), J3 microSD 278 (F, DNP), J2 FPC 246 (F), J5 B2B 117 (F), J1 USB-C 100 (B), SW1–SW3 3×51 (B, 6×6 mm), J7 38 (B, DNP).
Reduction options (decision needed): smaller tactile switches (e.g. 3×4 mm SMD: ~3×12 mm² → −115 mm²), a pad row / Tag-Connect footprint instead of J7, pogo TPs at 1.0 mm.

### 45×45 / 4-layer floorplan proposal (v0.6, 2026-10-09)
Constraints (measured courtyard): U1 28.6×28.6 (B); J1 USB-C 9.5×10.7 (B, 4 THT shell legs → also occupies the F side); J2 FPC 24.0×10.4 (F, top); J3 microSD 17.8×15.8 (F, left centre, DNP); J5 B2B 8.7×13.8 (F); M2 holes (5.75 / 39.25 ; 8.25 / 41.75).
Collision: J1 fits neither to the right (J5 on F) nor to the left (J3 on F) of the current J5/J3 → **two relocations are needed**:
1. **U1 module 2 mm to the left** (x 22.5 → 20.5): right B strip 10.2 mm → J1 fits (B, right edge, opening to the right, y ≈ 22.5).
2. **J5 to the bottom of the F side, horizontal** (≈ x 17–31, y 36–44.7): the right F strip is freed for the power block and the J1 shell legs. ⚠ The FRONT follows the new J5 location (the FRONT is not designed yet → no cost).

```
 B (module side, back view NOT mirrored, top view)         F (camera side)
 +---------------------------------------------+          +---------------------------------------------+
 |MH1  SW1 SW2 SW3  J7(padrow)   TP-grid   MH2 |          |MH1 U6/CAM-pwr [  J2 FPC 15p  ]  U2 CH224A MH2|
 |     [------- U1 module 28.6 x 28.6 ------]  |          |  R/C                           CC, PD-strap  |
 |RF   [                                    ]  J1|          |[J3     ]   pull-ups,  R24–R29   U3 eFuse     |
 |J4/π [   (under it: L3 GND, L2 GND)       ] USB|          |[microSD]   (F under module)     U4 buck + L1 |
 |LED  [                                    ]  -C|          |[ DNP   ]   U8 SD-pwr            C5/C6/C8..   |
 |     [------------------------------------]  |          |            IR block (DNP)       TH1/NTC      |
 |MH3   C20–C23 (P84–86)  C24 VO4          MH4 |          |MH3      [==== J5 B2B (horizontal) ====]  MH4 |
 +---------------------------------------------+          +---------------------------------------------+
```
Layers: L2 continuous GND; L3 power islands (VBUS/VBUS_SW/3V3) + GND under CSI/RF/USB.

## As-built placement – MAIN v0.6 (measured from the PCB, 2026-10-10)
Status: **final rev A (2026-10-11)** – after the fix passes of round 8, measured from the snapshot of round 9 (final review) (pcbnew; md5-identical to the `kicad/MAIN` board). **128 footprints (124 components + MH1–4), of which 38 DNP; F 81 + 4 MH, B 43; fitted (CPL) 72: F 47 / B 25.** ~~Status: after the round 7 review and the removal of the DNP stubs, before the round 8 layout fix passes; 127 footprints (123 + MH1–4), 39 DNP; F 81 + 4 MH, B 42~~ (2026-10-10). Coordinates: **KiCad frame** (origin at the top-left corner, X to the right, Y **downward**, F-side view; the B components are also in this frame) – into the product frame above: x unchanged, y₀₆ = 45 − y. The mechanical interface (outline, MH, J2, J5, J1, J4, J7, buttons, LED) in detail: `05` §3.1a.

| Group | Refdes | Side | Location (x; y, mm) | Note |
|---|---|---|---|---|
| P4 module | U1 | B | (20.5; 25.0); courtyard x 6.2–34.8, y 10.7–39.3 | 2 mm to the left of the board centre |
| Module 3V3 decoupling | C20 47 µF, C21 10 µF, C22/C23 100 nF | B | C20 (19.75; 42.4); C21 (14.8; 41.85) −90°; C22 (13.05; 40.75) −90°; C23 (11.55; 40.75) −90° | **round 8: under pads P84–P86** (0.8 mm B-side rail); the +3V3 pad of C22/C23 is 0.525 mm from the tips of P85–P87 → U1 hand soldering: `05` §15 |
| VO4 | C24 1 µF, TP7 | B | C24 (31.5; 41.3), TP7 (37.6; 35.0) | |
| Strap / EN | R20 (BOOT_EN), R21/R22 (C6_IO9/IO8), R23/C25 (ESP_EN RC) | B | R20 (31.5; 43.4); R21/R22 (3.2; 27.45 / 25.75); R23/C25 (3.2; 29.55 / 31.25) | R23/C25: FIT (on the board as well, round 8) |
| UART0 series R | R40/R41 1k | B | (27.0; 41.3 / 43.4) | → J7.7/J7.8 |
| USB-C + TVS | J1, D1 | B | J1 (40.8; 22.5) right edge; D1 (40.5; 13.5) below U3 | the TVS is not next to J1 but 6.8 mm away – accepted deviation (05 §0.1) |
| USB ESD | U5 | F | (34.0; 21.2) 90° | |
| USB shield RC | R1 1 MΩ, C1 4.7 nF (200 V) | F | R1 (43.6; 21.7) −90°; **C1 (43.8; 26.75) −90°** | next to the SE shell tab of J1; C1.2 has its own GND via (43.5; 28.35) |
| RF | R34 0R (FIT), C27/C28 (DNP), J4 | B | R34 (3.9; 34.5) 180°; C27 / C28 (5.55 / 2.25; 34.02) 90°, DNP; J4 (3.0; 38.3) left edge | U1 P2 (7.625; 34.5) → J4, path 7.96 mm (0.302 mm); the shunt pads on the y 34.5 line; GND fence + In2 100 % GND (round 8) |
| Buttons | SW1 BOOT / SW2 RESET / SW3 USER | B | (11.5; 3.0) / (33.5; 3.0) / (33.5; 7.4) | top edge; C40 (USER 100 nF) (29.4; 7.6) |
| Status LED | D20, R30 1k | B | (3.2; 14.35 / 16.05) | left edge |
| C6 / UART0 pad row | J7 (DNP) | B | (22.5; 2.0), horizontal | top edge |
| eFuse FLT pull-up | R11 10k | B | (36.0; 15.5) | |
| PDM CLK series R | R70 47 Ω | B | (17.0; 8.0) | below J2 |
| CC tap Zener | D21/D22 (DNP) | B | (1.8 / 4.6; 20.0) | |
| Test points | TP1–TP4, TP7, TP16A/B, TP17–TP19 / TP5 / TP6 | B | group x 37.6–43.1, y 29.5–40.5 (2.75 mm grid); TP5 (12.6; 6.6); TP6 (36.3; 10.4) | `05` §12 |
| Camera FPC | J2 | F | (22.5; 7.5), 180° | top edge, cable from the top edge |
| CAM_3V3 switch | U6, C50–C52, R50, R53, R51/R52 (DNP), R28 | F | x 2.75–12.6, y 11.0–16.3; U6 (3.6; 13.7), C50 (2.75; 11.0), R28 (3.0; 16.3) | top-left; R28 = 10k; C50 0.25 mm to the left (MH1 courtyard) |
| I2C pull-up | R31/R32 (DNP) | F | (16.4; 14.2 / 15.9) | |
| GPIO pull-downs | R24, R25, R26, R29 (DNP) | F | (19.8; 13.6), (24.05; 19.45), (19.75; 16.8), (35.45; 8.7) | next to the CSI corridor |
| eFuse block | U3, R6–R10, C3, C4, **C14**, JP1 | F (C4: **B**) | U3 (40.8; 13.4); R6 (36.2; 11.25), R7 (36.0; 12.95), R8 (35.95; 14.65), R9 (35.95; 16.2); **R10 (43.8; 12.75) −90°; C3 (43.5; 9.45) 90°; C4 → B (42.9; 16.2); C14 new (42.675; 16.0)**; JP1 (36.4; 4.5) | top-right; C4 1.005 mm from the J1 shell leg; C14 (1 µF, U3 OUT) 1.14 mm from U3.6; **C3 / R10 / C1 0.7–0.8 mm from the right edge → no panel tab there** |
| PD (CH224A) | U2, R2, R3, C2 | F | U2 (40.75; 31.05) 180°; R2 (39.75; 35.55); R3 (37.3; 35.5); C2 (42.6; 36.4) | right, below J1 |
| Buck | U4, L1, C5, C6, C8–C13, R14–R16 | F | **U4 (29.4; 25.74), L1 (31.4; 30.02) −90°**; C5 (27.35; 20.45), C6 (30.65; 20.5), C8 (25.46; 26.25), C9 (27.26; 26.465), C10 (33.17; 24.2), C11 (32.85; 26.45), C12 (27.55; 29.74), C13 (25.48; 29.74), R14 (27.915; 23.62), R15 (30.965; 23.62), R16 (26.6; 32.48) 180°; courtyard x 24.4–34.4, y 18.1–33.5 | centre-right, behind the module (B); **round 8 rearrangement**: C9 at the VIN/GND pins (hot loop 1.44 mm²), R14/R15 at FB, C10/C11 at the SS / BST pins, SW on F only |
| VBUS monitor | R12, R13, C7, D2 | F | x 20.2–26.9, y 32.9–34.7 | D2 → DNP (2026-10-10) |
| NTC | TH1, R33, C26 | F | TH1 (22.0; 29.1), R33 (23.5; 30.2), C26 (20.0; 23.0) | |
| B2B | J5 | F | (22.5; 40.2), 90° | bottom edge, horizontal |
| microSD (DNP) | J3, U8, C60–C63, R60–R66 | F | J3 (9.0; 25.0) left edge; U8 (10.2; 35.4); pull-ups x 19.5–22.7, y 20.1–30.0 | R27 (SD_EN 100k, FIT) **(7.3; 37.93)** 90° (round 8: MH3 courtyard) |
| IR branch (DNP) | U7, R71–R73, C70, C71, TP8A/B | F | x 31.0–42.75, y 38.45–43.7; U7 (33.95; 39.3), R72 (42.6; 39.2), **R73 (42.75; 42.8)**, **C71 (35.25; 43.7)** | bottom-right, next to J5; R73 / C71 moved slightly (MH4) |
| Rd / CC tap (DNP) | R4, R5, R35, R36, C29, C30 | F | **R4 (2.15; 43.9)**; R5 (12.6; 40.4), R35 (12.6; 42.1), **R36 (12.9; 43.75)**; **C29 (10.1; 41.6) −90°, C30 (9.6; 43.9)** | bottom-left; the CC1 → R4/R35 and CC1_ADC copper removed (05 §0.1); round 8: moved aside around MH3 |
| Mounting holes | MH1–MH4 | NPTH | (5.75 / 39.25; 8.25 / 41.75) | centre (22.5; 25.0) – `05` §3.1a; stock `MountingHole_2.2mm_M2` (mask = hole, courtyard r 2.45 on F); washer: nylon on MH1/2/4, none on MH3 (`05` §3) |

**Moves relative to the 2026-10-10 table (round 8, pcbnew comparison with the pre-fix board):** C4 F → **B** (43.4; 18.65 → 42.9; 16.2); **C14 new** (F, 42.675; 16.0); C3 (y 11.4 → 9.45); R10 (43.4; 15.6 → 43.8; 12.75); R9 (y 16.35 → 16.2); C1 (43.6; 24.8 → 43.8; 26.75); buck: U4, L1, C6, C8–C13, R14–R16; C20–C23 (x 12.0–19.8 / y 41.3–43.4 → under P84–P86); C50, R27; DNP: C27/C28 (y 34.5 → 34.02), C29, C30, C71, R4, R36, R73. Not moved: the `05` §3.1a interface elements (outline, MH, J1, J2, J4, J5, J7, SW1–3, D20/R30, U1, J3), U2/U3/U5/U6, the TPs. Value change: R28 100k → 10k; DNP status: R23/C25 → FIT, D2 → DNP.

Deviation from the v0.6 ASCII proposal above: the TP grid is not in the top-right corner but in the bottom-right quadrant (B); the RF/J4 in the bottom-left quadrant, the status LED in the upper third of the left edge; the power block (eFuse top-right, CH224A right, buck in the centre) per the 2026-10-10 rearrangement.
