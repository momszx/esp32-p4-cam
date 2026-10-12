# Prepare Freerouting run: lock all existing copper (exported as protected wiring), add an F.Cu keepout
# under the B.Cu RF line (CPWG reference), export DSN and drop GND from the netlist (GND = pours + stitching).
# Usage: python3 autoroute_prep.py <out.dsn>
import re, sys
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
RF_KEEPOUT = (1.0, 33.2, 8.9, 37.6)  # x0, y0, x1, y1 (mm), F.Cu only; RF line is B.Cu x 3.0-9.62, y 34.5-36.3
out = sys.argv[1]
b = pcbnew.LoadBoard(BOARD); mm = pcbnew.FromMM

for t in b.GetTracks():
    t.SetLocked(True)

if not any(z.GetIsRuleArea() and z.GetZoneName() == 'RF_F_KEEPOUT' for z in b.Zones()):
    z = pcbnew.ZONE(b); z.SetIsRuleArea(True); z.SetZoneName('RF_F_KEEPOUT'); z.SetLayer(pcbnew.F_Cu)
    z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(False); z.SetDoNotAllowPads(False)  # vias allowed: GND fence
    z.SetDoNotAllowZoneFills(False); z.SetDoNotAllowFootprints(False)
    x0, y0, x1, y1 = RF_KEEPOUT
    ol = z.Outline(); ol.NewOutline()
    for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        ol.Append(mm(x), mm(y))
    b.Add(z)

REMOVED_TPS = ('TP9A', 'TP9B', 'TP10', 'TP11', 'TP12', 'TP13', 'TP14', 'TP15')  # TP grid thinned 2026-10-09 (J7 duplicates, USB)
fps = list(b.GetFootprints())  # snapshot: swig iteration breaks after Remove()
mh = [(f.GetReference(), f.GetPosition()) for f in fps if f.GetReference().startswith('MH')]
zones = list(b.Zones())
for z in zones:  # recreate MH keepouts each run so radius changes apply
    if z.GetZoneName().startswith('MH_KEEPOUT_'): b.Remove(z)
zone_names = [z.GetZoneName() for z in zones if not z.GetZoneName().startswith('MH_KEEPOUT_')]
for f in fps:
    if f.GetReference() in REMOVED_TPS: b.Remove(f)

MH_KEEPOUT_R = 1.75  # mm (2.0 hit the MH4 power trunks); NPTH mask opening is wider than the DSN hole keepout -> solder_mask_bridge otherwise
for ref, c in mh:
    name = f'MH_KEEPOUT_{ref}'
    if name in zone_names: continue
    z = pcbnew.ZONE(b); z.SetIsRuleArea(True); z.SetZoneName(name)
    ls = pcbnew.LSET(); ls.AddLayer(pcbnew.F_Cu); ls.AddLayer(pcbnew.B_Cu); z.SetLayerSet(ls)
    z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True); z.SetDoNotAllowPads(False)
    z.SetDoNotAllowZoneFills(False); z.SetDoNotAllowFootprints(False)
    ol = z.Outline(); ol.NewOutline()
    import math
    for k in range(16):
        a = 2 * math.pi * k / 16
        ol.Append(c.x + mm(MH_KEEPOUT_R * math.cos(a)), c.y + mm(MH_KEEPOUT_R * math.sin(a)))
    b.Add(z)

pcbnew.SaveBoard(BOARD, b)
for z in list(b.Zones()):  # pours are refilled afterwards; keep them out of the DSN (GND net is dropped anyway)
    if not z.GetIsRuleArea(): b.Remove(z)
assert pcbnew.ExportSpecctraDSN(b, out), 'DSN export failed'

dsn = open(out).read()
dsn, n = re.subn(r'\(net GND\s*\(pins[^)]*\)\s*\)', '', dsn)
assert n == 1, f'GND net block not found exactly once ({n})'
open(out, 'w').write(dsn)
print('DSN ok, GND dropped, protected wires:', dsn.count('(type protect)'))
