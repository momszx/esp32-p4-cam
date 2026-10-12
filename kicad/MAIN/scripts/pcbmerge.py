# Text-level 3-way merge for .kicad_pcb files (KiCad 10, net names inline).
#   diff  <base> <mod> <delta.json>     top-level items keyed by uuid (or head#n), zone fills ignored
#   apply <master> <delta.json> [...]   applies deltas; refuses an item whose master text differs from the delta's base
# All boards must be saved by the same pcbnew version (load+save once to normalise) so unchanged items are byte-identical.
import hashlib, json, re, sys

def children(text):
    """[(start, end_exclusive)] of the root's direct children."""
    out, depth, i, n, start, instr = [], 0, 0, len(text), None, False
    while i < n:
        c = text[i]
        if instr:
            if c == '\\': i += 1
            elif c == '"': instr = False
        elif c == '"': instr = True
        elif c == '(':
            depth += 1
            if depth == 2: start = i
        elif c == ')':
            if depth == 2: out.append((start, i + 1))
            depth -= 1
        i += 1
    return out

def head(item):
    return re.match(r'\(\s*([^\s()"]+)', item).group(1)

def uuid_of(item):
    depth, instr, i = 0, False, 0
    while i < len(item):
        c = item[i]
        if instr:
            if c == '\\': i += 1
            elif c == '"': instr = False
        elif c == '"': instr = True
        elif c == '(':
            depth += 1
            if depth == 2 and item.startswith('(uuid', i): return re.match(r'\(uuid\s+"?([^")\s]+)', item[i:]).group(1)
        elif c == ')': depth -= 1
        i += 1
    return None

FILL = re.compile(r'\n(\t*)\(filled_polygon\b.*?\n\1\)(?=\n)', re.S)  # closing paren at the same indent as the opener
def norm(item):
    return FILL.sub('', item) if item.startswith('(zone') else item

def items(text):
    res, seen = {}, {}
    for s, e in children(text):
        it = text[s:e]
        u = uuid_of(it)
        if u: k = 'uuid:' + u
        else:
            hd = head(it); seen[hd] = seen.get(hd, 0) + 1; k = f'{hd}#{seen[hd]}'
        res[k] = (s, e, it)
    return res

def h(t): return hashlib.sha1(norm(t).encode()).hexdigest()

def diff(base, mod, out=None):
    A, B = items(open(base).read()), items(open(mod).read())
    d = {'removed': {k: h(A[k][2]) for k in A if k not in B},
         'added': {k: B[k][2] for k in B if k not in A},
         'changed': {k: {'base': h(A[k][2]), 'text': B[k][2]} for k in A if k in B and norm(A[k][2]) != norm(B[k][2])}}
    if out:
        json.dump(d, open(out, 'w'))
        print(f"{out}: removed {len(d['removed'])}, added {len(d['added'])}, changed {len(d['changed'])}")
    return d

def apply(master, deltas):
    text = open(master).read()
    M = items(text)
    touched, edits, adds, conflicts = set(), [], [], []
    for path in deltas:
        d = json.load(open(path))
        for k, bh in d['removed'].items():
            if k not in M or k in touched or h(M[k][2]) != bh: conflicts.append((path, 'removed', k)); continue
            edits.append((M[k][0], M[k][1], '')); touched.add(k)
        for k, c in d['changed'].items():
            if k not in M or k in touched or h(M[k][2]) != c['base']: conflicts.append((path, 'changed', k)); continue
            edits.append((M[k][0], M[k][1], c['text'])); touched.add(k)
        for k, t in d['added'].items():
            if k in M or k in touched: conflicts.append((path, 'added', k)); continue
            adds.append(t); touched.add(k)
    if conflicts:
        for c in conflicts: print('CONFLICT', *c)
        sys.exit(1)
    for s, e, t in sorted(edits, reverse=True):
        if t == '':  # drop the item together with its leading newline + indent
            while s > 0 and text[s - 1] == '\t': s -= 1
            if s > 0 and text[s - 1] == '\n': s -= 1
        text = text[:s] + t + text[e:]
    end = text.rstrip().rfind(')')
    text = text[:end] + ''.join('\t' + t + '\n' for t in adds) + text[end:]
    open(master, 'w').write(text)
    print(f'applied {len(deltas)} delta(s): {len(edits)} edits, {len(adds)} adds')

def selftest():
    t = ('(kicad_pcb\n\t(version 1)\n\t(segment\n\t\t(start 0 0)\n\t\t(uuid "a")\n\t)\n\t(zone\n\t\t(uuid "z")\n'
         '\t\t(filled_polygon\n\t\t\t(layer "F.Cu")\n\t\t\t(pts\n\t\t\t\t(xy 0 0)\n\t\t\t)\n\t\t)\n'
         '\t\t(filled_polygon\n\t\t\t(pts\n\t\t\t\t(xy 1 1)\n\t\t\t)\n\t\t)\n\t)\n)\n')
    I = items(t)
    assert set(I) == {'version#1', 'uuid:a', 'uuid:z'}, I
    assert norm(I['uuid:z'][2]) == '(zone\n\t\t(uuid "z")\n\t)', repr(norm(I['uuid:z'][2]))
    print('selftest ok')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'test'
    if cmd == 'diff': diff(*sys.argv[2:5])
    elif cmd == 'apply': apply(sys.argv[2], sys.argv[3:])
    else: selftest()
