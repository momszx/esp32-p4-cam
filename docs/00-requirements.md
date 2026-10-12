# 00 – Requirements and decisions

Date: 2026-10-09 · Status: **design / documentation phase**

## Goal
Compact camera that streams over WiFi (RTSP/MJPEG, HW H.264), based on the ESP32-P4.

## Mandatory requirements
| # | Requirement | Note |
|---|---|---|
| K1 | Main MCU: ESP32-P4 | Bare chip vs module: research decides (`01-esp32-p4.md`) |
| K2 | Wireless: ESP32-C6 coprocessor | The P4 has no radio; esp-hosted (`02-esp32-c6-and-programming.md`) |
| K3 | Camera: OV5640 (or a better-supported alternative) | connector: `03-camera-ov5640.md` |
| K4 | PCB: **MAIN 4 layers, 45×45 mm** (v0.6, 2026-10-09 owner decision – compact camera; routing of the 2-layer 60×50 rev A did not close: GND fragmentation, saturated under-module zone). FRONT: 2 layers, if sufficient | JLC04101H-3313A, L2 = continuous GND → proper CSI/USB/RF impedance |
| K5 | Compact: several stacked PCBs | pin header / board-to-board |
| K6 | Both chips must be programmable | P4 + C6 flash path |
| K7 | Power: **USB-C, PD sink (9 V), reduced mode on PC 5 V** | no battery; details: `05` §4 |
| K8 | **OTA update (P4 + C6)**, USB only for the first flash | `05` §9–10 |

## Extra features (owner decision)
- microSD card
- Microphone (PDM MEMS)
- IR LED + IR-cut filter (night vision)
- Button + status LED

> **Rev A:** proof-of-concept prototype (MAIN first, gates G0–G6, DNP blocks): `05` §0. The K IDs in this file are referenced as **00-Kn** (e.g. 00-K8 = OTA).

> **Enclosure: later.** For now only the PCBs are being designed; enclosure items: `05` §18.

## Use case
WiFi live-view stream (RTSP / MJPEG). Continuous power → deep sleep is not a priority, thermal management is.

## Document map
Full index with descriptions and conventions: [`README.md`](README.md).

| File | Content |
|---|---|
| `01-esp32-p4.md` | P4 pinout, power, boot, camera interfaces |
| `02-esp32-c6-and-programming.md` | C6 module, P4↔C6 link, programming |
| `03-camera-ov5640.md` | OV5640 interface, connector, power rails |
| `04-peripherals.md` | microSD, microphone, IR, button/LED, USB-C power |
| `05-architecture.md` | **Rev A plan (§0, gates G0–G6)**, PCB stack, power tree, GPIO assignment (E20 pad map), connectors |
| `06-floorplan.md` | Area and height budget (G = 7 mm), ASCII floorplan, conflicts (06-Kn) |
| `07-bom-plan.md` | BOM skeleton (MPN/LCSC/package/footprint/rev A fit-DNP), value calculation sheet, USB-C pin map, CAM_3V3 CT |
| `08-diagrams.md` | Block, power, net-map, connector, stack and gate diagrams (Mermaid), derived from 05 |
| `09-pcb-layers.md` | As-built MAIN rev A layer plots, stackup and copper statistics |
| `90-review-log.md` | Results of the review rounds |
