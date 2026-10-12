# Count DRC errors that are real after a route: ignore stale-fill zone clearances and thermal spokes.
import json, sys
d = json.load(open(sys.argv[1]))
zone = lambda v: any(('zóna' in i['description'] or 'zone' in i['description']) for i in v['items'])
bad = [v for v in d['violations'] if v['severity'] == 'error' and v['type'] != 'starved_thermal'
       and not (v['type'] in ('clearance', 'hole_clearance') and zone(v))]
print(len(bad))
for v in bad[:5]: print(v['type'], [i['description'][:50] for i in v['items']], file=sys.stderr)
