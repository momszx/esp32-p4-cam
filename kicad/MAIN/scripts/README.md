# MAIN board layout automation scripts

These are the scripts used to place, route and finish the **ESP32-P4-CAM MAIN** PCB (`../ESP32-P4-CAM-MAIN.kicad_pcb`).
They are working tools written while the board was being laid out, not a polished library. The board went through two phases,
and many scripts belong to only one of them:

| Phase | Board | Notes |
|---|---|---|
| 2L draft (2-layer) | 60 x 50 mm, F.Cu + B.Cu | Routing never closed (GND fragmentation and congestion). Abandoned; snapshot in [`../../archive/MAIN_2L_60x50_2026-10-09/`](../../archive/MAIN_2L_60x50_2026-10-09/). |
| v0.6, 4-layer (current) | 45 x 45 mm, stackup JLC04101H-3313A (In1 = solid GND plane, In2 = power zones + GND fill) | Routed, reviewed, fab package in [`../fab/`](../fab/) (see [`ORDERING.md`](../fab/ORDERING.md)). |

**Naming:** the script comments (and the early entries of the [review log](../../../docs/90-review-log.md)) say "rev A" for
the 2-layer 60 x 50 draft. The board that is actually ordered as **rev A** is the 4-layer v0.6 board. This README uses
"2L" for the draft.

Every script was written for this one board. Coordinates, reference designators, net names and file paths are baked in unless
noted otherwise. Read a script before you run it. **Most of them write the master board in place, so back it up first.**

Tested with KiCad 10.0.5 (`kicad-cli`), its bundled Python 3.9, and system Python 3.11 with numpy 2.4.

---

## Two Python interpreters

The scripts need two different interpreters. Using the wrong one fails right away on `import pcbnew` or `import numpy`.

| Interpreter | Has | Lacks | Used for |
|---|---|---|---|
| **KiCad Python** `/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3` | `pcbnew` | numpy | everything that loads or saves a board |
| **System `python3`** | numpy | `pcbnew` | the grid router (`maze.py`) and its raster helpers, JSON-only tools, orchestrators that call the KiCad interpreter as a subprocess |

The examples below use these shell variables:

```bash
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
BOARD=/path/to/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb
```

## Status legend

- **current**: used on the finished 4-layer board, safe to run there (after a backup).
- **reusable**: a general tool. It does not depend on this board, or only needs its paths or constants parameterised.
- **historical**: a one-off from the 2L phase or the early 4-layer phase. Its coordinates no longer match the board. It is kept as a reference and as a pattern to copy.
- **do-not-use**: known to damage the board or make routing worse.

## Index

### `scripts/`

| Script | Interpreter | Status | Purpose |
|---|---|---|---|
| `pcbmerge.py` | either (stdlib only) | **reusable** | 3-way merge of `.kicad_pcb` files, keyed by uuid, with conflict detection (for parallel editing) |
| `regioncheck.py` | KiCad | **reusable** | Fence check: every item an editor removed, changed or added must lie inside its assigned region |
| `project_rules.py` | system (stdlib only) | **current** | Single source of truth for board rules, net classes and net-class patterns; writes them into `.kicad_pro` |
| `gnd_pour.py` | KiCad | **current** | (Re)creates the GND pours on F, B and In2 and refills every zone |
| `move.py` | KiCad | reusable | Moves footprints to positions listed in a JSON file, flipping sides if needed |
| `legalize.py` | KiCad | historical (early 4L), reusable idea | Push-apart legalizer that removes courtyard overlaps |
| `freespot.py` | KiCad | historical (early 4L), reusable idea | Moves parts to the nearest free spot (spiral search) |
| `power_place.py` | KiCad | historical (early 4L) | One-off re-placement of the power block |
| `place45.py` | KiCad | **do-not-use** on the current board | One-off 2-layer to 4-layer conversion; **deletes all copper, zones and the outline** |
| `route_csi4.py` | KiCad | historical (early 4L) | Scripted MIPI-CSI routing with skew-matching serpentines; rips everything in the CSI corridor |
| `prep4.py` | KiCad | historical (early 4L) | Freerouting DSN export for 4 layers (GND kept as the In1 plane) |
| `place.py` | KiCad | historical (2L) | Netlist to footprints, nets and 2L 60 x 50 placement |
| `gpio_swap_pcb.py` | KiCad | historical (2L) | One-off v0.6 GPIO reassignment on U1 pads, plus moves for J7, R27 and R28 |
| `autoroute_prep.py` | KiCad | historical (2L) | Freerouting DSN export for 2 layers (drops GND, adds an RF keepout, removes TP footprints) |
| `route_csi.py` | KiCad | historical (2L) | Scripted CSI routing for the 2L board |
| `route_pwr.py` | KiCad | historical (2L) | Scripted power trunks for the 2L board (also deletes GND copper and nudges parts) |
| `route_rf.py` | KiCad | historical (2L) | Scripted RF line plus J4, C27, R34 and C28 placement for the 2L board |
| `route_usb.py` | KiCad | historical (2L) | Scripted USB FS routing plus U5 placement for the 2L board |

### `scripts/maze/` (custom grid router and its drivers)

| Script | Interpreter | Status | Purpose |
|---|---|---|---|
| `kgeom.py` | KiCad | **current / reusable** | Bridge between the board and the router: `export` obstacles, `apply` routes, `gndmap` |
| `maze.py` | system + numpy | **current / reusable** | A* router on a 0.05 mm grid over 3 routing layers, with an optional SOFT rip-up mode |
| `ripthru.py` | system (orchestrator) | **current / reusable** | Targeted rip-up and reroute: SOFT search, rip only the crossed items, reroute the victims, keep only on improvement |
| `prune.py` | KiCad | **current, use with care** | Removes redundant copper (loops and dead-end stubs) using a per-net spanning tree |
| `errs.py` | system (stdlib only) | current | Counts "real" DRC errors in a kicad-cli JSON report (ignores stale-fill zone clearances and starved thermals) |
| `view.py` | system + numpy | reusable (debug) | Renders the router's obstacle raster for a box to `v.ppm` |
| `gnd_fanout.sh` | bash | historical (early 4L), reusable pattern | DRC-guarded GND pad to via fan-out to the In1 plane |
| `guarded.sh` | bash | historical (early 4L, with `NOGND=1`) | Routes every DRC open one by one and reverts any route that adds errors |
| `zone_drop.py` | system + numpy | historical (early 4L) | Connects power-net pads to their In2 power zone with a stub and a via |
| `ripall.sh` | bash | historical (early 4L), superseded by `ripthru.py` | Box rip-up around each open, then reroute, kept only on improvement |
| `ripup.py` | system (orchestrator) | historical, superseded by `ripthru.py` | Box rip-up plus a greedy reroute loop (endpoint layers 0/1 only) |
| `finish4.sh` | bash | historical (early 4L) | Freerouting, then GND fan-out, then guarded maze, then a DRC report |
| `island_stitch.py` | system + numpy | historical (2L only) | Finds GND copper islands and proposes stitching vias or maze pairs |
| `stitch.py` | system + numpy | historical (2L) | RF fence, CSI return vias and a GND stitching grid (2L coordinates) |
| `gnd_fix.sh` | bash | historical (2L) | Iterative GND island joining (vias, then `ripup.py`) |
| `region_reroute.sh` | bash | historical (2L) | Region rip-up, then Freerouting, then maze leftovers, then cleanup; best of N |
| `finish.sh` | bash | historical (2L) | `region_reroute.sh`, then a GND island loop, then a report |
| `route_all.py` | system (orchestrator) | **do-not-use** | Global rip-all and reroute. It made routing worse. |
| `cleanup.py` | KiCad | **do-not-use** on this board | Deletes items DRC flags as dangling. On this board those are T-junction bridges, and deleting them opens nets. |

---

## Reusable tools in detail

### `pcbmerge.py`: uuid-keyed 3-way merge of `.kicad_pcb`

This is a text-level merge of KiCad 10 board files (net names are inline, so there are no top-level `(net ...)` items). Each
**top-level s-expression item** of the board (footprint, segment, via, arc, zone, gr_*, group and so on) is keyed by its
`(uuid ...)`. Items without a uuid (`version`, `general`, `setup`, `layers` and similar) are keyed as `head#n`.

- **Zone fills are ignored.** `(filled_polygon ...)` blocks are stripped before items are compared or hashed, so a refill alone never counts as a change.
- `diff` produces a delta with three parts: `removed` (key to the base hash), `added` (key to the item text) and `changed` (key to the base hash plus the new text).
- `apply` applies one or more deltas to a master board. It reports a **conflict** in three cases: the master's current text for a removed or changed item does not hash to the delta's base hash; two deltas touch the same key; or an added key already exists. On any conflict it prints `CONFLICT <delta> <kind> <key>` lines, **exits 1 and writes nothing**.
- New items are appended before the root's closing paren. Removed items are cut out together with their leading newline and indent.

```bash
python3 pcbmerge.py                                  # selftest
python3 pcbmerge.py diff  base.kicad_pcb mod.kicad_pcb delta.json
python3 pcbmerge.py apply master.kicad_pcb deltaA.json deltaB.json ...   # edits master in place
```

**Requirement:** every board must have been saved by the same pcbnew version. Load and save the base once with pcbnew to
normalise it, so unchanged items stay byte-identical and do not show up as changes.

**After a merge:** the merged zone fills are stale. Refill (`$KPY gnd_pour.py fill`), re-run `project_rules.py`, then run DRC.

### `regioncheck.py`: region fence for parallel editing

```bash
$KPY regioncheck.py base.kicad_pcb mod.kicad_pcb "x0,y0,x1,y1;x0,y0,x1,y1"   # mm, union of rectangles
```

The script runs `pcbmerge.diff` and then checks the bounding box of every removed item (as it was in the base), every added
item (in mod), and every changed item (in both). Each **corner** of the bounding box must lie in some rectangle, with a
0.05 mm tolerance. A footprint's bounding box is the union of its pad boxes. Changes to non-uuid items such as `setup` are
always reported. The script prints `REGION OK` and exits 0, or prints `OUTSIDE REGION ...` lines and exits 1.

The corner test is approximate. It is enough when the rectangles tile the board, but an item whose corners land in two
different rectangles passes even if it crosses a gap between them.

### Parallel region-fenced editing workflow

This workflow let several agents fix different parts of the board at the same time:

1. Normalise the master: load and save it once with pcbnew. Copy it to `base.kicad_pcb`.
2. Give each editor a **full project copy** (board, `.kicad_pro` and `.kicad_dru`) in its own directory, plus a region given as rectangles.
3. Each editor changes only copper and parts inside its region. Editors may refill zones, because fills are ignored. They must **not** re-create pours (`gnd_pour.py` without `fill`): that replaces whole-board zones with new uuids and fails the fence. Note that `gnd_pour.py` (like most scripts here) has the **master** board path hardcoded, so on a copy it must be patched first or it edits the master.
4. The coordinator runs `regioncheck.py base mod "<region>"` for each editor, then `pcbmerge.py diff base mod <key>.json`.
5. The coordinator backs up the master, runs `pcbmerge.py apply master A.json B.json ...` and resolves any conflicts by hand.
6. Refill the zones, run `project_rules.py`, run DRC (`$CLI pcb drc --format json ...`), and check `errs.py` and the unconnected count.

### `kgeom.py` + `maze.py`: custom grid router

`kgeom.py` (KiCad Python) converts between the board and plain JSON. `maze.py` (system Python with numpy) does the search.

**`kgeom.py`**

```bash
$KPY kgeom.py export  $BOARD geom.json    # obstacles: pads + tracks + vias per routing layer, inflated by clearance
$KPY kgeom.py apply   $BOARD routes.json  # adds the routed segments/vias, saves the board in place
$KPY kgeom.py gndmap  $BOARD gnd.json     # actual GND copper (zone fills, pads, tracks) + GND via positions
```

- Routing layers are `0 = F.Cu`, `1 = B.Cu` and `2 = In2.Cu`. In1 is the GND plane and is not routed.
- Each obstacle polygon is inflated by the clearance of its own net class. These values come from the `CLR` table, which **must mirror `project_rules.py`**. When the table still held 2-layer values, the router reported false `NO ROUTE` results.
- Each polygon is exported twice: once inflated for a track (`t`) and once for a via (`v`). It also records whether it is locked or a pad (`lk`) and its uuid (`id`), which SOFT mode needs. A pad's drilled hole is added as an obstacle on routing layers where the pad has no copper (NPTH: all three layers; PTH: F.Cu and B.Cu only). Rule-area keepouts, including the ones inside footprints, are exported separately.
- `apply` reuses an existing same-net via within 0.8 mm instead of stacking a new one. Vias are 0.5/0.25 mm for the `Default` net class and 0.6/0.3 mm otherwise. New tracks are **unlocked**.
- Environment variables:
  - `TRACK_W` (default `0.2`): the routed track width. It is used for both export inflation and apply, so **use the same value for both steps**. Use `0.1` for tight low-speed escapes.
  - `GRID_MARGIN` (default `0.03`): extra inflation to absorb raster error. Use `0` or `0.02` for tight pin escapes, and only together with a DRC guard.

**`maze.py`**

```bash
python3 maze.py geom.json <NET> <ax,ay,layers> <bx,by,layers> out.json [append]
python3 maze.py geom.json GND   <ax,ay,layers> VIA            out.json   # fan-out: route to the nearest legal via spot
```

- The `layers` field is a digit string: `0` for an F.Cu SMD pad, `1` for B.Cu, and `012` for a PTH pad or a via endpoint. The orchestrators read endpoints from the `pos` fields of `unconnected_items` in a kicad-cli DRC JSON report.
- The grid is 0.05 mm. Moves go in 8 directions, and each layer change costs `VIA_COST` = 30 steps (1.5 mm). The router keeps 0.65 mm from the board edge for copper and 0.85 mm for vias. It never places a via in or touching an SMD pad, including pads of its own net. It applies the DRC rule max(own clearance, obstacle clearance).
- The cell path is string-pulled into straight, **any-angle** segments, so the output is not restricted to 45 degree angles.
- Output: a JSON list of `{net, segs: [[layer, x1, y1, x2, y2], ...], vias: [[x, y], ...]}`. On failure the script exits non-zero with `NO ROUTE <net>`.
- **SOFT mode** (`SOFT=1`, with `SOFT_COST` per grid step, default 8) lets the path cross unlocked foreign copper at a cost. A via on top of soft copper costs an extra `4 * SOFT_COST`. The output then also lists `victims`: the uuids of the foreign tracks and vias whose clearance zone the path crosses. **A SOFT route is not DRC-safe**: applying one directly once caused shorts. Use it only through `ripthru.py`, which rips the victims first and then routes again in hard mode.
- The router connects **one pair of points** per call. Multi-pin nets are completed one DRC open at a time.
- Every net is routed at `TRACK_W`, whatever its net-class width. Set `TRACK_W` for power nets.
- DRC 0 on routed copper does not mean the layout is good. Review hot loops, return paths and reference planes separately.

A typical single-connection loop, run from `scripts/maze/` because these files use relative paths:

```bash
cd kicad/MAIN/scripts/maze
cp $BOARD /tmp/backup.kicad_pcb
$KPY kgeom.py export $BOARD geom.json
python3 maze.py geom.json I2C_SCL 12.3,4.5,0 30.1,22.0,012 r.json
$KPY kgeom.py apply $BOARD r.json
python3 ../project_rules.py
$CLI pcb drc --format json -o drc.json $BOARD
python3 errs.py drc.json          # revert from the backup if this went up
```

### `ripthru.py`: targeted rip-up and reroute

```bash
python3 ripthru.py <workdir> "NET" ...                       # bare net: take its first open from DRC
python3 ripthru.py <workdir> "NET ax,ay,L bx,by,L" ...       # explicit endpoints (maze.py syntax)
DEPTH=3 python3 ripthru.py <workdir> I2C_SCL EF_ILM          # recursion depth for victims (default 2)
```

For each job the script does the following:

1. Copies the board to `<workdir>/pre.kicad_pcb`, runs `project_rules.py` and DRC, and records the non-GND opens and the `errs.py` count.
2. Tries a normal (hard) maze route. If that fails, it runs a SOFT route to find the cheapest corridor and **deletes exactly the victim tracks and vias**, then routes again in hard mode.
3. Applies the new route and locks it temporarily. It then reroutes the victim nets' opens the same way with `depth - 1`, for up to 2 rounds.
4. Unlocks everything it locked and runs DRC again. **It keeps the result only if the non-GND opens dropped and the real errors did not rise.** Otherwise it restores the backup.

It edits the master board in place, at the hardcoded path, and writes `geom.json` and `r_rt.json` in `maze/`.

### `prune.py`: remove redundant copper

```bash
$KPY prune.py --dry     # report only
$KPY prune.py           # remove and save
```

For each net, the script builds a graph of pads, tracks and vias. Two items are connected when an endpoint of one hit-tests
the other, which also covers T-junctions. It keeps a minimum spanning tree that always includes locked items and prefers short
items, and then strips dead-end leaves that are not pads. It removes **unlocked tracks and vias only**. Nets joined by zones
(`GND`, `VBUS`, `VBUS_SW`), the empty net and `unconnected-*` are skipped, because the graph alone cannot prove their
connectivity. Arcs are not modelled properly (an arc ending on a pad is not detected).

**Always run DRC afterwards.** Once it cut an I2C_SCL link.

### `project_rules.py`: board rules and net classes

```bash
python3 project_rules.py
```

The script writes the v0.6 4-layer rules into `../ESP32-P4-CAM-MAIN.kicad_pro`. It does **not** touch the custom rules in `../ESP32-P4-CAM-MAIN.kicad_dru`.

- Board minimums: track 0.09 mm, hole 0.2 mm, via 0.45 mm, via annular ring 0.1 mm, clearance 0.15 mm.
- Net classes:

  | Class | Track (mm) | Clearance (mm) | Via d/drill (mm) | Diff pair w/gap (mm) |
  |---|---|---|---|---|
  | Default | 0.15 | 0.15 | 0.5/0.25 | - |
  | CSI_DIFF | 0.204 | 0.2 | 0.6/0.3 | 0.204/0.203 |
  | USB | 0.262 | 0.2 | 0.6/0.3 | 0.262/0.203 |
  | RF_50 | 0.302 | 0.25 | 0.6/0.3 | - |
  | PWR | 0.4 | 0.2 | 0.6/0.3 | - |
  | PWR_LIGHT | 0.3 | 0.2 | 0.5/0.25 | - |

- Patterns: `VBUS`, `VBUS_SW`, `3V3_BUCK`, `BK_SW`, `IR_VIN` and `IR_VIN_SH` map to PWR. `+3V3`, `SD_3V3`, `CAM_3V3` and `CAM_3V3_SW` map to PWR_LIGHT. `CSI_*` maps to CSI_DIFF, `USB_D*` to USB, and `RF*` to RF_50.

Run it after any KiCad GUI session, any MCP-server operation, and any pcbnew `SaveBoard` into the project directory (see
Gotchas). Every orchestrator except the 2L `gnd_fix.sh` runs it before each `kicad-cli` DRC. If you change a clearance here, also change the `CLR`
table in `maze/kgeom.py`.

### `gnd_pour.py`: GND pours and refill

```bash
$KPY gnd_pour.py         # re-create GND_F, GND_B, GND_In2 (whole-board rectangle) and refill all zones
$KPY gnd_pour.py fill    # refill all zones only, then save (any argument means fill-only)
```

Zone settings: priority 0 (the In2 power zones `VBUS`/`VBUS_SW` are priority 2 and take precedence), clearance 0.2 mm,
minimum width 0.2 mm, thermal reliefs with a 0.3 mm gap and 0.35 mm spokes, and islands always removed. The script never
deletes or re-creates `GND_In1` (the reference plane) or any rule area; it only refills them. It prints the filled area of
each GND zone.

Re-creating the pours replaces any hand-edited outline or setting of those three zones and gives them new uuids. On the
finished board, use `fill` unless you mean to reset the pours.

---

## Other scripts (usage notes)

### Placement (`scripts/`)

- **`move.py`**: `$KPY move.py positions.json`. The JSON is `{"REF": [x_mm, y_mm, rot_deg, "F"|"B"], ...}`. The script flips a footprint if the side differs, sets its position and rotation, and saves.
- **`legalize.py`**: `$KPY legalize.py [REF,REF,...]`. Pushes courtyard bounding boxes apart (plus a 0.15 mm gap) for up to 400 iterations, with a weak spring back to each part's original position and a 0.05 mm snap. Fixed obstacles are the big parts (`FIXED` set), the M2 keepouts, the J1 shell slots and locked F/B copper. With a REF list, only those parts move. Board size (45 x 45) and the mounting-hole centres are constants in the script.
- **`freespot.py`**: `$KPY freespot.py REF[,REF...]`. Spiral search (0.2 mm radius steps, current rotation or +90 degrees, 0.05 mm snap) for the nearest spot on the same side that is clear of courtyards, M2 keepouts, J1 slots and locked copper, and at least 0.4 mm from the edge. **If no spot is found it prints `None` and leaves the part at the last candidate it tried.** Keep a backup.
- **`power_place.py`**: `$KPY power_place.py`. A one-off anchor placement of the eFuse, CH224A and buck blocks (plus the VBUS_SW monitor divider and NTC) on F.Cu, followed by `legalize.py <printed refs>`.
- **`place45.py`**: `$KPY place45.py`. A one-off conversion to v0.6. It removes **all tracks, vias, zones and Edge.Cuts**, sets 4 copper layers and 0.97 mm thickness, draws the 45 x 45 outline with 1 mm corner radii, swaps SW1 to SW3 to `SW_SPST_B3U-1000P` and J7 to `PadRow_1x09_P1.27mm_SMD`, and places parts from its table. It skips the `MH*` mounting holes, which is why they kept their 2L positions. **Never run it on the routed board.**
- **`place.py`**: `$KPY place.py <netlist.xml>`, where the netlist is a KiCad XML export (`kicad-cli sch export netlist --format kicadxml`). Adds missing footprints, assigns pad nets, sets DNP and exclusion flags, and places the newly added parts from the 2L 60 x 50 table.
- **`gpio_swap_pcb.py`**: `$KPY gpio_swap_pcb.py <board>`. A one-off v0.6 GPIO swap on the U1 pads that also creates `unconnected-*` nets for freed pins, then moves J7, R27 and R28 using 2L-board coordinates. Do not re-run it.

### Scripted routing (`scripts/`)

- **`route_csi4.py`**: `$KPY route_csi4.py`. 4-layer MIPI-CSI. It first deletes all `CSI_*` copper and **rips every other net's copper and vias** in the F.Cu corridor (20.8, 9.0)-(34.2, 18.4) and the B/In2 corridor (27.0, 12.9)-(33.0, 18.0). It then draws locked 0.204 mm tracks with one via per signal, nested as D0 inner, D1 middle and CLK outer, adds trombone serpentines for intra-pair skew, and prints lengths and skew. The printed skew is not trustworthy: the round 7 review found that the D1/CLK serpentines are smaller than the track width and add almost no delay, and the round 8 fix pass reworked the CSI routing. Re-running the script on the final board would undo that work and delete the GND return vias added in the corridor.
- **`route_csi.py`, `route_pwr.py`, `route_rf.py`, `route_usb.py`**: hand-coded 2L routes, all of them idempotent for their own nets. `route_pwr.py` also deletes **all GND copper** except the USB ESD stub and nudges R16, R11, R3 and C2. `route_rf.py` and `route_usb.py` re-place J4, C27, R34, C28 and U5 using pad geometry. None of them apply to the 45 x 45 board.

### Freerouting preparation (`scripts/`)

Freerouting cannot be used on the final board (see Gotchas). These scripts are reference only.

- **`prep4.py`**: `$KPY prep4.py out.dsn`. Locks all tracks (unless `FR_RESPECT_LOCKS=1` is set), adds `MH_KEEPOUT_*` rule areas on all copper layers, and **saves the master**. It then exports a DSN with only the `GND_In1` plane and the rule areas, so Freerouting fans GND out to the plane.
- **`autoroute_prep.py`**: `$KPY autoroute_prep.py out.dsn`. The 2-layer version. It locks all tracks, adds `RF_F_KEEPOUT` at 2L coordinates, re-creates the MH keepouts, **deletes footprints TP9A, TP9B and TP10 to TP15**, saves the master, and exports a DSN with the pours and the GND net removed.

### Router drivers and helpers (`scripts/maze/`)

All `.sh` files are **bash** scripts. They use absolute paths or `cd` into the right directory themselves, so they can be
started from anywhere. Run them with `bash script.sh ...`. The DRC-open parsers in `guarded.sh`, `ripall.sh`,
`region_reroute.sh` and `ripup.py` only emit endpoint layer codes `0`, `1` and `01` (2-layer era, no In2); `ripthru.py`,
`route_all.py` and `gnd_fanout.sh` also handle In2.

- **`errs.py`**: `python3 errs.py drc.json`. Prints the number of severity-`error` violations, excluding `starved_thermal` and zone-related `clearance`/`hole_clearance` (these come from stale fills). The first 5 go to stderr. Every guard uses this count.
- **`view.py`**: `cd maze && python3 view.py <NET> x0 y0 x1 y1 [x,y ...]`. Reads `./geom.json` and `./maze.py` and writes `v.ppm` with F.Cu and B.Cu side by side. Dark cells are blocked for tracks, light blue cells are blocked for vias only, and red marks the given points.
- **`gnd_fanout.sh`**: `GRID_MARGIN=0 bash gnd_fanout.sh <workdir>`. For every unconnected GND pad or track end in the DRC report, it routes a short stub to the nearest legal via spot (`maze.py ... VIA`) down to In1. It reverts each step that raises `errs.py` above the starting count.
- **`guarded.sh`**: `NOGND=1 bash guarded.sh <workdir>`. Maze-routes every non-GND DRC open, one at a time, and reverts any route that raises `errs.py`. Without `NOGND` it then runs a GND island phase through `island_stitch.py`, which only works on 2 layers.
- **`zone_drop.py`**: `python3 zone_drop.py geom.json pwr_targets.json <NET> zd.json`. For each pad of a power net, it routes the shortest stub to a via spot at least 0.6 mm inside that net's In2 zone. Environment: `ZD_ONLY=REF.PAD,...`, `ZD_MAXD` (default 6 mm) and `ZD_MAXP` (default 200 cells). Apply the output with `kgeom.py apply`. `pwr_targets.json` has the form `{"pads": {NET: [[ref, pad, x, y, "layers"], ...]}, "zones": {NET: [[x, y], ...]}}`. It was written ad hoc and no script here generates it.
- **`ripall.sh`**: `RIPM=2 bash ripall.sh <workdir>`. For each open, it rips a box (endpoints ± `RIPM`; for links longer than 8 mm in x or y, only ± `RIPM`+1 around the start) with `ripup.py`, then reroutes. It keeps the result if the opens dropped and the errors did not rise.
- **`ripup.py`**: `cd maze && python3 ripup.py <board> <NET> <a> <b> <x0,y0,x1,y1> [max_iter=15]`. Rips unprotected nets in the box, routes the target, then greedily routes DRC opens. Endpoint layer specs are `0`/`1`/`01` only, with no In2.
- **`finish4.sh`**: `bash finish4.sh <workdir>`. Runs `project_rules`, then `prep4.py` to make a DSN, then Freerouting (`-mp 25`, then 15, with a 900 s timeout). It imports the SES, widening any via whose annular ring is below 0.1 mm, and refills. It then runs `gnd_fanout.sh`, then `guarded.sh` (`NOGND=1`), then a DRC summary.
- **`island_stitch.py`**: `python3 island_stitch.py geom.json gnd.json isl.json`. Labels GND copper components (vias join layers) and writes `isl.json` (single-via joins as a route JSON), `isl.json.pairs` (maze endpoint pairs for islands that one via cannot join) and `isl.json.useless` (GND vias not touching the main component). It assumes **2 layers**: the current `kgeom.py gndmap` also emits In2 (layer 2) polygons, and the script fails on them (index error).
- **`stitch.py`**: `python3 stitch.py geom.json stitch.json`. Places an RF fence, CSI return vias and a 2 mm GND stitching grid at the nearest legal spots. All target coordinates are 2L.
- **`gnd_fix.sh`**, **`region_reroute.sh`**, **`finish.sh`**: 2-layer island and region loops built on `island_stitch.py`, `ripup.py`, `autoroute_prep.py`, Freerouting and `cleanup.py`. Usage: `bash gnd_fix.sh [rounds]`, `bash region_reroute.sh <x0,y0,x1,y1> <attempts> <workdir>`, and `bash finish.sh <box> <attempts> <workdir>`.
- **`route_all.py`** (**do-not-use**): rips **all** unlocked non-GND copper and reroutes every open in order (power first, then long to short). On this board it made routing worse than the incremental tools.
- **`cleanup.py`** (**do-not-use** here): `$KPY cleanup.py <board> <drc.json>` deletes items DRC flags as `track_dangling` or non-GND `via_dangling`, plus zero-length tracks. On this board the "dangling" warnings are **T-junction bridges** (a track end landing in the middle of another track), so deleting them opened nets.

### Data files

- `pos_v1.json`, `pos_v1_fix.json`: `move.py` inputs for the 2L 60 x 50 board (historical).
- `pos_v06_45x45.json`: an early v0.6 45 x 45 placement snapshot for `move.py` (127 parts; later placement changes are not in it).
- `maze/*.json`, `maze/*.json.*`, `maze/*.ppm`, `maze/out.txt`, `maze/tried.txt`: scratch output (router geometry, routes, DRC reports, island data, `pwr_targets.json`). All of them are git-ignored, so a fresh clone has none of them. Everything except `pwr_targets.json` can be regenerated; that one was written by hand.

---

## Hardcoded absolute paths (parameterise before reuse)

Several scripts point at the author's machine. Replace these paths with arguments or environment variables before using the
scripts anywhere else.

| Hardcoded path | Scripts |
|---|---|
| Board `/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb` | `autoroute_prep.py`, `freespot.py`, `gnd_pour.py`, `legalize.py`, `move.py`, `place.py`, `place45.py`, `power_place.py`, `prep4.py`, `route_csi.py`, `route_csi4.py`, `route_pwr.py`, `route_rf.py`, `route_usb.py`, `maze/prune.py`, `maze/ripthru.py`, `maze/route_all.py`, and every `maze/*.sh` |
| Project file `.../kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pro` | `project_rules.py` |
| `.../kicad/MAIN/scripts/project_rules.py` (called by absolute path) | `maze/ripup.py`, `maze/ripthru.py`, `maze/route_all.py`, and every `maze/*.sh` except `gnd_fix.sh` |
| KiCad app (`/Applications/KiCad/KiCad.app/...` Python and `kicad-cli`) | `maze/ripthru.py`, `maze/ripup.py`, `maze/route_all.py`, and every `maze/*.sh` |
| Footprint libraries (KiCad `SharedSupport/footprints/` and `.../kicad/lib/ESP32-P4-CAM.pretty`) | `place.py`, `place45.py` |
| Freerouting `~/.kicad-mcp/freerouting.jar` | `maze/finish4.sh`, `maze/region_reroute.sh` |

The scripts that take every path as an argument are `pcbmerge.py`, `regioncheck.py`, `kgeom.py`, `maze.py`, `errs.py`,
`cleanup.py`, `island_stitch.py`, `stitch.py`, `zone_drop.py` and `gpio_swap_pcb.py`. `view.py` and `ripup.py` use relative
files in `maze/`. Separately, almost every placement and routing script also hardcodes board geometry: the 45 x 45 outline,
the mounting-hole centres, the J1 slots, corridor boxes, reference designators and net names.

---

## Gotchas

- **pcbnew SWIG: do not `Remove()` while iterating.** Take a snapshot first (`for t in list(b.GetTracks()): ...`). After `b.Remove()`, iterators and `Pads()` lists you obtained earlier can become invalid, so read pad positions **before** removing anything (as `route_pwr.py` and `route_rf.py` do).
- **pcbnew objects are unhashable, and Python identity is unreliable.** Wrappers are recreated on every access (`a is b` is false for the same item). Key sets and dicts by `item.m_Uuid.AsString()`, as `regioncheck.py`, `kgeom.py` and `ripthru.py` do.
- **`pcbnew.SaveBoard()` rewrites the `.kicad_pro` next to the destination file.** If the board was loaded without its project (for example a copy in another directory), the rewritten `.kicad_pro` contains **defaults**: net classes, patterns and rules are lost. Never `SaveBoard` into the master project directory from a board that was loaded elsewhere. After any save, restore the `.kicad_pro` or re-run `project_rules.py`. Before routing or DRC, check that `b.FindNet('VBUS').GetNetClassName() == 'PWR'`.
- **Closing the KiCad GUI can overwrite `.kicad_pro` with stale in-memory rules.** This happened twice. The 4-layer rules reverted to 2-layer values (min track 0.127, min drill 0.3, old net-class widths), and DRC jumped to 733 errors. Do not keep the project open in the GUI while scripts run, close it **without saving**, compare `.kicad_pro` against a known-good copy after any GUI session, and re-run `project_rules.py`.
- **zsh does not word-split an unquoted `$var`.** For example, `set -- $pair` yields one argument. The `.sh` drivers are bash scripts (`#!/bin/bash`, and macOS bash 3.2 has no associative arrays). Run them with `bash`, and do not paste their loops into a zsh prompt.
- **Freerouting cannot be used on the final board.** It sees 102 violations in the existing copper and makes no progress. Everything built on Freerouting (`prep4.py`, `autoroute_prep.py`, `finish4.sh`, `region_reroute.sh`, `finish.sh`) is historical. Even in the early phase, long runs (high `-mp`) wrote empty SES files.
- **The KiCad Python has no numpy, and the system Python has no pcbnew.** Raster work goes in system `python3`, and board I/O goes through `$KPY` (see the table at the top).
- **Zone fills go stale.** `kicad-cli pcb drc` does not refill zones unless you pass `--refill-zones`, and `pcbmerge.py` ignores fills. Run `gnd_pour.py fill` before DRC while you work. `errs.py` deliberately ignores zone clearance errors, so do the final DRC after a refill and read the full report. For fabrication, follow the gate in [`ORDERING.md`](../fab/ORDERING.md): refill and save with `kicad-cli pcb drc --refill-zones --save-board` **inside `kicad/MAIN`**, next to the `.kicad_pro` and `.kicad_dru`. A refill outside the project folder loses the `.kicad_dru` rules (for example the 1 mm edge clearance of the power zones) and gives different copper.
- **DRC output is localised.** `kicad-cli` writes descriptions in the UI language (Hungarian on the author's machine). `errs.py`, `cleanup.py` and `gnd_fanout.sh` match both Hungarian and English words (`zóna`/`zone`, `Forrszem`/`Pad`, `Vezetősáv`/`Track`, `hossza`/`length`). Other parsers rely on `[NET]`, `F.Cu`, `In2`, `PTH` and `Via` substrings. Check these parsers if you use another locale.
- **Keep the router's clearances in sync.** The `CLR` table in `kgeom.py` must match `project_rules.py`. Use the same `TRACK_W` for `export` and `apply`. SOFT-mode routes are never safe to apply directly.
- **Scripts that can delete good copper:** `cleanup.py` (T-junction bridges), `prune.py` (verify with DRC), `route_all.py` (rips everything), `place45.py` (wipes the board), `route_pwr.py` (deletes almost all GND copper), `ripup.py` (box rip), and the corridor rip in `route_csi4.py`.
- **Back up first.** Most scripts save the master board in place. Only `ripthru.py`, `guarded.sh`, `gnd_fanout.sh`, `ripall.sh` and `region_reroute.sh` keep their own per-step backup in the work directory and revert on their own.
