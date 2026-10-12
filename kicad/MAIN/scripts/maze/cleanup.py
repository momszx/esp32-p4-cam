# Remove items DRC flags as dangling (non-GND vias, track stubs) and zero-length tracks, by UUID.
# Usage: cleanup.py <board> <drc.json>   (run repeatedly with fresh DRC until it removes 0)
import json, sys, pcbnew
B, D = sys.argv[1], sys.argv[2]
d = json.load(open(D))
ids = set()
for v in d['violations']:
    if v['type'] == 'track_dangling' or (v['type'] == 'via_dangling' and '[GND]' not in v['items'][0]['description']):
        ids.add(v['items'][0]['uuid'])
    if v['type'] == 'tracks_crossing':
        for i in v['items']:
            if 'hossza 0.0000' in i['description'] or 'length 0.0000' in i['description']: ids.add(i['uuid'])
b = pcbnew.LoadBoard(B)
rm = [t for t in b.GetTracks() if t.m_Uuid.AsString() in ids or (t.GetClass() != 'PCB_VIA' and t.GetStart() == t.GetEnd())]
for t in rm: b.Remove(t)
pcbnew.SaveBoard(B, b); print('cleanup removed', len(rm))
