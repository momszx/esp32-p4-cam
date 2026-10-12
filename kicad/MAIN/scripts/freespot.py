# Move the given footprints (same side as now) to the nearest spot free of courtyards, M2 keepouts, J1 shell slots
# and locked copper. Usage: freespot.py REF[,REF...]
import math, sys
import pcbnew
BOARD = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
T, mm = pcbnew.ToMM, pcbnew.FromMM
b = pcbnew.LoadBoard(BOARD)
fp = {f.GetReference(): f for f in b.GetFootprints()}
refs = sys.argv[1].split(',')
def cyb(f):
    bb = f.GetCourtyard(pcbnew.B_CrtYd if f.IsFlipped() else pcbnew.F_CrtYd).BBox()
    return T(bb.GetLeft()), T(bb.GetTop()), T(bb.GetRight()), T(bb.GetBottom())
for ref in refs:
    f = fp[ref]; side = f.IsFlipped()
    rects = [cyb(g) for r, g in fp.items() if r != ref and g.IsFlipped() == side and not r.startswith('MH')]
    rects += [(x - 2, y - 2, x + 2, y + 2) for x, y in ((5.75, 8.25), (39.25, 8.25), (5.75, 41.75), (39.25, 41.75))]
    for p in fp['J1'].Pads():
        if p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH):
            bb = p.GetBoundingBox(); rects.append((T(bb.GetLeft()) - .4, T(bb.GetTop()) - .4, T(bb.GetRight()) + .4, T(bb.GetBottom()) + .4))
    lay = pcbnew.B_Cu if side else pcbnew.F_Cu
    for t in b.GetTracks():
        if t.IsLocked() and t.GetClass() != 'PCB_VIA' and t.GetLayer() == lay:
            s, e = t.GetStart(), t.GetEnd(); w = T(t.GetWidth()) / 2 + 0.3
            rects.append((min(T(s.x), T(e.x)) - w, min(T(s.y), T(e.y)) - w, max(T(s.x), T(e.x)) + w, max(T(s.y), T(e.y)) + w))
    ox, oy = T(f.GetPosition().x), T(f.GetPosition().y); best = None
    for rad in [i * 0.2 for i in range(0, 100)]:
        for k in range(max(1, int(rad * 10))):
            a = 2 * math.pi * k / max(1, int(rad * 10))
            for rot in (f.GetOrientationDegrees(), f.GetOrientationDegrees() + 90):
                f.SetOrientationDegrees(rot)
                f.SetPosition(pcbnew.VECTOR2I(mm(round((ox + rad * math.cos(a)) / 0.05) * 0.05), mm(round((oy + rad * math.sin(a)) / 0.05) * 0.05)))
                l, t_, r, bt = cyb(f)
                if l >= .4 and t_ >= .4 and r <= 44.6 and bt <= 44.6 and all(r + .15 <= a0 or l - .15 >= a2 or bt + .15 <= a1 or t_ - .15 >= a3 for a0, a1, a2, a3 in rects):
                    best = (rot, T(f.GetPosition().x), T(f.GetPosition().y)); break
            if best: break
        if best: break
    print(ref, '->', best)
pcbnew.SaveBoard(BOARD, b)
