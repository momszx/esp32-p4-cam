# MAIN v0.6: power block re-placement along the power flow (anchors), then legalize only these parts.
# eFuse top-right, CH224A below J1, buck as one block under the module (centre), VBUS monitor + NTC next to it.
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
mm = pcbnew.FromMM
A = {  # ref: (x, y, rot)  all F.Cu
 # eFuse block (top right, above the J1 shell slots, right of MH2)
 'U3': (40.8, 13.4, 0), 'C3': (43.4, 11.4, 90), 'C4': (43.4, 15.6, 90), 'R10': (38.4, 15.9, 90),
 'R6': (36.0, 11.4, 0), 'R7': (36.0, 13.0, 0), 'R8': (36.0, 14.6, 0), 'R9': (36.0, 16.2, 0),
 # CH224A (below the J1 shell slots)
 'U2': (40.6, 31.2, 0), 'C2': (36.9, 34.8, 0), 'R2': (40.6, 34.8, 0), 'R3': (43.6, 34.6, 90),
 # buck block (centre, under the module, below the CSI corridor)
 'C5': (26.0, 21.0, 90), 'C6': (29.6, 21.0, 90), 'C8': (32.8, 24.2, 90), 'C9': (32.8, 27.6, 90),
 'U4': (29.6, 26.6, 0), 'C11': (29.6, 24.2, 0), 'C10': (26.4, 27.0, 0), 'R14': (26.4, 25.4, 0), 'R15': (26.4, 28.6, 0),
 'L1': (29.6, 31.8, 0), 'C12': (33.2, 31.4, 90), 'C13': (33.2, 34.8, 90), 'R16': (25.8, 32.6, 90),
 # VBUS_SW monitor divider + NTC next to the buck
 'R12': (23.8, 31.0, 90), 'R13': (23.8, 34.4, 90), 'C7': (22.2, 34.4, 90), 'D2': (26.2, 35.0, 0),
 'R33': (22.0, 30.2, 90), 'TH1': (22.0, 26.6, 90), 'C26': (22.0, 23.0, 90),
 'R11': (34.2, 24.6, 90),
}
b = pcbnew.LoadBoard(BOARD)
for f in list(b.GetFootprints()):
    r = f.GetReference()
    if r in A:
        x, y, rot = A[r]
        if f.IsFlipped(): f.Flip(f.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
        f.SetOrientationDegrees(rot); f.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
pcbnew.SaveBoard(BOARD, b)
print(','.join(A))
