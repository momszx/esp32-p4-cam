# Push-apart legalizer: removes courtyard overlaps of small parts while keeping big/fixed parts in place.
# Rectangles = courtyard bboxes (+gap); fixed obstacles = big parts, mounting-hole keepouts, J1 shell slots (both sides).
import sys, math
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
FIXED = {'U1', 'J1', 'J2', 'J3', 'J5', 'J4', 'J7', 'SW1', 'SW2', 'SW3', 'D1'}
GAP, EDGE, W, H = 0.15, 0.4, 45.0, 45.0
T, mm = pcbnew.ToMM, pcbnew.FromMM
b = pcbnew.LoadBoard(BOARD)
fps = [f for f in b.GetFootprints() if not f.GetReference().startswith('MH')]
items = {}
for f in fps:
    side = 'B' if f.IsFlipped() else 'F'
    bb = f.GetCourtyard(pcbnew.B_CrtYd if side == 'B' else pcbnew.F_CrtYd).BBox()
    cx, cy = T(f.GetPosition().x), T(f.GetPosition().y)
    items[f.GetReference()] = dict(f=f, side=side, ox=T(bb.GetCenter().x) - cx, oy=T(bb.GetCenter().y) - cy,
                                   w=T(bb.GetWidth()) + GAP, h=T(bb.GetHeight()) + GAP, x=cx, y=cy, x0=cx, y0=cy)
obst = []   # (side or '*', cx, cy, w, h)
for x, y in ((5.75, 8.25), (39.25, 8.25), (5.75, 41.75), (39.25, 41.75)):
    obst.append(('*', x, y, 4.0, 4.0))
j1 = items['J1']['f']
for p in j1.Pads():
    if p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH):
        bb = p.GetBoundingBox(); obst.append(('F', T(bb.GetCenter().x), T(bb.GetCenter().y), T(bb.GetWidth()) + 0.8, T(bb.GetHeight()) + 0.8))
for r, it in items.items():
    if r in FIXED: obst.append((it['side'], it['x'] + it['ox'], it['y'] + it['oy'], it['w'], it['h']))
ONLY = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else None
for t in b.GetTracks():   # locked copper (CSI, manual trunks) is an obstacle on its layer
    if not t.IsLocked() or t.GetClass() == 'PCB_VIA': continue
    side = 'F' if t.GetLayer() == pcbnew.F_Cu else ('B' if t.GetLayer() == pcbnew.B_Cu else None)
    if side is None: continue
    s_, e_ = t.GetStart(), t.GetEnd(); w_ = T(t.GetWidth()) + 0.6
    obst.append((side, (T(s_.x) + T(e_.x)) / 2, (T(s_.y) + T(e_.y)) / 2, abs(T(s_.x) - T(e_.x)) + w_, abs(T(s_.y) - T(e_.y)) + w_))
mov = [r for r in items if r not in FIXED and (ONLY is None or r in ONLY)]
for r, it in items.items():
    if r not in FIXED and r not in mov: obst.append((it['side'], it['x'] + it['ox'], it['y'] + it['oy'], it['w'], it['h']))
def rect(it): return it['x'] + it['ox'], it['y'] + it['oy'], it['w'], it['h']
def push(a, cx, cy, w, h, k=1.0):
    ax, ay, aw, ah = rect(a)
    dx, dy = ax - cx, ay - cy
    ox, oy = (aw + w) / 2 - abs(dx), (ah + h) / 2 - abs(dy)
    if ox <= 0 or oy <= 0: return 0
    if ox < oy: a['x'] += math.copysign(ox * k, dx or 1e-3)
    else: a['y'] += math.copysign(oy * k, dy or 1e-3)
    return 1
for it_ in range(400):
    n = 0
    for i, ra in enumerate(mov):
        a = items[ra]
        for s, cx, cy, w, h in obst:
            if s in ('*', a['side']): n += push(a, cx, cy, w, h)
        for rb in mov[i + 1:]:
            c = items[rb]
            if c['side'] != a['side']: continue
            ax, ay, aw, ah = rect(a); bx, by, bw, bh = rect(c)
            dx, dy = ax - bx, ay - by
            ox, oy = (aw + bw) / 2 - abs(dx), (ah + bh) / 2 - abs(dy)
            if ox > 0 and oy > 0:
                n += 1
                if ox < oy: s_ = math.copysign(ox / 2, dx or 1e-3); a['x'] += s_; c['x'] -= s_
                else: s_ = math.copysign(oy / 2, dy or 1e-3); a['y'] += s_; c['y'] -= s_
        ax, ay, aw, ah = rect(a)   # keep inside the board
        a['x'] += max(0, EDGE + aw / 2 - ax) - max(0, ax + aw / 2 - (W - EDGE))
        a['y'] += max(0, EDGE + ah / 2 - ay) - max(0, ay + ah / 2 - (H - EDGE))
        a['x'] += 0.02 * (a['x0'] - a['x']); a['y'] += 0.02 * (a['y0'] - a['y'])
    if n == 0: break
for r in mov:
    it = items[r]; it['f'].SetPosition(pcbnew.VECTOR2I(mm(round(it['x'] / 0.05) * 0.05), mm(round(it['y'] / 0.05) * 0.05)))
pcbnew.SaveBoard(BOARD, b)
moved = sorted(((round(math.hypot(items[r]['x'] - items[r]['x0'], items[r]['y'] - items[r]['y0']), 2), r) for r in mov), reverse=True)
print('iterations', it_ + 1, 'remaining overlaps', n, 'largest moves', moved[:10])
