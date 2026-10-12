> ⚠️ Kutatási jegyzet (2026-10-09). Ahol ellentmond a 05-architektura.md-nek, a 05 érvényes. Ismert elavult pontok: külön C6 modul helyett a Waveshare modulon belüli C6H8 (F-10); P4 USB OTG HS = GPIO20/21 és az SDIO lábkiosztás (CMD18/CLK19/D0 20…) hibás – E18: CLK=18, CMD=19, D0=14, D1=15; GPIO20/21 = ADC (F-9); egyetlen USB-C (GPIO24/25); LiPo/akku és PTC+SY8089 (5,5 V-os buck) elavult – PD + eFuse + széles bemenetű buck (E-1, E-2, E-13); C6 programozás: C6_EN (GPIO54) + IO9 pad, OTA (05 §10).

# ESP32-C6 koprocesszor, P4<->C6 kapcsolat, programozás és tápellátás

> **FIGYELEM – források állapota:** a kutatás során a WebFetch eszközt egy helyi governance hook blokkolta (hibás node-útvonal), a WebSearch pedig csak általános találatokat adott (nem hozta le a pin-táblázatokat). Ezért az alábbi konkrét számok (GPIO-k, méretek, áramok) **a modell tanult tudásából származnak**, és ahol nem volt elsődleges forrással megerősítve, **[NEM ELLENŐRZÖTT]** jelölést kapnak. A kapcsolási rajz véglegesítése előtt KÖTELEZŐ ellenőrizni az "Források" szekció dokumentumaival (különösen az EV-board sematikával és a C6 datasheet-tel).

## 1. ESP32-C6 modul opciók

| Modul | Méret (kb.) | Antenna | Megjegyzés |
|---|---|---|---|
| ESP32-C6-MINI-1 | ~13,2 x 16,6 x 2,4 mm [NEM ELLENŐRZÖTT] | PCB (on-board) | legkisebb, antennás; keep-out a PCB-antenna alatt/mellett |
| ESP32-C6-MINI-1U | ~13,2 x 12,5 x 2,4 mm [NEM ELLENŐRZÖTT] | u.FL | legkisebb, külső antennával |
| ESP32-C6-WROOM-1 | ~18 x 25,5 x 3,2 mm [NEM ELLENŐRZÖTT] | PCB | nagyobb, több flash opció |
| ESP32-C6-WROOM-1U | ~18 x 19,2 x 3,2 mm [NEM ELLENŐRZÖTT] | u.FL | |
| Csupasz chip (QFN40) | 5x5 mm | külső | RF illesztés, kristály, flash, 4+ réteg ajánlott; **2 rétegen kerülendő** |

**Keep-out (általános Espressif szabály):** PCB-antennás modulnál az antennarész alatt és körül (kb. 15 mm az antenna végétől oldalirányban, a modul antennás oldalán) **nincs réz, nincs alkatrész, nincs via**, és a modul antennás vége a panel szélén/túl lógjon. Az antenna ne kerüljön fém ház, akku, kamera-flex vagy FPC közelébe (min. ~15 mm). [pontos értékek: NEM ELLENŐRZÖTT – lásd modul datasheet "Placement" ábra]. A földsík a modul alatt (nem az antennarész alatt) folytonos legyen.

**Ajánlás kompakt kamerához:** **ESP32-C6-MINI-1** (PCB-antenna, legkisebb lábnyom, nincs RF-layout), ha a panel szélén biztosítható a keep-out. Ha műanyag/fém ház vagy halmozott panelek zavarják az antennát: **MINI-1U + u.FL pigtail + kis FPC/chip antenna a házon**. Modul = az RF-illesztés, kristály és flash gyárilag kész, ezért 2 rétegen is megvalósítható.

## 2. P4 <-> C6 kapcsolat (esp-hosted-mcu)

Az ESP32-P4-nek nincs rádiója; Wi-Fi/BLE az `esp-hosted-mcu` + `esp_wifi_remote` komponenssel a C6-on keresztül érhető el (a C6 "slave" firmware-t futtat).

| Transzport | Jelek | Megjegyzés |
|---|---|---|
| **SDIO 4 bites** (ajánlott, az EV board is ezt használja) | CLK, CMD, D0-D3 + reset (+ opcionális handshake/data-ready) | legnagyobb sebesség; a gyakorlati áteresztés a C6 2,4 GHz Wi-Fi6 20 MHz-es kapcsolatát (~40-60 Mbit/s valós) simán kiszolgálja [NEM ELLENŐRZÖTT] |
| SDIO 1 bites | CLK, CMD, D0 | kevesebb vezeték, kisebb sebesség; stacked csatlakozón kevesebb pin |
| SPI | CLK, MOSI, MISO, CS, handshake, data-ready, reset | kevesebb pin, de lassabb (esp-hosted szerint tipikusan 10-30 Mbit/s [NEM ELLENŐRZÖTT]) |
| UART | TX, RX (+RTS/CTS), reset | leglassabb, csak alacsony sávszélességre; nem javasolt kamera-streamhez |

**C6 SDIO slave fix lábak** (a C6 SDIO slave periféria IOMUX-hoz kötött) [NEM ELLENŐRZÖTT, ellenőrizni: ESP32-C6 datasheet "SDIO" / TRM]:
- CMD = GPIO18, CLK = GPIO19, D0 = GPIO20, D1 = GPIO21, D2 = GPIO22, D3 = GPIO23.
- Ezek nem esnek egybe a strapping lábakkal (GPIO4/5/8/9/15), így kapcsolási konfliktus nincs.

**Espressif EV board (ESP32-P4-Function-EV-Board) – P4 oldal** [NEM ELLENŐRZÖTT, az esp-hosted dokumentációból emlékezetből]: SDMMC Slot 1: CLK=GPIO18, CMD=GPIO19, D0=GPIO14, D1=GPIO15, D2=GPIO16, D3=GPIO17, a C6 reset (EN) a P4 GPIO54-éhez kötve. A P4 SDMMC Slot 1 lábai GPIO matrixon át szabadon is kioszthatók, de az IOMUX-lábak (GPIO14-19) a legnagyobb sebességhez/legjobb jelintegritáshoz a legjobbak. Slot 0 IOMUX: GPIO39-44 (SD-kártya számára hagyható).

**Elektromos követelmények SDIO-hoz:**
- Külső **pull-up (10 kohm, jellemzően 10-47 kohm) a CMD és D0-D3 vonalakon 3,3 V-ra** (a C6-nak SDIO slave módban a pull-up kell; az EV board is így csinálja) [NEM ELLENŐRZÖTT a pontos érték].
- A CLK-ra opcionális kis soros ellenállás (22-33 ohm) a source-nál a túllövés ellen.
- Mindkét oldal VDDIO = 3,3 V (a P4 megfelelő VDDPST domainje 3,3 V legyen; az SD-slot tápját ne a P4 belső LDO-jára kösd, ha nem arra tervezett).
- Rövid, egyforma hosszú (±5-10 mm) vezetékek, földsík alatta; 2 rétegen a 4 bites SDIO 20-40 MHz-en kivitelezhető, ha a vezeték < ~5-6 cm. Halmozott panelen a csatlakozón való átvezetés lerontja – kezdetben **40 MHz alá** konfigurálni.

**Reset és boot vezérlés:** a P4 egy GPIO-ja hajtja a C6 EN lábát (push-pull vagy nyitott kollektoros; EN-en 10 kohm pull-up + 1 uF RC a C6 oldalon az Espressif ajánlás szerint). Ha a P4 szeretné a C6 download módjába is lökni, a C6 GPIO9-et is ki kell vezetni egy P4 GPIO-ra (vagy tüskére) – lásd 3. pont.

## 3. Mindkét chip programozása

### 3.1 C6 strapping lábak [NEM ELLENŐRZÖTT – ellenőrizni: ESP32-C6 datasheet "Strapping Pins"]
- **GPIO9** (belső pull-up): 1 = SPI boot (normál), **0 = Download boot** (a reset felengedésekor LOW).
- **GPIO8**: download módban **1** kell legyen (belső pull-up nélkül lebeghet! legyen külső pull-up, vagy hagyjuk a modul alap bekötését). Egyes dokumentáció szerint GPIO8 is "don't care" normál boot módban. **Nálunk: a C6_IO8 10k felhúzás KÖTELEZŐ (05 E6, 5. fejezet).**
- **GPIO15**: a JTAG jelforrást választja (USB-Serial-JTAG vs. külső láb eFuse-szal) és/vagy a ROM-log; alapértelmezett érték (általában nem kell külső hajtás). Ne kösd erősen sem föld, sem táp felé hajtott perifériához.
- GPIO4/GPIO5: SPI-boot strapping (flash táp / JTAG), kerülendő erős külső hajtás reset alatt.
- ESP32-C6-MINI/WROOM modulon a flash-hoz tartozó lábak belül kezeltek; a modul adatlapja listázza a használható GPIO-kat.

### 3.2 C6 programozási lehetőségek a végterméken
| Mód | Hogyan | Pro | Kontra |
|---|---|---|---|
| (a) UART pad-ok | C6 U0TXD=GPIO16, U0RXD=GPIO17, EN, GPIO9 kivezetve (6 pad: 3V3/GND/TX/RX/EN/IO9) – Tag-Connect TC2030 / pogo / 1,27 mm header | független a P4-től, mindig működik; kiváló gyári első programozáshoz | kell hozzá pad-terület és külső USB-UART |
| (b) P4 frissíti a C6-ot esp-hosted OTA-val | `esp_hosted` slave OTA: a P4 a C6-nak OTA-képet küld SDIO-n át | nincs külön csatlakozó a végfelhasználónál; terepi frissítés | **első** C6 firmware nélkül nem megy (a C6 üres/gyári), és a slave-firmware-nek már futnia kell; hibás C6 firmware esetén recovery csak (a)/(c)-vel |
| (c) C6 USB-Serial-JTAG | GPIO12 (D-), GPIO13 (D+) USB-ra (natív USB, nincs külön bridge) | gyors, DTR/RTS emuláció a beépített USB-Serial-JTAG-vel (reset + boot automatikusan) | külön USB csatlakozó vagy mux kell; a P4 USB-je nem ugyanaz a port |

**Ajánlás:** a C6-nál **(a) vagy (c) pad-ok a fejlesztéshez + (b) OTA a végtermékben**. A pad-ok maradjanak a rajzon (ne kerüljenek ki), különben egy elrontott slave FW "bricket" jelent. Legalább TX/RX/EN/IO9/3V3/GND (6 pad).

### 3.3 Auto-reset kapcsolás UART esetén
Klasszikus 2 db NPN (pl. MMBT3904) DTR/RTS keresztbe: DTR->EN-hez, RTS->IO9-hez (vagy az esptool "classic reset" szekvenciához megfelelő kombináció). Ha a P4 amúgy is hajtja a C6 EN-jét, ügyelj, hogy ne harcoljon a bridge-dzsel (soros 1-4,7 kohm védőellenállás vagy dióda-OR).

## 4. A P4 programozása [NEM ELLENŐRZÖTT a részletek]

- A P4 **natív USB-Serial-JTAG** lábai: GPIO24 (D-), GPIO25 (D+) – ezek alkalmasak flash-elésre és debuggolásra (esptool a beépített ROM bootloaderen át), így **külön CH340/CP2102 nem szükséges**.
- A P4 **USB 2.0 OTG HS** PHY külön fix lábakon van (GPIO20/21) [NEM ELLENŐRZÖTT] – ez az alkalmazás-USB (UVC/MSC); ne keverd a Serial-JTAG-gel. A debug port legyen a GPIO24/25.
- **UART0**: TX=GPIO37, RX=GPIO38 [NEM ELLENŐRZÖTT]; ROM-logok és tartalék programozás pad-ról (3V3/GND/TX/RX/EN/BOOT).
- **Boot strapping**: GPIO35 (Boot, LOW = Download), GPIO36/37/38 további strapping (ROM-log, UART/USB download). Külön BOOT+RESET nyomógomb (vagy pad-ok) ajánlott, mert az USB-Serial-JTAG-vel az auto-reset sem mindig tud download módot kikényszeríteni üres/hibás flash esetén.
- A P4-nek nincs belső flash: **külső SPI/QSPI NOR flash** kell (16 MB vagy több), a PSRAM (16/32 MB) a csomagban van. A flash/PSRAM tápsínje a P4 belső LDO-ja – lásd datasheet.
- **USB-C csatlakozó**: CC1 és CC2 lábakra külön 5,1 kohm pulldown (Rd) a GND felé (különben a C-C kábelen nem ad 5 V-ot a gazda); D+/D- a két sorból párhuzamosan; VBUS-on TVS/ESD; shield GND-re (RC vagy 1 Mohm + 4,7 nF). Az USB D+/D- differenciális 90 ohm – 2 rétegen rövid (<~3 cm), szűk csatolású vezetékkel és alatta folytonos föld.
- **ESD**: USBLC6-2SC6 (vagy hasonló, pl. TPD2EUSB30) a D+/D- vonalakon, a csatlakozóhoz közel; VBUS-on SMF5.0A vagy hasonló TVS, plusz polyfuse/PTC vagy kapcsolt áramkorlát.
- **Legkisebb programozó rendszer (ajánlott):**
  1. P4: **natív USB-C** (GPIO24/25 Serial-JTAG), BOOT + RESET gomb.
  2. C6: **6 pad Tag-Connect TC2050/TC2030 vagy pogo** (TX/RX/EN/IO9/3V3/GND), csak gyári első flash-eléshez és recovery-hez; a mindennapi frissítés a P4-ről **esp-hosted OTA**.
  3. Alternatíva: külön, lecsatolható "programozó panel" (CP2102N/CH340C + auto-reset tranzisztorok), ami pogo-pinekkel illeszkedik a C6/P4 pad-jaira; a termékpanelen így nincs bridge IC és USB-C a C6-nak.

## 5. Táplálás – C6

- **VDD**: 3,3 V (3,0-3,6 V tartomány) [NEM ELLENŐRZÖTT pontos tartomány]. Modul esetén a modulon van a hidegítés, de külső **10 uF + 0,1 uF** a modul 3V3 lábánál ajánlott.
- **Csúcsáram**: Wi-Fi TX csúcs ~350 mA körüli (szűk impulzus), a hivatalos tervezési ajánlás szerint a táp legyen legalább **500 mA** a modulra [NEM ELLENŐRZÖTT]. A teljes 3,3 V sínt a P4-gyel együtt méretezd (lásd 6.).
- **Bulk kapacitás**: 22 uF + 100 uF (low-ESR kerámia/tantál) a 3,3 V sínre a C6 közelében; a kondenzátor kerüljön a modul 3V3 lábához a legközelebb.
- **EN lap**: 10 kohm pull-up + 1 uF a GND felé (RC reset-késleltetés); az EN-t a P4 GPIO-ja nyitott kollektorosan hajtsa.
- **Bekapcsoláskori sorrend**: a C6 3,3 V-ja ne késsen jelentősen a P4 SDMMC VDDIO-jához képest, különben a CMD/CLK vonalak a P4 felől betáplálják a C6-ot (ESD-diódákon át). SDIO előtt a C6 EN-t a P4 tartsa LOW-on, amíg a sín stabil.

## 6. Teljes tápellátás – kompakt kamerához

**P4 tápfa az EV boardon** [NEM ELLENŐRZÖTT, a sematikából nézendő]: 5 V USB -> 3,3 V buck (több sínre), a P4 belső LDO-i adják a MIPI PHY (kb. 2,5 V), a flash/PSRAM (1,8 V / 3,3 V) és a core (kb. 1,1 V) feszültségeket – külső alkatrészekkel (induktor, kondenzátorok) a datasheet szerint; a P4 core-t külső DC/DC látja el a hardware design guideline szerint a nagyobb áram miatt. **Ennek pontos felépítését az ESP32-P4 Hardware Design Guidelines "Power Supply" fejezetéből KELL kiolvasni** – ez a legnagyobb kockázat a 2 rétegű panelnél.

**Ajánlott bemenetek:**
1. **USB-C 5 V** (fő): CC Rd 5,1 kohm; szükséges áram ~1-1,5 A (P4 + kamera + C6 + LED-ek). Bemeneten ideális-dióda/load-switch (pl. TPS2113A vagy dióda-OR) ha LiPo is van.
2. **Opcionális LiPo + töltő**: kompakt bq24074 (power-path, 1 A) vagy MCP73831 (egyszerű); a TP4056 olcsó, de nincs power-path és melegszik – nem ajánlott hosszú távon. Védőáramkör (DW01 + 8205) az elemnél, ha az nincs bent.
3. **3,3 V sín**: szinkron buck, ≥ 2 A (pl. TPS62xxx család, SY8089 2 A, TPS63xxx buck-boost ha az akku tartománya a 3,3 V köré esik). 2 rétegen tartsd a kapcsolóhurkot nagyon kicsire, az induktor alatt ne legyen megszakítás a földben.
4. **Kamera-sínek** (a kamera modul datasheetje szerint): jellemzően 1,8 V + 2,8 V (AVDD, DVDD, IOVDD) – külön LDO-k (pl. 2 db AP7343 / TLV733) a kamera közelében.
5. Hűtés/EMC: 3,3 V sínre ferritgyöngy a kamera analóg és a digitális rész között; P4 VDD lábaknál minden pin-hez 100 nF + minden sínhez bulk.

**Összefoglaló javaslat:** USB-C 5 V -> TVS+PTC -> (opcionális power-path + LiPo) -> 3,3 V buck (≥ 2 A) -> P4 + C6 modul + flash; P4 belső LDO-k a datasheet szerinti külső kondenzátorokkal; kamera 1,8/2,8 V külön LDO-kkal.

## Források (a megerősítendő elsődleges dokumentumok; ebben a munkamenetben NEM voltak letölthetők)
- ESP32-C6 Datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf
- ESP32-C6 Hardware Design Guidelines: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/index.html
- ESP32-C6-MINI-1 datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf
- ESP32-P4 Datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-p4_datasheet_en.pdf
- ESP32-P4 Hardware Design Guidelines: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32p4/index.html
- ESP32-P4-Function-EV-Board user guide + sematika: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html
- esp-hosted-mcu: https://github.com/espressif/esp-hosted-mcu (docs/sdio.md, docs/spi_full_duplex.md, docs/ota.md)
- esp_wifi_remote: https://github.com/espressif/esp-protocols/tree/master/components/esp_wifi_remote
- Komponens-registry (WebSearch találat, csak példa-kódot adott): https://components.espressif.com/components/espressif/esp_hosted
- ESPHome esp32_hosted (WebSearch találat): https://esphome.io/components/esp32_hosted/

## Nyitott kérdések / kockázatok
1. **Minden konkrét GPIO, méret, áram [NEM ELLENŐRZÖTT]** – ellenőrizni a fenti datasheet-ekkel és az EV-board sematikával mielőtt a kapcsolási rajz készül.
2. **P4 tápfa 2 rétegen:** a P4 több belső LDO-t és külső DC/DC-t igényel, a QFN/BGA kivezetés (P4 BGA) 2 rétegen legvalószínűbb problémás (via-in-pad, fanout). Érdemes mérlegelni 4 réteget vagy kész **P4 modul** (ha létezik) használatát.
3. **SDIO jelintegritás stacked csatlakozón át**: kezdetben 1 bites/alacsony órajel fallback-et tervezz (pad a 0 ohm-os átkötésekhez).
4. **C6 RF/antenna**: ha a P4-es panel fölé/alá kerül a C6 modul, az antenna-keep-out a halmozásnál sérülhet.
5. **USB-C**: a P4 USB OTG HS (fix GPIO) és a Serial-JTAG (GPIO24/25) két külön port – eldöntendő, hogy egy vagy két csatlakozó kell (vagy USB mux).
6. **C6 recovery**: az OTA-only frissítés megbízhatatlan, ha a slave FW elromlik – a pad-ok megtartása kötelező.
7. **P4 szilícium-revízió** (v1.0 vs. v3.x): a boot/strap és USB viselkedés revíziófüggő lehet; ellenőrizni az errata-t.
8. Auto-reset kapcsolás: a P4/C6 DTR/RTS logika megerősítendő az esptool aktuális reset-szekvenciájával.
