#!/bin/bash
# Iteratively join GND islands: single vias where possible, else rip-up around the island + maze GND link + reroute.
M=/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN; B=$M/ESP32-P4-CAM-MAIN.kicad_pcb
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3; CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
cd $M/scripts/maze
: > tried.txt  # macOS bash 3.2: no assoc arrays
for round in $(seq 1 ${1:-20}); do
  $PY kgeom.py gndmap $B gnd.json >/dev/null 2>&1; $PY kgeom.py export $B geom.json >/dev/null 2>&1
  out=$(python3 island_stitch.py geom.json gnd.json isl.json); echo "round $round: $out"
  if ! echo "$out" | grep -q "joined now 0"; then
    $PY kgeom.py apply $B isl.json >/dev/null 2>&1; $PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1; continue
  fi
  pair=""; while read -r a b; do grep -qxF "$a" tried.txt || { pair="$a $b"; break; }; done < isl.json.pairs
  [ -z "$pair" ] && { echo "no untried islands left"; break; }
  set -- $pair; echo "$1" >> tried.txt
  ax=$(echo $1 | cut -d, -f1); ay=$(echo $1 | cut -d, -f2)
  box=$(python3 -c "print(f'{$ax-2.5},{$ay-2.5},{$ax+2.5},{$ay+2.5}')")
  echo "  ripup GND $1 -> $2 box $box"
  python3 ripup.py $B GND $1 $2 $box 12 2>&1 | grep -E "GND:|NO ROUTE GND|iter .*open|FAILED" | tail -3
  $PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
done
$CLI pcb drc --format json -o drc_g.json $B >/dev/null 2>&1
python3 -c "
import json;d=json.load(open('drc_g.json'))
from collections import Counter
print(Counter((v['severity'],v['type']) for v in d['violations'] if 'silk' not in v['type'] and 'lib' not in v['type']))
print('unconnected',len(d['unconnected_items']),'nonGND',sum(1 for u in d['unconnected_items'] if '[GND]' not in u['items'][0]['description']))"
