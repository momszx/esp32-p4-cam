# MAIN v0.6: 4-layer 45x45 board from the existing (netlisted) board: strip copper, new outline, swap SW/J7
# footprints, place per docs/06 45x45 floorplan. Board coords: top view, origin top-left. side B = module side.
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
STD = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/'
OWN = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/lib/ESP32-P4-CAM.pretty'
W = H = 45.0
mm = pcbnew.FromMM
B, F = 'B', 'F'
P = {
 # ---------------- B (module side) ----------------
 'U1': (20.5, 25.0, 0, B),
 'J1': (40.8, 22.5, -90, B), 'D1': (40.5, 13.5, 0, B), 'R1': (43.2, 2.6, 90, B), 'C1': (43.2, 6.2, 90, B),
 'J7': (22.5, 2.0, 0, B), 'SW1': (11.5, 3.0, 0, B), 'SW2': (33.5, 3.0, 0, B), 'SW3': (33.5, 7.4, 0, B), 'C40': (29.4, 7.6, 0, B),
 'R21': (3.2, 27.4, 0, B), 'R22': (3.2, 25.8, 0, B), 'D20': (3.2, 14.4, 0, B), 'R30': (3.2, 16.0, 0, B),
 'R23': (3.2, 29.6, 0, B), 'C25': (3.2, 31.2, 0, B),
 'C27': (5.4, 34.5, 90, B), 'R34': (3.9, 34.5, 180, B), 'C28': (2.4, 34.5, 90, B), 'J4': (3.0, 38.3, -90, B),
 'C20': (12.0, 42.4, 0, B), 'C21': (16.4, 42.4, 0, B), 'C22': (19.8, 41.3, 0, B), 'C23': (19.8, 43.4, 0, B),
 'C24': (31.5, 41.3, 0, B), 'R20': (31.5, 43.4, 0, B), 'R40': (27.0, 41.3, 0, B), 'R41': (27.0, 43.4, 0, B),
 # ---------------- F (camera side) ----------------
 'J2': (22.5, 7.5, 180, F), 'J3': (9.0, 25.0, -90, F), 'J5': (22.5, 40.2, 90, F),
 # camera power (left of J2, above J3)
 'U6': (3.6, 13.6, 0, F), 'C50': (3.0, 10.6, 0, F), 'R28': (3.0, 16.4, 0, F), 'R50': (8.2, 12.4, 0, F),
 'C51': (8.2, 14.0, 0, F), 'R53': (8.2, 15.6, 0, F), 'C52': (12.6, 12.4, 0, F), 'R51': (12.6, 14.0, 0, F), 'R52': (12.6, 15.6, 0, F),
 'R70': (16.4, 12.6, 0, F), 'R31': (16.4, 14.2, 0, F), 'R32': (16.4, 15.8, 0, F),
 # SD (right of J3, under module): pull-ups next to J3 pins, switch below
 'R62': (19.4, 20.07, 0, F), 'R65': (19.4, 25.57, 0, F), 'R63': (19.4, 27.77, 0, F),
 'R61': (22.4, 21.18, 0, F), 'C63': (22.4, 24.0, 0, F), 'R64': (22.4, 26.68, 0, F),
 'U8': (11.0, 35.4, 0, F), 'C61': (7.0, 35.0, 90, F), 'C60': (14.6, 34.6, 0, F), 'R60': (14.6, 36.2, 0, F),
 'C62': (11.0, 38.3, 0, F), 'R27': (7.0, 38.6, 90, F), 'R66': (19.4, 30.0, 0, F),
 # e-fuse block (top right, between MH2 and J1 shell slots)
 'U3': (40.5, 13.6, 0, F), 'C3': (43.4, 11.8, 90, F), 'C4': (43.6, 15.2, 90, F), 'R10': (35.7, 11.6, 0, F),
 'R6': (35.7, 13.2, 0, F), 'R7': (35.7, 14.8, 0, F), 'R8': (35.7, 16.4, 0, F), 'R9': (31.5, 16.4, 0, F),
 'R11': (31.5, 14.8, 0, F), 'JP1': (31.6, 12.0, 0, F),
 # USB ESD on F, opposite the J1 data pads
 'U5': (34.0, 21.2, 90, F),
 # PD controller (right, below J1 shell slots)
 'U2': (40.5, 31.4, 0, F), 'C2': (36.2, 35.6, 0, F), 'R2': (40.0, 35.6, 0, F), 'R3': (43.6, 35.6, 90, F),
 # buck + bulk (centre-right, under module)
 'C5': (30.0, 21.0, 90, F), 'C6': (30.0, 26.0, 90, F), 'R12': (26.6, 19.0, 90, F), 'R13': (26.6, 22.6, 90, F), 'C7': (25.0, 22.6, 90, F),
 'D2': (26.4, 16.6, 0, F), 'U4': (31.0, 30.6, 0, F), 'C8': (27.6, 30.6, 90, F), 'C9': (27.6, 33.8, 90, F), 'C11': (34.4, 29.2, 0, F),
 'C10': (34.4, 32.8, 0, F), 'R14': (34.4, 34.4, 0, F), 'R15': (34.4, 36.0, 0, F),
 'L1': (31.0, 35.4, 0, F), 'C12': (26.4, 27.4, 90, F), 'C13': (24.4, 27.4, 90, F), 'R16': (25.4, 31.4, 90, F),
 'R33': (25.0, 34.6, 90, F), 'TH1': (23.4, 34.6, 90, F), 'C26': (21.8, 34.6, 90, F),
 # strap / pull-downs under module
 'R24': (25.0, 13.0, 0, F), 'R25': (28.8, 13.0, 0, F), 'R26': (25.0, 14.6, 0, F), 'R29': (28.8, 14.6, 0, F),
 # PD CC taps / external Rd (all DNP): bottom-left
 'R4': (3.0, 44.0 - 1.5, 0, F), 'R5': (12.6, 41.0, 0, F), 'R35': (12.6, 42.6, 0, F), 'R36': (12.6, 44.0, 0, F),
 'C29': (9.0, 41.0, 0, F), 'C30': (9.0, 42.6, 0, F), 'D21': (1.8, 20.0, 90, B), 'D22': (4.6, 20.0, 90, B),
 # IR block (DNP): bottom right of J5
 'U7': (34.0, 40.0, 0, F), 'C70': (31.4, 42.6, 0, F), 'R71': (34.0, 43.2, 0, F), 'C71': (36.6, 43.2, 0, F),
 'R72': (42.6, 39.6, 90, F), 'R73': (42.6, 43.0, 90, F), 'TP8A': (36.8, 38.8, 0, F), 'TP8B': (31.0, 38.8, 0, F),
}
TPS = ['TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'TP6', 'TP7', 'TP16A', 'TP16B', 'TP17', 'TP18', 'TP19']
for i, t in enumerate(TPS):
    P[t] = (37.6 + 2.75 * (i % 3), 29.5 + 2.75 * (i // 3), 0, B)
SWAP = {'SW1': (STD + 'Button_Switch_SMD.pretty', 'Button_Switch_SMD', 'SW_SPST_B3U-1000P'),
        'SW2': (STD + 'Button_Switch_SMD.pretty', 'Button_Switch_SMD', 'SW_SPST_B3U-1000P'),
        'SW3': (STD + 'Button_Switch_SMD.pretty', 'Button_Switch_SMD', 'SW_SPST_B3U-1000P'),
        'J7': (OWN, 'ESP32-P4-CAM', 'PadRow_1x09_P1.27mm_SMD')}

b = pcbnew.LoadBoard(BOARD)
tracks, zones, drawings, fps = list(b.GetTracks()), list(b.Zones()), list(b.GetDrawings()), list(b.GetFootprints())
for t in tracks: b.Remove(t)
for z in zones: b.Remove(z)          # pours and keepouts are re-created for the new geometry
for d in drawings:
    if d.GetLayer() == pcbnew.Edge_Cuts: b.Remove(d)
b.SetCopperLayerCount(4)
ds = b.GetDesignSettings(); ds.SetBoardThickness(mm(0.97))
# outline: 45x45, R1 corners
r = 1.0
def seg(x1, y1, x2, y2):
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1))
    s.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1))); s.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2))); b.Add(s)
def arc(cx, cy, sx, sy, ang):
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_ARC); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1))
    s.SetCenter(pcbnew.VECTOR2I(mm(cx), mm(cy))); s.SetStart(pcbnew.VECTOR2I(mm(sx), mm(sy))); s.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(ang, pcbnew.DEGREES_T)); b.Add(s)
seg(r, 0, W - r, 0); seg(W, r, W, H - r); seg(W - r, H, r, H); seg(0, H - r, 0, r)
arc(W - r, r, W - r, 0, 90); arc(W - r, H - r, W, H - r, 90); arc(r, H - r, r, H, 90); arc(r, r, 0, r, 90)

new_fps = []
for f in fps:
    ref = f.GetReference()
    if ref in SWAP:
        path, lib, name = SWAP[ref]
        n = pcbnew.FootprintLoad(path, name); n.SetFPID(pcbnew.LIB_ID(lib, name))
        n.SetReference(ref); n.SetValue(f.GetValue()); n.SetDNP(f.IsDNP())
        nets = {p.GetNumber(): p.GetNet() for p in f.Pads()}
        for p in n.Pads():
            if p.GetNumber() in nets: p.SetNet(nets[p.GetNumber()])
        b.Remove(f); b.Add(n); new_fps.append(n)
missing = []
for f in [f for f in fps if f.GetReference() not in SWAP] + new_fps:
    ref = f.GetReference()
    if ref.startswith('MH'): continue
    if ref not in P: missing.append(ref); continue
    x, y, rot, side = P[ref]
    if f.IsFlipped() != (side == B): f.Flip(f.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    f.SetOrientationDegrees(rot); f.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
pcbnew.SaveBoard(BOARD, b)
print('placed; missing positions:', missing)
