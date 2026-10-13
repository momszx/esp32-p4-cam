# 07 – BOM plan and value-calculation sheet (v0.4 – rev A BOM closed)

Date: 2026-10-09 · Status: **rev A: G4 closed (2026-10-11, §0)**; originally ~~skeleton – filled in by gate G4 (05 §0.2), BEFORE the MAIN schematic~~ (K-8) · Basis: `05-architecture.md` v0.5 (from v0.3: v0.6 as-built), `06-floorplan.md` v0.3 · v0.2 (R4): new passive-group rows (#53–#60), TP plan, status LED, J7 pin list · **v0.3 (2026-10-10, as-built + round 7 review):** R23/C25 FIT (#22a), D2 DNP (#23), R28 10k (#54), camera control ESD and SD ESD → rev B (#38, #42), J2/J5/L1 placeholder footprints, J7 / TP / J4 as-built, G4 open · **v0.4 (2026-10-11, rounds 8–9): G4 closed for rev A – final BOM in §0** (72 fitted items with LCSC numbers, C14 new, selected special parts, stock reservation, remaining owner decisions); the TBDs in §1 preserve the v0.3 state; where §0 / `BOM_jlc.csv` says otherwise, that is authoritative · **v0.4a (2026-10-13, round 10):** the 8 CC option parts (R4 / R5 Rd, R35 / R36, C29 / C30, D21 / D22) are excluded from the rev A board and BOM (schematic only); the IR bypass R73 moved to the B side; BOM / CPL unchanged
Notation: **TBD** = not yet selected / calculated · **[UNVERIFIED]** = own knowledge, not yet confirmed by a datasheet. The "class" column is **not a part selection**, only the name of the requirement; the MPN must be filled in based on the datasheet. Rev A column: **FIT** = fitted, **DNP** = footprint present, not fitted, **not on board** = symbol in the schematic only ("Exclude from board" / "Exclude from BOM"), no footprint on the rev A PCB.
Rule: the schematic may not start while the rev A **FIT** rows contain a TBD (MPN, LCSC#, footprint source) or there is an uncalculated value in section 2.

> **G4 status (2026-10-11, round 9): ✅ CLOSED for rev A.** All 72 fitted items have LCSC / MPN / Manufacturer fields in the schematic and on the PCB (schematic = PCB = `BOM_jlc.csv` = CPL, parity 0); U3 `attr smd`, U1 / MH1–4 / TP / JP1 / DNP excluded; the 2026-10-10 decisions (R23 + C25 FIT, D2 DNP, R28 10k) and the new C14 carried over. Open owner decisions: **Q6** (J2 contact side), **Q17** (J5 height), **U5** second source – §0.4. **Round 10 (2026-10-13):** R4, R5, R35, R36, C29, C30, D21, D22 are set to "Exclude from board" and "Exclude from BOM" (schematic-only rev B option, `05` §0.1) – the BOM (40 rows) and the CPL (72 rows, F 47 / B 25) are unchanged. ~~2026-10-10, round 7: OPEN – not a single MPN / LCSC field; J2 / J5 / L1 placeholders; U3 SMD attribute missing; CPL = 70 rows~~ (historical).

## 0. Rev A final BOM (G4 closed, 2026-10-11)

Source: `kicad/MAIN/fab/` – `BOM_jlc.csv` (40 rows, 72 references), `CPL_jlc.csv` (72 rows), `parts.json` (per-reference data, stock), `BOM_NOTES.md` (selection rationale). Stock / price / Basic-Extended: JLCPCB parts + LCSC, checked via browser 2026-10-11 – **refresh before ordering**. The values (UVLO 4.40 / 4.00 V, OVLO 10.87 V, ILIM 2.03 A, FB 3.328 V, SS 1.45 ms) are unchanged.

### 0.1 Summary
| | |
|---|---|
| Fitted items (CPL rows) | **72** (the 71 FIT of 2026-10-10 + the new **C14**) – **F 47 / B 25** (C4 moved to the B side) |
| Unique parts (BOM rows) | **40**: **16 Basic** (45 placements), **24 Extended** (27 placements) |
| Extended setup fee | 24 × ~3 USD ≈ **~72 USD / order** (check JLC's current fee table when ordering) |
| Parts cost / board | ≈ **8.8 USD** (1+ unit price, **without the U1 module**); most expensive: J2 2.21 · U3 1.28 · U4 1.15 · U2 0.45 · U6 0.40 USD |
| PCBA | double-sided → **JLC Standard PCBA** (Economic is single-sided only) |
| Excluded | U1 (hand soldering, sourced by the owner), TP1–TP19, JP1, MH1–4, all DNP; **not on the rev A board at all (round 10):** R4, R5, R35, R36, C29, C30, D21, D22 (schematic only) |

### 0.2 Selected special parts
| Ref | Part (MPN) | LCSC | Note |
|---|---|---|---|
| U2 | WCH **CH224A** (ESSOP10) | C42459160 | PD sink, I2C 0x22/0x23, FW: read only (`05` §4.1) |
| U3 | TI **TPS259470ARPWR** (RPW0010A) | **C3662799** | eFuse; stock ~300 (331) → **reserve**; paste 82 / 93 % (TI stencil) |
| U4 | TI **TPS62933FDRLR** (SOT-583) | C5219272 | buck FCCM, 1.2 MHz; 1936 pcs |
| U5 | TECH PUBLIC **TPD2E2U06DCKR-TP** (SC-70-3) | **C5350871** | **clone** – the TI original (C1855726) only 1 pc; the pinout (1 D+, 2 D−, **3 GND**) is **not confirmed** → check on the LCSC datasheet before ordering, otherwise TI C1855726 / global sourcing; bring-up: D± ↔ GND |
| U6 | TI TPS22917DBVR | C2681320 | CAM_3V3 load switch |
| D1 | Diodes **SMAJ10A-13-F** | C134939 | TVS; pad 1 = cathode = VBUS – check in the JLC preview |
| L1 | Taiyo Yuden **NRS5024T2R2NMGJ** | C222926 | 2.2 µH, Isat 4.1 A, Irms 3.1 A, 29 mΩ, 4.9×4.9×**2.4 mm** (≤3.3 mm ✓); the generic `L_Taiyo-Yuden_NR-50xx` land has not been compared with the NRS5024 drawing → JLC DFM / 3D preview |
| J1 | HRO TYPE-C-31-M-12 | C165948 | **4 shell legs without paste** → JLC manual / selective soldering or own (`05` §3.1, §15) |
| J2 | **TE 1-84953-5** (15 p, 1.0 mm, TOP contact, slide lock) | **C5164008** | the footprint is the part itself; **JLC stock 31 pcs → reserve**; its bottom-contact counterpart 1-84952-5 (C3170098, same land, ~1 pc); contact side **Q6** |
| J4 | Hirose U.FL-R-SMT-1(80) | C88374 | RF, rev A FIT (G2 / Q25 open) |
| J5 | **Hong Cheng HC-PZ127-7.2L-2x10PS** | **C41375929** | MAIN plug; FRONT receptacle: HC-PM127-4.3H-2x10PS (C27985222); mated 5.3 mm → at a 7.0 mm gap ~2.3 mm insertion depth [UNVERIFIED]; generic land; **Q17 open** (Samtec FTSH-110-02 / FLE-110-01, 7.47 mm → 7.5 mm standoff + footprint swap) |
| C1 | YAGEO CC0603KRX7RABB472 (4.7 nF **200 V** X7R 0603) | C596328 | ≥250 V not in stock in 0603; 1 kV only in 1206 (footprint swap, rev B); the schematic Value field still reads "4.7nF 50V" |
| C14 | Samsung CL10B105KA8NNNC (1 µF 25 V X7R 0603) | C29936 | **new**, U3 OUT (TI 8.4.1); optional swap 2.2 µF / 25 V X7R |
| C5/C6, C8 | Samsung CL32A226KAJNNNE (22 µF 25 V X5R 1210) · CL21A106KAYNNNE (10 µF 25 V 0805) | C52306 · C15850 | VBUS_SW bulk; deviates from the "35–50 V" rule, accepted given the 10.87 V OVLO (`05` §4.1) |
| C12/C13, C20 | CL21A226MAQNNNE (22 µF 25 V 0805) · Murata GRM32ER61C476KE15L (47 µF 16 V 1210) | C45783 · C77101 | 3V3 output / module bulk; the schematic Value fields (10 V) are lower than the ordered parts |
| R6 | UNI-ROYAL 0603WAF2673T5E (267k 1 %) | **C22963** | **only 180 pcs**, no other 267k 0603 available → reserve (UVLO divider) |
| TH1 | KUU KNTC0603/10KF3950 | C2892547 | B25/85 = **3987 K** (LCSC) – the FW NTC model calculates with this value |
| SW1–3 | Omron B3U-1000P | C231329 | |
| D20 + R30 | KENTO KT-0603G + 1k | C12624 / C21190 | ~0.3–0.5 mA, dim; optional R30 → 470 Ω |

### 0.3 Stock reservation (at order time)
**J2 C5164008 (31 pcs)**, **U3 C3662799 (~300 pcs)**, **R6 C22963 (180 pcs)** – reserve / pre-order; Extended fees expected. Refresh all stock before ordering; in the JLC placement preview check rotation and pin 1: U2–U6, D1 (cathode = VBUS), D20, J1, J2, J4, J5 and all 25 B-side parts.

### 0.4 Remaining owner decisions
| # | Decision | Impact |
|---|---|---|
| Q6 | J2 contact side + FFC with the real camera | **before the camera is first powered on**; wrong side = 3V3/GND swap at the camera; does not block PCB fabrication (same land as the bottom-contact variant) |
| Q17 | J5: keep the Hong Cheng pair (MAIN unchanged, corrected via the FRONT receptacle height) or Samtec 7.47 mm | with Samtec, swap the MAIN J5 footprint **before ordering** + 7.5 mm standoff |
| U5 | accept the TECH PUBLIC clone (pin 3 = GND confirmed) or TI C1855726 | before ordering |
| C1 | accept the 200 V 0603 (rev B: 1206 / 1 kV) | – |
| optional | BOM swap on the same footprint: **R28 → 4.7k**, **C14 → 2.2 µF / 25 V X7R**, **R30 → 470 Ω** | before ordering, without layout change |

## 1. BOM skeleton (every part class from 05)

| # | Function | Class / requirement | MPN | LCSC# | Package | Footprint source | Rev A | Gate |
|---|---|---|---|---|---|---|---|---|
| **Power** | | | | | | | | |
| 1 | USB-C input J1 | 16 pin USB-C receptacle, USB 2.0, 4 THT shell legs | TYPE-C-31-M-12 (HRO) | C165948 | SMD + THT shell | manufacturer / LCSC | FIT | ✅ (shell legs: JLC manual / selective or own soldering, §0.2) |
| 2 | USB ESD | **3.3 V array, no VBUS pin** (TPD2E2U06 / PRTR5V0U2X class) [UNVERIFIED] | TPD2E2U06DCKR-TP (TECH PUBLIC clone) | C5350871 | SC-70-3 | manufacturer | FIT | ✅ – pinout to be confirmed before ordering (§0.4) |
| 3 | TVS | SMAJ10A class (standoff 10 V; leakage 9.45 V / 85 °C) | SMAJ10A-13-F (Diodes) | C134939 | SMA | manufacturer | FIT | ✅ (as-built: B, under U3) |
| 4 | PD sink | **CH224A** (PD3.2 sink, I2C 0x22/0x23, PG open-drain active low) – E22 | CH224A | **C42459160** | ESSOP10 | WCH datasheet v2.1 (`ref/datasheets/`) | FIT | ✅ |
| 5 | CH224A voltage strap | fixed R for 9 V, never floating | TBD | TBD | 0603 | – | FIT | G1 (section 2 S10) |
| 6 | PG pull-up | R to 3V3 (polarity: G1) | TBD | TBD | 0603 | – | FIT | G1 (S9) |
| 7 | Rd ×2 | 5.1k – **only without CH224A, never both at once** (R4 / R5) | TBD | TBD | 0603 | – | ~~DNP~~ → **not on board** (schematic only, round 10) | K-1 |
| 8 | eFuse (main) | adjustable OVP ~10.5–11 V, reverse-blocking, auto-retry, UVLO 4.4/3.9 V, ILIM ~2 A, soft-start (TPS25947 / TPS2595x class) [UNVERIFIED] | TPS259470ARPWR | C3662799 | RPW0010A 2×2 | TI datasheet | FIT | ✅ (stock ~300 → reserve) |
| 9 | VBUS_SW bulk | **35–50 V MLCC**, effective C after DC bias ≤47 µF in total. As-built: C5/C6 22 µF 25 V (1210), C8 10 µF 25 V – electrically adequate given the 10.87 V OVLO, but deviates from the 35–50 V rule (electrical-09) | TBD | TBD | 1210 | – | FIT | G4 |
| 10 | VBUS→VBUS_SW bridge | 0 Ω / solder bridge, ≥2 A | TBD | TBD | 1206 | – | **DNP** | K-1 |
| 11 | Buck 3V3 | wide-input, forced-PWM, ≥2 A (TPS62933F class) [UNVERIFIED] | TPS62933FDRLR | C5219272 | SOT583 | manufacturer | FIT | ✅ |
| 12 | Buck inductor | 2.2 µH, Isat ≥3.5 A, ≤3.3 mm tall. **On the PCB (L1) a generic `L_Taiyo-Yuden_NR-50xx` footprint** – the 4.0 mm variant of the series does not fit under the camera (mech-09) → to be finalised together with the MPN | NRS5024T2R2NMGJ (Taiyo) | C222926 | 4.9×4.9×2.4 | manufacturer (land: NR-50xx, not compared) | FIT | ✅ (Isat 4.1 A) |
| 13 | Buck CIN / COUT | MLCC, VIN side ≥25 V (9.45 V + spike) | CL32A226KAJNNNE / CL21A106KAYNNNE / CL21A226MAQNNNE | C52306 / C15850 / C45783 | 1210 / 0805 | – | FIT | ✅ |
| 13a | **eFuse OUT capacitor (C14, new 2026-10-11)** | ≥1 µF on U3 OUT (TI 8.4.1), VBUS_SW → GND | CL10B105KA8NNNC | C29936 | 0603 | – | FIT | ✅ (opt. 2.2 µF / 25 V X7R) |
| 14 | Buck output 0 Ω | + TP4 (bench power injection, K-1) | TBD | TBD | 0603 | – | FIT | K-1 |
| 15 | Module 3V3 bulk | **47 µF + 10 µF + 100 nF** at pads P84–P86 | TBD | TBD | 1210 / 0805 / 0402 | – | FIT | G4 |
| 16 | CAM_3V3 load switch | **TPS22917DBV** (TPS22918 class; 1–5.5 V, 2 A, CT, QOD – KiCad library pinout: 1 VIN, 2 GND, 3 ON, 4 CT, 5 QOD, 6 VOUT); QOD → 0R (R53) → VOUT; CT = 1 nF starting value (tune in bring-up step 7) | TPS22917DBVR | C2681320 | SOT-23-6 | KiCad Power_Management | FIT | ✅ (U6) |
| 17 | SD_3V3 load switch | **TPS22917DBV** (U8), QOD → R60 0R, CT 1 nF | TPS22917DBVR | TBD | SOT-23-6 | KiCad Power_Management | **DNP** | ✅ type |
| 18 | IR branch 2nd eFuse | **TPS259470ARPW** (U7; 23 V, RILM 6.65k → ILIM 0.50 A (0.425–0.575), auto-retry; EN/UVLO = IR_SW_EN, OVLO → GND); shunt R72 0.1 Ω + TP8A/B; bypass R73 0R (**round 10: B side under U7; U7 / R73 routed, fittable without wires**) | TPS259470ARPW | TBD | RPW0010A | TI datasheet (E22) | **DNP** | ✅ type |
| 19 | IR fused 0 Ω (rev B alternative; rev A: the whole IR branch DNP) | fused 0 Ω / PTC, ~0.75 A | TBD | TBD | 1206 | – | **DNP** | K-3 |
| 20 | IR shunt + TP8 | MAIN front side | TBD | TBD | 1206 | – | **DNP** | G6 (S8) |
| 21 | Supervisor | TPS3840 class, **open-drain**, ~3.08 V [UNVERIFIED] | TBD | TBD | SOT-23-5 | manufacturer | **not drawn → rev B** | K-14 |
| 22 | Supervisor → ESP_EN 0 Ω | | TBD | TBD | 0603 | – | **not drawn → rev B** | K-14 |
| 22a | **ESP_EN RC** (R23, C25) | **10k → 3V3 + 1 µF → GND**; Q3 (the module's own EN RC) open, but without a pull-up the board does not start | 0603WAF1002T5E / CL10A105KB8NNNC | C25804 / C15849 | 0603 ×2 | – | **FIT** (2026-10-10; previously DNP) | ✅ |
| 23 | VBUS_SW ADC divider | R12 200k / R13 54.9k (1%) + C7 100 nF → GPIO 20; **3.6 V Zener (D2, BZT52C3V6): DNP** (2026-10-10 – its leakage at the 43 kΩ node would distort the 8 V mode threshold) | TBD | TBD | 0603 / SOD-123 | – | FIT (D2: **DNP**) | G4 (S11) |
| 24 | CC-tap ×2 | 100k + 10 nF + 3.6 V Zener → GPIO 21/22 (R35 / R36, C29 / C30, D21 / D22) | TBD | TBD | 0603 / SOD-323 | – | ~~DNP~~ → **not on board** (schematic only, round 10) | K-15 |
| 25 | NTC + divider | ADC2 (GPIO 49), 100 nF | TBD | TBD | 0603 | – | FIT | G4 (S13) |
| **Module / MCU** | | | | | | | | |
| 26 | P4 module | Waveshare ESP32-P4-Module (25×25×3.3, 88 castellated pads) | ESP32-P4-Module | – | castellated | **Waveshare land pattern zip** (G2) | FIT | G2 |
| 27 | VO4 | 1 µF + TP; external source forbidden | TBD | TBD | 0603 | – | FIT | – |
| 28 | Strap pull-ups | GPIO36 10k; C6_IO9 10k; **C6_IO8 10k (mandatory)** | TBD | TBD | 0603 | – | FIT | – |
| 29 | BOOT / RESET / USER | SMD tact ×3 – **Omron B3U-1000P** (LCSC C231329; owner decision 2026-10-09, `90-review-log.md`; no MPN field in the schematic yet) | B3U-1000P | C231329 | 3.0×2.5 | KiCad (official) | FIT | G4 (field fill-in) |
| 30 | Status LED + series R | discrete 0603, **MAIN back side** (GPIO 6; J5.17 spare) | TBD | TBD | 0603 | – | FIT | G4 |
| 31 | I2C pull-up | **DNP until the camera I/O level is known** | TBD | TBD | 0603 | – | **DNP** | G3 |
| 32 | C6 + UART0 pad row J7 | **as-built: 9 SMD pads, 1.27 mm** (`PadRow_1x09_P1.27mm_SMD`, own), B side, top edge (22.5; 2.0): GND, C6_TXD, C6_RXD, C6_IO9, C6_IO8, GPIO 54 / C6_EN (P82; Q2), UART0 TX, UART0 RX, 3V3-ref (05 §6) | – | – | pad row | own | **DNP** (no header) | K-17 |
| 33 | TPs (back side) | **as-built: TP1–TP7, TP16A/B, TP17–TP19 = 12 pads** (GND: TP3, TP18, TP19), 10 on the 2.75 mm pogo grid + TP5, TP6 separately; ~~TP9a/b, TP10–TP15, 20 pads / 2.0 mm~~ deleted; TP8A/B on the front side, DNP (05 §12) | – | – | Ø1.5 pad | KiCad TestPoint | FIT | – |
| 34 | u.FL J4 | at the board edge (left edge, B), strain relief; **as-built: J4 + R34 0R FIT** (G2 / Q25 open; the module's IPEX is an alternative) | TBD | TBD | u.FL | KiCad (Hirose U.FL-R-SMT-1) | FIT | G2 |
| 35 | π-network ×3 + CPWG | every element 0 Ω / DNP-capable | TBD | TBD | 0603 | – | FIT (0 Ω) | G2 |
| 36 | Antenna ×2 | 2.4 GHz, IPEX Gen1 / u.FL | TBD | – | – | – | procurement | G0/G2 |
| **Camera** | | | | | | | | |
| 37 | J2 FPC 15 pin 1.0 mm | candidates: 1.0K-GT-15PB or Hirose FH12-15S-1SH [UNVERIFIED]. **On the PCB the footprint is a placeholder: TE 1-84953-5** (`Connector_FFC-FPC:TE_1-84953-5_1x15-1MP_P1.0mm_Horizontal`, per its description "top-side contacts"); the candidates' footprints differ [UNVERIFIED]; **contact side (Q6) open** – wrong side = 3V3/GND swap at the camera. Decision before ordering: either the TE 1-84953-5 is the purchased part (JLC availability checked), or a footprint swap to the chosen MPN. The pin ↔ net map (RPi order) has been checked. **2026-10-11: the TE 1-84953-5 is the ordered part (footprint = part); stock 31 pcs → reserve; Q6 before the camera is first powered on (§0.4)** | 1-84953-5 (TE) | C5164008 | ZIF (slide lock) | KiCad (official TE) | FIT | ✅ G4 · Q6: G3 |
| 38 | Control signal ESD (J2) | low-C array (CAM_PWDN = CAM_IO0, SCL, SDA); 05 §0.1 + 06 §2.2 row. **Formally deferred to rev B (2026-10-10):** not in the schematic; Q6 open, the J2 area is crowded | TBD | TBD | SOT-xx | – | ~~FIT~~ → **rev B** | rev B |
| 39 | Camera module | OV5640 MIPI 2-lane, onboard osc + LDO, **NoIR or fixed lens** (rev A) | TBD | – | – | module STEP | procurement | G3 |
| 40 | FFC | standard 50 and 100 mm + 25–30 mm custom | TBD | – | – | – | procurement | G3 |
| **microSD** | | | | | | | | |
| 41 | J3 microSD | push-push (on the PCB a Hirose DM3AT-SF-PEJM5 footprint – its description says "push-pull", to be checked, mech-14) | TBD | TBD | SMD | KiCad | **DNP** | K-16 |
| 42 | SD ESD + pull-ups | ESD ≤3.5 pF, pull-up to SD_3V3. **The SD ESD footprint is not in the schematic → rev B** (2026-10-10); the pull-ups (R61–R66) are present with DNP footprints | TBD | TBD | – | – | pull-up: **DNP**; ESD: **rev B** | K-16 |
| **FRONT (G6)** | | | | | | | | |
| 43 | IR LED ×4 | 850 nm, 3535 | TBD | TBD | 3535 | manufacturer | G6 | Q19 |
| 44 | IR CC driver ×2 | buck-CC, Vin 4.5–9.45 V (criterion 4.2) | TBD | TBD | SOT-23-6 | manufacturer | G6 | Q19 |
| 45 | NFET ×2 | AO3400 class | TBD | TBD | SOT-23 | – | G6 | – |
| 46 | ICR H-bridge | DRV8837 class, **from 3V3** | TBD | TBD | TBD | manufacturer | **DNP** | rev B |
| 47 | J6 ICR | JST-SH 1.0 mm 2 pin | TBD | TBD | SMD | manufacturer | **DNP** | rev B |
| 48 | PDM microphone | MSM261D3526H1CPM / MP34DT05-A [UNVERIFIED] | TBD | TBD | LGA | manufacturer | G6 | Q20 |
| 49 | Microphone LC + CLK series R | 33–100 Ω | TBD | TBD | 0603 | – | G6 | – |
| 50 | VEML7700 | DNP, IR-shielded | TBD | TBD | TBD | manufacturer | **DNP** | – |
| **Passive groups (R4)** | | | | | | | | |
| 53 | USB-C shield RC | 1 MΩ ‖ 4.7 nF between the 4 THT shield legs and GND (J1; 05 §5, §6; §3 below); as-built R1 / C1 on the F side | 0603WAF1004T5E / CC0603KRX7RABB472 (**200 V**) | C22935 / C596328 | 0603 ×2 | – | FIT | ✅ |
| 54 | GPIO pull-downs | **100k:** GPIO 26 IR_PWM (R24), 27 ICR_IN1 (R25), 28 ICR_IN2 (R26), **53 SD_EN (R27)** – FIT; GPIO 32 IR_SW_EN (R29) – **DNP** together with the IR branch. **10k: GPIO 4 CAM_3V3_EN (R28)** – 2026-10-10 (previously 100k; the internal pull-up of GPIO 4 / MTMS during reset [UNVERIFIED]). ~~GPIO 29 SD_EN, 33 CAM_3V3_EN~~ (pre-v0.6 assignment). As-built: MAIN **front side (F)** (05 §5) | TBD | TBD | 0603 ×6 | – | FIT (GPIO 32: **DNP**) | G4 |
| 55 | UART0 series R | 1–4.7k ×2 (GPIO 37 TX / 38 RX; 05 §5.1) | TBD | TBD | 0603 ×2 | – | FIT | G4 |
| 56 | GPIO 33 (USER, v0.6) filter | 100 nF on the pin (05 §5) | TBD | TBD | 0402 / 0603 | – | FIT | G4 |
| 57 | CH224A supply capacitors | VHV 1 µF 50 V (the VBUS pin tied to VHV); counts toward the ≤10 µF effective pre-eFuse budget (05 §4.1) | – | TBD | 0603 | – | FIT | ✅ (C2) |
| 58 | CAM_3V3 0 Ω measurement jumper | after the load switch + TP5 (05 §0.1, §12) | TBD | TBD | 0603 | – | FIT | G4 |
| 59 | Buck FB divider | R1 / R2 (E96) for 3.3 V | TBD | TBD | 0603 ×2 | – | FIT | G4 (**S1**) |
| 60 | eFuse OVP / UVLO / ILIM resistors | OVP divider, UVLO divider, R_ILIM (main eFuse; ~5 pcs) | TBD | TBD | 0603 | – | FIT | G4 (**S4, S5, S6**) |
| **Mechanics** | | | | | | | | |
| 51 | B2B J5 pair | 2×10, 1.27 mm, **mated height 7 mm**, short wipe. **Generic footprint on the PCB** (`PinHeader_2x10_P1.27mm_Vertical_SMD`), (22.5; 40.2) – ~~the type (and with it the footprint) not yet selected~~ → **2026-10-11: the Hong Cheng pair in the BOM (5.3 mm mated, ~2.3 mm insertion depth at 7.0 mm); the land remained generic; Q17 open (§0.2)** | HC-PZ127-7.2L-2x10PS (Hong Cheng) | C41375929 | SMT | KiCad (generic) | FIT (MAIN) | Q17 |
| 52 | M2 standoff ×4 | 7 mm, 33.5 mm pitch + screws | TBD | – | – | – | procurement | G3 |

## 2. Value-calculation sheet (G4, before the schematic)

Every result is **TBD** until we have the datasheet of the corresponding type in hand; the formulas are starting rules. Units: V, A, Ω.

| # | Parameter | Formula / rule | Input | Result |
|---|---|---|---|---|
| S1 | Buck FB divider | Vout = Vref·(1 + R1/R2) → R1 = R2·(Vout/Vref − 1) | Vout = 3.3 V; Vref = datasheet (e.g. 0.8 V [UNVERIFIED]); example R2 = 10k → R1 ≈ 31.25k → E96 series | TBD (G4) |
| S2 | Buck inductor | L = Vout·(1 − Vout/Vin_max) / (fsw·ΔIL); ΔIL ≈ 0.3·Iout_max; Isat ≥ Iout_max + ΔIL/2 | Vin_max = 9.45 V; Iout_max ≥ 1.1 A (05 4.3), designed for ≥2 A; fsw = datasheet | TBD; starting point 2.2 µH, Isat ≥3.5 A |
| S3 | Buck COUT | datasheet Cout min/max (B-27); ΔVout ≈ ΔIL/(8·fsw·Cout); transient: WiFi TX step ~350 mA; **effective C** after DC bias | datasheet, MLCC DC-bias curve | TBD |
| S4 | eFuse OVP | Vovp = Vref_ovp·(1 + R_top/R_bot); target **10.5–11 V** | Vref_ovp = datasheet | TBD |
| S5 | eFuse UVLO | Vuv(↑) = **4.4 V**, Vuv(↓) = **3.9 V** (divider or fixed hysteresis from the datasheet) | datasheet | TBD |
| S6 | eFuse ILIM | R_ILIM from the datasheet table / formula, target **~2 A**; check: I_inrush = C·dV/dt = 47 µF × 30 mV/µs ≈ **1.41 A** < ILIM ✓ | C_eff ≤47 µF (05 4.1) | TBD (R_ILIM) |
| S7 | IR LED current | I_LED = Vsense / Rsense → Rsense = Vsense / 0.15 A; P_R = I²·R; headroom: Vin_min − Vsense ≥ Vf_max(−20 °C) + 0.3 V | driver Vsense (datasheet), LED Vf (Q19) | TBD |
| S8 | IR branch ILIM | ILIM (2nd eFuse) ≥ 2× the input peak current: 1.2 W / 4.5 V ≈ 0.27 A → **0.5–0.7 A** ✓; R_ILIM from the datasheet | 05 4.2 | TBD (R_ILIM) |
| S9 | PG pull-up | R_PU = (V_rail − V_OL) / I_sink; **V_rail = 3V3** (not VBUS; GPIO max 3.6 V); example 3.3 V / 10k = 0.33 mA | CH224A PG type (open-drain?) and polarity: G1 | TBD (G1) |
| S10 | CH224A strap | R_cfg for 9 V from the datasheet table; fixed, not floating | CH224A datasheet | TBD (G1) |
| S11 | VBUS_SW divider | Vadc = Vbus·R2/(R1+R2): 9.45 V × 54/254 = **2.01 V** ✓ (≤3.3 V); Zener leakage × R1 error | R1 = 200k, R2 = 54k | done (to be checked) |
| S12 | CC-tap (rev A: not on the board) | τ = 100k × 10 nF = 1 ms; thresholds 05 4.3; ADC / Zener leakage × 100k error | 05 4.1 | rev B |
| S13 | NTC divider | Vadc = 3.3 V·Rntc/(Rntc + R_ref); R_ref = R25; range 25–85 °C | NTC B value (TBD) | TBD |
| S14 | Supervisor threshold | threshold variant below 3V3 − tolerance, compared against the buck tolerance (~3.08 V [UNVERIFIED]) | buck Vout tolerance | TBD |
| S15 | CAM_3V3 CT | see section 4 | | |

## 3. USB-C 16 pin – pin map (K-20) [UNVERIFIED: check against the datasheet of the specific MPN]

| Connector pin | Signal | Connection |
|---|---|---|
| A1, B12 | GND | GND |
| A4, B9, B4, A9 | VBUS | VBUS (TVS + ESD at the connector) |
| A5 | CC1 | CH224A CC1 |
| B5 | CC2 | CH224A CC2 |
| **A6 + B6** | D+ | **tied together** → USB-Serial-JTAG D+ = **GPIO 25 (P51)**, ESD 3.3 V array |
| **A7 + B7** | D− | **tied together** → USB-Serial-JTAG D− = **GPIO 24 (P50)**, ESD |
| A8, B8 | SBU1, SBU2 | **NC** |
| B1, A12 | GND | GND |
| Shield (4 THT legs) | | 1 MΩ ‖ 4.7 nF → GND (BOM #53) |

Notes: USB 2.0 only; **no external Rd on CC** (the CH224A contains an internal Rd [UNVERIFIED]; the 2× 5.1k Rd is schematic-only in rev A – not on the board since round 10 – and only for use without CH224A); CH224A **DP/DM NC**; in 16-pin types the duplicated A/B pins may be tied together internally – per the MPN datasheet; the D± tie must be made on the board if the connector does not tie them together.

## 4. CAM_3V3 load switch – CT / slew and inrush (K-22)

| Item | Value / rule |
|---|---|
| Switch | TPS22918 class, rise time adjustable via the CT pin [UNVERIFIED] |
| Goal | charge the camera module's input capacitance slowly: **I_inrush = C_in·dV/dt ≤ ~0.3 A**, 3V3 rail droop **≤ ~100 mV** (target) |
| Calculation | dt ≥ C_in·3.3 V / 0.3 A; example C_in = 22 µF → dt ≥ ~0.24 ms; **recommended slew 0.5–1 ms** |
| CT value | **TBD (G4)** – from the datasheet's CT–tR chart / table; starting candidate 1 nF [UNVERIFIED]; C_in from the selected camera module (G3) |
| Measurement | bring-up step 7: scope on the CAM_3V3 and 3V3 rails, current through the 0 Ω measurement jumper; if the droop > target → increase CT |
| Timing | power sequence: 3V3 → CAM_IO0 → I2C (05 §7) |

## 5. Footprint source and DFM checklist

- [x] Waveshare ESP32-P4-Module land pattern (DXF) imported (`Waveshare_ESP32-P4-Module_HandSolder`, 88 pads match the DXF); pad extension 1.5 mm outward; vias under the module tented (05 3.1); the STEP import is not checked here
- [x] LCSC# / JLC assemblability on every FIT row (16 Basic / 24 Extended; §0); FPC, u.FL, USB-C checked separately; no 7 mm B2B pair available (Q17); USB-C shell legs: manual / selective soldering
- [ ] Double-sided assembly: which parts go on the back side (module by hand, USB-C THT)
- [ ] Footprint source marked in every row (manufacturer / LCSC / own); silkscreen labels: "NEVER BOTH", pin 1, "no hot-plug"
- [x] EDA tool selected: **KiCad** (05 3.1, Q26)
- [ ] Fabrication order (round 7 → round 9): stackup **JLC04101H-3313A** by name (~~no stackup block in the board file~~ → now included in the board file and in the gbrjob: ENIG, impedance, Rev A), impedance-control requirement, **ENIG** (the 0.3 mm gap of JP1 without a solder-mask dam may get bridged with HASL), 45 × 45 mm (not the gbrjob's 45.1), revision label (silk: "rev A 2026-10"), **rails only on the top / bottom edge** (fiducials on the rail), ~~keep-out zones for panel tabs (right edge y 16–29, top edge x 10–35)~~ → **no tab on the right edge at y > 5.8 mm, nor on the top edge between x 10–35 mm** (C3 / R10 / C1 at 0.7–0.8 mm from the right edge); **only after the pre-order gate** (refill + save in the project folder, DRC without refill 0 errors, Gerber `--check-zones`; 05 §3.1)
- [x] CPL / BOM export: U3 SMD attribute, U1 + MH1–4 + TP + JP1 excluded, DNP attributes in sync (R4/R5 DNP; since round 10 not on the board), U1 and the DNP footprints without paste → **CPL 72 rows (F 47 / B 25)**, `BOM_jlc.csv` 40 rows (`kicad/MAIN/fab/`)
