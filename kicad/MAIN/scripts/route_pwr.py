# Power trunks: VBUS (J1 -> TVS -> eFuse U3 / CH224A U2 / JP1), VBUS_SW (U3 -> C5/C6 -> buck U4, IR eFuse U7, R73),
# BK_SW, 3V3_BUCK (L1 -> C12/C13 -> R16), +3V3 (R16 -> B trunk -> C20/C21 -> module P84-86, C22/C23),
# IR_VIN (U7 shunt -> C71 -> J5 pins 1/2, between J5 columns), GND vias at power caps.
# Small control nets (FB/SS/BST, eFuse UVLO/OVLO/ILM/DVDT, CC, PG, I2C) are left for the general routing step.
# Idempotent: deletes copper of the trunk nets + all GND copper except the USB ESD stub/via, then redraws.
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
NETS = ('VBUS', 'VBUS_SW', '3V3_BUCK', 'BK_SW', '+3V3', 'IR_VIN', 'IR_VIN_SH')
b = pcbnew.LoadBoard(BOARD); mm = pcbnew.FromMM; T = pcbnew.ToMM
fp = {f.GetReference(): f for f in b.GetFootprints()}
F, B = pcbnew.F_Cu, pcbnew.B_Cu

# --- placement nudges (front side) ---
for ref, x, y, rot in (('R16', 44.0, 42.5, 270), ('R11', 49.0, 22.0, 180), ('R3', 56.5, 3.2, 0), ('C2', 56.5, 6.4, 0)):
    fp[ref].SetOrientationDegrees(rot); fp[ref].SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
def pad(ref, n):
    p = [q for q in fp[ref].Pads() if q.GetNumber() == n][0].GetPosition()
    return (round(T(p.x), 3), round(T(p.y), 3))
assert pad('R16', '1')[1] < pad('R16', '2')[1], 'R16: 3V3_BUCK pad must be on top'
assert pad('R11', '1')[0] > pad('R11', '2')[0], 'R11: FLT pad must be on the right'
r16, r11 = pad('R16', '2'), pad('R11', '2')  # read before track removal (swig Pads() breaks afterwards)
placed = {k: pad(*k) for k in (('R16', '1'), ('R16', '2'), ('R11', '1'), ('R11', '2'), ('R3', '1'), ('C2', '1'))}

def in_esd_box(t):  # keep USB ESD GND stub/via from route_usb.py
    pts = [t.GetPosition()] if t.GetClass() == 'PCB_VIA' else [t.GetStart(), t.GetEnd()]
    return all(46.0 <= T(q.x) <= 48.6 and 19.7 <= T(q.y) <= 20.3 for q in pts)
for t in list(b.GetTracks()):
    n = t.GetNetname()
    if n in NETS or (n == 'GND' and not in_esd_box(t)): b.Remove(t)

def track(pts, n, layer=F, w=0.6):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1))); t.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
        t.SetWidth(mm(w)); t.SetLayer(layer); t.SetNet(b.FindNet(n)); b.Add(t)
def via(x, y, n, d=0.8, drill=0.4):
    v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y))); v.SetWidth(mm(d)); v.SetDrill(mm(drill))
    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetNet(b.FindNet(n)); b.Add(v)

# --- VBUS ---
track([(51.45, 17.55), (50.3, 17.55)], 'VBUS', B, 0.6)                       # J1 A4/B9 (narrow between A1/B8)
track([(50.3, 17.55), (46.6, 17.55)], 'VBUS', B, 0.8)
track([(47.5, 15.6), (47.5, 17.55)], 'VBUS', B, 0.8)                          # D1 TVS
via(46.6, 17.2, 'VBUS'); via(46.6, 18.2, 'VBUS')
track([(51.45, 22.45), (49.7, 22.45), (49.3, 23.0)], 'VBUS', B, 0.6)         # J1 A9/B4 -> via south of USB
via(49.3, 23.4, 'VBUS')
track([(49.3, 23.4), (46.2, 23.4), (45.6, 22.8), (45.6, 18.2), (46.6, 18.2)], 'VBUS', F, 0.6)
track([(46.6, 18.2), (46.6, 14.35), (54.5, 14.35), (54.5, 16.6), (55.35, 17.3)], 'VBUS', F, 0.8)  # -> C3
track([(55.75, 18.3), (56.05, 18.65), (56.05, 19.05)], 'VBUS', F, 0.28)     # C3 -> U3.5 top end (0.2 slot)
track([(46.6, 15.6), (48.17, 15.6)], 'VBUS', F, 0.3)                         # R6 (UVLO top)
track([(46.6, 18.2), (48.17, 18.8)], 'VBUS', F, 0.3)                         # R8 (OVLO top)
track([(55.0, 14.35), (56.0, 13.35), (56.5, 13.0)], 'VBUS', F, 0.5)          # JP1.1
track([(56.6, 12.0), (56.6, 8.0), (56.0, 6.9)], 'VBUS', F, 0.3)              # JP1.1 -> C2 (VHV cap)
track([(55.73, 6.4), (55.28, 6.3), (54.3, 5.6), (54.0, 5.4)], 'VBUS', F, 0.3)
via(54.0, 5.4, 'VBUS', 0.6, 0.3)
track([(54.0, 5.4), (52.64, 5.0)], 'VBUS', F, 0.3)                           # U2.8 VBUS sense
track([(54.0, 5.4), (54.0, 4.6), (50.8, 4.6), (50.8, 1.6), (46.0, 1.6), (46.0, 2.5)], 'VBUS', B, 0.3)  # SW1/SW2 gap
via(46.0, 2.5, 'VBUS', 0.6, 0.3)
track([(46.0, 2.5), (46.6, 3.0), (47.36, 3.0)], 'VBUS', F, 0.3)              # U2.1 VHV

# --- VBUS_SW ---
track([(56.55, 20.2), (56.55, 21.75)], 'VBUS_SW', F, 0.28)                   # U3.6 bottom end
track([(56.55, 21.75), (56.55, 21.9)], 'VBUS_SW', F, 0.4)
track([(56.55, 21.9), (55.0, 23.45), (55.0, 25.4), (54.02, 26.4), (54.02, 27.3)], 'VBUS_SW', F, 0.8)
track([(54.02, 27.3), (47.0, 27.3)], 'VBUS_SW', F, 0.8)                     # C6 -> R12 -> C5
track([(50.0, 26.32), (50.0, 27.3)], 'VBUS_SW', F, 0.4)
track([(46.4, 27.48), (45.9, 27.48), (45.2, 28.2), (45.2, 37.5), (44.6, 38.2)], 'VBUS_SW', F, 0.5)
track([(45.2, 33.45), (47.0, 33.45)], 'VBUS_SW', F, 0.5)                     # C8
track([(45.2, 37.08), (46.2, 37.08)], 'VBUS_SW', F, 0.5)                     # C9
track([(47.0, 33.45), (47.725, 33.45), (48.0, 33.75), (49.0, 33.75)], 'VBUS_SW', F, 0.5)
track([(49.0, 33.75), (50.26, 33.75)], 'VBUS_SW', F, 0.3)                    # U4.3 VIN
track([(58.15, 12.5), (58.8, 13.2), (58.8, 13.9)], 'VBUS_SW', F, 0.5)       # JP1.2 bypass side
via(58.8, 13.9, 'VBUS_SW')
track([(58.8, 13.9), (58.8, 25.0), (58.6, 25.2)], 'VBUS_SW', B, 0.6)
via(58.6, 25.2, 'VBUS_SW')
track([(58.6, 25.2), (57.9, 25.4), (55.0, 25.4)], 'VBUS_SW', F, 0.6)
via(44.6, 38.2, 'VBUS_SW')                                                    # IR eFuse feed on B, north of MH4
track([(44.6, 38.2), (44.6, 39.55), (36.8, 39.55), (34.4, 41.95), (24.75, 41.95)], 'VBUS_SW', B, 0.6)
via(24.75, 41.95, 'VBUS_SW')
track([(24.75, 41.95), (24.75, 43.3)], 'VBUS_SW', F, 0.5)
track([(24.75, 43.3), (24.75, 43.85)], 'VBUS_SW', F, 0.28)                  # U7.5 top end
track([(24.75, 41.95), (30.13, 41.95), (30.13, 46.0), (28.4, 47.3)], 'VBUS_SW', F, 0.4)  # R73.1 (DNP bypass)

# --- buck: BK_SW, 3V3_BUCK ---
track([(51.74, 34.25), (52.075, 34.25), (52.4, 34.55)], 'BK_SW', F, 0.3)
track([(52.4, 34.55), (51.0, 35.95), (49.6, 36.9), (49.2, 37.6)], 'BK_SW', F, 0.6)
track([(52.8, 40.6), (52.8, 41.0), (52.0, 41.8), (47.75, 41.8), (46.9, 41.6)], '3V3_BUCK', F, 0.8)
track([(46.4, 41.45), (44.0, 41.59)], '3V3_BUCK', F, 0.8)                   # C12 -> R16.1
track([(47.75, 41.8), (47.75, 45.95), (46.9, 45.95)], '3V3_BUCK', F, 0.6)   # C13
track([(52.8, 37.4), (52.8, 37.0), (53.85, 36.0), (53.85, 33.6), (54.27, 33.25)], '3V3_BUCK', F, 0.25)  # FB sense -> R14

# --- +3V3 ---
track([r16, (42.6, r16[1] + 0.2), (42.6, 44.6)], '+3V3', F, 0.8)
via(42.6, 43.6, '+3V3'); via(42.6, 44.6, '+3V3')
track([(42.6, 43.6), (42.6, 44.06), (21.5, 44.06)], '+3V3', B, 0.8)
track([(21.5, 44.06), (14.8, 44.06)], '+3V3', B, 0.6)
track([(14.8, 44.06), (14.05, 44.8)], '+3V3', B, 0.6)                       # C21
track([(14.8, 44.06), (13.8, 43.2)], '+3V3', B, 0.6)                        # C20
track([(14.0, 38.9), (16.0, 38.9)], '+3V3', B, 0.4)                         # P84-86 tie
track([(14.0, 38.9), (13.6, 40.7)], '+3V3', B, 0.6)
track([(16.0, 38.9), (16.2, 39.6), (18.4, 39.6), (18.73, 40.525)], '+3V3', B, 0.4)  # C22
track([(18.73, 41.0), (18.73, 42.6)], '+3V3', B, 0.4)                       # C23
via(47.0, 22.4, '+3V3', 0.6, 0.3)                                            # R11 pull-up feed (B network later)
track([(47.0, 22.4), r11], '+3V3', F, 0.3)

# --- IR_VIN / IR_VIN_SH (IR block DNP in rev A, routed for later fit) ---
track([(31.05, 44.3), (31.05, 42.0), (40.5, 32.5), (40.5, 19.29)], 'IR_VIN', F, 0.6)
track([(39.75, 19.29), (41.25, 19.29)], 'IR_VIN', F, 0.6)                    # J5.1 / J5.2 inner ends
track([(31.3, 45.9), (32.6, 47.5)], 'IR_VIN', F, 0.5)                       # C71 -> TP8B
track([(32.6, 48.6), (32.3, 49.2), (26.3, 49.2), (25.91, 48.6)], 'IR_VIN', F, 0.5)  # TP8B -> R72.2 along edge
track([(25.25, 45.9), (25.25, 46.6), (24.4, 47.4)], 'IR_VIN_SH', F, 0.28)  # U7.6 -> R72.1
track([(23.58, 48.0), (21.0, 48.0)], 'IR_VIN_SH', F, 0.5)                   # TP8A
via(23.4, 46.6, 'IR_VIN_SH', 0.6, 0.3); via(31.0, 47.2, 'IR_VIN_SH', 0.6, 0.3)
track([(23.4, 46.6), (23.9, 47.3)], 'IR_VIN_SH', F, 0.3)
track([(23.4, 46.6), (23.9, 47.2), (31.0, 47.2)], 'IR_VIN_SH', B, 0.4)      # R73.2 hop under IR_VIN
track([(31.0, 47.2), (30.42, 47.6)], 'IR_VIN_SH', F, 0.3)

# --- GND vias at power parts (pours tie the rest) ---
for (x, y), stub in (((47.8, 30.9), [(47.0, 31.55), (47.8, 30.9)]),            # C8.2
                     ((47.8, 34.9), [(46.2, 35.52), (47.5, 35.1), (47.8, 34.9)]),  # C9.2
                     ((47.8, 38.7), [(46.4, 39.55), (47.8, 38.7)]),            # C12.2
                     ((46.9, 42.9), [(46.4, 43.55), (46.9, 42.9)]),            # C13.2
                     ((46.2, 25.5), None), ((47.8, 25.5), None),               # C5.2
                     ((57.0, 29.65), [(56.98, 28.6), (57.0, 29.65)]),          # C6.2
                     ((57.9, 16.6), [(57.25, 17.7), (57.9, 16.6), (59.0, 18.57)]),  # C3.2, R10.2
                     ((57.4, 35.6), [(56.33, 34.8), (57.4, 35.6), (56.27, 36.4)]),  # R15.2, C10.2
                     ((49.6, 4.4), None), ((49.6, 5.5), None)):                # U2 EP
    via(x, y, 'GND', 0.6, 0.3)
    if stub: track(stub, 'GND', F, 0.4)
track([(50.26, 32.75), (49.3, 32.75), (48.1, 31.8), (47.5, 31.55)], 'GND', F, 0.3)   # U4.1 -> C8.2
track([(50.26, 34.25), (49.6, 34.25), (49.0, 34.9), (47.8, 34.9)], 'GND', F, 0.3)    # U4.4 -> via

pcbnew.SaveBoard(BOARD, b)
print(placed)
