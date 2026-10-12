#!/bin/bash
# 4-layer: give every unconnected GND pad a short stub + via to the In1 GND plane (DRC-guarded).
M=/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN; B=$M/ESP32-P4-CAM-MAIN.kicad_pcb
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3; CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
W=$1; mkdir -p $W; cd $M/scripts/maze
python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/d.json $B >/dev/null 2>&1; base=$(python3 errs.py $W/d.json 2>/dev/null)
python3 - $W/d.json > $W/gpads.txt <<'P'
import json,sys
d=json.load(open(sys.argv[1])); seen=set()
for u in d['unconnected_items']:
    for i in u['items']:
        ds=i['description']
        if '[GND]' in ds and ('Forrszem' in ds or 'Pad' in ds or 'Vezetősáv' in ds or 'Track' in ds):
            k=(round(i['pos']['x'],3),round(i['pos']['y'],3))
            if k in seen: continue
            seen.add(k); print(f"{k[0]},{k[1]},{'0' if 'F.Cu' in ds else ('2' if 'In2' in ds else '1')}")
P
echo "GND pads to fan out: $(wc -l < $W/gpads.txt)"
while read -r a; do
  cp $B $W/pre.kicad_pcb
  $PY kgeom.py export $B geom.json >/dev/null 2>&1
  if python3 maze.py geom.json GND "$a" VIA r.json >/dev/null 2>&1; then
    $PY kgeom.py apply $B r.json >/dev/null 2>&1
    python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/one.json $B >/dev/null 2>&1
    e=$(python3 errs.py $W/one.json 2>/dev/null)
    if [ "$e" -gt "$base" ]; then cp $W/pre.kicad_pcb $B; echo "reverted $a"; else echo "ok $a"; fi
  else echo "noroute $a"; fi
done < $W/gpads.txt
