# 4-layer Freerouting prep: lock copper, mounting-hole keepouts, export DSN keeping GND (In1 GND zone = plane, so
# Freerouting fans GND pads out to the plane). F/B/In2 pours are left out of the export (refilled afterwards).
import math, sys
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
out = sys.argv[1]
b = pcbnew.LoadBoard(BOARD); mm = pcbnew.FromMM
tracks, zones, fps = list(b.GetTracks()), list(b.Zones()), list(b.GetFootprints())
import os
if not os.environ.get('FR_RESPECT_LOCKS'):  # default: freeze all copper; set -> unlocked wires stay rip-up-able for Freerouting
    for t in tracks: t.SetLocked(True)
names = [z.GetZoneName() for z in zones]
for ref, c in [(f.GetReference(), f.GetPosition()) for f in fps if f.GetReference().startswith('MH')]:
    name = f'MH_KEEPOUT_{ref}'
    if name in names: continue
    z = pcbnew.ZONE(b); z.SetIsRuleArea(True); z.SetZoneName(name)
    ls = pcbnew.LSET.AllCuMask(); z.SetLayerSet(ls)
    z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True); z.SetDoNotAllowPads(False)
    z.SetDoNotAllowZoneFills(False); z.SetDoNotAllowFootprints(False)
    ol = z.Outline(); ol.NewOutline()
    for k in range(16):
        a = 2 * math.pi * k / 16
        ol.Append(c.x + mm(1.75 * math.cos(a)), c.y + mm(1.75 * math.sin(a)))
    b.Add(z)
pcbnew.SaveBoard(BOARD, b)
for z in zones:   # export: keep only the In1 GND plane and rule areas
    if not z.GetIsRuleArea() and z.GetZoneName() != 'GND_In1': b.Remove(z)
assert pcbnew.ExportSpecctraDSN(b, out), 'DSN export failed'
s = open(out).read()
print('planes:', s.count('(plane '), ' layers:', [l for l in ('F.Cu', 'In1.Cu', 'In2.Cu', 'B.Cu') if f'(layer {l}' in s or f'(layer "{l}"' in s])
