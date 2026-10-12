# Move existing footprints to positions (x,y,rot,side). Side flips if needed.
import sys, json, pcbnew
BOARD='/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
P=json.load(open(sys.argv[1]))
b=pcbnew.LoadBoard(BOARD); mm=pcbnew.FromMM
fps={f.GetReference():f for f in b.GetFootprints()}
for ref,(x,y,rot,side) in P.items():
    f=fps[ref]; pos=pcbnew.VECTOR2I(mm(x),mm(y))
    want_b=(side=='B')
    if f.IsFlipped()!=want_b: f.Flip(f.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    f.SetPosition(pos); f.SetOrientationDegrees(rot)
pcbnew.SaveBoard(BOARD,b); print('moved',len(P))
