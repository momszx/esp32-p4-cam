# Global re-route: rip all unlocked non-GND copper, then maze-route every open connection in order
# (power classes first, then signals long -> short), refreshing the ratsnest from DRC every REFRESH routes.
# Usage: route_all.py <workdir>      (board backup is the caller's job)
import json, math, os, re, subprocess, sys
PY = '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3'
CLI = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
M = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN'
B, D = M + '/ESP32-P4-CAM-MAIN.kicad_pcb', M + '/scripts/maze'
W = sys.argv[1]; os.makedirs(W, exist_ok=True)
REFRESH = 25
POWER = re.compile(r'^(VBUS|VBUS_SW|3V3_BUCK|BK_SW|IR_VIN|IR_VIN_SH|\+3V3|SD_3V3|CAM_3V3|CAM_3V3_SW)$')
run = lambda *a: subprocess.run(a, cwd=D, capture_output=True, text=True)

def rip():
    code = f'''
import pcbnew
b = pcbnew.LoadBoard({B!r})
rm = [t for t in b.GetTracks() if not t.IsLocked() and t.GetNetname() != 'GND']
for t in rm: b.Remove(t)
pcbnew.SaveBoard({B!r}, b); print('ripped', len(rm))'''
    print(run(PY, '-c', code).stdout.strip())

def opens():
    run('python3', M + '/scripts/project_rules.py')
    run(CLI, 'pcb', 'drc', '--format', 'json', '-o', W + '/ra.json', B)
    d = json.load(open(W + '/ra.json')); out = []
    for u in d['unconnected_items']:
        it = u['items']; m = re.search(r'\[([^\]]+)\]', it[0]['description'])
        if not m or m.group(1) == 'GND': continue
        def spec(i):
            ds = i['description']
            ls = '012' if ('PTH' in ds or ds.startswith('Via')) else ('0' if 'F.Cu' in ds else ('2' if 'In2' in ds else '1'))
            return f"{i['pos']['x']},{i['pos']['y']},{ls}", (i['pos']['x'], i['pos']['y'])
        (a, pa), (b, pb) = spec(it[0]), spec(it[1])
        out.append((m.group(1), a, b, math.dist(pa, pb)))
    return sorted(out, key=lambda o: (not POWER.match(o[0]), -o[3]))

def route(net, a, b):
    run(PY, 'kgeom.py', 'export', B, 'geom.json')
    r = run('python3', 'maze.py', 'geom.json', net, a, b, 'r_all.json')
    if r.returncode == 0: run(PY, 'kgeom.py', 'apply', B, 'r_all.json')
    return r.returncode == 0

rip()
failed = set()
for rnd in range(40):
    todo = [o for o in opens() if (o[0], o[1], o[2]) not in failed]
    print(f'round {rnd}: {len(todo)} open', flush=True)
    if not todo: break
    for net, a, b, dist in todo[:REFRESH]:
        ok = route(net, a, b)
        if not ok: failed.add((net, a, b))
        print(f'  {"ok" if ok else "FAIL"} {net} {dist:.1f}mm', flush=True)
print('failed', sorted({f[0] for f in failed}))
