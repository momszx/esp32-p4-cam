# USB FS (USB-Serial-JTAG): U1 P50 DM / P51 DP -> U5 ESD inline -> J1 (B7/A7 DM, A6/B6 DP), all B.Cu, no vias on data.
# DP tie A6<->B6 behind the pads (under receptacle body, x=52.6); DM tie A7->B7 in front of pads (L stub at x=50.1).
# Idempotent for USB_DP / USB_DM copper; U5 re-placed by pad geometry (rear side mirrored).
import pcbnew
BOARD='/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
W=0.25; YDM,YDP=19.35,20.65; XE=45.5
b=pcbnew.LoadBoard(BOARD); mm=pcbnew.FromMM; T=pcbnew.ToMM
fp={f.GetReference():f for f in b.GetFootprints()}
def pads(f): return {p.GetNumber():(round(T(p.GetPosition().x),3),round(T(p.GetPosition().y),3)) for p in f.Pads()}
u5=fp['U5']
for rot in (0,90,180,270):
    u5.SetOrientationDegrees(rot); u5.SetPosition(pcbnew.VECTOR2I(mm(XE),mm(20.0)))
    p=pads(u5)
    if abs(p['1'][0]-p['2'][0])<0.01 and p['2'][1]<p['1'][1] and p['3'][0]>p['1'][0]: break
else: raise SystemExit('U5 rotation not found')
dx=XE-p['1'][0]; u5.SetPosition(pcbnew.VECTOR2I(mm(XE+dx),mm(20.0))); p=pads(u5)
def in_esd_box(t):  # ESD GND stub/via between the USB lines next to U5
    pts=[t.GetPosition()] if t.GetClass()=='PCB_VIA' else [t.GetStart(),t.GetEnd()]
    return all(46.0<=T(q.x)<=48.6 and 19.7<=T(q.y)<=20.3 for q in pts)
for t in list(b.GetTracks()):
    if t.GetNetname() in ('USB_DP','USB_DM') or (t.GetNetname()=='GND' and in_esd_box(t)): b.Remove(t)
def track(pts,n,layer=pcbnew.B_Cu,w=W):
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        t=pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(x1),mm(y1))); t.SetEnd(pcbnew.VECTOR2I(mm(x2),mm(y2)))
        t.SetWidth(mm(w)); t.SetLayer(layer); t.SetNet(b.FindNet(n)); b.Add(t)
track([(35.38,19.5),(43.5,19.5),(43.65,YDM),(47.6,YDM),(47.7,19.25),(51.45,19.25)],'USB_DM')      # P50 -> U5.2 -> J1 B7
track([(51.45,20.25),(50.1,20.25),(50.1,19.25)],'USB_DM')                                         # J1 A7 -> DM line
track([(35.38,20.5),(43.5,20.5),(43.65,YDP),(47.6,YDP),(47.7,20.75),(51.45,20.75)],'USB_DP')      # P51 -> U5.1 -> J1 B6
track([(51.45,19.75),(52.6,19.75),(52.6,20.75),(51.45,20.75)],'USB_DP')                           # J1 A6 <-> B6 behind pads
track([p['3'],(46.5,20.0)],'GND',w=0.3)
v=pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(46.5),mm(20.0))); v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3)); v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetNet(b.FindNet('GND')); b.Add(v)
pcbnew.SaveBoard(BOARD,b)
print('U5 pads',p)
