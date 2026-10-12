# Rip-up-and-reroute driver. Usage: ripup.py <board> <net> <a> <b> <x0,y0,x1,y1 rip box> [max_iter]
import json, re, subprocess, sys
PY = '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3'
CLI = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
PROTECT = re.compile(r'^(VBUS|VBUS_SW|3V3_BUCK|BK_SW|IR_VIN|IR_VIN_SH|CSI_.*|USB_.*|RF_.*|GND)$')
board, net, a, b, box = sys.argv[1:6]
max_iter = int(sys.argv[6]) if len(sys.argv) > 6 else 15

def kpy(code):
    return subprocess.run([PY, '-c', code], capture_output=True, text=True).stdout

def rip(boxs, keep_net):
    x0, y0, x1, y1 = map(float, boxs.split(','))
    print(kpy(f'''
import pcbnew, re
T = pcbnew.ToMM; b = pcbnew.LoadBoard({board!r}); P = re.compile({PROTECT.pattern!r})
inb = lambda p: {x0} <= T(p.x) <= {x1} and {y0} <= T(p.y) <= {y1}
rm = [t for t in b.GetTracks() if t.GetNetname() != {keep_net!r} and not P.match(t.GetNetname())
      and (inb(t.GetPosition()) if t.GetClass() == 'PCB_VIA' else (inb(t.GetStart()) or inb(t.GetEnd())))]
for t in rm: b.Remove(t)
pcbnew.SaveBoard({board!r}, b); print('ripped', len(rm), sorted(set(t.GetNetname() for t in rm)))
''').strip())

def route(net, a, b):
    subprocess.run([PY, 'kgeom.py', 'export', board, 'geom.json'], capture_output=True)
    r = subprocess.run(['python3', 'maze.py', 'geom.json', net, a, b, 'r.json'], capture_output=True, text=True)
    print(' ', (r.stdout or r.stderr).strip().splitlines()[-1])
    if r.returncode == 0: subprocess.run([PY, 'kgeom.py', 'apply', board, 'r.json'], capture_output=True)
    return r.returncode == 0

def unconnected():
    subprocess.run(['python3', '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py'], capture_output=True)
    subprocess.run([CLI, 'pcb', 'drc', '--format', 'json', '-o', 'drc_r.json', board], capture_output=True)
    d = json.load(open('drc_r.json'))
    errs = [v for v in d['violations'] if v['severity'] == 'error']
    out = []
    for u in d['unconnected_items']:
        it = u['items']; m = re.search(r'\[([^\]]+)\]', it[0]['description'])
        if not m or m.group(1) == 'GND': continue
        def spec(i):
            ds = i['description']; ls = '01' if ('PTH' in ds or ds.startswith('Via')) else ('0' if 'F.Cu' in ds else '1')
            return f"{i['pos']['x']},{i['pos']['y']},{ls}"
        out.append((m.group(1), spec(it[0]), spec(it[1])))
    return out, errs

rip(box, net)
route(net, a, b)
failed = set()
for k in range(max_iter):
    todo, errs = unconnected()
    todo = [t for t in todo if t not in failed]
    print(f'iter {k}: {len(todo)} open, {len(errs)} DRC errors')
    if not todo: break
    n, sa, sb = todo[0]
    if not route(n, sa, sb): failed.add(todo[0])
print('FAILED', failed)
