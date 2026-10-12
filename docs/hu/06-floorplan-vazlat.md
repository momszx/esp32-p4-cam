# 06 – Floorplan vázlat: terület- és magasságköltségvetés (v0.3; as-built kiegészítés 2026-10-10, végső rev A as-built 2026-10-11)

Dátum: 2026-10-09 · Státusz: **tervezői vázlat, review-célra** · Alap: `05-architektura.md` **v0.5** (Rev A terv: §0), `07-bom-terv.md`, `90-review-log.md`
Jelölés: **[F]** = feltételezés (nem mért, nem primer forrásból) – a Q5 (kamera modul) és a Waveshare footprint/STEP után felülvizsgálandó. Minden méret mm. Hivatkozás-előtag: **06-Kn** = e dokumentum Kn konfliktusa, **00-Kn** = követelmény.
Változás v0.1 → v0.2: **G = 7,0 mm** (a Z-összegek újraszámolva, kamera alatti limit **3,3 mm**); ESD = 3,3 V array; CC-tap = 100k + 10 nF + Zener (DNP rev A); TP8 a MAIN front oldalán; a költségvetés kiegészítve (IR eFuse #2 + shunt, CAM_3V3 switch, supervisor, USER gomb, NTC, VBUS osztó, DNP header, bypass-ok); eFuse bulk 35–50 V; PDM soros R a FRONT-ra került; modul 3V3 bulk egy érték; TP1–TP17; FFC 25–30 mm; lencse-kivágás indoklás javítva; modul-lábnyom 28×28 (K-10); új K14 (CSI pad-sorrend), K15 (lapméret).
> ⚠️ **Felülírva (as-built, 2026-10-10):** a §0–§6 a **60×50 mm / 2 rétegű** rev A tervre és egy szimmetrikus 45×45-ös „magra” épül – ez **elavult**. A MAIN v0.6 **45×45 mm, 4 réteg**; az M2 raszter középpontja **(22,5; 25,0)**, nem a lapközép (a §1 „sarkoktól 5,75 mm” csak X-ben igaz: Y-ban 8,25 / 3,25 mm). Érvényes: a v0.6 szakaszok a dokumentum végén, az **„As-built elhelyezés”** tábla és a befagyasztott interfész a `05` §3.1a-ban. A Z-stack (§3) és a FRONT-költségvetés (§2.3–§2.4) számai továbbra is irányadók.

Változás v0.2 → v0.3 (R4): **TP-terv a 05 §12 szerint** (hátoldali pogo csoport TP1–TP7, TP9–TP17 = 18 pad + 2 GND; TP4–TP6 pad-jai is hátul, a 0 Ω jumperek elöl; TP8 front, DNP); **minden 100k lehúzás a MAIN hátoldalon** (a FRONT-ról törölve); **státusz LED a MAIN hátoldalon** (a FRONT-ról törölve); J2 vezérlő-jel ESD a front költségvetésben; USB shield RC és UART0/GPIO 5 passzívok a hátoldalon; K5 számtan pontosítva; a CSI-döntés G3-ban (K14, K12).

## 0. Verdikt röviden

| Kérdés | Verdikt |
|---|---|
| Terület, MAIN hátoldal (modul oldal) | **befér** (kihasználtság ~50 %) |
| Terület, MAIN elülső oldal (kamera felőli) | **befér** (összesen ~56 %, gyűrűre vetítve ~82 %); G = 7-nél a kamera árnyékában ≤3,3 mm alkatrész állhat → a W gyűrű túlterheltsége (06-K5) megoldható |
| Terület, FRONT mindkét oldal | **bőven befér** (elöl ~8 %, hátul ~32 %); a korlát nem a terület, hanem az IR-LED/lencse/mikrofon távolság |
| Z-stack | **G = 7,0 mm**: kamera alatt ≤3,3 mm (G − 3,2 − 0,5); 6,0 mm elvetve |
| Kamera FFC a résben | bring-up: **50–100 mm szabványos FFC, nyitott stack, MAIN önállóan**; zárt stack: **25–30 mm egyedi kábel** (06-K1) |
| CSI útvonal modul (hátoldal) → J2 (front) | szimmetrikus via-pár (05 §13); **a pad-sorrend eltér a J2-től** (E20) → pár-keresztezés várható, ⏳ G3 (06-K14) |

Fő ok: a terület nem szűk keresztmetszet. A szűk keresztmetszet a **peremgyűrű** (a 25×25-ös modul körül 10 mm, a forrasztó pad-hosszabbítás után ~8,5), a **Z-magasság** és az **FFC hossz**.

## 1. Feltételezések

**Padszámozás:** a **jel ↔ pad hozzárendelés primer forrásból való (05 E20)**; a **térbeli elrendezés [F]**: a modul felülnézetből (hátoldalról, a modul oldaláról nézve), pad 1 bal felső sarok, számozás **óramutatóval ellentétes**, 22 pad/oldal, 1,0 mm osztás, az oldal közepére centrálva (a sarkoknál ~2 mm üres). Tehát: bal oldal 1–22 (fentről le), alsó oldal 23–44 (balról jobbra), jobb oldal 45–66 (lentről fel), felső oldal 67–88 (jobbról balra). Következmények (modul-felülnézet koordinátákban, modul 25×25, kezdőpont a modul bal alsó sarka):

| Jel | Pad (E20) | Oldal / hely [F] |
|---|---|---|
| RF (LNA_OUT) | P2 | bal oldal, fent (v≈32,5) |
| C6 UART/IO9/IO8 | P4, P5, P9, P10 | bal oldal, felső harmad |
| CSI | P41 D0N, P42 D0P, P43 CLKP, P44 CLKN / P45 D1N, P46 D1P | alsó oldal jobb vége / jobb oldal alja → **jobb alsó sarok** |
| USB-Serial-JTAG D−/D+ | P50, P51 (a P48/P49 HS PHY NC) | jobb oldal, alulról 6–7. pad (v≈17,5–18,5) |
| BOOT/strapping/UART0 | P62 / P63, P64, P65 | jobb oldal felső fele |
| VO4 | P66 | jobb felső sarok |
| SD | P67–P72 | felső oldal jobb vége |
| VBAT / ESP_3V3 / EN | P84 / P85–P86 / P87 | felső oldal bal fele |

Ha a tényleges footprint más (pl. CW, vagy a sarok-padok be vannak számolva), az egész kiosztást forgatni kell; a terület- és magasságszámok nem változnak.

**Koordinátarendszer:** *termék-keret*: elölről (lencse felől) nézve X jobbra, Y fel; a lap 0..45 × 0..45. A MAIN hátoldalát (modul) **hátulról nézve** rajzolom (modul-felülnézet), ott a jobb-bal a termék-kerethez képest tükrözött: nézeti u = 45 − x. A modul a lap közepén (10..35 × 10..35), **a forrasztó pad-hosszabbítás (K-10: kifelé ≥1,5 mm) miatt a lábnyom 28×28**; a modul 1 mm-rel az USB-C-vel ellentétes él felé tolva. Forgatás 0° a fenti számozással → **termék-keretben** a CSI/J2 a bal alsó sarokban (SW), az USB-C a bal élen (W), az RF/u.FL a jobb felső sarokban (NE), az SD a felső él bal felén, a 3V3 pad-ok a felső él jobb felén.

**Kamera modul [F]:** OV5640 MIPI, 25×24 mm NYÁK, 1,2 mm vastag; hátoldalán FPC aljzat + oszcillátor/LDO, együtt max. 2,0 mm magas; elöl 14×14 négyzetes holder + M12 hordó, optika-magasság a NYÁK elülső síkja felett ~18 mm (M12) vagy ~7 mm (Ø8 hordós AF-változat). **Rev A: NoIR vagy fix lencse**, ICR rev B. **Rögzítés "A" variáns**: a modul NYÁK-ja a FRONT hátsó síkjához fekszik, a holder + hordó egy **16×16 mm** (R1 sarkú) kivágáson át előre nyúlik. ("B" variáns: a holder a FRONT mögött marad, csak a hordó megy át a lyukon → a rés ≥10 mm kellene; nem javasolt.) A 05 szerinti "lencse furat +0,5 mm" ezért egy négyzetes kivágás, nem Ø furat.

**Egyéb [F]:** B2B 2×10, 1,27 mm, SMT: ~15×6 mm, párosított magasság **G = 7,0 mm** (a 7 mm-es 1,27 mm-es B2B elérhetősége [NEM ELLENŐRZÖTT], 05 Q17); lap 1,0 mm; M2 furatok a 33,5 mm raszteren (±16,75 a középtől → a sarkoktól 5,75 mm), keep-out Ø3,8; peremtiltás 0,5 mm; a "+30 %" a földterület/routing/keep-out felár.

## 2. Terület- és magasságköltségvetés

> **Rev A:** a MAIN 60×50 mm (05 0, Q22). Az alábbi számok a **45×45-ös végcélra** vonatkoznak; rev A-ban +975 mm² lapterület a többlet-sávban.

Rendelkezésre álló terület lapról: 45×45 = 2025; −peremtiltás (44×44) = 1936; −4 lyuk keep-out (4×11,3) = 45.

### 2.1 MAIN – hátoldal (modul oldal)

Levonás: modul + kézi forrasztási pad-hosszabbítás = **28×28 = 784**. **Elérhető: 1936 − 784 − 45 = 1107 mm².**

| Alkatrész | W×H | Terület | Magasság | Megjegyzés |
|---|---|---|---|---|
| USB-C 16 pin (top/mid-mount, THT shell) | 9,4×7,5 | 70,5 | 3,2 | a modul 1 mm-es eltolásával ≥2 mm szabad távolság a pad-hosszabbítástól (06-K8) |
| TVS (SMA/SMAJ10A osztály) | 6,8×3,0 | 20,4 | 2,4 | USB-C mellett |
| USB ESD **3,3 V array** (TPD2E2U06 / PRTR5V0U2X osztály, nincs VBUS láb) | 2,9×2,4 | 7 | 1,1 | az USBLC6-2SC6 törölve (05 B-1) |
| u.FL + π-háló (3×0603) – minden elem 0 Ω / DNP-képes | 3,4×3,0 + 6×2 | 22 | 1,25 | rev A: a modul saját IPEX-e alternatíva (05 G2) |
| BOOT + RESET + **USER** (3× SMD tact) | 3× 4,5×3,8 | 51,3 | 2,0 | lapszélen |
| **Supervisor** (nyílt-drain) + 0 Ω → ESP_EN + 100 nF (**DNP rev A**) | – | 12 | 1,0 | az EN (P87) közelében |
| Modul 3V3 bulk (**47 µF 1210 + 10 µF 0805 + 100 nF**) | – | 22 | 2,5 | a P84–P86 pad-oknál; egy érték, 05-tel azonos |
| VO4 1 µF + TP, strapping/felhúzás (6×0603) | – | 33 | 0,5 | C6_IO8/IO9 10k felhúzás, GPIO36 10k |
| Pogo TP csoport **TP1–TP7, TP9–TP17** (TP9a/b, TP16a/b kettéosztva) = **18 pad** (17 jel + TP3 GND) **+ 2 GND pad = 20 pad**, 2,0 mm raszter, Ø1,5 pad | ~22×5 | 95 | 0 | a C6 TP-k (TP10–13) külön, bal gyűrű; a TP4–TP6 pad-jai is itt (a 0 Ω jumperek elöl, via-val kivezetve, 05 §12); TP8 a front oldalon |
| **C6 + UART0 DNP header footprint** (1,27 / 2,54 mm) | ~12×3 | 36 | 0 (DNP) | a P2 (RF) padtól távoli élen (05 K-17) |
| Státusz LED 0603 + soros R (GPIO 6) | – | 9 | 0,6 | a modul közelében (a FRONT-ról ide került, 05 §5) |
| USB shield RC (1 MΩ ‖ 4,7 nF, 2×0603) | – | 6 | 0,5 | a J1 THT shield lábai mellett |
| Kisalkatrészek: **100k lehúzások (GPIO 26–28, 32 hátoldal; GPIO 53, 4 előlap a cél-IC mellett – v0.6)**, UART0 soros R ×2, GPIO 33 (USER) 100 nF, I2C felhúzás (DNP) | – | 45 | 0,5 | a lehúzások a modul közelében (05 K-7); a PDM soros R a FRONT-on van (nem itt); a VBUS osztó a front oldalon |
| **Összeg** | | **429,2** | | |
| **+30 %** | | **558** | | |
| **Kihasználtság** | | **558 / 1107 = 50 %** | | |

Legmagasabb: modul 3,3 mm; USB-C 3,2 mm.

### 2.2 MAIN – elülső oldal (kamera felőli)

Levonás: csak a lyukak. **Elérhető: 1936 − 45 = 1891 mm²**; ebből a gyűrű (kamera árnyékán kívül) ≈ 1891 − 600 = 1291 mm².

| Alkatrész | W×H | Terület | Magasság | Megjegyzés |
|---|---|---|---|---|
| J2 FPC 15 pin, 1,0 mm (ZIF) | 19×5,5 | 105 | 1,0–2,5 [F] | lapszélen, nyitott aktuátor ≥ +2,5 |
| J5 B2B 2×10 aljzat | 15×6 | 90 | G/2 = 3,5 | |
| microSD push-push (**DNP rev A**) | 14,5×14 | 203 | 1,85 | lapszélen; a lap pereme fölé 1–1,5 mm-t kinyúlhat |
| PD blokk (CH224A ESSOP10 + strap R + PG pull-up + 2× Rd **DNP** + CC-tap 2×(100k, 10 nF, 3,6 V Zener) **DNP**) | – | 80 | 1,5 | a régi 1k + BAT54S CC-sense **törölve** |
| eFuse blokk (TPS2595x 3×3 + 6 R/C + **2×1210 bulk 35–50 V** + 4,7 µF + VBUS→VBUS_SW 0 Ω híd **DNP**) | – | 76 | 2,5 (1210) | |
| Buck blokk (TPS62933F SOT583 + L 5×5×2,8 + 2×1210 CIN + 2×0805 COUT + 5 passzív + kimeneti 0 Ω/TP4) | – | 86 | **2,8 (L)** | 4×4×2,1-es induktorral ~75 |
| SD blokk (TPS22918 + 5 felhúzás + ESD tömbök + kondik; **DNP rev A**) | – | 55 | 1,1 | |
| **IR ág:** 2. eFuse (≥18 V, ILIM 0,5–0,7 A) + ~10 passzív + shunt + **TP8** + biztosított 0 Ω footprint (**DNP rev A**) | – | 52 | 1,1 | a TPS22810 osztály elvetve (nincs állítható ILIM) |
| **CAM_3V3 load switch** (TPS22918 + CT + C + 0 Ω mérő-jumper) | – | 20 | 1,1 | |
| **VBUS_SW osztó** (≥200k/54k + 3,6 V Zener + 100 nF; az eFuse után) | – | 14 | 0,6 | |
| **J2 vezérlő-jel ESD** (alacsony-C array: CAM_IO0, SCL, SDA; `07` #38) | 3×3 + pad | 8 | 1,1 | a J2 mellett (FIT) |
| **NTC + osztó + 100 nF** (ADC2, GPIO 49) | – | 10 | 0,6 | a buck/IR közelében |
| Egyéb (0 Ω mérő-jumperek a TP4–TP6-hoz; a TP pad-ok a hátoldali pogo csoportban vannak, via-val kivezetve; TP8 front) | – | 20 | 0,5 | |
| **Összeg** | | **819** | | |
| **+30 %** | | **1065** | | |
| **Kihasználtság** | | **1065 / 1891 = 56 %** (gyűrűre vetítve 1065 / 1291 = 82 %) | | |

Magasság-szabály: a kamera árnyékában (25×24, lásd 3. fejezet) **G = 7,0-nál ≤ 3,3 mm** magas alkatrész állhat → induktor (2,8), 1210 kondik (2,5) és microSD (1,85) az árnyékban is elhelyezhető; a J5 (3,5) és a J2 (nyitott aktuátor) a gyűrűbe vagy a szélre kerül.

### 2.3 FRONT – elülső oldal

Levonás: lyukak + lencse kivágás 16×16 = 256. **Elérhető: 1936 − 45 − 256 = 1635 mm².**

| Alkatrész | W×H | Terület | Magasság |
|---|---|---|---|
| IR LED 3535 ×4 (pad + hőterítő via) | 4× 4,2×4,2 | 70,6 | 2,0 [F] |
| PDM mikrofon (+ akusztikai port Ø~1) | 4,3×3,4 | 14,6 | 1,0 |
| VEML7700 (DNP) + IR-árnyékoló gyűrű | 3,5×3,0 | 10,5 | 0,9 |
| **Összeg** | | **95,7** | |
| **+30 %** | | **124** | |
| **Kihasználtság** | | **124 / 1635 = 8 %** | |

A státusz LED a MAIN hátoldalán van (2.1). VEML7700: a saját 850 nm IR LED-ektől és a FR4-n átszivárgó fénytől árnyékolt (Cu gyűrű + fekete hab / ablak-apertúra), különben a nap/éj mérés oszcillál (05 D7).

**Lencse kivágás: 16×16 mm.** A négyzetes holder **14×14 mm, tengelyhez igazítva** (nem elforgatva) – ezért 1 mm/oldal hézaggal átfér a 16×16-os kivágáson; az R1 sarok-lekerekítés a kivágás sarkát csak 0,3 mm-rel viszi beljebb, ami a holder sarkát nem érinti. A 19,8 mm-es átló csak elforgatott holdernél lenne releváns (ilyenkor 18×18 vagy Ø20 kellene). A végleges méret a tényleges kamera modul STEP-jével ellenőrizendő [F].

### 2.4 FRONT – hátsó oldal

Levonás: kamera modul 25×24 = 600 + lyukak 45. **Elérhető: 1936 − 600 − 45 = 1291 mm².**

| Alkatrész | W×H | Terület | Magasság |
|---|---|---|---|
| B2B 2×10 fej + lokális 10 µF + 100 nF | 15×6 + 12 | 102 | G/2 = 3,5 |
| IR CC driver ×2 (IC SOT-23-6, induktor 4×4×1,8, Schottky, CIN/COUT 1206, Rsense, 3 kis passzív) | 2× 69 | 138 | 2,1 (L) |
| AO3400 ×2 (IR PWM) | 2× 9 | 18 | 1,1 |
| ICR: DRV8837 + 2 kondi + J6 JST-SH 2p (**DNP rev A**; a ICR_IN lehúzások a MAIN-en) | – | 37 | 1,5 |
| Mikrofon LC + CLK soros R (33–100 Ω) | – | 10 | 0,5 |
| IR LED anód kondik (Cout ≤1 µF); **a 100k lehúzások nem itt, hanem a MAIN hátoldalon vannak** (05 K-7) | – | 10 | 1,0 |
| **Összeg** | | **315** | |
| **+30 %** | | **410** | |
| **Kihasználtság** | | **410 / 1291 = 32 %** | |

A TP8 shunt/jumper **nem itt** van: a MAIN front oldalán (2.2), mert a FRONT-on a TP zárt stack-ben elérhetetlen.

Peremsávok (a kamera körüli 9,5 mm): N és S sáv ~29,7×9,5 = 282 mm² (egyenként egy IR driver ~108 mm² +30 %-kal), E sáv B2B, W sáv ICR – elfér.

## 3. Z-stack

### 3.1 Rétegek (elölről hátra, a "G = 7,0" tervezési pontra)

| Elem | Vastagság / magasság |
|---|---|
| Lencse/hordó kiállása a FRONT elülső síkja előtt | **M12: ≈ 17,0** (18 − 1,0 lap) · Ø8 AF: ≈ 5,5 [F] |
| FRONT elülső alkatrész (IR LED 3535 lencsével) | 2,0 [F] (a hordó mögött) |
| FRONT NYÁK | 1,0 |
| **Rés G** (B2B párosított magasság = M2 távtartó hossz) | **7,0** |
| – ebből a kamera modul NYÁK | 1,2 |
| – ebből a modul hátoldali alkatrészei (FPC aljzat/osc.) | 2,0 |
| – ebből szabad a MAIN front oldal fölött a kamera árnyékában | 7,0 − 3,2 = **3,8** (alkatrész-limit 0,5 légréssel: **3,3**) |
| MAIN NYÁK | 1,0 |
| MAIN hátoldal: P4 modul (legmagasabb) | 3,3 (USB-C 3,2, tact 2,0) |
| **Összes vastagság – lencse nélkül** | 2,0 + 1,0 + 7,0 + 1,0 + 3,3 = **14,3** |
| **Összes – M12 lencsével** | 17,0 + 1,0 + 7,0 + 1,0 + 3,3 = **29,3** |
| **Összes – Ø8 AF hordóval** | 5,5 + 1,0 + 7,0 + 1,0 + 3,3 = **17,8** |

### 3.2 Rés (G) feltételek

Alsó korlátok: G ≥ 3,2 (modul) + h_max(MAIN front a kamera árnyékában) + 0,5 mm légrés, azaz **h_max = G − 3,2 − 0,5**.

| G (B2B + távtartó) | Max. magasság a kamera alatt | Értékelés |
|---|---|---|
| 5,0 | 1,3 | csak 0603/0805 + IC-k; **elvetve** |
| 6,0 | 2,3 | a v0.1 minimuma; induktor (2,8) és 1210 (2,5) csak a gyűrűben; **elvetve** (05 v0.3) |
| **7,0** | **3,3** | **választott** (05 v0.4); induktor, 1210 és microSD is lehet az árnyékban |
| 8,0 | 4,3 | az FFC hurok (K1) miatt sem szükséges: a zárt stack 25–30 mm kábellel megy |

Gyűrű-átfedés: a FRONT hátoldal gyűrű-alkatrészei (≤ 2,1) + MAIN front gyűrű-alkatrészei (≤ 2,8) = 4,9 < 7,0 − 0,5 = 6,5 → átmegy. A J2 nyitott aktuátora (kb. +2,5 a konnektor fölött = 4,5–5,0) csak **a stack zárása előtt** nyílik, ezért nem ütközik a FRONT-hátoldali S-sáv IR driverével (összeszerelési sorrend, 05 3. fejezet).

B2B tűrés: párosított magasság ±0,2–0,3 mm [F]; a 4 távtartó a szerkezeti elem (05 3.) → 2×10-es 1,27 mm-es fej rövid érintkező-letörlési úttal (wipe) választandó, hogy a tűrést bírja.

### 3.3 FFC hajlítás és J2 magasság

- FFC kiindulási hosszak: a legkisebb készletes 15 pin 1,0 mm FFC jellemzően ~50 mm [F]. **Rev A bring-up:** szabványos **50–100 mm FFC, nyitott stack, a MAIN önállóan** (05 §0, K-7) – a hossz itt nem gond.
- A modul FPC aljzata és J2 között vízszintesen ~8–20 mm van, függőlegesen ~2–3 mm. 50 mm kábelből (szabad hossz ~43) **~25–33 mm felesleg** marad → Ω-hurok, ami **7 mm résben sem** tartható a B2B és az alkatrészek mellett. Ezért a **zárt stack: 25–30 mm egyedi kábel / rövid flex** (05 v0.3 döntés, Q5/Q6 kapu).
- Hajlítási sugár: 0,1–0,2 mm-es FFC-nél R ≥ 2 mm javasolt → S-kanyarhoz ≥ 4 mm függőleges + ≥ 4 mm vízszintes hely kell; a J2-nél a kábelnek az aktuátoron kívül ≥ 3 mm egyenes szakasz kell.

## 4. Floorplan vázlat (ASCII)

Rajzmérték: 1 karakter = 1 mm vízszintesen, 1 sor = 2 mm függőlegesen. `O` = M2 furat (Ø3,8 keep-out). Az ASCII a vázlat tájékoztató; a pontos hely a Waveshare footprint importja után dől el. (A pad-számok E20-ból, az élek [F].)

### 4.1 MAIN hátoldal (modul oldal) – hátulról nézve (tükrözött X)

Modul-felülnézet; pad 1 bal felül. Termék-keretben a bal oldal a jobb (tükrözés).

```
+---------------------------------------------+
|                 SUP   rrrrr                 |   SUP: supervisor + 0 ohm (DNP) az EN (P87) mellett
|            ddddddddddd RSTrr                |   RST: RESET gomb a felso elen
|    OOO     3V3-DECdddd rrrrr         OO     |   3V3-DEC: 47 uF + 10 uF + 100 nF a P84-P86 padoknal
|    OOO     ddddddddddd     SDvias    OO     |   SDvia: P67-P72 -> via a front oldali uSD-hez (DNP)
|            ddddddddddd     ssssss  VO4v     |   VO4: P66, 1 uF + TP
|uuuu      ######################### vvvv     |
|uFLu      #########################          |   uFL a P2 mellett (DNP-kepes; a modul IPEX-e alternativa)
|uuuu      #########################     BOOT |   BOOT gomb (P62/P63 magassaganal)
| ccccc    #########################     bbbb |
| ccccc    #########################   tttttt |   TVS
| C6TPc    #########################   TVSttt |
| ccccc    P4 MODUL 25x25###########   UUUUUUU|   (pad-hosszabbitassal 28x28)
| ccccc    #########################   UUUUUUU|   USB-C a jobb elen (P50/P51 magassaganal), >=2 mm a pad-hosszabbitastol
|          #########################   USB-CUU|
|          #########################   UUUUUUU|
|          #########################   UUUUUUU|
|          #########################   eeeeee |   ESD (3,3 V array)
|          #########################   ESDeee |
|            kis-alkppppp  CSIviaxxxx  eeeeee |   CSIvia: P41-P46 -> via J2-hoz (front)
|    OOO     pppppppppppp  xxxxxxxxxx  OO  USR|   USR: USER gomb (GPIO5)
|    OOO  POGO TP1-7,9-17PPPPP        OO      |   POGO: TP1-TP7, TP9-TP17 (18 pad + 2 GND; TP8 front)
|  HDR(DNP)  PPPPPPPPPPPPPPPPPPPPP   LED      |   HDR: C6/UART0 header J7 (DNP), a P2-tol tavol; LED: statusz LED (GPIO 6)
|                                             |
+---------------------------------------------+
```

- A 100k lehúzások (GPIO 26–28, 32) a modul közelében; GPIO 53 / 4 (SD_EN / CAM_3V3_EN, v0.6) az U8 / U6 mellett, a hátoldalon (nincsenek külön a rajzon); az USB shield RC a J1 mellett.
- A C6 TP csoport (`C6TP`, TP10–13) a bal élen, a P4/P5/P9/P10 magasságában (v 19–28); az RF-vezeték (P2 → u.FL) fölötte, ~4–5 mm-re. A DNP header (`HDR`) a lap alján, az RF-padtól a lehető legtávolabb.
- Az USB-C a jobb élen v≈13–22; a TVS és az ESD közvetlenül fölötte/alatta.

### 4.2 MAIN elülső oldal (kamera felől) – termék-keret, elölről nézve

```
+---------------------------------------------+
|          SSSSSSSSSSSSSS                     |
|          SSSSSSSSSSSSSS  wwwwwwwww          |   uSD (DNP rev A): felso el, bal fele (P67-P72 alatt, via)
|    OOO   SSSSSSSSSSSSSS  SD-SWwwww   OO     |   SD-SW: load switch, felhuzasok, ESD (DNP rev A)
|    OOO   uSDSSSSSSSSSSS  wwwwwwwww   OO     |
|          SSSSSSSSSSSSSS                     |
|          SSSSSSSSSSSSSS...........          |
|          SSSSSSSSSSSSSS...........          |
|BBBBBBBBBB.........................          |
|BBBBBBBBBB.........................   555555 |   J5: B2B 2x10 a jobb elen (FRONT-tal tukorpar)
|BUCK+LBBBB.........................   555555 |   (L 2,8 mm: a kamera arnyekaban is lehet, <=3,3 mm)
|BBBBBBBBBB.........................   555555 |
|BBBBBBBBBBKAMERA-ARNYEK (<=3.3mm)..   J55555 |   '.' = kamera modul arnyeka: csak <=3,3 mm
|BBBBBBBBBB.........................   555555 |
|PD+CCDDDDD.........................   555555 |   PD: CH224A, strap, PG; CC-tap + Rd DNP
|DDDDDDDDDD.........................   555555 |
|DDDDDDDDDD.........................   555555 |
|eFuse+BRG..........................  IRsw    |   BRG: VBUS->VBUS_SW hid (DNP); IRsw: 2. eFuse/fused 0R (DNP)
|EEEEEEEEEEFFC-savffffffff.........   TP8     |   TP8: IR shunt TP, a MAIN front oldalan
|EEEEEEEEEEfffffffffffffff   NTC VBUSdiv      |   NTC, VBUS osztó (eFuse után)
|    OOO JJJJJJJJJJJJJJJJJJJ  CAMsw 0R4 OO    |   J2: also el, bal harmad; CAMsw: CAM_3V3 switch; 0R4: buck kimeneti 0 ohm (a TP4 pad a hatoldali pogo csoportban)
|    OOO J2 FPCJJJJJJJJJJJJJ  miscmmmm OO     |
|        JJJJJJJJJJJJJJJJJJJ  mmmmmmmm        |
|                                             |
+---------------------------------------------+
```

- A bal oldali gyűrű (x 0,5–9,5) az USB-C bejövő teljesítményút: eFuse → PD+CC → buck, a 3V3 a felső peremen/hátoldali rétegen megy az NE sarok P84–P86 pad-jaihoz (06-K6).
- A buck a bal élen van, azaz az u.FL-től (NE) a lehető legtávolabb; G = 7-nél az induktor és az eFuse bulk a kamera árnyékába is behúzható (≤3,3 mm).

### 4.3 FRONT elülső oldal – termék-keret

```
+---------------------------------------------+
|                                             |
|                                             |
|    OOO                               OO     |
|    OOO        IIIII     IIIII        OO     |   IR LED par (N ag, 2 soros LED)
|               IRIII     IRIII               |
|               IIIII     IIIII         mmm   |
|                                       MIC   |   PDM mic a jobb elen (>=10 mm az IR LED-ektol, ~13 mm)
|              LLLLLLLLLLLLLLLL         mmm   |
|              LLLLLLLLLLLLLLLL               |
|              LLLLLLLLLLLLLLLL               |
|              LLLLLLLLLLLLLLLL               |
|              LENS 16x16LLLLLL         ALS   |   VEML7700 (DNP) + IR arnyekolo gyuru
|              LLLLLLLLLLLLLLLL         vvv   |
|              LLLLLLLLLLLLLLLL               |
|              LLLLLLLLLLLLLLLL               |
|                                             |
|               IIIII     IIIII               |   IR LED par (S ag)
|               IRIII     IRIII               |
|    OOO        IIIII     IIIII        OO     |
|    OOO                               OO     |
|                                             |
|                                             |
+---------------------------------------------+
```

- LED-ek a lencse tengelyétől ~14,9 mm-re (≥ 10 mm teljesül), a kivágás széléig ~4,25 mm → Cu baffle gyűrű ≤ 3 mm széles lehet.

### 4.4 FRONT hátsó oldal – átlátszó nézet (termék-keret)

```
+---------------------------------------------+
|        DDDDDDDDDDDDDD qqqq                  |   DRV-N: N ag IR CC driver + AO3400 (Q)
|        DRV-NDDDDDDDDD Qqqq                  |
|    OOO DDDDDDDDDDDDDD qqqq           OO     |
|    OOO                               lllll  |   mic LC + CLK soros R a mikrofon mogott
|                                      micll  |
|          CCCCCCCCCCCCCCCCCCCCCCCCC   lllll  |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|          CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |   B2B: a MAIN J5-tel azonos termek-keret hely
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
| ICRiiii  KAMERA MODUL 25x24CCCCCCC   B2BBBB |   ICR (DNP rev A) a bal savban
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
| iiiiiii  CCCCCCCCCCCCCCCCCCCCCCCCC   BBBBBB |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|          CCCCCCCCCCCCCCCCCCCCCCCCC          |
|                                             |
|    OOO                               OO     |
|    OOO DDDDDDDDDDDDDD Qqqq   ppp     OO     |   DRV-S: S ag driver; ppp: LED anod kondik
|        DRV-SDDDDDDDDD qqqq                  |
|        DDDDDDDDDDDDDD                       |
+---------------------------------------------+
```

- Az ASCII a kamera modul 25×24-es lábnyomát mutatja; a lencse kivágás a közepén van (4.3). A B2B a MAIN J5-tel termék-keretben pontosan egymás fölött; pin 1 és tükrözés a papír-próbán ellenőrzendő (P-22).
- A mikrofon szándékosan a jobb élen van (nem a bal élen), mert a MAIN buck/induktor a bal élen van, közvetlenül a FRONT bal sávja alatt (06-K7). A **TP8 nincs a FRONT-on** (MAIN front oldal, 4.2).

### 4.5 Modul forgatás – a három követelmény

| Követelmény | Teljesül-e 0°-nál [F számozás] | Megjegyzés |
|---|---|---|
| CSI P41–P46 → J2 | **igen**: a CSI a jobb alsó sarokban (hátulról) = SW (termék-keret), J2 az alsó él bal harmadában | P41–P44 az alsó oldalon, P45–P46 a bal oldalon (termék-keret) – a pár P45/P46 a sarkon át megy, ~2–3 mm többlet. **A pad-sorrend eltér a J2-től (06-K14)** |
| P2 (RF) → u.FL | **igen**: P2 = NE sarok | u.FL a jobb él felső részén, RF < 6 mm; vagy a modul saját IPEX-e (rev A, G2) |
| P50/P51 → USB-C | **igen**: bal él (termék-keret), alulról 6–7. pad | USB-C a bal élen v≈13–22, D± a pad-hosszabbítás miatt ≥2 mm hézaggal a modultól |

Mellékhatás: az RF (P2) és a 3V3/EN pad-ok (P84–P87) ugyanabban a sarokban vannak (NE), a CSI és az USB pedig ugyanabban a negyedben (SW) → mindkét sarok zsúfolt.

## 5. Konfliktusok és kockázatok

| # | Súly | Konfliktus | Javaslat / állapot |
|---|---|---|---|
| K1 | **HIGH** | Kamera FFC: a 40–60 mm kábel a ~8–20 mm-es modul→J2 távolsághoz kb. 25–33 mm felesleget ad; 7 mm résben sem gyártható hurok | **Döntés (05 v0.3/v0.4):** zárt stack **25–30 mm egyedi kábel / rövid flex**; rev A bring-up **50–100 mm FFC, nyitott stack**, MAIN önállóan. A tényleges hossz Q5/Q6 (G3) |
| K2 | **HIGH** | A CSI páros a hátoldali modul-padról a front oldali J2-re megy → laprétegváltás | ✅ 05 §13: egyetlen szimmetrikus rétegváltás (P+N együtt, 2 GND visszatérő via), a J2 padoknál ≤1 mm; front oldali GND-sáv marad. **A pár-sorrend miatt több kell lehet → 06-K14** |
| K3 | **HIGH** | 2 réteges, kétoldalas beültetés mellett nincs tömör alsó GND | A hátsó réteg CSI/RF alatt a front réteg GND-öntvény; az NE sarok (RF) mögött és az S sáv (CSI) mögött a front oldalon alkatrész-tilalom (csak GND). A J5 (E gyűrű, y 14–29) nem ütközik az RF-vezetékkel (y≈33–37) |
| K4 | MED | A 3V3 pad-ok (P84–P86) az NE-felső élen vannak, a buck a W gyűrűn (~35 mm) → hosszú 3V3 vezeték; az N gyűrűt az SD foglalja a front oldalon (rev A: SD DNP) | 3V3 a hátoldali rétegen a felső gyűrűben, ≥1,2 mm széles; helyi bulk a pad-oknál (47 µF + 10 µF + 100 nF) |
| K5 | MED | MAIN front W gyűrű kihasználtsága ~100 %: a **nettó** PD (80) + eFuse (76) + buck (86) = **242 mm²** (+30 % felár nélkül, a 2.2 sorai szerint); az **IR ág 52 mm²-ével (DNP rev A) együtt ≈ 294 ≈ 295 mm²**; a 282 mm² a gyűrű becsült nettó területe | ✅ rev A-ban a 242 mm² (kb. 86 %) a mérvadó (az IR ág DNP, de a footprint helyet foglal → ~104 %); G = 7-nél az induktor és az eFuse bulk (≤3,3 mm) a kamera árnyékába húzható; a CC-tap DNP |
| K6 | MED | RF pad P2, 3V3, EN, VO4, SD-pad-ok mind az NE/N sarokban; a C6 TX/RX pad-ok 2 mm-re vannak a P2-től | Pogo/TP-k a bal élre vissza, GND-via kerítés az RF-vezeték mellett (P-30), a C6 TP-k a hátoldalon; a DNP header az RF-padtól távol (K-17) |
| K7 | MED | A buck/induktor a FRONT bal sávja alatt van; ha a mikrofon is a bal sávban lenne, P-27 sérülne | A mikrofon a jobb élre került (4.3); a PDM CLK-t a jobb sávban, a B2B GND-k között vezetni |
| K8 | MED | USB-C mélysége 7,5 mm vs 8,75 mm-es gyűrű; **a ≥1,5 mm pad-hosszabbítás (K-10) után ~1,0 mm marad**; THT shell lábak a modul-lábnyúlványnál | A modul **1 mm-rel az USB-C-vel ellentétes él felé** tolva → ≥2 mm hézag (asszimetrikus gyűrű), vagy mid-mount csatlakozó (a lap pereme kivágva) |
| K9 | MED | Lencse kivágás: a 05 "furat +0,5 mm" nem elég négyzetes holder esetén; plated négyzet + IR baffle Cu gyűrű | Marótt négyzetes kivágás R1 sarkokkal; a **tengelyhez igazított 14×14 holder 16×16-ban 1 mm/oldal hézaggal átfér** (az átló nem releváns, ha nincs elforgatva); a baffle gyűrű Cu mindkét oldalon + fekete hab; ellenőrzés a tényleges modullal |
| K10 | MED | microSD a résben: a FRONT fölötte 7 mm-re van, a kártya csak oldalról cserélhető | Ház nélkül rendben (rev A: SD DNP), házban a rés oldalnyílása szükséges (05 18.) |
| K11 | LOW | M2 furatok 33,5 mm rasztere vs J2 (x≥8,3), SD (x≥9,9), USB-C (y≥13): a keep-out-ok nem ütköznek, de a sarkok használhatatlanok (~45 mm² oldalanként) | – |
| K12 | LOW | A térbeli számozási feltételezés [F]: ha a footprint más, a sarok-hozzárendelések (CSI/RF/USB/SD) elfordulnak | Footprint import (G2) után a 4. fejezet újrarajzolandó; a CSI/J2 döntés G3-ban |
| K13 | LOW | IR driver S sáv a FRONT hátoldalon a MAIN J2 fölött: 2,1 + 2,5 = 4,6 < 7,0 − 0,5 | G = 7-nél rendben; zárt stack-ben az aktuátor már lehajtva |
| K14 | **HIGH** | **CSI pad-sorrend (E20): D0N, D0P, CLKP, CLKN, D1N, D1P vs J2: D0, D1, CLK (CLK_N, CLK_P)** – a CLK pár P/N sorrendje fordított, és a pár-sorrend is eltér (D0–CLK–D1 vs D0–D1–CLK) → sík 2 rétegen legalább egy pár-keresztezés / P-N csavar | ⏳ **G3** (a kamera kiválasztása után; a G2 csak a footprint térbeli sorrendjét adja): opciók: kamera / FFC adapter sorrendje, CSI lane/polaritás csere (TRM [NEM ELLENŐRZÖTT]), via-keresztezés a J2 padoknál (rev A mérés); lane-swapra nem építünk |
| K15 | ✅ | **Lapméret:** rev A MAIN **60×50 mm** (döntés 2026-10-09), azonos M2 raszter + J2/J5 koordináta; a 45×45-ös számítás a rev B célra érvényes. Rev A-ban a W-gyűrű (100 %) és a USB-C 1,25 mm-es rés (K8) feloldódik: USB-C, microSD, J7, pogo csoport a többlet-sávba. | lezárva |

## 6. Állapot a 05-höz képest

A v0.1 javaslatai a **05 v0.3/v0.4**-be beépültek: G = 7,0 mm; négyzetes 16×16 kivágás (A variáns); a CSI "nincs via" szabály helyett szimmetrikus via-pár; az FFC 40–60 mm S-hurok helyett 25–30 mm kábel (zárt stack) és 50–100 mm FFC (rev A bring-up); a padtérkép-feltételezés a 05 §14-ben, E20 primer pad-hozzárendeléssel. A Q8 (Z-stack költségvetés) e dokumentummal G = 7-re zárt; a tényleges kamera modul (Q5/G3) után újra kell számolni. Nyitott: 06-K14 (CSI sorrend, G3), 06-K15 (lapméret), a footprint-import utáni újrarajzolás (06-K12).


> **2026-10-09 (huzalozás):** TP9A/B, TP10–TP15 törölve (J7/USB duplikátum); TP5 (CAM_3V3) a hátoldal bal-felső részére (11,6; 9,0) került; R31/R32 az előlapra a J2 mellé; R27/R28 előlapra az U8/U6 mellé; J7 a bal-felső lapszélre (60×50-es állapot – v0.6-ban a J7 a felső élen, TP5 (12,6; 6,6): lásd lent, „As-built elhelyezés”). Részletek: `90-review-log.md`.


## 45×45 mm, 4 réteg – helyigény (v0.6, 2026-10-09)
Mérve a jelenlegi footprintekből (courtyard-terület): előlap 1134 mm², hátoldal 1299 mm², összesen 2433 mm² (123 alkatrész, ebből 39 DNP). Rendelkezésre álló terület: ~1900 mm²/oldal (furat-keepout és 0,5 mm lapszél nélkül) → **~64 % kihasználtság** (B: ~68 %, F: ~60 %). 4 rétegen kivitelezhető, kevés tartalékkal.
Legnagyobb tételek: U1 modul 812 (B), J3 microSD 278 (F, DNP), J2 FPC 246 (F), J5 B2B 117 (F), J1 USB-C 100 (B), SW1–SW3 3×51 (B, 6×6 mm), J7 38 (B, DNP).
Csökkentési lehetőségek (döntés kell): kisebb tapintókapcsolók (pl. 3×4 mm SMD: ~3×12 mm² → −115 mm²), J7 helyett pad-sor / Tag-Connect lábnyom, pogo TP-k 1,0 mm-re.

### 45×45 / 4 réteg floorplan-javaslat (v0.6, 2026-10-09)
Kényszerek (mért courtyard): U1 28,6×28,6 (B); J1 USB-C 9,5×10,7 (B, 4 THT köpenyláb → az F oldalon is foglal); J2 FPC 24,0×10,4 (F, felül); J3 microSD 17,8×15,8 (F, bal közép, DNP); J5 B2B 8,7×13,8 (F); M2 furatok (5,75 / 39,25 ; 8,25 / 41,75).
Ütközés: a J1 sem jobbra (J5 az F-en), sem balra (J3 az F-en) nem fér a jelenlegi J5/J3 mellett → **két áthelyezés kell**:
1. **U1 modul 2 mm-rel balra** (x 22,5 → 20,5): jobb oldali B-sáv 10,2 mm → a J1 elfér (B, jobb él, nyílás jobbra, y ≈ 22,5).
2. **J5 az F oldal aljára, vízszintesen** (≈ x 17–31, y 36–44,7): a jobb F-sáv felszabadul a táp-blokknak és a J1 köpenylábainak. ⚠ A FRONT a J5 új helyéhez igazodik (a FRONT még nincs tervezve → költségmentes).

```
 B (modul oldal, hátulnézet NEM tükrözve, felülnézet)      F (kamera oldal)
 +---------------------------------------------+          +---------------------------------------------+
 |MH1  SW1 SW2 SW3  J7(padsor)   TP-rács   MH2 |          |MH1 U6/CAM-táp [  J2 FPC 15p  ]  U2 CH224A MH2|
 |     [------- U1 modul 28,6 x 28,6 -------]  |          |  R/C                           CC, PD-strap  |
 |RF   [                                    ]  J1|          |[J3     ]   pull-upok, R24–R29   U3 eFuse     |
 |J4/π [   (alatta L3: GND, L2: GND)        ] USB|          |[microSD]   (modul alatti F)     U4 buck + L1 |
 |LED  [                                    ]  -C|          |[ DNP   ]   U8 SD-táp            C5/C6/C8..   |
 |     [------------------------------------]  |          |            IR blokk (DNP)       TH1/NTC      |
 |MH3   C20–C23 (P84–86)  C24 VO4          MH4 |          |MH3      [==== J5 B2B (vízszintes) ====]  MH4 |
 +---------------------------------------------+          +---------------------------------------------+
```
Rétegek: L2 folytonos GND; L3 táp-szigetek (VBUS/VBUS_SW/3V3) + GND a CSI/RF/USB alatt.

## As-built elhelyezés – MAIN v0.6 (NYÁK-ról mérve, 2026-10-10)
Állapot: **végső rev A (2026-10-11)** – a 8. kör javító körei után, a 9. kör (végső review) pillanatképéről mérve (pcbnew; a `kicad/MAIN` lappal md5-azonos). **128 lábkép (124 alkatrész + MH1–4), ebből 38 DNP; F 81 + 4 MH, B 43; beültetett (CPL) 72: F 47 / B 25.** ~~Állapot: a 7. kör review és a DNP-csonkok eltávolítása után, a layout-javító kör előtt; 127 lábkép (123 + MH1–4), 39 DNP; F 81 + 4 MH, B 42~~ (2026-10-10). Koordináták: **KiCad-keret** (origó bal-felső sarok, X jobbra, Y **lefelé**, F-oldali nézet; a B-alkatrészek is ebben a keretben) – a fenti termék-keretbe: x változatlan, y₀₆ = 45 − y. A mechanikai interfész (kontúr, MH, J2, J5, J1, J4, J7, gombok, LED) részletesen: `05` §3.1a.

| Csoport | Refdes | Oldal | Hely (x; y, mm) | Megjegyzés |
|---|---|---|---|---|
| P4 modul | U1 | B | (20,5; 25,0); udvar x 6,2–34,8, y 10,7–39,3 | a lapközéptől 2 mm-rel balra |
| Modul 3V3 hidegítés | C20 47 µF, C21 10 µF, C22/C23 100 nF | B | C20 (19,75; 42,4); C21 (14,8; 41,85) −90°; C22 (13,05; 40,75) −90°; C23 (11,55; 40,75) −90° | **8. kör: a P84–P86 padok alá** (0,8 mm-es B-sín); a C22/C23 +3V3 padja 0,525 mm-re a P85–P87 csúcsoktól → U1 kézi forrasztás: `05` §15 |
| VO4 | C24 1 µF, TP7 | B | C24 (31,5; 41,3), TP7 (37,6; 35,0) | |
| Strap / EN | R20 (BOOT_EN), R21/R22 (C6_IO9/IO8), R23/C25 (ESP_EN RC) | B | R20 (31,5; 43,4); R21/R22 (3,2; 27,45 / 25,75); R23/C25 (3,2; 29,55 / 31,25) | R23/C25: FIT (a lapon is, 8. kör) |
| UART0 soros R | R40/R41 1k | B | (27,0; 41,3 / 43,4) | → J7.7/J7.8 |
| USB-C + TVS | J1, D1 | B | J1 (40,8; 22,5) jobb él; D1 (40,5; 13,5) az U3 alatt | a TVS nem a J1 mellett, 6,8 mm-re – elfogadott eltérés (05 §0.1) |
| USB ESD | U5 | F | (34,0; 21,2) 90° | |
| USB shield RC | R1 1 MΩ, C1 4,7 nF (200 V) | F | R1 (43,6; 21,7) −90°; **C1 (43,8; 26,75) −90°** | a J1 DK köpenyfüle mellett; C1.2 saját GND via (43,5; 28,35) |
| RF | R34 0R (FIT), C27/C28 (DNP), J4 | B | R34 (3,9; 34,5) 180°; C27 / C28 (5,55 / 2,25; 34,02) 90°, DNP; J4 (3,0; 38,3) bal él | U1 P2 (7,625; 34,5) → J4, út 7,96 mm (0,302 mm); a shunt-padok az y 34,5-ös egyenesen; GND kerítés + In2 100 % GND (8. kör) |
| Gombok | SW1 BOOT / SW2 RESET / SW3 USER | B | (11,5; 3,0) / (33,5; 3,0) / (33,5; 7,4) | felső él; C40 (USER 100 nF) (29,4; 7,6) |
| Státusz LED | D20, R30 1k | B | (3,2; 14,35 / 16,05) | bal él |
| C6 / UART0 padsor | J7 (DNP) | B | (22,5; 2,0), vízszintes | felső él |
| eFuse FLT felhúzás | R11 10k | B | (36,0; 15,5) | |
| PDM CLK soros R | R70 47 Ω | B | (17,0; 8,0) | a J2 alatt |
| CC-tap Zener | D21/D22 (DNP) | B | (1,8 / 4,6; 20,0) | |
| Teszt pontok | TP1–TP4, TP7, TP16A/B, TP17–TP19 / TP5 / TP6 | B | csoport x 37,6–43,1, y 29,5–40,5 (2,75 mm rács); TP5 (12,6; 6,6); TP6 (36,3; 10,4) | `05` §12 |
| Kamera FPC | J2 | F | (22,5; 7,5), 180° | felső él, kábel a felső él felől |
| CAM_3V3 kapcsoló | U6, C50–C52, R50, R53, R51/R52 (DNP), R28 | F | x 2,75–12,6, y 11,0–16,3; U6 (3,6; 13,7), C50 (2,75; 11,0), R28 (3,0; 16,3) | bal-felső; R28 = 10k; C50 0,25 mm-rel balra (MH1 udvar) |
| I2C felhúzás | R31/R32 (DNP) | F | (16,4; 14,2 / 15,9) | |
| GPIO lehúzások | R24, R25, R26, R29 (DNP) | F | (19,8; 13,6), (24,05; 19,45), (19,75; 16,8), (35,45; 8,7) | a CSI-folyosó mellett |
| eFuse blokk | U3, R6–R10, C3, C4, **C14**, JP1 | F (C4: **B**) | U3 (40,8; 13,4); R6 (36,2; 11,25), R7 (36,0; 12,95), R8 (35,95; 14,65), R9 (35,95; 16,2); **R10 (43,8; 12,75) −90°; C3 (43,5; 9,45) 90°; C4 → B (42,9; 16,2); C14 új (42,675; 16,0)**; JP1 (36,4; 4,5) | jobb-felső; a C4 1,005 mm-re a J1 köpenylábtól; a C14 (1 µF, U3 OUT) 1,14 mm-re az U3.6-tól; **C3 / R10 / C1 0,7–0,8 mm-re a jobb éltől → ott nincs panel-fül** |
| PD (CH224A) | U2, R2, R3, C2 | F | U2 (40,75; 31,05) 180°; R2 (39,75; 35,55); R3 (37,3; 35,5); C2 (42,6; 36,4) | jobb, a J1 alatt |
| Buck | U4, L1, C5, C6, C8–C13, R14–R16 | F | **U4 (29,4; 25,74), L1 (31,4; 30,02) −90°**; C5 (27,35; 20,45), C6 (30,65; 20,5), C8 (25,46; 26,25), C9 (27,26; 26,465), C10 (33,17; 24,2), C11 (32,85; 26,45), C12 (27,55; 29,74), C13 (25,48; 29,74), R14 (27,915; 23,62), R15 (30,965; 23,62), R16 (26,6; 32,48) 180°; udvar x 24,4–34,4, y 18,1–33,5 | középen-jobbra, a modul (B) mögött; **8. kör átrendezés**: C9 a VIN/GND lábaknál (forró hurok 1,44 mm²), R14/R15 az FB-nél, C10/C11 az SS / BST lábaknál, SW csak F-en |
| VBUS monitor | R12, R13, C7, D2 | F | x 20,2–26,9, y 32,9–34,7 | D2 → DNP (2026-10-10) |
| NTC | TH1, R33, C26 | F | TH1 (22,0; 29,1), R33 (23,5; 30,2), C26 (20,0; 23,0) | |
| B2B | J5 | F | (22,5; 40,2), 90° | alsó él, vízszintes |
| microSD (DNP) | J3, U8, C60–C63, R60–R66 | F | J3 (9,0; 25,0) bal él; U8 (10,2; 35,4); felhúzások x 19,5–22,7, y 20,1–30,0 | R27 (SD_EN 100k, FIT) **(7,3; 37,93)** 90° (8. kör: MH3 udvar) |
| IR ág (DNP) | U7, R71–R73, C70, C71, TP8A/B | F | x 31,0–42,75, y 38,45–43,7; U7 (33,95; 39,3), R72 (42,6; 39,2), **R73 (42,75; 42,8)**, **C71 (35,25; 43,7)** | jobb-alsó, a J5 mellett; R73 / C71 kissé mozdult (MH4) |
| Rd / CC-tap (DNP) | R4, R5, R35, R36, C29, C30 | F | **R4 (2,15; 43,9)**; R5 (12,6; 40,4), R35 (12,6; 42,1), **R36 (12,9; 43,75)**; **C29 (10,1; 41,6) −90°, C30 (9,6; 43,9)** | bal-alsó; a CC1 → R4/R35 és a CC1_ADC réz eltávolítva (05 §0.1); 8. kör: MH3 körül arrébb |
| Szerelőfuratok | MH1–MH4 | NPTH | (5,75 / 39,25; 8,25 / 41,75) | középpont (22,5; 25,0) – `05` §3.1a; gyári `MountingHole_2.2mm_M2` (maszk = furat, udvar r 2,45 F-en); alátét: nylon az MH1/2/4-en, az MH3-on nincs (`05` §3) |

**Mozgások a 2026-10-10-i táblához képest (8. kör, pcbnew-összevetés a javítás előtti lappal):** C4 F → **B** (43,4; 18,65 → 42,9; 16,2); **C14 új** (F, 42,675; 16,0); C3 (y 11,4 → 9,45); R10 (43,4; 15,6 → 43,8; 12,75); R9 (y 16,35 → 16,2); C1 (43,6; 24,8 → 43,8; 26,75); buck: U4, L1, C6, C8–C13, R14–R16; C20–C23 (x 12,0–19,8 / y 41,3–43,4 → P84–P86 alá); C50, R27; DNP: C27/C28 (y 34,5 → 34,02), C29, C30, C71, R4, R36, R73. Nem mozdult: a `05` §3.1a interfész-elemei (kontúr, MH, J1, J2, J4, J5, J7, SW1–3, D20/R30, U1, J3), U2/U3/U5/U6, TP-k. Értékváltozás: R28 100k → 10k; DNP-állapot: R23/C25 → FIT, D2 → DNP.

Eltérés a fenti v0.6 ASCII-javaslattól: a TP-rács nem a jobb-felső sarokban, hanem a jobb-alsó negyedben van (B); az RF/J4 a bal-alsó negyedben, a státusz LED a bal él felső harmadában; a táp-blokk (eFuse jobb-felső, CH224A jobb, buck középen) a 2026-10-10-i átrendezés szerint.
