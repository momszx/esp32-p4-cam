# MAIN v0.6 (4-layer) MIPI-CSI: module P41-P46 (B.Cu) -> one via each, under the module body -> F.Cu (ref. In1 GND)
# -> J2 pins from below. Nesting: D0 inner (straight up), D1 middle, CLK outer. Intra-pair skew matched with a
# serpentine on the shorter leg. Rips other copper in the CSI corridor first. Idempotent.
import math
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
W = 0.204
CORR_F = (20.8, 9.0, 34.2, 18.4)          # F.Cu corridor (all other nets ripped)
CORR_B = (27.0, 12.9, 33.0, 18.0)         # B.Cu / In2.Cu under the module body
b = pcbnew.LoadBoard(BOARD); mm = pcbnew.FromMM; T = pcbnew.ToMM
F, Bl, I2 = pcbnew.F_Cu, pcbnew.B_Cu, pcbnew.In2_Cu
def inbox(p, box): return box[0] <= T(p.x) <= box[2] and box[1] <= T(p.y) <= box[3]
rm = []
for t in list(b.GetTracks()):
    n = t.GetNetname()
    if n.startswith('CSI_'): rm.append(t); continue
    pts = [t.GetPosition()] if t.GetClass() == 'PCB_VIA' else [t.GetStart(), t.GetEnd()]
    if t.GetClass() == 'PCB_VIA':
        if any(inbox(p, CORR_F) for p in pts) or any(inbox(p, CORR_B) for p in pts): rm.append(t)
    elif t.GetLayer() == F and any(inbox(p, CORR_F) for p in pts): rm.append(t)
    elif t.GetLayer() in (Bl, I2) and any(inbox(p, CORR_B) for p in pts): rm.append(t)
for t in rm: b.Remove(t)

def track(pts, net, layer):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if (x1, y1) == (x2, y2): continue
        t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1))); t.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
        t.SetWidth(mm(W)); t.SetLayer(layer); t.SetNet(b.FindNet(net)); t.SetLocked(True); b.Add(t)
def via(x, y, net):
    v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y))); v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3))
    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetNet(b.FindNet(net)); v.SetLocked(True); b.Add(v)
def length(pts): return sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))
def serpentine(pts, seg_i, extra, amp_dir, pitch=0.5):
    """Insert a trombone serpentine into straight segment seg_i of pts adding ~extra length; amp_dir = unit normal."""
    (x1, y1), (x2, y2) = pts[seg_i], pts[seg_i + 1]
    L = math.dist((x1, y1), (x2, y2)); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    n = max(1, int((L - 0.6) / (2 * pitch)))              # number of bumps that fit
    amp = extra / (2 * n)
    out = [(x1, y1)]; s = 0.3
    for k in range(n):
        a = (x1 + ux * s, y1 + uy * s); c = (a[0] + ux * pitch, a[1] + uy * pitch)
        out += [a, (a[0] + amp_dir[0] * amp, a[1] + amp_dir[1] * amp), (c[0] + amp_dir[0] * amp, c[1] + amp_dir[1] * amp), c]
        s += 2 * pitch
    out.append((x2, y2))
    return pts[:seg_i] + [(round(x, 4), round(y, 4)) for x, y in out] + pts[seg_i + 2:], amp

pairs = {}
# ---- D0 (inner): D0N pad x28 -> J2 28.5 ; D0P pad x29 -> J2 27.5 (P/N swap through the via positions) ----
b0n = [(28.0, 12.12), (28.0, 13.6), (28.3, 13.95)]; v0n = (28.3, 13.95)
f0n = [v0n, (28.3, 11.2), (28.5, 11.0), (28.5, 9.6)]
b0p = [(29.0, 12.12), (29.0, 14.75), (27.5, 14.75)]; v0p = (27.5, 14.75)
f0p = [v0p, (27.5, 9.6)]
pairs['D0'] = (('CSI_D0N', b0n, v0n, f0n), ('CSI_D0P', b0p, v0p, f0p))
# ---- D1 (middle): pads P45/P46 right column -> vias at the pad inner ends -> F lanes y 15.4/15.807 -> J2 25.5/24.5 ----
yn, yp = 15.4, 15.807
b1n = [(33.38, 14.5), (31.7, 14.5)]; v1n = (31.7, 14.5)
f1n = [v1n, (30.8, yn), (25.9, yn), (25.5, yn - 0.4), (25.5, 9.6)]
b1p = [(33.38, 15.5), (31.7, 15.5)]; v1p = (31.7, 15.5)
f1p = [v1p, (31.393, yp), (24.9, yp), (24.5, yp - 0.4), (24.5, 9.6)]
pairs['D1'] = (('CSI_D1N', b1n, v1n, f1n), ('CSI_D1P', b1p, v1p, f1p))
# ---- CLK (outer): pads x30 (P) / x31 (N) -> south on B -> vias -> F lanes y 16.6 / 17.007 -> J2 22.5 / 21.5 ----
cn, cp = 16.6, 17.007
bcn = [(31.0, 12.12), (31.0, 16.6)]; vcn = (31.0, 16.6)
fcn = [vcn, (22.9, cn), (22.5, cn - 0.4), (22.5, 9.6)]
bcp = [(30.0, 12.12), (30.0, 17.4)]; vcp = (30.0, 17.4)
fcp = [vcp, (29.607, cp), (21.9, cp), (21.5, cp - 0.4), (21.5, 9.6)]
pairs['CLK'] = (('CSI_CLKN', bcn, vcn, fcn), ('CSI_CLKP', bcp, vcp, fcp))

# length match: serpentine on the shorter leg's F vertical run into J2 (meander side given per pair)
SIDE = {'D0': (1, 0), 'D1': (1, 0), 'CLK': (-1, 0)}
report = {}
for name, legs in pairs.items():
    Ls = [length(bp) + length(fp) for _, bp, _, fp in legs]
    short = 0 if Ls[0] < Ls[1] else 1
    extra = abs(Ls[0] - Ls[1])
    net, bp, v, fp = legs[short]
    if extra > 0.1:
        seg = max(range(len(fp) - 1), key=lambda i: math.dist(fp[i], fp[i + 1]) if fp[i][0] == fp[i + 1][0] else 0)
        fp, amp = serpentine(fp, seg, extra, SIDE[name])
        legs = list(legs); legs[short] = (net, bp, v, fp); pairs[name] = tuple(legs)
    report[name] = [round(length(bp) + length(fp), 3) for _, bp, _, fp in pairs[name]]
for name, legs in pairs.items():
    for net, bp, v, fp in legs:
        track(bp, net, Bl); via(*v, net); track(fp, net, F)
pcbnew.SaveBoard(BOARD, b)
print('ripped', len(rm), 'lengths (N,P):', report, 'skew:', {k: round(abs(a - c), 3) for k, (a, c) in report.items()})
