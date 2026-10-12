#!/bin/bash
# For every open connection: rip-up around its endpoints (bbox, capped) and reroute, then guarded pass.
M=/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN; B=$M/ESP32-P4-CAM-MAIN.kicad_pcb
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3; CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
W=$1; mkdir -p $W; cd $M/scripts/maze
$PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/d.json $B >/dev/null 2>&1
python3 - $W/d.json > $W/todo.txt <<'P'
import json,re,sys
d=json.load(open(sys.argv[1]))
for u in d['unconnected_items']:
    it=u['items']; m=re.search(r'\[([^\]]+)\]',it[0]['description'])
    if not m or m.group(1)=='GND': continue
    def spec(i):
        ds=i['description']; ls='01' if ('PTH' in ds or ds.startswith('Via')) else ('0' if 'F.Cu' in ds else '1')
        return f"{i['pos']['x']},{i['pos']['y']},{ls}"
    a,b=it[0]['pos'],it[1]['pos']
    x0,x1=sorted((a['x'],b['x'])); y0,y1=sorted((a['y'],b['y']))
    import os; m=float(os.environ.get('RIPM','2')); L=m+1   # rip margin (env RIPM), long-link half box m+1
    if x1-x0>8 or y1-y0>8: x0,x1,y0,y1=a['x']-L,a['x']+L,a['y']-L,a['y']+L   # long link: rip around its start only
    else: x0,x1,y0,y1=x0-m,x1+m,y0-m,y1+m
    print(m.group(1), spec(it[0]), spec(it[1]), f"{x0:.2f},{y0:.2f},{x1:.2f},{y1:.2f}")
P
cat $W/todo.txt
while read -r net a b box; do
  cp $B $W/pre_rip.kicad_pcb
  python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/pre.json $B >/dev/null 2>&1
  pre=$(python3 -c "import json;d=json.load(open('$W/pre.json'));print(sum(1 for u in d['unconnected_items'] if '[GND]' not in u['items'][0]['description']))")
  pre_e=$(python3 errs.py $W/pre.json 2>/dev/null)
  python3 ripup.py $B "$net" "$a" "$b" "$box" 12 >/dev/null 2>&1
  $PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
  python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/post.json $B >/dev/null 2>&1
  post=$(python3 -c "import json;d=json.load(open('$W/post.json'));print(sum(1 for u in d['unconnected_items'] if '[GND]' not in u['items'][0]['description']))")
  e=$(python3 errs.py $W/post.json 2>/dev/null)
  if [ "$post" -lt "$pre" ] && [ "$e" -le "$pre_e" ]; then echo "kept $net: $pre -> $post"; else cp $W/pre_rip.kicad_pcb $B; echo "reverted $net: $pre -> $post (err $e)"; fi
done < $W/todo.txt
