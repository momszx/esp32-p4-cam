# KiCad-python side: 'export <board> <out.json>' dumps copper polygons inflated for track/via clearance;
# 'apply <board> <routes.json>' adds the routed segments/vias.
import json, sys
import pcbnew
T, FM = pcbnew.ToMM, pcbnew.FromMM
CLR = {'Default': 0.15, 'CSI_DIFF': 0.2, 'USB': 0.2, 'RF_50': 0.25, 'PWR': 0.2, 'PWR_LIGHT': 0.2}  # 4-layer netclasses (project_rules.py); unknown 0.2
import os
GRID_MARGIN = float(os.environ.get("GRID_MARGIN", "0.03"))  # raster error at 0.05 mm grid; 0 for tight pin escapes (DRC-guarded)
TRACK_W = float(os.environ.get("TRACK_W", "0.2"))  # routed track width (export inflation + apply); 0.1 for tight low-speed escapes
def infl(it, half):
    if it.GetClass() == 'PAD' and it.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH: return 0.3 + half + GRID_MARGIN   # hole clearance 0.25
    return CLR.get(str(it.GetNetClassName()), 0.2) + half + GRID_MARGIN
LAYERS = {0: pcbnew.F_Cu, 1: pcbnew.B_Cu, 2: pcbnew.In2_Cu}  # In1 = GND plane (not routed)

def outlines(ps):
    res = []
    for i in range(ps.OutlineCount()):
        o = ps.Outline(i)
        res.append([(round(T(o.CPoint(j).x), 3), round(T(o.CPoint(j).y), 3)) for j in range(o.PointCount())])
    return res

def shape(item, layer, infl):
    ps = pcbnew.SHAPE_POLY_SET()
    item.TransformShapeToPolygon(ps, layer, FM(infl), FM(0.01), pcbnew.ERROR_OUTSIDE)
    return outlines(ps)

def export(board, out):
    b = pcbnew.LoadBoard(board)
    items = [p for f in b.GetFootprints() for p in f.Pads()] + list(b.GetTracks())
    polys = []
    for it in items:
        for li, layer in LAYERS.items():
            if not it.IsOnLayer(layer): continue
            polys.append({'net': it.GetNetname(), 'l': li, 'k': it.GetClass(), 'smd': it.GetClass() == 'PAD' and it.GetAttribute() == pcbnew.PAD_ATTRIB_SMD,
                          'c': round(infl(it, 0) - GRID_MARGIN, 3),
                          'lk': it.GetClass() == 'PAD' or it.IsLocked(), 'id': it.m_Uuid.AsString(),
                          't': shape(it, layer, infl(it, TRACK_W / 2)), 'v': shape(it, layer, infl(it, 0.3))})
        if it.GetClass() == 'PAD' and it.HasHole():  # drilled hole blocks both layers
            for li, layer in LAYERS.items():
                if not it.IsOnLayer(layer) and it.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH or (not it.IsOnLayer(layer) and li < 2):
                    polys.append({'net': it.GetNetname(), 'l': li, 't': shape(it, LAYERS[0], infl(it, TRACK_W / 2)), 'v': shape(it, LAYERS[0], infl(it, 0.3))})
    keep = []
    for z in list(b.Zones()) + [z for f in b.GetFootprints() for z in f.Zones()]:  # incl. footprint keepouts
        if not z.GetIsRuleArea(): continue
        pts = outlines(z.Outline())
        for li, layer in LAYERS.items():
            if z.IsOnLayer(layer): keep.append({'l': li, 'p': pts, 'tr': z.GetDoNotAllowTracks(), 'via': z.GetDoNotAllowVias()})
    bb = b.GetBoardEdgesBoundingBox()
    netclr = {n: CLR.get(str(ni.GetNetClassName()), 0.2) for n, ni in b.GetNetsByName().items()}
    json.dump({'polys': polys, 'keep': keep, 'netclr': {str(k): v for k, v in netclr.items()}, 'board': [T(bb.GetLeft()), T(bb.GetTop()), T(bb.GetRight()), T(bb.GetBottom())]}, open(out, 'w'))

def apply(board, routes):
    b = pcbnew.LoadBoard(board)
    for r in json.load(open(routes)):
        net = b.FindNet(r['net'])
        own = [(T(t.GetPosition().x), T(t.GetPosition().y)) for t in b.GetTracks()
               if t.GetClass() == 'PCB_VIA' and t.GetNetname() == r['net']]
        snap = {}
        for x, y in r['vias']:  # reuse an existing same-net via within 0.8 mm instead of stacking a new one
            near = [q for q in own if (q[0] - x) ** 2 + (q[1] - y) ** 2 < 0.64]
            if near: snap[(x, y)] = near[0]
        r['segs'] = [[l, *snap.get((x1, y1), (x1, y1)), *snap.get((x2, y2), (x2, y2))] for l, x1, y1, x2, y2 in r['segs']]
        for x, y in dict.fromkeys(map(tuple, r['vias'])):  # one via per spot (path may change layer twice on one cell)
            if (x, y) in snap: continue
            own.append((x, y))
            small = str(net.GetNetClassName()) == 'Default'   # Default netclass via 0.5/0.25 (maze shrinks its via keep-out to match)
            v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(FM(x), FM(y))); v.SetWidth(FM(0.5 if small else 0.6)); v.SetDrill(FM(0.25 if small else 0.3))
            v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetNet(net); b.Add(v)
        for l, x1, y1, x2, y2 in r['segs']:
            t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(FM(x1), FM(y1))); t.SetEnd(pcbnew.VECTOR2I(FM(x2), FM(y2)))
            t.SetWidth(FM(TRACK_W)); t.SetLayer(LAYERS[l]); t.SetNet(net); b.Add(t)
    pcbnew.SaveBoard(board, b)

def gndmap(board, out):
    """Actual GND copper per layer (zone fills, pads, tracks; not inflated) + GND via positions."""
    b = pcbnew.LoadBoard(board)
    polys = []
    for z in b.Zones():
        if z.GetIsRuleArea() or z.GetNetname() != 'GND': continue
        for li, layer in LAYERS.items():
            if z.IsOnLayer(layer): polys.append({'l': li, 'p': outlines(z.GetFilledPolysList(layer))})
    vias = []
    for it in [p for f in b.GetFootprints() for p in f.Pads()] + list(b.GetTracks()):
        if it.GetNetname() != 'GND': continue
        if it.GetClass() == 'PCB_VIA':
            vias.append((T(it.GetPosition().x), T(it.GetPosition().y))); continue
        for li, layer in LAYERS.items():
            if it.IsOnLayer(layer): polys.append({'l': li, 'p': shape(it, layer, 0.0)})
    json.dump({'polys': polys, 'vias': vias}, open(out, 'w'))

if __name__ == '__main__':
    {'export': export, 'apply': apply, 'gndmap': gndmap}[sys.argv[1]](sys.argv[2], sys.argv[3])
