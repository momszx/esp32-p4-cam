# CSI 2-lane routing, rev A (05 §13: one layer change per signal, symmetric via pairs).
# D0, CLK: module pads (B.Cu) -> B lanes above module -> via under J2 body -> F stub into J2 pad (from top).
# CLK P/N order fix happens at the layer change (vias at different x). D1: right-edge pads -> vias -> F lanes below J2 -> pad from bottom.
import pcbnew
BOARD='/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
W=0.3; VD,VDR=0.6,0.3
b=pcbnew.LoadBoard(BOARD); mm=pcbnew.FromMM
def net(n): return b.FindNet(n)
def track(pts,layer,n):
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        t=pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(x1),mm(y1))); t.SetEnd(pcbnew.VECTOR2I(mm(x2),mm(y2)))
        t.SetWidth(mm(W)); t.SetLayer(layer); t.SetNet(net(n)); b.Add(t)
def via(x,y,n):
    v=pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(x),mm(y))); v.SetWidth(mm(VD)); v.SetDrill(mm(VDR))
    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetNet(net(n)); b.Add(v)
F,B=pcbnew.F_Cu,pcbnew.B_Cu
# idempotent: remove previous CSI copper
for t in list(b.GetTracks()):
    if t.GetNetname().startswith('CSI_'): b.Remove(t)
# D0 (D0N has +3.8 mm U-meander on B for intra-pair match)
track([(30,12.12),(30,10.3),(28.1,10.3),(28.1,9.4),(30,9.4),(30,7.5),(28.5,7.5)],B,'CSI_D0N'); via(28.5,7.5,'CSI_D0N'); track([(28.5,7.5),(28.5,9.3)],F,'CSI_D0N')
track([(31,12.12),(31,6.6),(27.5,6.6)],B,'CSI_D0P'); via(27.5,6.6,'CSI_D0P'); track([(27.5,6.6),(27.5,9.3)],F,'CSI_D0P')
# CLK (P/N swap at layer change; CLKP has +1.8 mm bump on B)
track([(32,12.12),(32,4.5),(25.5,4.5),(25.5,5.4),(24.5,5.4),(24.5,4.5),(21.5,4.5)],B,'CSI_CLKP'); via(21.5,4.5,'CSI_CLKP'); track([(21.5,4.5),(21.5,9.3)],F,'CSI_CLKP')
track([(33,12.12),(33,3.6),(22.5,3.6)],B,'CSI_CLKN'); via(22.5,3.6,'CSI_CLKN'); track([(22.5,3.6),(22.5,9.3)],F,'CSI_CLKN')
# D1 (D1N +0.6 mm jog on F vertical for intra-pair match)
track([(35.38,14.5),(37.7,14.5)],B,'CSI_D1N'); via(37.7,14.5,'CSI_D1N'); track([(37.7,14.5),(37.7,13.5),(38.0,13.5),(38.0,12.5),(37.7,12.5),(37.7,10.9),(25.5,10.9),(25.5,9.3)],F,'CSI_D1N')
track([(35.38,15.5),(37.0,15.5)],B,'CSI_D1P'); via(37.0,15.5,'CSI_D1P'); track([(37.0,15.5),(37.0,11.45),(24.5,11.45),(24.5,9.3)],F,'CSI_D1P')
pcbnew.SaveBoard(BOARD,b)
print('CSI routed; lengths: reload board and measure')
