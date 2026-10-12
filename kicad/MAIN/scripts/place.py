# Netlist -> MAIN PCB: add footprints, assign nets, place per 05/06 floorplan (rev A 60x50).
import sys, pcbnew, xml.etree.ElementTree as ET
BOARD='/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb'
NET=sys.argv[1]
STD='/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/'
LIBS={'ESP32-P4-CAM':'/Users/momsz/Documents/CAD/ESP32-P4_CAM/kicad/lib/ESP32-P4-CAM.pretty'}
B,F='B','F'
# ref: (x, y, rot, side)   board coords mm, top view
P={
 # ---- REAR (module side) ----
 'J1':(56.5,20,90,B),'D1':(49,14.5,90,B),'U5':(49,25,0,B),'R1':(49,28,0,B),'C1':(52,28,0,B),
 'C20':(16,43.5,0,B),'C21':(12,43.5,0,B),'C22':(14.5,41.2,0,B),'C23':(17.5,41.2,0,B),
 'R23':(10,41.2,0,B),'C25':(10,46,0,B),'C24':(39.5,36,0,B),'R20':(39.5,32.5,0,B),
 'R21':(5,27.5,0,B),'R22':(5,26,0,B),
 'R24':(39.5,21.5,0,B),'R25':(39.5,23,0,B),'R26':(39.5,24.5,0,B),'R27':(39.5,26,0,B),'R28':(39.5,29.5,0,B),'R29':(39.5,28,0,B),
 'R30':(5,15.5,0,B),'D20':(5,13.5,0,B),'R31':(5,18,0,B),'R32':(5,19.5,0,B),
 'J4':(3,36.5,0,B),'R34':(6.5,34.5,0,B),'C27':(6.5,33,0,B),'C28':(4,33,0,B),
 'SW1':(48.5,5.5,0,B),'SW2':(55,5.5,0,B),'SW3':(56,45,0,B),'C40':(52,45.5,0,B),
 'R40':(42,33.5,0,B),'R41':(42,35,0,B),'J7':(46,47.5,90,B),
 # pogo grid 4x5, 2.0 mm
 # ---- FRONT (camera side) ----
 'U2':(51,9,0,F),'C2':(46.5,6.5,0,F),'R2':(55.5,6.5,0,F),'R3':(55.5,8,0,F),'R4':(46.5,11.5,0,F),'R5':(46.5,13,0,F),
 'JP1':(51,14,0,F),'U3':(51,18.5,0,F),'C3':(46.5,18.5,90,F),'R6':(55.5,17,0,F),'R7':(55.5,18.5,0,F),
 'R8':(55.5,20,0,F),'R9':(55.5,21.5,0,F),'C4':(48,21.5,0,F),'R10':(51,22.5,0,F),'R11':(55.5,15.5,0,F),
 'C5':(46.5,26,90,F),'C6':(50,26,90,F),'R12':(54,25,0,F),'R13':(54,26.5,0,F),'C7':(54,28,0,F),'D2':(57.5,27,90,F),
 'U4':(51,33,0,F),'C8':(46.5,31.5,90,F),'C9':(47,34,0,F),'C10':(55,35.5,0,F),'C11':(53.5,30.5,0,F),
 'L1':(51,39,0,F),'R14':(55.5,32,0,F),'R15':(55.5,33.5,0,F),'C12':(46.5,40,90,F),'C13':(46.5,43,90,F),'R16':(51,44,0,F),
 'R33':(57.5,40,90,F),'TH1':(57.5,43,90,F),'C26':(57.5,46,90,F),
 'R35':(58.5,9,90,F),'C29':(58.5,12,90,F),'D21':(58.5,15.5,90,F),'R36':(44,9,90,F),'C30':(44,12,90,F),'D22':(44,15.5,90,F),
 'J2':(26.5,5,180,F),'U6':(12,8,0,F),'C50':(9,8,90,F),'C52':(12,11,0,F),'R50':(15.5,8,0,F),'R53':(15.5,10,0,F),'C51':(18.5,8,90,F),
 'R51':(9,11.5,0,F),'R52':(9,13,0,F),
 'J5':(41.5,25,0,F),'R70':(18,10.5,0,F),
 'U7':(25,44,0,F),'R71':(28.5,44,0,F),'C70':(22,44,0,F),'R72':(25,47.5,0,F),'R73':(31,47.5,0,F),'TP8A':(19,47.5,0,F),'TP8B':(35,47.5,0,F),'C71':(31.5,44,0,F),
 'J3':(8,25,270,F),'U8':(5,14,0,F),'C60':(8,16,0,F),'R60':(3,16,0,F),'C61':(3,12,90,F),'C62':(5,36,90,F),'C63':(8,36,0,F),
 'R61':(3,38,0,F),'R62':(6,38,0,F),'R63':(9,38,0,F),'R64':(3,39.5,0,F),'R65':(6,39.5,0,F),'R66':(9,39.5,0,F),
}
tps=['TP1','TP2','TP3','TP4','TP5','TP6','TP7','TP9A','TP9B','TP10','TP11','TP12','TP13','TP14','TP15','TP16A','TP16B','TP17','TP18','TP19']
for i,t in enumerate(tps):
    P[t]=(47.5+2.0*(i%4), 31+2.0*(i//4), 0, B)

root=ET.parse(NET).getroot()
comps={c.get('ref'):c for c in root.find('components')}
pinnet={}
for n in root.find('nets'):
    for node in n.findall('node'):
        pinnet[(node.get('ref'),node.get('pin'))]=n.get('name')
b=pcbnew.LoadBoard(BOARD)
have={f.GetReference():f for f in b.GetFootprints()}
netinfo={}
def net(name):
    if name not in netinfo:
        ni=b.FindNet(name)
        if ni is None:
            ni=pcbnew.NETINFO_ITEM(b,name); b.Add(ni)
        netinfo[name]=ni
    return netinfo[name]
mm=pcbnew.FromMM
missing=[]
for ref,c in comps.items():
    if ref.startswith('#'): continue
    fpid=c.findtext('footprint') or ''
    props={p.get('name'):p.get('value') for p in c.findall('property')}
    fp=have.get(ref)
    if fp is None:
        lib,name=fpid.split(':')
        path=LIBS.get(lib, STD+lib+'.pretty')
        fp=pcbnew.FootprintLoad(path,name)
        if fp is None: missing.append((ref,fpid)); continue
        fp.SetFPID(pcbnew.LIB_ID(lib,name))
        fp.SetReference(ref); fp.SetValue(c.findtext('value') or '')
        b.Add(fp)
        x,y,rot,side=P.get(ref,(70,10+len(missing),0,F))
        if ref not in P: missing.append((ref,'NO POSITION'))
        pos=pcbnew.VECTOR2I(mm(x),mm(y)); fp.SetPosition(pos)
        if side==B: fp.Flip(pos, pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
        fp.SetOrientationDegrees(rot)
    fp.SetDNP('dnp' in props)
    if 'dnp' in props: fp.SetExcludedFromPosFiles(True); fp.SetExcludedFromBOM(True)
    for pad in fp.Pads():
        nm=pinnet.get((ref,pad.GetNumber()))
        if nm: pad.SetNet(net(nm))
pcbnew.SaveBoard(BOARD,b)
print('footprints:',len(b.GetFootprints()),'nets:',b.GetNetCount(),'missing:',missing)
