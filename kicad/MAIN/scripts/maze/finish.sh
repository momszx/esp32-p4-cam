#!/bin/bash
# region reroute (best-of-N) then GND island vias until stable, refill, report.
M=/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN; B=$M/ESP32-P4-CAM-MAIN.kicad_pcb
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3; CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
$M/scripts/maze/region_reroute.sh "$1" "$2" "$3" 2>&1 | grep -v swig/python
cd $M/scripts/maze
for it in 1 2 3 4; do
  $PY kgeom.py gndmap $B gnd.json >/dev/null 2>&1; $PY kgeom.py export $B geom.json >/dev/null 2>&1
  out=$(python3 island_stitch.py geom.json gnd.json isl.json); echo "gnd $it: $out"
  echo "$out" | grep -q "joined now 0" && break
  $PY kgeom.py apply $B isl.json >/dev/null 2>&1; $PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
done
$PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $3/final.json $B >/dev/null 2>&1
python3 errs.py $3/final.json; python3 -c "
import json;d=json.load(open('$3/final.json'))
for u in d['unconnected_items']: print(' / '.join(i['description'][:40]+' @(%.1f,%.1f)'%(i['pos']['x'],i['pos']['y']) for i in u['items']))"
