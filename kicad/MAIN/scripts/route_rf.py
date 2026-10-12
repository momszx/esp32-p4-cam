# RF: U1 P2 (LNA_OUT) -> C27 shunt (DNP) -> R34 0R series -> C28 shunt (DNP) along y=34.5 on B.Cu,
# then one 90-deg bend down into J4 u.FL (rotated, center pin facing up; trace never runs under the u.FL body).
# Rotations chosen by actual pad geometry (rear side is mirrored). Idempotent for RF nets.
import pcbnew
BOARD='/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
Y=34.5; W=0.7
b=pcbnew.LoadBoard(BOARD); mm=pcbnew.FromMM; T=pcbnew.ToMM
fp={f.GetReference():f for f in b.GetFootprints()}
def pads(f): return {p.GetNumber():(T(p.GetPosition().x),T(p.GetPosition().y)) for p in f.Pads()}
def place(ref,x,y,ok):
    f=fp[ref]
    for rot in (0,90,180,270):
        f.SetPosition(pcbnew.VECTOR2I(mm(x),mm(y))); f.SetOrientationDegrees(rot)
        if ok(pads(f)): return rot
    raise SystemExit(ref+': no rotation fits')
r={}
JX,JPIN=3.0,36.3
r['J4']=place('J4',JX,JPIN+1.52,lambda p: abs(p['1'][0]-JX)<0.01 and p['1'][1]<JPIN+1.0)
r['C27']=place('C27',7.7,Y-0.48,lambda p: abs(p['1'][1]-Y)<0.05 and p['2'][1]<Y)
r['R34']=place('R34',6.0,Y,lambda p: p['1'][0]>p['2'][0] and abs(p['1'][1]-Y)<0.01)
r['C28']=place('C28',4.4,Y-0.48,lambda p: abs(p['1'][1]-Y)<0.05 and p['2'][1]<Y)
P=pads(fp['R34']); J=pads(fp['J4'])   # read pads BEFORE removing tracks (swig invalidation)
for t in list(b.GetTracks()):
    if t.GetNetname() in ('RF_ANT','RF_UFL'): b.Remove(t)
def track(pts,n):
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        t=pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(x1),mm(y1))); t.SetEnd(pcbnew.VECTOR2I(mm(x2),mm(y2)))
        t.SetWidth(mm(W)); t.SetLayer(pcbnew.B_Cu); t.SetNet(b.FindNet(n)); b.Add(t)
track([(9.62,Y),(P['1'][0],Y)],'RF_ANT')                              # P2 -> R34 pad1 (through C27 pad1)
track([(P['2'][0],Y),(J['1'][0],Y),(J['1'][0],J['1'][1])],'RF_UFL')   # R34 pad2 -> C28 pad1 -> bend -> J4 pin
pcbnew.SaveBoard(BOARD,b)
print('rotations',r,'R34',P,'J4 pin',J['1'])
