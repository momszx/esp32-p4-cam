# Connect each pad of a power net to its In2 power zone: shortest stub (pad layer) to a via spot inside the zone.
# Usage: zone_drop.py <geom.json> <pwr_targets.json> <net> <out.json>
import json, math, sys
import numpy as np
argv = sys.argv; sys.argv = ['x']
exec(open(__file__.replace('zone_drop.py', 'maze.py')).read().split("if __name__")[0])
geom = json.load(open(argv[1])); tg = json.load(open(argv[2])); net = argv[3]
T, V, g = raster(geom, net)
x0, y0, nx, ny = g
poly = np.asarray(tg['zones'][net])
X, Y = np.meshgrid(x0 + (np.arange(nx) + 0.5) * R, y0 + (np.arange(ny) + 0.5) * R)
inside = np.zeros((ny, nx), bool)
xs, ys = poly[:, 0], poly[:, 1]; xb, yb = np.roll(xs, -1), np.roll(ys, -1)
for k in range(len(xs)):
    if ys[k] == yb[k]: continue
    inside ^= ((ys[k] > Y) != (yb[k] > Y)) & (X < (xb[k] - xs[k]) * (Y - ys[k]) / (yb[k] - ys[k]) + xs[k])
m = int(0.6 / R)                                    # stay 0.6 mm inside the zone outline
core = inside.copy()
for dj in (-m, 0, m):
    for di in (-m, 0, m): core &= np.roll(np.roll(inside, dj, 0), di, 1)
viaok = ~V.any(axis=0) & core
out = []; done = 0
import os
ONLY = set(os.environ.get('ZD_ONLY', '').split(',')) - {''}
MAXD, MAXP = float(os.environ.get('ZD_MAXD', '6')), int(os.environ.get('ZD_MAXP', '200'))
for ref, num, px, py, lay in tg['pads'][net]:
    if ONLY and f'{ref}.{num}' not in ONLY: continue
    layers = [int(c) for c in lay]
    src = cells((px, py), layers, T, g)
    pj, pi = int((py - y0) / R), int((px - x0) / R)
    cj, ci = np.nonzero(viaok)
    if not len(cj): break
    d = (cj - pj) ** 2 + (ci - pi) ** 2
    order = np.argsort(d)[:1600:40]                  # a spread of near candidates
    ok = False
    for k in order:
        tx, ty = x0 + (ci[k] + 0.5) * R, y0 + (cj[k] + 0.5) * R
        if math.hypot(tx - px, ty - py) > MAXD: break
        for l in layers:
            path = astar(T, V, src, cells((tx, ty), [l], T, g))
            if path and len(path) < MAXP:
                segs, vias = to_segments(path, T, g, (px, py), (round(tx, 3), round(ty, 3)))
                out.append({'net': net, 'segs': segs, 'vias': vias + [(round(tx, 3), round(ty, 3))]}); ok = True; break
        if ok: break
    done += ok
    print(f'{ref}.{num}: {"ok" if ok else "FAIL"}')
json.dump(out, open(argv[4], 'w'))
print(f'{net}: {done}/{len(tg["pads"][net])} pads dropped to the zone')
