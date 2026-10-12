#!/bin/bash
# 4-layer completion pass: Freerouting (all existing copper locked) -> GND fan-out -> guarded signal maze -> report.
M=/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN; B=$M/ESP32-P4-CAM-MAIN.kicad_pcb
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3; CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
W=$1; mkdir -p $W; cd $M
python3 scripts/project_rules.py >/dev/null
$PY scripts/prep4.py $W/f.dsn >/dev/null 2>&1
for mp in 25 15; do (cd $W && timeout 900 java -jar ~/.kicad-mcp/freerouting.jar -de f.dsn -do f.ses -mp $mp -l en > fr.log 2>&1); [ -s $W/f.ses ] && break; done
grep "Optimization was completed" $W/fr.log | cut -c60-200
$PY - <<P 2>/dev/null | grep import
import pcbnew
b=pcbnew.LoadBoard('$B'); n0=len(b.GetTracks()); ok=pcbnew.ImportSpecctraSES(b,'$W/f.ses')
T=pcbnew.ToMM
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA':
        t.SetRemoveUnconnected(False)
        if (T(t.GetWidth(pcbnew.F_Cu))-T(t.GetDrillValue()))/2<0.1-1e-6: t.SetWidth(pcbnew.FromMM(T(t.GetDrillValue())+0.2))
pcbnew.ZONE_FILLER(b).Fill(b.Zones()); pcbnew.SaveBoard('$B',b); print('import',ok,n0,len(b.GetTracks()))
P
cd $M/scripts/maze
GRID_MARGIN=0 ./gnd_fanout.sh $W/gf 2>&1 | grep -c "^ok" | sed 's/^/gnd fanout ok: /'
NOGND=1 GRID_MARGIN=0.02 ./guarded.sh $W/g 2>&1 | grep -v swig | grep "^ok\|^errors" | sort | uniq -c
cd $M; $PY scripts/gnd_pour.py fill >/dev/null 2>&1; python3 scripts/project_rules.py >/dev/null
$CLI pcb drc --format json -o $W/final.json $B >/dev/null 2>&1
python3 -c "
import json,re
from collections import Counter
d=json.load(open('$W/final.json'))
print(Counter((v['severity'],v['type']) for v in d['violations'] if 'silk' not in v['type'] and 'lib_' not in v['type']))
sig=[re.search(r'\[([^\]]+)\]',u['items'][0]['description']).group(1) for u in d['unconnected_items']]
print('unconnected',len(sig),Counter(sig).most_common(25))"
