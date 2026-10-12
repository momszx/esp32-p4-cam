# v0.6 GPIO swap on PCB: U1 pad nets, J7 to top-left edge, R27/R28 pull-downs to front next to U8/U6.
import sys, pcbnew
B = sys.argv[1]
b = pcbnew.LoadBoard(B); mm = pcbnew.FromMM; T = pcbnew.ToMM
fp = {f.GetReference(): f for f in b.GetFootprints()}
newnet = {'19': 'CAM_3V3_EN', '56': 'EFUSE_FLT', '57': 'PDM_DATA', '60': 'USER_BTN', '80': 'SD_CD', '81': 'SD_EN'}
freed = {'17': 2, '20': 5, '28': 13}
for p in fp['U1'].Pads():
    n = p.GetNumber()
    if n in newnet: p.SetNet(b.FindNet(newnet[n]))
    elif n in freed:
        ni = pcbnew.NETINFO_ITEM(b, 'unconnected-(U1-GPIO%d-Pad%s)' % (freed[n], n)); b.Add(ni); p.SetNet(ni)
def pads(f): return {p.GetNumber(): (T(p.GetPosition().x), T(p.GetPosition().y)) for p in f.Pads()}
j7 = fp['J7']
for rot in (0, 90, 180, 270):
    j7.SetOrientationDegrees(rot); j7.SetPosition(pcbnew.VECTOR2I(mm(10), mm(10))); q = pads(j7)
    if abs(q['1'][0] - q['9'][0]) < 0.01 and q['1'][1] > q['9'][1]: break
j7.SetPosition(pcbnew.VECTOR2I(mm(10 + 2.0 - q['1'][0]), mm(10 + 11.2 - q['1'][1])))
for ref, x, y in (('R27', 11.0, 37.9), ('R28', 3.0, 16.0)):
    f = fp[ref]
    if f.IsFlipped(): f.Flip(f.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    f.SetOrientationDegrees(0); f.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
pcbnew.SaveBoard(B, b); print('swap ok', pads(j7)['1'], pads(fp['R27'])['1'], pads(fp['R28'])['1'])
