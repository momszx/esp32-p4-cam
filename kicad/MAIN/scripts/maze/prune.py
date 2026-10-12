# Remove redundant copper: per net (zone nets skipped) build the item graph (tracks, vias, pads), keep a minimum
# spanning tree (locked items forced in, short items preferred), then strip non-pad dead-end leaves.
# Only unlocked tracks/vias are removed. Usage: prune.py [--dry]   (verify with DRC afterwards)
import sys
from collections import defaultdict
import pcbnew
B = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
SKIP = {'GND', 'VBUS', 'VBUS_SW', ''}   # nets joined by zones: graph alone can't prove connectivity
b = pcbnew.LoadBoard(B); T = pcbnew.ToMM
pads = [p for f in b.GetFootprints() for p in f.Pads()]
tracks = list(b.GetTracks())
bynet = defaultdict(list)
for p in pads: bynet[p.GetNetname()].append(p)
for t in tracks: bynet[t.GetNetname()].append(t)

def touches(a, c):   # geometric connection between two items of the same net
    def pts(t): return [t.GetStart(), t.GetEnd()] if t.GetClass() == 'PCB_TRACK' else [t.GetPosition()]
    for x, y in ((a, c), (c, a)):
        if x.GetClass() == 'PCB_TRACK':
            for q in pts(x):
                if y.GetClass() == 'PCB_TRACK':
                    if y.GetLayer() == x.GetLayer() and y.HitTest(q): return True   # end-to-end and T-junctions
                elif y.HitTest(q) and y.IsOnLayer(x.GetLayer()): return True
    if a.GetClass() == 'PCB_VIA' and c.GetClass() == 'PAD': return c.HitTest(a.GetPosition())
    if c.GetClass() == 'PCB_VIA' and a.GetClass() == 'PAD': return a.HitTest(c.GetPosition())
    return False

removed = 0; report = []
for net, items in bynet.items():
    if net in SKIP or net.startswith('unconnected'): continue
    n = len(items)
    if n < 3 or not any(i.GetClass() != 'PAD' for i in items): continue
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if touches(items[i], items[j]): edges.append((i, j))
    parent = list(range(n))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    w = lambda k: 0 if items[k].GetClass() == 'PAD' or items[k].IsLocked() else T(items[k].GetLength()) if items[k].GetClass() == 'PCB_TRACK' else 0.5
    keep_e = []
    for i, j in sorted(edges, key=lambda e: max(w(e[0]), w(e[1]))):
        a, c = find(i), find(j)
        if a != c: parent[a] = c; keep_e.append((i, j))
    adj = defaultdict(set)
    for i, j in keep_e: adj[i].add(j); adj[j].add(i)
    alive = set(range(n))
    used = {k for e in keep_e for k in e} | {k for k in range(n) if items[k].GetClass() == 'PAD' or items[k].IsLocked()}
    alive &= used
    changed = True
    while changed:   # strip dead-end leaves that are not pads / locked
        changed = False
        for k in list(alive):
            if items[k].GetClass() == 'PAD' or items[k].IsLocked(): continue
            if len(adj[k] & alive) <= 1: alive.discard(k); changed = True
    drop = [items[k] for k in range(n) if k not in alive and items[k].GetClass() != 'PAD' and not items[k].IsLocked()]
    if drop: report.append((net, len(drop))); removed += len(drop)
    if '--dry' not in sys.argv:
        for t in drop: b.Remove(t)
if '--dry' not in sys.argv: pcbnew.SaveBoard(B, b)
print('removed', removed, sorted(report, key=lambda r: -r[1])[:25])
