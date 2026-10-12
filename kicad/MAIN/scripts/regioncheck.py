# Checks that every item a fix-agent removed/changed/added lies inside its region (parallel-edit fence for pcbmerge.py).
# usage (KiCad python): regioncheck.py <base.kicad_pcb> <mod.kicad_pcb> "x0,y0,x1,y1;x0,y0,x1,y1"   (mm, union of rects)
import os, sys
import pcbnew
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcbmerge import diff

TOL = 0.05
T = pcbnew.ToMM

def inside(bb, rects):
    l, t, r, b = T(bb.GetLeft()), T(bb.GetTop()), T(bb.GetRight()), T(bb.GetBottom())
    # every corner must sit in some rect (good enough for a union of axis-aligned rects that tile the board)
    corners = [(l, t), (r, t), (l, b), (r, b)]
    return all(any(x0 - TOL <= x <= x1 + TOL and y0 - TOL <= y <= y1 + TOL for x0, y0, x1, y1 in rects) for x, y in corners)

def index(board):
    b = pcbnew.LoadBoard(board)
    idx = {}
    for it in list(b.GetTracks()) + list(b.Zones()) + list(b.GetDrawings()):
        idx['uuid:' + it.m_Uuid.AsString()] = it
    for f in b.GetFootprints():
        idx['uuid:' + f.m_Uuid.AsString()] = f
    return b, idx

def bbox(it):
    if isinstance(it, pcbnew.FOOTPRINT):
        bb = pcbnew.BOX2I()
        for p in it.Pads(): bb.Merge(p.GetBoundingBox())
        return bb
    return it.GetBoundingBox()

def main(base, mod, spec):
    rects = [tuple(map(float, r.split(','))) for r in spec.split(';') if r.strip()]
    d = diff(base, mod)
    bA, A = index(base)
    bB, B = index(mod)
    bad = []
    for k in d['removed']: bad += [('removed', k)] if k not in A or not inside(bbox(A[k]), rects) else []
    for k in d['added']: bad += [('added', k)] if k not in B or not inside(bbox(B[k]), rects) else []
    for k in d['changed']:
        if k not in A or k not in B or not inside(bbox(A[k]), rects) or not inside(bbox(B[k]), rects): bad.append(('changed', k))
    print(f"removed {len(d['removed'])}, added {len(d['added'])}, changed {len(d['changed'])}")
    for kind, k in bad:
        it = A.get(k) or B.get(k)
        desc = it.GetReference() if isinstance(it, pcbnew.FOOTPRINT) else (it.GetClass() + ' ' + it.GetNetname() if it else 'non-uuid item (setup/title/etc)')
        bb = bbox(it) if it else None
        print('OUTSIDE REGION', kind, k, desc, [round(T(v), 2) for v in (bb.GetLeft(), bb.GetTop(), bb.GetRight(), bb.GetBottom())] if bb else '')
    print('REGION OK' if not bad else f'REGION VIOLATIONS: {len(bad)}')
    return not bad

if __name__ == '__main__':
    sys.exit(0 if main(*sys.argv[1:4]) else 1)
