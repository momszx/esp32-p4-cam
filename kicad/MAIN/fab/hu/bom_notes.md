# MAIN rev A – BOM / alkatrész-választás (G4), 2. javítókör

Dátum: 2026-10-11 · Forrás: a mester séma (`kicad/MAIN/*.kicad_sch`, csak olvasva) és a NYÁK footprintjei (`pcbnew.LoadBoard`, csak olvasva) · Készlet, ár és Basic/Extended besorolás: **JLCPCB parts library + LCSC, böngészővel ellenőrizve 2026-10-11** (a készlet napról napra változik, rendelés előtt frissíteni kell).
Kimenetek: `bom_jlc.csv` (JLC assembly BOM), `parts.json` (hivatkozásonkénti adat), `fields_apply.py` (LCSC / MPN / Manufacturer mezők a sémába és a NYÁK-ra), `work/make_bom.py` (a CSV és a JSON generátora, benne a teljes alkatrész-tábla).

## 1. Összesítés

| | |
|---|---|
| Beültetett tételek (CPL-sorok) | **72** = a mesterben lévő 71 FIT (U1, TP-k, JP1, MH1–4 nélkül) **+ az új C14** |
| Egyedi alkatrész (BOM-sor) | **40**: **16 Basic** (45 beültetés), **24 Extended** (27 beültetés) |
| Extended beállítási díj | 24 × ~3 USD ≈ **72 USD / rendelés** (a JLC aktuális díjtábláját rendeléskor ellenőrizni) |
| Alkatrész-költség / lap | ≈ **8,80 USD** (1+ egységár, U1 modul nélkül); a legdrágább: J2 2,21 · U3 1,28 · U4 1,15 · U2 0,45 · U6 0,40 |
| Beültetési oldal | F: 47 (C14-gyel), **B: 25** (C4 a B oldalra került; C20–C25, C40, D1, D20, J1, J4, R11, R20–R23, R30, R34, R40, R41, R70, SW1–3) → **kétoldalas = JLC Standard PCBA** (az Economic csak egyoldalas) |
| Kizárva (a NYÁK-on már xb/xp) | U1 (kézi forrasztás, a tulajdonos veszi), TP1–TP19, JP1, MH1–4, minden DNP |

A meglévő értékek (UVLO 4,40/4,00 V, OVLO 10,87 V, ILIM 2,03 A, FB 3,328 V, SS 1,45 ms – 7. kör review) **változatlanok**: az E96-os ellenállásokra a pontos értékű UNI-ROYAL 1 %-os Extended tételek kerültek.

## 2. Kockázatos / kevés készletű / nem teljesen megfelelő tételek

| Ref | Választás | Gond | Teendő |
|---|---|---|---|
| **J2** | TE 1-84953-5, **C5164008** | csak **31 db** JLC-készlet, 2,21 USD | rendelés előtt foglalni / előrendelni; kontakt-oldal (Q6) lásd 3. pont |
| **R6** 267k | UNI-ROYAL 0603WAF2673T5E, **C22963** | csak **180 db**; más gyártó 267k 0603 nincs készleten | időben rendelni; vész-tartalék: más E96 páros (UVLO újraszámolás kell) |
| **U3** | TPS259470ARPWR, **C3662799** | csak **331 db** | foglalni |
| **U5** | TECH PUBLIC TPD2E2U06DCKR-TP, **C5350871** (9175 db) | az eredeti TI TPD2E2U06DCKR (C1855726) **1 db**-os készleten → lábkompatibilis második forrás; a lábkiosztás (1 IO1, 2 IO2, 3 GND) **ellenőrizve** az LCSC termékoldal pinout-ábráján (2026-10-11), egyezik a TI-vel | tulajdonos: második forrás elfogadása, vagy TI eredeti globális beszerzésből |
| **D20** | KENTO KT-0603G, **C12624** | a korábbi favorit Everlight C72043 már csak 1 db; zöld InGaN Vf ≈ 2,8–3,1 V → R30 = 1k-val 3V3-ról ≈ 0,3–0,5 mA (halvány, de látható) | ha fényesebb kell: R30 csökkentése (pl. 330 Ω) vagy sárgászöld AlGaInP LED |
| **C1** | YAGEO CC0603KRX7RABB472, **C596328**, 4,7 nF **200 V** X7R 0603 | **≥250 V 0603-ban nincs készleten** (Walsin C3880764, CCTC C5375795, Knowles, Venkel: mind 0 db); 1 kV 4,7 nF csak 1206-tól (FH 1206B472K102NT C9192, 86 435 db) | 200 V-tal megy; 1 kV-hoz a C1 lábképet 1206-ra kell cserélni (layout-feladat) |
| **J5** | Hong Cheng HC-PZ127-7.2L-2x10PS, **C41375929** | **7,00 mm-es párosított magasságú pár nem található**; a land pattern nincs adatlappal ellenőrizve | tulajdonosi döntés (Q17), lásd 5. pont |
| **L1** | Taiyo NRS5024T2R2NMGJ, **C222926** | a Taiyo-rajz szerinti land pattern nincs összevetve a KiCad `L_Taiyo-Yuden_NR-50xx` lábképpel (ugyanaz a 4,9×4,9-es NR/NRS család) | a Taiyo NRS5024 katalógus-rajzával ellenőrizni |

## 3. J2 – 15 pólusú 1,0 mm FPC: döntési táblázat

A NYÁK lábképe: `Connector_FFC-FPC:TE_1-84953-5_1x15-1MP_P1.0mm_Horizontal`. A „land pattern egyezés” oszlop a KiCad gyári lábképeinek padonkénti összevetése (pozíció és méret, KiCad python).

| Alkatrész | LCSC | JLC készlet | Land pattern a jelenlegi J2-höz | Kontakt-oldal (leírás szerint) | Megjegyzés |
|---|---|---|---|---|---|
| **TE 1-84953-5** | **C5164008** | **31** | **azonos** (ez maga a lábkép) | **TOP** (TE/JLC: „Top Contact”; KiCad: „15 top-side contacts”) | **választott**; csúszózáras (slide lock), SMT, fekvő |
| TE 1-84952-5 | C3170098 | 1 | **azonos** (KiCad `TE_1-84952-5…` padjai 1:1 egyeznek) | **BOTTOM** (TE/JLC: „Bottom Contact”) | ugyanaz a ház alsó érintkezővel; most gyakorlatilag nem rendelhető |
| JUSHUO AFA07-S15FCA-00 | C262721 | 5507 | **ELTÉR** (jelpadok y = −3,375 / 0,6×1,8 mm a −1,8 / 0,61×2,0 mm helyett) | BOTTOM | csak lábkép-cserével (`JUSHUO_AFA07-S15FCA-00…`, KiCad gyári); 2,5 mm magas |

Kínai, a TE 84953-mal **padonként azonos** lábképű 15 pólusú 1,0 mm-es csatlakozót nem találtam (a talált kínai 1,0 mm-es ZIF típusok, pl. BOOMELE H2.5, JUSHUO AFA07, más padgeometriájúak).

**Mit jelent a kontakt-oldal (Q6, G3):** TOP-contact J2-ben az FFC fém érintkezőinek **felfelé (a NYÁK-tól elfelé)** kell nézniük, BOTTOM-contactban lefelé. Ha a kamera felől érkező kábel (A típus = azonos oldali / B típus = ellentétes oldali érintkezők, plusz a hajtás iránya) a MAIN-nél rossz oldalra néz, a kábelt csak megfordítva lehet bedugni → 1↔15 tükrözés → **3V3/GND csere a kameránál**. A J2 pin ↔ háló térképe nem változik, csak a kábel / csatlakozó-oldal választásán múlik. A végleges kábel és kameramodul kezébe vételekor kell eldönteni: TE 1-84953-5 (top) marad, vagy 1-84952-5 (bottom, azonos lábkép, de most nincs készleten), vagy fordított típusú FFC.

## 4. L1 – buck induktor

**Taiyo Yuden NRS5024T2R2NMGJ (C222926)**: 2,2 µH ±30 %, **Isat 4,1 A**, Irms 3,1 A, DCR 29 mΩ, 4,9×4,9×**2,4 mm** (≤3,3 mm a kamera alatt ✓), JLC 1136 db, 0,24 USD.
- A TPS62933F RT = GND → 1,2 MHz; ΔIL = 3,3·(1 − 3,3/9,45)/(2,2 µH · 1,2 MHz) ≈ 0,81 A → 2 A terhelésnél Ipeak ≈ 2,4 A < 4,1 A ✓. A követelmény (Isat ≥ 3,5 A) teljesül; az adatlap „ideálisan Isat ≥ IHS_LIMIT (max 5,8 A)” ajánlását egy 5×5-ös alkatrész sem teljesíti (a zárlati áramkorlát így is véd).
- Alternatívák: Taiyo LCXND5050WDL2R2NMG (C5379987, azonos adatok, 195 db); NRS5030T2R2NMGJ (3,0 mm, Isat 4,2 A, csak 6 db); **NRS5020T2R2NMGJ nem jó** (Isat 2,9 A); NR5040 (4,0 mm) **tilos** (mech-09: nem fér a kamera alá).

## 5. J5 – B2B 2×10, 1,27 mm (MAIN oldal) + párja

A cél 7,0 mm párosított magasság (a befagyasztott M2 távtartókkal). **Kész, adatlap szerint 7,00 mm-es pár nincs** a kínálatban:

| Változat | MAIN (dugó) | FRONT (aljzat) | Teljes illesztési magasság | 7,0 mm-es résnél | Beszerzés |
|---|---|---|---|---|---|
| **A – BOM-ba írt (JLC-n beültethető)** | Hong Cheng **HC-PZ127-7.2L-2x10PS C41375929** (szigetelő 1,0 mm, tüske 4,0 mm) | Hong Cheng **HC-PM127-4.3H-2x10PS C27985222** (4,3 mm) | 5,3 mm | a tüske ~**2,3 mm**-t merül az aljzatba (±0,3 mm tűréssel 2,0–2,6) – az érintkezési mélység **NEM ELLENŐRZÖTT** | 1809 / 907 db |
| A′ | BOOMELE 1.27-2*10P C59981 (1,5 / 3,0 mm) | Kinghelm KH-1.27FH-2X10P-H4.3-SMT C2938399 | 5,8 mm | ~1,8 mm merülés (gyengébb) | 5458 / 2471 db |
| **B – adatlap szerinti pár** | Samtec **FTSH-110-02-x-DV(-A)** | Samtec **FLE-110-01-G-DV(-A)** | **7,47 mm** (samtec.com „Full Mated Sets”) | 7,0 mm-es távtartóval **nem ül fel** → **7,5 mm-es távtartó** kell | JLC: FTSH-110-02-L-DV C6950077 2 db, FLE-110-01-G-DV-A C3322884 17 db → Samtec / disztribútor |
| C | Samtec TFM-110-02-L-D(-A) | Samtec SFM-110-02-L-D(-A) | 6,35 mm (8,13 mm a TFM-…-12-vel) | 0,65 mm-rel alul ül | JLC-n alig van |

Javaslat: rev A bring-uphoz (a stack csak stabil kép után zár, K-7) az **A változat** elég; ha a zárt stack mechanikailag is számít, a **B (Samtec 7,47 mm + 7,5 mm távtartó)** a tiszta megoldás – ehhez a J5 lábképet a Samtec FTSH-…-DV ajánlott padképére kell cserélni, és a `-A` (vezetőcsap) változathoz furatok kellenek. Egyik változat land patternje sincs a KiCad generikus `PinHeader_2x10_P1.27mm_Vertical_SMD` (padok 2,4×0,74 mm, x = ±1,95 mm) lábképpel adatlapon összevetve. **A FRONT oldali aljzat lábképe tükrözött** (KiCad `PinSocket_2x10…`: pin 1 a +x oldalon) – a FRONT tervezésénél figyelni.

## 6. C1 – USB-C shield kondenzátor

YAGEO CC0603KRX7RABB472 (**C596328**), 4,7 nF **200 V** X7R ±10 % 0603, 10 996 db. A kért ≥250 V (ideálisan 1 kV) **0603-ban nem kapható készletről**; 1 kV-hoz 1206-os lábkép kellene (FH 1206B472K102NT C9192 vagy YAGEO CC1206KKX7RCBB472 C107198). A séma értéke („4.7nF 50V”) frissíthető „4.7nF 200V”-ra.

## 7. Egyéb választások röviden

- **C14 (új, VBUS_SW → GND az U3 kimenetén)**: Samsung CL10B105KA8NNNC (**C29936**), 1 µF 25 V **X7R** 0603, Extended. Basic tartalék: C15849 (1 µF 50 V X5R) – megspórolja a 3 USD-t.
- **C5/C6** 22 µF 25 V 1210: Samsung CL32A226KAJNNNE (C52306, X5R). X7R alternatíva: Murata GRM32ER71E226KE15L (C21397). A 07 #9 „35–50 V” szabálytól a séma szerinti 25 V-tal tér el (a 10,87 V-os OVLO mellett elfogadott).
- **C20** 47 µF: Murata GRM32ER61C476KE15L (C77101) **16 V** X5R – a 10 V-os értéknél jobb DC-bias tartalék.
- **C12/C13** 22 µF és **C8/C21** 10 µF: Basic 25 V-os 0805 (C45783, C15850).
- **D1** SMAJ10A: Diodes SMAJ10A-13-F (C134939); alternatíva Littelfuse C148210. A pad 1 = katód = VBUS – a JLC CPL-előnézetben a polaritást ellenőrizni.
- **TH1** NTC 10k: KUU KNTC0603/10KF3950 (C2892547); az LCSC 3987 K-t ír (B25/85), a típusnév B3950 (B25/50) – FW-kalibráció a G5b-n.
- **J1** HRO TYPE-C-31-M-12 (C165948), **J4** Hirose U.FL-R-SMT-1(80) (C88374), **SW1–3** Omron B3U-1000P (C231329, a 07 #29 döntés szerint), **U2** CH224A (C42459160), **U4** TPS62933FDRLR (C5219272), **U6** TPS22917DBVR (C2681320).

## 8. Ha csökkenteni kell az Extended díjat (opcionális, nem javasolt most)

C14 → C15849 (−1), C1 → C53987 50 V Basic (−1, de az ESD-tartalék csökken), az 5 db E96 ellenállás (R6, R8, R10, R13, R14) Basic értékekre cserélése csak újraszámolással (UVLO/OVLO/ILIM/FB/VBUS_MON), ami a 7. kör ellenőrzött értékeit érintené (−5). Az NTC-re, a csatlakozókra és az IC-kre nincs Basic alternatíva.

## 9. `fields_apply.py` – mezők a sémába és a NYÁK-ra

Használat: `python3 fields_apply.py <séma könyvtár> <board.kicad_pcb> [--parts parts.json] [--dry-run]` (sima python3 elég, pcbnew nem kell). Minden FIT szimbólum és a megfelelő footprint kap rejtett **LCSC / MPN / Manufacturer** mezőt (a saját „Datasheet” property-blokkjuk klónja, a NYÁK-on új uuid-dal). Idempotens; DNP elemhez nem nyúl; a hiányzó hivatkozásokat kiírja.

Teszt a mester másolatán (`test/kicad/`):
- 71/71 szimbólum és footprint megkapta a 3 mezőt (213 + 213); C14 „NOT FOUND” (még nincs a mesterben – várt).
- `kicad-cli sch erc`: **0** (előtte is 0). `drc.py`: errors **7** courtyards_overlap, unconnected **12**, parity **4 extra_footprint** (MH1–4) – **pontosan a kiinduló állapot**.
- pcbnew-vel betöltve mind a 71 footprintnél jó és rejtett a 3 mező; a pcbnew-újramentés **bájtra azonos** a szkript kimenetével (nincs formátum-eltérés). A `kicad-cli sch export bom` LCSC-re csoportosítva 39 sort ad, mind egyezik a `parts.json`-nal.
- **Fontos:** a KiCad 10 paritás-ellenőrzés jelzi az eltérő mezőket (`footprint_symbol_field_mismatch`, próbával igazolva) → a szkriptet **mindig a sémára és a NYÁK-ra együtt** kell futtatni, és **a régiós változtatások összefésülése után** (a mezők módosítják a footprint-blokkokat, ami uuid-alapú merge-ben ütközne más ágensek mozgatásaival). A C14-et előbb sémába és NYÁK-ra is fel kell venni.

## 10. A tulajdonosnak még meg kell erősítenie

1. **J2 kontakt-oldal (Q6)** a valódi kameramodul + FFC alapján (TOP = jelenlegi TE 1-84953-5); a 31 db-os készlet foglalása.
2. **J5 párosítás (Q17)**: A (JLC-s Hong Cheng pár, ~2,3 mm merülés 7 mm-nél, nem ellenőrzött) vagy B (Samtec 7,47 mm + 7,5 mm-es távtartó + lábkép-csere).
3. **U5** második forrás (TECH PUBLIC) elfogadása vagy TI eredeti beszerzése.
4. **C1** 200 V-os 0603 elfogadása (vagy 1206-os lábkép az 1 kV-hoz).
5. **L1** land pattern a Taiyo NRS5024 rajzával; **D20** fényerő (R30 értéke).
6. Rendelés előtt a készletek frissítése (J2 31, R6 180, U3 331), a JLC CPL-előnézetben a forgatások és polaritások (D1, D20, U2–U6, J1, J2, J4) ellenőrzése, kétoldalas Standard PCBA, U1 + MH + TP kizárva.
