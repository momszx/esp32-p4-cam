#!/bin/bash
# Guarded maze pass: route each open connection (signals, then GND island pairs); revert a route if it adds real DRC errors.
M=/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN; B=$M/ESP32-P4-CAM-MAIN.kicad_pcb
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3; CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
W=$1; mkdir -p $W; cd $M/scripts/maze
route_list() {
  while read -r net a b; do
    cp $B $W/pre_one.kicad_pcb
    $PY kgeom.py export $B geom.json >/dev/null 2>&1
    if python3 maze.py geom.json "$net" "$a" "$b" r.json >/dev/null 2>&1; then
      $PY kgeom.py apply $B r.json >/dev/null 2>&1
      python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/one.json $B >/dev/null 2>&1
      e=$(python3 errs.py $W/one.json 2>/dev/null)
      if [ "$e" -gt "$base" ]; then cp $W/pre_one.kicad_pcb $B; echo "reverted $net"; else echo "ok $net"; fi
    else echo "noroute $net"; fi
  done < $1
}
$PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/d.json $B >/dev/null 2>&1; base=$(python3 errs.py $W/d.json 2>/dev/null)
python3 - $W/d.json > $W/todo.txt <<'P'
import json,re,sys
d=json.load(open(sys.argv[1]))
for u in d['unconnected_items']:
    it=u['items']; m=re.search(r'\[([^\]]+)\]',it[0]['description'])
    if not m or m.group(1)=='GND': continue
    def spec(i):
        ds=i['description']; ls='01' if ('PTH' in ds or ds.startswith('Via')) else ('0' if 'F.Cu' in ds else '1')
        return f"{i['pos']['x']},{i['pos']['y']},{ls}"
    print(m.group(1), spec(it[0]), spec(it[1]))
P
route_list $W/todo.txt
[ -n "$NOGND" ] && set -- "$1" && for it in; do :; done
for it in $( [ -n "$NOGND" ] || echo 1 2 3 ); do
  $PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
  $PY kgeom.py gndmap $B gnd.json >/dev/null 2>&1; $PY kgeom.py export $B geom.json >/dev/null 2>&1
  out=$(python3 island_stitch.py geom.json gnd.json isl.json); echo "gnd $it: $out"
  if echo "$out" | grep -q "joined now 0"; then
    sed 's/^/GND /' isl.json.pairs > $W/gtodo.txt; route_list $W/gtodo.txt; break
  fi
  $PY kgeom.py apply $B isl.json >/dev/null 2>&1
done
$PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/final.json $B >/dev/null 2>&1
echo "errors $(python3 errs.py $W/final.json 2>/dev/null)"; python3 -c "
import json;d=json.load(open('$W/final.json'))
for u in d['unconnected_items']: print(' / '.join(i['description'][:40]+' @(%.1f,%.1f)'%(i['pos']['x'],i['pos']['y']) for i in u['items']))"
