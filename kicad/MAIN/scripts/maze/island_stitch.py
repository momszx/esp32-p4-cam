# Join GND copper islands to the main GND net with vias placed where an island overlaps main copper on the other layer.
# Usage: island_stitch.py <geom.json> <gndmap.json> <out.json>  -> prints component stats
import json, math, sys
from collections import deque
import numpy as np
argv = sys.argv; sys.argv = ['x']
exec(open(__file__.replace('island_stitch.py', 'maze.py')).read().split("if __name__")[0])
geom = json.load(open(argv[1])); gm = json.load(open(argv[2]))
T, V, g = raster(geom, 'GND')
x0, y0, nx, ny = g
W, H = geom['board'][2] - x0, geom['board'][3] - y0
def fill(mask, poly):
    q = np.asarray(poly); xs, ys = q[:, 0], q[:, 1]
    i0, i1 = max(0, int((xs.min() - x0) / R) - 1), min(nx, int((xs.max() - x0) / R) + 2)
    j0, j1 = max(0, int((ys.min() - y0) / R) - 1), min(ny, int((ys.max() - y0) / R) + 2)
    if i0 >= i1 or j0 >= j1: return
    X, Y = np.meshgrid(x0 + (np.arange(i0, i1) + 0.5) * R, y0 + (np.arange(j0, j1) + 0.5) * R)
    ins = np.zeros(X.shape, bool); xa, ya, xb, yb = xs, ys, np.roll(xs, -1), np.roll(ys, -1)
    for k in range(len(xs)):
        if ya[k] == yb[k]: continue
        ins ^= ((ya[k] > Y) != (yb[k] > Y)) & (X < (xb[k] - xa[k]) * (Y - ya[k]) / (yb[k] - ya[k]) + xa[k])
    mask[j0:j1, i0:i1] ^= ins   # xor: holes inside fills
C = np.zeros((2, ny, nx), bool)
for p in gm['polys']:
    for poly in p['p']:
        tmp = np.zeros((ny, nx), bool); fill(tmp, poly); C[p['l']] |= tmp
# label components: 4-connectivity within layer, vias join layers
lab = np.full((2, ny, nx), -1, np.int32)
via_cells = set()
for x, y in gm['vias']:
    i, j = int((x - x0) / R), int((y - y0) / R)
    for dj in range(-4, 5):
        for di in range(-4, 5):
            if dj * dj + di * di <= 16 and 0 <= j + dj < ny and 0 <= i + di < nx: via_cells.add((j + dj, i + di))
ncomp = 0; sizes = []
for l in (0, 1):
    for j, i in zip(*np.nonzero(C[l])):
        if lab[l, j, i] >= 0: continue
        q = deque([(l, j, i)]); lab[l, j, i] = ncomp; n = 0
        while q:
            a, b_, c = q.popleft(); n += 1
            for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                jj, ii = b_ + dj, c + di
                if 0 <= jj < ny and 0 <= ii < nx and C[a, jj, ii] and lab[a, jj, ii] < 0:
                    lab[a, jj, ii] = ncomp; q.append((a, jj, ii))
            if (b_, c) in via_cells and C[1 - a, b_, c] and lab[1 - a, b_, c] < 0:
                lab[1 - a, b_, c] = ncomp; q.append((1 - a, b_, c))
        sizes.append(n); ncomp += 1
main = int(np.argmax(sizes))
# erode copper by 0.2 mm so the via sits well inside both fills
def erode(A, r):
    out = A.copy()
    for dj in range(-r, r + 1):
        for di in range(-r, r + 1):
            if dj * dj + di * di <= r * r: out &= np.roll(np.roll(A, dj, -2), di, -1)
    return out
Ce = erode(C, 4)
viaok = ~(V[0] | V[1])
m = int(0.9 / R); viaok[:m, :] = viaok[-m:, :] = viaok[:, :m] = viaok[:, -m:] = False
new = []
for k in range(ncomp):
    if k == main: continue
    best = None
    for l in (0, 1):
        cand = (lab[l] == k) & Ce[l] & Ce[1 - l] & (lab[1 - l] == main) & viaok
        js, is_ = np.nonzero(cand)
        if len(js):
            idx = len(js) // 2
            best = (round(x0 + (is_[idx] + 0.5) * R, 3), round(y0 + (js[idx] + 0.5) * R, 3)); break
    if best: new.append(best)
json.dump([{'net': 'GND', 'segs': [], 'vias': new}], open(argv[3], 'w'))
# pairs for maze routing of islands that could not be joined by a single via
pairs = []
mj, mi = np.nonzero(Ce[0] & (lab[0] == main)); mj1, mi1 = np.nonzero(Ce[1] & (lab[1] == main))
mainpts = np.concatenate([np.stack([mj, mi, np.zeros_like(mj)], 1), np.stack([mj1, mi1, np.ones_like(mj1)], 1)])[::7]
joined = set()
for k in range(ncomp):
    if k == main: continue
    pts = [(l, j, i) for l in (0, 1) for j, i in zip(*np.nonzero((lab[l] == k) & Ce[l]))]
    if not pts: pts = [(l, j, i) for l in (0, 1) for j, i in zip(*np.nonzero(lab[l] == k))]
    l, j, i = pts[len(pts) // 2]
    d = (mainpts[:, 0] - j) ** 2 + (mainpts[:, 1] - i) ** 2
    t = mainpts[int(np.argmin(d))]
    xy = lambda jj, ii: (round(x0 + (ii + 0.5) * R, 3), round(y0 + (jj + 0.5) * R, 3))
    a = xy(j, i); bpt = xy(t[0], t[1])
    pairs.append(f"{a[0]},{a[1]},{l} {bpt[0]},{bpt[1]},{int(t[2])}")
open(argv[3] + '.pairs', 'w').write('\n'.join(pairs) + '\n')
# GND vias not touching the main component are useless (isolated pockets) -> report for removal
useless = []
for x, y in gm['vias']:
    i, j = int((x - x0) / R), int((y - y0) / R)
    if lab[0, j, i] != main and lab[1, j, i] != main: useless.append((round(x, 3), round(y, 3)))
json.dump(useless, open(argv[3] + '.useless', 'w'))
print(f'useless vias {len(useless)}; ', end='')
print(f'components {ncomp}, main size {sizes[main]}, others {sorted(sizes)[-6:-1]}, joined now {len(new)}, unjoinable {ncomp - 1 - len(new)}')
