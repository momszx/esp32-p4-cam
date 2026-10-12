# Documentation index

This folder holds the design documentation of ESP32-P4-CAM. The English documents here are the **primary** set. [`hu/`](hu/) holds the Hungarian originals, frozen on 2026-10-12 and no longer maintained (the Hungarian originals of the fabrication notes are in [`../kicad/MAIN/fab/hu/`](../kicad/MAIN/fab/hu/)). Where documents disagree, [`05-architecture.md`](05-architecture.md) wins.

Project overview, current status and quick start: [top-level README](../README.md).

## Documents

| Doc | Content |
|---|---|
| [00-requirements](00-requirements.md) | Goal, mandatory requirements (K1–K8), extra features, use case, document map |
| [01-esp32-p4](01-esp32-p4.md) | Early ESP32-P4 hardware research (2026-10-09): chip variants, power, boot and strapping, camera interfaces. Partly superseded by 05 |
| [02-esp32-c6-and-programming](02-esp32-c6-and-programming.md) | ESP32-C6 options, esp-hosted P4 ↔ C6 link, programming both chips, power |
| [03-camera-ov5640](03-camera-ov5640.md) | OV5640 interfaces and P4 support, FPC connectors and pinouts, camera power and control |
| [04-peripherals](04-peripherals.md) | microSD, microphone, IR night vision, buttons and LED, USB-C power |
| [**05-architecture**](05-architecture.md) | **Authoritative.** Rev A plan (§0: fit/DNP, gates, procurement), primary-source facts, PCB stack and the frozen mechanical interface (§3.1a), stackup (§3.2), power tree and budget (§4), GPIO map, connectors, test points, bring-up sequence (§15), open questions (§17) |
| [06-floorplan](06-floorplan.md) | Area and height budget (7 mm gap), ASCII floorplans, conflicts, as-built placement of MAIN |
| [07-bom-plan](07-bom-plan.md) | Rev A BOM with MPN/LCSC numbers, value-calculation sheet, USB-C pin map, CAM_3V3 load switch |
| [08-diagrams](08-diagrams.md) | Mermaid diagrams derived from 05: block, power tree, net map, J5 and J2 pinouts, stack, programming, gates |
| [09-pcb-layers](09-pcb-layers.md) | As-built MAIN rev A layer plots (L1–L4, mask/silkscreen, 3D views), stackup and copper statistics |
| [90-review-log](90-review-log.md) | Chronological record of the review rounds and layout work, with corrections to earlier entries |
| [`img/`](img/) | Board renders, routing snapshots and layer plots used by the documents |

Documents 01–04 are research notes from the start of the project. Each one opens with a banner listing the points that 05 has since overridden.

### Outside `docs/`

| File | Content |
|---|---|
| [`kicad/MAIN/fab/ORDERING.md`](../kicad/MAIN/fab/ORDERING.md) | JLC ordering guide: files, PCB form settings, assembly notes, pre-power checks, firmware rules for rev A, accepted deviations |
| [`kicad/MAIN/fab/BOM_NOTES.md`](../kicad/MAIN/fab/BOM_NOTES.md) | Part selection rationale, low-stock items, J2/J5 options, items still to be confirmed by the owner |
| [`kicad/MAIN/scripts/README.md`](../kicad/MAIN/scripts/README.md) | Layout automation scripts (placement, routing, merge), their status and known pitfalls |

## Conventions

The same terms are used in every document:

| Term | Meaning |
|---|---|
| **MAIN / FRONT** | The two boards of the stack. MAIN carries the module, power and camera connector; FRONT (not started) carries the IR LEDs and the microphone. |
| **F side / B side** | F = front copper (L1), also called the top or front side of MAIN (camera-facing). B = back copper (L4), also called the bottom or back side (module side). |
| **rev A / rev B** | rev A is the 4-layer 45 × 45 mm MAIN board (v0.6) that is being ordered; rev B collects the deferred items. Early entries of the review log (and the script comments) use "rev A" for the abandoned 2-layer 60 × 50 mm draft. |
| **FIT / fitted** | The part is placed in the rev A assembly. |
| **DNP** | Do not populate: the footprint is on the board, the part is not fitted. |
| **as-built** | Measured from the actual board file, as opposed to the plan. |
| **gate (G0–G6, G5b)** | A project checkpoint with an exit criterion; the next gate starts only after the previous one is closed (05 §0.2). |
| **round** | One numbered iteration of review or layout work in the review log. Rounds 7–9 are the MAIN PCB review (NO-GO), the fix passes, and the final review (conditional GO). |
| **fix pass** | One parallel, region-fenced fixing step inside round 8. |
| **pre-order gate** | The checks to repeat on the exact board file before ordering: refill and save inside `kicad/MAIN`, then DRC without refill, ERC (see `ORDERING.md`). |
| **owner** | The project owner, who takes the decisions marked 👤 and the open questions (Qn). |
| **Qn** | Open question, listed in 05 §17. |
| **En** | Browser-verified primary-source fact, 05 §1 (for example E20 = module pad map). |
| **X-n** (E-7, P-17, F-1, B-6, A-25, C-22, K-19, …) | Item of a review round in the review log; the letter is the reviewer group. |
| **K1–K8 / 00-Kn** | Mandatory requirements in 00. **06-Kn** = conflict Kn in 06. |
| **[UNVERIFIED]** | Not yet confirmed by a primary source (datasheet, schematic, measurement). |
| **[VERIFIED – source]** | Confirmed, with the source named (used in the research notes 03–04). |
| **[WS]** | Taken from a web-search excerpt; the full source was not read (01). |
| **[F]** | Assumption (05, 06, 08); the letter comes from the Hungarian original. |
