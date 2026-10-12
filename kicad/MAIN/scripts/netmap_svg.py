# Net-class coloured SVG map of each copper layer (zone fills, tracks, pads, vias, rule areas) for the docs.
# usage (KiCad python): netmap_svg.py <board.kicad_pcb> <out_dir>   — refills zones in memory only, never saves the board
import sys, os, html
import pcbnew
board, out = sys.argv[1], sys.argv[2]
b = pcbnew.LoadBoard(board); T = pcbnew.ToMM
LAYERS = [('L1_F_Cu', pcbnew.F_Cu, 'L1 F.Cu (top)'), ('L2_In1_Cu', pcbnew.In1_Cu, 'L2 In1.Cu (GND plane)'),
          ('L3_In2_Cu', pcbnew.In2_Cu, 'L3 In2.Cu (power planes + GND fill)'), ('L4_B_Cu', pcbnew.B_Cu, 'L4 B.Cu (bottom, seen from top)')]
CLS = {'GND': '#56606b', 'VBUS': '#e5484d', 'VBUS_SW': '#f5a524', 'PWR': '#ff7b72', 'PWR_LIGHT': '#d2a8ff',
       'CSI_DIFF': '#3fb950', 'USB': '#58a6ff', 'RF_50': '#ff4fd8', 'Default': '#c9d1d9'}
def colour(it):
    n = it.GetNetname()
    if n in ('GND', 'VBUS', 'VBUS_SW'): return CLS[n]
    return CLS.get(str(it.GetNetClassName()), CLS['Default'])
def path(ps):
    d = []
    for i in range(ps.OutlineCount()):
        for poly in [ps.Outline(i)] + [ps.Hole(i, h) for h in range(ps.HoleCount(i))]:
            pts = [poly.CPoint(j) for j in range(poly.PointCount())]
            if pts: d.append('M' + ' L'.join(f'{T(p.x):.3f},{T(p.y):.3f}' for p in pts) + ' Z')
    return ' '.join(d)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
for name, L, title in LAYERS:
    els = []
    for z in b.Zones():
        if z.GetIsRuleArea() or not z.IsOnLayer(L): continue
        els.append(f'<path d="{path(z.GetFilledPolysList(L))}" fill="{colour(z)}" fill-opacity="0.55" fill-rule="evenodd"/>')
    for z in b.Zones():
        if z.GetIsRuleArea() and z.IsOnLayer(L):
            els.append(f'<path d="{path(z.Outline())}" fill="none" stroke="#ffffff" stroke-width="0.08" stroke-dasharray="0.4,0.3"/>')
    for t in b.GetTracks():
        if t.GetClass() == 'PCB_TRACK' and t.GetLayer() == L:
            s, e = t.GetStart(), t.GetEnd()
            els.append(f'<line x1="{T(s.x):.3f}" y1="{T(s.y):.3f}" x2="{T(e.x):.3f}" y2="{T(e.y):.3f}" stroke="{colour(t)}" stroke-width="{T(t.GetWidth()):.3f}" stroke-linecap="round"/>')
    for f in b.GetFootprints():
        for p in f.Pads():
            if not p.IsOnLayer(L): continue
            ps = pcbnew.SHAPE_POLY_SET(); p.TransformShapeToPolygon(ps, L, 0, pcbnew.FromMM(0.01), pcbnew.ERROR_INSIDE)
            els.append(f'<path d="{path(ps)}" fill="{colour(p)}"/>')
    for t in b.GetTracks():
        if t.GetClass() == 'PCB_VIA':
            c = t.GetPosition()
            els.append(f'<circle cx="{T(c.x):.3f}" cy="{T(c.y):.3f}" r="{T(t.GetWidth(L))/2:.3f}" fill="{colour(t)}" stroke="#ffffff" stroke-width="0.03"/><circle cx="{T(c.x):.3f}" cy="{T(c.y):.3f}" r="{T(t.GetDrillValue())/2:.3f}" fill="#101418"/>')
    bb = b.GetBoardEdgesBoundingBox(); x0, y0, w, h = T(bb.GetLeft()), T(bb.GetTop()), T(bb.GetWidth()), T(bb.GetHeight())
    legend = [('GND', CLS['GND']), ('VBUS', CLS['VBUS']), ('VBUS_SW', CLS['VBUS_SW']), ('PWR (3V3_BUCK, BK_SW, IR)', CLS['PWR']),
              ('PWR_LIGHT (+3V3, CAM/SD 3V3)', CLS['PWR_LIGHT']), ('CSI diff pairs', CLS['CSI_DIFF']), ('USB', CLS['USB']), ('RF 50 ohm', CLS['RF_50']), ('other signals', CLS['Default'])]
    lg = ''.join(f'<rect x="{x0 + w + 2}" y="{y0 + 4 + i * 2.6}" width="1.8" height="1.8" fill="{c}"/><text x="{x0 + w + 4.4}" y="{y0 + 5.5 + i * 2.6}" font-size="1.5" fill="#e6edf3" font-family="Helvetica">{html.escape(t)}</text>' for i, (t, c) in enumerate(legend))
    lg += f'<line x1="{x0 + w + 2}" y1="{y0 + 4 + len(legend) * 2.6 + 0.9}" x2="{x0 + w + 3.8}" y2="{y0 + 4 + len(legend) * 2.6 + 0.9}" stroke="#fff" stroke-width="0.12" stroke-dasharray="0.4,0.3"/><text x="{x0 + w + 4.4}" y="{y0 + 5.5 + len(legend) * 2.6}" font-size="1.5" fill="#e6edf3" font-family="Helvetica">rule area / keep-out</text>'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - 1} {y0 - 4} {w + 30} {h + 5}" width="{(w + 31) * 30:.0f}" height="{(h + 5) * 30:.0f}">'
           f'<rect x="{x0 - 1}" y="{y0 - 4}" width="{w + 30}" height="{h + 5}" fill="#101418"/>'
           f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="1" fill="#0b2e1f" stroke="#e3b341" stroke-width="0.15"/>'
           f'<text x="{x0}" y="{y0 - 1.2}" font-size="2" fill="#e6edf3" font-family="Helvetica">ESP32-P4-CAM MAIN rev A — {html.escape(title)}</text>'
           + ''.join(els) + lg + '</svg>')
    open(os.path.join(out, f'netmap_{name}.svg'), 'w').write(svg)
    print('wrote', name, len(els))
