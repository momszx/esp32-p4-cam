# Single source of truth for MAIN v0.6 (4-layer, JLC04101H-3313A) board rules + netclasses + patterns.
# Re-apply after anything (KiCad GUI / MCP server) may have rewritten ESP32-P4-CAM-MAIN.kicad_pro with stale settings.
import copy, json
P = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pro'
RULES = dict(min_track_width=0.09, min_through_hole_diameter=0.2, min_via_diameter=0.45, min_via_annular_width=0.1, min_clearance=0.15)
CLASSES = {  # name: (track, clearance, via_d, via_drill, diff_w, diff_gap)
    'Default':   (0.15, 0.15, 0.5, 0.25, None, None),
    'CSI_DIFF':  (0.204, 0.2, 0.6, 0.3, 0.204, 0.203),
    'USB':       (0.262, 0.2, 0.6, 0.3, 0.262, 0.203),
    'RF_50':     (0.302, 0.25, 0.6, 0.3, None, None),
    'PWR':       (0.4, 0.2, 0.6, 0.3, None, None),
    'PWR_LIGHT': (0.3, 0.2, 0.5, 0.25, None, None),
}
PATTERNS = [('PWR', n) for n in ('VBUS', 'VBUS_SW', '3V3_BUCK', 'BK_SW', 'IR_VIN', 'IR_VIN_SH')] + \
           [('PWR_LIGHT', n) for n in ('+3V3', 'SD_3V3', 'CAM_3V3', 'CAM_3V3_SW')] + \
           [('CSI_DIFF', 'CSI_*'), ('USB', 'USB_D*'), ('RF_50', 'RF*')]
d = json.load(open(P))
d['board']['design_settings']['rules'].update(RULES)
ns = d['net_settings']
base = next(c for c in ns['classes'] if c['name'] == 'Default')
by = {c['name']: c for c in ns['classes']}
for name, (tw, cl, vd, vdr, dw, dg) in CLASSES.items():
    c = by.get(name) or copy.deepcopy(base)
    c.update(name=name, track_width=tw, clearance=cl, via_diameter=vd, via_drill=vdr)
    if dw: c.update(diff_pair_width=dw, diff_pair_gap=dg)
    if name not in by: ns['classes'].append(c)
ns['netclass_patterns'] = [{'netclass': c, 'pattern': n} for c, n in PATTERNS]
json.dump(d, open(P, 'w'), indent=2)
print('project rules applied:', [(c['name'], c['track_width']) for c in ns['classes']], len(PATTERNS), 'patterns')
