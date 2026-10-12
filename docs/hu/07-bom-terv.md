# 07 – BOM-terv és értékszámítási lap (v0.4 – rev A BOM lezárva)

Dátum: 2026-10-09 · Státusz: **rev A: G4 lezárva (2026-10-11, §0)**; eredetileg ~~váz – a G4 kapu (05 §0.2) kitölti, a MAIN sematik ELŐTT~~ (K-8) · Alap: `05-architektura.md` v0.5 (v0.3-tól: v0.6 as-built), `06-floorplan-vazlat.md` v0.3 · v0.2 (R4): új passzív-csoport sorok (#53–#60), TP-terv, státusz LED, J7 pin-lista · **v0.3 (2026-10-10, as-built + 7. kör review):** R23/C25 FIT (#22a), D2 DNP (#23), R28 10k (#54), kamera vezérlő-ESD és SD ESD → rev B (#38, #42), J2/J5/L1 helyőrző lábképek, J7 / TP / J4 as-built, G4 nyitott · **v0.4 (2026-10-11, 8–9. kör): G4 rev A-ra lezárva – végleges BOM a §0-ban** (72 beültetett tétel LCSC-számmal, C14 új, kiválasztott speciális alkatrészek, készlet-foglalás, maradék tulajdonosi döntések); a §1 TBD-i a v0.3 állapotot őrzik, ahol a §0 / `BOM_jlc.csv` mást mond, az az érvényes
Jelölés: **TBD** = még nincs kiválasztva / kiszámolva · **[NEM ELLENŐRZÖTT]** = saját tudás, adatlappal még nem igazolt. Az "osztály" oszlop **nem alkatrész-választás**, csak a követelmény neve; az MPN-t adatlap alapján kell kitölteni. Rev A oszlop: **FIT** = beültetve, **DNP** = footprint van, nincs beültetve.
Szabály: a sematik nem indulhat, amíg a rev A **FIT** sorokban van TBD (MPN, LCSC#, footprint-forrás) vagy a 2. fejezetben kiszámítatlan érték.

> **G4 állapot (2026-10-11, 9. kör): ✅ rev A-ra LEZÁRVA.** Mind a 72 beültetett tétel LCSC / MPN / Manufacturer mezővel a sémában és a NYÁK-on (séma = NYÁK = `BOM_jlc.csv` = CPL, paritás 0); U3 `attr smd`, U1 / MH1–4 / TP / JP1 / DNP kizárva; a 2026-10-10-i döntések (R23 + C25 FIT, D2 DNP, R28 10k) és az új C14 átvezetve. Nyitott tulajdonosi döntés: **Q6** (J2 kontakt-oldal), **Q17** (J5 magasság), **U5** második forrás – §0.4. ~~2026-10-10, 7. kör: NYITOTT – egyetlen MPN / LCSC mező sincs; J2 / J5 / L1 helyőrző; U3 SMD-attribútum hiányzik; CPL = 70 sor~~ (történeti).

## 0. Rev A végleges BOM (G4 lezárva, 2026-10-11)

Forrás: `kicad/MAIN/fab/` – `BOM_jlc.csv` (40 sor, 72 hivatkozás), `CPL_jlc.csv` (72 sor), `parts.json` (hivatkozásonkénti adat, készlet), `bom_notes.md` (választási indoklás). Készlet / ár / Basic-Extended: JLCPCB parts + LCSC, böngészővel 2026-10-11 – **rendelés előtt frissíteni**. Az értékek (UVLO 4,40 / 4,00 V, OVLO 10,87 V, ILIM 2,03 A, FB 3,328 V, SS 1,45 ms) változatlanok.

### 0.1 Összesítés
| | |
|---|---|
| Beültetett tételek (CPL-sor) | **72** (a 2026-10-10-i 71 FIT + az új **C14**) – **F 47 / B 25** (a C4 a B oldalra került) |
| Egyedi alkatrész (BOM-sor) | **40**: **16 Basic** (45 beültetés), **24 Extended** (27 beültetés) |
| Extended beállítási díj | 24 × ~3 USD ≈ **~72 USD / rendelés** (a JLC aktuális díjtábláját rendeléskor ellenőrizni) |
| Alkatrész-költség / lap | ≈ **8,8 USD** (1+ egységár, **U1 modul nélkül**); legdrágább: J2 2,21 · U3 1,28 · U4 1,15 · U2 0,45 · U6 0,40 USD |
| PCBA | kétoldalas → **JLC Standard PCBA** (az Economic csak egyoldalas) |
| Kizárva | U1 (kézi forrasztás, a tulajdonos szerzi be), TP1–TP19, JP1, MH1–4, minden DNP |

### 0.2 Kiválasztott speciális alkatrészek
| Ref | Alkatrész (MPN) | LCSC | Megjegyzés |
|---|---|---|---|
| U2 | WCH **CH224A** (ESSOP10) | C42459160 | PD sink, I2C 0x22/0x23, FW: csak olvasás (`05` §4.1) |
| U3 | TI **TPS259470ARPWR** (RPW0010A) | **C3662799** | eFuse; készlet ~300 (331) → **foglalni**; paszta 82 / 93 % (TI stencil) |
| U4 | TI **TPS62933FDRLR** (SOT-583) | C5219272 | buck FCCM, 1,2 MHz; 1936 db |
| U5 | TECH PUBLIC **TPD2E2U06DCKR-TP** (SC-70-3) | **C5350871** | **klón** – a TI eredeti (C1855726) csak 1 db; a lábkiosztás (1 D+, 2 D−, **3 GND**) **nem igazolt** → rendelés előtt az LCSC adatlapon ellenőrizni, különben TI C1855726 / globális beszerzés; bring-up: D± ↔ GND |
| U6 | TI TPS22917DBVR | C2681320 | CAM_3V3 load switch |
| D1 | Diodes **SMAJ10A-13-F** | C134939 | TVS; pad 1 = katód = VBUS – JLC-előnézetben ellenőrizni |
| L1 | Taiyo Yuden **NRS5024T2R2NMGJ** | C222926 | 2,2 µH, Isat 4,1 A, Irms 3,1 A, 29 mΩ, 4,9×4,9×**2,4 mm** (≤3,3 mm ✓); a generikus `L_Taiyo-Yuden_NR-50xx` land a NRS5024 rajzával nincs összevetve → JLC DFM / 3D előnézet |
| J1 | HRO TYPE-C-31-M-12 | C165948 | **4 köpenyláb paszta nélkül** → JLC kézi / szelektív forrasztás vagy saját (`05` §3.1, §15) |
| J2 | **TE 1-84953-5** (15 p, 1,0 mm, TOP contact, csúszózáras) | **C5164008** | a lábkép maga az alkatrész; **JLC-készlet 31 db → foglalni**; bottom-contact párja 1-84952-5 (C3170098, azonos land, ~1 db); kontakt-oldal **Q6** |
| J4 | Hirose U.FL-R-SMT-1(80) | C88374 | RF, rev A FIT (G2 / Q25 nyitott) |
| J5 | **Hong Cheng HC-PZ127-7.2L-2x10PS** | **C41375929** | MAIN dugó; FRONT-aljzat: HC-PM127-4.3H-2x10PS (C27985222); illesztett 5,3 mm → 7,0 mm-es résnél ~2,3 mm merülés [NEM ELLENŐRZÖTT]; generikus land; **Q17 nyitott** (Samtec FTSH-110-02 / FLE-110-01, 7,47 mm → 7,5 mm távtartó + lábkép-csere) |
| C1 | YAGEO CC0603KRX7RABB472 (4,7 nF **200 V** X7R 0603) | C596328 | ≥250 V 0603-ban nincs készleten; 1 kV csak 1206-ban (lábkép-csere, rev B); a séma Value-mezője még „4.7nF 50V” |
| C14 | Samsung CL10B105KA8NNNC (1 µF 25 V X7R 0603) | C29936 | **új**, U3 OUT (TI 8.4.1); opcionális csere 2,2 µF / 25 V X7R |
| C5/C6, C8 | Samsung CL32A226KAJNNNE (22 µF 25 V X5R 1210) · CL21A106KAYNNNE (10 µF 25 V 0805) | C52306 · C15850 | VBUS_SW bulk; a „35–50 V” szabálytól eltér, a 10,87 V-os OVLO mellett elfogadva (`05` §4.1) |
| C12/C13, C20 | CL21A226MAQNNNE (22 µF 25 V 0805) · Murata GRM32ER61C476KE15L (47 µF 16 V 1210) | C45783 · C77101 | 3V3 kimenet / modul bulk; a séma Value-mezői (10 V) a rendeltnél alacsonyabbak |
| R6 | UNI-ROYAL 0603WAF2673T5E (267k 1 %) | **C22963** | **csak 180 db**, más 267k 0603 nincs → foglalni (UVLO-osztó) |
| TH1 | KUU KNTC0603/10KF3950 | C2892547 | B25/85 = **3987 K** (LCSC) – a FW NTC-modellje ezzel számol |
| SW1–3 | Omron B3U-1000P | C231329 | |
| D20 + R30 | KENTO KT-0603G + 1k | C12624 / C21190 | ~0,3–0,5 mA, halvány; opcionális R30 → 470 Ω |

### 0.3 Készlet-foglalás (rendeléskor)
**J2 C5164008 (31 db)**, **U3 C3662799 (~300 db)**, **R6 C22963 (180 db)** – foglalni / előrendelni; Extended-díjak várhatók. Rendelés előtt minden készletet frissíteni; a JLC elhelyezési előnézetében a forgatás és a pin 1 ellenőrzése: U2–U6, D1 (katód = VBUS), D20, J1, J2, J4, J5 és mind a 25 B-oldali alkatrész.

### 0.4 Maradék tulajdonosi döntések
| # | Döntés | Hatás |
|---|---|---|
| Q6 | J2 kontakt-oldal + FFC a valódi kamerával | **a kamera első bekapcsolása előtt**; rossz oldal = 3V3/GND csere a kameránál; a NYÁK-gyártást nem blokkolja (azonos land a bottom-contact változattal) |
| Q17 | J5: Hong Cheng pár marad (MAIN változatlan, a FRONT-aljzat magasságával korrigál) vagy Samtec 7,47 mm | Samtec esetén a MAIN J5 lábképét a **rendelés előtt** cserélni + 7,5 mm-es távtartó |
| U5 | TECH PUBLIC klón elfogadása (pin 3 = GND igazolva) vagy TI C1855726 | rendelés előtt |
| C1 | 200 V-os 0603 elfogadása (rev B: 1206 / 1 kV) | – |
| opcionális | BOM-csere azonos lábképen: **R28 → 4,7k**, **C14 → 2,2 µF / 25 V X7R**, **R30 → 470 Ω** | rendelés előtt, layout-változás nélkül |

## 1. BOM-váz (minden alkatrész-osztály a 05-ből)

| # | Funkció | Osztály / követelmény | MPN | LCSC# | Tok | Footprint forrás | Rev A | Gate |
|---|---|---|---|---|---|---|---|---|
| **Táp** | | | | | | | | |
| 1 | USB-C bemenet J1 | 16 pin USB-C receptacle, USB 2.0, 4 THT shell láb | TYPE-C-31-M-12 (HRO) | C165948 | SMD + THT shell | gyártói / LCSC | FIT | ✅ (köpenylábak: JLC kézi / szelektív vagy saját forrasztás, §0.2) |
| 2 | USB ESD | **3,3 V array, nincs VBUS láb** (TPD2E2U06 / PRTR5V0U2X osztály) [NEM ELLENŐRZÖTT] | TPD2E2U06DCKR-TP (TECH PUBLIC klón) | C5350871 | SC-70-3 | gyártói | FIT | ✅ – lábkiosztás rendelés előtt igazolandó (§0.4) |
| 3 | TVS | SMAJ10A osztály (standoff 10 V; szivárgás 9,45 V / 85 °C) | SMAJ10A-13-F (Diodes) | C134939 | SMA | gyártói | FIT | ✅ (as-built: B, az U3 alatt) |
| 4 | PD sink | **CH224A** (PD3.2 sink, I2C 0x22/0x23, PG open-drain aktív alacsony) – E22 | CH224A | **C42459160** | ESSOP10 | WCH adatlap v2.1 (`ref/datasheets/`) | FIT | ✅ |
| 5 | CH224A feszültség-strap | fix R a 9 V-hoz, soha lebegő | TBD | TBD | 0603 | – | FIT | G1 (2. fejezet S10) |
| 6 | PG pull-up | R a 3V3-ra (polaritás: G1) | TBD | TBD | 0603 | – | FIT | G1 (S9) |
| 7 | Rd ×2 | 5,1k – **csak CH224A nélkül, soha egyszerre** | TBD | TBD | 0603 | – | **DNP** | K-1 |
| 8 | eFuse (fő) | állítható OVP ~10,5–11 V, reverse-blocking, auto-retry, UVLO 4,4/3,9 V, ILIM ~2 A, soft-start (TPS25947 / TPS2595x osztály) [NEM ELLENŐRZÖTT] | TPS259470ARPWR | C3662799 | RPW0010A 2×2 | TI adatlap | FIT | ✅ (készlet ~300 → foglalni) |
| 9 | VBUS_SW bulk | **35–50 V MLCC**, effektív C DC-bias után ≤47 µF összesen. As-built: C5/C6 22 µF 25 V (1210), C8 10 µF 25 V – a 10,87 V-os OVLO mellett villamosan megfelel, de eltér a 35–50 V-os szabálytól (electrical-09) | TBD | TBD | 1210 | – | FIT | G4 |
| 10 | VBUS→VBUS_SW híd | 0 Ω / forrasztóhíd, ≥2 A | TBD | TBD | 1206 | – | **DNP** | K-1 |
| 11 | Buck 3V3 | széles bemenetű, forced-PWM, ≥2 A (TPS62933F osztály) [NEM ELLENŐRZÖTT] | TPS62933FDRLR | C5219272 | SOT583 | gyártói | FIT | ✅ |
| 12 | Buck induktor | 2,2 µH, Isat ≥3,5 A, ≤3,3 mm magas. **A NYÁK-on (L1) generikus `L_Taiyo-Yuden_NR-50xx` lábkép** – a sorozat 4,0 mm-es változata a kamera alá nem fér (mech-09) → MPN-nel együtt rögzítendő | NRS5024T2R2NMGJ (Taiyo) | C222926 | 4,9×4,9×2,4 | gyártói (land: NR-50xx, nem összevetve) | FIT | ✅ (Isat 4,1 A) |
| 13 | Buck CIN / COUT | MLCC, VIN oldal ≥25 V (9,45 V + tüske) | CL32A226KAJNNNE / CL21A106KAYNNNE / CL21A226MAQNNNE | C52306 / C15850 / C45783 | 1210 / 0805 | – | FIT | ✅ |
| 13a | **eFuse OUT kondi (C14, új 2026-10-11)** | ≥1 µF az U3 OUT-on (TI 8.4.1), VBUS_SW → GND | CL10B105KA8NNNC | C29936 | 0603 | – | FIT | ✅ (opc. 2,2 µF / 25 V X7R) |
| 14 | Buck kimeneti 0 Ω | + TP4 (bench betáp, K-1) | TBD | TBD | 0603 | – | FIT | K-1 |
| 15 | Modul 3V3 bulk | **47 µF + 10 µF + 100 nF** a P84–P86 padoknál | TBD | TBD | 1210 / 0805 / 0402 | – | FIT | G4 |
| 16 | CAM_3V3 load switch | **TPS22917DBV** (TPS22918 osztály; 1–5,5 V, 2 A, CT, QOD – a KiCad könyvtár lábkiosztása: 1 VIN, 2 GND, 3 ON, 4 CT, 5 QOD, 6 VOUT); QOD → 0R (R53) → VOUT; CT = 1 nF kiinduló (bring-up 7. lépésben hangolni) | TPS22917DBVR | C2681320 | SOT-23-6 | KiCad Power_Management | FIT | ✅ (U6) |
| 17 | SD_3V3 load switch | **TPS22917DBV** (U8), QOD → R60 0R, CT 1 nF | TPS22917DBVR | TBD | SOT-23-6 | KiCad Power_Management | **DNP** | ✅ típus |
| 18 | IR ág 2. eFuse | **TPS259470ARPW** (U7; 23 V, RILM 6,65k → ILIM 0,50 A (0,425–0,575), auto-retry; EN/UVLO = IR_SW_EN, OVLO → GND); shunt R72 0,1 Ω + TP8A/B; bypass R73 0R | TPS259470ARPW | TBD | RPW0010A | TI adatlap (E22) | **DNP** | ✅ típus |
| 19 | IR biztosított 0 Ω (rev B-s alternatíva; rev A: az egész IR ág DNP) | fused 0 Ω / PTC, ~0,75 A | TBD | TBD | 1206 | – | **DNP** | K-3 |
| 20 | IR shunt + TP8 | MAIN front oldal | TBD | TBD | 1206 | – | **DNP** | G6 (S8) |
| 21 | Supervisor | TPS3840 osztály, **nyílt-drain**, ~3,08 V [NEM ELLENŐRZÖTT] | TBD | TBD | SOT-23-5 | gyártói | **nincs rajzolva → rev B** | K-14 |
| 22 | Supervisor → ESP_EN 0 Ω | | TBD | TBD | 0603 | – | **nincs rajzolva → rev B** | K-14 |
| 22a | **ESP_EN RC** (R23, C25) | **10k → 3V3 + 1 µF → GND**; Q3 (a modul saját EN RC-je) nyitott, de felhúzás nélkül a lap nem indul | 0603WAF1002T5E / CL10A105KB8NNNC | C25804 / C15849 | 0603 ×2 | – | **FIT** (2026-10-10; korábban DNP) | ✅ |
| 23 | VBUS_SW ADC osztó | R12 200k / R13 54,9k (1%) + C7 100 nF → GPIO 20; **3,6 V Zener (D2, BZT52C3V6): DNP** (2026-10-10 – szivárgása a 43 kΩ-os csomóponton a 8 V-os módküszöböt torzítaná) | TBD | TBD | 0603 / SOD-123 | – | FIT (D2: **DNP**) | G4 (S11) |
| 24 | CC-tap ×2 | 100k + 10 nF + 3,6 V Zener → GPIO 21/22 | TBD | TBD | 0603 / SOD-323 | – | **DNP** | K-15 |
| 25 | NTC + osztó | ADC2 (GPIO 49), 100 nF | TBD | TBD | 0603 | – | FIT | G4 (S13) |
| **Modul / MCU** | | | | | | | | |
| 26 | P4 modul | Waveshare ESP32-P4-Module (25×25×3,3, 88 castellated pad) | ESP32-P4-Module | – | castellated | **Waveshare land pattern zip** (G2) | FIT | G2 |
| 27 | VO4 | 1 µF + TP; külső forrás tilos | TBD | TBD | 0603 | – | FIT | – |
| 28 | Strap felhúzások | GPIO36 10k; C6_IO9 10k; **C6_IO8 10k (kötelező)** | TBD | TBD | 0603 | – | FIT | – |
| 29 | BOOT / RESET / USER | SMD tact ×3 – **Omron B3U-1000P** (LCSC C231329; tulajdonosi döntés 2026-10-09, `90-review-log.md`; a sémában még nincs MPN-mező) | B3U-1000P | C231329 | 3,0×2,5 | KiCad (gyári) | FIT | G4 (mező-kitöltés) |
| 30 | Státusz LED + soros R | diszkrét 0603, **MAIN hátoldal** (GPIO 6; J5.17 tartalék) | TBD | TBD | 0603 | – | FIT | G4 |
| 31 | I2C felhúzás | **kamera I/O szint ismerete előtt DNP** | TBD | TBD | 0603 | – | **DNP** | G3 |
| 32 | C6 + UART0 padsor J7 | **as-built: 9 SMD pad, 1,27 mm** (`PadRow_1x09_P1.27mm_SMD`, saját), B oldal, felső él (22,5; 2,0): GND, C6_TXD, C6_RXD, C6_IO9, C6_IO8, GPIO 54 / C6_EN (P82; Q2), UART0 TX, UART0 RX, 3V3-ref (05 §6) | – | – | padsor | saját | **DNP** (header nincs) | K-17 |
| 33 | TP-k (hátoldal) | **as-built: TP1–TP7, TP16A/B, TP17–TP19 = 12 pad** (GND: TP3, TP18, TP19), 10 a 2,75 mm-es pogo-rácson + TP5, TP6 külön; ~~TP9a/b, TP10–TP15, 20 pad / 2,0 mm~~ törölve; TP8A/B a front oldalon, DNP (05 §12) | – | – | Ø1,5 pad | KiCad TestPoint | FIT | – |
| 34 | u.FL J4 | lapszélen (bal él, B), húzásmentesítés; **as-built: J4 + R34 0R FIT** (G2 / Q25 nyitott; a modul IPEX-e alternatíva) | TBD | TBD | u.FL | KiCad (Hirose U.FL-R-SMT-1) | FIT | G2 |
| 35 | π-háló ×3 + CPWG | minden elem 0 Ω / DNP-képes | TBD | TBD | 0603 | – | FIT (0 Ω) | G2 |
| 36 | Antenna ×2 | 2,4 GHz, IPEX Gen1 / u.FL | TBD | – | – | – | beszerzés | G0/G2 |
| **Kamera** | | | | | | | | |
| 37 | J2 FPC 15 pin 1,0 mm | jelöltek: 1.0K-GT-15PB vagy Hirose FH12-15S-1SH [NEM ELLENŐRZÖTT]. **A NYÁK-on a lábkép helyőrző: TE 1-84953-5** (`Connector_FFC-FPC:TE_1-84953-5_1x15-1MP_P1.0mm_Horizontal`, leírása szerint „top-side contacts”); a jelöltek lábképe eltér [NEM ELLENŐRZÖTT]; **kontakt-oldal (Q6) nyitott** – rossz oldal = 3V3/GND csere a kameránál. Döntés a rendelés előtt: vagy a TE 1-84953-5 a megvásárolt alkatrész (JLC-beszerezhetőség ellenőrizve), vagy lábkép-csere a választott MPN-re. A pin ↔ háló térkép (RPi sorrend) ellenőrizve. **2026-10-11: a TE 1-84953-5 a megrendelt alkatrész (lábkép = alkatrész); készlet 31 db → foglalni; Q6 a kamera első bekapcsolása előtt (§0.4)** | 1-84953-5 (TE) | C5164008 | ZIF (slide lock) | KiCad (gyári TE) | FIT | ✅ G4 · Q6: G3 |
| 38 | Vezérlő jel ESD (J2) | alacsony-C array (CAM_PWDN = CAM_IO0, SCL, SDA); 05 §0.1 + 06 §2.2 sor. **Formálisan rev B-re halasztva (2026-10-10):** nincs a sémában; Q6 nyitott, a J2 környéke zsúfolt | TBD | TBD | SOT-xx | – | ~~FIT~~ → **rev B** | rev B |
| 39 | Kamera modul | OV5640 MIPI 2-lane, onboard osc + LDO, **NoIR vagy fix lencse** (rev A) | TBD | – | – | modul STEP | beszerzés | G3 |
| 40 | FFC | szabványos 50 és 100 mm + 25–30 mm egyedi | TBD | – | – | – | beszerzés | G3 |
| **microSD** | | | | | | | | |
| 41 | J3 microSD | push-push (a NYÁK-on Hirose DM3AT-SF-PEJM5 lábkép – leírása „push-pull”, ellenőrizendő, mech-14) | TBD | TBD | SMD | KiCad | **DNP** | K-16 |
| 42 | SD ESD + felhúzások | ESD ≤3,5 pF, felhúzás SD_3V3-ra. **Az SD ESD lábképe nincs a sémában → rev B** (2026-10-10); a felhúzások (R61–R66) DNP lábképpel megvannak | TBD | TBD | – | – | felhúzás: **DNP**; ESD: **rev B** | K-16 |
| **FRONT (G6)** | | | | | | | | |
| 43 | IR LED ×4 | 850 nm, 3535 | TBD | TBD | 3535 | gyártói | G6 | Q19 |
| 44 | IR CC driver ×2 | buck-CC, Vin 4,5–9,45 V (4.2 kritérium) | TBD | TBD | SOT-23-6 | gyártói | G6 | Q19 |
| 45 | NFET ×2 | AO3400 osztály | TBD | TBD | SOT-23 | – | G6 | – |
| 46 | ICR H-híd | DRV8837 osztály, **3V3-ról** | TBD | TBD | TBD | gyártói | **DNP** | rev B |
| 47 | J6 ICR | JST-SH 1,0 mm 2 pin | TBD | TBD | SMD | gyártói | **DNP** | rev B |
| 48 | PDM mikrofon | MSM261D3526H1CPM / MP34DT05-A [NEM ELLENŐRZÖTT] | TBD | TBD | LGA | gyártói | G6 | Q20 |
| 49 | Mikrofon LC + CLK soros R | 33–100 Ω | TBD | TBD | 0603 | – | G6 | – |
| 50 | VEML7700 | DNP, IR-árnyékolt | TBD | TBD | TBD | gyártói | **DNP** | – |
| **Passzív csoportok (R4)** | | | | | | | | |
| 53 | USB-C shield RC | 1 MΩ ‖ 4,7 nF a 4 THT shield láb és GND között (J1; 05 §5, §6; §3 lent); as-built R1 / C1 az F oldalon | 0603WAF1004T5E / CC0603KRX7RABB472 (**200 V**) | C22935 / C596328 | 0603 ×2 | – | FIT | ✅ |
| 54 | GPIO lehúzások | **100k:** GPIO 26 IR_PWM (R24), 27 ICR_IN1 (R25), 28 ICR_IN2 (R26), **53 SD_EN (R27)** – FIT; GPIO 32 IR_SW_EN (R29) – **DNP** az IR ággal. **10k: GPIO 4 CAM_3V3_EN (R28)** – 2026-10-10 (korábban 100k; a GPIO 4 / MTMS reset alatti belső felhúzása [NEM ELLENŐRZÖTT]). ~~GPIO 29 SD_EN, 33 CAM_3V3_EN~~ (v0.6 előtti kiosztás). As-built: MAIN **előlap** (05 §5) | TBD | TBD | 0603 ×6 | – | FIT (GPIO 32: **DNP**) | G4 |
| 55 | UART0 soros R | 1–4,7k ×2 (GPIO 37 TX / 38 RX; 05 §5.1) | TBD | TBD | 0603 ×2 | – | FIT | G4 |
| 56 | GPIO 33 (USER, v0.6) szűrő | 100 nF a pinen (05 §5) | TBD | TBD | 0402 / 0603 | – | FIT | G4 |
| 57 | CH224A tápkondik | VHV 1 µF 50 V (a VBUS láb a VHV-re kötve); beleszámít a ≤10 µF effektív pre-eFuse keretbe (05 §4.1) | – | TBD | 0603 | – | FIT | ✅ (C2) |
| 58 | CAM_3V3 0 Ω mérő-jumper | a load switch után + TP5 (05 §0.1, §12) | TBD | TBD | 0603 | – | FIT | G4 |
| 59 | Buck FB osztó | R1 / R2 (E96) a 3,3 V-hoz | TBD | TBD | 0603 ×2 | – | FIT | G4 (**S1**) |
| 60 | eFuse OVP / UVLO / ILIM ellenállások | OVP osztó, UVLO osztó, R_ILIM (fő eFuse; ~5 db) | TBD | TBD | 0603 | – | FIT | G4 (**S4, S5, S6**) |
| **Mechanika** | | | | | | | | |
| 51 | B2B J5 pár | 2×10, 1,27 mm, **párosított magasság 7 mm**, rövid wipe. **A NYÁK-on generikus lábkép** (`PinHeader_2x10_P1.27mm_Vertical_SMD`), (22,5; 40,2) – ~~a típus (és vele a lábkép) még nincs kiválasztva~~ → **2026-10-11: BOM-ban a Hong Cheng pár (5,3 mm illesztett, ~2,3 mm merülés 7,0 mm-nél); a land generikus maradt; Q17 nyitott (§0.2)** | HC-PZ127-7.2L-2x10PS (Hong Cheng) | C41375929 | SMT | KiCad (generikus) | FIT (MAIN) | Q17 |
| 52 | M2 távtartó ×4 | 7 mm, 33,5 mm raszter + csavarok | TBD | – | – | – | beszerzés | G3 |

## 2. Értékszámítási lap (G4, a sematik előtt)

Minden eredmény **TBD**, amíg a megfelelő típus adatlapja nincs kezünkben; a képletek kiindulási szabályok. A mértékegységek: V, A, Ω.

| # | Paraméter | Képlet / szabály | Bemenet | Eredmény |
|---|---|---|---|---|
| S1 | Buck FB osztó | Vout = Vref·(1 + R1/R2) → R1 = R2·(Vout/Vref − 1) | Vout = 3,3 V; Vref = adatlap (pl. 0,8 V [NEM ELLENŐRZÖTT]); példa R2 = 10k → R1 ≈ 31,25k → E96 sor | TBD (G4) |
| S2 | Buck induktor | L = Vout·(1 − Vout/Vin_max) / (fsw·ΔIL); ΔIL ≈ 0,3·Iout_max; Isat ≥ Iout_max + ΔIL/2 | Vin_max = 9,45 V; Iout_max ≥ 1,1 A (05 4.3), tervezett ≥2 A; fsw = adatlap | TBD; kiinduló 2,2 µH, Isat ≥3,5 A |
| S3 | Buck COUT | adatlap Cout min/max (B-27); ΔVout ≈ ΔIL/(8·fsw·Cout); tranziens: WiFi TX lépcső ~350 mA; **effektív C** DC-bias után | adatlap, MLCC DC-bias görbe | TBD |
| S4 | eFuse OVP | Vovp = Vref_ovp·(1 + R_top/R_bot); cél **10,5–11 V** | Vref_ovp = adatlap | TBD |
| S5 | eFuse UVLO | Vuv(↑) = **4,4 V**, Vuv(↓) = **3,9 V** (osztó vagy fix hiszterézis az adatlapból) | adatlap | TBD |
| S6 | eFuse ILIM | R_ILIM az adatlap táblázatából / képletéből, cél **~2 A**; ellenőrzés: I_inrush = C·dV/dt = 47 µF × 30 mV/µs ≈ **1,41 A** < ILIM ✓ | C_eff ≤47 µF (05 4.1) | TBD (R_ILIM) |
| S7 | IR LED áram | I_LED = Vsense / Rsense → Rsense = Vsense / 0,15 A; P_R = I²·R; fejmagasság: Vin_min − Vsense ≥ Vf_max(−20 °C) + 0,3 V | driver Vsense (adatlap), LED Vf (Q19) | TBD |
| S8 | IR ág ILIM | ILIM (2. eFuse) ≥ 2× a bemeneti csúcsáram: 1,2 W / 4,5 V ≈ 0,27 A → **0,5–0,7 A** ✓; az R_ILIM az adatlapból | 05 4.2 | TBD (R_ILIM) |
| S9 | PG pull-up | R_PU = (V_rail − V_OL) / I_sink; **V_rail = 3V3** (nem VBUS; GPIO max 3,6 V); példa 3,3 V / 10k = 0,33 mA | CH224A PG típus (open-drain?) és polaritás: G1 | TBD (G1) |
| S10 | CH224A strap | a 9 V-hoz tartozó R_cfg az adatlap táblázatából; fix, nem lebegő | CH224A adatlap | TBD (G1) |
| S11 | VBUS_SW osztó | Vadc = Vbus·R2/(R1+R2): 9,45 V × 54/254 = **2,01 V** ✓ (≤3,3 V); Zener szivárgás × R1 hibája | R1 = 200k, R2 = 54k | kész (ellenőrizni) |
| S12 | CC-tap (DNP rev A) | τ = 100k × 10 nF = 1 ms; küszöbök 05 4.3; ADC / Zener szivárgás × 100k hiba | 05 4.1 | rev B |
| S13 | NTC osztó | Vadc = 3,3 V·Rntc/(Rntc + R_ref); R_ref = R25; tartomány 25–85 °C | NTC B-érték (TBD) | TBD |
| S14 | Supervisor küszöb | threshold változat a 3V3 − tűrés alatt, a buck tűrésével összevetve (~3,08 V [NEM ELLENŐRZÖTT]) | buck Vout tűrés | TBD |
| S15 | CAM_3V3 CT | lásd 4. fejezet | | |

## 3. USB-C 16 pin – pin map (K-20) [NEM ELLENŐRZÖTT: a konkrét MPN adatlapján ellenőrizni]

| Csatlakozó pin | Jel | Bekötés |
|---|---|---|
| A1, B12 | GND | GND |
| A4, B9, B4, A9 | VBUS | VBUS (TVS + ESD a csatlakozónál) |
| A5 | CC1 | CH224A CC1 |
| B5 | CC2 | CH224A CC2 |
| **A6 + B6** | D+ | **összekötve** → USB-Serial-JTAG D+ = **GPIO 25 (P51)**, ESD 3,3 V array |
| **A7 + B7** | D− | **összekötve** → USB-Serial-JTAG D− = **GPIO 24 (P50)**, ESD |
| A8, B8 | SBU1, SBU2 | **NC** |
| B1, A12 | GND | GND |
| Shield (4 THT láb) | | 1 MΩ ‖ 4,7 nF → GND (BOM #53) |

Megjegyzések: USB 2.0 only; **CC-n külső Rd nincs** (a CH224A belső Rd-t tartalmaz [NEM ELLENŐRZÖTT]; a 2× 5,1k footprint DNP, csak CH224A nélkül); a CH224A **DP/DM NC**; a 16 pin-es típusoknál az A/B duplikátum pin-ek belül össze lehetnek kötve – az MPN adatlapja szerint; a D± összekötést a lapon kell megoldani, ha a csatlakozó nem köti össze.

## 4. CAM_3V3 load switch – CT / slew és inrush (K-22)

| Elem | Érték / szabály |
|---|---|
| Kapcsoló | TPS22918 osztály, CT lábbal beállítható emelkedési idő [NEM ELLENŐRZÖTT] |
| Cél | a kamera modul bemeneti kapacitásának feltöltése lassan: **I_inrush = C_in·dV/dt ≤ ~0,3 A**, a 3V3 sín esése **≤ ~100 mV** (cél) |
| Számítás | dt ≥ C_in·3,3 V / 0,3 A; példa C_in = 22 µF → dt ≥ ~0,24 ms; **ajánlott slew 0,5–1 ms** |
| CT érték | **TBD (G4)** – az adatlap CT–tR diagramjából / táblázatából; kiinduló jelölt 1 nF [NEM ELLENŐRZÖTT]; C_in a kiválasztott kamera modulból (G3) |
| Mérés | bring-up 7. lépés: szkóp a CAM_3V3 és 3V3 sínen, a 0 Ω mérő-jumperen áram; ha az esés > cél → CT nő |
| Időzítés | táp-sorrend: 3V3 → CAM_IO0 → I2C (05 §7) |

## 5. Footprint-forrás és DFM ellenőrzőlista

- [x] Waveshare ESP32-P4-Module land pattern (DXF) importálva (`Waveshare_ESP32-P4-Module_HandSolder`, 88 pad a DXF-fel egyezik); pad-hosszabbítás 1,5 mm kifelé; a modul alatti viák tentelve (05 3.1); a STEP-import itt nem ellenőrzött
- [x] LCSC# / JLC beültethetőség minden FIT soron (16 Basic / 24 Extended; §0); FPC, u.FL, USB-C külön ellenőrizve; 7 mm-es B2B pár nincs (Q17); USB-C köpenylábak: kézi / szelektív forrasztás
- [ ] Kétoldalas beültetés: mely alkatrészek a hátoldalon (modul kézi, USB-C THT)
- [ ] Footprint-forrás megjelölve minden sorban (gyártói / LCSC / saját); selyem-feliratok: "NEVER BOTH", pin 1, "no hot-plug"
- [x] EDA eszköz kiválasztva: **KiCad** (05 3.1, Q26)
- [ ] Gyártási rendelés (7. kör → 9. kör): stackup **JLC04101H-3313A** név szerint (~~a lapfájlban nincs stackup-blokk~~ → a lapfájlban és a gbrjob-ban már benne van: ENIG, impedancia, Rev A), impedancia-kontroll igény, **ENIG** (a JP1 maszk-gát nélküli 0,3 mm-es rése HASL-lel áthidalódhat), 45 × 45 mm (nem a gbrjob 45,1-e), revízió-felirat (silk: „rev A 2026-10”), **sínek csak a felső / alsó élen** (fiduciálok a sínen), ~~panel-fülek tiltott zónái (jobb él y 16–29, felső él x 10–35)~~ → **a jobb élen y > 5,8 mm és a felső élen x 10–35 mm között nincs fül** (C3 / R10 / C1 0,7–0,8 mm-re a jobb éltől); **csak a rendelés előtti kapu után** (refill + mentés a projektmappában, DRC refill nélkül 0 hiba, Gerber `--check-zones`; 05 §3.1)
- [x] CPL / BOM export: U3 SMD attribútum, U1 + MH1–4 + TP + JP1 kizárva, DNP-attribútumok szinkronban (R4/R5 DNP), U1 és a DNP-lábképek paszta nélkül → **CPL 72 sor (F 47 / B 25)**, `BOM_jlc.csv` 40 sor (`kicad/MAIN/fab/`)
