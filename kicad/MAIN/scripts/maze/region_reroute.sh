#!/bin/bash
# Region rip-up + Freerouting + maze leftovers + cleanup; keeps the best of N attempts.
# Usage: region_reroute.sh <x0,y0,x1,y1> <attempts> <workdir>
set -u
M=/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN; B=$M/ESP32-P4-CAM-MAIN.kicad_pcb
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3; CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
BOX=$1; N=$2; W=$3; mkdir -p $W; cp $B $W/start.kicad_pcb
nopen() { python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/d.json $B >/dev/null 2>&1; python3 -c "
import json,re;d=json.load(open('$W/d.json'))
e=sum(1 for v in d['violations'] if v['severity']=='error' and v['type']!='starved_thermal')
n=sum(1 for u in d['unconnected_items'] if '[GND]' not in u['items'][0]['description'])
print(n+100*e)"; }
best=999
for a in $(seq 1 $N); do
  cp $W/start.kicad_pcb $B
  $PY - <<P 2>/dev/null | grep ripped
import pcbnew, re
T=pcbnew.ToMM; b=pcbnew.LoadBoard('$B'); x0,y0,x1,y1=map(float,'$BOX'.split(','))
P=re.compile(r'^(VBUS|VBUS_SW|3V3_BUCK|BK_SW|IR_VIN|IR_VIN_SH|CSI_.*|USB_.*|RF_.*|GND)$')
inb=lambda p: x0<=T(p.x)<=x1 and y0<=T(p.y)<=y1
tr=list(b.GetTracks())
rm=[t for t in tr if not P.match(t.GetNetname()) and (inb(t.GetPosition()) if t.GetClass()=='PCB_VIA' else (inb(t.GetStart()) or inb(t.GetEnd())))]
for t in rm: b.Remove(t)
pcbnew.SaveBoard('$B',b); print('ripped',len(rm))
P
  $PY $M/scripts/autoroute_prep.py $W/r.dsn >/dev/null 2>&1
  for mp in 20 15 12; do
    (cd $W && timeout 400 java -jar ~/.kicad-mcp/freerouting.jar -de r.dsn -do r.ses -mp $mp -l en > fr.log 2>&1)
    [ -s $W/r.ses ] && break
  done
  $PY -c "
import pcbnew; b=pcbnew.LoadBoard('$B'); print('ses', pcbnew.ImportSpecctraSES(b,'$W/r.ses')); pcbnew.SaveBoard('$B',b)" 2>/dev/null | grep ses
  # maze leftovers (one pass) + cleanup
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
    print(m.group(1), spec(it[0]), spec(it[1]))
P
  while read -r net sa sb; do
    (cd $M/scripts/maze && $PY kgeom.py export $B geom.json >/dev/null 2>&1 && python3 maze.py geom.json "$net" "$sa" "$sb" r.json >/dev/null 2>&1 && $PY kgeom.py apply $B r.json >/dev/null 2>&1)
  done < $W/todo.txt
  $PY $M/scripts/gnd_pour.py fill >/dev/null 2>&1
  for i in 1 2 3 4 5 6; do
    python3 /Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/scripts/project_rules.py >/dev/null; $CLI pcb drc --format json -o $W/c.json $B >/dev/null 2>&1
    out=$($PY $M/scripts/maze/cleanup.py $B $W/c.json 2>/dev/null | grep cleanup); [ "$out" = "cleanup removed 0" ] && break
  done
  s=$(nopen); echo "attempt $a score $s (open + 100*errors)"
  if [ "$s" -lt "$best" ]; then best=$s; cp $B $W/best.kicad_pcb; fi
  [ "$best" -eq 0 ] && break
done
s0=$(cp $W/start.kicad_pcb $B; nopen); if [ "$best" -lt "$s0" ]; then cp $W/best.kicad_pcb $B; else cp $W/start.kicad_pcb $B; best=$s0; fi; echo "BEST $best (start $s0)"
