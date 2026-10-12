> ⚠️ Kutatási jegyzet (2026-10-09). Ahol ellentmond a 05-architektura.md-nek, a 05 érvényes. Ismert elavult pontok: I2S mikrofon helyett PDM MEMS (E-16, F-7); 470 µF VBUS kapacitás törölve – ≤10 µF a csatlakozónál + eFuse soft start (E-2); VDDPST_5 külső 3,3 V helyett VO4 → 3,3 V firmware-ből, kapcsolt SD_3V3 felhúzásokkal (E-3, E-4); SD slot0 lábak „emlékezetből” – E17 igazolja; SY8089/PTC/SMBJ5.0A elavult (E-1, E-13, P-26); LDR/fényérzékelő helyett kamera AE (E-21); WS2812 helyett diszkrét LED (E-34); reset RC nyitott (E-22); USB-C 5 V only helyett PD sink 9 V (K7); I2S/USB elavult állítások (E-36); a „2 rétegű panel” megszorítások a MAIN-re elavultak (MAIN v0.6: 4 réteg, 45×45, 00 K4); a gombok/LED/SD-vezérlés tényleges kiosztása a 05 §5 / §3.1a szerint (pl. SD_EN = GPIO 53, USER = GPIO 33, státusz LED = GPIO 6).

# 04 – Perifériák: microSD, mikrofon, IR éjjellátó, gombok/LED, tápellátás

Státusz: kutatási vázlat. Jelölések: **[ELLENŐRZÖTT]** = webes elsődleges forrás alapján (a keresés találataiból); **[NEM ELLENŐRZÖTT]** = memóriából / tipikus érték, schematic előtt ellenőrizendő.

A WebSearch működött (ESP-IDF docs találatok), de a WebFetch egy helyi hook hiba miatt blokkolt (hook interpreter nem található), ezért az EV board kapcsolási rajzát, a gyártói datasheeteket és az LCSC készletet NEM sikerült megnyitni. Minden alkatrészszám és áram-érték emiatt [NEM ELLENŐRZÖTT], kivéve ahol jelölve van.

---

## 1. microSD

### 1.1 SDMMC host slotok
- A P4-nek 2 SDMMC slotja van. Az ESP-IDF v5.4/5.5 dokumentáció szerint a slot 1 a nem-UHS-I használatra való, a slot 0 UHS-I-hez van fenntartva (a driver UHS-I-t még nem támogatja) **[ELLENŐRZÖTT – keresési kivonat]**.
- Eltérő források: a keresési találatok szerint az újabb dokumentáció a GPIO-mátrixot említi mindkét slotra, egy régebbi dokumentáció-változat fix IO_MUX kiosztást ír. Közösségi/Arduino PR források szerint az EV boardon a **slot 0 az SD kártya, a slot 1 a C6 SDIO** kapcsolata **[részben ellenőrzött – harmadik fél]**.
- Emlékezetből (**[NEM ELLENŐRZÖTT]**): slot 0 fix IO_MUX lábai GPIO39–44 (D0=39, D1=40, D2=41, D3=42, CLK=43, CMD=44), a VDDPST_5 (VDD_IO_5) tápdomainben; ez az a domain, amelyet az on-chip LDO (LDO_VO4 – pontos szám ellenőrizendő) tud 3.3 V / 1.8 V között táplálni UHS-I-hez. Slot 1 a GPIO-mátrixon bármely lábra rakható; az EV boardon a C6 SDIO ott fut (CLK=18, CMD=19, D0–D3=14–17, C6 reset=54 – **[NEM ELLENŐRZÖTT]**, a P4-pinout agent anyagával keresztellenőrizni).
- Következmény a projektre: ha a C6 SDIO-ja slot 1 (GPIO-mátrix), akkor az SD kártya a **slot 0**-ra kerül (fix lábak, 2 rétegű panelen is egyszerű vezetés, mert a lábak egymás mellett vannak). Ez nem ütközik. Ha a C6-ot SPI-ra tennénk, a slot 1 szabad lenne, de az SDIO a gyorsabb (esp-hosted-nél ajánlott).

### 1.2 IO feszültség
- A P4-nek külső tápot kell adni a VDDPST_5 (SD_VREF) lábra, ha nincs LDO-ból táplálva; UHS-I nélkül 3.3 V-ra köthető **[ELLENŐRZÖTT – keresési kivonat]**.
- Javaslat: 3.3 V-os kártya, nincs 1.8 V-os átkapcsolás (nincs UHS-I) → VDDPST_5 = 3.3 V fix. Egyszerűbb, és a throughput 4-bit High-Speed módban (50 MHz, ~20–25 MB/s elméleti) bőven elég egy 1080p MJPEG/H.264 felvételhez. Az on-chip LDO-s 1.8 V opció csak UHS-I-hez kellene.
- Kártyatáp: 3.3 V-ról **load switch**-en át (lásd 1.4), hogy hibás kártya-állapotból áramtalanítással lehessen visszatérni (power-cycle).

### 1.3 4-bit vs SPI
- **4-bit SDMMC javasolt** (slot 0, fix lábak). SPI mód lassabb és a P4 SDMMC hardveréből nincs hasznos nyereség. SD üzemmódhoz CMD és D0–D3 felhúzó kell: **10 kΩ** (külső, ne csak a belső ~45 kΩ). CLK-ra nem kell felhúzó; soros 22–33 Ω a CLK-ra opcionális (EMI, 2 rétegnél hasznos).
- Boot-strapping figyelem: ellenőrizni, hogy a GPIO39–44 egyike sem strapping láb **[NEM ELLENŐRZÖTT]**.

### 1.4 Alkatrészek (mind [NEM ELLENŐRZÖTT] az LCSC készletre)
| Funkció | Javaslat | Megjegyzés |
|---|---|---|
| microSD foglalat, push-push, SMD, kártya-detekt (CD) kapcsolóval | TF-01A (HRO / Korean Hroparts) vagy "TF-015" kategória (LCSC-n több, ~C91145 jellegű) | A pontos C-szám ellenőrizendő; a JLCPCB extended parts között több push-push típus van. Hand-solder: kézi forrasztáshoz a lábak oldalt vannak, 1.0 mm-es raszterrel |
| Load switch | TPS22918 (SOT-23-5) vagy SY6280 / "AP2552" | 3.3 V, ≥300 mA, vezérlés GPIO; ON-ra 10 µs–ms soft start. SD kártya csúcs ~100–200 mA írásnál |
| ESD | USBLC6-4SC6 (SOT-23-6) vagy 4-5 csatornás TVS-array (pl. IP4234CZ6 / "ESDA6V1") a CMD/CLK/D0–D3 vonalakra | Max kapacitás <~10 pF, hogy ne rontsa a 50 MHz jelet |
| Felhúzók | 6× 10 kΩ 0402 | CMD, D0–D3; CD külön felhúzó |
| Táp-pufferelés | 10 µF + 100 nF a kártya VDD-nél | Írási tüske miatt |

- Card detect: a foglalat CD-kapcsolója → GPIO, 10 kΩ felhúzóval (aktív alacsony); P4 oldalon bármely GPIO.
- A kártya foglalat helye: panel szélén, a kártya kihúzhatóan hozzáférhető a ház falán.

---

## 2. Mikrofon

### 2.1 Interfész választás
- Az ESP-IDF I2S dokumentáció szerint a P4-en **PDM RX az I2S0-n érhető el** (a standard és TDM mód I2S0–2 mind), és csak 1 vezérlőn **[ELLENŐRZÖTT – keresési kivonat, v5.4.x]**. A PDM busz: CLK + DIN (1 adatvonal). Megjegyzés: a v5.2/5.3 doksi 1 I2S periféria, v5.4+ háromról ír – a P4 esetén a 3 I2S a helyes (újabb IDF) **[ellentmondás a forrásokban]**.
- Két út:
  1. **PDM MEMS** (pl. MSM261D3526H1CPM – PDM, 2.7 mm × 1.9 mm × 0.9 mm → inkább a MSM261S4030H0 I2S változat; vagy SPH0641LU4H-1, vagy MP34DT05): 2 vezeték (CLK, DAT), 1.8–3.3 V, nagyon olcsó. Hátrány: PDM→PCM szűrés a P4 hardverében (I2S0 PDM RX), a P4-ben az I2S0 PDM RX használata más I2S-igényt blokkolhat (lásd lent). Jellemzően 1.6–3.6 V.
  2. **I2S MEMS** (INMP441 – 3.3 V-os, 24-bit I2S, LGA-14, forrasztása kézzel nehéz; ICS-43434; MSM261S4030H0 – PCM/I2S kimenet, JLCPCB-n gyakori): 3 vezeték (BCLK, WS, SD) + L/R választó láb. Standard I2S RX → nincs PDM-szűrő-kérdés.
- **Javaslat:** I2S MEMS, mert (a) szabványos I2S RX driver, mindkét periféria használható, (b) nincs PDM-aliasing/szűrés a firmware-ben, (c) egyszerűbb vezetés zajos 2 rétegű panelen is. Konkrét típus: **MSM261S4030H0R** (LCSC jellegű, olcsó, "bottom-port" 4.72×3.76 mm) – [NEM ELLENŐRZÖTT], vagy ICS-43434 (TDK, drágább, jobb SNR). INMP441-et kerülném (LGA-14, nehéz kézi forrasztás, EOL-közeli).
- Ha mégis PDM: PDM MEMS 1.8 V domainről is mehet, de a P4 jelszintje 3.3 V a legtöbb GPIO-n; MSM261D3526 3.3 V-on is működik **[NEM ELLENŐRZÖTT]**.

### 2.2 P4 lábak
- I2S RX: BCLK, WS, DIN = 3 GPIO (GPIO-mátrixon szabadon választható – ellenőrizendő a P4-pinout anyagban, hogy az I2S lábak IO_MUX-on is vannak-e). PDM esetén 2 GPIO (CLK, DAT). Nem szükséges MCLK MEMS-hez.
- Ha az audió kimenet (hangszóró) nem kell, csak RX.

### 2.3 Akusztikai port
- Bottom-port MEMS: a NYÁK-on lyuk (0.5–1.0 mm, a gyártó ajánlása szerint) a mikrofon alatt, a ház elülső vagy oldalfalán akusztikai nyílás; tömítés (gumigyűrű/ragasztógyűrű) a ház és a NYÁK között a hangbeszivárgás ellen.
- Top-port MEMS esetén a lyuk a házon van, a NYÁK-on nincs kivágás. Minimum 3–4 mm távolság a ventilátor/DC-DC induktortól; a mikrofontáp külön LC/ferrit-szűrős (10 µF + 100 nF + ferrit), mert a WiFi TX burst (217 Hz GSM-szerű "TDMA-zaj" nem releváns, de a buck switching zaja igen).
- 2 rétegen: a mikrofon fölött/alatt ne fusson digitális jelvezeték, az I2S vonalak rövidek legyenek, földsík folytonos.

---

## 3. IR éjjellátó

### 3.1 IR-cut szűrő (ICR) kezelés
- A kamera-modulok (OV5640 ICR-es változatai, ill. M12 objektíves modulok) mechanikus IR-cut szűrője általában **kétvezetékes bistabil tekercs**: egy +/− polaritású impulzus (~50–100 ms, ~5 V / 60–120 mA) húzza be az IR-cut szűrőt (nappal), ellenkező polaritású impulzus kiveszi (éjjel). A kapcsolt állapotot nem kell tartani.
- Szükséges: **H-híd** (két félhíd), 2 GPIO a P4-ről. Opciók **[NEM ELLENŐRZÖTT]**:
  - **DRV8833** (HTSSOP-16/WQFN, kis dual H-bridge, 1.5 A/csatorna): túlméretezett, de elterjedt, LCSC-n kapható.
  - **BA6208** (SOP-8): tipikusan IP-kamerákban használt ICR-meghajtó; olcsó, de a kapható készlet bizonytalan.
  - **DRV8837 / DRV8838** (WSON-6/ SOT) kisebb; vagy
  - **diszkrét megoldás**: 2× komplementer MOSFET-pár (pl. 2× AO3401 + 2× AO3400 hajtva, vagy 2 db "CJ3134K" félhíd) + 4 védődióda – sok alkatrész; egy dual half-bridge IC kevesebb hely.
  - **Legegyszerűbb:** 2 db ULN-szerű vagy 1× "FM116B"-típusú IC; vagy egy `SGM2xx`-szerű "motor driver". A pontos darabot a LCSC készlet alapján a következő iterációban válasszuk.
- A tekercs induktív: **szabadonfutó/TVS diódák** (SS14 vagy a H-híd IC beépített védelme).
- Impulzus alatt a 5 V sín megugrik ~100 mA-rel; 100 µF fojtó (bulk) kondenzátor ajánlott.
- A projekt kérdése: van-e ICR a kiválasztott kamera modulon? A kamera-agent anyagával egyeztetni (sok OV5640 modulon nincs mechanikus ICR; ilyenkor "IR-érzékeny / no-IR-cut" modul + IR LED-ek elegendők, nappal színeltolódással).

### 3.2 IR LED hullámhossz
- **850 nm**: gyenge vörös izzás látható (a LED-ek enyhén világítanak), de ~2–3× jobb érzékenység CMOS-szenzorokon (OV5640 QE 850 nm-en jobb, mint 940-en). Jó választás távolabbi megvilágításhoz.
- **940 nm**: láthatatlan, de a szenzor érzékenysége 940 nm-en jóval kisebb (kb. 1/3–1/2 a 850 nm-hez képest) → több LED/áram kell ugyanahhoz a fényhez.
- **Javaslat:** 850 nm, 3–6 db 5 mm-es / 3535 SMD LED (pl. OSRAM SFH 4235 / "Everlight IR333"), ill. LCSC-s 850 nm 3535 SMD típusok; max ~20 cm–3 m hatótáv szoba-megfigyeléshez. [NEM ELLENŐRZÖTT – konkrét alkatrészszám]

### 3.3 Meghajtás és PWM
- 850 nm IR LED Vf ≈ 1.4–1.6 V @ 100 mA. 5 V-ról **2 LED sorosan + soros ellenállás** (Vf ≈ 3 V → 2 V esik az ellenálláson, 100 mA-hez ~20 Ω) vagy 3 LED sorosan (4.5 V – feszültség-tartalék kevés, USB-feszültség esés miatt nem javasolt).
- **Egyszerű:** 2 × (2 LED + ellenállás) párhuzamos ágak, **alacsony oldali N-MOSFET** (pl. AO3400/ 2N7002 / SI2302), a gate-et a P4 GPIO-ja PWM-mel (LEDC) hajtja; ellenállás áramkorlátoz. Áramstabilitás gyenge (Vf hőfüggés, 5 V ingadozás), de ez IR segédfényhez elfogadható.
- **Jobb:** konstans-áramú LED-meghajtó, pl. **AL8860** (buck, 1 A, SOT-89/SOT-23-5 változat), **AP3012**, **PT4115**; vagy lineáris CC-meghajtó (pl. **AL5809 / AL8805**). Előnye: PWM-dimming pin (DIM/ADJ) közvetlenül a GPIO-ról, áram független a tápfeszültségtől. A buck IC induktort igényel, ami zajt és helyet jelent egy 2 rétegű, kis panelen – ezért az egyszerű ellenállásos/MOSFET megoldás az első prototípusra.
- PWM frekvencia: ≥ 1 kHz, kamera-rolling-shutter bandingot kerülendő: vagy DC (PWM nélkül), vagy 20 kHz+ PWM. A kamera exposure-ral összefüggő csíkok ellen a LED legyen folyamatosan (nem szinkronizált PWM <1 kHz).
- Világos/sötét érzékelés: a) **LTR-303ALS / VEML7700 / BH1750** I2C fényérzékelő (a P4 I2C-n már van SCCB a kamerához – külön I2C busz ajánlott a szenzorhoz, ill. megosztható a 7-bit címek miatt); b) **LDR + osztó → ADC** (olcsó, de kalibráció kell, a P4 ADC-lábai ellenőrizendők). c) **Alternatíva:** nincs külön szenzor – a kamera auto-exposure/AGC értékéből (OV5640 regiszterek) vagy a frame átlagfényességéből döntsön a firmware. Ez a legkevesebb hardver, javasolt kiindulás; az ambient szenzor opcionális. [NEM ELLENŐRZÖTT]
- Ügyelni: az IR LED fénye a szenzor ablak mögött visszaverődik (glare) – a LED-ek optikailag el kell legyenek szigetelve a lencsétől (fekete gyűrű/sötét válaszfal).

### 3.4 Áramkeret USB-C 5 V-on
- Csak 2× 5.1 kΩ Rd-vel a forrás **nem tudja, mennyit kérhetünk**: egy USB-C portnak legalább **500 mA (USB 2.0) / 900 mA (USB 3.x)** alapérték van; a **Rd-vel a source "Default USB power" módban marad**, vagyis tipikusan 500 mA (régi USB-A–C kábel, USB-A host). Ha a source 1.5 A vagy 3 A-t hirdet Rp-vel, az Rd-ből a feszültség-szint ezt jelzi, de a sink (mi) az áramot a CC-feszültségből nem olvassa ki, csak feltételezi. Vagyis a TERVEZÉSI BIZTOS határ = **500 mA** (USB 2.0 default), a 900 mA–1.5 A–3 A csak "ha a töltő képes" – hasonló egyszerű, Rd-s kameráknál elterjedt, de a tápból való lekapcsolás (brown-out) kockázatot jelent. [Forrás: USB-C specifikáció, emlékezetből – NEM ELLENŐRZÖTT.]
- Következmény: az IR LED-ek átlagárama a költségvetésben ~ **100–200 mA** legyen; csúcsban max 300 mA (rövid ideig). Ha a teljes rendszer csúcsa 500 mA fölé megy, USB-C PD/CC-detekció (pl. egy "CC-logika IC", FUSB302/STUSB4500 – 5 V/1.5 A-t kér-ellenőriz) vagy lágy áramkorlát (LED-et visszavenni WiFi TX alatt) kell.
- Termikus: 2–4 LED × 100 mA × 1.5 V = 0.3–0.6 W a LED-eken + 0.4–0.5 W az ellenállásokon (ha 5 V-ról ellenállással). Összesen ~1 W, kis zárt házban 10–15 °C emelkedés. A P4 + C6 + kamera együtt ~1–2 W: **a ház hőmérséklete (OV5640 zaj nő)** és a LED élettartama szempont. A buck-os CC-driver hatásfoka jobb (~85–90%), az ellenállásos ~60%. Termikus via-k és réz felület a hőelvezetésre.

---

## 4. Gombok és státusz LED

| Elem | Javaslat | Megjegyzés |
|---|---|---|
| BOOT (GPIO35, strapping – P4: boot mód) | Tact switch 3×4×2 mm SMD (pl. "TS-1187A" jellegű) | P4-nél a download-boot strapping láb **GPIO35** [NEM ELLENŐRZÖTT – ellenőrizendő a P4-pinout agenttel]; 10 kΩ felhúzó + gomb a GND-re |
| RESET (CHIP_PU/EN) | Tact switch + 100 nF kondi + 10 kΩ felhúzó (RC) | Auto-reset, USB-s programozás esetén a soros USB-JTAG/Serial (P4-nek natív USB 2.0 OTG HS és USB-Serial-JTAG van [NEM ELLENŐRZÖTT]) |
| User gomb | Tact switch → GPIO, belső felhúzó vagy 10 kΩ, 100 nF debounce | Pl. WiFi-provisioning / factory reset (hosszú nyomás) |
| Státusz LED | **Egyszerű 0603 LED-ek** (zöld/piros, 1 kΩ-os előtét) vagy **WS2812B-2020 / SK6812 mini** | WS2812: 1 GPIO, de 5 V-os adatjelszint kell (3.3 V GPIO-ról a legtöbb WS2812B nem megbízható; SK6812 mini-e vagy WS2812B-2020 3.3 V-os adat is elmegy, ha a táp 4–5 V – [NEM ELLENŐRZÖTT]); alternatíva: 74LVC1T45 szintillesztő. RGB LED áram ~5–10 mA egyenként → 20–30 mA a költségvetésben |

- Javaslat: **1 db egyszínű/RGB egyszerű LED** (3 GPIO PWM-mel, vagy 1 db 2 színű), vagy WS2812-2020 egy GPIO-val; a kisebb bonyolultság a diszkrét 0603 LED-ek. Ha 2 rétegű, kevés láb van, a WS2812 GPIO-takarékos.
- A BOOT/RESET gombok a panel szélén, ház-nyílással, "pinhole" reset ajánlott a véletlen resetek ellen.

---

## 5. Tápfa (USB-C 5 V)

### 5.1 Bemenet
- **USB-C receptacle, 16 pólusú** (USB 2.0-only, pl. HRO TYPE-C-31-M-12 / "TYPE-C 16P" – LCSC-n gyakori, JLCPCB extended), 2× **5.1 kΩ** CC1/CC2 → GND (Rd). Csak 5 V, nincs PD. A D+/D− az ESP32-P4 USB 2.0 HS (OTG) PHY-ra / programozásra vezetve (P4-pinout agenttel egyeztetve), 22 Ω soros nem kell, de ESD igen.
- **Védelem:**
  - Polyfuse (PTC) 1.1–1.5 A hold (pl. 1206L110) **vagy** eFuse (pl. TPS2553/TPS259xx, vagy olcsóbb "SY6280"-féle áramkorlátozó load switch) → az eFuse pontos áramkorlát (pl. 1.0 A), túlfeszültség/vissza-folyás védelem is. Az 500 mA default miatt akár 700 mA-es áramkorlát is szóba jöhet.
  - **TVS:** SMBJ5.0A (nagy, 600 W – túlméretezett, ugyanakkor erős lökés ellen) vagy kisebb SMAJ5.0A / ESD9B5.0 / "PESD5V0" a VBUS-on; ESD-array (USBLC6-2SC6) a D+/D−-ra és a CC lábakra.
  - Bemeneti kapacitás: 10–22 µF kerámia + 100 µF bulk (hot-plug tüske csillapítására soros ferrit/RC, a USB-C hot-plug ringing miatt).
  - Fordított polaritás: USB-C-nél nem szükséges.

### 5.2 3.3 V sín (fő)
- Buck 5 V → 3.3 V, ≥2 A (a WiFi TX csúcs miatt, ~1.5–2 A névleges tartalék). Opciók **[NEM ELLENŐRZÖTT – LCSC készlet]**:
  - **SY8089** (SOT-23-5, 2 A, 2.7–5.5 V be, egyszerű, JLCPCB-n gyakori, olcsó). Jó első választás.
  - **TPS62A02** (SOT-583/ 2 A, 6-pin, nagyon kicsi, de drágább, kisebb induktor 1 µH).
  - **MP2143 / MP2161** (2 A, 3-pin kis) – ugyanilyen osztály.
  - Induktor 2.2 µH, ≥3 A telítés, árnyékolt (pl. 4×4 mm); kimenet 22 µF ×2.
- 2 rétegen: a buck hurkot (be-C, IC, induktor) a panel egyik sarkában, rövid hurokkal, a mikrofontól és a kamerától távol; a földsík megszakítás nélküli.

### 5.3 A P4 saját tápsínjai (keresztellenőrzés a P4-pinout agenttel!)
- Az ESP32-P4 **VDD_HP/core** feszültséget **a chip belső (integrált) szabályozója** állítja elő? A P4 hivatalos hardvertervezési útmutatója szerint a chip **külső 3.3 V-ot** (VDDA, VDD_DIG-IO, VDD_FLASH) kér, és a core-feszültség a belső DCDC/LDO-ból jön – a **P4 belső DCDC** (VDD_HP-hoz) külső induktort igényelhet [NEM ELLENŐRZÖTT – kritikus, a hardveres designguide elolvasandó!]. Megjegyzés: az ESP32-P4-Function-EV-Board kapcsolási rajzán egy külön PMIC/DCDC ('VDD_HP' ellátás) és a chip LDO-i (pl. VDD_PSRAM/VDD_MIPI 1.8 V / 2.5 V) láthatók – ezt a rajzot meg kell nyitni, mielőtt a tápfát lezárjuk.
- Belső LDO-k (emlékezetből, [NEM ELLENŐRZÖTT]): LDO_VO1..4 – az egyik a MIPI-DSI/CSI PHY analóg tápja (VDD_MIPI_DPHY 2.5 V a belső LDO-ról), egy másik a VDDPST_5 (SD) 1.8 V/3.3 V, egy a PSRAM/flash. Ezek a belső LDO-k külső kondenzátort igényelnek.
- Beépített PSRAM/flash: a P4 modul (ESP32-P4 "Function" chip) PSRAM-ot csomagban tartalmaz (16/32 MB); külső SPI flash 3.3 V vagy 1.8 V (verziófüggő) – a P4-pinout agens.

### 5.4 Kamera sínek (OV5640)
- Tipikus OV5640: **AVDD 2.8 V** (analóg, zajérzékeny), **DVDD 1.5 V** (core; sok modulon beépített LDO), **DOVDD 1.8 V** (IO) vagy 2.8 V. MIPI CSI a P4-en: az IO-szint ~1.8 V.
- LDO-k: **ME6211C28** (2.8 V, 500 mA, SOT-23-5) és **ME6211C18** (1.8 V); DVDD 1.5 V: **ME6211C15** vagy RT9013-15; mindhárom megvan az LCSC-n (ME6211 sorozat JLCPCB basic/extended). **Rögzített feszültségű változatok**, 1 µF–2.2 µF bemeneti/kimeneti kerámia. AVDD-hez külön LDO (kis zaj) és ferrit. A kamera-agent anyagával egyeztetni: ha csatlakozós, kész **kamera modul** (FPC) van, a modul tipikusan 3.3 V-ot vagy 2.8 V-ot kér, és tartalmaz LDO-kat.
- Sorrend (power-up sequencing): OV5640 datasheet: AVDD → DVDD → DOVDD sorrend/ PWDN/RESET lábak – a SOT-23-5 LDO-k EN lábai a P4 GPIO-ja vagy RC-késleltetésű; [NEM ELLENŐRZÖTT – a kamera agent anyaga].

### 5.5 Áramköltségvetés (BECSLÉS – mind [NEM ELLENŐRZÖTT])
| Fogyasztó | Átlag (mA @ 5 V-ra vetítve, ~85% hatásfok) | Csúcs | Megjegyzés |
|---|---|---|---|
| ESP32-P4 (streaming, 1080p kódolás, 2×400 MHz + PSRAM) | ~250–350 | ~450 | Becsült; mérés kell. A P4 saját számok a hivatalos datasheetben (TX/RX/aktív mód) – ellenőrizendő |
| ESP32-C6 (WiFi 6 TX átlag/csúcs) | ~80–120 | ~350 (TX csúcs, 3.3 V) | A 350 mA a feladatban megadott TX csúcs; 5 V-os oldalon ~230 mA |
| Kamera modul (OV5640 + MIPI) | ~120–150 (3.3 V-on ~150 mA) | ~180 | Becsült |
| microSD (írás) | ~50–100 (3.3 V-on) | ~150–200 | Becsült; 4-bit írás csúcs |
| Mikrofon, gombok, LED | ~5–30 | ~40 | WS2812 RGB: +20–30 mA |
| IR LED-ek (850 nm, 2–4 LED) | 0 (nappal) / 100–200 (éjjel) | 300 | A fő változó; lásd 3.4 |
| Buck veszteség, ICR impulzus | beleszámítva | +100 mA (<100 ms) | |
| **Összeg (nappal)** | **~450–650 mA @ 5 V** | ~800–900 mA | **Az 500 mA default USB-limitet átléphetjük!** |
| **Összeg (éjjel, IR-rel)** | **~600–850 mA** | ~1.1 A | 1.5 A-s töltő kell |

- Következmény: a rendszer **tipikusan 500 mA fölé megy** egy USB 2.0 portról. Javasolt: (1) USB-C töltőről (5 V/≥1.5 A) üzemeltetni, (2) a dokumentációban rögzíteni a minimum töltőt (5 V/2 A), (3) firmware-ben az IR LED-et a WiFi TX terhelés mellett korlátozni, (4) a bemeneten ≥470 µF/low-ESR bulk a TX burstökre és a hot-plug-ra.

---

## Források (Források)
- SDMMC Host Driver, ESP32-P4 (v5.5.x): https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32p4/api-reference/peripherals/sdmmc_host.html (keresési kivonat; a lap tartalma nem lett megnyitva)
- SDMMC Host Driver, ESP32-P4 (v5.4): https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32p4/api-reference/peripherals/sdmmc_host.html
- Régebbi sdmmc_host.rst (GitHub, fix IO_MUX kiosztás eltérő változat): https://github.com/espressif/esp-idf/blob/636ff35b/docs/en/api-reference/peripherals/sdmmc_host.rst
- Arduino-ESP32 PR (P4 EV board, SD = slot 0, C6 SDIO = slot 1): https://github.com/espressif/arduino-esp32/pull/10460
- I2S driver, ESP32-P4 (v5.4.x, PDM RX csak I2S0): https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32p4/api-reference/peripherals/i2s.html
- Nem sikerült megnyitni (WebFetch hook hiba): ESP32-P4 datasheet / hardware design guide, ESP32-P4-Function-EV-Board schematic, LCSC/JLCPCB készlet, gyártói datasheetek (SY8089, TPS62A02, ME6211, DRV8833, AL8860, MSM261S4030H0).

## Nyitott kérdések / kockázatok
1. **EV board kapcsolási rajz** (ESP32-P4-Function-EV-Board) megnyitása: SD slot 0 pontos lábai, VDDPST_5 táplálás (on-chip LDO vs külső 3.3 V), C6 SDIO láb-kiosztás – [NEM ELLENŐRZÖTT] minden itt megadott GPIO-szám.
2. **P4 core-tápellátás**: kell-e külső induktor / DCDC (VDD_HP)? A hardware design guide alapján kötelezően ellenőrizendő a tápfa lezárása előtt (a P4-pinout agenttel).
3. **USB-C áramkorlát**: Rd-only → 500 mA default; a becsült fogyasztás ezt meghaladhatja. Döntés kell: csak ≥1.5 A töltővel használható, vagy CC-detektáló/PD-sink IC.
4. **Mérési adatok hiányoznak**: P4 streaming áram, C6 átlag/TX csúcs, kamera áram, SD áram – a táblázat becslés.
5. **ICR megléte** a választott kamera modulon (sok OV5640 modulon nincs mechanikus ICR). Ha nincs, a H-híd elhagyható.
6. **PDM vs I2S**: P4-en a PDM RX csak I2S0 (v5.4 doksi szerint); I2S MEMS javasolt. IDF-verziók közt ellentmondó I2S-szám (1 vs 3) – ellenőrizendő az aktuális IDF-ben.
7. **WS2812 3.3 V adatjelszint**: megbízhatatlan 3.3 V GPIO-ról; szintillesztő vagy 3.3 V-kompatibilis LED.
8. **Termikus**: zárt házban a P4 + IR LED + buck ~1.5–2 W; az OV5640 zajszintje és a LED élettartama; hőelvezetés 2 rétegen korlátozott.
9. **2 rétegű PCB**: SD 4-bit 50 MHz, I2S és buck zaj vezetése; a mikrofon és a kamera AVDD zajérzékeny a buck közelében.
10. **LCSC/JLCPCB készlet és C-számok** nem ellenőrizve: minden alkatrészszámot a végleges BOM előtt ellenőrizni kell.
