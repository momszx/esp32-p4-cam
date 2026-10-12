# MAIN rev A – BOM / part selection (G4), round 8 fix pass 2

Date: 2026-10-11 · Source: the master schematic (`kicad/MAIN/*.kicad_sch`, read-only) and the PCB footprints (`pcbnew.LoadBoard`, read-only) · Stock, price and Basic/Extended classification: **JLCPCB parts library + LCSC, checked in a browser on 2026-10-11** (stock changes from day to day; it must be refreshed before ordering).
Outputs: `BOM_jlc.csv` (JLC assembly BOM), `parts.json` (per-reference data), `fields_apply.py` (LCSC / MPN / Manufacturer fields into the schematic and onto the PCB), `work/make_bom.py` (generator of the CSV and the JSON, containing the full part table). Only `BOM_jlc.csv`, `CPL_jlc.csv` and `parts.json` are in this repository (next to this file); `fields_apply.py`, `work/make_bom.py`, `drc.py` and the `test/kicad/` copy were session work files and are not included.

## 1. Summary

| | |
|---|---|
| Fitted items (CPL rows) | **72** = the 71 FIT in the master (excluding U1, TPs, JP1, MH1–4) **+ the new C14** |
| Unique parts (BOM rows) | **40**: **16 Basic** (45 placements), **24 Extended** (27 placements) |
| Extended setup fee | 24 × ~3 USD ≈ **72 USD / order** (check JLC's current fee table when ordering) |
| Part cost / board | ≈ **8.80 USD** (1+ unit price, excluding the U1 module); the most expensive: J2 2.21 · U3 1.28 · U4 1.15 · U2 0.45 · U6 0.40 |
| Placement side | F: 47 (with C14), **B: 25** (C4 moved to the B side; C20–C25, C40, D1, D20, J1, J4, R11, R20–R23, R30, R34, R40, R41, R70, SW1–3) → **double-sided = JLC Standard PCBA** (Economic is single-sided only) |
| Excluded (already xb/xp on the PCB) | U1 (hand-soldered, bought by the owner), TP1–TP19, JP1, MH1–4, all DNP |

The existing values (UVLO 4.40/4.00 V, OVLO 10.87 V, ILIM 2.03 A, FB 3.328 V, SS 1.45 ms – round 7 review) are **unchanged**: for the E96 resistors, exact-value UNI-ROYAL 1 % Extended items were selected.

## 2. Risky / low-stock / not fully compliant items

| Ref | Choice | Issue | Action |
|---|---|---|---|
| **J2** | TE 1-84953-5, **C5164008** | only **31 pcs** JLC stock, 2.21 USD | reserve / pre-order before ordering; contact side (Q6) see point 3 |
| **R6** 267k | UNI-ROYAL 0603WAF2673T5E, **C22963** | only **180 pcs**; no other manufacturer's 267k 0603 in stock | order in time; emergency fallback: a different E96 pair (UVLO recalculation needed) |
| **U3** | TPS259470ARPWR, **C3662799** | only **331 pcs** | reserve |
| **U5** | TECH PUBLIC TPD2E2U06DCKR-TP, **C5350871** (9175 pcs) | the original TI TPD2E2U06DCKR (C1855726) has **1 pc** in stock → pin-compatible second source; the pinout (1 IO1, 2 IO2, 3 GND) **verified** against the pinout drawing on the LCSC product page (2026-10-11), matches the TI part | owner: accept the second source, or source the TI original globally |
| **D20** | KENTO KT-0603G, **C12624** | the earlier favourite Everlight C72043 is down to 1 pc; green InGaN Vf ≈ 2.8–3.1 V → with R30 = 1k from 3V3 ≈ 0.3–0.5 mA (dim, but visible) | if brighter is needed: reduce R30 (e.g. 330 Ω) or use a yellow-green AlGaInP LED |
| **C1** | YAGEO CC0603KRX7RABB472, **C596328**, 4.7 nF **200 V** X7R 0603 | **≥250 V is not in stock in 0603** (Walsin C3880764, CCTC C5375795, Knowles, Venkel: all 0 pcs); 1 kV 4.7 nF only from 1206 upward (FH 1206B472K102NT C9192, 86 435 pcs) | proceeding with 200 V; for 1 kV the C1 footprint must be changed to 1206 (layout task) |
| **J5** | Hong Cheng HC-PZ127-7.2L-2x10PS, **C41375929** | **no mated pair with a 7.00 mm mated height was found**; the land pattern has not been checked against a datasheet | owner decision (Q17), see point 5 |
| **L1** | Taiyo NRS5024T2R2NMGJ, **C222926** | the land pattern per the Taiyo drawing has not been compared with the KiCad `L_Taiyo-Yuden_NR-50xx` footprint (same 4.9×4.9 NR/NRS family) | check against the Taiyo NRS5024 catalogue drawing |

## 3. J2 – 15-pin 1.0 mm FPC: decision table

The PCB footprint: `Connector_FFC-FPC:TE_1-84953-5_1x15-1MP_P1.0mm_Horizontal`. The "land pattern match" column is a pad-by-pad comparison of KiCad's stock footprints (position and size, KiCad python).

| Part | LCSC | JLC stock | Land pattern vs. the current J2 | Contact side (per description) | Note |
|---|---|---|---|---|---|
| **TE 1-84953-5** | **C5164008** | **31** | **identical** (this is the footprint itself) | **TOP** (TE/JLC: "Top Contact"; KiCad: "15 top-side contacts") | **selected**; slide lock, SMT, horizontal |
| TE 1-84952-5 | C3170098 | 1 | **identical** (the pads of KiCad `TE_1-84952-5…` match 1:1) | **BOTTOM** (TE/JLC: "Bottom Contact") | the same housing with bottom contacts; practically not orderable right now |
| JUSHUO AFA07-S15FCA-00 | C262721 | 5507 | **DIFFERENT** (signal pads y = −3.375 / 0.6×1.8 mm instead of −1.8 / 0.61×2.0 mm) | BOTTOM | only with a footprint change (`JUSHUO_AFA07-S15FCA-00…`, KiCad stock); 2.5 mm tall |

I did not find a Chinese 15-pin 1.0 mm connector whose footprint is **pad-for-pad identical** to the TE 84953 (the Chinese 1.0 mm ZIF types found, e.g. BOOMELE H2.5, JUSHUO AFA07, have a different pad geometry).

**What the contact side means (Q6, G3):** in a TOP-contact J2 the metal contacts of the FFC must face **upward (away from the PCB)**, in a BOTTOM-contact one downward. If the cable coming from the camera (type A = same-side / type B = opposite-side contacts, plus the direction of the fold) faces the wrong way at MAIN, the cable can only be inserted flipped → 1↔15 mirroring → **3V3/GND swap at the camera**. The J2 pin ↔ net map does not change; it depends only on the choice of cable / connector side. To be decided once the final cable and camera module are in hand: TE 1-84953-5 (top) stays, or 1-84952-5 (bottom, identical footprint, but currently out of stock), or an FFC of the reversed type.

## 4. L1 – buck inductor

**Taiyo Yuden NRS5024T2R2NMGJ (C222926)**: 2.2 µH ±30 %, **Isat 4.1 A**, Irms 3.1 A, DCR 29 mΩ, 4.9×4.9×**2.4 mm** (≤3.3 mm under the camera ✓), JLC 1136 pcs, 0.24 USD.
- TPS62933F with RT = GND → 1.2 MHz; ΔIL = 3.3·(1 − 3.3/9.45)/(2.2 µH · 1.2 MHz) ≈ 0.81 A → at 2 A load Ipeak ≈ 2.4 A < 4.1 A ✓. The requirement (Isat ≥ 3.5 A) is met; the datasheet recommendation "ideally Isat ≥ IHS_LIMIT (max 5.8 A)" is not met by any 5×5 part (the short-circuit current limit still protects).
- Alternatives: Taiyo LCXND5050WDL2R2NMG (C5379987, identical data, 195 pcs); NRS5030T2R2NMGJ (3.0 mm, Isat 4.2 A, only 6 pcs); **NRS5020T2R2NMGJ is not suitable** (Isat 2.9 A); NR5040 (4.0 mm) is **forbidden** (mech-09: does not fit under the camera).

## 5. J5 – B2B 2×10, 1.27 mm (MAIN side) + its mate

The target is a 7.0 mm mated height (with the frozen M2 standoffs). **There is no ready-made pair that is 7.00 mm per datasheet** on the market:

| Variant | MAIN (plug) | FRONT (socket) | Total mated height | At a 7.0 mm gap | Sourcing |
|---|---|---|---|---|---|
| **A – written into the BOM (assemblable at JLC)** | Hong Cheng **HC-PZ127-7.2L-2x10PS C41375929** (insulator 1.0 mm, pin 4.0 mm) | Hong Cheng **HC-PM127-4.3H-2x10PS C27985222** (4.3 mm) | 5.3 mm | the pin engages ~**2.3 mm** into the socket (2.0–2.6 with ±0.3 mm tolerance) – the contact depth is **[UNVERIFIED]** | 1809 / 907 pcs |
| A′ | BOOMELE 1.27-2*10P C59981 (1.5 / 3.0 mm) | Kinghelm KH-1.27FH-2X10P-H4.3-SMT C2938399 | 5.8 mm | ~1.8 mm engagement (weaker) | 5458 / 2471 pcs |
| **B – datasheet pair** | Samtec **FTSH-110-02-x-DV(-A)** | Samtec **FLE-110-01-G-DV(-A)** | **7.47 mm** (samtec.com "Full Mated Sets") | with a 7.0 mm standoff the board **does not seat** → a **7.5 mm standoff** is needed | JLC: FTSH-110-02-L-DV C6950077 2 pcs, FLE-110-01-G-DV-A C3322884 17 pcs → Samtec / distributor |
| C | Samtec TFM-110-02-L-D(-A) | Samtec SFM-110-02-L-D(-A) | 6.35 mm (8.13 mm with the TFM-…-12) | falls 0.65 mm short | hardly any at JLC |

Recommendation: for rev A bring-up (the stack is only closed after a stable image, K-7) **variant A** is enough; if the closed stack also matters mechanically, **B (Samtec 7.47 mm + 7.5 mm standoff)** is the clean solution – for this the J5 footprint must be replaced with the recommended pad layout of the Samtec FTSH-…-DV, and the `-A` (guide post) variant needs holes. For neither variant has the datasheet land pattern been compared with the KiCad generic `PinHeader_2x10_P1.27mm_Vertical_SMD` footprint (pads 2.4×0.74 mm, x = ±1.95 mm). **The footprint of the FRONT-side socket is mirrored** (KiCad `PinSocket_2x10…`: pin 1 on the +x side) – keep this in mind when designing FRONT.

## 6. C1 – USB-C shield capacitor

YAGEO CC0603KRX7RABB472 (**C596328**), 4.7 nF **200 V** X7R ±10 % 0603, 10 996 pcs. The requested ≥250 V (ideally 1 kV) is **not available from stock in 0603**; 1 kV would need a 1206 footprint (FH 1206B472K102NT C9192 or YAGEO CC1206KKX7RCBB472 C107198). The schematic value ("4.7nF 50V") can be updated to "4.7nF 200V".

## 7. Other choices in brief

- **C14 (new, VBUS_SW → GND at the U3 output)**: Samsung CL10B105KA8NNNC (**C29936**), 1 µF 25 V **X7R** 0603, Extended. Basic fallback: C15849 (1 µF 50 V X5R) – saves the 3 USD.
- **C5/C6** 22 µF 25 V 1210: Samsung CL32A226KAJNNNE (C52306, X5R). X7R alternative: Murata GRM32ER71E226KE15L (C21397). With the 25 V per the schematic this deviates from the 07 #9 "35–50 V" rule (accepted given the 10.87 V OVLO).
- **C20** 47 µF: Murata GRM32ER61C476KE15L (C77101) **16 V** X5R – better DC-bias margin than the 10 V value.
- **C12/C13** 22 µF and **C8/C21** 10 µF: Basic 25 V 0805 (C45783, C15850).
- **D1** SMAJ10A: Diodes SMAJ10A-13-F (C134939); alternative Littelfuse C148210. Pad 1 = cathode = VBUS – check the polarity in the JLC CPL preview.
- **TH1** NTC 10k: KUU KNTC0603/10KF3950 (C2892547); LCSC lists 3987 K (B25/85), the type name says B3950 (B25/50) – FW calibration at G5b.
- **J1** HRO TYPE-C-31-M-12 (C165948), **J4** Hirose U.FL-R-SMT-1(80) (C88374), **SW1–3** Omron B3U-1000P (C231329, per the 07 #29 decision), **U2** CH224A (C42459160), **U4** TPS62933FDRLR (C5219272), **U6** TPS22917DBVR (C2681320).

## 8. If the Extended fee has to be reduced (optional, not recommended now)

C14 → C15849 (−1), C1 → C53987 50 V Basic (−1, but the ESD margin is reduced); replacing the 5 E96 resistors (R6, R8, R10, R13, R14) with Basic values is only possible with recalculation (UVLO/OVLO/ILIM/FB/VBUS_MON), which would affect the values checked in round 7 (−5). There is no Basic alternative for the NTC, the connectors or the ICs.

## 9. `fields_apply.py` – fields into the schematic and onto the PCB

Usage: `python3 fields_apply.py <schematic directory> <board.kicad_pcb> [--parts parts.json] [--dry-run]` (plain python3 is enough, pcbnew is not needed). Every FIT symbol and its corresponding footprint gets hidden **LCSC / MPN / Manufacturer** fields (clones of their own "Datasheet" property block, with a new uuid on the PCB). Idempotent; does not touch DNP elements; prints the missing references.

Test on a copy of the master (`test/kicad/`):
- 71/71 symbols and footprints received the 3 fields (213 + 213); C14 "NOT FOUND" (not yet in the master – expected).
- `kicad-cli sch erc`: **0** (0 before as well). `drc.py`: errors **7** courtyards_overlap, unconnected **12**, parity **4 extra_footprint** (MH1–4) – **exactly the starting state**.
- Loaded in pcbnew, all 71 footprints have the 3 fields correct and hidden; a pcbnew re-save is **byte-identical** to the script's output (no format difference). `kicad-cli sch export bom` grouped by LCSC gives 39 rows, all matching `parts.json`.
- **Important:** the KiCad 10 parity check flags mismatching fields (`footprint_symbol_field_mismatch`, confirmed by a trial) → the script must **always be run on the schematic and the PCB together**, and **after the regional changes have been merged** (the fields modify the footprint blocks, which in a uuid-based merge would conflict with other agents' moves). C14 must first be added to both the schematic and the PCB.

## 10. Still to be confirmed by the owner

1. **J2 contact side (Q6)** based on the real camera module + FFC (TOP = current TE 1-84953-5); reserving the 31 pcs of stock.
2. **J5 mating (Q17)**: A (JLC Hong Cheng pair, ~2.3 mm engagement at 7 mm, [UNVERIFIED]) or B (Samtec 7.47 mm + 7.5 mm standoff + footprint change).
3. **U5** accept the second source (TECH PUBLIC) or procure the TI original.
4. **C1** accept the 200 V 0603 part (or a 1206 footprint for 1 kV).
5. **L1** land pattern against the Taiyo NRS5024 drawing; **D20** brightness (value of R30).
6. Before ordering: refresh stock levels (J2 31, R6 180, U3 331), check rotations and polarities in the JLC CPL preview (D1, D20, U2–U6, J1, J2, J4), double-sided Standard PCBA, U1 + MH + TP excluded.
