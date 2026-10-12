# 09 – MAIN rev A PCB layers (as-built, 2026-10-12)

Board: `kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb`, 45 × 45 mm, 4 layers, JLC04101H-3313A stackup, ENIG, 1.0 mm nominal thickness.

All plots are viewed **from the top (F side)**, including the bottom layer, unless the file name says `mirrored`. They use KiCad coordinates: origin at the top-left corner, X to the right, Y down (see [05 §3.1a](05-architecture.md)).
The images were generated from the board file with `kicad-cli` and `rsvg-convert`. The net-class maps come from a small pcbnew script. To regenerate them, see [Regenerating](#regenerating).

## Stackup

| Layer | Name | Material | Thickness | Use |
|---|---|---|---|---|
| L1 | F.Cu | Cu 1 oz | 0.035 mm | components (front), CSI, USB, buck, power entry, GND pour |
| – | prepreg | 3313 + 1080 | 0.107 + 0.0764 mm | Dk ≈ 4.1 / 3.91 |
| L2 | In1.Cu | Cu 0.5 oz | 0.0152 mm | **solid GND plane** (reference for L1) |
| – | core | FR4 | 0.5 mm | Dk ≈ 4.6 |
| L3 | In2.Cu | Cu 0.5 oz | 0.0152 mm | **power planes (VBUS, VBUS_SW) + GND fill**, slow signal routing (reference for L4) |
| – | prepreg | 1080 + 3313 | 0.0764 + 0.107 mm | |
| L4 | B.Cu | Cu 1 oz | 0.035 mm | module (U1, hand-soldered), USB-C, RF, signal routing, GND pour |

Impedance targets (JLC calculator, outer layer referenced to the adjacent plane):

| Net class | Width / gap | Target |
|---|---|---|
| RF_50 | 0.302 mm | 50 Ω single-ended |
| CSI_DIFF | 0.204 / 0.203 mm | 100 Ω differential |
| USB | 0.262 / 0.203 mm | 90 Ω differential |

Copper statistics (as-built):

| Layer | Tracks | Track length | Filled zones |
|---|---|---|---|
| F.Cu | 831 | 836 mm | GND_F 1038 mm² (20 islands), BK_3V3_F 18 mm² (buck output) |
| In1.Cu | 0 | – | GND_In1 1793 mm², **1 island** (≈ 89 % of the board) |
| In2.Cu | 263 | 798 mm | GND_In2 1040 mm² (32 islands), PWR_VBUS_In2 139 mm² (1 island), PWR_VBUSSW_In2 151 mm² (1 island) |
| B.Cu | 654 | 812 mm | GND_B 1006 mm² (16 islands) |

There are 306 vias: 236 × 0.5/0.25 mm, 69 × 0.6/0.3 mm and 1 × 0.5/0.3 mm. 148 of them are GND stitching or return vias. All vias are through vias, tented.
Footprints: 85 on F and 43 on B. Fitted SMD parts: 47 on F and 25 on B; the U1 module is hand-soldered on B.

Colour key of the net-class maps (`netmap_*.png`):

| Colour | Meaning |
|---|---|
| grey | GND |
| red | VBUS (USB-C input, before the eFuse) |
| orange | VBUS_SW (after the eFuse U3, buck input) |
| salmon | other PWR nets (3V3_BUCK, BK_SW, IR branch) |
| lilac | PWR_LIGHT (+3V3, CAM_3V3, SD_3V3) |
| green | MIPI CSI-2 differential pairs |
| blue | USB FS D+/D− |
| magenta | RF 50 Ω (module P2 → R34 → u.FL J4) |
| light grey | other signals |
| dashed white | rule areas / keep-outs (MH keep-outs, `KO_RF_In2`, `KO_VBUS_In2`, `CSI_STUB_In2_NOTRACK`, `J1_BODY_NOVIA`) |

## L1 – F.Cu (top)

![L1 F.Cu net-class map](img/layers/netmap_L1_F_Cu.png)

Contents:
- J2, the camera FPC on the top edge, and its CSI breakout to the module pads.
- The buck converter U4 TPS62933F. It has a tight input loop: C9 and C8 sit directly at pins 3/4, and the loop measures about 1.4 mm². The switch node stays on F only, and the BK_3V3_F output island is included.
- The eFuse U3 with C14 at its OUT pin, CH224A U2, the USB ESD part U5, and J5 (the board-to-board connector to FRONT) on the bottom edge.
- The GND pour, stitched to In1.

KiCad plot (copper only):

![L1 F.Cu plot](img/layers/L1_F_Cu.png)

## L2 – In1.Cu (solid GND plane)

![L2 In1.Cu net-class map](img/layers/netmap_L2_In1_Cu.png)

This layer holds no tracks: it is one continuous GND island covering about 89 % of the board. The only holes are via antipads and the mounting holes.
During the review rounds, rows of antipads near the buck and the USB via cluster were broken up so the plane stays solid under the hot loop, the switch node, the feedback network and the CSI lanes.

![L2 In1.Cu plot](img/layers/L2_In1_Cu_GND.png)

## L3 – In2.Cu (power planes + GND fill)

![L3 In2.Cu net-class map](img/layers/netmap_L3_In2_Cu.png)

Contents:
- **PWR_VBUS_In2** (red): USB-C VBUS from J1 to the eFuse input. One island; a DRU rule keeps it at least 1 mm from the board edge, and the `KO_VBUS_In2` keep-out keeps tracks out of it.
- **PWR_VBUSSW_In2** (orange): eFuse output to the buck input. One island.
- **GND_In2** fills the rest. It is the reference plane for the B.Cu RF line and the CSI B.Cu stubs:
  - `KO_RF_In2` keeps every non-GND conductor out from under the RF path.
  - `CSI_STUB_In2_NOTRACK` keeps tracks out from under the CSI stubs.
- Low-speed signals and +3V3 distribution are routed here as well.

![L3 In2.Cu plot](img/layers/L3_In2_Cu_power.png)

## L4 – B.Cu (bottom, viewed from the top)

![L4 B.Cu net-class map](img/layers/netmap_L4_B_Cu.png)

Contents:
- The Waveshare ESP32-P4-Module (U1) land pattern. U1 is hand-soldered after SMT.
- USB-C J1 on the right edge and the u.FL J4 on the left edge.
- The RF line U1.P2 → R34 → J4: 0.302 mm wide, with a GND via fence on both sides.
- The decoupling cluster C20–C23 at module pins P84–P86.
- Test pads TP1–TP7, TP16A/B and TP17–TP19, plus BOOT/RESET/USER switches, D1, D20 and the J7 UART pad row.
- The GND pour.

![L4 B.Cu plot](img/layers/L4_B_Cu.png)

Both outer copper layers overlaid (red F, blue B):

![F + B copper](img/layers/F_and_B_Cu.png)

## Solder mask and silkscreen

Front (F.Mask + F.Silkscreen), viewed from the top:

![Front silkscreen and mask](img/layers/F_silk_mask.png)

Back (B.Mask + B.Silkscreen), **mirrored**, i.e. as seen when looking at the bottom side:

![Back silkscreen and mask, mirrored](img/layers/B_silk_mask_mirrored.png)

## 3D views

| Top | Bottom |
|---|---|
| ![3D top](img/main_revA_top.png) | ![3D bottom](img/main_revA_bottom.png) |

![3D isometric, top](img/layers/3d_iso_top.png)

![3D isometric, bottom](img/layers/3d_iso_bottom.png)

## Regenerating

```bash
cd kicad/MAIN
kicad-cli pcb export svg --mode-single --page-size-mode 2 --exclude-drawing-sheet --layers "In2.Cu,Edge.Cuts" -o /tmp/In2.svg ESP32-P4-CAM-MAIN.kicad_pcb
rsvg-convert -w 1400 -b '#101418' /tmp/In2.svg -o ../../docs/img/layers/L3_In2_Cu_power.png
kicad-cli pcb render --side top --perspective --rotate "-35,0,30" --zoom 0.9 --width 1400 --height 1100 --quality high -o ../../docs/img/layers/3d_iso_top.png ESP32-P4-CAM-MAIN.kicad_pcb
```

To regenerate the net-class maps, run `kicad/MAIN/scripts/netmap_svg.py`, then convert its SVG output with `rsvg-convert`:

```bash
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 kicad/MAIN/scripts/netmap_svg.py kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb /tmp
rsvg-convert -w 1700 /tmp/netmap_L3_In2_Cu.svg -o docs/img/layers/netmap_L3_In2_Cu.png
```

The script refills zones in memory only; it never saves the board.
