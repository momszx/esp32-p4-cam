# ESP32-P4-CAM MAIN rev A – JLC ordering guide (2026-10-11)

Source: `kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb`. The zones are filled using the project rules. Pre-order gate: DRC **without** zone refill 0 errors, ERC 0, schematic↔board parity 0, and 12 unconnected items, all on DNP parts.

## Files to upload

| File | Purpose |
|---|---|
| `gerber_jlc.zip` | PCB: 4 copper layers, plus mask, paste, silkscreen and edge layers, and PTH/NPTH drill |
| `BOM_jlc.csv` | PCBA bill of materials: 40 unique line items with LCSC numbers, 72 placements |
| `CPL_jlc.csv` | placement file: 72 rows, 47 top + 25 bottom, matches the BOM exactly |
| `BOM_NOTES.md`, `parts.json` | part selection rationale, stock, price |

## PCB settings (JLC form)

| Field | Value |
|---|---|
| Layers | 4 |
| Size | 45 × 45 mm (the gbrjob says 45.1 because of the outline line width) |
| Thickness | 1.0 mm |
| **Stackup** | **JLC04101H-3313A** – this one must be selected explicitly; the trace widths are only correct for this stackup |
| **Impedance control** | **Yes** (50 Ω RF 0.302 mm; CSI 100 Ω 0.204/0.203; USB 90 Ω 0.262/0.203) |
| Copper | outer 1 oz, inner 0.5 oz |
| **Surface finish** | **ENIG** (0.2 mm pad gaps on U3/U4/J1; JP1 is an open solder jumper) |
| Via | tented (covered), through vias only; minimum drill 0.25 mm, pad 0.5 mm |
| Panel | single board; **frame rails on the top and bottom edges only**, with fiducials on them |
| Tab / V-cut | **nothing on the right edge** (C3, R10, C1 are 0.7 mm from the edge), no V-cut anywhere |

## Assembly (PCBA)

- Double-sided SMT, 0.10 mm stencil. The U3 paste is reduced per the TI recommendation (82 / 93 %). There is no paste on U1 or on the DNP parts.
- **U1 (Waveshare ESP32-P4-Module) is not in the BOM.** You solder it by hand after SMT. Use a fine conical tip on pins P83–P88, then inspect the gap between P87 and C23, as well as the R34/J4 solder joints.
- **J1 USB-C retention legs:** the 4 shell legs will probably not solder properly in SMT. Request hand or selective soldering from JLC, or solder them yourself before plugging in a cable for the first time.
- **In the JLC placement preview, check** rotation and pin 1 for:
  - U2, U3, U4, U5, U6;
  - D1 (cathode on the VBUS side), D20;
  - J1, J2, J4, J5;
  - all 25 bottom-side parts.
- **Reserve in advance** (low stock):
  - J2 – C5164008, 31 pcs;
  - U3 – C3662799, ~330 pcs;
  - R6 – C22963, 180 pcs.
- Extended parts: 24 items, approx. 72 USD setup fee. Parts cost approx. 8.8 USD/board, excluding U1.
- U5 (TECH PUBLIC C5350871): I checked the pinout on the LCSC product page: 1 IO1, 2 IO2, 3 GND, the same as the TI part.

## Before first power-on (ohmmeter, U1 soldered in)

1. TP16A (ESP_EN) ↔ TP4 (+3V3): approx. 10 kΩ. If it reads 0 Ω, P87 and C23 are bridged.
2. 3V3_BUCK ↔ GND: between 5–16 kΩ. A higher value indicates an R14/R15/R33 fault; in that case the buck may output as much as 9 V.
3. VBUS ↔ VBUS_SW: approx. 300 kΩ, with JP1 open.
4. VBUS, D+, D− ↔ GND: no short circuit.

## Firmware rules for rev A

- I2C at 100 kHz.
- The CH224A is read-only, and only after CAM_3V3 has been switched on. **Never write to it**: through register 0x0A it could request 20/28 V.
- Derive the PD mode from the PG pin and the VBUS_MON ADC.
- Keep IR_SW_EN low.
- Never enable the USB HS PHY on this layout: FS only (12 Mbps).

## Mechanics

- Holes MH1, MH2 and MH4 need a nylon standoff or washer.
- No washer at MH3: the screw head must be at most Ø4.0 mm, and the u.FL cable must exit towards the west or north.

## Owner decisions (they do not block PCB fabrication)

- **Q6 – J2 contact side and the FFC cable:** must be decided with the real camera and cable before the first camera power-on. If the pin order is reversed, swap the cable for the other type (same-side ↔ opposite-side contacts).
- **Q17 – J5 board-to-board connector height:** the chosen Hong Cheng pair is 5.3 mm. With a 7.0 mm standoff this gives approx. 2.3 mm of engagement. The FRONT board needs a taller socket; the MAIN board is not affected.

## Deviations deliberately accepted for rev A (based on the round 9 review)

- The D1 TVS is at the eFuse input, not next to J1.
- The CSI data-to-clock skew is ≈0.05 UI, CLK is 21.4 mm. G5b requires a soak test with error counters for it.
- The reference of the USB FS lines is partly the VBUS_SW plane or empty area.
- The layer transitions of the +3V3 main trace go through single vias, 21 mΩ.
- Gaps in the GND via fence along the board edge.
- ESD protection for J2/SD/CC deferred to rev B.
- The via drills at R14.1 and R27.2 overhang into the pad by 0.03 / 0.07 mm (same net). Measurement step 2 covers this.
- 12 unconnected items, all on DNP parts (CC1/CC1_ADC/CC2/CC2_ADC, U7/R73). **If you ever fit these parts, route them first.**
