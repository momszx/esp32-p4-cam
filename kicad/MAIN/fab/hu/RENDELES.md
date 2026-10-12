# ESP32-P4-CAM MAIN rev A – JLC rendelési útmutató (2026-10-11)

Forrás: `kicad/MAIN/ESP32-P4-CAM-MAIN.kicad_pcb`. A zónák a projekt-szabályokkal vannak kitöltve. Gyártás előtti kapu: DRC zóna-újratöltés **nélkül** 0 hiba, ERC 0, séma↔lap paritás 0, és 12 bekötetlen ág, mind DNP.

## Feltöltendő fájlok

| Fájl | Mire |
|---|---|
| `gerber_jlc.zip` | NYÁK: 4 réz-, maszk-, paszta-, szita- és él-réteg, valamint PTH/NPTH fúrás |
| `BOM_jlc.csv` | PCBA anyagjegyzék: 40 egyedi tétel LCSC-számmal, 72 beültetési hely |
| `CPL_jlc.csv` | beültetési fájl: 72 sor, 47 felső + 25 alsó, a BOM-mal pontosan egyezik |
| `bom_notes.md`, `parts.json` | alkatrész-választás indoklása, készlet, ár |

## NYÁK beállítások (JLC űrlap)

| Mező | Érték |
|---|---|
| Rétegek | 4 |
| Méret | 45 × 45 mm (a gbrjob 45,1-et ír a kontúrvonal vastagsága miatt) |
| Vastagság | 1,0 mm |
| **Stackup** | **JLC04101H-3313A** – kifejezetten ezt kell kiválasztani; a sávszélességek csak erre jók |
| **Impedancia-vezérlés** | **Igen** (50 Ω RF 0,302 mm; CSI 100 Ω 0,204/0,203; USB 90 Ω 0,262/0,203) |
| Réz | külső 1 oz, belső 0,5 oz |
| **Felület** | **ENIG** (0,2 mm-es padrések az U3/U4/J1-en; a JP1 nyitott forrasztó-áthidaló) |
| Via | tented (fedett), csak átmenő via; legkisebb furat 0,25 mm, pad 0,5 mm |
| Panel | egyedi lap; **keretsín csak a felső és az alsó élen**, rajtuk fiduciálok |
| Fül / V-vágás | **a jobb élen semmi** (a C3, R10, C1 0,7 mm-re van a széltől), V-vágás sehol |

## Beültetés (PCBA)

- Kétoldalas SMT, 0,10 mm-es stencil. Az U3 pasztája TI-ajánlás szerint csökkentett (82 / 93 %). Az U1-en és a DNP alkatrészeken nincs paszta.
- **U1 (Waveshare ESP32-P4-Module) nincs a BOM-ban.** Te forrasztod kézzel az SMT után. Finom kúpos heggyel menj a P83–P88 lábakon, utána nézd meg a P87 és a C23 közti rést, valamint az R34/J4 forrasztását.
- **J1 USB-C tartólábak:** a 4 köpenyláb SMT-vel valószínűleg nem forrad be. Kérd a JLC-től kézi vagy szelektív forrasztásként, vagy forraszd be magad, mielőtt először bedugod a kábelt.
- **A JLC beültetési előnézetében ellenőrizd** a forgatást és az 1-es lábat:
  - U2, U3, U4, U5, U6;
  - D1 (a katód a VBUS oldalon), D20;
  - J1, J2, J4, J5;
  - mind a 25 alsó oldali alkatrészt.
- **Foglald le előre** (alacsony készlet):
  - J2 – C5164008, 31 db;
  - U3 – C3662799, ~330 db;
  - R6 – C22963, 180 db.
- Extended tételek: 24 db, kb. 72 USD beállítási díj. Az alkatrészek kb. 8,8 USD/lap, az U1 nélkül.
- U5 (TECH PUBLIC C5350871): a lábkiosztást az LCSC termékoldalán ellenőriztem: 1 IO1, 2 IO2, 3 GND, ugyanaz, mint a TI-é.

## Első bekapcsolás előtt (ohmméter, U1 beforrasztva)

1. TP16A (ESP_EN) ↔ TP4 (+3V3): kb. 10 kΩ. Ha 0 Ω, akkor a P87 és a C23 összeforrt.
2. 3V3_BUCK ↔ GND: 5–16 kΩ között. Nagyobb érték R14/R15/R33 hibát jelez, ilyenkor a buck akár 9 V-ot is kiadhat.
3. VBUS ↔ VBUS_SW: kb. 300 kΩ, a JP1 legyen nyitva.
4. VBUS, D+, D− ↔ GND: nincs rövidzár.

## Firmware-szabályok rev A-ra

- I2C 100 kHz-en.
- A CH224A csak olvasható, és csak a CAM_3V3 bekapcsolása után. **Soha ne írj bele**: a 0x0A regiszterrel 20/28 V-ot kérhetne.
- A PD módot a PG lábból és a VBUS_MON ADC-ből kell venni.
- Az IR_SW_EN maradjon alacsony.
- Az USB HS PHY-t soha ne kapcsold be ezen a layouton: csak FS (12 Mbps).

## Mechanika

- Az MH1, MH2 és MH4 furatokhoz nylon távtartó vagy alátét kell.
- Az MH3-nál ne legyen alátét: a csavarfej legfeljebb Ø4,0 mm, és az u.FL kábel nyugat vagy észak felé lépjen ki.

## Tulajdonosi döntések (a NYÁK-gyártást nem blokkolják)

- **Q6 – a J2 érintkező-oldala és az FFC kábel:** a valós kamerával és kábellel kell eldönteni az első kamera-bekapcsolás előtt. Ha a lábsorrend fordított, cseréld a kábelt a másik típusúra (azonos oldali ↔ ellentétes oldali érintkezős).
- **Q17 – a J5 lap-lap csatlakozó magassága:** a választott Hong Cheng pár 5,3 mm-es. 7,0 mm-es távtartónál ez kb. 2,3 mm-es illeszkedés. A FRONT lapon magasabb aljzat kell, a MAIN lapot ez nem érinti.

## Rev A-ra tudatosan elfogadott eltérések (a 9. körös review alapján)

- A D1 TVS az eFuse bemeneténél van, nem a J1 mellett.
- A CSI adat–órajel eltérése ≈0,05 UI, a CLK 21,4 mm. A G5b-ben hibaszámlálós tartósteszt kell rá.
- Az USB FS vonalak referenciája részben a VBUS_SW sík vagy üres terület.
- A +3V3 fővezeték rétegváltásai egyes viákon mennek, 21 mΩ.
- Hiányok a lap szélén a GND viák kerítésében.
- A J2/SD/CC ESD-védelme rev B-re halasztva.
- Az R14.1 és az R27.2 viájának furata 0,03 / 0,07 mm-t lóg a padba (azonos neten). A 2. pont mérése ezt lefedi.
- 12 bekötetlen ág, mind DNP-hez megy (CC1/CC1_ADC/CC2/CC2_ADC, U7/R73). **Ha valaha beültetnéd ezeket, előtte be kell kötni.**
