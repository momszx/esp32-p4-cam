# Grid A* router, 3 routing layers (0=F.Cu, 1=B.Cu, 2=In2.Cu; In1 = GND plane), 0.05 mm grid, 0.2 mm tracks, 0.6 mm vias.
# Usage: maze.py <geom.json> <net> <ax,ay,layers> <bx,by,layers> <out.json>   layers e.g. "0", "1", "01"
import heapq, json, math, sys
import numpy as np
R = 0.05
VIA_COST = 30          # in grid steps (1.5 mm) -> prefer staying on a layer
EDGE_MARGIN = 0.65     # copper-edge 0.5 + half track 0.1 + raster margin

def raster(geom, net, soft=False):
    x0, y0, x1, y1 = geom['board']
    nx, ny = int(math.ceil((x1 - x0) / R)), int(math.ceil((y1 - y0) / R))
    NL = 3
    T = np.zeros((NL, ny, nx), bool); V = np.zeros((NL, ny, nx), bool)
    cr = geom.get('netclr', {}).get(net, 0.15)   # DRC uses max(own, obstacle) clearance; polys carry the obstacle's
    TE = np.zeros((NL, ny, nx), bool); VE = np.zeros((NL, ny, nx), bool)   # obstacles needing extra inflation
    ST = np.zeros((NL, ny, nx), bool); SV = np.zeros((NL, ny, nx), bool)   # soft (rip-up-able) obstacles
    def fill(mask, poly):
        p = np.asarray(poly); xs, ys = p[:, 0], p[:, 1]
        i0, i1 = max(0, int((xs.min() - x0) / R) - 1), min(nx, int((xs.max() - x0) / R) + 2)
        j0, j1 = max(0, int((ys.min() - y0) / R) - 1), min(ny, int((ys.max() - y0) / R) + 2)
        if i0 >= i1 or j0 >= j1: return
        X, Y = np.meshgrid(x0 + (np.arange(i0, i1) + 0.5) * R, y0 + (np.arange(j0, j1) + 0.5) * R)
        inside = np.zeros(X.shape, bool)
        xa, ya, xb, yb = xs, ys, np.roll(xs, -1), np.roll(ys, -1)
        for k in range(len(xs)):
            if ya[k] == yb[k]: continue
            inside ^= ((ya[k] > Y) != (yb[k] > Y)) & (X < (xb[k] - xa[k]) * (Y - ya[k]) / (yb[k] - ya[k]) + xa[k])
        mask[j0:j1, i0:i1] |= inside
    for p in geom['polys']:
        if p['l'] >= NL: continue
        if p['net'] == net:
            if p.get('smd'):  # never put a via into (or touching) an SMD pad, own net included
                for poly in p['v']: fill(V[p['l']], poly)
            continue
        if soft and not p.get('lk', True):   # unlocked foreign copper: passable at a cost (rip-up candidates)
            for poly in p['t']: fill(ST[p['l']], poly)
            for poly in p['v']: fill(SV[p['l']], poly)
            continue
        low = p.get('c', 0.2) < cr - 1e-6
        for poly in p['t']: fill((TE if low else T)[p['l']], poly)
        for poly in p['v']: fill((VE if low else V)[p['l']], poly)
    K = np.zeros((NL, ny, nx), bool); KV = np.zeros((NL, ny, nx), bool)
    for k in geom['keep']:
        if k['l'] >= NL: continue
        for poly in k['p']:
            if k.get('tr', True): fill(K[k['l']], poly)
            if k.get('via', True): fill(KV[k['l']], poly)
    def dilate(A, r):  # square-ish dilation by r cells (keepouts are not inflated in the export)
        out = A.copy()
        for dj in range(-r, r + 1):
            for di in range(-r, r + 1):
                if dj * dj + di * di > r * r: continue
                out |= np.roll(np.roll(A, dj, axis=-2), di, axis=-1)
        return out
    T |= dilate(K, int(math.ceil(0.13 / R))); V |= dilate(KV, int(math.ceil(0.33 / R)))
    ext = int(math.ceil((cr - 0.15) / R - 1e-6))   # ponytail: assumes low obstacles are Default 0.15
    T |= dilate(TE, ext); V |= dilate(VE, ext)
    if cr <= 0.15 + 1e-6: V = ~dilate(~V, 1)   # Default nets get 0.5/0.25 vias (kgeom apply): via keep-out 1 cell smaller
    for A, marg in ((T, EDGE_MARGIN), (V, 0.5 + 0.3 + 0.05)):  # via: edge clr 0.5 + via radius 0.3
        m = int(math.ceil(marg / R))
        A[:, :m, :] = A[:, -m:, :] = A[:, :, :m] = A[:, :, -m:] = True
    if soft: return T, V, (x0, y0, nx, ny), dilate(ST, ext) & ~T, dilate(SV, ext)
    return T, V, (x0, y0, nx, ny)

def cells(pt, layers, T, g, rad=0.12):
    x0, y0, nx, ny = g
    x, y = pt
    out = []
    for l in layers:
        for j in range(int((y - rad - y0) / R), int((y + rad - y0) / R) + 1):
            for i in range(int((x - rad - x0) / R), int((x + rad - x0) / R) + 1):
                cx, cy = x0 + (i + 0.5) * R, y0 + (j + 0.5) * R
                if (cx - x) ** 2 + (cy - y) ** 2 <= rad * rad: out.append((l, j, i))
    return out

import os
SOFT_COST = float(os.environ.get('SOFT_COST', '8'))   # per grid step through rip-up-able copper (SOFT=1 mode); high = detour over rip

def astar(T, V, src, dst, via_target=False, ST=None, SV=None):
    free = ~T; via_ok = ~V.any(axis=0)
    sv = SV.any(axis=0) if SV is not None else None
    sc = (lambda l, j, i: SOFT_COST if ST[l, j, i] else 0) if ST is not None else (lambda l, j, i: 0)
    for l, j, i in src + dst: free[l, j, i] = True
    dset = set(dst)
    if dst:
        tj = np.mean([d[1] for d in dst]); ti = np.mean([d[2] for d in dst])
        h = lambda j, i: max(abs(j - tj), abs(i - ti)) + 0.414 * min(abs(j - tj), abs(i - ti))
    else:
        h = lambda j, i: 0.0   # via-target search (GND fan-out): plain Dijkstra
    g = {}; prev = {}; pq = []
    for s in src: g[s] = 0.0; heapq.heappush(pq, (h(s[1], s[2]), 0.0, s))
    moves = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]
    _, ny, nx = T.shape
    while pq:
        f, gc, cur = heapq.heappop(pq)
        if gc > g.get(cur, 1e18): continue
        if cur in dset or (via_target and via_ok[cur[1], cur[2]] and gc > 0):
            path = [cur]
            while path[-1] in prev: path.append(prev[path[-1]])
            return path[::-1]
        l, j, i = cur
        nbrs = [((l, j + dj, i + di), c + sc(l, j + dj, i + di)) for dj, di, c in moves if 0 <= j + dj < ny and 0 <= i + di < nx and free[l, j + dj, i + di]]
        if via_ok[j, i]:
            vc = VIA_COST + (4 * SOFT_COST if sv is not None and sv[j, i] else 0)
            nbrs += [((m, j, i), vc) for m in range(T.shape[0]) if m != l and free[m, j, i]]
        for n, c in nbrs:
            ng = gc + c
            if ng < g.get(n, 1e18):
                g[n] = ng; prev[n] = cur; heapq.heappush(pq, (ng + h(n[1], n[2]), ng, n))
    return None

def clear_line(free, l, a, b):
    (j0, i0), (j1, i1) = a, b
    n = int(max(abs(j1 - j0), abs(i1 - i0)) * 2) + 1
    for t in np.linspace(0, 1, n):
        if not free[l, int(round(j0 + (j1 - j0) * t)), int(round(i0 + (i1 - i0) * t))]: return False
    return True

def to_segments(path, T, g, a_pt, b_pt):
    x0, y0, _, _ = g
    free = ~T
    for l, j, i in path: free[l, j, i] = True
    xy = lambda j, i: (round(x0 + (i + 0.5) * R, 3), round(y0 + (j + 0.5) * R, 3))
    runs, vias = [], []
    cur = [path[0]]
    for p in path[1:]:
        if p[0] != cur[-1][0]:
            runs.append(cur); vias.append(xy(p[1], p[2])); cur = [p]
        else: cur.append(p)
    runs.append(cur)
    segs = []
    for run in runs:
        l = run[0][0]
        pts = [run[0]]
        k = 0
        while k < len(run) - 1:  # string pulling
            m = len(run) - 1
            while m > k + 1 and not clear_line(free, l, run[k][1:], run[m][1:]): m -= 1
            pts.append(run[m]); k = m
        for p, q in zip(pts, pts[1:]):
            segs.append([l, *xy(p[1], p[2]), *xy(q[1], q[2])])
    # tie path ends to the exact item points
    s0, e0 = path[0], path[-1]
    segs.insert(0, [s0[0], *a_pt, *xy(s0[1], s0[2])])
    segs.append([e0[0], *xy(e0[1], e0[2]), *b_pt])
    return [s for s in segs if (s[1], s[2]) != (s[3], s[4])], vias

def victims(geom, net, path, g):
    """uuids of unlocked foreign tracks/vias whose clearance zone the (soft) path crosses."""
    x0, y0 = g[0], g[1]
    xy = lambda j, i: (x0 + (i + 0.5) * R, y0 + (j + 0.5) * R)
    trk = {}
    for l, j, i in path: trk.setdefault(l, []).append(xy(j, i))
    via = [xy(p[1], p[2]) for p, q in zip(path, path[1:]) if p[0] != q[0]]
    def hit(poly, pts):
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        for x, y in pts:
            if not (bx0 <= x <= bx1 and by0 <= y <= by1): continue
            c = False
            for k in range(len(poly)):
                (xa, ya), (xb, yb) = poly[k], poly[(k + 1) % len(poly)]
                if (ya > y) != (yb > y) and x < (xb - xa) * (y - ya) / (yb - ya) + xa: c = not c
            if c: return True
        return False
    out = set()
    for p in geom['polys']:
        if p['net'] == net or p.get('lk', True) or p['l'] > 2: continue
        if any(hit(q, trk.get(p['l'], [])) for q in p['t']) or any(hit(q, via) for q in p['v']): out.add(p['id'])
    return sorted(out)

def parse(s):
    x, y, ls = s.split(','); return (float(x), float(y)), [int(c) for c in ls]

if __name__ == '__main__':
    geom = json.load(open(sys.argv[1])); net = sys.argv[2]
    (a, al) = parse(sys.argv[3]); (b, bl) = ((0, 0), []) if sys.argv[4] == 'VIA' else parse(sys.argv[4])
    import os
    soft = bool(os.environ.get('SOFT'))
    T, V, g, *SS = raster(geom, net, soft)
    vt = sys.argv[4] == 'VIA'
    ST, SV = SS or (None, None)
    path = astar(T, V, cells(a, al, T, g), [] if vt else cells(b, bl, T, g), via_target=vt, ST=ST, SV=SV)
    if path is None: sys.exit(f'NO ROUTE {net}')
    if vt:   # GND fan-out: end at the via spot, drop the via there
        x0_, y0_ = g[0], g[1]; e = path[-1]
        b = (round(x0_ + (e[2] + 0.5) * R, 3), round(y0_ + (e[1] + 0.5) * R, 3))
    segs, vias = to_segments(path, T, g, a, b)
    if vt: vias.append(b)
    out = json.load(open(sys.argv[5])) if len(sys.argv) > 6 and sys.argv[6] == 'append' else []
    entry = {'net': net, 'segs': segs, 'vias': vias}
    if soft: entry['victims'] = victims(geom, net, path, g)
    out.append(entry)
    json.dump(out, open(sys.argv[5], 'w'))
    print(f'{net}: {len(segs)} segs, {len(vias)} vias, path {len(path)} cells')
