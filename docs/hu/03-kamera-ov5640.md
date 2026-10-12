> ⚠️ Kutatási jegyzet (2026-10-09). Ahol ellentmond a 05-architektura.md-nek, a 05 érvényes. Ismert elavult pontok: az OV5640 MIPI támogatás „nem igazolt” megjegyzése felülírva: E11 igazolja (F-11); a 2592×1944 felbontás helyett 1080p30 cap (ISP max 1920×1080, F-28); a kamera modul kötelezően onboard oszcillátorral + LDO-kkal + 3V3 bemenettel (F-27, E-17); MIPI sáv ≤800 Mbps/lane; WebFetch-blokk miatti „emlékezetből” állítások nem ellenőrzöttek; a „max. 2 réteg” feladat-korlát megszűnt – a MAIN v0.6 4 rétegű (00 K4; CSI 100 Ω: 0,204/0,203 mm, 05 §3.2), az 5. fejezet 2 rétegű megfontolásai a MAIN-re elavultak; a kamera-csatlakozó a NYÁK-on egyelőre helyőrző lábkép (TE 1-84953-5, 05 §6, Q6).

# 03 – Kamera: OV5640 és alternatívák ESP32-P4-hez

> **Megbízhatósági megjegyzés (fontos).** A kutatás során a közvetlen oldal-letöltés (WebFetch és quarantine-reader) **blokkolva volt** (hook hiba, illetve a domain nincs engedélyezési listán). Csak WebSearch-összefoglalók álltak rendelkezésre. Amit ezekből megerősítettem, az **[ELLENŐRZÖTT – forrás]**; ami csak előzetes tudásból származik, az **[NEM ELLENŐRZÖTT]**. Gyártás előtt a datasheeteket és az EV-board kapcsolási rajzot kézzel kell ellenőrizni.

## 1. OV5640 interfészek és ESP32-P4 támogatás

### 1.1 OV5640 oldalról
- 5 MP-es szenzor; DVP 8/10 bites párhuzamos és MIPI CSI-2 (1 vagy 2 lane) kimenet is van. [NEM ELLENŐRZÖTT – általános ismeret, datasheet nem volt olvasható]
- SCCB (I2C-szerű) cím: 0x78 (írás) / 0x79 (olvasás), azaz 7 bites **0x3C**. [NEM ELLENŐRZÖTT]

### 1.2 ESP32-P4 oldalról
- Az Espressif ESP-IDF kameradoksi három hardver utat sorol fel: **MIPI-CSI**, **DVP az ISP modulon keresztül** és **DVP a LCD_CAM modulon keresztül**. Tehát a P4-nek van DVP-je is. [ELLENŐRZÖTT – ESP-IDF Camera Controller Driver oldal (keresési összefoglaló)]
- MIPI-CSI: a példakód 2 data lane-nel dolgozik; ISP használatakor a kamerarendszer max. kimenet 1920x1080; MIPI-CSI max. 1,5 Gbps/lane. [ELLENŐRZÖTT – esp_cam_sensor readme]
- Egy dokumentált példa: 2592x1944 (OV5645) fogadható a P4 sávszélességén. [ELLENŐRZÖTT – esp_cam_sensor readme]

### 1.3 Mi jobb a P4-hez: DVP vagy MIPI?
| Szempont | MIPI CSI-2 (2 lane) | DVP (8 bit) |
|---|---|---|
| Jelszám | 5 diff. pár/pin (CLK, D0, D1) + I2C | ~8 adat + PCLK + VSYNC + HREF + XCLK + I2C = 14+ GPIO |
| ISP (Bayer→RGB/YUV, AE/AWB) | Hardveres ISP-n át | ISP-DVP úton lehetséges, de OV5640 DVP jellemzően már YUV/RGB-t ad (a szenzor ISP-je dolgozik) |
| Sávszélesség | Magas, nagy felbontás/fps | PCLK-limitált; 5 MP-hez gyenge |
| 2 rétegű PCB | Kritikus a diff. pár (lásd 5.) | Könnyebb impedanciamentesen, de sok vezeték, nehéz a kompakt halmozott kártyán |
| Szoftvertámogatás | esp-video + esp_cam_sensor (elsődleges út) | LCD_CAM/ISP-DVP, kevesebb példa a P4-hez |
**Összegzés:** a P4 „natív” és legjobban támogatott útja a MIPI-CSI + ISP. DVP tartalék/egyszerűsítő megoldás, de sok GPIO-t foglal.

### 1.4 Az OV5640 támogatottsága MIPI-n
- Az esp_cam_sensor README-ben az OV5640 említése csak az ESP32-S3-hoz kapcsolódik (JPEG kimenet, 2 MP), **P4 MIPI-hoz nem találtam megerősítést**. [ELLENŐRZÖTT, hogy nincs említve a kapott részletekben; a teljes tábla NEM volt olvasható]
- Biztosan szerepel a komponensben az **SC2336** (1920x1080, MIPI és DVP, 8/10 bit RAW). [ELLENŐRZÖTT – readme-részlet]
- **OV5647, OV02C10, SC202CS** stb. P4-es hivatalos támogatása: ismereteim szerint léteznek a komponensben, de ez **[NEM ELLENŐRZÖTT]** (a keresés nem hozta vissza a táblázatot). A verzió/lista változik – a docs.espressif.com/projects/esp-video-components oldalon kell nézni az aktuálisat.
- **Következtetés:** az OV5640 MIPI-n a P4-hez gyenge/ellenőrizetlen támogatású → saját regisztertábla és ISP-hangolás kellhet. Ha MIPI kell, az SC2336 vagy OV5647 biztosabb választás.

## 2. Modulcsatlakozók és kiosztások

### 2.1 Espressif ESP32-P4-Function-EV-Board
- Kamera csatlakozó: **1.0K-GT-15PB, 15 pólus, 1,0 mm raszter**, külső kameramodulhoz; adapterpanel + előre irányú szalagkábel. [ELLENŐRZÖTT – EV-board user guide (keresési összefoglaló)]
- Lábkiosztás (jel/GPIO): **nem volt olvasható** → a kapcsolási rajzból kell kiolvasni. [NEM ELLENŐRZÖTT] Valószínűleg a Raspberry Pi 15 pólusú kiosztáshoz hasonló, de **ne feltételezd**.

### 2.2 Raspberry Pi 15 pólusú CSI (1,0 mm) – gyakori MIPI modulforma
| Láb | Jel |
|---|---|
| 1 | GND |
| 2 / 3 | CAM_D0_N / CAM_D0_P |
| 4 | GND |
| 5 / 6 | CAM_D1_N / CAM_D1_P |
| 7 | GND |
| 8 / 9 | CAM_CK_N / CAM_CK_P |
| 10 | GND |
| 11 / 12 | CAM_IO0 / CAM_IO1 (LED/PWDN-szerű GPIO) |
| 13 / 14 | CAM_SCL / CAM_SDA |
| 15 | CAM_3V3 |
Az 1–12. láb [ELLENŐRZÖTT – Arducam pinout], a 13–15. láb [NEM ELLENŐRZÖTT – ismeretből]. Az Arducam szerint a kiosztás változattól függetlenül azonos. Csatlakozó (kamera oldal): Amphenol SFW15R-2STE1LF (1 mm, jobb szögű) [ELLENŐRZÖTT – Arducam]; hoszt oldal: pl. TE 1-1734248-5 (állítólag RPi-kártyákon) [ELLENŐRZÖTT – Arducam].

### 2.3 Raspberry Pi Zero/CM/5 22 pólusú (0,5 mm)
Ismereteim szerint: 1 GND, 2/3 D0 N/P, 4 GND, 5/6 D1 N/P, 7 GND, 8/9 CLK N/P, 10 GND, 11/12 D2 N/P, 13 GND, 14/15 D3 N/P, 16 GND, 17 CAM_GPIO, 18 CAM_CLK, 19 GND, 20 SCL, 21 SDA, 22 3V3. **[NEM ELLENŐRZÖTT]** – 4 lane-es forma, a P4-nek csak 2 lane-je van, így az D2/D3 lábak üresek maradnak.

### 2.4 24 pólusú, 0,5 mm DVP FPC (ESP32-CAM jellegű OV5640 modulok)
- A kiosztás **gyártónként eltér**, ezért nem adok általános táblát; a konkrét modul adatlapja kell. Az Element14 fórumban látott DVP-lista eleje: VCC 3.3V, GND, SCL, SDA, VSYNC, HREF, PCLK… [ELLENŐRZÖTT, részleges]
- Tipikus jelkészlet: AVDD/DOVDD/DVDD(vagy 3V3), GND, SCL, SDA, VSYNC, HREF, PCLK, XCLK, D2–D9, PWDN, RESET, (AF-nél AF_VDD). [NEM ELLENŐRZÖTT]
- Pl. a Kurokesu 687.5640A MIPI-s 24 pólusú 0,5 mm modul Würth 68712414522 csatlakozót használ (22. láb: power-down). [ELLENŐRZÖTT – Kurokesu wiki] – ez MIPI, nem DVP kiosztás.

### 2.5 Csatlakozó-ajánlás
- **15 pólus, 1,0 mm:** Hirose FH12-15S-1SH(55) vagy azonos raszterű LCSC alternatíva. A kontaktusoldal (felső/alsó) és az LCSC cikkszám **[NEM ELLENŐRZÖTT]** – a gyártó adatlapja és a kábel/modul fordítása alapján kell megválasztani (a „forward/reverse” szalagkábel kérdés alap hiba).
- **0,5 mm, 22/24 pólus:** Würth 68712414522 (24 p.) fent említve; 22 p. változat Hirose FH12-22S-0.5SH [NEM ELLENŐRZÖTT].
- Mindig ellenőrizd: kontaktus fent/lent, zárófogantyú, FPC vastagság (0,3 mm).

## 3. Táplálás és vezérlés

| Sín | Érték | Megjegyzés |
|---|---|---|
| AVDD | 2,6–3,0 V (tip. 2,8 V) | analóg, zajérzékeny, külön LDO |
| DOVDD | 1,8 V vagy 2,8 V | I/O szint |
| DVDD | 1,5 V | belső szabályozóval is működik (külső kondenzátor) |
Értékek [NEM ELLENŐRZÖTT – általános ismeret, a datasheet nem volt olvasható]. Becsült fogyasztás: AVDD ~20–30 mA, DVDD/DOVDD ~50–100 mA, össz. ~100–150 mA aktív módban [NEM ELLENŐRZÖTT].

- **Modulok:** a legtöbb kész OV5640 modul (RPi stílusú vagy 24 pólusú) saját LDO-kat tartalmaz egyetlen 3,3 V-os bemenetből (CAM_3V3 az RPi csatiban), de ez modulfüggő. Ha saját szenzort forrasztunk, 2,8 V + 1,8 V (+ 1,5 V) LDO kell.
- **Bekapcsolási sorrend** (datasheet 2.7 szerint, Linux driver patchekből idézve): DOVDD stabil → ≥5 ms → PWDN le → ≥1 ms → RESETB fel → ≥20 ms → első SCCB hozzáférés. [ELLENŐRZÖTT – linuxtv patch]. Hardveres reset bekapcsoláskor ajánlott/előírt. [ELLENŐRZÖTT]
- **RESETB** belső felhúzása a DOVDD-hez megy; 2,8 V-ot ne adjunk 1,8 V-os DOVDD-s RESETB-re. SCL/SDA tűri a magasabb felhúzást. [ELLENŐRZÖTT – Allwinner app note]
- Egyes modulok nem vezetik ki PWDN/RESETB-t. [ELLENŐRZÖTT]
- **XCLK:** 6–27 MHz, tipikusan 24 MHz [NEM ELLENŐRZÖTT]. A P4 LEDC-je alacsony sebességű módban használható, és a timerek közös órajelet használnak; 24 MHz előállíthatósága és jitter-e **nincs megerősítve** (a dokumentáció az XCLK-t nem említi). [ELLENŐRZÖTT a LEDC korlátokra, a többi NEM] Biztosabb: önálló 24 MHz oszcillátor a kártyán, vagy olyan modul, amelyen van saját oszcillátor (sok RPi-kamerán van).
- **SCCB pull-up:** 2,2–4,7 kΩ a DOVDD-hez illeszkedő szintre; a P4 GPIO-szint és a szenzor I/O-szintje közötti illesztésre figyelni kell (3,3 V ↔ 1,8 V). [NEM ELLENŐRZÖTT]
- A P4 MIPI D-PHY-hez külön tápot igényel (belső LDO csatornából). [NEM ELLENŐRZÖTT – P4 hardverreferencia ellenőrzendő]

## 4. Autofókusz (AF) változat
- Az AF-es OV5640 modulok VCM-et tartalmaznak; az OV5640 beágyazott vezérlővel és firmware-letöltéssel (SCCB-n át) működtethető AF-et támogat. [NEM ELLENŐRZÖTT]
- Kiegészítő kérdések: VCM tápja (tip. 2,8 V), külön AF_VDD láb a 24 pólusú modulokon, a firmware (~4 KB) letöltése bootkor, extra szoftver-munka az esp_cam_sensor-ban (nem biztos, hogy van kész támogatás). Fix fókuszos változattal egyszerűbb.

## 5. Elrendezés 2 rétegű PCB-n
- **Megvalósítható, de kockázatos.** A MIPI D-PHY 100 Ω diff. pár; 2 rétegen a referencia-sík a másik oldalon van, 1,6 mm lemezen a 100 Ω diff. impedancia keskeny pár + széles távolság kérdés (pár cm-nél rövid szakasz elviselhető). [NEM ELLENŐRZÖTT – általános jó gyakorlat]
- Tippek: az FPC csatlakozót közvetlenül a P4 mellé; a diff. párt a legrövidebb úton, teljes GND-sík alatta, via-mentesen; pár-lengthmatch ±0,1–0,2 mm (a pár két tagja), lane-ek között lazább; ne keresztezzen szakadékot a GND-síkban; tápbontás a PHY lábaknál. 1,5 Gbps/lane felett veszteség-érzékeny; alacsonyabb lane sebességű módot (pl. 720p30) választva a kockázat csökken.
- Ha a gyártó (pl. JLC) 2 rétegre ad impedanciaszámolót, használd; 4 rétegű kártya erősen ajánlott, ha lehetséges. A feladat max. 2 réteg → tartalékként DVP.

## 6. Ajánlás a projektre
1. **Elsődleges:** MIPI-CSI 2 lane, **RPi-kompatibilis 15 pólusú 1,0 mm FPC** csatlakozó közvetlenül a P4 mellett (EV-board kompatibilis), **SC2336 vagy OV5647** modullal (Espressif támogatottság a komponensben jobb/megerősítettebb, az SC2336 [ELLENŐRZÖTT]).
2. **OV5640 MIPI-n:** csak ha az 5 MP / AF kell; a támogatás ellenőrizetlen → kockázat, saját driver-munka lehet.
3. **OV5640 DVP (LCD_CAM):** biztonságos tartalék, de ~14 GPIO + hosszabb vezetékek a kompakt halmozott kártyán; 24 pólusú 0,5 mm FPC.
4. Az XCLK-t érdemes külön 24 MHz oszcillátorból vagy a modulból venni; LEDC-vel csak teszt után.
5. Tervezz a kártyán jumper/0 Ω lehetőségeket a tápsínekhez és PWDN/RESET-hez.

Kompromisszum: MIPI = kevesebb jel, jobb támogatás, de érzékeny elrendezés 2 rétegen; DVP = egyszerű impedancia, de sok GPIO és gyengébb sávszélesség.

## Források
- https://components.espressif.com/components/espressif/esp_cam_sensor (és /versions/2.6.0/readme) – keresési összefoglaló
- https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32p4/api-reference/peripherals/camera_driver.html
- https://docs.espressif.com/projects/esp-idf/en/v5.3/esp32p4/api-reference/peripherals/ledc.html
- https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html
- https://docs.espressif.com/projects/esp-faq/en/latest/application-solution/camera-application.html
- https://docs.arducam.com/Raspberry-Pi-Camera/raspberry-pi-camera-pinout/
- https://wiki.kurokesu.com/books/6875640-camera-module/export/html
- https://patchwork.linuxtv.org/project/linux-media/patch/20221219143056.4070-2-j-luthra@ti.com/mbox
- https://wiki.linux-sunxi.org/A31s/HDK/A31s_HDK-20140222/device_data/camera/OV5640_Camera_Module_Hardware_Application_Notes_R1.0_Allwinnertech.pdf
- https://www.mouser.lt/datasheet/3/902/1/LI_OV5640_MIPI_AF_SPEC.pdf (nem olvasható)
- OV5640 datasheet (cdn.sparkfun.com/datasheets/Sensors/LightImaging/OV5640_datasheet.pdf) – nem sikerült megnyitni

## Nyitott kérdések / kockázatok
- Az OV5640 hivatalos MIPI-támogatása a P4-en (esp_cam_sensor lista) – ellenőrizendő.
- EV-board kamera csatlakozó pontos lábkiosztása és GPIO-k (I2C, XCLK, RESET) – kapcsolási rajzból.
- A 15-pin RPi 13–15. láb és a 22-pin kiosztás vizsgálata hivatalos RPi dokumentációból.
- 24 MHz XCLK LEDC-ből: jitter, megvalósíthatóság.
- Tápfeszültségek, áramok, DVDD belső szabályozó – OV5640 datasheetből.
- Szintillesztés P4 GPIO (3,3 V) ↔ szenzor I/O (1,8/2,8 V).
- 2 rétegű MIPI impedancia és a gyártói stackup.
- AF firmware és VCM támogatás a szoftverben.
- Csatlakozó kontaktusoldal és LCSC cikkszámok.
