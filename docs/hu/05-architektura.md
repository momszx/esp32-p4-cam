# 05 – Rendszerarchitektúra (v0.6 as-built)

Dátum: 2026-10-09 · as-built frissítés: 2026-10-10 · **végső rev A as-built: 2026-10-11** · Státusz: **v0.6 végső as-built – a §0.1, §0.2, §3, §3.1, §3.1a, §4.1, §6, §13, §15 a 8. kör (javító körök) és a 9. kör (végső többagentes review, feltételes GO) mért állapotára igazítva**; előtte: **v0.6 as-built – a §0.1, §3, §3.1, §5, §6, §12 a MAIN v0.6 lapjához (45×45, 4 réteg) igazítva a 7. kör NYÁK-review alapján**; előtte **v0.5 – az 1–3. review kör és a 4. kör (R4: diagram visszaellenőrzés, `08` hibalista) tételei beépítve; a Rev A terv a §0-ban** (`90-review-log.md`); floorplan-forrás: `06-floorplan-vazlat.md` (v0.3); BOM / kapu-lap: `07-bom-terv.md`
Ez a dokumentum **felülírja** a 01–04 dokumentumok ajánlásait, ahol ellentmondás van.
Jelölés: **[NEM ELLENŐRZÖTT]** = saját tudás / becslés, primer forrással még nem igazolt. Ami nincs jelölve és nem E-tény, az tervezési döntés. **Notáció:** modul pad = **"P" előtag** (P2, P41–P46, P50/P51, P66, P82); processzor láb = **"GPIO n"**. (A padszámok a Waveshare pinout táblából származnak – **E20, primer forrás**; a *térbeli* padtérkép, azaz melyik pad melyik élen/sarokban van, feltételezés, lásd 14.)

Változások v0.1 → v0.2: USB-C PD bemenet eFuse/OVP-vel, széles bemenetű buck; MAIN kétoldalas 45×45 mm, 1,0 mm; modul a hátoldalon; IR driver + ICR a FRONT lapon; SD domain-javítás (VO4); GPIO újraosztás; OTA; új szekciók (tápfa, hő, stream, FW/OTA, helyreállítás, tesztpontok, bring-up, gyári teszt, layout, padtérkép). Ház: halasztva.
Változások v0.2 → v0.3 röviden: **VBUS max 9 V** (PD 9 V, 5 V fallback; "5–12 V" törölve); eFuse paraméterek (OVP/UVLO/ILIM/reverse-blocking/auto-retry) és kapacitás-költségvetés; **CH224A + PG → GPIO + VBUS_SW ADC**, külső Rd tilos; CC-tap átméretezve; **FULL/MID/LOW tápmódok** (boot mindig LOW, ≥1,5 s settle); tápbüdzsé újraszámolva (4,5 V, η 0,82, nappali csúcs, LOW csúcs); USB ESD 3,3 V array; **IR külön high-side kapcsoló** + driver Vin 4,5–9,45 V kritérium, soros NFET dimming, LEDC ≥40 kHz; ICR H-híd 3V3-ról; CAM_3V3 load switch kötelező; supervisor; CSI rétegváltás-szabály (symmetric via-pár); GND-pour szabály; **stack-rés 7 mm**, négyzetes 16×16 lencse-kivágás; strapping tábla + ellenőrzés; EMC alszekció; NTC + hőkeret; PD hard-reset és áramszünet-tűrés tesztek; C6 OTA bring-up kapu; §17/§19 frissítve.
Változások v0.3 → v0.4 röviden: **új §0 Rev A terv** (cél, Fit/DNP tábla, kapuk G0–G6, beszerzési lista); **E20** teljes pad-térkép → minden TBD pad kitöltve, a CSI pad-sorrend eltérése a J2-től jelezve (CLK P/N fordított, pár-sorrend D0–CLK–D1 vs D0–D1–CLK); független tápút (DNP bypass-ok, TP4 betáp; K-1); IR ág: 2. eFuse / biztosított 0 Ω (K-3); a hibás "20 V esetben eFuse OVP véd" mondat javítva, a TVS az eFuse előtt van (K-4); ICR csak rev B (K-5); RF/antenna döntés a modul sematikája után (K-6); hivatalos bring-up = MAIN önállóan standard FFC-vel (K-7); modul-forrasztás és EDA/folyamat (§3.1; K-10, K-18); DNP blokkok: supervisor, CC-tap, SD, C6/UART0 header (K-14..K-17); kamera alatti magasság-limit **G − 3,2 − 0,5 = 3,3 mm** (G = 7); a "CC-tap ~5 %" állítás törölve; tápmódonkénti minimum forrás (4.3); `00-K8` / `06-K8` hivatkozás-előtagok; C6_IO8 felhúzás mindenhol kötelező; az 1,0 mm CPWG-számok a 0,8 mm sorokból származtatva → field solver; **új `07-bom-terv.md`**.
Változások v0.4 → v0.5 röviden (R4, `08` hibalista): **IR ág rev A-ban teljesen DNP** (a "biztosított 0 Ω" szöveg javítva); **TP-terv**: hátoldali pogo csoport TP1–TP7, TP9–TP17, TP9 és TP16 kettéosztva (18 pad, ebből TP3 = GND, + 2 GND pad), TP8 front/DNP; **minden 100k lehúzás a MAIN hátoldalon** (K-7); **státusz LED a MAIN hátoldalon** (GPIO 6), J5.17 tartalék; **CC ADC kikerült a rev A boot-sorrendből**; tápfa: nyers VBUS → CH224A VDD, NTC osztó, VEML7700, TVS + ESD a hátoldalon (VBUS ≥2 via-n a front eFuse-hoz); §0.1 kiegészítve (VO4, strap, I2C, ESD, shield RC, Rd); **J7 = 1×9**; "GPIO 54 / C6_EN (P82)" felirat (Q2) mindenhol; **új kapu G5b**; a **CSI/J2 döntés G3-ba került** (a G2–G3 körkörösség megszűnt); §5: nem használt padok; §6: J3, J4, J6, J7 pin-táblák; §0.4: Q26, Q15 👤.
Változások v0.5 → v0.6 as-built (2026-10-09/10; a NYÁK-ról mérve, `90-review-log.md` 7. kör): **MAIN 45×45 mm, 4 réteg** (a 60×50 / 2 rétegű rev A felülírva, 00 K4); **új §3.1a: befagyasztott mechanikai interfész** (M2 raszter középpontja (22,5; 25,0) – 2,5 mm-rel a lapközép alatt; J2, J5, J1, J4, J7, SW1–3, D20 koordináták); §5 GPIO v0.6 a modul padjairól ellenőrizve; §0.1: 2026-10-10-i delegált döntések (R23/C25 FIT, D2 DNP, R28 10k, kamera vezérlő-ESD és SD ESD → rev B, DNP-csonkok eltávolítva); §12: as-built TP-lista (12 pad); §6 J7 / J2 / J4 as-built.
Változások v0.6 → v0.6 végső as-built (2026-10-11; `90-review-log.md` 8–9. kör): **C14 1 µF / 25 V az U3 OUT-on (új FIT)**; R23/C25 FIT, D2 DNP, R28 10k a sémában és a lapon is átvezetve; **G4 rev A-ra lezárva** (72 FIT tétel LCSC-számmal, `07`); J2 = TE 1-84953-5 (megrendelt alkatrész), J5 = Hong Cheng pár (Q17 nyitott); MH = gyári `MountingHole_2.2mm_M2` + alátét-szabály; stackup / ENIG / impedancia a lapfájlban; D1 TVS helye elfogadott eltérés; **USB csak FS**; CSI as-built hosszak és elfogadott skew (§13); **rendelés előtti kapu** (refill + DRC + `--check-zones`, §3.1); bring-up: első táp előtti mérések, U1 / J1 kézi forrasztás, rev A FW-szabályok, G5b CSI soak teszt (§15).

## 0. Rev A terv (v0.5) – bizonyító prototípus

**Cél:** a **magútvonal bizonyítása**: USB-C PD (9 V) → eFuse → buck 3V3 → P4 modul → OV5640 MIPI → ISP → H.264 → RTSP → esp-hosted C6 WiFi, 24 órás folyamatos működéssel. **Sikerkritérium:** stabil stream (a G0-n mért legjobb felbontás/fps, cél 1080p30), 24 h reset nélkül, 9 V PD tárgyalás + PG helyes, PD hard reset ×20 túlélése. **Nem cél rev A-ban:** éjjellátó (IR/ICR), microSD, MID mód, zárt házas hőtűrés, végleges mechanika. Ami nem a magútvonalhoz kell, az **footprint-tel jelen van, de DNP** (rev B-ben újratervezés nélkül beültethető).

- **Hivatalos bring-up konfiguráció (K-7):** a **MAIN önállóan**, a kamera **szabványos 50–100 mm FFC-n**, nyitott (nem összezárt) stack. A stack-et (FRONT + 25–30 mm FFC) csak **stabil kép után** zárjuk.
- **Rendelési sorrend (K-13):** **MAIN először**; a FRONT később (G6), mert a kamera STEP-jétől függ (kivágás, datumok, rés).
- **Lapméret (K-12):** ~~rev A MAIN = 60×50 mm, 2 réteg (Q22)~~ → **felülírva (tulajdonosi döntés 2026-10-09, 00 K4): a rev A MAIN = 45×45 mm, 4 réteg** (JLC04101H-3313A, 0,97 mm; §3.2). A 60×50 / 2 rétegű változat archív (`kicad/archive/MAIN_2L_60x50_2026-10-09/`, nem teljesen huzalozott). A FRONT 45×45. **A FRONT és a ház felé a befagyasztott interfész a §3.1a as-built táblája** – a szerelőfurat-raszter **nem** a lapközépre szimmetrikus (középpontja (22,5; 25,0), a lapközép (22,5; 22,5)).
- **Mód-logika (K-15):** boot mindig LOW; **FULL** csak ha ≥1,5 s settle után VBUS_SW ≥ 8 V (ADC + PG), különben LOW. MID nincs (a CC-tap DNP): 5 V/1,5 A forráson LOW-ban fut.
- Minden becslés **[NEM ELLENŐRZÖTT]**, amíg a G0 mérései nem cserélik le.

### 0.1 Fit vs DNP (rev A)
| Blokk | Rev A | Megjegyzés |
|---|---|---|
| USB-C J1 (16 pin) + 3,3 V ESD array + TVS (SMAJ10A osztály) | **FIT** | pin map: `07` §3; ~~terv: a TVS + ESD a MAIN hátoldalon, a J1 mellett~~. **As-built (végső, 9. kör): a D1 TVS (SMAJ10A-13-F) a B oldalon az eFuse (U3) bemeneténél / alatt (40,5; 13,5), egyenesen 6,8 mm-re a J1-től – elfogadott eltérés (tulajdonosi aláírás, `90` 9. kör)**; a D1.1-nek saját B-útja van a J1 A4/B9-hez (~8 mm); az **U5 USB ESD (F, (34,0; 21,2))** és az R1/C1 shield RC (F) a J1 mellett. J1 köpenylábak forrasztása: §3.1, §15 |
| J1 shield: 1 MΩ ‖ 4,7 nF → GND | **FIT** | `07` #53; a C1 **200 V-os** alkatrész (YAGEO C596328; a séma Value-mezője még „50V”) |
| CH224A + feszültség-strap + PG → GPIO 31 | **FIT** | strap; PG: open-drain, aktív alacsony (E22) – a G1 méréssel igazolja |
| eFuse (állítható OVP/UVLO/ILIM, reverse-blocking, auto-retry) | **FIT** | **TPS259470ARPWR (C3662799)** – `07` §0 |
| **C14 1 µF / 25 V X7R 0603 az U3 OUT-on (VBUS_SW → GND)** | **FIT** (2026-10-11, új) | TI 8.4.1 (≥1 µF az eFuse kimenetén); F (42,675; 16,0), 1,14 mm-re az U3.6-tól; 9 V-on effektív <1 µF – opcionális BOM-csere 2,2 µF / 25 V X7R azonos lábképen |
| VBUS → VBUS_SW 0 Ω / forrasztóhíd az eFuse körül | DNP | bring-up / eFuse-hiba bypass (K-1) |
| 2× 5,1k Rd footprint | DNP | **csak ha a CH224A nincs beültetve – soha egyszerre** (K-1) |
| Buck 3V3 + kimeneti 0 Ω + TP4 | **FIT** | a 0 Ω kivétele után TP4-en bench betáp; **USB-vel egyszerre soha** (K-1) |
| P4 modul + 3V3 bulk (47 µF + 10 µF + 100 nF) | **FIT** | kézi forrasztás, 3.1 |
| CAM_3V3 load switch + 0 Ω mérő-jumper | **FIT** | CT / slew: `07` §4 |
| J2 FPC 15 pin, J5 B2B | **FIT** | a MAIN FRONT nélkül is működik (K-7). ~~J2 lábkép = helyőrző~~ → **J2 = TE 1-84953-5 (C5164008, TOP contact) – a lábkép maga a megrendelt alkatrész**; kontakt-oldal **Q6**: a kamera első bekapcsolása előtt dől el (a bottom-contact 1-84952-5 azonos lábképű → alkatrész- / kábelcsere, nem újratervezés); **J5 = Hong Cheng HC-PZ127-7.2L-2x10PS (C41375929)**, generikus land, **Q17 nyitott** (`07` §0) |
| VBUS_SW ADC osztó (R12 200k / R13 54,9k + C7 100 nF), NTC (ADC2), PG pull-up | **FIT** | **D2 (BZT52C3V6, VBUS_MON clamp Zener): DNP** (2026-10-10) |
| BOOT / RESET / USER gomb (SW1–SW3, B oldal); hátoldali TP-k **as-built: TP1–TP7, TP16A/B, TP17–TP19 = 12 pad** (TP16A = ESP_EN, TP16B = GPIO 35; GND: TP3, TP18, TP19). ~~TP9a/b, TP10–TP15~~ törölve (2026-10-09): a C6 / UART0 hozzáférés csak a J7 padsoron | **FIT** | a TP8A/B külön sor (front oldal, DNP); lista + koordináták: §12 |
| Státusz LED (0603 + soros R, GPIO 6) | **FIT** | MAIN hátoldal, a modul közelében; J5.17 tartalék (NC) |
| VO4: 1 µF + TP7 | **FIT** | külső forrás tilos |
| Strap felhúzások: GPIO 36 10k, C6_IO9 10k, C6_IO8 10k | **FIT** | §5.1; `07` #28 |
| Lehúzások: **100k** – GPIO 26, 27, 28 (R24–R26), 53 (SD_EN, R27); **10k – GPIO 4 (CAM_3V3_EN, R28; 2026-10-10, korábban 100k)** | **FIT** | as-built: **MAIN előlap (F)**, a modul alatt / a cél-IC mellett (K-7 teljesül: a MAIN önállóan működik); a GPIO 32 (IR_SW_EN, R29) lehúzása az IR ággal együtt DNP |
| UART0 soros R 1–4,7k ×2 (GPIO 37/38; as-built R40/R41 1k → J7.7/J7.8) + GPIO 33 (USER, v0.6) 100 nF (C40) | **FIT** | §5, §5.1 |
| I2C felhúzás (SDA/SCL, MAIN) | **DNP** | a kamera I/O szintjének ismeretéig (G3); addig csak a CH224A belső felhúzói → **rev A FW: I2C 100 kHz** (§15) |
| J2 vezérlő-jel ESD (CAM_PWDN = CAM_IO0, SCL, SDA) | ~~FIT~~ → **rev B (formálisan halasztva, 2026-10-10)** | nincs a sémában; a J2 kontakt-oldala (Q6) nyitott, a J2 környéke zsúfolt; a vonalak FFC-n belüliek – bring-upnál ESD-óvatosság a kézi FFC-csatlakoztatásnál. `07` #38 |
| CC1/CC2 ESD clamp | **rev B** (2026-10-11) | nincs a sémában; a CH224A CC abs max 32 V; rev A-ban a CC csak J1 → U2 (CC1 10,97 / CC2 7,8 mm) |
| Supervisor (nyílt-drain változat) + 0 Ω → ESP_EN | ~~DNP~~ → **nincs rajzolva (rev B)** | K-14; a sémán csak TODO-szöveg (nincs ellenőrzött szimbólum / lábkép) |
| **ESP_EN RC: R23 10k → 3V3 + C25 1 µF → GND** | **FIT** (2026-10-10; korábban DNP) | Q3 (van-e EN RC a modulon) nyitott; egy dupla RC csak kissé módosítja az időállandót, a hiányzó felhúzás viszont nem induló lapot jelent (az ESP_EN-t más nem húzza fel); B oldal (3,2; 29,55) / (3,2; 31,25) |
| CC-tap (100k + 10 nF + 3,6 V Zener ×2) | **DNP** | K-15 |
| u.FL + π-háló + CPWG | footprint FIT, minden elem 0 Ω / DNP-képes | K-6; G2 dönt: a modul saját IPEX-e vagy u.FL. **As-built: J4 + R34 (0R) FIT, C27/C28 DNP**; 0,302 mm-es microstrip a B rétegen (ref. In2), ~7 mm sáv (U1 P2 → J4.1 út 7,96 mm), via nélkül; **9. kör: In2 100 % GND alatta, GND kerítés 10 / 14 via 1,0 / 1,5 mm-en belül** |
| C6 UART/EN/IO9 + UART0 header J7 | **J7 = 9 SMD pad-sor, 1,27 mm (pad 0,85×1,6), DNP** (header nincs beültetve); a C6 pogo padok (TP10–TP13) törölve | K-17; as-built: B oldal, felső él (22,5; 2,0), vízszintes (§3.1a) |
| microSD blokk (J3, SD_3V3 switch U8, felhúzások) | **DNP** (footprint marad) | K-16; engedélyezés később. **SD ESD: lábkép nincs a sémában → rev B** (2026-10-10). Az R27 (SD_EN 100k lehúzás) FIT |
| IR ág: 2. eFuse / high-side kapcsoló (vagy biztosított 0 Ω) + shunt + TP8 + IR_SW_EN lehúzás (GPIO 32) | **DNP** – a footprint marad | rev A: az IR_VIN táp nélkül, a FRONT-tal együtt (G6); a TP8 a front oldalon |
| FRONT lap: IR LED + driver + NFET, mikrofon, VEML7700 (DNP) | **később (G6)** | külön lap, a kamera STEP után; a státusz LED a MAIN-en van |
| ICR (DRV8837, J6) | **DNP / nincs** | rev B (K-5) |
| Kamera | bármely, a 7. követelményeit teljesítő modul, **NoIR vagy fix lencse** | K-5 |

**Delegált tulajdonosi döntések – 2026-10-10 (7. kör review, `90-review-log.md`):**
1. **R23 10k + C25 1 µF (ESP_EN RC) → FIT** (electrical-02; Q3 ettől függetlenül nyitott).
2. **D2 (VBUS_MON Zener) → DNP**: a BZT52C3V6 szivárgása a 43,1 kΩ-os (200k ‖ 54,9k) csomóponton már ~2,7 µA-nél elviszi a 8 V-os FULL/LOW küszöb tartalékát (8,55 V-os PDO-alsóhatárnál ~0,12 V az ADC-n) [szivárgás-adat NEM ELLENŐRZÖTT]; a P4 lábat a 43 kΩ forrás-ellenállás eleve korlátozza. ADC-kalibráció a G5b-n.
3. **R28 100k → 10k** (CAM_3V3_EN lehúzás): ha a GPIO 4 (MTMS) reset alatt belső felhúzással indul (~45 kΩ, [NEM ELLENŐRZÖTT]), 100k-val ~2,3 V jutna a TPS22917 ON lábára (kamera reset alatt bekapcsolna, „boot mindig LOW” sérül); 10k-val ~0,6 V. Ellenőrzés a G5b-n: CAM_3V3 a TP5-ön reset alatt.
4. **Kamera vezérlő-jel ESD (CAM_PWDN / SCL / SDA) → formálisan rev B**: nincs a sémában; a J2 kontakt-oldala (Q6) nyitott, a terület zsúfolt.
5. **SD ESD lábképek → rev B** (az SD blokk rev A-ban amúgy is DNP).
6. **DNP-csonkok eltávolítva a rev A layoutból (EMC):** **CC1 → R4/R35** (~97 mm-es élmenti ág), **CC1_ADC → C29/R35/D21** (a hálónak – a GPIO 21 / P30 padtól – nincs reze), **VBUS_SW élcsonk → R73** (~44,5 mm, In2). **Ezeket az alkatrészeket beültetés előtt újra be kell kötni**, a korábbi 3 DNP-szakadással együtt (**CC2 → R5/R36, U7 GND, VBUS_SW → U7**). ~~A NYÁK-on így 9 bekötetlen ratsnest-elem van~~ → **a végső lapon 12 bekötetlen elem (kicad-cli DRC, 2026-10-11), mind DNP-padon** (a CC2_ADC ág is ide tartozik). A K-1 Rd-tartalék (R4/R5) csak mindkét CC-ág bekötése után működik (különben egy dugó-orientációban sem garantált).

~~**Átvezetés:** a sémában (2026-10-10) az R23/C25 még DNP, a D2 FIT, az R28 100k értékű – …~~ **Átvezetve (8. kör, 2026-10-11):** séma, NYÁK-attribútumok és BOM a fenti döntések szerint (R23/C25 FIT, D2 DNP, R28 10k), + az új C14; ERC 0, DRC 0 hiba (refill-lel), séma ↔ lap paritás 0.

### 0.2 Kapuk (sorrendben; a következő csak az előző zárása után)
| Kapu | Tartalom | Kilépési feltétel |
|---|---|---|
| **G0** | **Dev-kit stream + áram (K-2):** Waveshare ESP32-P4-Module dev board vagy ESP32-P4X-Function-EV-Board + jelölt kamera: OV5640 MIPI → ISP → H.264 → RTSP **esp-hosted C6 WiFi-n**; **24 h soak**; áramfelvétel mérése állapotonként (idle, stream, WiFi TX csúcs, kamera be/ki); RSSI-teszt a jelölt antennákkal; **sdkconfig + komponens-verziók befagyasztása** (IDF, esp_cam_sensor, esp-hosted, esp-video) | stabil stream 24 h; a mért táblázat **lecseréli a 4.3 becsléseit**; a lánc **még soha nem futott** a tervezés eddigi részében – ez az első bizonyíték |
| **G1** | **CH224A breakout bench teszt (K-4):** MacBook, olcsó PD töltő, USB-A→C kábel; 9 V PDO tárgyalás, feszültség-strap, PG polaritás / szint, DP/DM NC viselkedés az USB-Serial-JTAG mellett | 9 V stabil, PG szint ismert, nincs 20 V; strap-tábla az adatlapból igazolva (Q13) |
| **G2** | **Modul sematik + footprint + antenna-döntés:** Waveshare modul sematik elolvasása a MAIN routing előtt (Q1–Q3, Q9–Q11: VDDPST_5/VO4, EN RC, C6_EN, MIPI PHY táp, RF út, esp-hosted reset); footprint import (a G2 **csak** a modul footprintet / sematikát szállítja; a CSI térbeli pad-sorrend innen ismert, de a J2-döntés a **G3-ban** van); **antenna: ha a modul saját IPEX-e használható (a modul a hátoldalon, elérhető), rev A-ban azt használjuk** (K-6) | footprint + 1:1 papírpróba; antenna-döntés; supervisor beültetési döntés |
| **G3** | **Kamera modul befagyasztva:** NoIR / fix lencse, 15 pin, onboard osc + LDO, CAM_IO0 polaritás, I/O szint, **STEP**, FFC hosszak (bring-up 50–100 mm; zárt 25–30 mm) | egy modul kiválasztva; GPIO 23 pull (Q5) eldöntve; **a végleges CSI pad-sorrend / J2 pinout döntés (Q24)**: a kiválasztott kamera / FFC sorrendje + a G2 footprint térbeli sorrendje + a lane / polaritás csere TRM-ellenőrzése + via-keresztezés (§6, §13) |
| **G4** | **BOM-lap kész** (`07`): MPN / LCSC# / footprint-forrás minden alkatrész-osztályra + ellenállás-számítások (buck FB/L/Cout, eFuse OVP/UVLO/ILIM, IR áram/shunt, PG pull-up sín, CH224A strap) **a sematik előtt** (K-8) | nincs TBD a rev A FIT sorokban – **✅ rev A-ra lezárva 2026-10-11** (72/72 LCSC; nyitott tulajdonosi döntés: Q6, Q17 – `07` §0) |
| **G5** | **MAIN sematik → layout → DRC → 1:1 print → rendelés** (JLC; modul utoljára kézzel) | MAIN megrendelve – **csak a rendelés előtti kapu után** (refill + mentés a projektmappában, DRC refill nélkül 0 hiba, `--check-zones` Gerber; §3.1, `90` 9. kör) |
| **G5b** | **Bring-up – MAIN önállóan, kamera 50–100 mm FFC-n (§15)**: a 15. szakasz 0–7. lépése, nyitott stack; **+ CSI soak teszt hibaszámlálókkal (§15 7a)** | a §0 sikerkritérium: stabil stream (G0-n mért legjobb felbontás/fps), 24 h reset nélkül, 9 V PD + PG helyes, PD hard reset ×20 túlélve; CSI hiba- / CRC- / ECC-számláló ≥1 h alatt 0 |
| **G6** | **FRONT** (IR, mikrofon; ICR rev B): a **G5b** zárása (a MAIN stabil képe) után, a kamera STEP-pel; IR bench teszt árnyékoló csővel (K-19) | FRONT megrendelve |

### 0.3 Beszerzési lista (K-9, K-2, K-4, K-6)
| Tétel | Db | Cél | Kapu |
|---|---|---|---|
| Dev kit (Waveshare ESP32-P4-Module dev board **vagy** ESP32-P4X-Function-EV-Board) + jelölt kamera | 1 | stream-lánc, áram, RSSI | G0 |
| ESP32-P4 modul (Waveshare, 88 pad) | 3–4 | MAIN + forrasztási próba + tartalék | G2/G5 |
| Kamera modul jelöltek (15 pin MIPI, onboard osc/LDO, NoIR vagy fix lencse) | 2–3 | lemérés, STEP, egy befagyasztása | G3 |
| FFC minták: szabványos 50 és 100 mm (15 pin, 1,0 mm, egyenes) + 25–30 mm egyedi / rövid flex | 3 + 2 | bring-up / zárt stack | G3 |
| B2B 2×10 1,27 mm párosított pár, 7 mm magasság (**2026-10-11: BOM-ban Hong Cheng C41375929 + C27985222, 5,3 mm; Samtec 7,47 mm alternatíva – Q17**) | 2–3 pár | stack, tűrés, wipe (Q17) | G3/G4 |
| USB-C 16 pin receptacle (THT shell) minták | 3–5 | footprint, forrasztás | G4 |
| microSD kártya (márkás) | 2 | rev B SD | – |
| IR LED 850 nm 3535 | 8–10 | rev B / FRONT | G6 |
| PD trigger / analyzer, amely **hard reset-et tud kényszeríteni** | 1 | PD hard reset ×20 (4.1, 15.) | G1 |
| USB teljesítménymérő (V/A) | 1 | áram, UVLO | G1 |
| USB-UART (3,3 V logika) | 1–2 | C6 UART flash | G5 |
| CH224A breakout (+ MacBook, olcsó PD töltő, USB-A→C kábel) | 2 | strap / PG / DP-DM teszt | G1 |
| Forrasztópáka + fluxus, hot-air / előmelegítő, forrasztószalag | 1 | modul kézi forrasztás (3.1) | G5 |
| 1:1 3D print (stack-makett: 2 lap, 4 távtartó, kamera) | 1 | mechanika, pin 1 | G3 |
| Antenna (2,4 GHz, IPEX Gen1 / u.FL) | 2 | RSSI összehasonlítás | G0/G2 |
| Árnyékoló cső / ablak-távtartó (fekete) | 1 | IR bench teszt (K-19) | G6 |

### 0.4 Nyitott tulajdonosi döntések
- ~~**Q22:**~~ ✅ **lezárva: rev A MAIN 60×50 mm** – **felülírva 2026-10-09: MAIN 45×45 mm, 4 réteg (00 K4; §3.1a)**. Eredeti kérdés: rev A MAIN nagyobb (pl. 60×50 mm), **azonos M2 raszterrel és J2/J5 koordinátákkal**? (a 45×45 marad a cél; a nagyobb lap a bring-up és a forrasztás hozzáférhetőségét javítaná)
- **Q26:** EDA = **KiCad** ✅ (2026-10-09); nyitott maradék: USB-C THT shell JLC-beültetése → **2026-10-11: a J1 köpenylábak paszta nélküliek (`attr smd`), a JLC reflow forrasztatlanul hagyja őket → rendeléskor döntés: JLC kézi / szelektív forrasztás, vagy a tulajdonos forrasztja az első kábel-bedugás előtt (§15).**
- **Q6, Q17** (J2 kontakt-oldal, J5 magasság) és az **U5 klón-lábkiosztás**: `07` §0; a tulajdonosi tételek teljes listája: `90-review-log.md` 9. kör.
- **Q15:** 👤 beltéri v1 (hat a hőkeret T_amb-jére és a LED-választásra).

## 1. Böngészővel ellenőrzött tények (primer forrás, 2026-10-09)

| # | Tény | Forrás |
|---|---|---|
| E1 | Waveshare **ESP32-P4-Module**: ESP32-P4NRW32 (32 MB PSRAM in-package) + 16 MB flash + **ESP32-C6H8 a modulon belül, SDIO-n** | waveshare.com/wiki/ESP32-P4-Module |
| E2 | Modul méret **25 × 25 × 3,3 mm**, 88 castellated pad, **1,0 mm** osztás (alsó padok: land pattern zipben ellenőrizni) | uo. (size.jpg) |
| E3 | Modul táp: **ESP_3V3 (P85, P86)** + **VBAT (P84)** → 3,3 V. Belső DCDC/LDO a modulon → nekünk csak 3,3 V kell | uo. pinout |
| E4 | Kivezetett: MIPI-CSI 2 lane (P41–P46), MIPI-DSI, USB HS (P48/P49), USB-Serial-JTAG / FS PHY GPIO24/25 (P50/P51), GPIO0–13, 20–23, 26–54, ESP_EN (P87), ESP_LDO_VO4 (P66) | uo. |
| E5 | **Nincs kivezetve** GPIO14–19 → belül a C6 SDIO linkje foglalja (**következtetés**, nem közvetlen állítás) | uo. (következtetés) |
| E6 | C6 programozó lábak kivezetve: C6_U0RXD (P4), C6_U0TXD (P5), C6_IO9 (P9, BOOT), C6_IO8 (P10; a wiki 10k felhúzást ajánl → **nálunk kötelező**), C6 JTAG IO4–7 | uo. |
| E7 | C6 antenna: **LNA_OUT (P2)** padra van kötve alapból; IPEX Gen1 csak 0 Ω átforrasztással (→ rev A: ha a modul hátoldali és az IPEX elérhető, azt használjuk, §0 G2) | uo. |
| E8 | P4 BOOT: **GPIO35** low bekapcsoláskor = download (ha GPIO36 felhúzva); **GPIO36 10k felhúzás 3,3 V-ra** ajánlott | uo. |
| E9 | GPIO39–48 IO tápja az **ESP_LDO_VO4** (alap 1,8 V, szoftverből állítható) | uo. |
| E10 | P4 USB-Serial-JTAG: **GPIO24 (D−) / GPIO25 (D+)** (alternatíva 26/27); flash + konzol + JTAG, auto download mode → **nem kell USB-UART chip** | IDF docs usb-serial-jtag-console (esp32p4) |
| E11 | esp_cam_sensor: **OV5640 támogatott MIPI és DVP** módban is P4-en (RGB565/YUV422 kimenet). SC2336, OV5647, OV5645, GC2145 stb. is | github espressif/esp-video-components esp_cam_sensor/README; esp_cam_sensor README, master ág, 2026-10 |
| E12 | P4 ISP max bemenet 1920×1080; MIPI-CSI max **1,5 Gbps/lane** | uo. |
| E13 | Espressif EV board kamera csatlakozó: **1.0K-GT-15PB** (15 pin, 1,0 mm FPC), egyenes ("forward") kábel | esp-dev-kits P4-Function-EV-Board v1.5.2 user guide |
| E14 | EV board v1.5.2 **EOL**; aktuális: ESP32-P4X-Function-EV-Board (chip rev v3.x) | uo. |
| E15 | EV board: microSD 4-bit, I2C a GPIO7/8-on (J1 header), UART0 = GPIO37 TX / 38 RX | uo. |
| E16 | P4 SDMMC: **slot1 = GPIO-mátrix** (nem-UHS), **slot0 = UHS-I, IO_MUX fix lábak**; IO feszültség kívülről a **VDDPST_5 (SD_VREF)** lábon. Nem-UHS esetén mehet fix 3,3 V-ra, vagy on-chip LDO-ról (`sd_pwr_ctrl_new_on_chip_ldo`) | IDF docs sdmmc_host (esp32p4) |
| E17 | SD slot0 lábak P4-en: **CLK=43, CMD=44, D0=39, D1=40, D2=41, D3=42**; IDF példa: on-chip **LDO ID 4** (= VO4), kártya táp-reset default **GPIO45** | esp-idf examples/storage/sd_card/sdmmc Kconfig + esp-hosted-mcu Kconfig.host.sdio |
| E18 | esp-hosted P4 + C6 (EV board): SDIO **slot1**, CLK=18, CMD=19, D0=14, D1=15 (D2/D3=16/17), **C6 reset = GPIO54** (P4 default) | esp-hosted-mcu host/mcu/.../Kconfig.host.sdio |
| E19 | esp-hosted-ben van `mcu_hosted_sdio_sdmmc_combined` példa → SD kártya + C6 SDIO együtt egy hoston támogatott | esp-hosted-mcu repo fa |
| E20 | **Teljes modul pad-térkép** (88 pad): P1 GND, P2 LNA_OUT, P3 GND, P4 C6_U0RXD, P5 C6_U0TXD, P6 C6_IO15, P7 C6_IO14, P8 C6_IO13, P9 C6_IO9, P10 C6_IO8, P11–P14 C6_IO7..IO4 (JTAG), P15 GND, P16 GPIO1, P17–P28 GPIO2..GPIO13, P29–P32 GPIO20..GPIO23, P33 GND, P34–P39 DSI, P40 GND, P41 CSI_D0N, P42 CSI_D0P, P43 CSI_CLKP, P44 CSI_CLKN, P45 CSI_D1N, P46 CSI_D1P, P47 GND, P48 USB_DM(HS), P49 USB_DP(HS), P50 GPIO24, P51 GPIO25, P52 GND, P53–P61 GPIO26..GPIO34, P62 GPIO35, P63 GPIO36, P64 GPIO37, P65 GPIO38, P66 ESP_LDO_VO4, P67–P82 GPIO39..GPIO54, P83 GND, P84 VBAT, P85 ESP_3V3, P86 ESP_3V3, P87 ESP_EN, P88 GPIO0. **Megjegyzés:** a CSI pad-sorrend D0N, D0P, **CLKP, CLKN**, D1N, D1P – a CLK pár P/N sorrendje fordított a D párokhoz képest (lásd 6. J2 megjegyzés, 14.) | waveshare.com/wiki/ESP32-P4-Module, pinout tábla (primer forrás) |

## 2. Fő döntések

| ID | Döntés | Indok |
|---|---|---|
| D1 | **Waveshare ESP32-P4-Module** bare QFN104 helyett | 2 rétegen a QFN104 + VDD_HP DCDC + flash + kristály + C6 + RF túl kockázatos (01-doc) |
| D2 | C6 = modulon belüli C6H8 | E1. Nincs SDIO routing a mi NYÁK-unkon |
| D3 | Kamera: **OV5640 MIPI 2-lane**, 15 pin 1,0 mm FPC; a modul **kötelezően** saját oszcillátorral + LDO-kkal + 3V3 bemenettel (az FPC-n nincs XCLK). **ICR-es (IR-cut) lencse: rev B-ben kötelező; rev A-ban NoIR vagy fix lencsés modul is jó** (K-5, Q5) | E11, E13, F-27, A-37, K-5 |
| D4 | Programozás: USB-C → GPIO 24/25 USB-Serial-JTAG (csak első flash); utána OTA (D8) | E10 |
| D5 | Táp: **USB-C PD sink, VBUS max 9 V**: CH224A (+PG pin → GPIO, kötelező; 9 V kérés, PC/legacy porton 5 V fallback) → ESD/TVS (SMAJ10A osztály) → állítható-OVP, reverse-blocking, auto-retry eFuse → széles bemenetű forced-PWM buck 3V3 ≥2 A (TPS62933F osztály) [alkatrészek **NEM ELLENŐRZÖTT**]. **Nincs 2. (termék-)tápbemenet**; rev A-ban csak DNP debug-utak (§0, 4.1) | E-1, E-2, E-13, E-35, B-4, B-11, K-1 |
| D6 | **2 db, ~1,0 mm FR4**: FRONT 45×45 (2 réteg, ha elég) + **MAIN 45×45, 4 réteg** (JLC04101H-3313A, 0,97 mm; §3.2) – a korábbi „rev A: 60×50, 2 réteg” felülírva (00 K4). Közös interfész (M2 raszter, J5, J2): **§3.1a as-built**. MAIN kétoldalas (lásd 3.) | P-2, P-3, P-8, 00 K4 |
| D7 | Mikrofon: PDM MEMS a FRONT-on (jobb sáv); fényérzékelés: nincs LDR, nap/éj a kamera AE/gain alapján; opcionális VEML7700 footprint (DNP), **a saját 850 nm IR LED-ektől árnyékolva** (Cu gyűrű + fekete hab / ablak-apertúra) | E-16, E-21 |
| D8 | **OTA**: P4 app 2 OTA partíció (16 MB flash); C6 slave FW esp-hosted OTA-val a P4-ről. USB csak az első flash-hez. **C6 OTA = bring-up kapu** (9., 15.) | 00-K8, A-36 |
| D9 | IR: 850 nm, 4× 3535 LED, ágankénti CC meghajtó a FRONT-on, **külön, második állítható-ILIM eFuse (≥18 V rating, ILIM 0,5–0,7 A) a MAIN-en** – a TPS22810 osztálynak nincs állítható áramkorlátja [NEM ELLENŐRZÖTT], ezért elvetve; **rev A: az egész IR ág DNP, a footprint marad** (az IR_VIN táp nélkül G6-ig; a biztosított 0 Ω csak rev B-s alternatíva); soros NFET dimming; ICR H-híd (DRV8837 osztály) a FRONT-on **3V3-ról**, **rev A-ban DNP (ICR: rev B)**. Ágtopológia a 4.2 kritérium szerint | E-9, E-10, E-19, B-14..16, B-25, K-3, K-5 |
| D10 | Ház: **később** – most csak NYÁK. Lásd 18. | |
| D11 | Firmware tápmódok: **FULL / MID / LOW**, boot mindig LOW (4.3) | B-2, B-3, B-17, B-19 |
| D12 | **Rev A = bizonyító prototípus**: MAIN először, kapuk G0–G6, DNP blokkok (§0) | K-2, K-7, K-13 |

## 3. NYÁK stack (mechanika)

Floorplan-forrás: **`06-floorplan-vazlat.md`** (terület- és magasságköltségvetés, ASCII floorplan, K1–K13). A padszámozás ott **feltételezés [F]**, a Waveshare footprint importjáig így kezelendő (14.).

```
 előre (lencse irány) ↑
 ┌──────────────────────────────────────────────┐
 │ FRONT  45×45, 1,0 mm, 2 réteg                  │ elöl: lencse-kivágás ~16×16 mm négyzet (R1), IR LED ×4 (3535),
 │                                                │       PDM mikrofon (jobb sáv), (VEML7700 DNP)
 │                                                │ hátul: kamera modul, IR CC driverek (+NFET), DRV8837 + ICR csatl. (DNP),
 │                                                │       B2B header
 └──────────────┬─────────────────────────────────┘
        B2B 2×10 1,27 mm párosított magasság 7 mm [NEM ELLENŐRZÖTT: elérhetőség]  +  4× M2 távtartó 7 mm (szerkezeti elem)
        kamera FPC: rövid flex vagy 25–30 mm egyedi kábel (kapu: Q5/Q6), a modul saját FPC aljzatából MAIN J2-be
 ┌──────────────┴─────────────────────────────────┐
 │ MAIN   45×45, 4 réteg, 0,97 mm, KÉTOLDALAS     │ front oldal (F): J2 FPC (felső él; vezérlő-jel ESD: rev B), J5 B2B (alsó él), buck + eFuse + PD IC, IR ág (2. eFuse; rev A: DNP) + shunt + TP8,
 │                                                │       CAM_3V3 switch, microSD (bal él, DNP), NTC, VBUS osztó (eFuse után), GPIO-lehúzások; kamera alatt alkatrész ≤3,3 mm
 │                                                │ hátoldal (REAR, B): P4 modul, USB-C (jobb él) + TVS, u.FL (bal él), BOOT/RESET/USER gomb (felső él),
 │                                                │       státusz LED (GPIO 6), TP-k (TP1–TP7, TP16A/B, TP17–TP19), C6/UART0 DNP padsor (J7, felső él); supervisor: rev B
 └────────────────────────────────────────────────┘
 as-built koordináták és oldalak: §3.1a (a v0.5-ös 60×50 / 2 rétegű terv felülírva)
 hátra ↓
```

| Szabály | Érték / döntés | Ref |
|---|---|---|
| Lapvastagság | **1,0 mm** mindkét lap, minden számolás erre; **MAIN as-built: 0,97 ± 0,10 mm** (4 réteg, JLC04101H-3313A, §3.2) | P-8, E-28, F-29 |
| Összeszerelési sorrend | 1. kamera FPC → J2 (ZIF a lap szélén, ≥20 mm ráhagyás) → 2. ellenőrzés (folytonosság/kép) → 3. stack zárása. **Rev A: a bring-up a MAIN-nel önállóan, szabványos 50–100 mm FFC-vel; a zárás csak stabil kép után** | P-13, K-7 |
| Gyártás | JLC SMT minden mást; P4 modul **utoljára** kézzel (3.1); **MAIN először, FRONT később** (a kamera STEP-jétől függ) | P-21, K-13 |
| **Rés (stack gap)** | **G = 7 mm**: B2B 2×10 1,27 mm header-pár, párosított magasság 7 mm [NEM ELLENŐRZÖTT: létezik-e ilyen alkatrész, tűrés ±0,2–0,3 mm, wipe]. A MAIN front oldali alkatrészek a **kamera alatt ≤3,3 mm** (= G − 3,2 − 0,5; 3,2 = kamera NYÁK 1,2 + hátoldali alkatrészek 2,0); FRONT hátoldali S-sáv (IR driver) + MAIN J2 aktuátor-zóna: 06-K13 (4,6 < 7). A modul 3,3 mm (E2) a hátoldalon | P-2, 06 §3/K13 |
| **Kamera FPC** | A hossz **kapu Q5/Q6-ban**: rövid flex (a modul saját FPC-je) vagy **25–30 mm egyedi kábel**; a korábbi "40–60 mm S-hurok" **törölve** (06-K1: ~25–33 mm felesleg nem tartható 7 mm résben). Egyenes ("forward") kábel, hajlítási R ≥2 mm. **Rev A bring-up: szabványos 50–100 mm FFC, nyitott stack** (§0); zárt stack: 25–30 mm | P-14, 06-K1, K-7 |
| Lencse-kivágás | **~16×16 mm négyzet** (R1 sarkok), marott, **nem Ø furat**; a kamera holder a kivágáson át előre nyúlik (06 "A" variáns); a **tengelyhez igazított** 14×14 mm holder 1 mm/oldal hézaggal átfér (a 19,8 mm átló csak elforgatott holdernél számít; az R1 sarok nem szűkít); végleges méret a kamera modul STEP-jével | P-24, 06-K9 |
| Rögzítés | 4× M2 távtartó, **33,5 mm közös raszter**, 2,2 mm NPTH, 3,8 mm keep-out; **a távtartó a szerkezeti elem, nem a header**. **As-built (MAIN v0.6):** MH1–MH4 = (5,75; 8,25), (39,25; 8,25), (5,75; 41,75), (39,25; 41,75), Ø2,2 NPTH – a raszter középpontja **(22,5; 25,0), 2,5 mm-rel a lapközép alatt** → befagyasztva, §3.1a. A furatok szimmetrikusra tolása ütközne (J4, TP17/TP18, JP1). ~~maszknyílás Ø3,2 (szabad GND-gyűrű)~~ → **végső: gyári `MountingHole_2.2mm_M2`** (board-only, BOM/CPL-ből kizárva): maszknyílás = furat (Ø2,2), a GND-réz r 1,36 mm-től maszk alatt → **nincs szabad GND-gyűrű, a csavar / távtartó elektromosan lebeg**; udvar r 2,45 csak az F oldalon (a B oldalt a DRC nem nézi). Jelréz a csavarfej / távtartó alatt (csak maszk szigetel): MH1 / MH2 I2C_SDA (B) 1,95 / 1,93 mm, MH2 EF_UVLO (F) 2,40 mm, MH4 I2C_SDA via 2,18 mm a furatközéptől. **Szerelési szabály (9. kör): nylon távtartó vagy nylon alátét az MH1 / MH2 / MH4-en; az MH3-on nincs alátét (a J4 GND padja 2,54 mm-re), csavarfej max. Ø4,0 mm, az u.FL kábel Ny / É felé lép ki** | P-16, P-23, mech-01, mech-04, mech-10 |
| Kamera rögzítés | 2 NPTH datum a FRONT-on | P-24 |
| IR → lencse | Cu gyűrű (IR baffle) a kivágás körül mindkét rétegen + fémezett perem; LED ≥10 mm sugárra a lencse tengelytől; LED hőterítés a hátoldali Cu-on | P-17, P-28 |
| Mikrofon | FRONT **jobb sáv** (termék-keret), a MAIN buck/induktortól (bal sáv alatt) távol (06-K7); ≥10 mm az IR LED-ektől / ICR-től; akusztikai port a FRONT-on | P-19, P-27 |
| USB-C és u.FL | **ellentétes élen** (modul forgatás-kényszer, lásd 14.); USB-C 4 THT shell láb; **modul ↔ USB-C szabad távolság ≥2 mm** a kiterjesztett forrasztó-padok után (a modul 1 mm-rel az USB-C-vel ellentétes él felé tolva, 3.1; 06-K8). ~~A TVS + USB ESD + shield RC a MAIN hátoldalon, a J1 mellett áll~~; a VBUS ≥2 via-n megy a front oldali eFuse-hoz (4.1). **As-built (végső):** J1 a jobb élen (B), J4 a bal élen (B) – ellentétes él ✅; modul-pad ↔ J1 réz-távolság **1,53 mm** (< 2 mm, dfm-08, elfogadva); a J1 homloklapja 0,55 mm-rel az él mögött (dugó-illeszkedés G3 makettel ellenőrizendő); **a D1 TVS a B oldalon az eFuse (U3) alatt, 6,8 mm-re a J1-től (elfogadott eltérés, §0.1); az U5 USB ESD és az R1 / C1 shield RC az F oldalon, a J1 mellett**; az U3 IN-re 3 VBUS via (J1 → U3.5 7,1 mΩ) | P-25, A-34, K-10, R4-21 |
| u.FL | lapszélen, húzásmentesítés; antenna: külső FPC antenna, ≥15 mm fémtől, korai RSSI teszt. **Rev A: ha a modul saját IPEX-e használható, azt használjuk; az u.FL / π-háló / CPWG footprintek minden eleme 0 Ω / DNP-képes; 2 antenna, RSSI a dev kit-en** (G0/G2) | P-11, P-12, K-6 |
| microSD | lapszélen, RF-től távol; **rev A: DNP (footprint marad)** | P-32, K-16 |
| Buck | az u.FL-lel és a mikrofonnal ellentétes sarokban | P-27 |
| Panelizálás | tab-route + mouse bite, 3 fiducial, lapok külön. **As-built (9. kör):** a lapon nincs fiduciál → egyedi lap **JLC sínekkel csak a felső és az alsó élen** (a sínek viszik a fiduciálokat); **a jobb élen y > 5,8 mm és a felső élen x 10–35 mm között nincs fül / V-cut** (C3 / R10 / C1 0,7–0,8 mm-re a jobb éltől); mouse-bite a kontúron kívül, ≥1 mm-re a via-gyűrűktől | P-34, dfm2-02 |
| Selyem | pin 1, FPC kontakt oldal, "no hot-plug" felirat (SD/FPC/B2B), mérőpont nevek. **As-built (2026-10-11):** silk DRC 0; B: „ESP32-P4-CAM MAIN”, „rev A 2026-10”, „USB-C PD 9V”, „no hot-plug of FRONT”, TP-hálónevek, BOOT / RESET / USER; F: J2 / J5 pin-1 „1”, „R16→”, JLC rendelésszám-helyőrző (x 22,3–32,5, y 13,8–15,0 – rendeléskor „specify location” vagy törlés) | P-37, E-30 |
| JLC DFM | header (7 mm), FPC konnektor, u.FL, USB-C THT elérhetőség ellenőrzendő. **2026-10-11: mind JLC-n beültethető (`07` §0); a J2 készlete 31 db (foglalni); 7,00 mm-es B2B pár nincs (Q17); a J1 köpenylábai kézi / szelektív forrasztást kérnek (§3.1)** | P-35 |
| Első prototípus | 1:1 papír/3D-print mechanikai vázlat a sematik **előtt** (footprint tükrözés, pin 1) | P-3, P-22 |

### 3.1 EDA, gyártási folyamat és modul-forrasztás (K-10, K-18)
| Téma | Döntés / követelmény |
|---|---|
| EDA eszköz | **KiCad** (tulajdonosi döntés, 2026-10-09). Teendő: JLC ~~2 rétegű 1,0 mm~~ **4 rétegű (v0.6: `scripts/project_rules.py` + `.kicad_dru`)** DRC szabályok, Waveshare footprint + 3D STEP importálása saját könyvtárba, LCSC mezők a szimbólumokban (BOM → 07), field solver: KiCad PCB Calculator. Követelmény: JLC/LCSC alkatrész-import, saját footprint (Waveshare modul), 3D STEP export a mechanikai ellenőrzéshez (06) |
| KiCad projekt (2026-10-09) | `kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pro`; közös könyvtár `kicad/lib/ESP32-P4-CAM.{pretty,kicad_sym}` (`${KIPRJMOD}/../lib`). Lapok: 01_tap, 02_p4_modul (U1), 03_kamera, 04_prog_tp, 05_b2b_front, 06_sd. NYÁK **(v0.6 as-built): 45×45 mm, R1 sarok, 4 réteg, 0,97 mm** (JLC04101H-3313A); netclass a 3313A szerint: CSI 0,204/0,203, USB 0,262/0,203, RF 0,302, PWR 0,4, PWR_LIGHT 0,3, Default 0,15; JLC 4L minimumok (nyom 0,09, furat 0,2, via 0,45) – §3.2. ~~60×50 mm, 1,0 mm, 2 réteg, CSI_DIFF 0,30/0,20, RF_50 0,70, PWR 0,60~~ (archív). ~~A netclass-szélesség a DRU-ban nincs kikényszerítve (7. kör)~~ → **8. kör: `.kicad_dru`: PWR ≥0,4 / PWR_LIGHT ≥0,3 mm figyelmeztető szabály (37 találat, elfogadva), CSI páron belüli skew ≤0,1 mm, PWR zónák ≥1 mm-re a lapszéltől**; CSI-hossz, RF- és USB-geometria szabály nincs (rev B) |
| MAIN koordináták | **→ §3.1a (as-built, befagyasztva).** ~~45×45 „mag” = x 0–45, y 2,5–47,5 (közép 22,5; 25); többlet-sáv x 45–60; „a FRONT ugyanezt a magot használja”~~ – a 45×45-ös lap kontúrja x 0–45, **y 0–45**; az M2 furatok a régi 60×50-es koordinátán maradtak (a `place45.py` kihagyta őket), ezért a raszter 2,5 mm-rel aszimmetrikus. **A FRONT a MAIN kontúrját és furatkoordinátáit 1:1 másolja**, nem egy szimmetrikus „magot” |
| Táp IC-k lezárva (E22, 2026-10-09, adatlapból) | **PD: CH224A** (LCSC C42459160, ESSOP10; a CH224K az LCSC-n *Discontinued*; a CH224D-nek nincs I2C-je). Rset CFG1→GND **6,8 kΩ = 9 V**; VBUS láb ↔ VHV; VHV 1 µF; **I2C 0x22/0x23** (CFG2=SCL, CFG3=SDA, belső 10k felhúzás, VIH 1,5–3,3 V) → reg 0x09 protokoll-státusz, 0x50 áram (×50 mA) → **B-4 megoldva**; PG open-drain, aktív alacsony; DP/DM NC; abs max DP/DM/CFG1 3,8 V. **eFuse: TPS259470ARPW** (adj. OVLO, aktív ILIM, auto-retry, FLT; 2,7–23 V, abs 28 V; reverse blocking): UVLO/OVLO küszöb 1,20 V↑ / 1,09 V↓ → R6/R7 = 267k/100k → **4,40 / 4,00 V**; R8/R9 = 80,6k/10k → **OVLO 10,87 / 9,88 V**; R10 RILM 1,65k → **2,03 A** (min 1,80); CdVdt = 2000/SR[V/ms] → 1 nF = 2 V/ms. **Buck: TPS62933F** (FCCM, 3,8–30 V, 3 A, SOT583): RT→GND 1,2 MHz, Vref 0,8 V → R14/R15 = 31,6k/10k = **3,33 V**, CSS 10 nF (min 6,8 nF), BST 100 nF, L 2,2 µH, COUT TI-ajánlás 30 µF eff. (min 10). Forrás: `ref/datasheets/` |
| Modul footprint (E21) | `Waveshare_ESP32-P4-Module`: **Waveshare land pattern DXF-ből** (`ref/waveshare-land-pattern/`): 88 pad **1,5×0,7 mm**, maszk 1,6×0,8 (+0,05), paste = pad, 1,0 mm osztás, padközép-keret 25,0 mm, külső 26,5 mm. Számozás a Waveshare pinout képről igazolva (felülnézet, CCW: P1 bal-felső → P22 bal-alsó → P23–P44 alul → P45–P66 jobb oldal felfelé → P67–P88 felül). **Kézi forrasztási variáns (K-10) kész:** `Waveshare_ESP32-P4-Module_HandSolder` – réz+maszk pad a modul élén túl +1,5 mm (2,25×0,7 mm), paszta az eredeti 1,5×0,7; courtyard ±14,25. **Elhelyezve (v0.6 as-built): U1, B.Cu, (20,5; 25,0), 0°** (a 60×50-es (22,5; 25)-ről 2 mm-rel balra) → USB P50/P51 a jobb él (J1) felé, CSI P41–P46 a jobb-felső sarok (J2) felé, RF P2 (7,625; 34,5) bal-alsó (J4) felé. 7. kör: a lib mind a 88 padja a DXF-fel 0,0002 mm-en belül egyezik, pin 1 helyes |
| JLC folyamat | **v0.6: 4 rétegű, JLC04101H-3313A, 0,97 mm** (§3.2); a JLC 4L minimumok teljesülnek (7. kör: nyom ≥0,10, rés ≥0,15, gyűrű ≥0,125 mm). ~~A lapfájlban nincs stackup-blokk, a gbrjob a KiCad alapértelmezését viszi~~ → **8. kör: a lapfájlban stackup-blokk (3313 0,107 + 1080 0,0764 / mag 0,5, Cu 35 / 15,2 / 15,2 / 35 µm), ENIG, dielectric_constraints, Rev A; a gbrjob: ENIG, ImpedanceControlled, Rev A, 0,9872 mm**; a rendelési űrlapon ennek ellenére név szerint: JLC04101H-3313A, impedancia-kontroll, ENIG, 45 × 45 mm (nem a gbrjob 45,1-e). Furattávolság: különböző háló min. 0,408 mm, azonos 0,253 mm (szabály 0,25 ✓; a JLC DFM jelezhet). **Rendelés előtti kapu (9. kör, kötelező; a mentett zóna-kitöltések elavultak → töltés nélkül plottolva GND-zárlatok):** (1) a rendelendő `kicad/MAIN` lapon, mellette a `.kicad_pro` + `.kicad_dru`: `kicad-cli pcb drc --refill-zones --save-board --schematic-parity --severity-all` (vagy GUI: Fill All Zones + Save); (2) DRC refill nélkül: **0 hiba / 12 bekötetlen (DNP) / paritás 0**; (3) `copper_diff.py` a review-pillanatképpel: 0 réz-eltérés, 0 elavult kitöltés; (4) `kicad-cli pcb export gerbers --check-zones …` + `export drill --excellon-separate-th`, az In2 Gerber-nézőben; (5) a rendelési csomag (`kicad/MAIN/fab/`) frissítése. **Projektmappán kívül refillelni / menteni tilos** (a DRU 1 mm-es él-szabálya elvész). ~~2 rétegű, 1,0 mm~~ (archív) |
| Impedancia | v0.6: a 3313A stackup a JLC kalkulátor szerinti szélességekkel (§3.2); impedancia-kontroll rendelési opció. ~~A JLC 2 rétegű gyártáson nincs impedancia-kontroll, ±10–20 %~~ (a 2 rétegű tervre vonatkozott); rev A-ban RSSI + képstabilitás validál |
| Kétoldalas SMT | a JLC mindkét oldalt beülteti (költség ↑; **Standard PCBA**); a P4 modul kézi. **As-built: 72 beültetett tétel, F 47 / B 25 (CPL 72 sor)**; U1, MH1–4, TP-k, JP1 és minden DNP kizárva. ~~USB-C THT shell láb beültetése (JLC vs kézi) nyitott kérdés~~ → **a J1 4 köpenylába (furatos rés, (37,67 / 41,85; 18,18 / 26,82)) paszta nélküli, a J1 `attr smd` → a reflow után valószínűleg forrasztatlan; a tápbemenetet csak a 16 SMD pad (~10,2 mm²) tartaná** → rendeléskor: JLC kézi / szelektív forrasztás, **vagy** a tulajdonos forrasztja F felől az első kábel-bedugás előtt (finom hegy, kevés ón; utána a C1.2 GND-pad 0,757 mm-es rése ellenőrizendő) – §15 |
| **Modul forrasztás (K-10)** | castellated modul, **forrasztópáka + fluxus** (+ előmelegítő / hot-air); a MAIN-en a modul pad-jai **kifelé ≥1,5 mm-rel meghosszabbítva** (a fillet hozzáférhető); **maszk / keep-out a modul alatt**: nincs nyitott Cu / via a modul alatt (kivéve szándékos GND pad), forrasztómaszk-gát a padok között; a modul lábnyom ezért **28×28 mm** (06); a **modul ↔ USB-C távolság nő** (≥2 mm a pad-hosszabbítástól; modul 1 mm eltolás). **As-built eltérés (végső):** 105 via (33 GND, 72 jel) és 290 B-szegmens fut a modul teste alatt (mind tentelve, a DXF szerint nincs középső pad – alacsony kockázat, dfm-14); modul ↔ J1 1,53 mm. **Kézi forrasztási kockázat (8. kör óta):** a C21–C23 (B) padjai 0,5 mm-re a P83–P86 padcsúcsoktól, a **C23.1 (+3V3) 0,525 mm-re a P87 (ESP_EN) csúcsától** – híd esetén nincs EN-késleltetés, és a SW2 (RESET) 3V3–GND zárlat lesz; az RF P2 csúcsa 1,82 mm-re az R34.1-től → **finom kúpos hegy a P83–P88-on, utána P87/C23 és R34/J4 szemle + TP16A ↔ TP4 mérés (§15)** |
| Próbaforrasztás | a 3–4 modulból legalább egy forrasztási próbára (§0.3) |

### 3.1a MAIN as-built mechanikai interfész (v0.6, NYÁK-ról mérve, 2026-10-10) – **BEFAGYASZTVA a FRONT és a ház felé**
Koordináták: KiCad-keret, mm – origó a lap bal-felső sarka, X jobbra, Y **lefelé**, nézet az F (kamera / FRONT felőli) oldalról; a B-oldali alkatrészek is ebben a keretben (átlátszó nézet). A 06 termék-keretébe (elölnézet, Y fel): x változatlan, y₀₆ = 45 − y.

| Elem | Oldal | Pozíció / forgatás | Megjegyzés |
|---|---|---|---|
| Lapkontúr | – | (0; 0)–(45; 45), R1 sarkok; 4 réteg, 0,97 mm | lapközép (22,5; 22,5) |
| MH1–MH4 (M2 távtartó) | NPTH | (5,75; 8,25), (39,25; 8,25), (5,75; 41,75), (39,25; 41,75); Ø2,2; ~~maszknyílás Ø3,2~~ → gyári `MountingHole_2.2mm_M2`, maszknyílás = furat (Ø2,2) | raszter 33,5 × 33,5, **középpont (22,5; 25,0) – 2,5 mm-rel a lapközép alatt** (a felső élig 8,25, az alsó élig 3,25 mm; a furat széle 2,15 mm-re az alsó éltől). Keep-out szabályterület r 1,75 (sáv/via tilos, alkatrész nem); ~~a furat-lábképnek nincs udvara (dfm-09)~~ → udvar r 2,45 (csak F; DRC 0 udvar-átfedés); F-en a legközelebbi beültetett alkatrész ≥2,87 mm (4 mm-es hatlapú távtartó r 2,31 elfér). **Alátét: nylon az MH1 / MH2 / MH4-en, az MH3-on nincs (csavarfej max. Ø4,0)** – §3 |
| J5 B2B 2×10, 1,27 mm | F | (22,5; 40,2), 90° – vízszintes, az **alsó él** mentén; pin 1 (16,785; 42,15), pin 2 (16,785; 38,25), pin 19 (28,215; 42,15), pin 20 (28,215; 38,25) | páratlan sor az él felé (y 42,15), páros sor y 38,25; udvar x 15,6–29,4, y 35,9–44,5. A FRONT párja ugyanezen X/Y-on a FRONT B oldalán – tükrözés / pin 1 papírpróbán (P-22). ~~Lábkép generikus, típus nincs (Q17)~~ → **BOM: Hong Cheng HC-PZ127-7.2L-2x10PS (C41375929)**, FRONT-aljzat: HC-PM127-4.3H-2x10PS (C27985222) – 5,3 mm-es illesztett magasság → 7,0 mm-es résnél ~2,3 mm merülés [NEM ELLENŐRZÖTT]; a land generikus (`PinHeader_2x10_P1.27mm_Vertical_SMD`); **Q17 nyitott** (Samtec 7,47 mm esetén MAIN lábkép-csere + 7,5 mm távtartó a rendelés előtt) |
| J2 kamera FPC 15 pin, 1,0 mm | F | (22,5; 7,5), 180° – **felső él**; kontaktsor y 9,3: pin 1 (29,5; 9,3) → pin 15 (15,5; 9,3); rögzítő padok (12,51 / 32,49; 6,5) | aktuátor és kábelbevezetés a felső él felől (udvar y 0,46–10,85, x 10,5–34,5) → az FFC a felső élen, az MH1–MH2 közötti ~28,9 mm-es ablakon lép ki; zárt stack-nél ~180°-os visszahajtás, ~4–5 mm-rel a kontúron kívül (becslés, G3). ~~Lábkép helyőrző~~ → **alkatrész = lábkép: TE 1-84953-5 (C5164008, TOP contact, csúszózáras; JLC-készlet 31 db – foglalni)**; kontakt-oldal **Q6** a kamera első bekapcsolása előtt (rossz oldal = 3V3/GND csere a kameránál) |
| J1 USB-C 16 pin (HRO TYPE-C-31-M-12) | B | (40,8; 22,5), −90° – **jobb él**, nyílás +X felé | jelpadok x 36,755; THT köpenylábak (37,67 / 41,85; 18,18 / 26,82) – az F oldalon is foglalnak; homloklap x ≈ 44,45 (0,55 mm-rel az él mögött); udvar x 35,5–45,0, y 17,1–27,9 |
| J4 u.FL | B | (3,0; 38,3), −90° – **bal él**; középső tüske (3,0; 36,775) | az MH3 csavarfej közvetlen szomszédja (alátét nem fér, mech-10: a J4 GND padja 2,54 mm, udvara 1,87 mm az MH3 középpontjától) → **MH3: nincs alátét, csavarfej max. Ø4,0 mm, az u.FL kábel Ny / É felé lép ki**; RF: U1 P2 (7,625; 34,5) → R34 (3,9; 34,5) → J4 |
| J7 C6/UART0 padsor 1×9, 1,27 mm (DNP) | B | (22,5; 2,0), 0° – **felső él**, vízszintes; pin 1 (17,42; 2,0) → pin 9 (27,58; 2,0) | pad 0,85×1,6; kiosztás: §6 J7 tábla |
| SW1 BOOT / SW2 RESET / SW3 USER (Omron B3U-1000P) | B | (11,5; 3,0) / (33,5; 3,0) / (33,5; 7,4) | felső él; a ház tűlyukai ehhez (§18) |
| D20 státusz LED (0603, zöld) + R30 1k | B | D20 (3,2; 14,35), R30 (3,2; 16,05) | bal él; fényvezető a házban (§18) |
| U1 P4 modul | B | (20,5; 25,0), 0° | udvar x 6,2–34,8, y 10,7–39,3 |
| J3 microSD (DNP) | F | (9,0; 25,0), −90° – bal él | rev A DNP; a behelyezett kártya ~4,8 mm-rel kinyúlik (mech-14) |
| Teszt pontok | B | §12 | a pogo-jig a §12 koordinátáiból |

**Változás a korábbi tervhez képest:** 60×50 / 2 réteg → **45×45 / 4 réteg**; a szimmetrikus „45×45 mag (y 2,5–47,5)” megszűnt, a furatok a régi koordinátán maradtak → raszter-középpont (22,5; 25,0); U1 (22,5; 25) → (20,5; 25,0); J5 függőleges (x 40,5) helyett **az F alsó élén vízszintesen** (a FRONT ehhez igazodik); J1 a többlet-sáv helyett a 45×45 jobb élén; J7 a bal-felső függőleges header helyett **felső élen vízszintes SMD padsor**; pogo-csoport 20 → 12 pad; SW1–3 → B3U-1000P (3,0×2,5 mm). **Ez az interfész a FRONT (G6) és a ház bemenete; csak a FRONT-tal együtt módosítható.** Ellenőrzés: 1:1 nyomtatott stack-makett (G3).

**Végső as-built (2026-10-11, review-pillanatkép):** a 8. kör a fenti interfész-elemek egyikét sem mozdította (kontúr, MH, J1, J2, J4, J5, J7, SW1–3, D20/R30, U1, J3 – újramérve, egyezik). Mozdult (nem interfész): **C4 → B (42,9; 16,2)**, **C14 új, F (42,675; 16,0)**, C3 (43,5; 9,45), R10 (43,8; 12,75), C1 (43,8; 26,75) −90°, U4 (29,4; 25,74), L1 (31,4; 30,02) −90°, a buck kondik / R14–R16, **C20–C23 a P84–P86 alá** (B, y 40,75–42,4), R27 (7,3; 37,93), C50 (2,75; 11,0) és DNP-k (R4, R36, C29, C30, C71, R73) – teljes lista: `06` „As-built elhelyezés”. 128 lábkép (124 alkatrész + MH1–4), 38 DNP; beültetett 72 (F 47 / B 25).


## 3.2 MAIN 4 rétegű felépítés (v0.6, 2026-10-09 – tulajdonosi döntés, böngészővel ellenőrizve)
Forrás: jlcpcb.com/impedance és jlcpcb.com/pcb-impedance-calculator (4 réteg, 1,0 mm, külső 1 oz, belső 0,5 oz; a kalkulátor első, „legolcsóbb, leggyorsabb” ajánlata).

| Réteg | Anyag | Vastagság | Szerep |
|---|---|---|---|
| L1 (F.Cu) | Cu 1 oz | 0,035 | jelek + alkatrészek (előlap) |
| prepreg | 3313 (0,107) + 1080 (0,0764) | 0,183 | |
| L2 (In1.Cu) | Cu 0,5 oz | 0,0152 | **folytonos GND sík** (vágás nélkül) |
| core | | 0,5 | |
| L3 (In2.Cu) | Cu 0,5 oz | 0,0152 | táp (VBUS / VBUS_SW / 3V3 szigetek) + lassú jelek, maradék GND-öntés |
| prepreg | 1080 + 3313 | 0,183 | |
| L4 (B.Cu) | Cu 1 oz | 0,035 | modul (hátoldal) + jelek |

Kész vastagság 0,97 ± 0,10 mm (JLC04101H-3313A).

| Impedancia (L1, ref. L2) | Szélesség | Rés |
|---|---|---|
| 50 Ω egyvezetékes (RF, ha F.Cu-n) | 0,302 mm | – |
| 100 Ω diff. (MIPI-CSI) | 0,204 mm | 0,203 mm |
| 90 Ω diff. (USB FS) | 0,262 mm | 0,203 mm |

L4 (B.Cu) jeleinek referenciája az L3: a CSI / RF / USB alatt az L3-on **GND-öntés** kötelező (táp-sziget nem lehet alatta), különben az impedancia nem érvényes. Rétegváltásnál GND-via a jelvia mellett. **MAIN méret: 45×45 mm** (a FRONT-tal közös interfész – M2 raszter, J5, J2 – as-built: **§3.1a**; a raszter nem a lapközépre szimmetrikus). Ár: **[NEM ELLENŐRZÖTT]** (kis 4 rétegű lap felára várhatóan néhány USD).

## 4. Tápfa + áramkeret

### 4.1 Tápfa
```
USB-C VBUS (max 9 V) ─ TVS (SMAJ10A; as-built D1: B oldal, az eFuse bemeneténél, 6,8 mm-re a J1-től) + USB ESD (as-built U5: F, a J1 mellett) ; 3 via az U3 IN-re ─ ≤10 µF EFFEKTÍV (CH224 kondik + TVS Cj is beleszámít) ─ eFuse (állítható OVP ~10,5–11 V,
        │                reverse-blocking, auto-retry, UVLO ~4,4 V felfelé / ~3,9 V lefelé, ILIM ~2 A, soft-start) ─ VBUS_SW ─┬─ C14 1 µF/25 V az U3 OUT-on + bulk ≤47 µF eff. (terv: 35–50 V MLCC; as-built 25 V: C5/C6 22 µF, C8 10 µF)
        │                (az eFuse körül: 0 Ω / forrasztóhíd VBUS→VBUS_SW, DNP – bypass, K-1)                                   ├─ BUCK 3V3 (forced-PWM, ≥2 A, 2,2 µH Isat ≥3,5 A) ─ 0 Ω ─ 3V3 sín (TP4 = bench betáp, ha a 0 Ω nyitva)
        │                                                                                                              │     ├─ P4 modul ESP_3V3 + VBAT (47 µF + 10 µF + 100 nF a P84–P86 padoknál)
        │                                                                                                              │     ├─ CAM_3V3 ← load switch (TPS22918 osztály, kötelező) → kamera modul
        │                                                                                                              │     ├─ SD_3V3 ← load switch (kisütéssel) (rev A: DNP)
        │                                                                                                              │     ├─ ICR H-híd (FRONT, 3V3-ról, sosem VBUS_SW-ről; rev A: DNP) + mikrofon (LC, FRONT)
        │                                                                                                              │     ├─ VEML7700 (FRONT, a J5 3V3 pinen át; rev A: DNP) + NTC osztó (MAIN, ADC2, GPIO 49)
        │                                                                                                              │     ├─ státusz LED (MAIN hátoldal, GPIO 6 hajtja, soros R; nem a J5-ön)
        │                                                                                                              │     └─ supervisor (TPS3840 osztály, nyílt-drain) → 0 Ω → ESP_EN (rev A: DNP)
        │                                                                                                              ├─ VBUS_SW ADC osztó (200k/54,9k + 100 nF; 3,6 V Zener D2: DNP) → GPIO 20
        │                                                                                                              └─ IR ág: 2. eFuse (≥18 V, állítható ILIM 0,5–0,7 A) + shunt (TP8) – rev A: DNP, footprint marad → IR_VIN → B2B → FRONT IR driverek
        ├─ nyers VBUS (TVS után, az eFuse ELŐTT) ─ CH224A VDD (+ CH224 kondik, a ≤10 µF effektív keretben)
        └─ CC1/CC2 ─ CH224A (belső Rd; külső Rd NINCS – a 2× 5,1k footprint DNP, csak CH224A nélkül, soha egyszerre) ; PG → GPIO 31 ; CC-tap ≥100k soros → GPIO 21/22 (rev A: DNP)
```
**VBUS átvezetés hátoldal → front oldal:** a J1 / TVS (hátoldal) és az eFuse (front oldal) között a VBUS **≥2 db via-n** megy (ajánlott 3–4; ILIM ~2 A → ≤1 A/via, Ø0,3 mm via ≈ 1 A [NEM ELLENŐRZÖTT]); a GND visszatérés ugyanennyi via-n, a TVS + ESD földje a J1 GND-jén (13.1). A CH224A VDD a nyers VBUS-ról (TVS után) kap tápot; a VDD tartomány / 9 V-bírás az adatlapból [NEM ELLENŐRZÖTT – Q13].
**As-built (végső, 9. kör mérése):** J1 A4/B9 → 2 via + közvetlen 0,8 mm-es B-kötés a D1.1-hez; A9/B4 → 2 via; az **U3.5 IN-en 3 via (0,6/0,3)**, az U3.6 OUT-on 2 via; DC J1 → U3.5 **7,1 mΩ**, U3.6 → U4.3 **22,95 mΩ**. A VBUS In2 zóna egy sziget (138,6 mm²), de az É–D nyak 1,05 mm, majd egy GND via mellett ~0,55 mm (párhuzamos B-út – villamosan elhanyagolható). A VBUS_SW In2 zóna egy sziget (147,5 mm²), de 12 idegen In2 háló szeli → síkként csak részben működik (az áram a 0,5 mm-es In2 sávon és F/B linkeken folyik). J1 GND: pin-páronként 2 via. **A D1 TVS nem a J1-nél, hanem az eFuse bemeneténél áll (6,8 mm; TI TPS25947 8.4.1: a védelem a védett eszköz mellé) – elfogadott rev A eltérés.** Az U5.3 (USB ESD GND) padnál nincs saját via (legközelebbi GND via 1,96 mm; rev B: ≤0,5 mm). **C14 1 µF / 25 V** az U3 OUT-on (1,14 mm-re az U3.6-tól, GND-je az U3.8-cal azonos F-szigeten); 100 nF az U3 IN-en nincs (a C3 4,7 µF 2,9 mm-re, másik F-GND szigeten) – rev B.

**Nincs 2. tápbemenet** (bench táp / 5 V pin / PoE nincs: visszatáplálás és ütközés elkerülése; E-35). Az egyetlen tápút az USB-C.

| Szabály | Érték / döntés | Ref |
|---|---|---|
| VBUS max | **9 V** (PD 9 V kérés, 5 V fallback). "5–12 V" **törölve** minden szekcióból; 12 V-os profil nincs | B-11, A-20 |
| CH224A feszültség-strap | **fix ellenállással GND-re/megfelelő konfig-pinre, soha nem lebegő** (lebegő strap → 20 V kérés lehet); **hibás / lebegő strap esetén 20 V-os PDO is érkezhet – ezt az eFuse OVP nem fogja meg: a TVS (SMAJ10A) az eFuse *előtt* áll, a lánc első eleme, és az megy tönkre először** → a strap helyességét a G1 bench teszt igazolja (MacBook, olcsó PD töltő, USB-A→C kábel; 9 V PDO, PG polaritás / szint, DP/DM NC az USB-JTAG mellett). Strap-táblázat a CH224A adatlapból **[NEM ELLENŐRZÖTT – Q: CH224A adatlap]** | B-13 |
| CH224A kiolvasás | **I2C (0x22/0x23)**: reg 0x09 = protokoll-státusz (PD/QC/BC/EPR aktív bitek), reg 0x50 = aktuális PD profil max. árama ×50 mA ~~→ a FULL/MID/LOW mód közvetlenül olvasható; PG → GPIO 31 megmarad tartaléknak~~ (E22; B-4 ✅). **Rev A FW-szabály (9. kör, electrical2-02): a PD-módot a PG (GPIO 31) + VBUS_SW ADC (GPIO 20) adja; a CH224A-t csak a CAM_3V3 bekapcsolása után olvassuk (vagy egyáltalán nem), soha nem írjuk; I2C 100 kHz.** Ok: a közös buszon csak a CH224A belső felhúzói vannak (R31/R32 DNP), a kikapcsolt kamera (CAM_3V3 ≈ 0 V a QOD miatt) a clamp-diódáival lehúzhatja a buszt; a TP4 bench-módban (nincs VBUS) a CH224A tápfeszültség nélküli → nincs felhúzás. G1: a CFG2/CFG3 üresjárati feszültsége ≤3,3 V legyen |
| **Külső Rd TILOS** | A CH224A a WCH referencia-kapcsolás szerint külső Rd nélkül, közvetlenül a CC-re kötve működik (E22; belső Rd) → **nem teszünk külső 5,1k-t** a CC-re (dupla Rd = hibás Rp-szint, PD tárgyalás). **Kivétel (K-1, csak rev A debug):** 2× 5,1k Rd footprint, DNP – **kizárólag akkor ültethető, ha a CH224A nincs beültetve; soha egyszerre** (selyem: "NEVER BOTH") | B-5, K-1 |
| CC-tap (ADC) | **≥100k soros** → 10 nF az ADC lábnál → 3,6 V Zener clamp (nem BAT54S 3V3-ra: nincs pumpálás). A 10 nF és a 100k a PD BMC-t nem terheli (a régi 1k + 100 nF AC-terhelés **törölve**). A CC-tap **csak nem-PD 5 V áramérzékelésre** (Rp-szint); PD alatt a CC ugrál → nem használjuk módválasztásra. A soros tap DC-áramot nem húz a CC-ről (az ADC bemenet nagy impedanciás); a hibát az ADC- és Zener-szivárgás × 100k adja, ez ellenőrzendő [NEM ELLENŐRZÖTT]. **Rev A: a CC-tap alkatrészei DNP** (K-15) | B-3, B-6, K-15 |
| CH224 DP/DM | **NC** (E22: DP/DM a BC1.2-höz kell, NC-n hagyva csak a BC1.2 detektálás esik ki; így nem ütközik az USB-JTAG D±-szal); bring-up teszt (15. 1. lépés) **[ – Q: CH224A adatlap]** | B-7 |
| VBUS monitor | osztó **VBUS_SW-ről (eFuse után)**, ≥200k/54k (9,45 V → ~2,0 V), 3,6 V Zener + 100 nF; nem a TVS-es nyers VBUS-ról (visszatáplálás, 4,25 V clamp). **As-built: R12 200k / R13 54,9k / C7 100 nF; a Zener (D2) DNP (2026-10-10)** – a szivárgása a 43 kΩ-os csomóponton a 8 V-os módküszöböt torzítaná (§0.1) | B-23 |
| TVS | **SMAJ10A osztály**: standoff 10 V; szivárgás 9,45 V-on/85 °C-on ellenőrzendő; clamp vs eFuse abs-max egyeztetve [NEM ELLENŐRZÖTT – adatlap]. **20 V-os PDO (strap-hiba) esetén a TVS megy tönkre először** (G1). **As-built: D1 = Diodes SMAJ10A-13-F (C134939), B oldal, az U3 alatt (40,5; 13,5) – a J1-től 6,8 mm (elfogadott eltérés); pad 1 = katód = VBUS (JLC-előnézetben ellenőrizni)** | B-12, K-4 |
| eFuse | **állítható OVP ~10,5–11 V**, **reverse-blocking** (hard reset után a VBUS_SW visszafolyás nélkül essen 0-ra, vSafe0V ellenőrzés), **auto-retry**, **UVLO ~4,4 V (↑) / ~3,9 V (↓)**, **ILIM ~2 A**, soft-start; ~~TPS25947 / TPS2595x osztály [NEM ELLENŐRZÖTT: konkrét típus, Q13]~~ → **TPS259470ARPWR (C3662799)**: UVLO 4,40 / 4,00 V, OVLO 10,87 V, ILIM 2,03 A (§3.1) | B-9, B-11, B-20 |
| **Kapacitás-költségvetés** | **≤10 µF effektív az eFuse előtt** (CH224 kondik, TVS Cj, ESD Cj is számít). **VBUS_SW teljes effektív C ≤47 µF** (PD slew ~30 mV/µs × C → ILIM alatt marad: 47 µF ≈ 1,4 A [NEM ELLENŐRZÖTT]; a 100 µF = 3 A > ILIM **törölve**). Beleszámít: buck bemenet, IR kapcsoló/driver bemenetek, B2B lokális 10 µF + 100 nF. **35–50 V-os MLCC** a VBUS oldalon, effektív C-t DC-bias (9,45 V) mellett megadni (pl. 10 µF/50 V 1206 → ~3–5 µF [NEM ELLENŐRZÖTT]). **As-built: a VBUS_SW oldalon 25 V-os MLCC** (C5/C6 22 µF 1210, C8 10 µF 0805, C14 1 µF 0603; névlegesen ~55 µF, 9 V-on DC-bias után kevesebb [NEM ELLENŐRZÖTT] – a bring-up 1. lépés attach-áram mérése igazolja) – a 10,87 V-os OVLO mellett elfogadott eltérés a 35–50 V-os szabálytól; az eFuse előtt C3 4,7 µF / 50 V és C2 1 µF / 50 V | B-10, B-28, B-29, E-2 |
| Buck L/Cout | tartomány-ellenőrzés a választott buck adatlapján (számítás: `07` §2) | B-27 ⏳ |
| **Bring-up / debug tápút (rev A, K-1)** | (1) **VBUS→VBUS_SW 0 Ω / forrasztóhíd** az eFuse körül (DNP): eFuse-hiba esetén a lánc többi része tesztelhető; (2) **2× 5,1k Rd** (DNP, csak CH224A nélkül); (3) **TP4 = 3V3 bench betáp**: a buck kimeneti 0 Ω-ját kivéve a 3V3 sín laborból táplálható (**USB-vel egyszerre soha**). Selyem: "NEVER BOTH". A termékben (rev B) nincs | K-1 |

### 4.2 IR ág (D9)
| Elem | Követelmény |
|---|---|
| Betáp | **külön, második állítható-ILIM eFuse (≥18 V rating, TPS2595x osztály [NEM ELLENŐRZÖTT]) a MAIN-en, ILIM 0,5–0,7 A**: IR zárlat/túláram nem reseteli a rendszert (közös ILIM helyett). A TPS22810 osztálynak **nincs állítható ILIM-je [NEM ELLENŐRZÖTT]** → elvetve. **Rev A: az egész IR ág DNP** (2. eFuse / high-side kapcsoló, shunt, TP8, IR_SW_EN lehúzás; a footprint marad, az IR_VIN táp nélkül G6-ig). Alternatíva (rev B-ig mérlegelhető): biztosított 0 Ω (fused 0 Ω / PTC footprint). **Áram-shunt + TP8 a MAIN *front* oldalán, az IR eFuse mellett** (a FRONT-on a TP elérhetetlen; a hátoldali pogo csoporton kívül) |
| Driver bemeneti tartomány | a FRONT-on lévő IR driver **Vin = 4,5 … 9,45 V**-on működjön |
| Fejmagasság-kritérium | **Vin_min − Vsense ≥ Vf_max(−20 °C) + 0,3 V** (soros LED-ekre Σ Vf). Ha a 2-LED-es sorosra (≈4,0 V terhelés) nem teljesül 4,5 V-on → **egyes (1-LED) ágak** buck-CC-vel, vagy **alacsony-dropout CC** (≥95% duty / LDO-mód). A "2×2 LED soros" csak a kritérium teljesülése esetén marad [Vf_max NEM ELLENŐRZÖTT – LED adatlap] |
| Dimming | **soros NFET (AO3400 osztály)** PWM-mel, **Cout ≤1 µF** a LED-eknél (a 10–22 µF a LED anódnál **törölve**: 20 kHz-en kapcsolgatva árampuffer-hiba); a nagy kondik a **driver bemenetére** kerülnek (a 47 µF VBUS_SW költségvetésben) |
| PWM frekvencia | **LEDC ≥40 kHz** (PDM mikrofon alias elkerülése); IR_PWM és PDM CLK a B2B-n GND-vel elválasztva |
| Pull | IR_PWM, ICR_IN1/2 (és SD_EN, CAM_3V3_EN, IR_SW_EN): **100k lehúzás (CAM_3V3_EN: 10k, 2026-10-10) a MAIN-en – as-built az előlapon, a modul alatt / a cél-IC mellett** (boot alatt lebegés ellen; K-7: a MAIN a FRONT nélkül is működik, ezért nem a FRONT-on) |
| Szem-biztonság | **LED-áram plafon = PCB-szintű követelmény** (a shunt/ILIM/driver hardveresen korlátozza, nem csak FW); IEC 62471 ház-szinten (18.) |
| Alkatrészek | LED: 850 nm 3535 [NEM ELLENŐRZÖTT – konkrét típus Q13/BOM]; driver: buck-CC osztály [NEM ELLENŐRZÖTT]; NFET: AO3400 osztály |
| Bench teszt (K-19) | az IR teszthez **árnyékoló cső / ablak-távtartó** kell a padon (a LED fénye ne világítson a lencsébe / a szembe; a kép- és AE-oszcilláció elkerülésére); szem-biztonság: a LED-áram plafon hardveres |
| ICR | H-híd (DRV8837 osztály) **3V3-ról (vagy LDO-ról), sosem VBUS_SW-ről** (VM max ~11 V, de 9,45 V + tüske nem kell) [NEM ELLENŐRZÖTT]; **FW impulzus-limit 50–100 ms** + **soros áramkorlát** (ellenállás) a tekercs védelmére; tekercs adatok az ICR lencse adatlapjából (Q5) | **Rev A: DNP** (K-5; ICR rev B) |

### 4.3 Áramkeret és tápmódok (egy készlet; becslés **[NEM ELLENŐRZÖTT]**, méréssel pontosítani – E-33, F-18; **a G0 mérései cserélik le**)

Számítási alap: **VBUS 4,5 V** (legrosszabb: kábelesés + UVLO felett), **buck η = 0,82**, IR ág bemeneti teljesítménye 1,2 W (2 ág × 150 mA, ~3,4 V/ág, CC η≈0,85).

| Fogyasztó | Sín | Tipikus | Csúcs |
|---|---|---|---|
| P4 (stream + H.264) | 3V3 | 250 mA | 400 mA |
| C6 WiFi TX | 3V3 | 100 mA | 350 mA |
| Kamera modul (saját LDO-k) | 3V3 | 120 mA | 200 mA |
| microSD írás | 3V3 | 50 mA | 100 mA |
| egyéb (mic, LED) | 3V3 | 20 mA | 30 mA |
| **3V3 össz** | | **540 mA = 1,8 W** | **1080 mA = 3,6 W** |
| Buck bemenet (η=0,82) | VBUS_SW | 2,20 W | 4,39 W |

| Üzemállapot | Teljesítmény (VBUS_SW) | I @ 4,5 V | I @ 9 V | Megjegyzés |
|---|---|---|---|---|
| **Nappal, tipikus** (IR ki) | 2,20 W | 0,49 A | 0,24 A | |
| **Nappal, csúcs** (WiFi TX csúcs, SD írás, IR ki) | 4,39 W | **0,98 A** | 0,49 A | nappali csúcs oszlop |
| **Éjjel, tipikus** (IR be) | 3,40 W | 0,76 A | 0,38 A | |
| **Éjjel, csúcs** | 5,59 W | **1,24 A** | 0,62 A | |
| **MID** (5 V/1,5 A forrás): IR ≤50% (0,6 W), WiFi TX cap (~200 mA) | ~3,9 W | 0,87 A | – | forrásból 4,5 V × 1,5 A = 6,75 W; margó szűk |
| **LOW boot** (kamera off, SD off, IR off, TX ≤10 dBm) | 1,49 W (370 mA 3V3) | **0,33 A** | – | ≤0,5 A (USB 2.0 unit load) → PC porton bootol |
| **LOW csúcs** (kamera 720p be, WiFi cap TX ≤10 dBm ~180 mA, nincs SD/IR) | 2,82 W (700 mA 3V3) | **0,63 A** | – | > 0,5 A → **PC = best effort** (USB 3.x/BC1.2 hoston ok; USB 2.0 hoston brown-out lehet) |

Hőszámításhoz: bemeneti csúcs 5,6 W → hőterhelés zártan **~4,5–4,9 W** (11.).

**Firmware tápmódok (B-2, B-3, B-17, B-19, E-11, E-12, F-3)**
| Mód | Feltétel | Viselkedés | Minimum forrás |
|---|---|---|---|
| **FULL** | **VBUS_SW ≥ 8 V** (PD 9 V) **vagy** nem-PD Rp = 3 A (CC ADC 1,31–2,04 V) | minden funkció, IR teljes (a termikus limitig) | **PD 9 V / ≥1,0 A** (éjszakai csúcs 0,62 A @9 V + tartalék; ajánlott 9 V/2 A) **vagy** nem-PD **5 V / 3 A** (éjszakai csúcs 1,24 A @4,5 V) [NEM ELLENŐRZÖTT; G0] |
| **MID** | nem-PD Rp = 1,5 A (CC ADC 0,70–1,16 V) | **IR ≤50%**, WiFi TX cap, 1080p30 megtartva ha a hő engedi | **5 V / 1,5 A** (nem-PD); csúcs ~0,87 A @4,5 V; **rev A-ban nincs** (CC-tap DNP) |
| **LOW** | alapértelmezett: USB/PC (Rp default, CC 0,25–0,61 V), ismeretlen vagy PD-tárgyalás alatt | **kamera boot-kor kikapcsolva**, WiFi **TX ≤10 dBm**, **720p**, **SD ki, IR ki**; elég programozáshoz/debughoz; **PC = best effort** | **5 V / 0,5 A** (USB 2.0 unit load): LOW boot 0,33 A elég; a LOW csúcs 0,63 A → ≥0,9 A (USB 3.x / BC1.2) kell, különben best effort |

Szabályok:
1. **Boot mindig LOW-ban indul.** A módot **csak ≥1,5 s VBUS settle után** döntjük el (PD tárgyalás 0,3–1 s; a boot 5 V-on indul, 9 V később jön).
2. A döntés **folyamatosan újraértékelődik**; CC-n **medián (≥8 minta) + hiszterézis** (a PD alatti Rp-toggle nem okozhat módugrálást). PD aktív időszakban a CC-t nem használjuk, **FULL = VBUS_SW ≥ 8 V** (ADC) / PG.
3. Lefelé váltás (FULL→LOW): VBUS ≤ 7,5 V vagy PG elvész → azonnali IR ki, WiFi TX cap; felfelé csak a settle után.
4. Boot sorrend: P4 + C6 → VBUS/PG mérés (GPIO 20, 31; a CC ADC GPIO 21/22 **rev B / ha a CC-tap be van ültetve**) → ≥1,5 s settle → mód → CAM_3V3 → SD (tri-state szabály, 5.) → IR.
5. PD hard reset (VBUS ~0 V): a bulk nem tartja át; az eFuse **auto-retry**, a rendszer hidegindul LOW-ba (9. áramszünet-tűrés).
6. **Rev A mód-logika (K-15):** boot LOW → **FULL** csak ha ≥1,5 s settle után VBUS_SW ≥ 8 V (ADC + PG), különben LOW; a CC-tap alkatrészei DNP, ezért MID nincs, a nem-PD Rp-ágak nem használhatók.

## 5. GPIO kiosztás (P4 modul)

A "modul pad" oszlop a Waveshare pinout táblából származik (**E20, primer forrás**; minden pad kitöltve). Megkülönböztetés: **P49 = modul pad, GPIO 49 = processzor láb** (különböző dolgok).
**As-built ellenőrzés (2026-10-10):** minden sor összevetve a NYÁK U1 padjainak hálóival és a séma-szimbólum lábneveivel (U1 pad n ↔ „GPIOx” lábnév, E20 szerint) – a GPIO ↔ pad ↔ háló hozzárendelés **mind egyezik** (v0.6 csere: SD_EN P81, SD_CD P80, CAM_3V3_EN P19, USER_BTN P60, EFUSE_FLT P56, PDM_DATA P57). A javítások csak a szöveges oszlopokat érintették (GPIO 45 sor, GPIO 54 TP, ESP_EN RC, GPIO 4 lehúzás, GPIO 7/8 CH224A, lehúzások oldala, UART0 / C6 TP-k).

| GPIO | Modul pad | Funkció | Pull / védelem | Megjegyzés |
|---|---|---|---|---|
| GPIO 24 / 25 | P50 / P51 | **USB-Serial-JTAG** D− / D+ (az egyetlen USB-megnevezés; a P48/P49 HS PHY **nem használt, NC – ezen a layouton soha nem engedélyezzük, csak FS (§6)**; az OTG FS funkció nincs használatban – sdkconfig-ban ellenőrizni, Q23) | ESD **TPD2E2U06 / PRTR5V0U2X osztály** (3,3 V array, **nincs VBUS láb**; USBLC6-2SC6 törölve – VBUS lába ~5 V-os, 9 V-on tönkremegy); shield 1 MΩ ‖ 4,7 nF | E10, E20; egyetlen USB-C; CH224 DP/DM NC |
| GPIO 35 | P62 | BOOT gomb | gomb GND-re | strapping, E8 |
| GPIO 36 | P63 | BOOT_EN felhúzás | 10k → 3V3 | E8 |
| GPIO 34, 37, 38 | P61 / P64 / P65 | strapping / UART0 TX,RX | **nincs terhelés**; UART0 csak a **J7.7 / J7.8** padon (DNP padsor), soros **R40 / R41 1k** (a TP14/TP15 törölve) | E-6, E20; részletes tábla: 5.1 |
| ESP_EN | P87 | RESET gomb (SW2) **OR** supervisor kimenet; TP16A | **R23 10k → 3V3 + C25 1 µF → GND: FIT (2026-10-10)** – a modul RC-je (Q3 ⏳) ismeretlen, a dupla RC csak az időállandót módosítja; az ESP_EN útvonala ~95 mm (gomb + TP). Supervisor TPS3840 osztály, nyílt-drain, 0 Ω-on át, RESET gombbal vezetékes-VAGY: **nincs rajzolva → rev B** | E-22 ⏳, B-21, K-14 |
| GPIO 7 / 8 | P22 / P23 | I2C SDA / SCL – **közös busz: kamera SCCB (J2.14/13) + CH224A (CFG3/CFG2, 0x22/0x23) + FRONT (J5.19/20, VEML7700)** | felhúzás egy helyen (MAIN, R31/R32 4,7k); **a felhúzás csak a kamera I/O szintjének ismerete után ültethető be** (1,8 V modul?) – addig DNP (addig csak a CH224A belső 10k-ja húz); a modul saját felhúzása ellenőrzendő. **FW: a CH224A-t csak olvasni** (egy hibás írás 20/28 V-ot kérhet – a TVS nem bírja; electrical-05); **rev A: I2C 100 kHz, a CH224A olvasása csak a CAM_3V3 bekapcsolása után (§4.1, §15)** | E15, E22, A-7 |
| GPIO 23 | P32 | Kamera PWDN/EN (FPC CAM_IO0) | **Pull = TBD (Q5)** – a választott modul PWDN/EN polaritásától függ: aktív-magas PWDN esetén a 100k lehúzás = *bekapcsolt* → ilyenkor felhúzás / GPIO-vezérlés; alapállapot = kamera kikapcsolva a **CAM_3V3 load switch** miatt is | E-17, E-26, A-3 |
| GPIO 4 | P19 | **CAM_3V3_EN** (load switch, TPS22917) **(v0.6 GPIO-csere, NYÁK huzalozhatóság)** | lehúzás **10k (R28, 2026-10-10; korábban 100k)** – a GPIO 4 = pad-JTAG MTMS, reset alatti belső felhúzása [NEM ELLENŐRZÖTT]; ellenőrzés: CAM_3V3 (TP5) reset alatt 0 V | B-22, E20, electrical-06 |
| GPIO 12 / 30 | P27 / P57 | PDM mic CLK / DATA (DATA: GPIO 13 → 30 **(v0.6 GPIO-csere, NYÁK huzalozhatóság)**) → J5.13 (PDM_CLK_J5) / J5.16 | CLK soros R70 47 Ω a forrásnál (B); I2S0 PDM RX | E-16 |
| GPIO 33 | P60 | User gomb **(v0.6 GPIO-csere, NYÁK huzalozhatóság)** | **MAIN hátoldal**; belső felhúzás + 100 nF a pinen | A-38 |
| GPIO 6 | P21 | Státusz LED (diszkrét 0603 + soros R, **MAIN hátoldal**, a modul közelében; FIT) | soros R (LED-áram ≤~2 mA, érték: `07`) | E-34; a J5.17 tartalék (NC) |
| GPIO 20 | P29 | **VBUS_SW monitor ADC** (200k/54,9k + 100 nF; a 3,6 V Zener D2 **DNP**, 2026-10-10) | – | ADC1; LDR kiváltva |
| GPIO 21 / 22 | P30 / P31 | CC1 / CC2 ADC (csak nem-PD 5 V áramérzékelés) | ≥100k soros + 10 nF + 3,6 V Zener (rev A: mind DNP) | ADC1; B-6. **Rev A as-built: a CC1_ADC hálónak nincs reze** (a P30 → C29/R35/D21 csonk eltávolítva, §0.1) – beültetés előtt bekötendő |
| GPIO 26 | P53 | IR PWM (LEDC **≥40 kHz**) | **100k lehúzás** | E-8, B-30, E20 |
| GPIO 27 / 28 | P54 / P55 | ICR IN1 / IN2 | **100k lehúzás** (R25 / R26, MAIN **előlap** (as-built), FIT; az ICR blokk **DNP rev A**) | E-8, E-9, E20 |
| GPIO 53 | P81 | SD_EN **(v0.6 GPIO-csere, NYÁK huzalozhatóság)** (U8 TPS22917, TPS22918-osztály; rev A: SD DNP) | 100k lehúzás (R27, előlap, FIT) | E-3 – nem VO4 domain; E20 |
| GPIO 52 | P80 | SD_CD **(v0.6 GPIO-csere, NYÁK huzalozhatóság)** | felhúzás a fő 3V3-ra (**csak CD**, nem-VO4 GPIO; az adatvonalak felhúzása SD_3V3-ra) | E-3, A-27, E20 |
| GPIO 31 | P58 | **PD PG** (CH224A Power-Good) – kötelező; TP17 | pull-up R3 10k a 3V3-ra (open-drain, aktív alacsony – E22; G1 méréssel igazol) | B-4, E20 |
| GPIO 32 | P59 | **IR_SW_EN** (az IR eFuse / kapcsoló engedélyezése; rev A: DNP) | **100k lehúzás** (R29, MAIN előlap (as-built); rev A: DNP az IR ággal) | B-25, E20 |
| GPIO 0 | P88 | **szabad** (a VEML7700 INT csak akkor, ha a J5 kap hozzá pint – jelenleg nincs szabad J5 pin → NC) | – | E20 |
| GPIO 1 | P16 | **szabad** (32k XTAL opció: ha használjuk, GPIO 0 + GPIO 1 együtt, a VEML INT ekkor kiesik [NEM ELLENŐRZÖTT]) | – | E20 |
| GPIO 29 | P56 | **EFUSE_FLT** **(v0.6 GPIO-csere, NYÁK huzalozhatóság)** (TPS259470A ~FLT, open-drain, aktív alacsony; 10k felhúzás a táp lapon, R11 – as-built B oldal) | – | 2026-10-09, sematik bekötéskor pótolva |
| GPIO 2, 3, 5, 13 | P17 / P18 / P20 / P28 | **szabad** (tartalék; v0.6 csere után) | – | E20 |
| GPIO 49 | P77 | **NTC ADC2** (buck/IR közelében) | NTC + osztó, 100 nF | B-26, E20; ADC2: GPIO 49–53 |
| GPIO 39–44 | P67–P72 | microSD D0 D1 D2 D3 / CLK CMD (**rev A: DNP**) | felhúzás a **kapcsolt SD_3V3**-ra, ESD ≤3,5 pF | E17, E20; SDMMC slot0 IO_MUX |
| GPIO 45, 46 | P73, P74 | – (nem használt, VO4 domain) | NC | az IDF SD-példa default power-reset pinje GPIO 45 → az **sdkconfig-ban kötelezően felülírni / letiltani** (SD_EN = **GPIO 53**, v0.6; a korábbi „GPIO 29” elavult); bring-up ellenőrzés: 15/4. lépés |
| GPIO 47, 48 | P75 / P76 | VO4 domain, nem használt | NC | E-5, E20 |
| GPIO 14–19 | – | C6 SDIO (modulon belül) | – | E5 (következtetés), E18 |
| GPIO 54 / C6_EN (P82) | P82 | C6_EN (**foglalt**; E20-ban nincs külön C6_EN pad, a P82 = GPIO 54) | **J7.6** pad (DNP padsor; a TP13 törölve) | E18; **Q2**: a modulon belül is C6_EN-re van kötve? |
| C6_IO9 | P9 | C6 BOOT | **10k felhúzás 3V3-ra** (R21) (+ J7.4 pad: jumper/pogo lehúzás a downloadhoz) | E6, A-4 |
| C6_IO8 | P10 | C6 strapping | **10k felhúzás kötelező** (R22; minden dokumentumban); J7.5 | E6, A-31 |
| GPIO 9–11, 50–51 | P24–P26, P78–P79 | szabad | – | E20 |
| C6_IO13–15 | P8 / P7 / P6 | **NC** (nem használt) | – | E20 |
| C6 JTAG IO7..IO4 | P11–P14 | **NC** (rev A-ban nem kivezetett, F-25) | – | E20 |
| DSI | P34–P39 | **NC** (nem használt) | – | E20 |
| GND padok | P1, P3, P15, P33, P40, P47, P52, P83 | **GND-re kötni** (mind; a NYÁK-on ellenőrizve) | – | E20 |
| VO4 | P66 | ESP_LDO_VO4 | C24 1 µF + TP7, **külső forrás tilos** | E-5 |

**v0.6 GPIO-csere (2026-10-09, MAIN rev A huzalozás):** a Freerouting 27–34 bekötést nem tudott megoldani, mert több funkció a modul ellentétes oldalán lévő alkatrészhez futott. Csere: SD_EN 29→53, SD_CD 30→52, CAM_3V3_EN 33→4, USER_BTN 5→33, EFUSE_FLT 2→29, PDM_DATA 13→30. Az ADC funkciók (GPIO 20–22, 49) változatlanok (ADC-képes láb csak GPIO 20–23 / 49–53). A lehúzások (R27 SD_EN 100k, R28 CAM_3V3_EN – 2026-10-10 óta 10k) a cél-IC mellé, az előlapra kerültek. **Firmware: pin-definíciók frissítendők; a GPIO 33-on (USER) a 100k lehúzás megszűnt, belső felhúzás + C40.** A csere a huzalozhatóság miatt történt, a reset-/strap-állapotok ellenőrzése nélkül → a GPIO 4 (MTMS) reset-állapota a P4 adatlapból ellenőrzendő [NEM ELLENŐRZÖTT].

**Lehúzások helye (as-built, 2026-10-10):** mind a **MAIN előlapján (F)**: R24 IR_PWM (19,8; 13,6), R25 ICR_IN1 (24,05; 19,45), R26 ICR_IN2 (19,75; 16,8), R29 IR_SW_EN (35,45; 8,7; DNP), R27 SD_EN (7,0; 38,15), R28 CAM_3V3_EN (3,0; 16,3) – KiCad-koordináták (§3.1a). ~~x 31,5, a modul alatt~~ és ~~MAIN hátoldal~~ elavult (a CSI-folyosó ürítésekor mozdultak). Nem a FRONT-on (K-7: a MAIN önállóan működik).

### 5.1 Strapping tábla (GPIO 34–38) – **adatlap ref: TODO**
Csak a Waveshare wikiből (E8) és az EV-board dokumentációból ismert; a ROM/strap funkció pinenként a P4 adatlapból kitöltendő **[NEM ELLENŐRZÖTT]**.
| GPIO | Pad | Tervezett terhelés | Boot-állapot elvárás | Adatlap ref |
|---|---|---|---|---|
| GPIO 34 | P61 | **nincs** (NC, nincs külső alkatrész) | alapállapot | TODO |
| GPIO 35 | P62 | BOOT gomb GND-re; **nincs más terhelés** | high = normál, low = download (ha GPIO 36 magas) | E8; TODO |
| GPIO 36 | P63 | 10k felhúzás 3V3-ra | high | E8; TODO |
| GPIO 37 | P64 | UART0 TX → R40 1k → J7.7 pad; **nincs felhúzás/lehúzás** | a teszt-adapter ne tartsa lent | TODO |
| GPIO 38 | P65 | UART0 RX → R41 1k → J7.8 pad; **nincs felhúzás/lehúzás** | ugyanaz | TODO |
Ellenőrzés: bring-up 4. lépés (15.) és gyári teszt (16.): mérés a strapping lábakon boot közben (nincs külső terhelés a dokumentált értékeken túl).

**SD szabályok (E-3/E-4/E-5/B-24; rev A: a blokk DNP, a footprint marad – K-16):**
1. Firmware: VO4-et **3,3 V-ra** állítani (`sd_pwr_ctrl` on-chip LDO ID 4), **utána** SD_EN (GPIO 53, v0.6).
2. Felhúzások (CMD, D0–D3) a **kapcsolt SD_3V3**-ra, nem a fő 3V3-ra (boot alatt VO4 = 1,8 V → túlfeszültség).
3. Load switch kisütéssel (TPS22918 osztály [NEM ELLENŐRZÖTT]); SD_3V3 10 µF + 100 nF; ESD az SD vonalakon.
4. Kikapcsolt kapcsolónál nincs visszatáplálás: nincs felhúzás a fő sínre (a CD kivétel, A-27).
5. **FW: az SD vonalakat tri-state-be (GPIO input) kell tenni, mielőtt SD_EN lekapcsol** (különben a hajtott lábak táplálják a kártyát).

## 6. Csatlakozók

| Ref | Típus | Hol | Megjegyzés |
|---|---|---|---|
| J1 | USB-C 16 pin (USB 2.0; HRO TYPE-C-31-M-12, C165948) | MAIN hátoldal, **jobb él** (40,8; 22,5) | D+/D−, CC1/CC2 → CH224A; shield 1 MΩ ‖ 4,7 nF (R1/C1, F). **USB csak FS (12 Mbps, USB-Serial-JTAG P50/P51): a P48/P49 HS PHY-t ezen a layouton soha nem engedélyezzük** – a D+/D− B-szakaszai alatt az In2 nem GND (DP 5,05 / DM 5,90 mm VBUS_SW / void felett), a D+ clamp 2,6 mm-es T-csonkon, az U5 (F) GND-visszaútja hosszú (U5.3-nál nincs via) – FS-en SI-hatás nincs, rev A-ban elfogadva (rev B: GND via ≤0,5 mm az U5.3-hoz, D+ in-line). **A 4 köpenyláb forrasztása: §3.1 / §15**; pin map: `07` §3 |
| J2 | FPC 15 pin 1,0 mm – ~~jelölt: 1.0K-GT-15PB vagy Hirose FH12-15S-1SH; a NYÁK-on a lábkép helyőrző~~ → **TE 1-84953-5 (C5164008, TOP contact; a lábkép maga a megrendelt alkatrész; JLC-készlet 31 db)** | MAIN front oldal, **felső él** (22,5; 7,5), 180°, kábelbevezetés a felső él felől | **kontakt oldal (Q6) + kábel irány** a kamera modullal ellenőrizendő (a kamera első bekapcsolása előtt) – rossz oldal = 3V3/GND csere a kameránál; az 1-84952-5 (bottom contact) azonos lábképű; egyenes kábel; merevítő; vezérlő-jel ESD: **rev B** (A-10..12; §0.1) |
| J3 | microSD (a lábkép Hirose DM3AT – push-pull leírású, a „push-push” ellenőrizendő, mech-14) | MAIN front oldal, bal él | **DNP rev A** (footprint, K-16) |
| J4 | u.FL / IPEX | MAIN hátoldal, **bal él** (3,0; 38,3) (USB-C-vel ellentétes él) | LNA_OUT (P2) → π-háló (DNP elemek) → 50 Ω vonal → u.FL | rev A: minden elem 0 Ω / DNP-képes; ha a modul saját IPEX-e használható (G2), a J4 DNP lehet. **As-built: J4 + R34 0R FIT** (a G2 / K-6 / Q25 döntés nyitott) |
| J5 | B2B 2×10, 1,27 mm, **párosított magasság 7 mm** ~~[NEM ELLENŐRZÖTT: alkatrész/elérhetőség]~~ → **BOM: Hong Cheng HC-PZ127-7.2L-2x10PS (C41375929)** + FRONT: HC-PM127-4.3H-2x10PS (C27985222); 7,00 mm-es kész pár nincs (5,3 mm-es pár → ~2,3 mm merülés; Samtec FTSH/FLE 7,47 mm → 7,5 mm távtartó + lábkép-csere) – **Q17** | MAIN front ↔ FRONT | lent; `07` §0 |
| J6 | ICR 2 pin JST-SH 1,0 mm | FRONT | DNP rev A (ICR: rev B); pin-tábla lent |
| J7 | 1×9 **SMD padsor, 1,27 mm** (`PadRow_1x09_P1.27mm_SMD`, pad 0,85×1,6) **(as-built: felső él, vízszintes, (22,5; 2,0); pin 1 (17,42; 2,0) → pin 9 (27,58; 2,0); az RF P2-től távol)**; ~~bal-felső lapszél, függőleges, x = 2,0~~ (60×50-es állapot, elavult) (GND, C6_TXD, C6_RXD, C6_IO9, C6_IO8, GPIO 54 / C6_EN (P82; Q2), UART0 TX, UART0 RX, 3V3-ref) | MAIN hátoldal, a P2 (RF) padtól **távoli** élén | **DNP** (K-17); az egyetlen C6 / UART0 hozzáférés (a TP10–TP15 törölve); az RF nyomvonal nem fut mellette; pin-tábla lent |
| SW1/SW2/SW3 | BOOT / RESET / USER – **Omron B3U-1000P** | MAIN hátoldal, felső él: (11,5; 3,0) / (33,5; 3,0) / (33,5; 7,4) | lapszélen, tűvel/pogo-val elérhető; USER (GPIO 33, v0.6) hátoldal |
| TP | teszt pontok (12 pad) | MAIN hátoldal | lásd 12. |

### J5 – 2×10 B2B (javaslat; csak logika + táp, GND a PDM CLK és IR PWM körül, rail-enként ≥2 pin)
| Sor | Páratlan | Páros |
|---|---|---|
| 1–2 | **IR_VIN** (az IR eFuse / biztosított 0 Ω után) | **IR_VIN** |
| 3–4 | GND | GND |
| 5–6 | IR_PWM | GND |
| 7–8 | ICR_IN1 | ICR_IN2 |
| 9–10 | GND | 3V3 |
| 11–12 | 3V3 (ICR H-híd táp is) | GND |
| 13–14 | PDM_CLK | GND |
| 15–16 | GND | PDM_DAT |
| 17–18 | tartalék (NC; a státusz LED a MAIN hátoldalán van, GPIO 6) | GND |
| 19–20 | SDA | SCL |
A J5.17 **tartalék (NC)**; GPIO 6 nem megy a B2B-re. Mirror/pin 1 ellenőrzés papír-próbán (P-22). I2C felhúzás csak egy helyen (MAIN). Header-áram: IR_VIN 2 pin ≥ 0,6 A (becsült ~0,3 A 4,5 V-on) **[NEM ELLENŐRZÖTT: pin áramterhelhetőség]**; az IR áramlépcső miatt **FRONT-on lokális 10 µF + 100 nF** a header mellett (a 47 µF VBUS_SW költségvetésben, 4.1).

### J3 – microSD (push-push; DNP rev A) – pin-tábla [NEM ELLENŐRZÖTT: a konkrét MPN adatlapján a lábszámozás ellenőrizendő; az alábbi a szabványos microSD kártya-pin sorrend]
| Kártya pin | Jel | Bekötés |
|---|---|---|
| 1 | DAT2 | GPIO 41 (P69); felhúzás SD_3V3-ra |
| 2 | DAT3 / CD | GPIO 42 (P70); felhúzás SD_3V3-ra |
| 3 | CMD | GPIO 44 (P72); felhúzás SD_3V3-ra |
| 4 | VDD | **SD_3V3** (kapcsolt; 10 µF + 100 nF) |
| 5 | CLK | GPIO 43 (P71) |
| 6 | VSS | GND |
| 7 | DAT0 | GPIO 39 (P67); felhúzás SD_3V3-ra |
| 8 | DAT1 | GPIO 40 (P68); felhúzás SD_3V3-ra |
| CD kapcsoló | card detect | GPIO 52 (P80, v0.6), felhúzás a **fő** 3V3-ra (a CD kivétel, 5. SD-szabály 4.); a kapcsoló másik lába GND |
| Shield | | GND |
Az SD vonalakon ESD ≤3,5 pF; SD_EN = GPIO 53 (P81, v0.6) → SD_3V3 load switch (E17, 5. SD-szabályok).

### J4 – u.FL (rev A: DNP, ha a modul saját IPEX-e használható, G2)
| Pin | Jel | Bekötés |
|---|---|---|
| 1 (központi) | RF | LNA_OUT (P2) → π-háló (DNP-képes) → 50 Ω vonal → u.FL (as-built: 0,302 mm microstrip a B rétegen, In2 referencia, ~7 mm sáv, U1 P2 → J4.1 út 7,96 mm; R34 0R FIT, C27/C28 DNP) |
| 2 (külső, árnyék) | GND | GND (via kerítés ≤2 mm, 13.) – ~~as-built (7. kör): nincs kerítés, 2 mm-en belül 0 GND via; az In2 referenciát a +3V3 sáv metszi → javítandó (rf-01/rf-02)~~ → **javítva (8. kör, a 9. kör mérése): GND via az RF középvonaltól 1,0 / 1,5 / 2,0 / 3,0 mm-en belül 10 / 14 / 14 / 18, mindkét oldalon (legnagyobb osztás 1,31 mm); a J4 GND padjai mellett via 0,10 mm-re; In2 alatta 100 % GND (egy 325,6 mm²-es sziget, 44 via), KO_RF_In2 tiltó terület (sávot tilt, nem-GND viát nem – rev B: DRU-szabály)** |

### J6 – ICR 2 pin JST-SH 1,0 mm (FRONT; DNP rev A)
| Pin | Jel | Bekötés |
|---|---|---|
| 1 | ICR_A | DRV8837 OUT1 (IN1 = GPIO 27 → J5.7) |
| 2 | ICR_B | DRV8837 OUT2 (IN2 = GPIO 28 → J5.8) |
A tekercs polaritása / nappal–éjszaka irány az ICR lencse adatlapjából (Q5) [NEM ELLENŐRZÖTT]; FW impulzus-limit 50–100 ms, soros áramkorlát (4.2).

### J7 – C6 / UART0 header 1×9 (MAIN hátoldal; DNP rev A, K-17)
| Pin | Jel | Modul pad / megjegyzés |
|---|---|---|
| 1 | GND | |
| 2 | C6_TXD (C6_U0TXD) | P5 (a TP10 törölve) |
| 3 | C6_RXD (C6_U0RXD) | P4 (a TP11 törölve) |
| 4 | C6_IO9 | P9 (BOOT; 10k felhúzás R21; a TP12 törölve) |
| 5 | C6_IO8 | P10 (10k felhúzás R22, kötelező) |
| 6 | GPIO 54 / C6_EN (P82) | P82 (a TP13 törölve); Q2 nyitott (a C6_EN-re kötés a modulon belül nem igazolt) |
| 7 | UART0 TX (U0TXD_TP) | GPIO 37 (P64), R40 1k után (a TP14 törölve) |
| 8 | UART0 RX (U0RXD_TP) | GPIO 38 (P65), R41 1k után (a TP15 törölve) |
| 9 | 3V3 (csak szint-referencia) | az USB-UART adapter **nem táplálhatja** a lapot (nincs 2. tápbemenet, 4.1) |

### J2 – 15 pin MIPI FPC (RPi szabvány; **EV adapter sematikával / kamera modullal ellenőrizendő**)
| Pin | Jel | Pin | Jel |
|---|---|---|---|
| 1 | GND | 9 | CLK_P |
| 2 | D0_N | 10 | GND |
| 3 | D0_P | 11 | CAM_IO0 (PWDN/EN) |
| 4 | GND | 12 | CAM_IO1 (LED, NC) |
| 5 | D1_N | 13 | SCL |
| 6 | D1_P | 14 | SDA |
| 7 | GND | 15 | 3V3 (CAM_3V3) |
| 8 | CLK_N | | |

**CSI pad-sorrend vs J2 (E20, R3-C):** a modul pad-sorrendje P41 D0N, P42 D0P, P43 **CLKP**, P44 **CLKN**, P45 D1N, P46 D1P; a J2 (RPi) sorrend D0_N, D0_P, D1_N, D1_P, CLK_N, CLK_P. Következmények: (1) a **CLK pár P/N sorrendje fordított** a D párokhoz képest (modulon P,N; J2-n N,P); (2) a **pár-sorrend is eltér** (modul: D0–CLK–D1; J2: D0–D1–CLK) → sík, 2 rétegű vezetéken legalább egy **pár-keresztezés / P-N csavar** várható, ami ütközik a 13. "jelenként max 1 rétegváltás" szabállyal. **⏳ G3** (a végleges döntés a kamera kiválasztásától függ; a G2 csak a footprintből adja a térbeli sorrendet): opciók: (a) olyan kamera modul / FFC adapter, amelynek sorrendje illik a modulhoz; (b) CSI lane / polaritás csere a P4-ben (TRM) [NEM ELLENŐRZÖTT]; (c) szimmetrikus via-keresztezés a J2 padoknál (rev A-ban mérés). A lane-swapra a TRM igazolásáig nem építünk (14.).

## 7. Kamera modul követelmények (P-1, E-17, F-27, A-37)
| Követelmény | Érték |
|---|---|
| Oszcillátor, LDO-k | **kötelezően a modulon** (az FPC-n nincs XCLK) |
| **ICR (IR-cut) lencse** | **rev B-ben kötelező; rev A-ban nem**: bármely, az elektromos követelményeket teljesítő modul (NoIR vagy fix lencse), az ICR blokk DNP (K-5). Éjszakai IR-kép ICR nélkül nem teljesül (A-37) → rev B |
| Táp | 3V3 bemenet a **CAM_3V3 load switchről (kötelező, TPS22918 osztály)**; 0 Ω mérő-jumper a kapcsoló után; **CT / slew érték: `07` §4, az inrush mérendő** (K-22) |
| I2C | a modulon lévő felhúzás ellenőrzendő; MAIN-on DNP; **a felhúzás beültetése kapu: a kamera I/O szintjének ismerete** |
| CAM_IO0 | polaritás a kiválasztott modul sematikájából (5. táblázat); CAM_3V3 off → kamera biztosan nem fut, a CAM_IO0 időzítés FW-ben (táp-sorrend: 3V3 → CAM_IO0 → I2C) |
| Mechanika | **FPC hossz kapu (Q5/Q6)**: rövid flex vagy 25–30 mm egyedi kábel; a modul NYÁK-ja + holder illeszkedik a **16×16 mm** kivágásba; MAIN alkatrész a kamera alatt ≤3,3 mm; STEP szükséges (G3) |
| MIPI sebesség | cél ≤800 Mbps/lane; stream cap **1080p30** |
| Szinkron I/O szint | 1,8 V lehet a modulon; ellenőrzendő (I2C szint) |
| Beszerzés | 2–3 jelölt modul beszerzése, lemérés, **egy befagyasztása STEP-pel** → ez előzi a mechanikai véglegesítést (P-1 ⏳, Q5) |
| Szoftver | `esp_cam_sensor` verzió rögzítendő (E11) |

## 8. Stream pipeline
```
OV5640 (MIPI 2-lane, ≤800 Mbps/lane) → CSI host → ISP (max 1920×1080, E12) → [PPA: skálázás/szín] → H.264 HW encoder → RTSP szerver → esp-hosted (SDIO) → C6 WiFi
                                                                                  └─ fallback: JPEG/MJPEG HTTP
```
| Lépés | Megjegyzés |
|---|---|
| Szenzor kimenet | RAW/YUV422/RGB565 (E11); 2592×1944 a szenzor max, a pipeline **1080p30-ra cap-elve** (LOW módban 720p) |
| Szín-konverzió | ISP kimenet → H.264 bemeneti formátum (pl. YUV420): konverzió helye (ISP vs PPA), támogatott formátumok **[NEM ELLENŐRZÖTT]** |
| H.264 enkóder | P4 HW enkóder, max felbontás/fps/profil **[NEM ELLENŐRZÖTT]** |
| RTSP | könyvtár/komponens kiválasztása nyitott (Q12) |
| Fallback | MJPEG (HW JPEG) alacsonyabb fps-sel; a bitráta WiFi + tápmód függvénye |
| Sávszél | 1080p30 H.264 ~2–6 Mbps cél **[NEM ELLENŐRZÖTT]**; SDIO nem szűk keresztmetszet |
| Nap/éj | kamera AE/gain alapú váltás (nincs LDR); IR be → ICR (ha van) vált (impulzus ≤50–100 ms) |

## 9. Firmware / OTA / partíció / áramszünet-tűrés
| Elem | Terv |
|---|---|
| Partíciós tábla (16 MB) | bootloader · nvs (32K) · otadata (8K) · phy_init (4K) · coredump (64K) · `c6fw` adat (~2 MB, C6 slave kép tárolás/staging) · **ota_0 (4 MB)** · **ota_1 (4 MB)** · config (1 MB); maradék tartalék. Méretek **[NEM ELLENŐRZÖTT]**, a valódi app méret alapján finomítandó |
| P4 OTA | HTTPS letöltés → inaktív OTA partíció → rollback (app rollback + diag. önellenőrzés) [NEM ELLENŐRZÖTT: pontos Kconfig] |
| C6 OTA | esp-hosted slave OTA a P4-ről (`c6fw` partícióból/HTTPS-ből) [NEM ELLENŐRZÖTT: API verziófüggő] |
| **C6 OTA = bring-up kapu (00-K8, A-36)** | Ha a C6 gyári FW **nem** OTA-képes: egyszeri UART flash ismert slave FW-vel (10.); a C6 FW utána **nem frissíthető terepen** USB/UART nélkül → a C6 FW verziót rögzítjük, a P4 app csak kompatibilis C6 verzióval fut; a hatás a kockázati listába kerül. Ha OTA-képes: 15. 11. lépés zárja |
| Rollback védelem | P4 app a C6 verzió-kompatibilitást ellenőrzi induláskor |
| **Áramszünet-tűrés (B-8)** | A PD hard reset VBUS-t ~0 V-ra viszi, a holdup nem segít → a firmware **bármely ponton bírja az áramszünetet**: NVS/config írás atomi (journal/CRC, dupla másolat), OTA csak az inaktív partícióra, `otadata` váltás az utolsó lépés, félkész C6 staging érvénytelenítése, SD fájlrendszer-ellenőrzés indulásnál; watchdog + rollback |
| Secure boot / flash enc. | **nyitott** (Q14); eFuse visszafordíthatatlan – a bring-up után döntendő |
| Tápmód logika | 4.3; mód-döntés ≥1,5 s settle után, boot mindig LOW |

## 10. Programozás és helyreállítás
| Eset | Út |
|---|---|
| P4 első flash | USB-C (GPIO 24/25 USB-Serial-JTAG); ha az eFuse tiltja, vagy a USB nem enumerál: BOOT (GPIO 35 low) + RESET, vagy UART0 pad (GPIO 37/38, E-25) |
| P4 helyreállítás | BOOT/RESET gombok a hátoldalon elérhetők (tokozva is); UART0 tartalék pad |
| C6 első flash | UART pad (C6_U0TXD P5 / C6_U0RXD P4) + **GPIO 54 / C6_EN (P82; Q2)** + **C6_IO9 (P9)** pad |
| C6 későbbi frissítés | OTA a P4-ről (D8) – **kapu**, lásd 9. |

**C6 UART flash eljárás** (F-21/F-22/E-23):
1. P4 tartása resetben (ESP_EN lehúzva) → GPIO 54 nem hajtja a C6_EN-t. Q2: a C6_EN pull-up helyzete a modulon ismeretlen.
2. USB-UART adapter (3,3 V logika) a C6 TX/RX/GND padokra – **as-built: a J7 padsor J7.2 / J7.3 / J7.1** (DNP padsor, 1,27 mm; K-17; C6_EN = J7.6 = GPIO 54 / P82, Q2; a TP10–TP13 törölve). **A modul pad az RF padhoz (P2) közel van** (K6): a nyomvonal az ellentétes rétegen, GND köztük (P-30); a **J7 az RF-től távoli (felső) élen** (A-26).
3. C6_IO9 → GND (jumper/pogo), C6_EN rövid lehúzás → felengedés (download mód). C6_IO9 **10k felhúzás** 3V3-ra; C6_IO8: 10k felhúzás kötelező (E6).
4. `esptool` chip-id + flash-id olvasás → **F-22: gyári FW verzió lekérdezése/mentése flash előtt**.
5. Slave FW írás, IO9 jumper el, reset. JTAG (IO4–7) v1-ben nem kivezetett (F-25).

## 11. Hőkezelés (PCB-szint)
| Elem | Terv |
|---|---|
| Hőforrások | P4+C6 ~1,5 W; buck veszteség ~0,8 W csúcson (4,39 W × 0,18); IR driverek + LED-ek ~0,5–1 W; kamera ~0,7 W |
| **Hőkeret** | zárt (tömített) házban, csúcsüzemben **~4,5–4,9 W** hő (4.3: 5,6 W bemenet − optikai/RF kimenet) **[NEM ELLENŐRZÖTT]**; feltételezett **környezeti hőmérséklet: 25–35 °C beltéri** – a megengedett T_amb és a szükséges hővezetés (gap-pad/ház-hőút) a ház-döntésnél (18.) véglegesítendő; kültéri (P-39 ⏳) esetén újraszámolandó |
| Modul | hátoldalon (ház felé): Cu pour + GND via-k a modul alatt; a modul alatti GND pad ismert-e: land pattern zipből **[NEM ELLENŐRZÖTT]** |
| IR LED | 3535 pad alatti termikus via-k + hátoldali Cu terítés; CC driver (nem lineáris) → kevés disszipáció |
| Buck | GND-pour az ellentétes rétegen, hőterítés a PGND körül |
| **NTC** | NTC **ADC2 lábon (GPIO 49, tartomány 49–53)** a buck/IR zóna közelében; a P4 belső hőmérője a mag hőjét méri, az NTC a lap hőjét |
| Firmware | P4 belső hőmérő + NTC (E-32); küszöbök (kiinduló, **[NEM ELLENŐRZÖTT]**): IR teljesítmény csökkentés → fps/bitráta csökkentés → riasztás; küszöb a mérésekből |
| Mérés | bring-up 10. lépés: zárt stack hőkamerás/termopár mérés a feltételezett T_amb-en |
| Ház/gap pad | halasztva (18.) |

## 12. Teszt pontok (E-29, P-29)
**As-built (MAIN v0.6, 2026-10-10):** minden TP `TestPoint_Pad_D1.5mm` (Ø1,5 pad, BOM/CPL-ből kizárva); koordináták KiCad-keretben (§3.1a).

| TP | Háló | Oldal / pozíció | Megjegyzés |
|---|---|---|---|
| TP1 | VBUS | B (42,95; 32,25) | pogo-csoport (0,15 mm-rel a 2,75 mm-es rácson kívül) |
| TP2 | VBUS_SW | B (40,35; 29,5) | pogo-csoport |
| TP3 | GND | B (43,1; 40,5) | pogo-csoport |
| TP4 | +3V3 | B (37,6; 32,25) | pogo-csoport; az R16 0R (F, K-1) kivéve → 3V3 bench betáp (USB-vel egyszerre soha). 7. kör: a TP4 → 3V3 út ~34 mm vékony In2 réz (~0,17 Ω) → 9. kör: TP4 → U1.84–86 **72,9 mΩ** (~39 / 79 mV 0,54 / 1,08 A-en) – debug-célra elfogadható; nagy áramhoz a bench betáp inkább az R16.2 / C20-on |
| TP5 | CAM_3V3 | B (12,6; 6,6) | **külön, a csoporton kívül**, a CAM_3V3 háló mellett (R50 0R mérő-jumper után) |
| TP6 | SD_3V3 | B (36,3; 10,4) | **külön, a csoporton kívül**; FIT pad, akkor is, ha az SD blokk DNP |
| TP7 | VO4 | B (37,6; 35,0) | pogo-csoport; C24 1 µF mellett; külső forrás tilos |
| TP8A / TP8B | IR_VIN_SH / IR_VIN (shunt R72 két vége) | F (36,85; 38,45) / (31,0; 39,15) | **DNP rev A** (az IR ággal); nem a hátoldali csoportban (A-25) |
| TP16A | ESP_EN | B (40,35; 35,0) | pogo-csoport |
| TP16B | BOOT (GPIO 35) | B (43,1; 35,0) | pogo-csoport |
| TP17 | PD_PG (CH224A) | B (37,6; 37,75) | pogo-csoport |
| TP18 | GND | B (40,35; 37,75) | pogo-csoport |
| TP19 | GND | B (43,1; 37,75) | pogo-csoport |
| ~~TP9a/b, TP10–TP13, TP14–TP15~~ | ~~USB D±; C6 TX/RX/IO9/EN; UART0~~ | – | **törölve** (tulajdonosi döntés 2026-10-09, „TP ritkítás”): a C6 és az UART0 csak a J7 padsoron (§6), az USB D± a J1/U5-ön mérhető |
| – | **CSI vonalon nincs TP** | – | P-7 |

**Pad-szám (as-built):** a B oldalon **12 TP-pad** (9 jel + 3 GND: TP3, TP18, TP19); ebből **10 egy pogo-csoportban, 2,75 mm-es rácson** (x 37,6–43,1, y 29,5–40,5; TP1 0,15 mm-rel eltolva), a **TP5 és a TP6 külön** áll. A TP8A/B (F, DNP) nem tartozik a csoportba. ~~20 pad, 2,0 mm raszter (R4-terv)~~ – a pogo jig-et a fenti koordinátákból kell tervezni; a C6 programozás a J7 1,27 mm-es padjain (0,85×1,6) pogo-val vagy forrasztott headerrel.

## 13. 2 rétegű layout szabályok
> **v0.6 megjegyzés:** a MAIN 4 rétegű (§3.2) – a szélesség-/réskiinduló értékeket a §3.2 (3313A, L2 = folytonos GND) felülírja; az alábbi 2 rétegű CPWG-számok csak a FRONT-ra (és archív referenciaként) érvényesek. A szabály-elvek (CSI rétegváltás + visszatérő GND via, RF kerítés / GND-referencia, buck kis hurok, ESD a csatlakozónál) a MAIN-re is kötelezők – ~~a 7. kör szerint ezek közül több sérül~~ → **a 8. kör után teljesülnek (9. kör mérése, `90-review-log.md`): CSI páronként 2 GND return via ≤1 mm, In2 100 % GND a CSI-csonkok és az RF alatt, RF kerítés, buck forró hurok 1,44 mm²**; elfogadott rev A eltérések: CSI hossz / skew (lent), USB csak FS (§6), D1 TVS az eFuse-nál (§4.1).

Mindenre: 1,0 mm FR4, Cu 35 µm [NEM ELLENŐRZÖTT]. **Minden geometria "field solverrel ellenőrizni" a végleges stackup-pal** (JLC 2 rétegű; εr ~4,2–4,6 [NEM ELLENŐRZÖTT]).

| Terület | Szabály / kiinduló érték |
|---|---|
| MIPI-CSI (100 Ω diff) | CPW diff pár GND-vel; kiinduló: **w≈0,30 / s≈0,20 / GND rés 0,2–0,3 mm** (P-6: a **0,8 mm-es sorokból származtatva / interpolálva, 1,0 mm-re nincs független forrás** → field solver) – *field solverrel ellenőrizni*. **Rétegváltás-szabály (A-19, 06-K2; a régi "nincs via a párban" helyett):** a modul a MAIN hátoldalán, J2 a front oldalon → a pár **egyetlen szimmetrikus rétegváltással** megy át: **P és N via egymás mellett, mellettük 2 GND visszatérő via a páronként**; **jelenként max 1 rétegváltás**, lehetőleg **a J2 padoknál (≤1 mm)**; a pár többi része a hátoldalon. Hossz modul pad → J2 **<15 mm**, ±0,1 mm illesztés, ≤1 mm taper a padnál, GND padok a párok közt, CSI távol az RF-től, **≤800 Mbps/lane**, nincs TP. **Pad-sorrend (E20): D0N, D0P, CLKP, CLKN, D1N, D1P vs J2 D0, D1, CLK → pár-keresztezés / P-N csavar várható, lásd 6. J2 megjegyzés (⏳ G3). Kivétel-javaslat a "jelenként max 1 rétegváltás" alól (Q24, a G3-ban dől el): ha a kamera / FFC sorrendje nem illeszkedik, a keresztezés a J2 padoknál (≤1 mm) történik, és ehhez legfeljebb **egy további szimmetrikus via-pár** engedélyezett [NEM ELLENŐRZÖTT; rev A-ban mérés]**. **As-built (MAIN rev A, 9. kör mérése): hossz D0 10,446 / D1 15,280 / CLK 21,415 mm (P/N), páron belül ≤0,003 mm; adat–órajel eltérés D0 10,97 / D1 6,14 mm ≈ 64 / 36 ps ≈ 0,05 / 0,03 UI @800 Mbps → a „<15 mm” (CLK, D1) és az adat–órajel illesztés sérül – elfogadott rev A eltérés, a G5b soak teszt igazolja (§15 7a); csatolt (≤0,25 mm rés) szakasz csak D1 ~5 / CLK ~7 mm, a többi 0,45–0,85 mm résű (becsült Zdiff ≈115–117 Ω); páronként 2 GND return via ≤1 mm-en; a 6 CSI via a modul alatt (tentelve)** |
| GND referencia | Mivel a MAIN **kétoldalas beültetésű, nincs "tömör alsó GND sík"**: a CSI és RF nyomvonalak **alatti ellentétes rétegen összefüggő GND-pour kötelező, alkatrész-tilalommal** ott (06-K3: az RF zóna mögött és a CSI sáv mögött a front oldalon csak GND) |
| RF (50 Ω) | LNA_OUT (P2) → u.FL **CPWG**, <10 mm, via kerítés ≤2 mm; kiinduló: **w≈0,6–0,8 / gap 0,2–0,25** (becslés – a P-9 **0,8 mm-es** CPWG-sorából [w≈0,5–0,6] származtatva, 1,0 mm-re független adat nincs) – *field solver kötelező*; JLC 2 rétegű: nincs impedancia-kontroll, ±10–20 % [NEM ELLENŐRZÖTT] (3.1); π-háló footprint (DNP); alatta GND-pour, alkatrész-tilalom. **As-built (MAIN, 4 réteg): 0,302 mm microstrip B-n, In2 100 % GND referencia, út 7,96 mm (0,111 λg), kerítés mindkét oldalon 0,70–1,48 mm-re a középvonaltól, max. osztás 1,31 mm (§6 J4)** |
| USB-Serial-JTAG (12 Mbps) | rövid, ESD (3,3 V array) a csatlakozónál, 90 Ω nem kritikus 12 Mbps-en. **As-built: csak FS; a HS PHY (P48/P49) ezen a layouton soha nem engedélyezhető (§6 J1)** |
| Buck | kis hurok, bemeneti MLCC közvetlenül VIN–GND, forced-PWM, 2,2 µH Isat ≥3,5 A. **As-built: C9 100 nF 0,6 mm-re az U4 lábaitól, forró hurok 1,44 mm² (via nélkül), SW csak F-en (3,0 mm), FB 2,77 mm, SS 3,42 mm, In1 100 % alatta; L1 = Taiyo NRS5024T2R2NMGJ (Isat 4,1 A, 2,4 mm magas)** |
| Mikrofon | LC táp szűrő, CLK soros R, GND körül, digitális vezeték nem fut felette |
| SD | 4-bit, rövid, ESD ≤3,5 pF, felhúzások SD_3V3-ra |

### 13.1 EMC (A-15, F-35)
| Forrás | Intézkedés |
|---|---|
| IR LED hurok (40 kHz+ PWM, 0,3 A) | kis hurkú tápvissza (driver bemenet kondi ↔ NFET ↔ LED ↔ GND), IR_PWM/IR_VIN a B2B-n GND-del szegélyezve, LEDC ≥40 kHz (PDM alias elkerülése), a LED hurok távol a mikrofontól és a CSI-tól |
| Buck (forced-PWM) | kis kapcsoló-hurok, árnyékoló GND-pour, a bal sávban (u.FL-től és mikrofontól távol), mérés a bring-up 2. lépésben (ripple) |
| USB ESD | TPD2E2U06 / PRTR5V0U2X osztály D±-on a csatlakozónál, shield 1 MΩ ‖ 4,7 nF; TVS+ESD földje közvetlenül a csatlakozó GND-jére, nem a buck GND-áramútján át |
| WiFi (2,4 GHz) | RF út rövid és GND-kerített; CSI-tól és PDM CLK-tól távol; a C6 UART TP-k RF-től távol; 3V3 helyi bulk a TX-tüskékre (E-14); korai RSSI teszt |
| Ált. | a header-GND páronként; "no hot-plug" felirat; ESD diódák FPC vezérlő jeleken (A-10..12); előzetes sugárzási/vezetett előmérés ház nélkül és házzal (18.) |

## 14. Padtérkép (P-4, P-5, P-22) – E20 beépítve
- **Jel ↔ pad hozzárendelés: kész, primer forrás (E20).** Az 5. fejezet GPIO tábla minden pad oszlopa kitöltve (a korábbi TBD-k: GPIO 26–33 → P53–P60, GPIO 47–53 → P75–P81 stb.).
- **A térbeli elrendezés továbbra is feltételezés [F]:** óramutató-ellenes, 22 pad/oldal, a sarkoknál ~2 mm üres (06 §1). Az E20 sorrendje ezzel konzisztens csoportokat ad (1. oldal P1–P22: RF + C6 + GPIO1–7; 2. oldal P23–P44: GPIO8–13/20–23, DSI, CSI D0 + CLK; 3. oldal P45–P66: CSI D1, USB, GPIO24–38, VO4; 4. oldal P67–P88: SD-GPIO, 3V3, EN), de az élek / sarkok a Waveshare footprint importjáig [F] (06-K12).
- A CSI pad P41–P46 valószínűleg a sarkon törik (D0 + CLK az egyik, D1 a következő oldalon) [következtetés, NEM ELLENŐRZÖTT]; RF P2, ESP_EN P87, SD P67–P72 is sarok közelében lehet.
- **Modul forgatás/elhelyezés csak a footprint importja után** dönthető: CSI → J2 felé, P2 → u.FL (vagy a modul IPEX-e) felé, P50/P51 (USB) → USB-C felé; **u.FL és USB-C ellentétes élen** (A-34; 06: USB-C W él, u.FL NE sarok).
- **CSI pad-sorrend vs J2: ellenőrizve, eltérés van** (CLK P/N fordított; pár-sorrend D0–CLK–D1 vs D0–D1–CLK) – lásd 6. J2 megjegyzés és 13. CSI sor; a lane-swapra nem építünk. **A végleges döntés a G3-ban van** (kiválasztott kamera / FFC), a G2 csak a footprintből adja a térbeli sorrendet.
- Footprint import + 1:1 papír próba (tükrözés, pin 1). Ezután újrarajzolandó a 06 4. fejezete.

## 15. Bring-up sorrend (F-34 alapján)
**Konfiguráció (K-7):** a MAIN önállóan, a kamera szabványos 50–100 mm FFC-n; a stack zárása csak stabil kép után. **Előfeltétel:** G0 (dev-kit stream), G1 (CH224A). Rev A-ban DNP: SD, IR, ICR, CC-tap, supervisor.
| Lépés | Mit | Siker |
|---|---|---|
| 0 | Szemrevételezés (U3, J1, U4 mikroszkóppal), rövidzár-mérés VBUS/VBUS_SW/3V3/GND; **VBUS ↔ VBUS_SW ellenállás (JP1 0,3 mm-es nyitott forrasztóhíd – nincs maszk-gát, áthidalás az eFuse-t kiiktatná; 7. kör)**. **Első táp előtti mérések (9. kör; DMM, U1 nélkül; a VBUS_SW ~54 µF miatt 15–30 s beállás):** (a) VBUS ↔ GND (TP1–TP3) ≈ 70–73 kΩ, VBUS_SW ↔ GND (TP2–TP3) ≈ 230–255 kΩ; (b) **VBUS ↔ VBUS_SW (TP1–TP2) ≈ 300–330 kΩ** (≈ az előző kettő összege; <1 kΩ = JP1- vagy U3 IN–OUT-híd → STOP); (c) **3V3_BUCK ↔ GND (TP4–TP3, R16 beültetve) ≈ 13,5 kΩ – vizsgálni, ha <5 kΩ vagy >16 kΩ** (>16 kΩ: R14 / R15 / R33 szakadás; szakadt R14 → FB 0 V → a buck a VBUS_SW (9 V) felé futhat; az R14.1 padjába via-furat lóg); (d) **VBUS, D+, D− ↔ GND nem zárlatos** (a D± egyben az U5 klón lábkiosztását is ellenőrzi: pin 3 = GND); (e) fordított zsinórral dióda-módban 0,000 V = zárlat | nincs rövidzár, a JP1 nyitott, minden érték a sávban |
| 0a | **J1 köpenylábak** (ha a JLC nem forrasztotta, §3.1): a 4 lábat F felől forrasztani **az első kábel-bedugás előtt** (finom hegy, kevés ón), utána a láb ↔ C1.2 (GND, 0,757 mm) rés szemléje | 4 láb forrasztva, nincs híd |
| 1 | Áramkorlátos USB (5 V): CH224A, eFuse, soft start (UVLO, OVP küszöb mérése); majd 9 V PD; **VBUS_SW effektív C és attach-áram mérés**; PG és VBUS ADC; **CH224 DP/DM NC viselkedés / USB-JTAG D± ütközés teszt**; **PD hard reset ≥20×** (eFuse auto-retry, vSafe0V) | VBUS_SW stabil, OVP/UVLO viselkedés, nincs host OCP | bypass-ok (K-1) csak hiba esetén; CH224A + Rd soha egyszerre |
| 2 | Buck 3V3 modul nélkül (0 Ω nyitva) | 3V3 helyes, ripple |
| 3 | P4 modul beültetve (utoljára; **finom kúpos hegy a P83–P88-on**, fluxus – a C21–C23 0,5 mm-re a P83–P86 csúcsoktól, a C23.1 (+3V3) 0,525 mm-re a P87 (ESP_EN) csúcsától); **szemle: P87/C23 rés, R34 / J4 GND-fillet** (a P2 csúcsa 1,82 mm-re az R34.1-től); táp előtt **TP16A (ESP_EN) ↔ TP4 (+3V3) ≈ 10 kΩ** (R23; **0 Ω = híd** → nincs EN-késleltetés és a SW2 3V3–GND zárlat lenne) és 3V3 ↔ GND > 1 kΩ; majd áramfelvétel; **ESP_EN viselkedés** (rev A: supervisor DNP; R23/C25 FIT + a modul RC-je, Q3) | nincs híd, nincs túláram |
| 4 | USB enumeráció; USB-JTAG eFuse állapot (F-23); P4 flash; **strapping ellenőrzés: GPIO 34–38 szintek boot közben, a 5.1 tábla szerint; GPIO 45 (NC) szintje; az sdkconfig SD power-reset (GPIO 45) felülírásának ellenőrzése** | `esptool` elér; strap értékek egyeznek |
| 5 | C6 chip-id, gyári FW (UART padok, F-22); esp-hosted SDIO; WiFi scan | C6 látszik |
| 6 | VBUS/PG ADC (a CC ADC: rev B / ha a CC-tap be van ültetve), **tápmód logika (rev A: LOW/FULL; ≥1,5 s settle, hiszterézis); PC porton LOW boot** | küszöbök egyeznek, nincs módugrálás |
| 7 | CAM_3V3 switch (**inrush mérés**, K-22; **a TP5 (CAM_3V3) reset alatt 0 V** – R28 10k), kamera **standard 50–100 mm FFC-n, MAIN önállóan**, **a J2 kontakt-oldal (Q6) ellenőrzése után**: I2C azonosítás (100 kHz) → MIPI kép → H.264 | 1080p30 stream |
| 7a | **CSI soak teszt (G5b, 9. kör):** 1080p30 a driver tényleges lane-rátáján (≤800 Mbps/lane) **≥1 h**, a CSI hiba-, CRC- és ECC-számlálók naplózásával; megismételni a hosszú (100 mm) FFC-vel – az as-built skew (≈0,05 / 0,03 UI) és a 21,4 mm-es CLK igazolása (§13) | 0 CSI / CRC / ECC hiba, nincs képkocka-vesztés |
| 8 | SD (**rev A: DNP**; később: VO4 → 3,3 V, majd SD_EN; tri-state SD_EN előtt), PDM mic (FRONT, G6) | SD r/w, mic jel |
| 9 | (**G6, FRONT**; bench: **árnyékoló cső / ablak-távtartó**, K-19) IR eFuse #2 + driverek (ILIM, shunt áram, Vin 4,5 V-on fejmagasság), ICR impulzus (ha van) | áram a számolt; nincs reset IR zárlatra |
| 10 | Hő (NTC + belső) + WiFi TX brown-out teszt zárt stackben | nincs reset |
| 11 | **OTA (P4 + C6)**, rollback; **C6 OTA kapu (00-K8)**; **OTA közbeni PD hard reset** | sikeres frissítés USB nélkül; a rendszer visszatér |

**Rev A firmware-szabályok (9. kör; a bring-up teljes ideje alatt kötelező):** (1) **I2C 100 kHz** (a buszon csak a CH224A belső felhúzói vannak, R31/R32 DNP; SDA 112,9 mm); (2) a PD-módot a **PG (GPIO 31) + VBUS_SW ADC (GPIO 20)** adja; a CH224A-t **csak olvassuk, és csak a CAM_3V3 bekapcsolása után** (vagy egyáltalán nem) – **írni soha** (20 / 28 V-os kérés → a TVS tönkremegy); (3) **IR_SW_EN (GPIO 32) mindig alacsonyan** (az R29 lehúzás DNP); (4) **az USB HS PHY-t (P48/P49) ezen a layouton soha nem engedélyezzük** – csak USB-Serial-JTAG FS (§6); (5) NTC-modell: B = 3987 K (TH1, LCSC-adat; a típusnév „B3950”), kalibráció a G5b-n.

## 16. Gyári / első teszt terv (F-33)
Pogo jig a hátoldali pad csoportra; tesztsor: (1) áram/rövidzár, (2) 3V3/VO4/SD_3V3/CAM_3V3 mérés, (3) USB enumeráció + flash (teszt FW), **(3a) strapping szintek ellenőrzése (GPIO 34–38)**, (4) C6 UART chip-id + FW feltöltés, (5) WiFi ping/RSSI (u.FL antenna), (6) kamera kép, (7) SD r/w, (8) mic RMS, (9) IR áram, (10) ICR kattanás (ha van), (11) gomb/LED, **(11a) PD 9 V tárgyalás + PG + hard reset 20×**, (12) naplózás: MAC, chip rev, FW verziók.

## 17. Nyitott kérdések
| # | Kérdés | Hogyan zárjuk |
|---|---|---|
| Q1 | ~~SD VDDPST_5~~ ✅ E16/E17; maradék: a modulon a VDDPST_5 belül VO4-re van-e kötve (**A-28 ⏳**) | modul sematik |
| Q2 | GPIO 54 = C6_EN a modulon is? C6_EN pull-up? | Waveshare modul sematik |
| Q3 | Modulon van-e EN RC, 40 MHz XTAL, felhúzások, C6_IO9 felhúzás (**E-22 ⏳, F-16 ⏳**) – a supervisor (B-21) beültetése ezután | modul sematik |
| Q4 | Modul P4 chip revízió (v1.x vs v3.x), hosszú távú elérhetőség (**F-2 ⏳**) | Waveshare / LCSC |
| Q5 | Kamera modul: 15 pin, 3V3, **onboard osc**, CAM_IO0 polaritás (→ GPIO 23 pull), I/O szint, **rövid flex / 25–30 mm FPC**; rev A: NoIR vagy fix lencse (ICR rev B-ben kötelező) (**P-1 ⏳**) | piaci keresés + minták (G3) |
| Q6 | FPC kontakt oldal + kábel (forward/reverse), FPC hossz kapu. ~~A NYÁK-on a J2 lábkép helyőrző (TE 1-84953-5)~~ → **a J2 a megrendelt TE 1-84953-5 (TOP contact, C5164008); a bottom-contact 1-84952-5 azonos lábképű. Rossz kontakt-oldal = 3V3/GND csere a kameránál** – ~~a rendelés előtt zárandó~~ → **a kamera első bekapcsolása előtt zárandó (a NYÁK-gyártást nem blokkolja, 9. kör)** | valódi kamera modul + FFC (G3) |
| Q7 | Modul tényleges áramfelvétel | Waveshare datasheet, majd mérés |
| Q8 | Z-stack költségvetés: G = 7 mm, kamera alatt ≤3,3 mm; újraszámolás a tényleges kamera modullal | 06 + Q5 STEP |
| Q9 | MIPI PHY táp (VO3) modulon belül kezelt-e (**E-18 ⏳**) | modul sematik |
| Q10 | RF út a P2 mögött a modulon (**P-10 ⏳**) | modul sematik |
| Q11 | esp-hosted handshake/reset GPIO a modulhoz (**F-26 ⏳**) | Waveshare példa sdkconfig |
| Q12 | RTSP komponens, H.264 HW enkóder limitek, formátum-konverzió helye | IDF/esp-video docs |
| Q13 | **CH224A adatlap**: feszültség-strap tábla, PG polaritás, belső Rd, DP/DM kezelés, kondi-igény; **eFuse konkrét típus** (állítható OVP, reverse-blocking, auto-retry, UVLO, ILIM); TVS SMAJ10A adatlap; **IR eFuse #2 típus** (≥18 V, állítható ILIM) | adatlapok (jelenleg [NEM ELLENŐRZÖTT]) |
| Q14 | Secure boot / flash encryption | bring-up után |
| Q15 | 👤 Beltéri v1? (**P-39 ⏳**; hat a hőkeret T_amb-jére és a LED-választásra) | tulajdonos |
| Q16 | C6 gyári FW OTA-képes-e (**00-K8 kapu**) | bring-up 5. és 11. lépés |
| Q17 | **B2B 2×10 1,27 mm header-pár, 7 mm párosított magasság**: létező alkatrész, elérhetőség, tűrés, áramterhelhetőség. **2026-10-11: 7,00 mm-es kész pár nincs; BOM-ban a Hong Cheng pár (C41375929 + C27985222, 5,3 mm → ~2,3 mm merülés 7,0 mm-nél, MAIN változatlan) – alternatíva Samtec FTSH-110 / FLE-110 (7,47 mm; 7,5 mm távtartó + MAIN lábkép-csere a rendelés előtt)** | 👤 tulajdonosi döntés (`07` §0) |
| Q18 | Buck L/Cout tartomány a választott típuson (**B-27 ⏳**) | buck adatlap |
| Q19 | IR LED típus: Vf_max(−20 °C), 2-LED soros vs egyes ág döntés (4.2 kritérium) | LED adatlap |
| Q20 | PDM mikrofon típus: MSM261D3526H1CPM / MP34DT05-A [NEM ELLENŐRZÖTT], elérhetőség | adatlap |
| Q21 | P4 strapping tábla (GPIO 34–38) funkciói | P4 adatlap (5.1 TODO) |
| Q22 | ✅ **Lezárva: rev A MAIN 60×50 mm** – **felülírva (2026-10-09): MAIN 45×45, 4 réteg (00 K4); as-built interfész §3.1a**. Eredeti: Rev A MAIN nagyobb (pl. 60×50 mm) azonos M2 raszterrel és J2/J5 koordinátákkal? (a 45×45 marad a cél, K-12) | tulajdonos |
| Q23 | USB-megnevezés: USB-Serial-JTAG GPIO 24/25; az OTG FS nincs használatban (sdkconfig, P4 adatlap) [NEM ELLENŐRZÖTT] | G0 sdkconfig |
| Q24 | CSI pad-sorrend / CLK P/N eltérés kezelése: lane / polaritás csere a P4-ben, kamera / FFC sorrend, via-keresztezés (6. J2 megjegyzés) | TRM, G3 (a footprint térbeli sorrendje: G2) |
| Q25 | Antenna: a modul saját IPEX-e használható-e (hátoldali, elérhető)? RSSI két antennával | G0 / G2 |
| Q26 | EDA = **KiCad** ✅; nyitott: USB-C THT shell JLC-beültetése (3.1) → **a köpenylábak paszta nélküliek: JLC kézi / szelektív forrasztás vagy saját forrasztás az első bedugás előtt (§0.4, §15 0a)** | rendeléskor |

## 18. Halasztva (ház)
Ide kerültek a ház-szintű tételek: ház anyaga, ablak 850 nm áteresztés, IR szem-biztonság (IEC 62471, P-38; a LED-áram plafon PCB-követelmény, 4.2), kültéri/beltéri védelem (P-39), szellőzés/hővezetés a T_amb feltételhez (11.), gap-pad a hátfalra (P-20), fekete hab gyűrű az IR szivárgás ellen (P-17 ház-oldal), mikrofon tömítés, tűlyukas BOOT/RESET és fényvezető (P-31), microSD rés oldalról (06-K10), pogo ablak (P-29), USB kábel húzásmentesítés (P-40), antenna kábel rögzítés. **PCB-szinten megmarad:** furatok/távtartók, FPC hozzáférés, IR baffle Cu gyűrű, gombok/TP elérhetősége.

## 19. Review-lefedettség (✅ tételek → szekció)

**R1 (kör 1):** E-1,2,13 → 4.1 · E-3,4,5 → 5 · E-6,8 → 5/5.1 · E-9,10,19 → 2/D9, 4.2, 6 · E-11,12 → 4.1/4.3 · E-14,15 → 4.1/13 · E-16,31 → 5/13 · E-17,26,F-27 → 7/5 · E-20,21 → 5/D7 · E-23,F-21,22 → 10 · E-24,25 → 5/6/10 · E-27 → 13 · E-28 → 3 · E-29 → 12 · E-30,P-37 → 3 · E-32,P-20 → 11 · E-33,F-18 → 4.3 · E-34 → 5 · E-35 → 2/D5, 4.1 (nincs 2. bemenet) · E-36,F-1,9,10,11 → banner 01–04 · P-1 → 7 (⏳) · P-2,3,8,13,14,16,21,23,24,34,35 → 3 · P-4,5,22 → 14 (⏳ footprint) · P-6,7,9 → 13 · P-11,12 → 3 · P-15 → 6 · P-17,28 → 3 · P-19 → 3 · P-25,26,27,29,30,31,32,33,36 → 3/4.1/10/12 · P-38,40 → 18 · F-3 → 4.3 · F-4 → 5 · F-5 → 3/6 · F-6 → D9 · F-7,30..32 → 5 · F-8 → 5.1 · F-12,24 → 5.1/15 · F-14,15 → 7 · F-17 → 4.2 · F-19,20 → 8/11/16 · F-23,25 → 10/15 · F-28 → 8 · F-29 → 3 · F-33 → 16 · F-34 → 15 · F-35..38 → 13.1/14/5.
**R2-B (kör 2):** B-1 → 5 (GPIO 24/25), 6, 13 · B-2 → 4.3 (szabály 1) · B-3 → 4.1 (CC-tap), 4.3 · B-4 → 2/D5, 4.1 · B-5 → 4.1 (külső Rd tilos) · B-6 → 4.1, 5 · B-7 → 4.1, 15/1 · B-8 → 4.3 (5. szabály), 9, 15/1, 15/11, 16 · B-9 → 4.1 (eFuse) · B-10 → 4.1 (kapacitás) · B-11 → 2/D5, 4.1 (9 V) · B-12 → 4.1 (TVS) · B-13 → 4.1 (strap) · B-14 → 4.2 (kritérium) · B-15 → 4.2 (NFET, Cout) · B-16 → 4.2 (ICR 3V3) · B-17 → 4.3 (módtábla) · B-18 → 4.3 (újraszámolás) · B-19 → 4.3 (LOW) · B-20 → 4.1 (UVLO) · B-21 → 5 (ESP_EN supervisor; Q3 ⏳ után) · B-22 → 4.1, 5 (GPIO 33), 7 · B-23 → 4.1 (VBUS osztó), 5 · B-24 → 5 (SD 5. szabály) · B-25 → 4.1, 4.2, 5 (GPIO 32) · B-26 → 11 (NTC, hőkeret), 5 · B-27 → Q18 ⏳ · B-28 → 4.1 (effektív C) · B-29 → 4.2, 6 (J5) · B-30 → 4.2, 5 (LEDC ≥40 kHz).
**R2-A (kör 2):** A-3 → 5, 7 · A-4 → 5, 10 (C6_IO9 felhúzás) · A-5/6 → 4.2, Q19–Q20 (IR, PDM jelölve) · A-7 → 5, 7 (I2C gate) · A-8 → 4.3 · A-9 → 5.1, 15/4, 16/3a · A-10..12 → 6, 13.1 · A-13 → 4.2 (szem-biztonság), 3 (06 hivatkozás) · A-14 → 7 (CAM_IO0 időzítés) · A-15 → 13.1 · A-17 → 4.1 (nincs 2. bemenet) · A-18 → 19 · A-19 → 13 (CSI rétegváltás), 3 · A-20/21 → 4.1 · A-22/23/24 → 4.1, 4.3 · A-25 → 4.1, 4.2, 12 (TP8) · A-26 → 10, 12 · A-27 → 5 · A-28 → Q1 ⏳ · A-29 → 5.1 · A-30 → 1 (P48/P49), 5 · A-31..33 → 1, 5, 10 (P-notáció, C6_IO8) · A-34 → 3, 14 · A-35 → 4.2 · A-36 → 9, 15/11 (C6 OTA kapu) · A-37 → 2/D3, 7 · A-38 → 5, 6 (user gomb).
**Koordinátori döntések (v0.3):** VBUS 9 V → 4.1 · CH224A+PG → 4.1 · tápmódok → 4.3 · újraszámolás → 4.3 · ESD → 5 · IR → 4.2 · ICR/Q5 → 4.2, 7 · CAM_3V3 → 4.1, 7 · supervisor → 5 · CSI/GND → 13 · stack 7 mm → 3 · P-notáció → 1, 5, 10, 14 · strapping/EMC/NTC/PD hard reset/C6 OTA → 5.1, 13.1, 11, 9, 15, 16.
**R3-C (kör 3):** 06 konzisztencia (ESD, CC-tap, 7 mm rés, TP8, költségvetés, bulk, TP-szám, FFC, lencse) → 06 v0.2 · GPIO2–4, GPIO0/1, GPIO45, pad-eredet, GPIO23 → 5 · CC-tap állítás → 4.1 · tápmódonkénti forrás → 4.3 · hivatkozás-előtagok → D8, 9, 15, Q16 · C6_IO8 → E6, 5 · VEML → D7 · 00 mic → 00 · USB-megnevezés → E4, 5, 13, Q23 · CPWG → 13.
**R3-K (kör 3):** K-1 → 0.1, 4.1 · K-2 → 0.2 (G0) · K-3 → D9, 4.1, 4.2 · K-4 → 4.1, 0.2 (G1) · K-5 → D3, 4.2, 7 · K-6 → E7, 3, 0.2 (G2) · K-7 → 0, 3, 15 · K-8 → 0.2 (G4), `07` · K-9 → 0.3 · K-10 → 3, 3.1 · K-12 → 0, Q22 · K-13 → 0, 3 · K-14..K-17 → 0.1, 5, 6 · K-18 → 3.1 · K-19 → 4.2, 15 · K-20, K-22 → `07` §3–§4, 7.
**R4 (kör 4, `08` hibalista 1–23):** 1 → 0.1 · 2, 3 → 12 · 4 → 5, 6, 10, 12 · 5, 6 → 4.1 · 7 → 4.1, 5, 6 · 8 → 4.2, 5 · 9 → 0.1 · 10 → 0.1 · 11 → D9, 4.1, 4.2 · 12 → 4.3, 15 · 13 → 6 (J7) · 14 → `07` · 15, 16 → 0.2 (G3), 6, 13, 14, Q24 · 17 → 0.2 (G5b) · 18 → téves · 19 → 6 · 20 → 5 · 21 → 3, 4.1 · 22 → 06-K5 · 23 → 0.4.
**R9 (9. kör, végső többagentes review, 2026-10-11, `90-review-log.md`):** C14 → 0.1, 4.1 · D1 hely → 0.1, 3, 4.1 · J2 / J5 / Q6 / Q17 → 0.1, 3.1a, 6, 17 · MH + alátét → 3, 3.1a · stackup / rendelés előtti kapu / panel → 3, 3.1 · J1 köpenyláb → 3.1, 0.4, 15 · USB FS → 5, 6, 13 · CSI as-built + soak → 13, 15 · bring-up mérések, U1 kézi forrasztás, FW-szabályok → 15 · BOM → `07` §0 · as-built elhelyezés → `06`.
**⏳ nyitva (nem építve be):** E-18, E-22, P-1, P-4, P-5, P-10, P-39, F-2, F-16, F-26, B-27, A-28 → 17.
