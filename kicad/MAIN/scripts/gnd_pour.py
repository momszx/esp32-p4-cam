# GND pours on F.Cu + B.Cu over the whole board (re-created each run), thermal pads / solid vias, islands removed.
# Usage: gnd_pour.py [fill-only]
import sys
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
mm = pcbnew.FromMM
b = pcbnew.LoadBoard(BOARD)
gnd = b.FindNet('GND')
if len(sys.argv) < 2:
    OWN = ('GND_F', 'GND_B', 'GND_In2')   # never touch GND_In1 (the 4-layer reference plane)
    zones = list(b.Zones())
    for z in zones:
        if not z.GetIsRuleArea() and z.GetZoneName() in OWN: b.Remove(z)
    bb = b.GetBoardEdgesBoundingBox()
    for layer, name in ((pcbnew.F_Cu, 'GND_F'), (pcbnew.B_Cu, 'GND_B'), (pcbnew.In2_Cu, 'GND_In2')):
        z = pcbnew.ZONE(b); z.SetLayer(layer); z.SetNet(gnd); z.SetZoneName(name)
        z.SetAssignedPriority(0)   # In2 power zones (VBUS, VBUS_SW) are priority 2 and win
        z.SetLocalClearance(mm(0.2)); z.SetMinThickness(mm(0.2))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(mm(0.3)); z.SetThermalReliefSpokeWidth(mm(0.35))
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        ol = z.Outline(); ol.NewOutline()
        for x, y in ((bb.GetLeft(), bb.GetTop()), (bb.GetRight(), bb.GetTop()), (bb.GetRight(), bb.GetBottom()), (bb.GetLeft(), bb.GetBottom())):
            ol.Append(x, y)
        b.Add(z)
filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())
pcbnew.SaveBoard(BOARD, b)
for z in b.Zones():
    if z.GetNetname() == 'GND':
        fp = z.GetFilledPolysList(z.GetLayer())
        print(z.GetZoneName(), 'filled outlines', fp.OutlineCount(), 'area mm2', round(pcbnew.ToMM(pcbnew.ToMM(fp.Area())), 1))
