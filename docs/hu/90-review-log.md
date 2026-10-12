# 90 – Review log

Jelölés: ✅ elfogadva → javítandó 05-ben (alkalmazva) · ❌ elutasítva (indok) · ⏳ nyitott / kapu (külső adat vagy mérés kell) · 👤 tulajdonosi döntés · ⟲ későbbi tétel felülírta

## Review kör 1 (2026-10-09)

### R1-E: Elektromos / táp / sematik teljesség (Sonnet) — 36 tétel

| # | Súly | Megállapítás | Javítás | St. |
|---|---|---|---|---|
| E-1 | BLOCKER | 5,5 V-os buck (SY8089/TPS62A02) USB-C hot-plug tüskénél (~2× VBUS) tönkremehet; SMBJ5.0A clamp ~9 V | Buck ≥17 V bemenettel (TPS62933 osztály) **vagy** eFuse/OVP (~5,8–6 V) előtte | ✅ |
| E-2 | BLOCKER | VBUS kapacitás attach-kor USB limit ~10 µF; 100/470 µF közvetlenül VBUS-on → host OCP | ≤10 µF csatlakozó oldalon, soft-start eFuse, bulk utána; 04-doc 470 µF törlés | ✅ |
| E-3 | BLOCKER | SD lábak VO4 domainen (alap 1,8 V) → 10k felhúzás 3V3-ra = túlfeszültség boot alatt | Felhúzások kapcsolt SD_3V3-ra; FW: VO4 → 3,3 V előbb, utána SD táp; CD + load switch EN le VO4-ről (GPIO26–33) | ✅ |
| E-4 | BLOCKER | Kártya visszatáplálás kikapcsolt load switchnél | Felhúzás + ESD a kapcsolt sínen; load switch kisütéssel (TPS22918); 10 µF + 100 nF | ✅ |
| E-5 | HIGH | VO4 (pad 66) kezelés hiányzik | 1 µF + TP, külső forrás tilos; GPIO47/48 is VO4 | ✅ |
| E-6 | HIGH | Strapping GPIO34–38 hiányos; 34 a szabad listában | 34/37/38 terhelés nélkül; debug pad soros 1–4,7k; strapping tábla datasheetből | ✅ |
| E-7 | HIGH | 05 §5 pin-számok ütköznek 01-gyel | ❌ 01 = chip QFN láb, 05 = modul pad (Waveshare tábla). 01-be banner | ❌ |
| E-8 | HIGH | IR PWM + ICR bemenet lebeg boot alatt | 100k lehúzás; inkább GPIO26–33 | ✅ |
| E-9 | HIGH | ICR tekercs adat ismeretlen; H-híd MAIN, tekercs FRONT | ICR datasheet előbb; H-híd FRONT-ra (DRV8837); nincs ICR → törlés | ✅ |
| E-10 | HIGH | IR LED driver alulméretezett | LED szám rögzítés; áramgenerátor/1206 ellenállás; AO3400; PWM ≥20 kHz (**→ ≥40 kHz, B-30**); 10–22 µF LED anódnál (**→ Cout ≤1 µF, B-15**) | ✅ ⟲ B-15, B-30 |
| E-11 | HIGH | CC közvetlenül GPIO-ra | 1k + BAT54S clamp + 100 nF (**→ 100k + 10 nF + Zener, B-6**); küszöb 0,25–0,61 / 0,70–1,16 / 1,31–2,04 V | ✅ ⟲ B-6 |
| E-12 | HIGH | >500 mA default port; boot = csúcs | Boot sorrend P4+C6 → CC → kamera+SD → IR; WiFi TX limit; min. 5 V/1,5 A forrás | ✅ |
| E-13 | HIGH | PTC 1,5 A melegben ~1 A | eFuse ~2 A (E-1/E-2-vel egyben) | ✅ |
| E-14 | HIGH | WiFi TX brown-out | 47–100 µF + 10 µF + 100 nF modul 3V3 padoknál | ✅ |
| E-15 | HIGH | Buck PFM zaj → mikrofon | forced-PWM, 2,2 µH Isat ≥3,5 A, mic LC szűrő | ✅ |
| E-16 | HIGH | Mic: 04 I2S vs 05 PDM, nincs part | PDM (MSM261D3526H1CPM / MP34DT05-A); CLK 33–100 Ω soros | ✅ |
| E-17 | HIGH | Kamera modul I2C szint, oszc., EN polaritás ismeretlen | Modul választás előbb; I2C felhúzás DNP; CAM_IO0 lehúzás; 0 Ω kamera 3V3-ban | ✅ |
| E-18 | HIGH | MIPI PHY táp (VO3) modulon belül? | modul sematik | ⏳ |
| E-19 | HIGH | J5 2×8 kevés GND | 2×10; IR driver + ICR FRONT-ra | ✅ |
| E-20 | MEDIUM | ADC1 csak GPIO20–23, mind foglalt | LDR ki → GPIO20 VBUS monitor | ✅ |
| E-21 | MEDIUM | Fényérzékelő látja saját IR-t | kamera AE/gain alapú váltás; opc. VEML7700 árnyékolva | ✅ |
| E-22 | MEDIUM | Reset RC dupla lehet | modul sematik | ⏳ |
| E-23 | MEDIUM | C6_EN pad hiányzik | TP C6_EN (pad 82), C6_IO9; 10k C6_IO8 + IO9 felhúzás | ✅ |
| E-24 | MEDIUM | USB-C shield, D± duplikálás, VBUS detect | 1 MΩ ‖ 4,7 nF; VBUS osztó | ✅ |
| E-25 | MEDIUM | USB-JTAG az egyetlen helyreállítás | UART0 pad tartalék; BOOT/EN elérhető tokozva | ✅ |
| E-26 | MEDIUM | Kamera 3V3 mindig be | load switch vagy CAM_IO0 lehúzás | ✅ |
| E-27 | MEDIUM | RF 50 Ω alul specifikált | stackup előbb, π-háló footprint | ✅ |
| E-28 | MEDIUM | NYÁK vastagság konfliktus | egy vastagság, minden arra számolva | ✅ |
| E-29 | MEDIUM | Teszt pont lista hiányzik | TP + 0 Ω mérő-jumperek | ✅ |
| E-30 | MEDIUM | ESD SD/FPC/header | SD ESD ≤3,5 pF; "no hot-plug" felirat | ✅ |
| E-31 | MEDIUM | Mic akusztika + zaj | LC, távolság, tömítés | ✅ |
| E-32 | MEDIUM | Hő | P4 belső hőmérő + IR throttling | ✅ |
| E-33 | LOW | Kamera áram ~200 mA lehet | mérés | ✅ |
| E-34 | LOW | WS2812 3,3 V adattal | diszkrét 0603 LED | ✅ |
| E-35 | LOW | Bench táp visszatáplálás | nincs 2. bemenet | ✅ |
| E-36 | LOW | 01/04 elavult állítások | banner | ✅ |

### R1-P: NYÁK / mechanika / gyártás (Sonnet) — 40 tétel

| # | Súly | Megállapítás | Javítás | St. |
|---|---|---|---|---|
| P-1 | BLOCKER | Kamera modul nincs kiválasztva → minden mechanika ettől függ | 2–3 jelölt beszerzése, lemérés, egy befagyasztása STEP-pel | ✅ |
| P-2 | BLOCKER | Nincs megadva a modul melyik oldalon van a MAIN-en; ütközik a kamerával | Modul + USB-C + u.FL + gombok a **hátsó** oldalon; FPC, B2B, buck, SD a kamera felőli oldalon; Z-stack költségvetés | ✅ |
| P-3 | BLOCKER | 38×38 mm irreális (modul körül 6,5 mm gyűrű) | ~45×45 mm kétoldalas, vagy 3 lap (POWER+USB / MAIN / FRONT); 1:1 mechanikai vázlat sematik előtt | ✅ |
| P-4 | BLOCKER | 88 pad ≈ 22/oldal → CSI pad 41–46 a sarkon törik (41–44 oldal 2, 45–46 oldal 3); RF pad 2 + EN 87 sarok; SD 67–72 sarok | Waveshare footprint → valós padtérkép; modul forgatás: CSI J2 felé, pad 2 u.FL felé, USB pad USB-C felé | ✅ |
| P-5 | HIGH | CSI pad sorrend vs FPC sorrend → sávkeresztezés via-val | Ellenőrzés forgatás előtt; lane swap-ra nem építünk | ✅ |
| P-6 | HIGH | 100 Ω diff 2 rétegen: 1,6 mm-en csak CPW (w≈0,20–0,25 / s≈0,15–0,20 / GND rés 0,2–0,3); 0,8 mm-en w≈0,30–0,35 / s≈0,2 [U] | MAIN 0,8–1,0 mm; field solver; lane rate korlát (≤800 Mbps/lane, 1080p30) | ✅ |
| P-7 | HIGH | Pad → pár átmenet, harmonikusok 2,4 GHz-en | ≤1 mm taper, GND padok párok közt, CSI távol RF-től, nincs TP CSI-n | ✅ |
| P-8 | HIGH | 0,8 mm lap: USB-C/SD mechanika, vetemedés | **1,0 mm** + 4 távtartó + ház támasztás | ✅ |
| P-9 | HIGH | 50 Ω RF 2 rétegen (0,8 mm ≈1,5 mm széles; 1,0 mm ≈1,8 mm) | CPWG (w≈0,5–0,6 / gap 0,2–0,25 @0,8 mm), via kerítés ≤2 mm, π-háló | ✅ |
| P-10 | HIGH | Modulon belüli RF út (pad 2 mögött mi van) dokumentálatlan | modul sematik | ⏳ |
| P-11 | HIGH | Antenna helye a stackben | külső FPC antenna műanyag falon, ≥15 mm fémtől; műanyag ház; korai RSSI teszt | ✅ |
| P-12 | HIGH | u.FL mechanika gyenge | lapszélen, húzásmentesítés | ✅ |
| P-13 | HIGH | FPC ZIF nem nyitható zárt stackben | szélre tett J2, összeszerelési sorrend, ≥20 mm ráhagyás | ✅ |
| P-14 | HIGH | FPC hossz/hajlítás | 40–60 mm, S-hurok, merevítő, egyenes kábel | ✅ |
| P-15 | HIGH | B2B header áram/zaj | ≥2× 5 V, ≥3 GND, GND a PDM körül, PWM nem a mic mellett; I2C felhúzás egy helyen | ✅ |
| P-16 | HIGH | Header magasság tűrés | definiált magasságú header, távtartó a szerkezeti elem | ✅ |
| P-17 | HIGH | IR szivárgás a lencsébe (FR4 átengedi 850 nm-t) | Cu gyűrű + fémezett furat, fekete hab gyűrű, LED ≥10 mm tengelytől, külön ablak-apertúra | ✅ |
| P-18 | HIGH | ALS saját IR → oszcilláció | = E-21 | ✅ |
| P-19 | HIGH | Mikrofon akusztika | = E-31 + ≥10 mm IR LED/ICR-től | ✅ |
| P-20 | HIGH | Hő 1,5–2 W zárt dobozban | modul hátoldalon → gap-pad a hátfalra; GND via-k; CC LED driver; throttling | ✅ |
| P-21 | HIGH | Összeszerelési sorrend, modul reflow | JLC SMT minden más, modul utoljára kézzel/hot-plate | ✅ |
| P-22 | MEDIUM | Footprint tükrözés / pin 1 hiba | Waveshare footprint import, 1:1 papír próba | ✅ |
| P-23 | MEDIUM | M2 furatok a modul sarok-padjainál | 33–34 mm közös raszter, 2,2 mm NPTH, 3,8 mm keep-out | ✅ |
| P-24 | MEDIUM | Kamera rögzítés FRONT-hoz nincs definiálva | 2 NPTH datum, lencse furat +0,5 mm | ✅ |
| P-25 | MEDIUM | USB-C mechanika | 4 THT shell láb, ház fogja | ✅ |
| P-26 | MEDIUM | SMBJ + 100 µF elko nagy | SMAJ/SOD-123 TVS, MLCC/polimer | ✅ |
| P-27 | MEDIUM | Buck layout zsúfolt sarokban | u.FL-lel és mic-kel ellentétes sarok | ✅ |
| P-28 | MEDIUM | IR LED gyűrű vs lencse furat | 3535 LED, ≥10 mm sugár, hátoldali Cu hőterítés | ✅ |
| P-29 | MEDIUM | Teszt hozzáférés stackben | pogo pad csoport hátoldalon + ház ablak | ✅ |
| P-30 | MEDIUM | C6 UART padok az RF pad mellett | ellentétes rétegen, GND köztük; IO9 jumper | ✅ |
| P-31 | MEDIUM | Gomb/LED ház interfész | tűlyukas BOOT/RESET, fényvezető | ✅ |
| P-32 | MEDIUM | microSD hozzáférés | lapszél, ház rés, távol RF-től | ✅ |
| P-33 | MEDIUM | VO4 + 3V3 decoupling a sarokban | = E-5 | ✅ |
| P-34 | MEDIUM | Panelizálás nincs | tab-route + mouse bite, 3 fiducial, lapok külön | ✅ |
| P-35 | MEDIUM | JLC DFM + alkatrész elérhetőség | ellenőrizni (header, FPC, u.FL, USB-C THT) | ✅ |
| P-36 | MEDIUM | 3 lapos opció döntés most | = P-3 | ✅ |
| P-37 | LOW | Selyemnyomat jelölések | pin 1, FPC kontakt oldal | ✅ |
| P-38 | LOW | Ház: szellőzés, ablak 850 nm, IR szem-biztonság (IEC 62471) | 06-mechanika doc | ✅ |
| P-39 | LOW | Kültéri/beltéri? | beltéri v1 (felhasználói megerősítés) | ⏳ **halasztva (ház, 05 §18; Q15)** |
| P-40 | LOW | USB kábel húzásmentesítés | ház | ✅ |

### R1-F: Firmware / konzisztencia (Haiku) — 38 tétel (duplikátumok az E/P tételekre hivatkoznak)

| # | Súly | Megállapítás | Javítás | St. |
|---|---|---|---|---|
| F-1 | BLOCKER | 01 "54-es láb" = chip láb (VDD_HP_1), nem GPIO54 | 01 banner; GPIO54 = E18 (esp-hosted) | ✅ |
| F-2 | HIGH | Modul chip: NRW32 (v1.x?) vs új tervhez v3.x | revízió + elérhetőség (Q4) | ⏳ |
| F-3 | HIGH | Átlag 610 mA már nappal >500 mA | min. forrás **5 V / 2 A**; CC policy minden terhelésre (**felülírva: B-17 FULL/MID/LOW, tápmódonkénti minimum forrás 4.3**) | ✅ ⟲ B-17 |
| F-4 | HIGH | SD VO4 domain | = E-3 | ✅ |
| F-5 | BLOCKER | Kamera topológia: FRONT-on a kamera, J2 MAIN-en → FPC útja nem definiált | Kamera modul saját FPC-je közvetlenül MAIN J2-be (a két lap közötti résben); hossz/útvonal §6-ban | ✅ |
| F-6 | HIGH | IR driver helye vs header, LED visszatérő út | driver FRONT-ra (= E-19) | ✅ |
| F-7 | MEDIUM | Mic I2S vs PDM | = E-16 (PDM) | ✅ |
| F-8 | MEDIUM | GPIO34 szabad listában | = E-6 | ✅ |
| F-9 | MEDIUM | 02/04 USB HS-t ír, 02 OTG GPIO20/21 hibás | egyetlen USB-C → GPIO24/25; 02/04 banner | ✅ |
| F-10 | MEDIUM | 02 elavult (külön C6 modul) | banner | ✅ |
| F-11 | MEDIUM | 03 szerint OV5640 MIPI nem igazolt | 03 banner → E11 felülírja; esp_cam_sensor verzió rögzítés | ✅ |
| F-12 | MEDIUM | Strapping logika tényként | datasheet strapping tábla, valós boardon teszt | ✅ |
| F-13 | MEDIUM | Reset RC 100 nF vs 1 µF | = E-22 | ⏳ |
| F-14 | MEDIUM | Kamera táp sorrend ellentmond | saját LDO-s modul kezeli; CAM_IO0 időzítés FW-ben | ✅ |
| F-15 | MEDIUM | Kamera I/O szint 1,8 V lehet | = E-17 | ✅ |
| F-16 | MEDIUM | Modul belső DCDC állítás wikiről | modul sematik (Q3) | ⏳ |
| F-17 | LOW | IR LED szám/hullámhossz/LED típus nincs 05-ben | = E-10, E-34; 850 nm | ✅ |
| F-18 | LOW | Áramkeret/bulk számok eltérnek | egy készlet 05-ben | ✅ |
| F-19 | MEDIUM | Hő szekció hiányzik (00 követelmény) | = E-32/P-20, új szekció | ✅ |
| F-20 | MEDIUM | Lefedettség: stream pipeline + hő nincs; K6/K7/SD/mic/ICR részleges | új szekciók | ✅ |
| F-21 | BLOCKER | C6 download nem érhető el | C6_EN (GPIO54) + IO9 pad lehúzás opcióval; eljárás dokumentálása | ✅ |
| F-22 | HIGH | C6 gyári firmware ismeretlen | első lépés: UART padokon C6 chip ID + FW verzió | ✅ |
| F-23 | MEDIUM | USB-JTAG engedélyezett-e (eFuse) | első bring-up | ✅ |
| F-24 | MEDIUM | UART0 pad strapping veszély | = E-6 | ✅ |
| F-25 | LOW | C6 JTAG/strapping padok | C6 JTAG nem kivezetett v1-ben | ✅ |
| F-26 | MEDIUM | esp-hosted handshake/reset GPIO a modulhoz | Waveshare példa sdkconfig | ⏳ |
| F-27 | HIGH | XCLK: 15 pin FPC-n nincs | kötelező: modul saját oszcillátorral (Q5) | ✅ |
| F-28 | HIGH | Stream pipeline nincs leírva; 03 2592×1944 vs ISP 1080p | új szekció: 1080p30 cap, ISP → H.264, MJPEG fallback | ✅ |
| F-29 | HIGH | NYÁK vastagság nincs rögzítve | = P-8: 1,0 mm | ✅ |
| F-30..32 | MED/LOW | ADC1 ok, LEDC ≥20 kHz, I2S0 a mic-é | rögzítés (**LEDC → ≥40 kHz, B-30**) | ✅ ⟲ B-30 |
| F-33 | MEDIUM | Gyári teszt terv nincs | új szekció | ✅ |
| F-34 | MEDIUM | Bring-up sorrend | új szekció (F-34 javaslat alapján) | ✅ |
| F-35..38 | LOW/MED | EMC, footprint import, VDDPST_5/VO4 elnevezés, E5 következtetés jelölés | rögzítés | ✅ |

### Összesítés kör 1
- 114 tétel, ebből BLOCKER: E-1..4, P-1..4, F-1, F-5, F-21 → **11**
- ⏳ külső adat kell (Waveshare modul sematik PDF, kamera modul): E-18, E-22, P-10, F-2, F-16, F-26, P-39

## Review kör 2 (2026-10-09) — 05 v0.2-re

### R2-B: Táp front-end mélyelemzés (Sonnet) — 30 tétel
| # | Súly | Megállapítás | Javítás | St. |
|---|---|---|---|---|
| B-1 | BLOCKER | USBLC6-2SC6 VBUS lába ~5 V-os; 9 V VBUS-on tönkremegy | pin 5 → 3V3, vagy VBUS láb nélküli 3,3 V array (TPD2E2U06 / PRTR5V0U2X) | ✅ |
| B-2 | HIGH | PD race: boot 5 V-on, 9 V csak 0,3–1 s múlva → rossz módválasztás | mód döntés ≥1,5 s settle után vagy PG/VBUS>8 V; folyamatos újraértékelés | ✅ |
| B-3 | HIGH | CC DC szint PD alatt ugrál (Rp toggle), sávok 90 mV-ra | FULL = VBUS≥8 V; CC csak nem-PD 5 V-ra, medián + hiszterézis | ✅ |
| B-4 | HIGH | CH224K ≠ CH224A (K: nincs I2C, csak PG) | választás: K + PG → GPIO + VBUS ADC, vagy I2C-s sink (CH224A/HUSB238/STUSB4500) | ✅ |
| B-5 | HIGH | CH224 belső 5,1k Rd → külső Rd TILOS | szabály a doksiba; MCU tap ≥200k (**tap-érték felülírva: B-6 → ≥100k**; a "külső Rd TILOS" marad, rev A DNP kivétellel: K-1) | ✅ ⟲ B-6 |
| B-6 | HIGH | CC tap 1k + 100 nF = AC terhelés PD BMC-re (max 200–600 pF); BAT54S 3V3-ra pumpál | ≥100k soros, 10 nF ADC-nél, 3,6 V Zener | ✅ |
| B-7 | HIGH | CH224 DP/DM (BC1.2/QC) ütközik USB-JTAG D±-szal | NC (ha datasheet engedi), különben bring-up teszt | ✅ |
| B-8 | HIGH | PD hard reset → VBUS ~0 V; holdup hasztalan | eFuse auto-retry; FW áramszünet-tűrő NVS/OTA; 20× hard reset teszt | ✅ |
| B-9 | HIGH | eFuse visszáram → vSafe0V check bukik | reverse-blocking eFuse | ✅ |
| B-10 | HIGH | Downstream C × PD slew (30 mV/µs) → 100 µF = 3 A > ILIM | VBUS_SW effektív C ≤47 µF, ILIM/timer erre | ✅ |
| B-11 | HIGH | VBUS 5–12 V vs OVP 10,8 V vs TVS ellentmond | **max 9 V**; állítható OVP eFuse 10,5–11 V | ✅ |
| B-12 | HIGH | TVS clamp vs eFuse abs-max | SMAJ10A; szivárgás 9,45 V/85 °C | ✅ |
| B-13 | HIGH | CH224 lebegő feszültség-strap → 20 V kérés | fix ellenállás GND-re, 20 V eset OVP-be fut | ✅ |
| B-14 | HIGH | IR CC 5 V-on: 2 LED string ~4,0 V vs 4,5 V Vin → 90% duty | ≥95% duty / LDO-CC, vagy 3 párhuzamos 1-LED ág | ✅ |
| B-15 | HIGH | 20 kHz PWM vs 10–22 µF a LED-en | soros NFET dimming, Cout ≤1 µF; nagy C a bemenetre | ✅ |
| B-16 | HIGH | ICR H-híd táp (DRV8837 VM ~11 V max) | 3V3-ról vagy LDO-ról, sosem VBUS_SW-ről | ✅ |
| B-17 | MEDIUM | 5 V/1,5 A mód ellentmondás | FULL / MID / LOW három mód | ✅ |
| B-18 | MEDIUM | Áramok 5,0 V-tal, η 0,88 optimista | újraszámolás 4,5 V, η 0,82, nappali csúcs oszlop | ✅ |
| B-19 | MEDIUM | PC porton 500 mA kevés boothoz | kemény LOW boot (kamera off, TX ≤10 dBm, 720p); PC = best effort | ✅ |
| B-20 | MEDIUM | UVLO nincs definiálva | eFuse UVLO ~4,4/3,9 V | ✅ |
| B-21 | MEDIUM | Nincs supervisor | TPS3840 osztály ESP_EN-re (modul RC után) | ✅ |
| B-22 | MEDIUM | Kamera 3V3 0 Ω, nem kapcsolt | load switch CAM_3V3 | ✅ |
| B-23 | MEDIUM | VBUS osztó: TVS clamp → 4,25 V GPIO20-on, visszatáplálás | VBUS_SW-ről, ≥200k/54k + Zener | ✅ |
| B-24 | MEDIUM | SD lábak hajtva SD táp nélkül | FW tri-state SD_EN off előtt | ✅ |
| B-25 | MEDIUM | Közös ILIM: IR hiba resetel mindent | külön high-side switch IR ágra (0,5–0,7 A) | ✅ |
| B-26 | MEDIUM | Hő alulszámolva (~4,5–4,9 W csúcs zártan) | hőkeret ambient feltétellel; NTC (ADC2 GPIO49–53) | ✅ |
| B-27 | MEDIUM | Buck L/Cout tartomány | datasheet ellenőrzés | ⏳ |
| B-28 | LOW | Kondi DC-bias 9 V-on | effektív C megadása, 35–50 V MLCC | ✅ |
| B-29 | LOW | Header IR áramlépcső | lokális 10 µF + 100 nF | ✅ |
| B-30 | LOW | PDM vs 20 kHz PWM alias | LEDC ≥40 kHz | ✅ |

### R2-A: Javítás-ellenőrzés + belső ellentmondások (Haiku) — 38 tétel
Státusz-korrekció: P-1, P-4, P-5 → ⏳ (külső adat: kamera minta, Waveshare footprint).

| # | Súly | Megállapítás | Javítás (koordinátor döntés) | St. |
|---|---|---|---|---|
| A-3 | HIGH | E-26: CAM_IO0 lehúzás aktív-high PWDN-nél = kamera BE; nincs CAM_3V3 switch | CAM_3V3 load switch kötelező (= B-22) | ✅ |
| A-4 | MEDIUM | C6_IO9 10k felhúzás hiányzik | hozzáadni | ✅ |
| A-5/6 | MED/LOW | IR alkatrészek, PDM part neve hiányzik | megnevezni [NEM ELLENŐRZÖTT] | ✅ |
| A-7 | MEDIUM | Kamera I2C szint nem kapu | gate: kamera I/O szint ismerete előtt nincs felhúzás beültetve | ✅ |
| A-8 | HIGH | F-3 (min. 5 V/2 A) hiányzik | FULL/MID/LOW módtábla (= B-17) | ✅ |
| A-9 | MEDIUM | Strapping ellenőrzés nincs a bring-upban | §15/§16 lépés | ✅ |
| A-10..12 | MED/LOW | ICR [NEM ELL.] jelölés, TVS tok, VEML árnyékolás, FPC/header ESD, merevítő | pótolni | ✅ |
| A-13 | MEDIUM | "06-mechanika" hivatkozás nem létezik; IR szembiztonság PCB-függő | LED áram plafon PCB követelmény; hivatkozás → 06-floorplan | ✅ |
| A-14/15/17/18 | LOW | CAM_IO0 időzítés, EMC szekció, "nincs 2. bemenet", §19 lefedettség hiányos | pótolni | ✅ |
| A-19 | HIGH | **CSI: modul hátul, J2 elöl → via kell, de szabály tiltja** | **Döntés: szimmetrikus via-pár (P+N együtt), mellette 2 GND visszatérő via, párban max 1 rétegváltás; J2 marad elöl (FPC a résben)** | ✅ |
| A-20/21 | HIGH/MED | VBUS 5–12 V vs OVP vs DRV8837 | max 9 V (= B-11, B-16) | ✅ |
| A-22/23/24 | MEDIUM | CC-sense DNP / 1,5 A sor / LOW mód csúcs >0,5 A | CC-sense + PG kötelező; módtábla; LOW csúcs sor WiFi cap-pel | ✅ |
| A-25 | MEDIUM | TP8 FRONT-on elérhetetlen | IR áram shunt MAIN-re (IR high-side switch mellé, = B-25) | ✅ |
| A-26 | MEDIUM | C6 UART pad "RF mellett" vs "RF-től távol" | modul pad az RF mellett van; nyomvonal ellentétes rétegen, TP-k távol | ✅ |
| A-27 | MEDIUM | SD CD felhúzás fő sínre vs szabály | szabály csak adatvonalakra; CD nem-VO4 GPIO | ✅ |
| A-28 | MEDIUM | VDDPST_5 = VO4 a modulon? (Q1 maradék) | gate a sematik előtt | ⏳ |
| A-29 | MEDIUM | Strapping pinenkénti terhelés tábla | tábla datasheet ref-fel | ⏳ (a tábla megvan, az **adatlap-hivatkozás TODO**, 05 5.1 / Q21) |
| A-30 | MEDIUM | E4 "USB HS (48/49)" pad szám, nem GPIO | "P48/P49" jelölés | ✅ |
| A-31..33 | LOW | C6_IO8 ajánlott/kötelező; C6 JTAG; pad vs GPIO jelölés | egységesítés; **padok "P" előtaggal** | ✅ |
| A-34 | MEDIUM | Modul forgatás: pad 2 (RF) és P50/51 (USB) ellentétes oldalon | élhozzárendelés: u.FL és USB-C ellentétes élen | ✅ |
| A-35 | LOW | IR számok jelöletlenek | [NEM ELLENŐRZÖTT] | ✅ |
| A-36 | MEDIUM | K8: C6 OTA nem igazolt | bring-up kapu + fallback hatása | ✅ |
| A-37 | MEDIUM | ICR DNP → IR-cut extra v1-ben nem teljesül | Q: ICR-es lencsés kamera modul választás (kötelező szempont Q5-ben) | ✅ |
| A-38 | LOW | User gomb helye/felhúzás | hátoldal, belső felhúzás + 100 nF | ✅ |

## Review kör 3 (2026-10-09) — 05 v0.3-ra → v0.4, 06 v0.1 → v0.2

### R3-C: Konzisztencia-ellenőrzés (31 tétel)
| # | Megállapítás | Javítás (hol) | St. |
|---|---|---|---|
| C-1 | 06: USBLC6 még szerepel (05: 3,3 V ESD array) | 06 2.1 → TPD2E2U06 / PRTR5V0U2X osztály | ✅ |
| C-2 | 06: CC-sense 1k / BAT54S (05: 100k + 10 nF + Zener) | 06 2.2 PD blokk; CC-tap DNP rev A | ✅ |
| C-3 | 06: rés 6,0 mm (05: 7,0 mm); Z-összegek | 06 3. újraszámolva: 14,3 / 29,3 / 17,8 mm | ✅ |
| C-4 | Kamera alatti magasság-limit: G − 3,2 − 0,5 = 3,3 mm @7 mm | 06 2.2, 3.2; 05 3., 7., Q8 | ✅ |
| C-5 | TP8 helye: MAIN front, az IR kapcsoló mellett (nem a hátoldali pogo csoportban) | 05 4.2, 12; 06 2.2, 4.2, 4.4 | ✅ |
| C-6 | 06 költségvetés: IR high-side alkatrész + shunt hiányzik | 06 2.2 (IR ág sor) | ✅ |
| C-7 | 06 költségvetés: CAM_3V3 switch hiányzik | 06 2.2 | ✅ |
| C-8 | 06 költségvetés: supervisor hiányzik | 06 2.1 (DNP rev A) | ✅ |
| C-9 | 06 költségvetés: USER gomb hiányzik | 06 2.1 (3 tact) | ✅ |
| C-10 | 06 költségvetés: NTC hiányzik | 06 2.2 | ✅ |
| C-11 | 06 költségvetés: VBUS osztó (eFuse után, MAIN front) hiányzik | 06 2.2 | ✅ |
| C-12 | eFuse bulk 35–50 V MLCC (06: ≥25 V) | 06 2.2; 05 4.1 már így | ✅ |
| C-13 | PDM soros R ne legyen a MAIN hátoldalon | 06 2.1 törölve; FRONT hátoldal (2.4) | ✅ |
| C-14 | Modul 3V3 bulk: egy érték mindkét doksiban | 47 µF + 10 µF + 100 nF (05 4.1 fa, 06 2.1) | ✅ |
| C-15 | TP-szám: TP1–TP17 mindkét doksiban | 05 12; 06 2.1 pogo csoport (TP8 nélkül) | ✅ |
| C-16 | FFC hossz szöveg → 25–30 mm | 06 0, 3.3, K1 | ✅ |
| C-17 | Lencse-kivágás indoklás: tengelyhez igazított 14×14 átfér 16×16-ban | 06 2.3, K9; 05 3. | ✅ |
| C-18 | 05: GPIO2, 3, 4 sorok hiányoznak | 05 5 (P17–P19, szabad) | ✅ |
| C-19 | GPIO0/1: egy funkció (VEML INT csak ha J5 kap pint; 32k XTAL opció) | 05 5 | ✅ |
| C-20 | GPIO45 NC, de az sdkconfig felülírja az IDF default SD power-reset pinjét + bring-up ellenőrzés | 05 5, 15/4 | ✅ |
| C-21 | Pad-eredet jelölése (E20, primer forrás) | 05 E20, banner, 5, 14 | ✅ |
| C-22 | GPIO23 pull = TBD (Q5) | 05 5 | ⏳ Q5 / G3 |
| C-23 | Téves "~5 % CC-tap terhelés" állítás törlése | 05 4.1 CC-tap sor | ✅ |
| C-24 | Tápmódonkénti minimum forrás | 05 4.3 mód-tábla | ✅ |
| C-25 | Hivatkozás-előtagok: "00-K8" / "06-K8" | 05 D8, 9, 15, Q16; 06 elején | ✅ |
| C-26 | C6_IO8 felhúzás kötelező mindenhol | 05 E6, 5, 10; 02 megjegyzés | ✅ |
| C-27 | VEML shielding megjegyzés | 05 D7; 06 2.3 | ✅ |
| C-28 | 00: mikrofon szöveg → PDM | 00 extra funkciók | ✅ |
| C-29 | Egy USB-megnevezés: USB-Serial-JTAG (GPIO 24/25) | 05 E4, 5, 13 | ✅ |
| C-30 | Megerősítendő: az OTG FS nincs használatban | 05 Q23 | ⏳ G0 sdkconfig |
| C-31 | 1,0 mm CPWG számok a 0,8 mm sorokból származtatva → field solver | 05 13 (CSI, RF) | ✅ |

### R3-K: "Prototípus-gyilkos" review (22 tétel)
| # | Megállapítás | Koordinátori döntés / javítás (hol) | St. |
|---|---|---|---|
| K-1 | **BLOCKER** Nincs független tápút (eFuse / CH224K hiba = minden áll) | DNP VBUS→VBUS_SW híd, 2× 5,1k Rd (csak CH224K nélkül), TP4 3V3 bench betáp, selyem "NEVER BOTH" (05 0.1, 4.1) | ✅ |
| K-2 | **BLOCKER** A firmware-lánc még soha nem futott | **G0**: dev-kit stream OV5640 → ISP → H.264 → RTSP esp-hosted C6 WiFi-n, 24 h soak, áram állapotonként, sdkconfig + verziók befagyasztása (05 0.2) | ⏳ gate |
| K-3 | TPS22810-nek nincs állítható ILIM-je [NEM ELLENŐRZÖTT] | 2. állítható-ILIM eFuse (≥18 V) az IR ágra, vagy rev A: biztosított 0 Ω (05 D9, 4.1, 4.2) | ✅ típus ⏳ G4 |
| K-4 | Téves mondat: "20 V esetben eFuse OVP véd" – a TVS az eFuse előtt van | javítva (05 4.1); G1 CH224K breakout bench teszt | ✅ szöveg ⏳ G1 |
| K-5 | ICR tartalék | rev A bármely modul NoIR / fix lencsével, ICR blokk DNP; ICR rev B (05 D3, 4.2, 7) | ✅ |
| K-6 | RF: modul sematik routing előtt | G2: sematik elolvasása; a modul saját IPEX-e rev A-ban, ha elérhető; u.FL / π / CPWG 0 Ω-DNP; 2 antenna; RSSI dev kit-en (05 3, 0.2) | ⏳ G2 |
| K-7 | Hivatalos bring-up konfiguráció | MAIN önállóan, szabványos 50–100 mm FFC; stack zárása stabil kép után (05 0, 15) | ✅ |
| K-8 | BOM-kapu a sematik előtt | **07-bom-terv.md** váz + értékszámítási lap; G4 (05 0.2) | ✅ váz ⏳ G4 |
| K-9 | Beszerzési lista | 05 0.3 | ✅ lista ⏳ beszerzés |
| K-10 | Modul-forrasztási módszer | páka + fluxus, külső pad ≥1,5 mm, maszk / keep-out a modul alatt, USB-C távolság ↑ (05 3.1; 06 2.1, K8) | ✅ |
| K-11 | 06 elavult a 05 v0.3-hoz képest (USBLC6, BAT54S, 6 mm rés, hiányzó switch-ek) | 06 v0.2 újragenerálva | ✅ |
| K-12 | Lapméret | 45×45 marad; nyitott kérdés: rev A MAIN nagyobb (pl. 60×50), azonos M2 raszter + J2/J5 koordináták (05 Q22; 06-K15) | 👤 |
| K-13 | Rendelési sorrend | MAIN először, FRONT később (G6) (05 0, 3) | ✅ |
| K-14 | Supervisor | nyílt-drain változat, 0 Ω az ESP_EN-be, DNP rev A (05 5) | ✅ |
| K-15 | Rev A mód-logika | boot LOW → FULL ha VBUS_SW ≥8 V settle után; CC-tap DNP (05 4.3 / 6. szabály) | ✅ |
| K-16 | SD blokk | DNP rev A, footprint marad (05 0.1, 5, 6) | ✅ |
| K-17 | C6 + UART0 header | DNP 2,54 / 1,27 mm footprint, hátoldali él, P2-től távol (05 6 J7; 06 2.1) | ✅ |
| K-18 | EDA / folyamat szekció | 05 3.1: EDA TBD, JLC 2 rétegű 1,0 mm DRC, nincs impedancia-kontroll (±10–20 %), USB-C THT kérdés | ✅ 👤 EDA eszköz |
| K-19 | IR teszthez árnyékoló cső / ablak-távtartó | 05 4.2, 15/9, 0.3 | ✅ |
| K-20 | USB-C 16 pin pin map | 07 §3 (A6/B6, A7/B7 összekötve; SBU NC; CC1/CC2 → CH224K) | ✅ |
| K-21 | GPIO tábla TBD padjai kitölthetők a Waveshare pinoutból | E20 pad-térkép, minden pad kitöltve | ✅ |
| K-22 | Kamera switch CT / slew érték | 07 §4; inrush mérés a bring-up 7. lépésben | ✅ keret ⏳ G4 érték |

### Összesítés kör 3
- Új tartalmi kapuk: G0–G6 (05 0.2). Az **új ⏳ tételek**: C-22, C-30, K-2 (G0), K-3 típus (G4), K-4 (G1), K-6 (G2), K-8 (G4), K-9 (beszerzés), K-22 érték (G4).
- 👤 tulajdonosi döntés: K-12 (rev A lapméret), K-18 (EDA eszköz), Q15 (beltéri v1).
- Új, a körön kívüli megállapítás (E20 beépítésekor): **CSI pad-sorrend eltér a J2-től** (05 6, 06-K14) → ⏳ G2/G3.

## Review kör 4 – diagram visszaellenőrzés (2026-10-09) — 05 v0.4 → v0.5, 06 v0.2 → v0.3, 07 v0.1 → v0.2, 08 v0.1 → v0.2

Forrás: a `08-diagramok.md` hibalistája (1–23) fordított ellenőrzése. A fordított ellenőrzés az 1–8., 10–17., 19–22. tételt visszaigazolta; #9 részben (07 #38 már FIT volt), #23 részben (csak Q26 hiányzott), #18 téves volt.

| # | Tétel | Javítás (hol) | St. |
|---|---|---|---|
| R4-1 | TP8 FIT vs DNP | 05 §0.1, §12; 07 #33 | ✅ |
| R4-2 | TP4–TP6 oldala | pad-ok hátul, 0 Ω elöl (05 §12; 06 §2.1, §2.2, §4.2) | ✅ |
| R4-3 | TP9 / TP16 szétbontás, pad-szám | 18 pad (17 jel + TP3 GND) + 2 GND = 20 (05 §12; 06 §2.1) | ✅ |
| R4-4 | "GPIO 54 / C6_EN (P82)" felirat + Q2 | 05 §5, §6, §10, §12; 07 #32; 08 | ✅ felirat ⏳ Q2 (G2) |
| R4-5 | CH224K VDD ← nyers VBUS | 05 §4.1 | ✅ |
| R4-6 | NTC, VEML7700 a 3V3 listán | 05 §4.1 | ✅ |
| R4-7 | Státusz LED a MAIN hátoldalon (GPIO 6), J5.17 NC, "LED-ek" pontosítva | 05 §0.1, §4.1, §5, §6; 06 §2.1, §2.3; 07 #30 | ✅ |
| R4-8 | 100k lehúzások a MAIN hátoldalon | 05 §4.2, §5; 06 §2.1, §2.4; 07 #54 | ✅ |
| R4-9 | J2 ESD a §0.1-ben és a front költségvetésben | 05 §0.1; 06 §2.2 | ✅ (07 #38 már FIT volt) |
| R4-10 | §0.1 kiegészítés (VO4, strap, I2C, ESD, shield RC, Rd) | 05 §0.1 | ✅ |
| R4-11 | IR ág rev A = DNP, "biztosított 0 Ω" javítva | 05 D9, §0.1, §4.1, §4.2 | ✅ |
| R4-12 | CC ADC kikerült a rev A boot-sorrendből | 05 §4.3, §15 | ✅ |
| R4-13 | J7 = 1×9 | 05 §6; 07 #32 | ✅ |
| R4-14 | 07 passzív-csoportok | 07 #53–#60 | ✅ |
| R4-15 | CSI keresztezés vs 1 rétegváltás | 05 §13 kivétel-javaslat [NEM ELLENŐRZÖTT] | ✅ szabály ⏳ Q24 (G3) |
| R4-16 | G2–G3 körkörösség | CSI/J2 döntés a G3-ban (05 §0.2, §6, §14, Q24; 06 K12/K14) | ✅ |
| R4-17 | G5b kapu | 05 §0.2 | ✅ |
| R4-18 | J5 GND-szomszédság | a szabály teljesül | ❌ téves |
| R4-19 | J3, J4, J6, J7 pin-táblák | 05 §6 | ✅ |
| R4-20 | Nem használt padok (P6–P8, P11–P14, P34–P39, GND padok) | 05 §5 | ✅ |
| R4-21 | TVS + ESD a hátoldalon, VBUS ≥2 via a front eFuse-hoz | 05 §3, §4.1 | ✅ |
| R4-22 | 06-K5 számtan (242 vs 295) | 06 K5 | ✅ |
| R4-23 | §0.4: Q26 felvéve, Q15 👤 | 05 §0.4, §17 | ✅ (részben téves) |
| R4-D | Diagram-hibák: D1 TPC6 szétbontva (J7 DNP), CSI él Q24; D2 SDB/TP6 szétbontva, IR_SW_EN DNP, LED-ek → státusz LED; hiányzó elemek (Rd, shield RC, I2C felhúzás) | 08 v0.2 | ✅ |
| R4-E | 06 költségvetés újraszámolva: hátoldal 429,2 → 558 mm² (50 %), front 819 → 1065 mm² (56 %), FRONT elöl 95,7 (8 %), FRONT hátul 315 → 410 mm² (32 %) | 06 §2 | ✅ |
| R4-F | 07 BOM-sorok (shield RC, lehúzások, UART0 R, GPIO 5, CH224K kondik, CAM_3V3 0 Ω, FB, eFuse R-ek) | 07 #53–#60 | ✅ (értékek ⏳ G4) |

Nyitva maradt: Q2 (C6_EN a modulon), Q24 (CSI sorrend, G3), 07 MPN / értékek (G4), a pogo-pad pontos szám a layoutban (20 pad: 17 jel + TP3 GND + 2 GND).

## Tulajdonosi döntések (2026-10-09, kör 4 után)
| Tétel | Döntés | Érintett |
|---|---|---|
| Q22 / K-12 / 06-K15 | **Rev A MAIN 60×50 mm**, FRONT 45×45; közös M2 raszter + J2/J5 koordináta; végcél 45×45 | 05 0, D6, 3; 06 |
| Q26 | **EDA: KiCad** (USB-C THT shell beültetés még nyitott) | 05 3.1, Q26; 07 |

## Táp lap bekötés (2026-10-09)
| Tétel | Eredmény |
|---|---|
| CH224K | LCSC-n **Discontinued** → tulajdonosi döntés: **CH224A** (C42459160); a CH224D-ről kiderült, hogy nincs I2C-je (korábbi koordinátori tévedés javítva) |
| B-4 (PD feszültség kiolvasás) | ✅ megoldva: CH224A I2C 0x22/0x23 (reg 0x09, 0x50) |
| Q13 (eFuse típus) | ✅ TPS259470ARPW, értékek E22-ben; RPW0010A footprint a TI land patternből (`kicad/lib`) |
| Q18 (buck) | ✅ TPS62933F, értékek E22-ben |
| `01_tap.kicad_sch` | 35 alkatrész, ERC 0 hiba a lapon; R4/R5 DNP; JP1 nyitott bypass |
| MCP eszköz-hiba | `batch_add_and_connect` 38 alkatrésszel időtúllépés → **0 bájtos lapfájl**; visszaállítva, ≤8 alkatrész/hívás |

## P4 modul lap bekötés (2026-10-09)
| Tétel | Eredmény |
|---|---|
| `02_p4_modul.kicad_sch` | U1 88/88 láb kezelve (57 globális címke + 31 NC); 33 passzív: 3V3 hidegítés (47 µF + 10 µF + 2×100 nF), VO4 1 µF, GPIO36/C6_IO9/C6_IO8 10k felhúzás, 100k lehúzások (IR_PWM, ICR_IN1/2, SD_EN, CAM_3V3_EN; IR_SW_EN DNP), státusz LED + 1k, NTC 10k osztó, u.FL + π (0R soros, 2× DNP sönt), I2C felhúzás 4,7k DNP, ESP_EN RC DNP (Q3), CC ADC leágazás DNP |
| Új hozzárendelés | **GPIO2 (P17) = EFUSE_FLT** – a táp lapon nem volt GPIO-ja (05 §5 frissítve) |
| ERC | 0 hiba; 23 warning = a még meg nem rajzolt lapok (kamera, prog/TP, SD, B2B) címkéi |

## Programozás / gombok / TP lap (2026-10-09)
| Tétel | Eredmény |
|---|---|
| `04_prog_tp.kicad_sch` | SW1 BOOT (GPIO35→GND), SW2 RESET (ESP_EN→GND), SW3 USER (GPIO5→GND, +100 nF C40); R40/R41 1k UART0 soros (U0TXD/RXD → _TP); J7 1×9 1,27 mm (GND, C6_TXD, C6_RXD, C6_IO9, C6_IO8, C6_EN, U0TXD_TP, U0RXD_TP, +3V3) **DNP**; 20 pogo pad Ø1,5: TP1–TP7, TP9A/B, TP10–TP15, TP16A/B, TP17, TP18/TP19 GND |
| Supervisor (K-14) | **nem rajzolva rev A-ban** (DNP; nincs ellenőrzött KiCad szimbólum / lábkiosztás) – TODO szöveg a lapon |
| ERC | 0 hiba; 18 warning = kamera / SD / B2B lap címkéi |

## Kamera lap (2026-10-09)
| Tétel | Eredmény |
|---|---|
| `03_kamera.kicad_sch` | J2 15p 1,0 mm FPC (RPi kiosztás, MP→GND, pin 12 NC); U6 **TPS22917DBV** CAM_3V3 kapcsoló (EN = CAM_3V3_EN, CT 1 nF, QOD → R53 0R → VOUT); R50 0R mérő-jumper → CAM_3V3 (TP5); C50/C51 1 µF; CAM_PWDN: R51 lehúzás / R52 felhúzás **mindkettő DNP** (Q5: csak az egyik ültethető) |
| TPS22918 → TPS22917 | ugyanaz az osztály; a TPS22917 lábkiosztása a KiCad könyvtárból ellenőrzött, a TI oldal cookie-ablaka miatt a TPS22918 adatlapot nem olvastam |
| Nyitott (lapon TODO szöveg) | Q24 CSI sorrend, Q5 PWDN polaritás, Q6 FPC érintkezőoldal (a TE 1-84953-5 footprint helykitöltő), I2C felhúzás DNP, 07 #38 vezérlőjel-ESD még nincs rajzolva |
| MCP eszköz-hiba | `batch_connect replace=true` nem törölte a régi globális címkét a U6 pin 5-ön → kézzel törölve |
| ERC | 0 hiba; 10 warning = SD és B2B lap címkéi |

## B2B J5 + IR ág és microSD lap (2026-10-09) – MAIN sematik első teljes változat
| Tétel | Eredmény |
|---|---|
| `05_b2b_front.kicad_sch` | J5 2×10 1,27 mm (05 §6 kiosztás; J5.17 NC), R70 47 Ω PDM_CLK soros a forrásnál (FIT). **IR ág DNP**: U7 TPS259470ARPW (EN = IR_SW_EN, OVLO → GND, RILM 6,65k = 0,5 A, CdVdt 1 nF), R72 0,1 Ω shunt + TP8A/B, R73 0R bypass, C71 10 µF → IR_VIN (J5.1/2) |
| `06_sd.kicad_sch` | **teljes lap DNP**: J3 Hirose DM3AT (DET_A → SD_CD, DET_B → GND), U8 TPS22917DBV (SD_EN), 5× 10k felhúzás SD_3V3-ra, CD 10k a fő 3V3-ra, 10 µF + 100 nF; TODO: SD ESD (E-30) |
| K-3 (IR eFuse típus) | ✅ TPS259470A, 0,5 A ILIM (a TPS22810-nek nincs állítható ILIM-je) |
| **Teljes MAIN sematik** | 6 lap, **131 alkatrész (92 FIT / 39 DNP), 122 net, ERC 0 hiba / 0 warning** |
| Nyitott (sematikon TODO) | Q24 CSI sorrend, Q5 PWDN, Q6 FPC oldal, Q2 C6_EN, Q3 EN RC, I2C felhúzás szint, vezérlőjel- és SD-ESD, supervisor (rev B), L1 / CH224A EP / TPD2E2U06 lábkiosztás ellenőrzés, B2B 7 mm típus (Q17) |

## MAIN NYÁK elhelyezés (2026-10-09)
| Tétel | Eredmény |
|---|---|
| Netlista → NYÁK | `kicad/MAIN/scripts/place.py` (pcbnew; az MCP nem oldja fel a `${KIPRJMOD}` könyvtárat): 131 footprint + 4 M2 furat, 123 net, DNP attribútum + BOM/pos kizárás a DNP-kre |
| Elhelyezés | hátoldal: U1 (22,5;25), J1 USB-C jobb él y=20 (270°, száj a lapszélen), D1/U5, SW1/SW2 fent, SW3 + J7 lent, pogo TP 4×5 / 2,6 mm (x 46,5–54,3, y 29,6–40), lehúzás-oszlop x=40,5, 3V3 hidegítés a P84–86 alatt, RF/u.FL a P2-nél. Előlap: táplánc a többlet-sávban (CH224A fent, eFuse a J1 furatai között, VBUS-monitor, buck + L1 lent), J2 a két M2 furat között a felső élen, J5 x=40,5, J3 (DNP) bal él, U6 csoport bal-fent, SD és IR (DNP) lent |
| DRC | **0 courtyard / clearance / short hiba**; maradt: felirat (silk) átfedések, 4 furat lib-eltérés (kozmetikai); 317 bekötetlen = huzalozás hiányzik |
| Képek | `docs/img/main_revA_front_placement.png`, `docs/img/main_revA_back_placement.png` |
| Nyitott | J2 iránya (rev A: kábel a lapszél felé – bring-uphoz jó; stack-változat G3), felirat-rendezés, huzalozás (CSI, RF, USB, táp) |

## CSI huzalozás (2026-10-09)
| Tétel | Eredmény |
|---|---|
| Szkript | `kicad/MAIN/scripts/route_csi.py` (idempotens: törli és újrarajzolja a CSI rezet) |
| Topológia | D0 + CLK: hátoldali sávok a modul fölött (y 3,6–7,5) → via-pár a J2 teste alatt → előlapi csonk felülről a J2 padba. D1: jobb oldali padok → via (x 37,0 / 37,7) → előlapi sáv a J2 alatt (y 10,9 / 11,45) → alulról a J2 padba. Jelenként **pontosan 1 rétegváltás** (05 §13) |
| **Q24 megoldva layoutban** | D0 és D1 sorrendje a fordulók miatt helyes; **CLK P/N csere a rétegváltásnál** (eltérő x-ű viák), keresztezés nélkül; a CLK × D1 keresztezés rétegek között (D1 előlap, CLK hátoldal) |
| Hosszak | D0 11,72/11,72, CLK 24,72/24,72, D1 20,32/20,32 mm → **párokon belül 0,0 mm** (D0N U-meander +3,8, CLKP bump +1,8, D1N jog +0,6). Párok között max. ~13 mm (≈85 ps ≈ 0,07 UI @ 800 Mbps) [NEM ELLENŐRZÖTT tűrés] |
| Geometria | 0,3 mm nyom, via 0,6/0,3; a párokon belüli csatolás laza (0,6–0,7 mm rés) → inkább egyvégű ~50–60 Ω viselkedés GND öntéssel; **GND öntés + visszatérő GND viák a via-párok mellé még hátravan**; field solver ellenőrzés TODO |
| DRC | 0 hiba, 0 CSI bekötetlen |
| Kép | `docs/img/main_revA_csi_routing.png` |

## RF huzalozás (2026-10-09)
| Tétel | Eredmény |
|---|---|
| Szkript | `kicad/MAIN/scripts/route_rf.py` (idempotens; a forgatást a valós pad-geometria alapján választja, a hátoldali tükrözés miatt) |
| Topológia | hátoldal, egyenes 0,7 mm vonal y = 34,5: **P2 (LNA_OUT) → C27 sönt (DNP) → R34 0R soros → C28 sönt (DNP)** → egy 90°-os forduló le → **J4 u.FL** (270°, középső láb felfelé; a nyom nem megy a u.FL teste alatt) |
| Javítás | 1. elhelyezés: R34 fordítva (tükrözés), J4 GND láb a vonalban, 0402-esek courtyard-ütközése (3,97 mm kellett 3,47 mm helyen) → átrendezve |
| Hossz | ~5 mm + 1,8 mm ≪ λ/10 (~7 mm FR4-ben 2,4 GHz-en [NEM ELLENŐRZÖTT becslés]) |
| DRC | 0 hiba (1 kozmetikai: J4 felirat a lapszélen) |
| Hátravan | GND öntés + via-kerítés (≤2 mm) a vonal két oldalán, a sönt- és u.FL-GND padok bekötése; 0,7 mm / rés field solverrel; G2: a modul saját IPEX-útja (K-6) |
| Kép | `docs/img/main_revA_rf_routing.png` |

## USB D+/D− huzalozás (2026-10-09)
| Tétel | Eredmény |
|---|---|
| Szkript | `kicad/MAIN/scripts/route_usb.py` (idempotens; U5 elhelyezése pad-geometria alapján) |
| Topológia | hátoldal, 0,25 mm, **adaton nincs via**: P50 DM / P51 DP → **U5 ESD a nyomon** (IO padok a vonalakon, x 45,5) → J1. DM: fővonal → B7, A7 → L-csonk a padok előtt (x 50,1). DP: fővonal → B6, **A6↔B6 a padok mögött** (x 52,6, a csatlakozótest alatt, 0,3 mm az A7-től). U5 GND → csonk + GND via (46,5; 20,0) a két vonal között |
| Javítások | 1. GND via az előlapi R9 padján → áthelyezve; a törlési feltétel zárójelezési hibája miatt ottmaradt csonk → dobozszűrős takarítás |
| DRC | 0 hiba; 1 „lógó via” (GND, megszűnik az öntéssel); TP9A/TP9B még bekötetlen (a pogo mezőben, általános huzalozásnál) |
| Kép | `docs/img/main_revA_usb_routing.png` |

## MAIN rev A – táp huzalozás (2026-10-09)
| Tétel | Állapot |
|---|---|
| Szkript | `kicad/MAIN/scripts/route_pwr.py` (idempotens; törli a táp netek + GND rézét, kivéve az USB ESD GND csonkot) |
| Netclass | `.kicad_pro` netclass_patterns pótolva (eddig üres volt): PWR = VBUS, VBUS_SW, 3V3_BUCK, BK_SW, +3V3, IR_VIN(_SH), CAM_3V3(_SW), SD_3V3; CSI_*, USB_D*, RF* |
| VBUS | J1 A4/B9 (B) → D1 TVS → 2× via (46.6, 17.2/18.2) → F trunk y 14.35 → C3 → U3.5 (0.28 mm nyak, 0.2 mm pad-rés). A9/B4: B → via (49.3, 23.4) → F az R-oszlop nyugati oldalán. JP1.1, C2 (VHV), U2.8, U2.1 (VHV, B ugrás az SW1/SW2 rés alatt) |
| VBUS_SW | U3.6 alul → C6 → y 27.3 → C5 → x 45.2 oszlop → C8/C9 → U4.3. JP1.2 → B x 58.8 oszlop. IR eFuse: B a MH4 felett (y 39.55) → via → U7.5. R73.1 (DNP bypass) vékony F ág |
| Buck | BK_SW U4.5 → L1.1; 3V3_BUCK L1.2 → C12 → R16.1, C13; FB sense L1.2 → R14.1 (0.25) |
| +3V3 | R16.2 → 2× via (42.6, 43.6/44.6) → B y 44.06 (MH4 alatt) → C20/C21 → modul P84–86 (y 38.9 összekötő) → C22/C23 |
| IR_VIN | C71 → F diagonál → J5 oszlopai között x 40.5 → J5.1/J5.2 belső vég; TP8B/R72.2 a peremen (y 49.2). IR_VIN_SH: U7.6 → R72.1/TP8A, R73.2 B ugrással |
| Elhelyezés-módosítás | R16 → (44.0, 42.5) rot 270; R11 rot 180 (FLT jobbra); R3 ↔ C2 csere (PG/CFG1/VHV keresztezés nélkül) |
| GND | via-k: C5, C6, C8, C9, C12, C13, C3/R10, R15/C10, U2 EP; U4 GND1→C8, GND4→via |
| DRC | 0 hiba; 13 via_dangling (GND + R11 +3V3 via) → öntés / általános huzalozás oldja |
| Nyitott (általános huzalozás) | +3V3 ágak: U6 (CAM kapcsoló), U8 (SD kapcsoló), C61, J5.10/11, J7.9, felhúzók (R3, R11, R20–23, R31–33, R66), TP4; TP1/TP2; BK_BST (C11), BK_FB/BK_SS, eFuse vezérlő netek, CC1/CC2, PD_PG, I2C |
| Kép | `docs/img/main_revA_power_routing.png` |

## MAIN rev A – általános huzalozás, Freerouting (2026-10-09)
| Tétel | Állapot |
|---|---|
| Eszköz | Freerouting 2.4.1 (`~/.kicad-mcp/freerouting.jar`, GitHub release, 64 076 787 B), Java 27 |
| Előkészítés | `kicad/MAIN/scripts/autoroute_prep.py`: minden meglévő réz zárolva (DSN `type fix`), `RF_F_KEEPOUT` szabályterület F.Cu (1,0–8,9 × 33,2–37,6) az RF CPWG alatt, GND kivéve a DSN netlistából (GND = öntés + varrás) |
| Futások | 1. kör: 60 menet, 834 új szegmens; 2. kör (rögzített 1. kör + újrafuttatás): +55 szegmens |
| Eredmény | 1098 track/via, 113 via; **28 nem-GND bekötés hiányzik**, 104 GND (öntés oldja) |
| DRC | 1 hiba: `solder_mask_bridge` BOOT nyom ↔ MH2 NPTH (37,6; 12,2); 12 via_dangling (GND) |
| Hiányzó (28) | VBUS_MON, BK_SW→C11, SD_3V3 (2), +3V3 J5.10↔11, CAM_3V3→TP5, CAM_3V3_SW, CC2, CC2_ADC, PD_PG, NTC_ADC, SD_EN, SD_CD, SD_D3, PDM_DATA, ESP_EN (2), BOOT→TP16B, USB_DP/DM→TP9A/B, C6_TXD (2), C6_IO9 (2), C6_EN, U0RXD_TP, USER_BTN, USB_SHIELD |
| Megfigyelés | 38 B.Cu szegmens a modul alatt (padgyűrűn belül). DXF szerint nincs középső pad → maszkkal OK, de **via-k tentelve** kellenek; G3-on a modul alja ellenőrizendő. Szűk keresztmetszet: B jobb oldali pogo/TP rács + J7 sarok, ide fut sok hosszú, táblán átívelő net (C6_*, ESP_EN, BOOT, USER_BTN) |
| Kép | `docs/img/main_revA_autoroute.png` |

## MAIN rev A – TP ritkítás, GPIO-csere v0.6, J7 áthelyezés, huzalozás v2 (2026-10-09)
| Tétel | Állapot |
|---|---|
| TP ritkítás (tulajdonosi döntés: 1. opció) | törölve: TP9A/B (USB), TP10, TP11, TP12, TP13 (C6 – a J7 duplikálja), TP14, TP15 (UART0 – J7 duplikálja). Maradt: TP1–TP7, TP16A/B, TP17–TP19 + TP8A/B (IR). ERC 0 |
| GPIO-csere v0.6 (tulajdonosi döntés) | SD_EN 29→53 (P81), SD_CD 30→52 (P80), CAM_3V3_EN 33→4 (P19), USER_BTN 5→33 (P60), EFUSE_FLT 2→29 (P56), PDM_DATA 13→30 (P57); felszabadult: GPIO 2, 5, 13. ADC-k változatlanok. `05` §5, §0.1, §6, J3; `06`, `07` frissítve. **`08-diagramok.md` még a régi kiosztást mutatja → újragenerálás + visszaellenőrzés kell** |
| J7 | bal-felső lapszél, függőleges (x 2,0; pin1 y 11,2 → pin9 y 1,04), a C6 padok fölött, RF-től távol |
| R27 / R28 | 100k lehúzások az előlapra az U8 / U6 mellé |
| Netclass | új `PWR_LIGHT` (0,3 mm): +3V3, SD_3V3, CAM_3V3, CAM_3V3_SW (az autorouter ne 0,6 mm-rel húzza a mellékágakat); kézi táp-gerincek változatlanok |
| Eszközök | `scripts/autoroute_prep.py` (zárolás, RF + MH keepout r1,75, TP törlés, DSN GND nélkül), `scripts/gpio_swap_pcb.py`, `scripts/maze/` (saját A* rácsos router 0,05 mm, 2 réteg + rip-up driver; DRC-tiszta eredmény). Freerouting 2.4.1: >25 menetnél üres SES-t ír → `-mp 25` |
| Eredmény | 1286 track, 142 via; DRC **0 hiba**; nem-GND hiányzó: **6** (LED_STAT_A, CAM_3V3_EN, I2C_SDA, C6_IO8 – bal-felső sarok; SD_QOD az U8-nál; +3V3 J5.10↔J5.11) |
| Kép | `docs/img/main_revA_autoroute.png` |

## MAIN rev A – huzalozás befejezve (nem-GND) (2026-10-09)
| Tétel | Állapot |
|---|---|
| Eredmény | **minden nem-GND bekötés kész**; DRC 0 hiba; sematik-paritás: nincs net-eltérés; 1564 track, 159 via; csak a 104 GND bekötés (öntés) + 12 GND via_dangling marad |
| Elhelyezés-módosítás | R31/R32 (I2C felhúzás, DNP) → előlap (23,0; 12,5 / 14,2) a J2 mellé (+3V3 fal megszűnt a bal-felső sarokban); C60 ↔ C61 csere (U8 jobb oldali lábsorrend: SD_3V3 / QOD / CT – keresztezés nélkül); **TP5 (CAM_3V3) → hátoldal (11,6; 9,0)**, a CAM_3V3 forrás közelébe – a pogo-csoportból kikerült (rögzítő tervnél figyelembe venni) |
| Módszer | régiós rip-up + Freerouting (`-mp ≤ 25`) + saját A* router a maradékra (`scripts/maze/`: `kgeom.py`, `maze.py`, `ripup.py`, `cleanup.py` (DRC-UUID alapú csonk-takarítás), `region_reroute.sh` (best-of-N, csak javulásnál ír felül)) |
| Minőségi teendők (G-review) | (1) néhány hosszú kerülő vékony (0,2 mm) nyom: +3V3 ágak J5.10/11 (~67–86 mm), CAM_3V3 → TP5 (~47 mm) – kis áram, de rövidíthető kézi push-and-shove-val; (2) sok B.Cu nyom a modul alatt (padgyűrűn belül) → via-tenting kötelező, a modul alját G3-on ellenőrizni; (3) a B.Cu GND-öntést a modul alatti nyomok feldarabolják → varró via-k sűrítése szükséges; (4) `08-diagramok.md` GPIO v0.6 frissítés |
| Kép | `docs/img/main_revA_routed.png` |

## MAIN rev A – GND öntés (2026-10-09)
| Tétel | Állapot |
|---|---|
| Zónák | `scripts/gnd_pour.py`: GND_F + GND_B a teljes táblán, 0,2 mm clearance, termikus pad (rés 0,3 / küllő 0,35), szigetek eltávolítva; `ESP32-P4-CAM-MAIN.kicad_dru`: `min_resolved_spokes 1` (sűrű kis passzívok) |
| Varró via-k | `scripts/maze/stitch.py`: RF kerítés 10 db (±1,05 mm a B.Cu RF vonaltól, ≤1 mm osztás), CSI visszatérő 4/6 via, 2 mm-es rács 232 db; `island_stitch.py` (raszteres GND-komponens elemzés → via ott, ahol a sziget a másik rétegen fő GND fölött van) + `gnd_fix.sh` (rip-up + GND link). Összesen 283 GND via |
| RF_F_KEEPOUT | most csak nyomot tilt, via-t enged (GND kerítés) |
| Állapot | DRC **0 hiba**; nyitott: **9 jel** (CC1, IR_ILM, PDM_CLK_J5, SD_D0, SD_D1, EFUSE_FLT, U0TXD_TP, C6_EN, LED_STAT) + **2 GND zóna-sziget**. A GND sziget-javítás rip-upjai jeleket bontottak, a visszahúzás nem konvergál teljesen (Freerouting ~10–14 nyitott, saját router a maradékból 3–5-öt köt) |
| Javaslat | a maradék 9+2 kézi befejezése a KiCad interaktív routerével (push-and-shove), utána `gnd_pour.py fill` + DRC; vagy elhelyezés-lazítás (SD blokk / J3 környéke a legsűrűbb) |
| Kép | `docs/img/main_revA_pour.png` |
| Javított hibák | `region_reroute.sh` csak javulásnál ír felül + a starved_thermal nem számít hibának; maze: via lapszél-távolság 0,85 mm (korábban 0,65 → copper_edge hiba); bash 3.2 kompatibilitás (`gnd_fix.sh`) |

## MAIN rev A – SD-blokk lazítás + GND/jel befejezési kísérlet (2026-10-09)
| Tétel | Állapot |
|---|---|
| SD lazítás (tulajdonosi döntés) | SD felhúzások a J3 lábai mellé, két oszlopban: R62 (D1) / R65 (CMD) / R63 (D2) x 19,4; R61 (D0) / C63 / R64 (D3) x 22,4 (udvar-ütközésmentes); a régi y≈40 hurok megszűnt |
| Via-in-pad hiba (saját router) | 21 via SMD padban (a maze rétegváltás a pad közepén + sziget-via a pad rezén) → **mind eltávolítva**, a router ezentúl semmilyen SMD padba nem tesz viát (`maze.py` V-maszk). Maradt: U2 EP 2 termikus via (szándékos) |
| Varró via-k | rács-via-k eltávolítva → jelek → újra-varrás (`stitch.py`), izolált (fő GND-t nem érő) via-k törlése (`island_stitch.py .useless`); 309 GND via |
| Eszközök | `scripts/maze/`: `guarded.sh` (útvonalanként DRC-őr, visszavon), `ripall.sh`, `finish.sh`, `errs.py`, `GRID_MARGIN` env (szoros lábkivezetés) |
| Állapot | DRC **0 hiba**, sematik-paritás tiszta, via-in-pad 0; nyitott: **6 jel** (CAM_QOD, CC1, LED_STAT, PDM_CLK_J5, PDM_DATA, U0TXD_TP) + **14 GND** (főleg J5 GND tüskék / R24–R29 hátoldali lehúzások, J1 A12, U1 P15, U7 GND, C24) |
| Értékelés | az automatikus rip-up/reroute itt stagnál (minden javítás máshol bont); a 2 rétegű 60×50 lap a modul alatti zónában és a J5 körül telített |
| Kép | `docs/img/main_revA_pour.png` |

## MAIN rev A – J5 környék átrendezés (2026-10-09)
| Tétel | Állapot |
|---|---|
| Lehúzások (tulajdonosi döntés, 2. opció) | R24 (IR_PWM), R25 (ICR_IN1), R26 (ICR_IN2), R29 (IR_SW_EN) a J5 alól (B) → **előlap, a modul alatt, x 31,5 / y 22,5–27,3** (GND láb a fő F-öntésbe). `05` §5 „lehúzások helye: MAIN hátoldal” → most MAIN előlap a modul alatt (K-7 továbbra is teljesül) |
| J5 GND | jobb oszlop GND tüskék (6, 12, 14, 18) rögzített F-csonk + via x 44,35 → B öntés; pin 4 a pin 6-hoz kötve (alatta USB D+ fut B-n). Eredmény: a J5 GND-ből csak a 15-ös tüske maradt nyitott |
| Állapot | DRC **0 hiba**, paritás tiszta, via-in-pad 0; nyitott **7 jel** (CC1, EFUSE_FLT ×2, LED_STAT, PDM_CLK_J5, PDM_DATA, VBUS_MON) + **~10 GND** (főleg zóna-töredék; konkrét padok: U1 P15, J5.15, U7.2) |
| Értékelés | a J5-átrendezés a GND-t javította, a jelek száma 6 → 7 (a régió-újrahúzás mást bontott). Az automatika itt platón van |
| Kép | `docs/img/main_revA_pour.png` |

## Döntés: MAIN 4 réteg, 45×45 mm (2026-10-09)
| Tétel | Állapot |
|---|---|
| Tulajdonosi döntés | „a cél egy kompakt kamera” → **4 réteg, 45×45 (A opció)**; K4 módosítva (`00`) |
| Rétegfelépítés | JLC04101H-3313A (böngészővel ellenőrizve, JLC impedance + kalkulátor): L1 jel / L2 GND / L3 táp+GND / L4 jel; 50 Ω 0,302 mm, CSI 100 Ω 0,204/0,203, USB 90 Ω 0,262/0,203 (`05` §3.2) |
| Helyigény | 2433 mm² courtyard / ~3800 mm² → ~64 % (`06`) |
| Archív | a 2 rétegű 60×50 állapot: `kicad/archive/MAIN_2L_60x50_2026-10-09/` (nem teljesen huzalozott: 7 jel + ~10 GND nyitott) |
| Következő | kisalkatrész-döntések (kapcsolóméret, J7), majd 45×45 elhelyezés 4 rétegen, kritikus jelek (CSI/RF/USB/táp) kézzel, maradék Freerouting |

## MAIN v0.6 – 45×45 / 4 réteg elhelyezés (2026-10-09)
| Tétel | Állapot |
|---|---|
| Alkatrészcsere (tulajdonosi döntés) | SW1–SW3 → **Omron B3U-1000P** (3,0×2,5 mm, LCSC C231329, raktáron, ~0,19 USD, gyári KiCad footprint; böngészővel ellenőrizve). Alternatíva: XKB TS-1088-AR02016 (4×3 mm, C720477, ~0,05 USD) – footprint-rajz kellene. J7 → `ESP32-P4-CAM:PadRow_1x09_P1.27mm_SMD` (saját, 9 SMD pad). ERC 0 |
| Floorplan (tulajdonosi döntés) | U1 modul x 20,5 (−2 mm); J1 USB-C hátoldal jobb él (40,8; 22,5); **J5 az előlap aljára, vízszintesen** (22,5; 40,2) – a FRONT ehhez igazodik |
| Szkriptek | `scripts/place45.py` (rézmentesítés, 4 réteg, 45×45 R1 kontúr, footprint-csere, blokk-elhelyezés), `scripts/legalize.py` (courtyard szétnyomó: fix nagy elemek, M2 keepout, J1 köpenyláb-keepout mindkét oldalon), pozíciók: `scripts/pos_v06_45x45.json` |
| Eredmény | DRC: **0 hiba**, courtyard-átfedés 0, sematik-paritás tiszta |
| Kép | `docs/img/main_v06_45x45_placement.png` |
| Következő | rétegtípusok (In1 = GND sík, In2 = táp/vegyes), netclass szélességek a 3313A szerint, kritikus huzalozás (CSI, RF, USB, táp) kézzel, maradék Freerouting (In1 kizárva), GND öntések |

## MAIN v0.6 – 4 rétegű huzalozás, 1. kör (2026-10-09)
| Tétel | Állapot |
|---|---|
| Beállítás | In1 = `LT_POWER` + `GND_In1` zóna → DSN `plane` (Freerouting a GND-t a síkra fan-outolja); In2 vegyes; netclass a 3313A szerint (CSI 0,204/0,203, USB 0,262/0,203, RF 0,302, PWR 0,4, PWR_LIGHT 0,3, Default 0,15); JLC 4 rétegű minimumok: nyom 0,09, furat 0,2, via 0,45 (böngészővel ellenőrizve) |
| ⚠ Projektfájl-felülírás | a `.kicad_pro` kétszer visszaíródott régi beállításokra (netclass-minták törlődtek) – valószínűleg a nyitott KiCad GUI / MCP szerver menti; javítás: `scripts/project_rules.py` (egyetlen forrás, minden DRC előtt újra alkalmazva) |
| Eszközök | `scripts/prep4.py`, a maze router 3 rétegre bővítve (F/B/In2, via csak ha mindhárom szabad), `gnd_fanout.sh` (GND pad/sziget → csonk + via az In1 síkra) |
| Eredmény | 1696 track, 191 via; DRC: 6 clearance (CSI via-k a Default 0,15-tel lerakva); **nyitott 11**: GND 6 (C51, U7 (DNP), C10, R7, J1 A12), VBUS 2, VBUS_SW 1, CC1 1, IR_VIN_SH 1 – mind a J1/U2/U3 táp-blokk környékén |
| ⚠ CSI minőség | autorouterrel: hossz-eltérés D0 **8,3 mm**, D1 2,6 mm, CLK 0,4 mm, nincs csatolt pár → **nem elfogadható**, kézi párhuzamos, hosszkiegyenlített CSI huzalozás kell (modul P41–P46 → J2) |
| Kép | `docs/img/main_v06_routing.png` (F / In2 / B) |

## MAIN v0.6 – CSI kézi huzalozás + 2. kör (2026-10-09)
| Tétel | Állapot |
|---|---|
| CSI (`scripts/route_csi4.py`) | modul P41–P46 (B) → 1 via/vezeték a modul-test alatt → **F.Cu (ref. In1 GND)** → J2 lábak alulról; „hagyma”: D0 belül (egyenesen fel, P/N csere a via-helyekkel), D1 középen (y 15,4/15,81), CLK kívül (y 16,6/17,01); szélesség 0,204, rés ~0,203 a csatolt szakaszokon; **hossz: D0 9,28 / D1 14,98 / CLK 21,12 mm, pár-skew 0,000** (serpentine a rövidebb lábon); zárolva |
| Folyosó-ürítés | R24, R25, R26, R29, D2, JP1, R9, R11 áthelyezve (5–11 mm) a CSI-folyosóból (F x 20,8–34,2 / y 9–18,4) |
| Befejező kör | `scripts/maze/finish4.sh` (Freerouting zárolt réz mellett → GND fan-out → őrzött maze), `ripall.sh`, `gnd_fanout.sh` |
| Állapot | DRC: 1 clearance; **nyitott 14**: GND 5 (C51, C10, U7×2 DNP), VBUS, VBUS_SW×2, VBUS_MON, CC1, +3V3, EF_ILM, IR_VIN_SH (DNP), I2C_SCL, ESP_EN – túlnyomórészt a táp-blokk (U2/U3/U4) körül |
| Kép | `docs/img/main_v06_routing.png` (F / In2 / B) |

## MAIN v0.6 – táp-blokk átrendezés + In2 táp-zónák (2026-10-10)
| Tétel | Állapot |
|---|---|
| Elhelyezés (`scripts/power_place.py` + `legalize.py ONLY`) | eFuse blokk jobb-felső (U3 + C3/C4/R6–R10), CH224A a J1 alatt (U2 + C2/R2/R3), buck egy tömbben a modul alatt (U4, L1, C5/C6, C8–C13, R14–R16), VBUS_MON osztó + NTC mellette; a legalizáló már a zárolt rezet (CSI) is akadálynak veszi; `scripts/freespot.py` |
| In2 táp-zónák | `PWR_VBUS_In2` (jobb sáv, 171 mm²) és `PWR_VBUSSW_In2` (buck-blokk + sáv az eFuse kimenetéig, 264 mm², a CSI B-csonkjai alatt nem) prioritás 2; `scripts/maze/zone_drop.py`: táp-padok rövid csonk + via a saját zónájukba (VBUS 14/14, VBUS_SW 6/11); `J1_BODY_NOVIA` szabályterület (fém köpeny alatt nincs via); NPTH lyuktávolság a routerben 0,3 |
| Állapot | DRC **0 hiba**; nyitott **16**: GND 4, VBUS_SW 2 (U3.6 kimenet, U7 DNP), CC1 2, PD_PG 2, PD_CFG1, EFUSE_FLT, NTC_ADC, PDM_CLK, IR_SW_EN (DNP ág), IR_VIN_SH (DNP) |
| Hátra | maradék 16 (kézi / interaktív router javasolt), F/B/In2 GND öntés + varrás, CSI via-k melletti GND via-k, végső DRC, `08` diagram-frissítés |
| Kép | `docs/img/main_v06_routing.png` |

## MAIN v0.6 – U2 (CH224A) környék lazítása + U3 kimenet (2026-10-10)
| Tétel | Állapot |
|---|---|
| U2 | 180°-kal forgatva, (40,75; 31,05); CC/CFG1/PG lábak a J1 felé; R2 (39,75; 35,55), R3 (37,3; 35,5), C2 (42,6; 36,4) |
| PD hálók | CC1 J1 A5 → kézi B-csonk + 0,5/0,25 via (35,56; 21,25) → U2.7; CC2 → J1 B5, PD_CFG1, PD_PG az U2-nél kész, zárolva; a CC1 kijáratot elzáró felesleges +3V3 hurok (R11 → via → vissza) törölve |
| U3 eFuse kimenet | VBUS_SW (pad 6, 0,3×2,4 csík) **először bekötve**: déli vég → 0,6/0,3 via (41,05; 15,0) → In2 0,5 mm y 14,9 → VBUS_SW zóna (36,71); a zónán belüli felesleges VBUS In2 sávok törölve |
| VBUS zóna | `KO_VBUS_In2` szabályterület (In2, sáv tilos, via szabad), kihagyva a VBUS_SW átvezetés folyosóját; a zónát szabdaló IR_SW_EN/CAM_3V3/I2C In2 sávok újravezetve → **VBUS In2 zóna 1 sziget** (északi U3 ↔ déli J1/U2 a keleti, ~1,9 mm-es nyakon) |
| USB árnyékoló RC | R1/C1 a B jobb-felső sarokból F oldalra a J1 köpenyfül mellé (43,6; 20,6 / 23,6), a 10 mm-es In2 árnyékoló-sáv megszűnt |
| Eszköz-javítás | `maze/kgeom.py` CLR táblája 4 rétegű értékekre (Default 0,15, USB/CSI/PWR 0,2) – eddig 2 rétegű 0,2/0,25 értékkel számolt, ezért nem talált kivezetést szűk lábsorokból; `prep4.py` `FR_RESPECT_LOCKS=1` opció |
| Freerouting | nem használható tovább: a meglévő rézen 102 saját szabálysértést lát → 0 előrelépés |
| Állapot | DRC **0 hiba**; nyitott **21** (GND 6, I2C_SCL 2, VBUS (TP1), VBUS_SW (U7 DNP), SD_3V3 (TP6), +3V3 (R11), CAM_3V3 (TP5), CC2 hosszú ág → R36, PD_PG (TP17), EF_ILM, NTC_ADC, IR_SW_EN, I2C_SDA (hiányzó via, a hely ütközik PD_PG via-val), EFUSE_FLT, PDM_CLK) |
| ⚠ Megfigyelések | maze 0,2 mm-es VBUS csonkokat tesz (PWR 0,4 helyett) – teljes áramú csonkok szélesítése kell; USB_DM a J1-től északi kerülővel (~10 mm) megy a modulhoz, a DP nyugatra → páron belüli hossz-eltérés ellenőrizendő; a B oldali TP-rács (U2 alatt) sok hosszú ágat okoz (TP1/5/6/17) |

## MAIN v0.6 – TP-áthelyezés + maze-javítások (2026-10-10, 2. kör)
| Tétel | Állapot |
|---|---|
| Áthelyezés | TP1 (VBUS) → (40,35; 32,25) a VBUS via mellé; TP5 (CAM_3V3) → B (12,6; 6,6) a CAM_3V3 hálóhoz; TP6 (SD_3V3) → B (23,4; 41,6); R10 (EF_ILM) → U3 keleti oldala (43,4; 15,6), C4 → (43,4; 18,65), R1/C1 → (43,6; 21,7 / 24,8); a 2,75 mm-es TP-rács ezzel megszűnt (tulajdonosi döntés: 1-es opció) |
| maze javítás | (1) a raszter a DRC szerinti max(saját, akadály) távolsággal tágít – eddig PWR/PWR_LIGHT/USB hálók Default akadály mellett DRC-hibásak lettek és visszavonódtak; (2) Default hálók 0,5/0,25 via-t kapnak (eddig mind 0,6/0,3); `ripall.sh` `RIPM` doboz-margó |
| Új eszköz | `maze/route_all.py` (globális feltépés + sorrendezett újravezetés) – kipróbálva: **rosszabb** (48 nyitott) → elvetve, d16 állapot visszaállítva |
| Állapot | DRC **0 hiba**; nyitott **20** (GND 9; nem-GND 11: +3V3 ×2 (R11), EFUSE_FLT, I2C_SCL, I2C_SDA, PDM_CLK, U0TXD_TP, SD_3V3 (TP6), valamint csak DNP-alkatrészekhez: CC2 → R5/R36, VBUS_SW → U7, IR_SW_EN → R29) |
| Kész ebben a körben | minden VBUS (J1 déli lábpár, TP1), CAM_3V3 (TP5), EF_ILM, PD_PG, NTC_ADC, PDM_CLK_J5 |

## MAIN v0.6 – célzott feltépés, GND öntés, hurokmetszés (2026-10-10, 3. kör)
| Tétel | Állapot |
|---|---|
| Új eszközök | `maze/ripthru.py` (puha akadályos maze → csak az átvágott sávokat tépi, a célt zárolva vezeti, az áldozatokat rekurzívan újravezeti; csak javulást tart meg); `maze/prune.py` (hálónként feszítőfa + zsákutca-levágás, zónás hálók kivéve) – **452 felesleges elem** (maze-hurkok) törölve, nyitott/hiba változatlan; maze `SOFT`/`SOFT_COST` mód |
| GND öntés | `gnd_pour.py` javítva (eddig argumentum nélkül a GND_In1 síkot is törölte volna!): GND_F, GND_B, GND_In2 (prioritás 0, a VBUS/VBUS_SW In2 zónák 2-es prioritással nyernek) |
| Áthelyezés | TP3 (GND) → (43,1; 40,5) |
| Kész ebben a körben | PDM_CLK, +3V3 ×2 (R11), EFUSE_FLT, I2C_SDA, IR_SW_EN (DNP ág) |
| Állapot | DRC **0 hiba**; nyitott **13**: működési 4 – I2C_SCL U2.2 (CH224A I2C, B-4), I2C_SCL J2.13 (kamera SCCB), U0TXD_TP (J7.7 ↔ R40.2), SD_3V3 (TP6); DNP 2 – VBUS_SW → U7, CC2 → R5/R36; GND 7 (zónaszigetek/varrás) |
| Megfigyelés | az U2 keleti EP–láb csatornája (0,75 mm) egy sávot enged; az SDA mindkét ága ezt foglalja; az SCL déli kijáratát zárolt VBUS via-k (TP1, U2.1) és TP-padok zárják. A J2 alatti sarokban a C6-köteg (In2), a CAM_PWDN (F, y 8,0) és az R70/R31/R32 oszlop zár |

## MAIN v0.6 – maradék működési hálók (2026-10-10, 4. kör)
| Tétel | Állapot |
|---|---|
| Méretnövelés | **elvetve** (a 4 maradékból csak 1–2-n segítene; J1/USB/CC/VBUS teljes újravezetése kellene) – a tulajdonos „ha segít” feltétellel engedte |
| I2C_SCL (U2, CH224A) | SDA déli ága megszűnt (B keleti szélsáv x 44,12 egyenesen), TP1 → (42,95; 32,25) az U2.1 VBUS via mellé, SCL F csonk a 0,75 mm-es EP–láb csatornában → via (41,95; 33,3) → In2 nyugatra (KO_VBUS_In2 bevágás y 30,2–33,75) → SCL via (30,35; 32,04); VBUS zóna 1 sziget ✅ |
| I2C_SCL (J2, kamera SCCB) | R70 (47R PDM CLK soros) → **B (17,0; 8,0)** a J2 alá (szabályos-hely keresés + maze-teszt); SCL F-en egyenesen le az R31 lábai között ✅; PDM_CLK, PDM_CLK_J5 újravezetve ✅ |
| SD_3V3 | TP6 → **B (36,3; 10,4)** ✅ |
| U3.8 GND | GND via (42,4; 13,7) → In1; EF_ILM újravezetve ✅ |
| Állapot | DRC **0 hiba**; nyitott **9**: U0TXD_TP (J7.7 ↔ R40.2), J1 A1 + A12 GND, GND szigetek (F/B öntés, C24, U7 DNP), DNP: VBUS_SW → U7, CC2 → R5/R36 |
| ⚠ Kritikus | **J1 A1/A12 (USB-C GND) bezárva**: É köpenyfül-furat, Ny zárolt USB_DP (x 35,58) ill. R11/EFUSE_FLT, K J1-test (via tilos) → a J1 kivezetés (USB DP/DM pár + CC + GND) újratervezése kell |
| U0TXD_TP | R40/R41 a J5 „zsebben” (B2B csomópont; PDM_CLK_J5, IR_VIN, SCL, U0RXD_TP vonalak zárják) – kapu nyitása vagy R40/R41 + UART útvonal újratervezése kell |

## MAIN v0.6 – J1 kivezetés újratervezése (2026-10-10, 5. kör)
| Tétel | Állapot |
|---|---|
| J1 A1 GND | USB_DP felesleges északi kitérője (In2 x 35,58 → via (35,54; 18,8) → B vissza) törölve, új USB_DP via (35,3; 20,5) → B a modul 51-es padjához (DP rövidebb lett); GND via (35,62; 19,15) + B csonk az A1-hez ✅ |
| J1 A12 GND | R11 (EFUSE_FLT felhúzó) → **B (36,0; 15,5)** (szabályos-hely keresés + maze-teszt, `scratchpad/spotsearch.py` mintájára); CC2 B kivezetés újra (B5 → egyenesen Ny y 24,25 → átló → via (37,12; 27,98)); EFUSE_FLT In2 vége újra a modul 56-os padjáig; GND via (35,78; 26,33) az A12-höz ✅ |
| GND öntés-szigetek | 4 rétegű sziget-varró (`scratchpad/stitch4.py`): 1 via; **C2.2 (CH224A VBUS-kondi GND) és TH1.2 (NTC GND) F-szigete még via nélkül** – a puha útkereső próbája rövidzárat adott, visszavonva |
| Állapot | DRC **0 hiba**; nyitott **7**: U0TXD_TP; GND: C2.2-, TH1.2-sziget, C24, U7 (DNP); DNP: VBUS_SW → U7, CC2 → R5/R36 |
| ⚠ USB | a DM a J1 test alatt É-i kerülővel megy (~10 mm-rel hosszabb a DP-nél) – HS-nél a páron belüli eltérés ellenőrizendő/javítandó |

## MAIN v0.6 – huzalozás lezárva (2026-10-10, 6. kör)
| Tétel | Állapot |
|---|---|
| C2.2 GND | C2 (CH224A VBUS-kondi) 180°-kal forgatva → GND láb a meglévő GND viák mellé; VBUS az U2.1 VBUS viájához ✅ |
| TH1.2 GND (NTC) | GND via (22,75; 28,15) + csonk; SD_D3 és SD_CLK helyben újravezetve (hosszabbak, SD alapsebességen elhanyagolható) ✅ |
| C24 GND (VO4 kondi) | GND via (31,5; 40,6) + B csonk (pontos ütközés-vizsgálatos helykeresés; a maze raszter túl óvatos volt) ✅ |
| U0TXD_TP | U0RXD_TP 0,1 mm-re vékonyítva (ugyanazon nyomvonalon), +3V3 via (18,48; 15,69) → (18,3; 15,85), U0TXD_TP 0,1 mm-es sávval (`TRACK_W=0.1`, GRID_MARGIN 0,01), ~56 mm, 6 via ✅ |
| Táp-szélesítés | 118 PWR/PWR_LIGHT szakasz → 0,4 / 0,3 mm (DRC-vezérelt, ahol nem fért, maradt) |
| USB | a P50/P51 FS USB-Serial-JTAG (12 Mbps) → a DM ~10 mm-es többlete **nem gond** |
| **Végső DRC** | **0 hiba**; figyelmeztetés: szitanyomat 198 (kozmetikai, rev A előtt refdes-rendezés), 12 lógó sáv + 2 lógó via (T-csatlakozás hidak – törlésük szakadást okoz, maradnak), 4 lib-eltérés |
| Nyitott (DNP, rev B) | **3**: CC2 → R5/R36 (Rd / CC-ADC tap), U7 GND, VBUS_SW → U7 (IR eFuse) – rev A-ban nem beültetett alkatrészek; beültetés előtt be kell kötni |
| Statisztika | 2404 sávszakasz, 233 via (141 × 0,5/0,25, 91 × 0,6/0,3), 3,1 m; legkisebb sáv 0,1 mm (JLC 4L min. 0,09) |
| Kép | `docs/img/main_v06_routing.png` (F / In2 / B, öntéssel) |
| Hátra | szitanyomat-rendezés, gyártási export (Gerber/drill/BOM/CPL), FRONT lap (J5 az alsó élen), G0–G6 kapuk, `08` diagramok GPIO v0.6-ra |

## MAIN v0.6 – többagentes NYÁK-review (2026-10-10, 7. kör)
7 független szakértő-agent (táp, SI, GND/EMC, RF, DFM, mechanika, villamos) + dimenziónként 1 szkeptikus újramérő + 1 hiánykereső/összegző (15 agent, ~790 eszközhívás). Másolaton dolgoztak, a projektfájl érintetlen.

**Ítélet: NO-GO gyártásra jelen állapotban; GO egy célzott layout-kör + BOM-döntések + célzott újramérés után.** Végzetes hiba nincs (DRC 0, séma↔NYÁK net-paritás tiszta, U1/U3/U4/CH224A padkép adatlap/DXF szerint egyezik, értékek: UVLO 4,40/4,00 V, OVLO 10,87 V, ILIM 2,03 A, FB 3,328 V, SS 1,45 ms) – a lap nagy valószínűséggel elindulna, de gyártás után nem javítható szabályokat sért.

| Súly | Kötelező | Tétel | Javítás |
|---|---|---|---|
| high | ✔ | **U4 buck layout**: nincs kondi a VIN/GND lábaknál, hurok 16 mm² 4 via-átmenettel, bemeneti kondik GND-je külön F-szigeten, BST/SW ág B-n a modul alatt, FB a BST/SW padok között, In1 antipad-rések (x≈31,5; y≈28) | 100 nF + 10 µF közvetlenül pin 3/4-re, C11 F-re pin 5/6, R14/R15 az FB-lábhoz, C10 pin 7-hez, 2–3 GND via a lábaknál, via-oszlopok szétszedése |
| high | ✔ | **RF út (U1 P2 → R34 → J4 u.FL, rev A-ban FIT)**: In2 referencia a +3V3 és CC1_ADC sávval elvágva (19%), lebegő In2 sziget, nincs GND kerítés | +3V3/CC1_ADC ki az x 0,5–9,5 / y 33–40,5 tartományból, In2 tiltó terület, GND viák J4-nél + kerítés ≤2 mm osztással |
| high | ✔ | **GND varrás**: csak 44 GND via (2L-ben 283–309 volt), F-öntés 25%-a >6 mm-re viától (max 12,3 mm), élen 0 via, GND_In2 30 sziget (23 egy viás) | ~60–100 via: élkerítés 3–4 mm, rács ≤5 mm, szigetenként ≥2 via; cél: max 6 mm via-távolság |
| high | ✔ | **G4 BOM-kapu nyitott**: 0 MPN/LCSC mező, 07-ben 73 TBD; J2 (FPC) lábkép helyőrző, érintkező-oldal (Q6) nyitott → rossz oldal = 3V3/GND csere a kameránál; J5, L1 helyőrző | MPN-ek, J2 alkatrész + oldal rögzítése a valós FFC/kamera alapján |
| high | ✔ | **ESP_EN**: R23 (10k) és C25 (1 µF) DNP → semmi nem húzza fel az EN-t (Q3 nyitott) | R23 + C25 FIT (csak BOM-változás) |
| medium | ✔ | CPL/BOM: U3 lábkép `attr smd` nélkül (CPL-ből kiesik), U1 + MH1–4 nincs kizárva; 51 DNP-attribútum eltérés | lib + lap attribútumok, DNP szinkron, CPL = 70 sor ellenőrzés |
| medium | ✔ | U3 eFuse: 0,2 mm rések 100% pasztával (TI: 82/93%); JP1 maszk-gát nélkül (VBUS↔VBUS_SW híd veszély) | paszta-csökkentés, ENIG, első táp előtt ellenállásmérés |
| medium | ✔ | C4 (EF_DVDT) 0,28 mm-re a J1 köpenyfül-padtól (DRC nem látja: J1 udvar csak B-n) | C4 (R9/R10) áthelyezés ≥1 mm, F.CrtYd gyűrű |
| medium | ✔ | CSI visszatérő út: J2 GND lábaknál nincs via (≥5 mm), páronként 1 return via, CSI_D0P csonk a +3V3 In2 sáv felett | via J2 GND lábakhoz, 2. return via, In2 sávok ki a CSI alól |
| medium | ✔ | Gyártási specifikáció hiányzik: nincs stackup a lapban (gbrjob = KiCad alap), nincs felület, rev-szöveg; 32–40 alkatrész <5 mm-re az éltől | JLC04101H-3313A + impedancia, ENIG, sínek + fiduciálok, rev szöveg |
| medium | – | CSI hossz: D0 9,6 / D1 15,3 / CLK 21,4 mm (adat–órajel 6–12 mm ≈ 0,03–0,05 UI); „pár-skew 0,000” állítás **hamis** (valós 1,2–1,4 mm), zegzug hangolás hatástalan | valódi meander vagy elfogadott eltérés + G3 szemábra-teszt; DRU szabályok |
| medium | – | 3V3 trönk: 0,15 mm-es nyak a SW pad mellett, 0,3 mm belső (0,5 oz) sáv, egyes 0,25 viák (~64 mΩ); netclass szélesség nincs DRU-ban kikényszerítve | ≥0,6 mm / 0,8–1,0 mm trönk, 2× 0,3 via, DRU track_width szabály |
| medium | – | USB DM: ESD (U5) a modul-elágazás után; U5 GND közös a buck bemeneti GND-vel; DM B-n VBUS sík felett | J1 → U5 → U1 sorrend, külön GND via |
| medium | – | USB-C táp-bemenet: J1 GND 2 kis via, TVS 13 mm-re, VBUS nyak 0,2–0,3 mm, VBUS_SW sík szétesik, U3 kimenetén nincs kondi | viák, nyak szélesítés, 1 µF az U3 OUT-ra |
| medium | – | Hosszú nyitott csonkok DNP-hez: CC1 ~97 mm, CC1_ADC 85 mm, VBUS_SW élcsonk 44,5 mm | DNP ágak rövidítése / 0R az elágazásnál |
| medium | – | Kamera vezérlő-ESD (05 §0.1 FIT) nincs a sémában; SD ESD lábkép hiányzik; CC védelem nincs | 3 csatornás ESD a J2-höz vagy formális rev B-re halasztás |
| medium | – | VBUS_MON: D2 zener szivárgás 43 kΩ-os csomóponton elviheti a 9 V / LOW döntést | D2 DNP vagy kis szivárgású clamp |
| medium | – | Közös I2C (CH224A + kamera + FRONT): csak CH224A belső felhúzók, CH224A 0x0A reg. 20/28 V-ot kérhet | FW: CH224A csak olvasás; inkább külön I2C láb |
| medium | – | Szerelőfuratok középpontja (22,5; 25,0) ≠ lapközép; MH lábképek udvar/kizárás nélkül, sáv csavarfej alatt | as-built koordináták rögzítése 05/06-ban a FRONT előtt |
| low | – | CAM_3V3_EN GPIO4 reset alatt; paszta U1-en és DNP-ken; via D1 padban; szitanyomat 198 + nincs név/rev | R28 10k; paszta; szitanyomat |
| info | – | 312 duplikált sávmásolat (GND 287); 12 „lógó” sávból csak 4 valódi T-híd; 90-log hibás állításai: pár-skew 0,000, U2 EP 2 via, 1,9 mm VBUS nyak, 10 viás RF kerítés | tisztítás másolaton; dokumentumok as-built frissítése |

Cáfolva: electrical-14 (D1 TVS polaritás helyes). Bizonytalan: J1 dugó-illeszkedés (mech-02), GPIO4 reset-állapot (electrical-06).
Nem ellenőrizhető offline: Waveshare modul séma (EN RC, RF 0R irány), ESP32-P4 adatlap (reset pull-ok), TPS22917/TPD2E2U06/J2/J5/L1 adatlapok, JLC élő képességek/készlet.
**Tanulság:** a „DRC 0 hiba” nem jelent jó layoutot – a 6. kör „huzalozás lezárva” túlzás volt; a buck, a varrás és az RF referencia minőségi szabályait a DRC nem ellenőrzi.

### Helyesbítések a korábbi bejegyzésekhez (7. kör review alapján)
A korábbi bejegyzéseket nem írjuk át. Az alábbi állításokat a 7. kör újramérése (a review `result.json`, dimenziónként szkeptikus újramérővel megerősítve) a MAIN v0.6 lap 2026-10-10-i pillanatképén **hibásnak vagy elavultnak** találta. A 2 rétegű (60×50) állapotra tett állítások akkor igazak lehettek, de a v0.6 lapra nem érvényesek.

| Eredeti állítás (bejegyzés) | Valós, mért állapot (v0.6) | Forrás |
|---|---|---|
| „hossz: D0 9,28 / D1 14,98 / CLK 21,12 mm, **pár-skew 0,000**” (*CSI kézi huzalozás + 2. kör*, 2026-10-09) | Mért hossz (csak sávok, duplikátum nélkül): D0 9,580 / 9,580, D1 15,280 / 15,285, CLK 21,415 / 21,415 mm. A D1N (8 zegzug, 0,145 mm) és a CLKN (12 zegzug, 0,114 mm) amplitúdója kisebb a 0,204 mm-es sávszélességnél → a +1,16 / +1,37 mm-es középvonal-többlet gyakorlatilag **nem késleltet** (a réz egy kiszélesedő szalag). **Valós páron belüli eltérés ≈1,2–1,4 mm** (D1 ≈1,16 mm ≈7 ps, CLK ≈1,37 mm ≈8 ps; ≈0,006 UI) – funkcionálisan elhanyagolható, de a „0,000” hamis. A D0N meander (0,727 mm amplitúdó) valódi. Adat–órajel eltérés: D0 11,8 mm, D1 6,1 mm (≈66–70 / 36 ps; 0,053 / 0,029 UI @ 800 Mbps); a CLK (21,4 mm) és a D1 (15,3 mm) túllépi a `05` §13 „<15 mm” szabályát | si-05, si-04 |
| „szélesség 0,204, rés ~0,203 a csatolt szakaszokon” (uo.) | a 0,203 mm-es résű csatolt szakasz rövid: D0 0 / 9,58 mm, D1 5,0–5,3 / 15,3 mm, CLK 7,0 / 21,4 mm; a többi 0,6–0,8 mm-es résű (becsült Zdiff ≈115–117 Ω; a D-PHY ablakon belül, a 100 Ω ±10 % célon kívül) | si-06 |
| „Maradt: **U2 EP 2 termikus via** (szándékos)” (*SD-blokk lazítás*, 2026-10-09, 2 rétegű) | a v0.6 lapon az EP-n belül (39,7–41,8 × 29,4–32,7) **nincs via**; a CH224A egyetlen GND-je (pin 0 = EP) **1 db, a padon kívüli viával** (41,175; 28,525) kötődik a síkhoz; a C2.2 (VHV-kondi GND) egy másik F-szigeten. ~0,11 W mellett alacsony kockázat; a forrasztást (röntgen / folytonosság) ellenőrizni | power-10 |
| „VBUS In2 zóna 1 sziget (északi U3 ↔ déli J1/U2 a keleti, **~1,9 mm-es nyakon**)” (*U2 (CH224A) környék lazítása*, 2026-10-10) | a két fél **csak egy ~0,2–0,3 mm-es nyakon** kapcsolódik: **x 41,6–42,0, y 14,8–15,2** (a VBUS_SW via (41,05; 15,0) és a GND viák (42,42; 14,88) / (42,83; 15,62) között); a keleti ujj (x 43,0–43,4) a (42,825; 15,625) GND via miatt y 15,2-nél zsákutca. ≤1 A-en az ellenállás és a melegedés elhanyagolható, de nincs tartalék, és a nyak a J1 → TVS úton van | power-06, power-07 |
| `PWR_VBUSSW_In2` „264 mm²”-es táp-zóna (*táp-blokk átrendezés + In2 táp-zónák*, 2026-10-10) | a zóna **3 szigetre** töltődik (80,07 / 25,08 / 15,47 mm²), ezeket 0,4 mm-es In2 sáv és egyes viák kötik (U3.6 → U4.3 ≈45 mΩ, minden átmenet 1 via – a `05` §4.1 „≥2 via” szabálya sérül) – síkként nem működik | power-05 |
| „RF kerítés **10 db** (±1,05 mm a B.Cu RF vonaltól, ≤1 mm osztás)” (*GND öntés*, 2026-10-09, 2 rétegű) | a v0.6 lapon **nincs RF-kerítés**: az RF középvonaltól 2 mm-en belül 0 GND via; a legközelebbi (5,742; 37,033) 2,01 mm, a következő (7,975; 37,475) 2,83 mm, a többi >9 mm. A teljes lapon 44 GND via (233-ból; a 2 rétegű változatban 283–309) – a 4 rétegű átdolgozásnál veszett el | si-01, rf-02, gnd_emc-01 |
| „U5 ESD a nyomon (IO padok a vonalakon)” (*USB D+/D− huzalozás*, 2026-10-09, 2 rétegű) | a v0.6 lapon a D− clamp a **modul-elágazás után** áll: J1.A7 → U1.50 18,78 mm, → U5.2 20,13 mm (a tranziens előbb éri a P4 lábat); az U5.3 GND egy sávon és egy vián osztozik a buck bemeneti kondijának visszatérő útjával (`05` §13.1 sérül). A D+ rendben (J1.A6 → U5.1 3,95 mm, → U1.51 6,60 mm) | gnd_emc-04 |
| „12 lógó sáv + 2 lógó via (**T-csatlakozás hidak** – törlésük szakadást okoz, maradnak)” (*huzalozás lezárva*, 6. kör) | a 12 lógó sávból **csak 4 valódi T-híd** (SD_3V3 In2 0,106 mm, +3V3 In2 0,071, PD_PG F 0,224, I2C_SDA B 0,112 mm); **8 zsákutca-csonk** (VBUS_SW F 2,75 → DNP U7; +3V3 F 1,48; CAM_3V3 In2 4,35; CC2 B 0,78; ICR_IN2 In2 2,69; I2C_SDA F 1,85; SD_D3 B 2,11; SD_CLK B 2,60 mm) – mind ≤4,35 mm, ártalmatlan, a 8 csonk törölhető | gnd_emc-17 |
| „Statisztika: **2404 sávszakasz**” (6. kör) | ebből **312 pontos duplikátum** (GND 287, VBUS 23, PDM_CLK_J5 1, EFUSE_FLT 1; egy szakasz legfeljebb 19×) → 2092 egyedi; a hossz-/skew-riportokat torzíthatja | gnd_emc-16, power-13 |
| „**huzalozás lezárva**”, „Végső DRC 0 hiba” (6. kör címe és összegzése) | **túlzás**: elektromosan minden FIT-pad bekötve (DRC 0, séma ↔ NYÁK paritás tiszta), de a 7. kör ítélete **NO-GO**: buck bemeneti hurok (nincs kondi a VIN/GND lábaknál, BST/SW a modul alatt B-n), RF-referencia (In2 metszve, kerítés nincs), GND-varrás (44 via, 30 In2-sziget, ebből 23 egy viás), J2/CSI visszatérő via hiánya – ezeket a DRC nem ellenőrzi. Helyes megfogalmazás: „**bekötve (DRC 0), minőségi layout-kör hátravan**” | 7. kör ítélet |

Dokumentum-oldal: a `05` (v0.6 as-built: §0.1 döntések, §3.1a befagyasztott interfész, §5, §6, §12), `06` („As-built elhelyezés”), `07` (v0.3) és `08` (v0.3, GPIO v0.6) e helyesbítések és a 2026-10-10-i delegált döntések szerint frissítve. A layout-javító kör eredményét külön bejegyzés rögzíti.

## MAIN v0.6 – javító körök a 7. kör review alapján (2026-10-10/11, 8. kör)
Párhuzamos, régiókra kerített javítás: agentenként teljes projektmásolat + saját laprégió, UUID-alapú visszafésülés (`kicad/MAIN/scripts/pcbmerge.py`, régióőr `regioncheck.py`); minden javítást független ellenőrző agent mért újra, hiány esetén javító kör.

| Kör | Terület | Eredmény (mérve) |
|---|---|---|
| előlépés | DNP-csonkok | CC1 (96,5 mm), CC1_ADC (85,4 mm), CC2_ADC (57,9 mm), VBUS_SW élcsonk (47,2 mm) törölve – rev B beültetés előtt újra kell húzni; 255 duplikált sávmásolat törölve; MH1–4 → gyári `MountingHole_2.2mm_M2` (board-only) |
| 1 / buck | U4 TPS62933F | bemeneti hurok 16,3 → ~1,4 mm² (C9 0,59 mm-re a lábaktól, via nélkül); SW csak F-en (B jumper törölve); FB csomópont 8,7 → 2,8 mm; SS 15,6 → 3,4 mm; In1 a hurok alatt 22–41% → 92–97%; 3V3_BUCK 0,15 → 0,8 mm + F zóna; U5 saját GND via |
| 1 / USB-C | J1, U3, D1, C4 | C4 ≥1 mm a J1 köpenyfuratoktól; J1 GND viák; VBUS nyak szélesítve; via kivéve a D1 padból; CH224A EP 2. GND via; C1 a köpenyfül mellé |
| 1 / CSI | J2 | GND via minden J2 GND lábnál; 2. return via minden CSI via-párnál; In2 GND a CSI csonkok alatt + In2 tiltó terület; hamis zegzug → valódi kitérő (D0 9,6 → 10,4 mm); adat–órajel eltérés **elfogadott** (≈0,05 UI), G3-on mérendő |
| 1 / RF | U1.2 → R34 → J4 | +3V3 ki az RF alól, In2 tiltó terület → GND_In2 folytonos az RF vonal alatt; GND kerítés + J4 GND viák |
| 1 / meta | séma, lib, DRU, attrib. | R23/C25 FIT, D2 DNP, R28 10k; DNP/BOM/pos jelölések; U3/U7 `attr smd` + paszta-csökkentés (TI), U1 paszta nélkül; stackup JLC04101H-3313A + ENIG + impedancia a lapfájlban; DRU: PWR ≥0,4 / PWR_LIGHT ≥0,3 figyelmeztető szabály, PWR zónák ≥1 mm a széltől |
| 2 / A (DNy) | modul táp | +3V3 R16 → U1.84-86: 40,0 → 28,4 mΩ, 0,8 mm sín a P84-86-on; C21/C22/C23 a P84-86 alá (C22/C23 0,2 mΩ); SD_EN ki az RF dobozból; MH3 körüli alkatrészek arrébb |
| 2 / B (K) | USB, eFuse | USB D− clamp-first; VBUS_SW In2 sík egyben; J1 A12/B1 2. GND via; **C14 1 µF/25 V az U3 OUT-on (új alkatrész, séma + lap)** |
| 2 / C (DK) | J5 K, TP-mező | MH4 körüli DNP-k arrébb; PD_PG 22,8 mm-es kerülő → 2,3 mm; GND kerítés + sziget-viák (max. via-távolság ≤5 mm) |
| 2 / D (É+Ny) | J2, U6, SD | MH1/C50; lógó csonkok; GND varrás |
| 2 / BOM | G4 | 72 beültetett tétel LCSC-számmal (16 Basic, 24 Extended), `fields_apply.py` → LCSC/MPN/Manufacturer mezők a sémában és a lapon; J2 = TE 1-84953-5 (kapható, készlet alacsony) |
| **Állapot (05:20)** | | DRC **0 hiba**, ERC 0, séma↔lap paritás **0** (volt 178); 12 bekötetlen, mind DNP; track_width figyelm. 125 → 37; lógó 14 → 1 |

## MAIN v0.6 – végső többagentes review (2026-10-11, 9. kör)
**Módszer:** 7 dimenzió (táp, SI, GND/EMC, RF, DFM, mechanika, villamos) – dimenziónként 1 szakértő + 1 szkeptikus újramérő, 1 kritikus/összegző, + a párhuzamos szitanyomat-agent (**16 agent**). A 8. kör utáni pillanatképen (a `kicad/MAIN` lappal md5-azonos) minden 7. körös tétel újramérve (javítva / részben / elfogadott / nem javítva), az új tételek szkeptikus ellenőrzéssel; a kritikus a fő hibát reprodukálta és a javítást másolaton igazolta. Projektfájlhoz nem nyúltak.

**Ítélet: feltételes GO a rev A rendelésre (JLC 4 réteg + kétoldalas PCBA)** – a design rendben, layout-változtatás nem kell; **rendelni csak egy újratöltött (refill) és a projektmappában mentett lapfájlból szabad.** Az egyetlen kritikus tétel folyamat-szintű: a lapfájlba mentett **zóna-kitöltések elavultak** – töltés nélkül plottolva a +3V3, VBUS, VBUS_SW és ~10 jelháló GND-zárlatot kapna (DRC refill nélkül **173 hiba**: 133 clearance, 27 hole_clearance, 13 solder_mask_bridge; refill-lel 0). Másolaton igazolva: `kicad-cli pcb drc --refill-zones --save-board` a projektmappában → DRC refill nélkül **0 hiba / 12 bekötetlen (mind DNP) / paritás 0**; a gbrjob ENIG / ImpedanceControlled / Rev A / 0,9872 mm; CPL 72 sor (47 F / 25 B). A projektmappán **kívüli** refill más rezet ad (a `.kicad_dru` 1 mm-es él-szabálya elvész: PWR_VBUS_In2 152,5 vs 138,6 mm²) → tilos. Az U1 modul reze a DXF-fel igazolt lábkép (csak a B.Paste törölve). A szitanyomat-agent lapja a pillanatképhez képest **0 réz-eltérésű** (silk DRC 214 → 0), de ugyanazokat az elavult kitöltéseket hordozza.

**Rendelés előtti kapu (a tulajdonos lássa lefutni, a szitanyomat-összefésülés után, a rendelendő `kicad/MAIN` fájlon, mellette a `.kicad_pro` + `.kicad_dru`):** (1) refill + mentés (`kicad-cli pcb drc --refill-zones --save-board …` vagy GUI: Fill All Zones + Save); (2) DRC refill nélkül: 0 hiba / 12 bekötetlen / paritás 0; (3) `copper_diff.py` a review-pillanatképpel: 0 réz-eltérés, 0 elavult kitöltés; (4) Gerber `--check-zones` + drill, az In2 réteg Gerber-nézőben; (5) frissített rendelési jegyzet. Az ennél korábbi Gerberből rendelni tilos.

**A 7. kör tételei – végső állapot** (✔ = a 7. körben kötelező)
| | Tétel | Állapot | Mért (9. kör) |
|---|---|---|---|
| ✔ | U4 buck layout | ✅ javítva | forró hurok 16,3 → **1,44 mm²** (C9-en át, via nélkül); SW csak F-en (3,0 mm, 0 via); FB 2,77 mm; SS 3,42 mm; In1 100 % a SW/BST/FB alatt; a buck F-GND szigeten 12 GND via |
| ✔ | RF út U1 P2 → R34 → J4 | ✅ javítva | In2 **100 % GND** az RF alatt (egy 325,6 mm²-es sziget, 44 via); GND via 1,0 / 1,5 mm-en belül **10 / 14** (volt 0 / 0); 0,302 mm végig, út 7,96 mm; KO_RF_In2 tiltó terület |
| ✔ | GND varrás | ◐ nagyrészt | GND via 44 → **148**; >6 mm-re viától lévő öntés 235 → **0 mm²**; élközeli (≤1,5 mm) via 0 → 38; maradék: él-kerítés rések (alsó 15,4, jobb 18,9 / 10,75 mm), In2 32 sziget, max. geodéziai 12,9 mm |
| ✔ | G4 BOM-kapu | ◐ adat kész | 72/72 FIT tétel LCSC / MPN / Manufacturer mezővel (séma = NYÁK = `bom_jlc.csv` = CPL); nyitott: Q6, Q17; dokumentumok ebben a körben frissítve |
| ✔ | ESP_EN RC | ✅ | R23 10k (C25804) + C25 1 µF (C15849) FIT, τ = 10 ms |
| ✔ | CPL/BOM attribútumok | ✅ | CPL 72 sor (47 / 25); U3 `attr smd`; U1, MH, TP, JP1, DNP kizárva; paszta F 159 / B 65 nyílás = pontosan a CPL-halmaz |
| ✔ | U3 paszta + JP1 | ✅ | U3 paszta 82 % (pad 5/6) / 93 % (sarok), a TI RPW0010A stencil szerint; ENIG a lapfájlban; JP1: első táp előtti VBUS ↔ VBUS_SW mérés |
| ✔ | C4 ↔ J1 köpenyláb | ✅ | C4 → B (42,9; 16,2): 0,279 → **1,005 mm**; F-en a legközelebbi idegen pad C1.2 (GND) 0,757 mm |
| ✔ | CSI visszatérő út | ✅ | páronként 2 GND via ≤1 mm-en; J2 GND lábak viája 5,05–6,13 → **0,68–1,49 mm**; In2 100 % GND a CSI B-csonkok alatt |
| ✔ | Gyártási specifikáció | ✅ (lapfájl) | stackup JLC04101H-3313A, ENIG, impedancia, Rev A a lapfájlban és a gbrjob-ban; a rendelési jegyzet elavult → tulajdonosi tétel |
| – | CSI hossz / skew | elfogadott | D0 10,446 / D1 15,280 / CLK 21,415 mm; páron belül ≤0,003 mm; adat–órajel 10,97 / 6,14 mm ≈ 64 / 36 ps ≈ **0,05 / 0,03 UI** @800 Mbps; G5b soak teszt (`05` §13, §15) |
| – | 3V3 trönk | részben | a 0,15 mm-es nyak megszűnt (0,8 mm + F zóna); R16.2 → U1.84–86 **21,2 mΩ** (volt ~43); maradt: 2 egyes 0,5/0,25 via sorban |
| – | USB D− / U5 | részben, rev A elfogadva | D− clamp-first (J1 → U5.2 1,85 mm); D+ 2,6 mm-es T-csonkon; az U5.3-nál nincs saját via (legközelebbi GND via 1,96 mm); USB csak FS |
| – | USB-C táp-bemenet | részben | J1 GND pin-páronként 2 via; J1 → U3.5 7,1 mΩ; U3 IN 3 / OUT 2 via; **C14 1 µF az U3 OUT-on**; VBUS In2 nyak 1,05 / 0,55 mm (párhuzamos B-út); D1 helye: elfogadott eltérés |
| – | DNP-csonkok | ✅ | CC1 107,4 → 10,97 mm; CC1_ADC / CC2_ADC 0 mm; VBUS_SW élcsonk törölve; maradt 1 lógó +3V3 In2 csonk (4,54 mm) |
| – | Kamera / SD / CC ESD | elfogadva → rev B | J2 vezérlő-ESD, SD ESD rev B; CC clamp nincs (CH224A CC abs max 32 V) → rev B listára |
| – | VBUS_MON D2 | ✅ | D2 DNP |
| – | Közös I2C (CH224A + kamera + J5) | nem javítva → FW-szabály | R31/R32 DNP; SDA 112,9 / SCL 63,9 mm; felfutás 10–15k / 25–35 pF mellett ~0,2–0,45 µs → **100 kHz** |
| – | Szerelőfuratok | elfogadva | gyári `MountingHole_2.2mm_M2` (maszk = furat, udvar csak F-en); koordináták befagyasztva; alátét-szabály (`05` §3) |

**Helyesbítések a 8. kör bejegyzéséhez:** „U5 saját GND via” → az U5.3 padnál nincs via: a legközelebbi GND via 1,96 mm-re (termikus küllőkön át), plusz egy 0,25 × 2,62 mm-es sáv egy 2,47 mm-re lévő viához (gnd_emc-04 vita); „VBUS_SW In2 sík egyben” → 1 sziget (147,5 mm²), de 12 idegen In2 háló szeli, a táplálás és az U4 VIN-viák között csak ~0,24–0,30 mm-es zóna-kapcsolat – az áram a 0,5 mm-es In2 sávon és F/B linkeken folyik (U3.6 → U4.3 22,95 mΩ); „+3V3 … 28,4 mΩ” → 21,2 mΩ (raszteres DC-megoldó; a 28,4 csak sávokra számolt); BOM-jegyzet „F 48 / B 24” → **F 47 / B 25** (a C4 a B oldalra került).

**Maradó tételek (közepes / alacsony) – döntés**
| Súly | Tétel | Döntés |
|---|---|---|
| közepes | Rendelési csomag elavult; a jobb élre írt fül-tartomány a C3-ra esik (C3/R10/C1 0,7–0,8 mm-re a jobb éltől) | **rendelés előtt**: JLC sínek csak felül / alul; a jobb élen y > 5,8 és a felső élen x 10–35 között nincs fül; BOM + 72 soros CPL (tulajdonosi tételek) |
| közepes | J1 USB-C köpenylábak: paszta nélkül, `attr smd` → a JLC reflow a 4 lábat valószínűleg forrasztatlanul hagyja | **rendelés előtt döntés**: JLC kézi / szelektív forrasztás, vagy a tulajdonos forrasztja az első kábel-bedugás előtt (`05` §15) |
| közepes | U1 kézi forrasztás: C23.1 (+3V3) 0,525 mm-re a P87 (ESP_EN) padcsúcstól; C21–C23 0,5 mm-re a P83–86 csúcsoktól – híd = EN-késleltetés nincs, SW2 3V3–GND zárlat | **rev A elfogad + bring-up ellenőrzés**: finom kúpos hegy, P87/C23 szemle; TP16A ↔ TP4 ≈ 10k (0 Ω = híd) |
| közepes | Közös I2C csak a CH224A belső felhúzóival; a QOD 0 V-on tartja a CAM_3V3-at → a kamera clamp-diódái lehúzhatják a buszt | **FW-szabály + bring-up**: 100 kHz; PD-mód PG + ADC-ből; CH224A csak olvasás, csak a CAM_3V3 után; G1-en CFG2/CFG3 üresjárati fesz. ≤3,3 V; R31/R32 a G3 után; rev B: külön I2C láb |
| alacsony | R14.1 és R27.2 padjába 0,03 / 0,07 mm-rel belelógó via-furat (R14 szakadás → FB 0 V → a 3V3 VBUS_SW felé futhat) | **bring-up ellenőrzés**: 3V3_BUCK ↔ GND 5k–16k (>16k → R14/R15/R33); rev B: via áthelyezés |
| alacsony | U5 = TECH PUBLIC klón (C5350871), lábkiosztás nem igazolt | **rendelés előtt**: LCSC adatlap, pin 3 = GND; különben TI C1855726; bring-up: D+/D− ↔ GND |
| alacsony | J5 Hong Cheng pár (5,3 mm illesztett): 7,0 mm-nél ~2,3 mm merülés, generikus land (Q17) | **tulajdonosi döntés** (Q17); rev A bring-up a MAIN-nel önállóan |
| alacsony | J2 kontakt-oldal (Q6), JLC-készlet 31 db | készlet-foglalás; Q6 a kamera első bekapcsolása előtt (nem gyártás-blokkoló) |
| alacsony | Lógó +3V3 In2 csonk (4,54 mm, via_dangling 1) | rev A elfogad (opcionálisan törölhető + kapu újrafuttatás) |
| alacsony | R28 10k: GPIO 4 reset alatti felhúzásánál a TPS22917 ON 0,60–0,83 V lehet [NEM ELLENŐRZÖTT] | **bring-up ellenőrzés**: TP5 = 0 V reset alatt; opcionális BOM-csere 4,7k |
| alacsony | CSI adat–órajel skew ≈0,05 / 0,03 UI, CLK / D1 > 15 mm | rev A elfogad; **G5b soak teszt CSI hibaszámlálókkal** |
| alacsony | USB FS: D± B-szakaszai VBUS_SW / void felett, D+ T-csonk, hosszú U5 GND-visszaút | rev A elfogad (**csak FS, HS PHY soha**); rev B: GND via ≤0,5 mm az U5.3-hoz, D+ in-line |
| alacsony | Táp-elosztás maradékai (+3V3 egyes viák, VBUS_SW zónát 12 háló szeli, VBUS nyak, C14 DC-bias, nincs 100 nF az U3 IN-en, C24 6,26 mm, C2 2,79 mm) | rev A elfogad; opcionális BOM-csere C14 → 2,2 µF / 25 V X7R; rev B: 2× via rétegváltásonként, 100 nF az U3.5/U3.8-on |
| alacsony | Él-varrás rések, SDA / +3V3 0,52 mm-re az éltől, 0,24 mm-es GND_In2 szalag | rev A elfogad; rev B: ≥0,75 mm-rel beljebb, ≤4 mm-es kerítés, In2 keep-out x ≥ 43,9 |
| alacsony | Furattávolság: különböző háló 0,408 mm, azonos 0,253 mm (szabály 0,25 ✓) | rev A elfogad, hacsak a JLC DFM nem kifogásolja |
| alacsony | Szerelőfuratok: jelréz a csavarfej alatt (MH1/MH2 SDA 1,95 / 1,93 mm, MH4 SDA via 2,18 mm), B oldal DRC nélkül | rev A: mechanikai szabály (nylon, `05` §3); rev B: réz-tiltó gyűrű |
| alacsony | RF maradék: a KO_RF_In2 nem tilt nem-GND viát, a sávok / kerítés nincs zárolva, R34/J4 szemle hiányzott | **bring-up ellenőrzés**: R34/J4 GND-fillet szemle az U1 után; rev B: DRU-szabály + zárolás |
| alacsony | EMC/ESD maradék: ESP_EN RC 13,2 mm-re a P87-től; SDA / VBUS / USB_DM a J1 köpeny alatt B-n; C1 200 V (8 kV / 150 pF → ~247 V); CC-n nincs clamp | rev A elfogad; rev B: C25 ≤2 mm a P87-hez, J1 alatt nincs jel, 1206 / 1 kV C1, CC clamp |
| alacsony | Dokumentumok elavult állításai | **lezárva ebben a körben** (`05` §0.1, §3, §3.1, §3.1a, §4.1, §6, §13, §15; `06`; `07`; `08`) |
| info | Séma Value-mezők a rendelt névleges feszültség alatt (C1 „50V” → 200 V-os alkatrész, C9/C11/C12/C13/C20/C21); TH1 B = 3987 K | rev A elfogad (a `bom_jlc.csv` LCSC-szám szerint helyes); FW NTC-modell: B = 3987 K; rev B: mező-szinkron |
| info | L1 land pattern (generikus NR-50xx) vs NRS5024 rajz | rendeléskor JLC DFM / 3D előnézet |
| info | Kozmetika: hegyesszögű / mikro-szegmensek, In1 antipad 3,39 mm², MH lib-név, TP8A/TP16A annotáció, D20 ~0,5 mA (halvány) | rev B; opcionális R30 → 470 Ω |

**Tulajdonosi tételek**
1. **Rendelés előtti kapu** (a fenti 5 lépés) – egy agent futtathatja, de a tulajdonos lássa a sikeres eredményt; ennél korábbi Gerberből nem rendelünk.
2. **JLC rendelési űrlap:** 4 réteg, 45 × 45 mm (nem a gbrjob 45,1-e), 1,0 mm, stackup JLC04101H-3313A, impedancia-kontroll be, ENIG, tentelt viák, PCBA mindkét oldalon; sínek csak felül / alul, a jobb élen nincs fül (C3/R10/C1 0,7 mm-re); `bom_jlc.csv` + 72 soros CPL feltöltése.
3. **JLC elhelyezési előnézet:** forgatás és pin 1 ellenőrzése: U2, U3, U4, U5, U6, D1 (katód = VBUS), D20, J1, J2, J4, J5 és mind a 25 B-oldali alkatrész (offline nem igazolható).
4. **J1 köpenylábak:** JLC kézi / szelektív forrasztás rendelése, vagy saját forrasztás az első kábel-bedugás előtt.
5. **U5 (TECH PUBLIC C5350871):** LCSC-n pin 3 = GND ellenőrzése; ha nem igazolható → TI C1855726.
6. **Készlet-foglalás:** J2 C5164008 (31 db), U3 C3662799 (~300), R6 C22963 (180); Extended-díjak várhatók.
7. **Q6** (J2 kontakt-oldal + FFC): a valódi kamerával és kábellel, a kamera első bekapcsolása előtt – a NYÁK-gyártást nem blokkolja.
8. **Q17** (J5 magasság): Hong Cheng pár marad (MAIN változatlan; a FRONT aljzat-magassága korrigál, ~2,3 mm merülés 7,0 mm-nél) vagy Samtec 7,47 mm (MAIN lábkép-csere a rendelés előtt + 7,5 mm távtartó).
9. **Opcionális BOM-cserék azonos lábképen:** R28 → 4,7k, C14 → 2,2 µF / 25 V X7R, R30 → 470 Ω.
10. **U1 kézi forrasztás:** finom kúpos hegy a P83–P88-on, utána a P87/C23 rés és az R34/J4 forrasztás szemléje.
11. **Első táp előtti mérések:** TP16A (ESP_EN) ↔ TP4 (+3V3) ≈ 10k (0 Ω = híd); 3V3_BUCK ↔ GND 5k–16k (szakadt R14 esetén a buck ~9 V-ig futhat); VBUS ↔ VBUS_SW ≈ 300k (JP1 nyitott); VBUS / D+ / D− ↔ GND nem zárlatos.
12. **Rev A firmware-szabályok:** I2C 100 kHz; PD-mód a PG + ADC-ből, a CH224A-t csak a CAM_3V3 bekapcsolása után olvasni, soha nem írni; IR_SW_EN alacsonyan; az USB HS PHY-t ezen a layouton soha nem engedélyezni.
13. **Mechanika:** nylon távtartó vagy nylon alátét az MH1/2/4-en; az MH3-on nincs alátét, csavarfej max. Ø4,0 mm, az u.FL kábel Ny/É felé lép ki.
14. **Elfogadott rev A eltérések (aláírás):** D1 TVS az eFuse-nál, nem a J1-nél; CSI skew ≈0,05 UI, CLK 21,4 mm; USB FS VBUS_SW / void referencián; egyes viák a +3V3 trönkön; él-kerítés rések; J2 / SD / CC ESD rev B-ben.
15. **Rendelés után:** a dokumentumok as-built frissítése (`05` / `06` / `07` / `90`) és a CSI hibaszámlálós soak teszt a `05` §15-ben – **elvégezve 2026-10-11** (ez a bejegyzés és a kapcsolódó doc-frissítés).

Nem mérve: hőviszonyok, a buck hurokstabilitása, a valós áramkeret, a JLC élő képességei, készlet és CPL-forgatások, a modul alsó oldala, a klón- / csatlakozó-adatlapok (offline nem elérhetők).
