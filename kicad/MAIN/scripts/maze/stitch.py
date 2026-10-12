# GND stitching via placement: RF fence, CSI return vias, then a regular grid. Writes routes JSON for kgeom.py apply.
# Usage: stitch.py <geom.json> <out.json>
import json, math, sys
import numpy as np
argv = sys.argv; sys.argv = ['x']
exec(open(__file__.replace('stitch.py', 'maze.py')).read().split("if __name__")[0])
geom = json.load(open(argv[1]))
T, V, g = raster(geom, 'GND')
x0, y0, nx, ny = g
W, H = geom['board'][2] - x0, geom['board'][3] - y0
P = np.zeros((ny, nx), bool)          # GND pads (+via clearance): no via-in-pad
existing = []
for p in geom['polys']:
    if p['net'] != 'GND': continue
    if p['k'] == 'PAD':
        for poly in p['v']: fill_mask = poly; _ = None
    if p['k'] == 'PCB_VIA':
        q = np.asarray(p['t'][0]); existing.append((q[:, 0].mean(), q[:, 1].mean()))
# rasterize GND pads (reuse raster's fill via a tiny local copy)
def fill(mask, poly):
    q = np.asarray(poly); xs, ys = q[:, 0], q[:, 1]
    i0, i1 = max(0, int((xs.min() - x0) / R) - 1), min(nx, int((xs.max() - x0) / R) + 2)
    j0, j1 = max(0, int((ys.min() - y0) / R) - 1), min(ny, int((ys.max() - y0) / R) + 2)
    X, Y = np.meshgrid(x0 + (np.arange(i0, i1) + 0.5) * R, y0 + (np.arange(j0, j1) + 0.5) * R)
    ins = np.zeros(X.shape, bool); xa, ya, xb, yb = xs, ys, np.roll(xs, -1), np.roll(ys, -1)
    for k in range(len(xs)):
        if ya[k] == yb[k]: continue
        ins ^= ((ya[k] > Y) != (yb[k] > Y)) & (X < (xb[k] - xa[k]) * (Y - ya[k]) / (yb[k] - ya[k]) + xa[k])
    mask[j0:j1, i0:i1] |= ins
for p in geom['polys']:
    if p['net'] == 'GND' and p['k'] == 'PAD':
        for poly in p['v']: fill(P, poly)
ok = ~(V[0] | V[1]) & ~P
placed = list(existing); new = []
def try_at(x, y, mind):
    if not (0.9 <= x - x0 <= W - 0.9 and 0.9 <= y - y0 <= H - 0.9): return False
    i, j = int((x - x0) / R), int((y - y0) / R)
    if not ok[j, i]: return False
    if any((x - a) ** 2 + (y - b) ** 2 < mind * mind for a, b in placed): return False
    placed.append((x, y)); new.append((round(x, 3), round(y, 3))); return True
def nearest(x, y, rmin, rmax, mind):
    for r in np.arange(rmin, rmax, 0.05):
        for a in np.linspace(0, 2 * math.pi, int(2 * math.pi * r / 0.1) + 1):
            if try_at(x + r * math.cos(a), y + r * math.sin(a), mind): return True
    return False
# 1) RF fence: RF B line y 34.5 x 3.0..9.62, then x 3.0 y 34.5..36.3 (CPWG, fence <= 2 mm pitch)
fence = 0
for x in np.arange(3.0, 9.8, 1.0):
    for dy in (-1.05, 1.05):
        fence += nearest(x, 34.5 + dy, 0.0, 0.45, 0.85)
for y in np.arange(34.5, 36.4, 1.0):
    for dx in (-1.05, 1.05):
        fence += nearest(3.0 + dx, y, 0.0, 0.45, 0.85)
# 2) CSI return vias next to each signal via
csi = [(28.5, 7.5), (27.5, 6.6), (37.7, 14.5), (37.0, 15.5), (22.5, 3.6), (21.5, 4.5)]
ret = sum(nearest(x, y, 0.95, 1.8, 0.9) for x, y in csi)
# 3) regular stitching grid
grid = 0
for y in np.arange(y0 + 1.0, y0 + H - 0.9, 2.0):
    for x in np.arange(x0 + 1.0, x0 + W - 0.9, 2.0):
        grid += nearest(x, y, 0.0, 0.5, 1.5)
json.dump([{'net': 'GND', 'segs': [], 'vias': new}], open(argv[2], 'w'))
print(f'fence {fence}, csi return {ret}, grid {grid}, total new {len(new)}, existing GND vias {len(existing)}')
