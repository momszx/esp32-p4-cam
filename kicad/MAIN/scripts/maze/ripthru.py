# Targeted rip-up-and-reroute: find the cheapest path for one connection treating unlocked foreign copper as
# passable-at-cost (maze SOFT=1), rip exactly the crossed tracks/vias, route the target (temporarily locked),
# then re-route the victims the same way (recursion depth DEPTH). Kept only if non-GND opens drop and real
# DRC errors don't rise. Usage: ripthru.py <workdir> "NET a b" ...     (env DEPTH, default 2)
import json, os, re, shutil, subprocess, sys
PY = '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3'
CLI = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
M = '/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN'
B, D = M + '/ESP32-P4-CAM-MAIN.kicad_pcb', M + '/scripts/maze'
W = sys.argv[1]; os.makedirs(W, exist_ok=True)
DEPTH = int(os.environ.get('DEPTH', '2'))
run = lambda *a, env=None: subprocess.run(a, cwd=D, capture_output=True, text=True, env=env)

def drc():
    run('python3', M + '/scripts/project_rules.py')
    run(CLI, 'pcb', 'drc', '--format', 'json', '-o', W + '/rt.json', B)
    d = json.load(open(W + '/rt.json')); ops = []
    for u in d['unconnected_items']:
        it = u['items']; m = re.search(r'\[([^\]]+)\]', it[0]['description'])
        if not m or m.group(1) == 'GND': continue
        def spec(i):
            ds = i['description']
            ls = '012' if ('PTH' in ds or ds.startswith('Via')) else ('0' if 'F.Cu' in ds else ('2' if 'In2' in ds else '1'))
            return f"{i['pos']['x']},{i['pos']['y']},{ls}"
        ops.append((m.group(1), spec(it[0]), spec(it[1])))
    return ops, int(run('python3', 'errs.py', W + '/rt.json').stdout.strip() or 0)

def pyb(body):   # run a pcbnew snippet on the board (b = board), save, return stdout
    return run(PY, '-c', f'import pcbnew\nb = pcbnew.LoadBoard({B!r})\n{body}\npcbnew.SaveBoard({B!r}, b)').stdout

def maze(net, a, b, soft=False):
    run(PY, 'kgeom.py', 'export', B, 'geom.json')
    env = dict(os.environ, SOFT='1') if soft else None
    r = run('python3', 'maze.py', 'geom.json', net, a, b, 'r_rt.json', env=env)
    return json.load(open(D + '/r_rt.json'))[0] if r.returncode == 0 else None

def apply_locked(route):   # add route, lock its new items; return their uuids
    before = set(pyb('print(" ".join(t.m_Uuid.AsString() for t in b.GetTracks()))').split())
    json.dump([route], open(D + '/r_rt.json', 'w')); run(PY, 'kgeom.py', 'apply', B, 'r_rt.json')
    new = pyb(f'''bef = set({sorted(before)!r})
new = [t for t in b.GetTracks() if t.m_Uuid.AsString() not in bef]
for t in new: t.SetLocked(True)
print(" ".join(t.m_Uuid.AsString() for t in new))''').split()
    return new

def solve(net, a, b, depth, held):
    """route net a-b, ripping soft obstacles; victims re-routed with depth-1. Adds locked uuids to held."""
    r = maze(net, a, b)
    if r: held += apply_locked(r); return True
    if depth == 0: return False
    soft = maze(net, a, b, soft=True)
    if not soft: return False
    geom = json.load(open(D + '/geom.json')); vid = set(soft['victims'])
    vnets = sorted({p['net'] for p in geom['polys'] if p.get('id') in vid})
    pyb(f'''ids = set({sorted(vid)!r})
for t in [t for t in b.GetTracks() if t.m_Uuid.AsString() in ids]: b.Remove(t)''')
    r = maze(net, a, b)
    if not r: return False
    held += apply_locked(r)
    for _ in range(2):
        todo = [o for o in drc()[0] if o[0] in vnets]
        if not todo: break
        for n, sa, sb in todo: solve(n, sa, sb, depth - 1, held)
    return True

for job in sys.argv[2:]:
    shutil.copy(B, W + '/pre.kicad_pcb')
    pre, pre_e = drc(); held = []
    if len(job.split()) == 1:   # bare net name: take its first current open from DRC
        cand = [o for o in pre if o[0] == job]
        if not cand: print(f'{job}: no open'); continue
        net, a, b = cand[0]
    else: net, a, b = job.split()
    ok = solve(net, a, b, DEPTH, held)
    pyb(f'''ids = set({sorted(held)!r})
for t in b.GetTracks():
    if t.m_Uuid.AsString() in ids: t.SetLocked(False)''')
    post, post_e = drc()
    if ok and len(post) < len(pre) and post_e <= pre_e:
        print(f'KEPT {net}: opens {len(pre)} -> {len(post)}, err {pre_e} -> {post_e}', flush=True)
    else:
        shutil.copy(W + '/pre.kicad_pcb', B)
        print(f'reverted {net}: ok={ok} opens {len(pre)} -> {len(post)}, err {pre_e} -> {post_e}', flush=True)
