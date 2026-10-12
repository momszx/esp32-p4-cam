# 08 – Diagramok (Mermaid, v0.4)

Dátum: 2026-10-09 · **v0.4 (2026-10-11): végső rev A as-built – D1 TVS az U3 alatt, U5 / R1 / C1 a front oldalon, új C14, G4 lezárva, G5 rendelés előtti kapu, G5b CSI soak** – lásd „Diagram-javítások (v0.4)” a végén · **v0.3 (2026-10-10): GPIO-kiosztás v0.6 (SD_EN 53, SD_CD 52, CAM_3V3_EN 4, USER 33, EFUSE_FLT 29, PDM_DATA 30), MAIN 45×45 / 4 réteg, as-built TP-k (TP9–TP15 törölve, C6/UART0 a J7 padsoron), 2026-10-10-i döntések (R23/C25 FIT, D2 DNP, R28 10k, kamera vezérlő-ESD → rev B)** – lásd „Diagram-javítások (v0.3)” a végén · Forrás: `05-architektura.md` v0.5 (autoritatív), `06-floorplan-vazlat.md` v0.3, `07-bom-terv.md` v0.2 · **v0.2 (R4): a hibalista javítva, a diagramok a 05/06/07 javított állapotát mutatják** (lásd "Diagram-javítások" a végén) · A diagramok **kizárólag** a 05 táblázataiból / szövegéből épülnek; a 06 és 07 csak a lap-oldal (front / rear) és a pin-térkép kiegészítésére szolgál, ahol a 05 hallgat (ezt az élcímke jelzi).

## Jelmagyarázat (minden diagramra)

| Jelölés | Jelentés |
|---|---|
| Folytonos nyíl, `§n` az élcímkén | a kapcsolat a 05 megadott szakaszában szerepel (`E20` = 05 §1 pad-térkép, `07 §3` = USB-C pin map) |
| Szaggatott nyíl | DNP-ág vagy opcionális kapcsolat (a v0.1 "HIÁNYZIK 05-ből" élei a javítások után mind rögzítve vannak, lásd a hibalistát) |
| Szaggatott **piros** keretű csomópont | rev A **DNP** (05 §0.1; footprint van, nincs beültetve) |
| Szaggatott **kék** keretű csomópont | **később (G6)**, a FRONT lapon (05 §0.1, §0.2) |
| Egyszerű keret | rev A **FIT** |

A modul pad = `P`-szám, processzor láb = `GPIO n` (05 jelölés-szabály). A pin-sorszámozás térbeli elrendezése **[F]** (feltételezés) a footprint-importig (05 §14, 06 §1) – **v0.3: a footprint importálva, a DXF-fel egyezik; a GPIO ↔ pad ↔ háló hozzárendelés a NYÁK U1 padjairól ellenőrizve (05 §5).**

---

## 1. Rendszer blokkdiagram

```mermaid
flowchart LR
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  subgraph MAINL["MAIN lap 45x45, 4 reteg (05 §3, §3.1a)"]
    J1["J1 USB-C 16 pin<br/>USB 2.0 (§6)"]
    TVS["TVS SMAJ10A (D1)<br/>MAIN rear, as-built: az eFuse U3 alatt (§0.1, §4.1)"]
    ESD["USB ESD 3,3 V array (U5)<br/>MAIN front, J1 mellett (§0.1, §5)"]
    PD["CH224A PD sink<br/>belso Rd, PG, strap (§4.1)"]
    EF["eFuse: OVP / UVLO / ILIM<br/>reverse-blocking, MAIN front (§4.1)"]
    BUCK["Buck 3V3<br/>forced-PWM, 2 A+ (§4.1)"]
    VDIV["VBUS_SW ADC oszto<br/>(§4.1)"]
    CAMSW["CAM_3V3 load switch<br/>(§4.1)"]
    SDSW["SD_3V3 load switch<br/>(§4.1)"]:::dnp
    IREF["IR ag (rev A: DNP): 2. eFuse + high-side<br/>+ shunt TP8 + IR_SW_EN lehuzas (§4.2)"]:::dnp
    J2["J2 FPC 15 pin 1,0 mm<br/>(§6)"]
    J3["J3 microSD<br/>(§6)"]:::dnp
    J5["J5 B2B 2x10 1,27 mm<br/>7 mm (§6)"]
    BTN["BOOT / RESET / USER<br/>SW1-SW3 (§6)"]
    NTC["NTC oszto<br/>(§11)"]
    J7["J7 SMD padsor 1x9, 1,27 mm (DNP header)<br/>GND, TXD, RXD, IO9, IO8, GPIO 54 / C6_EN, UART0 TX/RX, 3V3-ref (§6)<br/>TP10-TP15 torolve"]:::dnp
    TPU0["UART0 soros R40/R41 1k<br/>-> J7.7 / J7.8 (§5.1)"]
    J4["J4 u.FL + pi-halo + CPWG<br/>(§6, §13)"]
    SUP["Supervisor + 0R -> ESP_EN<br/>rev B, nincs rajzolva (§5)"]:::dnp
    ENRC["ESP_EN RC: R23 10k + C25 1 uF<br/>FIT 2026-10-10 (§0.1, §5)"]
    SLED["Statusz LED 0603 + soros R<br/>MAIN rear, GPIO 6 (§5)"]
    ESDC["J2 vezerlo-jel ESD<br/>CAM_IO0, SCL, SDA - rev B (07 #38)"]:::dnp
    SHRC["J1 shield: 1 MOhm || 4,7 nF<br/>(§5, 07 #53)"]
    PDN["Lehuzasok: 100k GPIO 26-28, 53; 10k GPIO 4 (FIT)<br/>GPIO 32 (DNP), MAIN front (§5, K-7)"]
    RDF["2x 5,1k Rd footprint<br/>csak CH224A nelkul (K-1)"]:::dnp
    I2CPU["I2C felhuzas SDA/SCL (MAIN)<br/>kamera I/O szintig (§5)"]:::dnp

    subgraph MOD["P4 modul: Waveshare ESP32-P4-Module (E1)"]
      P4["ESP32-P4NRW32<br/>32 MB PSRAM + 16 MB flash"]
      C6["ESP32-C6H8 (belso)<br/>WiFi, esp-hosted"]
      P4 ---|"SDIO slot1 belso, GPIO 14-19 (E5, E18)"| C6
    end
  end

  CAM["Kamera modul OV5640<br/>MIPI 2-lane, onboard osc+LDO (§7)"]

  subgraph FRONTL["FRONT lap 45x45 (05 §3)"]
    IRD["IR CC driver x2 + AO3400 x2<br/>(§4.2)"]:::g6
    IRL["IR LED 850 nm x4 (3535)<br/>(D9)"]:::g6
    MIC["PDM mikrofon + LC<br/>(D7, §4.1)"]:::g6
    VEML["VEML7700<br/>(D7)"]:::dnp
    ICR["ICR H-hid DRV8837 + J6<br/>3V3-rol (§4.2)"]:::dnp
  end

  J1 -->|"VBUS §4.1"| TVS
  TVS -->|"VBUS >=2 via rear->front §4.1"| EF
  TVS -->|"nyers VBUS -> CH224A VDD §4.1"| PD
  J1 -->|"shield §5"| SHRC
  ESDC -.->|"CAM_IO0, SCL, SDA §6 (rev B)"| J2
  PDN ---|"lehuzas §5"| P4
  ENRC ---|"ESP_EN P87 §5"| P4
  RDF -.->|"CC1/CC2, soha CH224A-val egyszerre K-1"| PD
  I2CPU -.->|"SDA/SCL §5"| J2
  J1 <-->|"CC1 / CC2 §4.1"| PD
  PD -->|"PG -> GPIO 31 (P58) §5"| P4
  PD <-->|"I2C 0x22/0x23 CFG2/CFG3 = GPIO 8/7, FW: csak olvasas §5"| P4
  EF -->|"EFUSE_FLT -> GPIO 29 (P56) §5"| P4
  J1 -->|"D+ / D- §5, 07 §3"| ESD
  ESD -->|"USB-Serial-JTAG GPIO 24/25 = P50/P51 §5"| P4
  EF -->|"VBUS_SW §4.1"| BUCK
  EF -->|"VBUS_SW §4.1"| VDIV
  VDIV -->|"ADC GPIO 20 (P29) §5"| P4
  BUCK -->|"3V3 -> P84 VBAT, P85/P86 ESP_3V3 §4.1, E3"| P4
  BUCK -->|"3V3 §4.1"| CAMSW
  P4 -->|"CAM_3V3_EN GPIO 4 (P19) §5"| CAMSW
  CAMSW -->|"CAM_3V3 -> J2 pin 15 §6"| J2
  P4 ==>|"MIPI-CSI 2-lane P41-P46 E20 -> J2 §6 - pad-sorrend eltér (Q24, G3)"| J2
  P4 <-->|"I2C GPIO 7/8 SCCB + CAM_IO0 GPIO 23 §5"| J2
  J2 ---|"15 pin FPC, 25-30 mm / 50-100 mm FFC §3"| CAM
  BUCK -->|"3V3 §4.1"| SDSW
  P4 -->|"SD_EN GPIO 53 (P81) §5"| SDSW
  SDSW -->|"SD_3V3 §4.1"| J3
  P4 -->|"SDMMC slot0 4-bit GPIO 39-44 (P67-P72) §5"| J3
  J3 -->|"SD_CD -> GPIO 52 (P80) §5"| P4
  EF -->|"VBUS_SW §4.1"| IREF
  P4 -->|"IR_SW_EN GPIO 32 (P59) §5"| IREF
  IREF -->|"IR_VIN -> J5 pin 1-2 §6"| J5
  P4 -->|"IR_PWM GPIO 26, ICR_IN1/2 GPIO 27/28 §5"| J5
  P4 -->|"PDM CLK/DATA GPIO 12/30 (I2S0 PDM RX) §5"| J5
  P4 <-->|"I2C GPIO 7/8 (VEML) §5"| J5
  BUCK -->|"3V3 -> J5 pin 10-11 §6"| J5
  P4 -->|"GPIO 6 (P21) -> soros R -> LED §5"| SLED
  J5 -->|"IR_VIN, IR_PWM §4.2"| IRD
  IRD -->|"agankenti CC §4.2"| IRL
  J5 -->|"PDM_CLK, PDM_DAT §6"| MIC
  J5 -->|"SDA, SCL §6"| VEML
  J5 -->|"3V3 J5.10-11 §4.1, §6"| VEML
  J5 -->|"ICR_IN1/2 + 3V3 §6"| ICR
  BTN -->|"GPIO 35, ESP_EN P87, USER GPIO 33 (P60) §5"| P4
  SUP -.->|"0R §5 (rev B)"| P4
  NTC -->|"ADC2 GPIO 49 (P77) §5"| P4
  J7 -.->|"UART P4/P5, IO9 P9, IO8 P10, GPIO 54 / C6_EN (P82; Q2) §6, §10"| C6
  TPU0 -->|"UART0 GPIO 37/38 §10"| P4
  TPU0 -.->|"J7.7 / J7.8"| J7
  C6 -->|"LNA_OUT P2 (E7) §6 J4"| J4
```

Megjegyzések: a státusz LED a MAIN hátoldalán van (GPIO 6 hajtja), a J5.17 tartalék (NC). ~~A TVS + USB ESD a MAIN hátoldalon áll~~ → **as-built (2026-10-11): a D1 TVS a hátoldalon, az eFuse (U3) alatt (6,8 mm-re a J1-től, elfogadott eltérés); az U5 USB ESD és az R1/C1 shield RC a front oldalon, a J1 mellett**; a VBUS 3 via-n jut a front oldali eFuse IN-re. Az "SDIO belső" link a modulon belül van (E5: GPIO 14–19 nincs kivezetve, **következtetés**); a P4–C6 között nincs MAIN-routing (D2). A kamera 3V3-át a CAM_3V3 load switch adja (nem a fő 3V3 sín közvetlenül, §7).

---

## 2. Tápfa

```mermaid
flowchart LR
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  subgraph LEG["Jelmagyarázat"]
    L1["FIT rev A"]
    L2["DNP rev A"]:::dnp
    L3["FRONT, G6"]:::g6
  end

  VBUS["VBUS max 9 V<br/>J1 A4,B9,B4,A9 (07 §3)"]
  TVS["TVS SMAJ10A (D1, rear, az U3 alatt)<br/>+ USB ESD (U5, front) - az eFuse ELOTT (§0.1, §4.1)"]
  CEFF["pre-eFuse C max 10 uF eff<br/>CH224 kondik + TVS Cj (§4.1)"]
  EF["eFuse: OVP 10,5-11 V, UVLO 4,4/3,9 V<br/>ILIM ~2 A, auto-retry (§4.1)"]
  BYP["VBUS -> VBUS_SW 0R / forrasztohid<br/>bypass (K-1)"]:::dnp
  VSW["VBUS_SW"]
  BULK["bulk max 47 uF eff<br/>as-built 25 V MLCC: C5/C6 22 uF, C8 10 uF (§4.1)"]
  C14N["C14 1 uF 25 V X7R az U3 OUT-on<br/>FIT, uj 2026-10-11 (§0.1, §4.1)"]
  BUCK["Buck 3V3 forced-PWM 2 A+<br/>2,2 uH Isat 3,5 A+ (§4.1)"]
  R0["0R a buck kimenetén<br/>(§4.1, §12 TP4)"]
  TP4["TP4 pad (rear pogo): bench betap<br/>ha a 0R nyitva (K-1)"]
  V3["3V3 sin"]
  VDIV["VBUS monitor oszto 200k/54,9k + 100 nF<br/>3,6 V Zener D2: DNP 2026-10-10 (§4.1)"]
  ADC20["GPIO 20 (P29) ADC1"]

  IRSW["IR ag (rev A: DNP, footprint marad):<br/>2. eFuse 18 V+, ILIM 0,5-0,7 A (rev B alt.: fused 0R) (§4.2, D9)"]:::dnp
  SHUNT["shunt + TP8<br/>MAIN front oldal (§4.2, §12)"]:::dnp
  IRVIN["IR_VIN -> J5 pin 1-2 (§6)"]:::dnp
  FIR["FRONT: IR CC driver x2 -> AO3400 x2 -> IR LED x4 (§4.2)"]:::g6
  IRSWEN["IR_SW_EN GPIO 32 (P59)<br/>100k lehuzas MAIN front, DNP az IR aggal (§5)"]:::dnp

  J1CC["J1 CC1 A5 / CC2 B5 (07 §3)"]
  PDI["CH224A<br/>belso Rd, DP/DM NC (§4.1)"]
  STRAP["feszultseg-strap fix R<br/>soha nem lebego (§4.1)"]
  PGN["PG -> GPIO 31 (P58)<br/>pull-up 3V3 + TP17 (§5, §12)"]
  CCTAP["CC-tap 100k+ soros, 10 nF, 3,6 V Zener x2<br/>-> GPIO 21/22 (§4.1, §5)"]:::dnp

  MODP["P4 modul: P84 VBAT, P85/P86 ESP_3V3<br/>47 uF + 10 uF + 100 nF (E3, §4.1)"]
  CAMSW["CAM_3V3 load switch TPS22917 (TPS22918-osztaly)<br/>EN GPIO 4 (P19), 10k lehuzas R28 (§4.1, §5)"]
  TP5["0R meroo-jumper + TP5 (§4.1, §12)"]
  J2P["J2 pin 15 CAM_3V3 (§6)"]
  CAMM["Kamera modul (§7)"]
  SDSW["SD_3V3 load switch kisutessel<br/>EN GPIO 53 (P81), 100k lehuzas R27 (§4.1, §5)"]:::dnp
  SDB["J3 microSD + felhuzasok + ESD (§5)"]:::dnp
  TP6["TP6 SD_3V3 pad (FIT, rear, kulon)<br/>(§12)"]
  MICLC["FRONT: mikrofon LC (J5 3V3) (§4.1)"]:::g6
  ICRH["ICR H-hid FRONT, csak 3V3-rol (§4.1, §4.2)"]:::dnp
  SLED["Statusz LED 0603 + soros R<br/>MAIN rear, GPIO 6 hajtja (§4.1, §5)"]
  RDF["2x 5,1k Rd footprint<br/>csak CH224A nelkul (K-1)"]:::dnp
  I2CPU["I2C felhuzas (MAIN)<br/>kamera I/O szintig (§5)"]:::dnp
  SUP["Supervisor TPS3840-osztaly<br/>-> 0R -> ESP_EN, rev B (§4.1, §5)"]:::dnp
  PU["10k felhuzas: GPIO 36, C6_IO9, C6_IO8 (§5)<br/>+ ESP_EN R23 10k / C25 1 uF FIT (2026-10-10)"]
  PGPU["PG pull-up 3V3-ra (§5)"]
  NTCN["NTC oszto + 100 nF -> GPIO 49 ADC2 (§5, §11)"]
  VEML["VEML7700 DNP (FRONT, J5 3V3) (D7)"]:::dnp
  VO4["P66 ESP_LDO_VO4: 1 uF + TP7<br/>kulso forras tilos (§5)"]
  MODI["P4 modul belso LDO"]

  VBUS -->|"§4.1"| TVS
  TVS -->|"VBUS >=2 via rear->front §4.1"| CEFF
  CEFF -->|"§4.1"| EF
  VBUS -->|"bypass K-1"| BYP
  BYP -->|"K-1"| VSW
  EF -->|"§4.1"| VSW
  VSW -->|"§4.1"| BULK
  VSW -->|"U3 OUT §4.1"| C14N
  VSW -->|"§4.1"| BUCK
  BUCK -->|"§4.1"| R0
  R0 -->|"§4.1"| V3
  TP4 -->|"K-1"| V3
  VSW -->|"§4.1"| VDIV
  VDIV -->|"§4.1"| ADC20
  VSW -->|"§4.1, §4.2"| IRSW
  IRSW -->|"§4.2"| SHUNT
  SHUNT -->|"§4.2"| IRVIN
  IRVIN -->|"B2B §4.2"| FIR
  IRSWEN -->|"engedelyezes §5"| IRSW

  J1CC <-->|"§4.1"| PDI
  STRAP -->|"§4.1"| PDI
  PDI -->|"PG §4.1"| PGN
  J1CC -->|"CC-tap §4.1"| CCTAP
  TVS -->|"nyers VBUS -> CH224A VDD (TVS utan, eFuse elott) §4.1"| PDI
  J1CC -.->|"K-1"| RDF
  V3 -->|"§5"| PGPU
  PGPU -->|"§5"| PGN

  V3 -->|"P84-P86 §4.1"| MODP
  V3 -->|"§4.1"| CAMSW
  CAMSW -->|"§4.1"| TP5
  TP5 -->|"§6"| J2P
  J2P -->|"§6"| CAMM
  V3 -->|"§4.1"| SDSW
  SDSW -->|"§4.1"| SDB
  SDSW -->|"SD_3V3 §12"| TP6
  V3 -->|"B2B J5 pin 10-11 §6"| MICLC
  V3 -->|"B2B J5 pin 11 §6"| ICRH
  V3 -->|"3V3 logika; GPIO 6 hajtja §4.1, §5"| SLED
  V3 -.->|"§5"| I2CPU
  V3 -.->|"§4.1 (rev B)"| SUP
  V3 -->|"§5"| PU
  MODI -->|"belso (E9)"| VO4
  V3 -->|"NTC osztó tápja 3V3 §4.1, 07 S13"| NTCN
  V3 -->|"3V3 via J5 pin 10-11 (FRONT) §4.1, §6"| VEML
```

Megjegyzés: a supervisor, ICR, VEML7700, NTC és a státusz LED ágak a 05 §4.1 fa 3V3 alatti listájából valók (a "LED-ek" sor a státusz LED-re pontosítva: MAIN hátoldal, GPIO 6); a FRONT oldali fogyasztók a 3V3-at a J5 pin 10–11-en át kapják (§6).

---

## 3. Jel / net térkép a P4 modul padjairól

```mermaid
flowchart LR
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  subgraph USB["USB-Serial-JTAG (§5, E10)"]
    A24["GPIO 24 / P50"]
    A25["GPIO 25 / P51"]
    A4849["P48 / P49 USB HS PHY"]
    AJ1["J1 A7+B7 D-<br/>ESD 3,3 V array (07 §3)"]
    AJ2["J1 A6+B6 D+<br/>ESD 3,3 V array (07 §3)"]
    ANC["NC - nem hasznalt (§5)"]
    A24 -->|"USB_DM"| AJ1
    A25 -->|"USB_DP"| AJ2
    A4849 -->|"NC"| ANC
    ASH["J1 shield 4 THT lab<br/>1 MOhm || 4,7 nF -> GND (07 #53)"]
  end

  subgraph CAMG["Kamera J2 (§5, §6)"]
    BCSI["P41-P46 CSI D0N D0P CLKP CLKN D1N D1P"]
    BJ2CSI["J2 pin 2,3,5,6,8,9<br/>(5. diagram)"]
    B7["GPIO 7 / P22"]
    B8["GPIO 8 / P23"]
    B23["GPIO 23 / P32"]
    B4["GPIO 4 / P19"]
    BSDA["J2 pin 14 SDA"]
    BSCL["J2 pin 13 SCL"]
    BIO0["J2 pin 11 CAM_IO0 PWDN/EN<br/>pull = TBD Q5"]
    BSW["CAM_3V3 load switch EN<br/>10k lehuzas R28 MAIN front"]
    BESD["J2 vezerlo-jel ESD<br/>CAM_IO0, SCL, SDA - rev B (07 #38)"]:::dnp
    BI2CPU["I2C felhuzas SDA/SCL (MAIN)<br/>DNP, kamera I/O szintig (§5)"]:::dnp
    BP15["J2 pin 15 CAM_3V3"]
    BP12["J2 pin 12 CAM_IO1"]
    BNC["NC (§6)"]
    BCSI ==>|"MIPI-CSI 2-lane; pad-sorrend eltér (Q24, G3; 5. diagram)"| BJ2CSI
    BIO0 -.- BESD
    BSDA -.- BESD
    BSCL -.- BESD
    BI2CPU -.-> BSDA
    BI2CPU -.-> BSCL
    B7 -->|"I2C SDA"| BSDA
    B8 -->|"I2C SCL"| BSCL
    B23 -->|"CAM_IO0"| BIO0
    B4 -->|"CAM_3V3_EN"| BSW
    BSW -->|"CAM_3V3 §6"| BP15
    BP12 -->|"NC"| BNC
  end

  subgraph SDG["microSD J3 - rev A DNP (§5, E17)"]
    C39["GPIO 39 / P67"]:::dnp
    C40["GPIO 40 / P68"]:::dnp
    C41["GPIO 41 / P69"]:::dnp
    C42["GPIO 42 / P70"]:::dnp
    C43["GPIO 43 / P71"]:::dnp
    C44["GPIO 44 / P72"]:::dnp
    C53["GPIO 53 / P81"]:::dnp
    C52["GPIO 52 / P80"]:::dnp
    CJ3["J3 DAT0 DAT1 DAT2 DAT3 CLK CMD<br/>felhuzas SD_3V3-ra, ESD: rev B"]:::dnp
    CSW["SD_3V3 load switch EN<br/>100k lehuzas R27 (FIT)"]:::dnp
    CCD["J3 CD felhuzas a fo 3V3-ra"]:::dnp
    C39 -->|"SD_D0"| CJ3
    C40 -->|"SD_D1"| CJ3
    C41 -->|"SD_D2"| CJ3
    C42 -->|"SD_D3"| CJ3
    C43 -->|"SD_CLK"| CJ3
    C44 -->|"SD_CMD"| CJ3
    C53 -->|"SD_EN"| CSW
    C52 -->|"SD_CD"| CCD
  end

  subgraph B2BG["B2B J5 -> FRONT (§5, §6)"]
    D26["GPIO 26 / P53"]
    D27["GPIO 27 / P54"]
    D28["GPIO 28 / P55"]
    D12["GPIO 12 / P27"]
    D30["GPIO 30 / P57"]
    D78["GPIO 7 / P22 es GPIO 8 / P23"]
    DJ5["J5 pin 5 IR_PWM<br/>100k lehuzas MAIN front"]
    DJ7["J5 pin 7 ICR_IN1 (ICR DNP)<br/>100k lehuzas MAIN front, FIT"]:::dnp
    DJ8["J5 pin 8 ICR_IN2 (ICR DNP)<br/>100k lehuzas MAIN front, FIT"]:::dnp
    DJ13["J5 pin 13 PDM_CLK_J5<br/>soros R70 47R a forrasnal"]
    DJ16["J5 pin 16 PDM_DAT"]
    DJ17["J5 pin 17 tartalek (NC)"]
    DJ1920["J5 pin 19 SDA / pin 20 SCL<br/>-> VEML7700 DNP"]
    D26 -->|"IR_PWM LEDC 40 kHz+"| DJ5
    D27 -->|"ICR_IN1"| DJ7
    D28 -->|"ICR_IN2"| DJ8
    D12 -->|"PDM CLK I2S0"| DJ13
    D30 -->|"PDM DATA"| DJ16
      D78 -->|"I2C"| DJ1920
  end

  subgraph MON["Mérés / vezérlés (§5)"]
    E20["GPIO 20 / P29"]
    E21["GPIO 21 / P30"]
    E22["GPIO 22 / P31"]
    E31["GPIO 31 / P58"]
    E32["GPIO 32 / P59"]
    E49["GPIO 49 / P77"]
    E33["GPIO 33 / P60"]
    E29["GPIO 29 / P56"]
    EEN["ESP_EN / P87"]
    EVB["VBUS_SW oszto 200k/54,9k + 100 nF<br/>Zener D2 DNP"]
    ECC1["CC1 tap 100k+ + 10 nF + Zener<br/>rev A: a CC1_ADC halonak nincs reze"]:::dnp
    ECC2["CC2 tap 100k+ + 10 nF + Zener"]:::dnp
    EPG["CH224A PG, pull-up 3V3, TP17"]
    EIR["IR eFuse2 / kapcsolo EN<br/>100k lehuzas MAIN front, DNP az IR aggal"]:::dnp
    E6["GPIO 6 / P21"]
    ELED["Statusz LED 0603 + soros R<br/>MAIN rear (FIT)"]
    EPD["Lehuzasok: 100k GPIO 26-28, 53; 10k GPIO 4 - FIT;<br/>GPIO 32 DNP; MAIN front (K-7)"]
    ENTC["NTC oszto + 100 nF, ADC2"]
    EUSR["USER gomb SW3 GND-re<br/>belso felhuzas + C40 100 nF"]
    EFLT["eFuse ~FLT (TPS259470A)<br/>open-drain, 10k felhuzas R11"]
    ERST["RESET gomb SW2 + R23 10k / C25 1 uF FIT<br/>supervisor rev B; TP16A ESP_EN"]
    E20 -->|"ADC1"| EVB
    E21 -->|"ADC1"| ECC1
    E22 -->|"ADC1"| ECC2
    E31 -->|"PD PG"| EPG
    E32 -->|"IR_SW_EN"| EIR
    E49 -->|"NTC ADC2"| ENTC
    E6 -->|"statusz LED"| ELED
    E33 -->|"User gomb"| EUSR
    EFLT -->|"EFUSE_FLT"| E29
    EEN -->|"reset"| ERST
  end

  subgraph C6G["C6 programozo header / pogo (§10, §12, E6)"]
    F5["P5 C6_U0TXD"]
    F4["P4 C6_U0RXD"]
    F9["P9 C6_IO9"]
    F10["P10 C6_IO8"]
    F82["GPIO 54 / C6_EN (P82) - Q2"]
    FJTAG["P11-P14 C6 JTAG IO7..IO4"]
    FTP10["J7.2 C6_TXD (TP10 torolve)"]
    FTP11["J7.3 C6_RXD (TP11 torolve)"]
    FTP12["J7.4 C6_IO9<br/>10k felhuzas R21, jumper GND-re (TP12 torolve)"]
    FPU8["10k felhuzas R22 3V3-ra, kotelezo; J7.5"]
    FTP13["J7.6 GPIO 54 / C6_EN (P82; Q2) (TP13 torolve)"]
    FJ7["J7 SMD padsor 1x9, 1,27 mm, DNP header: GND, TXD, RXD, IO9, IO8,<br/>GPIO 54 / C6_EN, UART0 TX/RX, 3V3-ref (§6)"]:::dnp
    FNC["v1-ben nincs kivezetve (F-25)"]
    F5 -->|"C6 TX"| FTP10
    F4 -->|"C6 RX"| FTP11
    F9 -->|"C6 BOOT"| FTP12
    F10 -->|"strapping"| FPU8
    F82 -->|"C6_EN"| FTP13
    FJTAG -->|"NC"| FNC
  end

  subgraph STRP["Strapping GPIO 34-38 (§5.1)"]
    G34["GPIO 34 / P61"]
    G35["GPIO 35 / P62"]
    G36["GPIO 36 / P63"]
    G37["GPIO 37 / P64"]
    G38["GPIO 38 / P65"]
    G34N["NC, nincs terheles"]
    G35B["BOOT gomb SW1 GND-re<br/>+ TP16B GPIO 35"]
    G36P["10k felhuzas 3V3"]
    G37T["R40 1k -> J7.7 UART0 TX (TP14 torolve)"]
    G38T["R41 1k -> J7.8 UART0 RX (TP15 torolve)"]
    G34 -->|"NC"| G34N
    G35 -->|"BOOT"| G35B
    G36 -->|"BOOT_EN"| G36P
    G37 -->|"UART0 TX"| G37T
    G38 -->|"UART0 RX"| G38T
  end

  subgraph RFP["RF es tap padok (E3, E7, E20)"]
    H2["P2 LNA_OUT"]
    H84["P84 VBAT"]
    H85["P85 / P86 ESP_3V3"]
    H66["P66 ESP_LDO_VO4"]
    HRF["pi-halo: R34 0R FIT, C27/C28 DNP -> 50 Ohm vonal -> J4 u.FL (FIT)<br/>vagy a modul IPEX-e (G2)"]
    H3V3["3V3 sin<br/>47 uF + 10 uF + 100 nF"]
    HVO["1 uF + TP7, kulso forras tilos"]
    H2 -->|"RF"| HRF
    H84 -->|"3V3"| H3V3
    H85 -->|"3V3"| H3V3
    H66 -->|"VO4"| HVO
  end

  subgraph FREE["Szabad / nem hasznalt (§5)"]
    Z1["GPIO 0 P88, GPIO 1 P16, GPIO 2, 3, 5 P17, P18, P20, GPIO 13 P28<br/>GPIO 9-11 P24-P26, GPIO 50-51 P78-P79<br/>-> szabad (v0.6)"]
    Z2["GPIO 45-48 P73-P76 -> NC, VO4 domain<br/>(GPIO 45: sdkconfig SD power-reset felulirando)"]
    Z3["P6-P8 C6_IO15..13 NC; P11-P14 C6 JTAG NC (rev A);<br/>P34-P39 DSI NC (§5)"]
    Z4["GND padok P1, P3, P15, P33, P40, P47, P52, P83 -> GND (§5)"]
  end
```

Megjegyzés: a pad-szám minden sorban a 05 §5 / E20 szerint van; a GPIO ↔ pad összerendelést ellenőriztem (nincs eltérés, lásd a végén).

---

## 4. B2B J5 2×10 pinout (MAIN → FRONT)

```mermaid
flowchart LR
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  subgraph SRC["MAIN oldali forras (§5, §4.1, §4.2)"]
    SIR["IR_VIN: IR eFuse2 / fused 0R kimenet<br/>rev A DNP (§4.2)"]:::dnp
    SGND["MAIN GND"]
    S26["GPIO 26 / P53 IR_PWM"]
    S27["GPIO 27 / P54 ICR_IN1"]:::dnp
    S28["GPIO 28 / P55 ICR_IN2"]:::dnp
    S3V3["MAIN 3V3 sin (buck)"]
    S12["GPIO 12 / P27 PDM CLK<br/>R70 47R -> PDM_CLK_J5"]
    S30["GPIO 30 / P57 PDM DATA"]
    S7["GPIO 7 / P22 SDA<br/>kozos busz: kamera + CH224A"]
    S8["GPIO 8 / P23 SCL<br/>kozos busz: kamera + CH224A"]
  end

  subgraph PINS["J5 pinek (§6 tabla: sor, paratlan / paros)"]
    P1["J5.1 IR_VIN"]
    P2["J5.2 IR_VIN"]
    P3["J5.3 GND"]
    P4["J5.4 GND"]
    P5["J5.5 IR_PWM"]
    P6["J5.6 GND"]
    P7["J5.7 ICR_IN1"]
    P8["J5.8 ICR_IN2"]
    P9["J5.9 GND"]
    P10["J5.10 3V3"]
    P11["J5.11 3V3"]
    P12["J5.12 GND"]
    P13["J5.13 PDM_CLK"]
    P14["J5.14 GND"]
    P15["J5.15 GND"]
    P16["J5.16 PDM_DAT"]
    P17["J5.17 tartalek (NC)"]
    P18["J5.18 GND"]
    P19["J5.19 SDA"]
    P20["J5.20 SCL"]
  end

  subgraph DST["FRONT oldali cel (§4.2, §6, D7)"]
    TIR["IR CC driver x2 bemenet<br/>+ lokalis 10 uF + 100 nF"]:::g6
    TGND["FRONT GND"]
    TPWM["AO3400 x2 (soros NFET dimming)<br/>PWM bemenet"]:::g6
    TIN1["DRV8837 IN1 (J6 ICR)"]:::dnp
    TIN2["DRV8837 IN2 (J6 ICR)"]:::dnp
    T3V3["FRONT 3V3: ICR H-hid tap, mikrofon LC"]:::g6
    TCLK["PDM mikrofon CLK<br/>soros 33-100 R"]:::g6
    TDAT["PDM mikrofon DATA"]:::g6
    TSDA["VEML7700 SDA (DNP)"]:::dnp
    TSCL["VEML7700 SCL (DNP)"]:::dnp
  end

  SIR --> P1
  SIR --> P2
  SGND --> P3
  SGND --> P4
  SGND --> P6
  SGND --> P9
  SGND --> P12
  SGND --> P14
  SGND --> P15
  SGND --> P18
  S26 --> P5
  S27 --> P7
  S28 --> P8
  S3V3 --> P10
  S3V3 --> P11
  S12 --> P13
  S30 --> P16
  S7 --> P19
  S8 --> P20

  P1 --> TIR
  P2 --> TIR
  P3 --> TGND
  P4 --> TGND
  P6 --> TGND
  P9 --> TGND
  P12 --> TGND
  P14 --> TGND
  P15 --> TGND
  P18 --> TGND
  P5 --> TPWM
  P7 --> TIN1
  P8 --> TIN2
  P10 --> T3V3
  P11 --> T3V3
  P13 --> TCLK
  P16 --> TDAT
  P19 --> TSDA
  P20 --> TSCL
```

Megjegyzések (05 §6 szerint): **as-built: J5 az F alsó élén, (22,5; 40,2), pin 1 (16,785; 42,15) – a FRONT párja ugyanezen X/Y-on (05 §3.1a)**; csak logika + táp; GND a PDM CLK és IR PWM körül; rail-enként ≥2 pin (IR_VIN 2, 3V3 2, GND 8); a J5.17 tartalék (NC) – a státusz LED a MAIN hátoldalán van (GPIO 6); pin 1 / tükrözés a papír-próbán (P-22). A **VEML INT-nek nincs J5 pinje** (05 §5, GPIO 0 szabad), így nincs hozzárendelve.

---

## 5. Kamera J2 15 pin – CSI pad-sorrend és a Q24 eltérés

Piros / narancs él = a pad-sorrend és a J2 sorrend eltérése (05 E20, §6 "CSI pad-sorrend vs J2", Q24, 06-K14). **Piros**: a CLK pár P/N sorrendje fordított (modulon P,N; J2-n N,P) **és** a pár helye is cserélődik; **narancs**: a D1 pár helye cserélődik a CLK párral (D0–CLK–D1 vs D0–D1–CLK).

```mermaid
flowchart LR
  subgraph MODPADS["P4 modul CSI padok - E20 sorrend"]
    M41["P41 CSI_D0N"]
    M42["P42 CSI_D0P"]
    M43["P43 CSI_CLKP"]
    M44["P44 CSI_CLKN"]
    M45["P45 CSI_D1N"]
    M46["P46 CSI_D1P"]
  end

  subgraph J2PINS["J2 FPC 15 pin - RPi sorrend (§6)"]
    J1["J2.1 GND"]
    J2["J2.2 D0_N"]
    J3["J2.3 D0_P"]
    J4["J2.4 GND"]
    J5["J2.5 D1_N"]
    J6["J2.6 D1_P"]
    J7["J2.7 GND"]
    J8["J2.8 CLK_N"]
    J9["J2.9 CLK_P"]
    J10["J2.10 GND"]
    J11["J2.11 CAM_IO0 PWDN/EN"]
    J12["J2.12 CAM_IO1 LED, NC"]
    J13["J2.13 SCL"]
    J14["J2.14 SDA"]
    J15["J2.15 CAM_3V3"]
  end

  M41 -->|"D0_N"| J2
  M42 -->|"D0_P"| J3
  M43 ==>|"CLK_P -> J2.9: pozicio + P/N csere (Q24)"| J9
  M44 ==>|"CLK_N -> J2.8: pozicio + P/N csere (Q24)"| J8
  M45 ==>|"D1_N -> J2.5: pár-keresztezes (Q24)"| J5
  M46 ==>|"D1_P -> J2.6: pár-keresztezes (Q24)"| J6

  GNDN["GND (P40, P47 padok E20; sik GND)"]
  GNDN --> J1
  GNDN --> J4
  GNDN --> J7
  GNDN --> J10

  G8["GPIO 8 / P23 I2C SCL"] --> J13
  G7["GPIO 7 / P22 I2C SDA"] --> J14
  G23["GPIO 23 / P32 CAM_IO0"] --> J11
  NC12["NC (§6)"] --> J12
  CAMSW["CAM_3V3 load switch kimenet + TP5"] --> J15

  linkStyle 2,3 stroke:#d00000,stroke-width:4px
  linkStyle 4,5 stroke:#e67e00,stroke-width:4px
```

Opciók a keresztezésre (05 §6): (a) a modul sorrendjéhez illő kamera / FFC adapter; (b) CSI lane / polaritás csere a P4-ben (TRM, **[NEM ELLENŐRZÖTT]**, nem építünk rá); (c) szimmetrikus via-keresztezés a J2 padoknál (rev A mérés). A 05 §13 szabálya ("jelenként max 1 rétegváltás") és a keresztezés ütközne: a 05 §13 kivétel-javaslatot rögzít (a J2 padoknál +1 szimmetrikus via-pár; hibalista 15. ✅). A végleges döntés a **G3-ban** van (kamera kiválasztva), a G2 csak a footprint térbeli sorrendjét adja (hibalista 16. ✅).

---

## 6. NYÁK stack oldalnézet (elölről hátra)

```mermaid
flowchart TB
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  FWD(["ELORE: lencse irany"])

  subgraph FE["FRONT elulso oldal (05 §3, 06 §2.3)"]
    FE0["Lencse-kivagas 16x16 mm, R1 sarok<br/>holder 14x14 + hordo atnyul (A variacio)"]
    FE1["IR LED x4 3535 (2,0 mm)"]:::g6
    FE3["PDM mikrofon, jobb sav + akusztikai port"]:::g6
    FE4["VEML7700 DNP + IR-arnyekolo Cu gyuru"]:::dnp
  end

  FPCB["FRONT NYAK 1,0 mm, 2 reteg (ha eleg)"]

  subgraph FB["FRONT hatoldal (05 §3, 06 §2.4)"]
    FB1["B2B 2x10 fej + 10 uF + 100 nF"]:::g6
    FB2["IR CC driver x2 + AO3400 x2 (2,1 mm)"]:::g6
    FB3["DRV8837 + J6 ICR"]:::dnp
    FB4["Mikrofon LC + CLK soros R"]:::g6
  end

  subgraph GAP["Res G = 7,0 mm (05 §3)"]
    CAM["Kamera modul NYAK 1,2 + hatoldali alk. 2,0 = 3,2 mm<br/>a FRONT hatso sikjahoz fekszik"]
    SP["M2 tavtarto x4, 33,5 mm raszter (szerkezeti elem)<br/>kozeppont (22,5; 25,0) - 2,5 mm-rel a lapkozep alatt (05 §3.1a)"]
    B2B["J5 B2B parosított magasság 7 mm"]
    FFC["Kamera FPC: zart stack 25-30 mm<br/>bring-up 50-100 mm FFC, nyitott stack"]
    LIM["MAIN alkatresz a kamera alatt max 3,3 mm = G - 3,2 - 0,5"]
  end

  subgraph MF["MAIN front oldal (05 §3, 06 §2.2)"]
    MF1["J2 FPC 15 pin"]
    MF2["J5 B2B aljzat (3,5 mm)"]
    MF3["CH224A PD blokk"]
    MF4["eFuse blokk + C14 + bulk (as-built 25 V)"]
    MF13["USB ESD U5 + shield RC R1/C1 (J1 kozeleben)"]
    MF5["Buck + induktor 2,8 mm"]
    MF6["VBUS_SW oszto, NTC"]
    MF7["CAM_3V3 load switch"]
    MF8["IR ag: 2. eFuse + shunt + TP8 (rev A DNP; TP8 front)"]:::dnp
    MF9["microSD J3 + SD_3V3 blokk"]:::dnp
    MF10["J2 vezerlo-jel ESD - rev B"]:::dnp
    MF11["0 Ohm merojumperek (R16 3V3, R50 CAM_3V3; a TP pad hatul)"]
    MF12["GPIO lehuzasok: 100k GPIO 26-28, 53; 10k GPIO 4<br/>(GPIO 32 DNP)"]
  end

  MPCB["MAIN NYAK 45x45, 4 reteg, 0,97 mm<br/>JLC04101H-3313A"]

  subgraph MR["MAIN hatoldal REAR (05 §3, 06 §2.1)"]
    MR1["P4 modul 3,3 mm + 3V3 bulk 47+10 uF + 100 nF"]
    MR2["USB-C J1 3,2 mm"]
    MR3["D1 TVS az U3 eFuse alatt, 6,8 mm a J1-tol (as-built, 05 §0.1, §4.1); VBUS 3 via az U3 IN-re"]
    MR4["u.FL J4 + pi-halo"]
    MR5["BOOT / RESET / USER 2,0 mm"]
    MR6["TP-k: TP1-TP7, TP16A/B, TP17-TP19 = 12 pad, 3 GND (TP8 front, DNP)"]
    MR9["Statusz LED 0603 + R (GPIO 6)"]
    MR7["C6 / UART0 padsor J7 (DNP header)"]:::dnp
    MR8["Supervisor + 0R (rev B)"]:::dnp
  end

  BACK(["HATRA"])

  FWD --> FE
  FE -->|"+ 1,0 mm"| FPCB
  FPCB -->|"hatulso sik"| FB
  FB -->|"7,0 mm"| GAP
  GAP -->|"kamera alatt max 3,3 mm"| MF
  MF -->|"+ 1,0 mm"| MPCB
  MPCB --> MR
  MR --> BACK
```

Összvastagság (06 §3.1): lencse nélkül 2,0 + 1,0 + 7,0 + 1,0 + 3,3 = **14,3 mm**; M12 lencsével **29,3 mm**; Ø8 AF hordóval **17,8 mm**.

---

## 7. Programozás és helyreállítás

```mermaid
flowchart TD
  S0(["Kiindulas: uj MAIN, P4 modul beforrasztva"])

  subgraph P4F["P4 elso flash (05 §10, E10)"]
    A1["USB-C J1 -> USB-Serial-JTAG GPIO 24/25 (P50/P51)<br/>esptool flash, konzol, JTAG - nincs USB-UART chip"]
    A2{"USB enumeral es az eFuse engedi?"}
    A3["BOOT gomb: GPIO 35 low, GPIO 36 10k felhuzva<br/>+ RESET (ESP_EN P87) -> download mod (E8)"]
    A4{"sikeres?"}
    A5["UART0: GPIO 37 TX / GPIO 38 RX<br/>J7.7 / J7.8 padok, soros R40/R41 1k (E-25; TP14/TP15 torolve)"]
    A6(["P4 flash kesz"])
  end

  subgraph C6F["C6 elso flash (05 §10, F-21 / F-22)"]
    C1["1. P4 resetben tartasa (ESP_EN lehuzva)<br/>GPIO 54 / C6_EN (P82) nem hajtja a C6_EN-t (Q2 nyitott)"]
    C2["2. USB-UART 3,3 V: C6_U0TXD P5 / C6_U0RXD P4 / GND<br/>J7.2 / J7.3 / J7.1 (SMD padsor 1,27 mm; TP10-TP11 torolve)"]
    C3["3. C6_IO9 (P9, J7.4) -> GND jumper/pogo<br/>GPIO 54 / C6_EN (P82, J7.6; Q2) rovid lehuzas -> felengedes: download mod"]
    C4["4. esptool chip-id + flash-id<br/>gyari FW verzio lekerdezese / mentese flash elott"]
    C5["5. slave FW iras, IO9 jumper el, reset"]
    C6OK(["C6 slave FW kesz"])
  end

  subgraph OTA["Tovabbi frissites (05 §9, D8)"]
    O1["P4 OTA: HTTPS -> inaktiv OTA partíció (ota_0 / ota_1)<br/>otadata valtas az utolso lepes, rollback"]
    O2{"C6 gyari FW OTA-kepes? (Q16, 00-K8 kapu)"}
    O3["C6 OTA esp-hosted slave OTA a P4-rol<br/>c6fw partíció vagy HTTPS"]
    O4["Nem frissitheto terepen USB/UART nelkul:<br/>C6 FW verzio rogzitve, P4 app csak kompatibilis C6-tal fut"]
    O5["Bring-up 11. lepes: OTA + rollback + OTA kozbeni PD hard reset"]
  end

  REC["P4 helyreallitas: BOOT / RESET a hatoldalon elerhetok tokozva is<br/>UART0 tartalek pad (05 §10)"]

  S0 --> A1
  A1 --> A2
  A2 -->|"igen"| A6
  A2 -->|"nem"| A3
  A3 --> A4
  A4 -->|"igen"| A6
  A4 -->|"nem"| A5
  A5 --> A6
  A6 -->|"C6 meg ures vagy ismeretlen FW"| C1
  C1 --> C2
  C2 --> C3
  C3 --> C4
  C4 --> C5
  C5 --> C6OK
  C6OK --> O1
  O1 --> O2
  O2 -->|"igen"| O3
  O2 -->|"nem"| O4
  O3 --> O5
  O4 --> O5
  A6 -.->|"hiba eseten"| REC
  REC -.-> A3
```

---

## 8. Bring-up kapuk G0–G6 (G5b-vel; 05 §0.2)

```mermaid
flowchart TD
  classDef gate fill:#f6f8fa,stroke:#57606a,stroke-width:2px,color:#000

  G0["G0 Dev-kit stream + aram (K-2)<br/>OV5640 MIPI -> ISP -> H.264 -> RTSP esp-hosted C6 WiFi-n<br/>24 h soak, aram allapotonkent, RSSI, sdkconfig + verziok befagyasztasa<br/>Kilepes: stabil stream 24 h, mert tablazat lecsereli a 4.3 becsleseket"]:::gate
  G1["G1 CH224A breakout bench teszt (K-4)<br/>MacBook, olcso PD toltő, USB-A->C kabel<br/>Kilepes: 9 V stabil, PG szint ismert, nincs 20 V, strap-tabla igazolva (Q13)"]:::gate
  G2["G2 Modul sematik + footprint + antenna-dontes<br/>Q1-Q3, Q9-Q11, footprint import (a G2 csak a modul footprintet / sematikat szallitja), antenna (K-6)<br/>Kilepes: footprint + 1:1 papirproba, antenna-dontes, supervisor beultetesi dontes"]:::gate
  G3["G3 Kamera modul befagyasztva + CSI / J2 dontes (Q24)<br/>NoIR / fix lencse, 15 pin, onboard osc + LDO, CAM_IO0 polaritas, I/O szint, STEP, FFC hosszak<br/>vegleges CSI pad-sorrend / J2 pinout (kamera + G2 footprint + TRM lane-csere ellenorzes + via-keresztezes)<br/>Kilepes: egy modul kivalasztva, GPIO 23 pull (Q5) es a CSI / J2 sorrend eldontve"]:::gate
  G4["G4 BOM-lap kesz (07), ellenallas-szamitasok a sematik elott (K-8)<br/>Kilepes: nincs TBD a rev A FIT sorokban<br/>2026-10-11: rev A-ra LEZARVA (72/72 LCSC; Q6, Q17 nyitott)"]:::gate
  G5["G5 MAIN sematik -> layout -> DRC -> 1:1 print -> rendeles (JLC, modul utoljara kezzel)<br/>csak a rendeles elotti kapu utan: refill + mentes, DRC 0, Gerber check-zones (05 §3.1)<br/>Kilepes: MAIN megrendelve"]:::gate
  G5B["G5b Bring-up - MAIN onalloan, kamera 50-100 mm FFC-n (05 §15, 0-7a. lepes, nyitott stack, K-7)<br/>+ CSI soak teszt hibaszamlalokkal, min. 1 h<br/>Kilepes: stabil stream, 24 h reset nelkul, 9 V PD + PG helyes, PD hard reset x20"]:::gate
  G6["G6 FRONT (IR, mikrofon; ICR rev B)<br/>a G5b zarasa utan, kamera STEP-pel, IR bench arnyekolo csovel (K-19)<br/>Kilepes: FRONT megrendelve"]:::gate

  G0 -->|"a következő csak az előző zárása után §0.2"| G1
  G1 --> G2
  G2 --> G3
  G3 --> G4
  G4 --> G5
  G5 --> G5B
  G5B --> G6
  G2 -.->|"footprint terbeli CSI sorrend (csak input)"| G3
```

---

## Rajzolás közben talált eltérések (javítva: 2026-10-09, review kör 4)

Jelölés: ✅ javítva · ❌ téves (a fordított ellenőrzés cáfolta) · ⏳ nyitva. A fordított ellenőrzés (R4) az 1–8., 10–17., 19–22. tételt visszaigazolta; a #9 részben, a #23 részben igaz, a #18 téves volt. A javítások a 05 v0.5 / 06 v0.3 / 07 v0.2 dokumentumokban vannak; a diagramok ezt mutatják. Súly: **H** = tervezési döntést érint, **M** = dokumentum-hiba, **L** = kozmetikai.

| # | Súly | Eltérés (v0.1) | Javítás (hol) | St. |
|---|---|---|---|---|
| 1 | H | TP8 FIT vs DNP (05 §0.1 "TP1–TP17 FIT" vs "TP8 DNP"; 07 #33 vs #20) | 05 §0.1: "TP1–TP7, TP9–TP17" FIT, TP8 külön DNP; 07 #33 | ✅ |
| 2 | M | TP4 / TP5 / TP6 oldala (05 §12 hátoldali csoport vs 06 §4.2 front) | döntés: a TP pad-ok a hátoldali pogo csoportban, a 0 Ω jumperek elöl, via-val kivezetve (05 §12; 06 §2.1/§2.2/§4.2) | ✅ |
| 3 | M | TP9 és TP16 két jelet hordoz → pad-szám | TP9a/b (D+/D−), TP16a/b (ESP_EN/GPIO 35); 18 pad (17 jel + TP3 GND) + 2 GND pad = 20 (05 §12; 06 §2.1: 95 mm²) | ✅ |
| 4 | H | a C6_EN nem külön pad (E20: P82 = GPIO 54) | felirat mindenhol "GPIO 54 / C6_EN (P82)" + Q2 (05 §5, §6, §10, §12; 08); Q2 maga továbbra is nyitott | ✅ felirat ⏳ Q2 (G2) |
| 5 | M | CH224A tápláló lába nincs a fában | 05 §4.1: nyers VBUS (TVS után, eFuse előtt) → CH224A VDD; diagramokon él | ✅ |
| 6 | M | NTC osztó és VEML7700 tápja nincs a fában | 05 §4.1 3V3 lista: NTC osztó (MAIN), VEML7700 (FRONT, J5 3V3, DNP) | ✅ |
| 7 | M | Státusz LED hozzárendelés kikövetkeztetett; "LED-ek" a 3V3 listán | LED a MAIN hátoldalon, GPIO 6 → soros R → LED; J5.17 tartalék (NC); a lista pontosítva (05 §4.1, §5, §6) | ✅ |
| 8 | H | 100k lehúzások helye ellentmondó | minden 100k lehúzás a MAIN hátoldalon, a modul közelében (05 §4.2, §5; 06 §2.1; 06 §2.4 sor törölve) | ✅ |
| 9 | M | J2 vezérlő-jel ESD hiányzik a rev A tervből és a költségvetésből | a **07 #38 már FIT volt** (az állítás ott téves); javítva: 05 §0.1 sor, 06 §2.2 sor (8 mm²) | ✅ (részben téves volt) |
| 10 | M | 05 §0.1 nem fedi le a 07 FIT/DNP sorait | 05 §0.1: VO4 + TP7, strap, 100k lehúzás, UART0 R + GPIO 5, I2C (DNP), J2 ESD, J1 shield RC, Rd (DNP) sorok | ✅ |
| 11 | M | IR ág "rev A" állapota: D9/fa vs §0.1 | rev A: az egész IR ág DNP, footprint marad (05 D9, §4.1, §4.2, §0.1) | ✅ |
| 12 | M | CC ADC rev A-ban DNP, mégis a boot-sorrendben | 05 §4.3 4. szabály, §15 6. lépés: "rev B / ha CC-tap beültetve" | ✅ |
| 13 | M | J7 header pinszám (7 jel vs 07 "1×9") | J7 = 1×9 (+ C6_IO8, 3V3-ref); pin-tábla 05 §6; 07 #32 | ✅ |
| 14 | M | 07 BOM-ból hiányzó passzív-csoportok | 07 #53–#60 (shield RC, 100k lehúzások nets, UART0 R, GPIO 5 100 nF, CH224A tápkondik, CAM_3V3 0 Ω, buck FB, eFuse OVP/UVLO/ILIM) | ✅ |
| 15 | H | CSI keresztezés vs "max 1 rétegváltás" | 05 §13: kivétel-javaslat (J2 padoknál +1 via-pár, G3 dönt, [NEM ELLENŐRZÖTT]) | ✅ szabály ⏳ Q24 (G3) |
| 16 | H | G2 és G3 körkörös | a CSI/J2 döntés a G3-ba került; a G2 csak footprintet / sematikát szállít (05 §0.2, §6, §14, Q24; 06 K12/K14) | ✅ |
| 17 | H | Nincs kapu a bring-up és a G6 között | új G5b kapu (05 §0.2); a G6 a G5b zárása után | ✅ |
| 18 | L | J5 szomszédság vs EMC-szabály | **téves**: az IR_PWM (J5.5) mellett GND áll (sor-pár J5.6, oszlop-szomszéd J5.3), a PDM_CLK (J5.13) mellett is (sor-pár J5.14, oszlop-szomszéd J5.15) → a "GND-vel elválasztva" szabály teljesül | ❌ téves |
| 19 | M | Pinmap hiányzik több csatlakozóhoz | 05 §6: J3 (microSD), J4 (u.FL), J6 (ICR), J7 pin-táblák | ✅ |
| 20 | L | Nem hivatkozott modul padok | 05 §5: P6–P8 NC, P11–P14 NC, P34–P39 NC, GND padok P1/P3/P15/P33/P40/P47/P52/P83 → GND | ✅ |
| 21 | M | TVS / USB ESD oldala nincs a 05-ben | 05 §3, §4.1: a MAIN hátoldalon a J1 mellett; VBUS ≥2 via-n a front eFuse-hoz | ✅ |
| 22 | L | 06-K5 számtani | 06 K5: nettó 242 mm² (PD 80 + eFuse 76 + buck 86); IR ággal (52) ≈ 294 ≈ 295 | ✅ |
| 23 | L | Dokumentum-hivatkozás (Q26 / Q15 a §0.4-ben) | csak a **Q26** hiányzott a 05 §0.4-ből; felvéve, a Q15 👤 jelölés pótolva | ✅ (részben téves volt) |

### Diagram-javítások (R4)

| Diagram | Javítás |
|---|---|
| 1. blokkdiagram | a TPC6 csomópont szétbontva: C6 pogo pad TP10–TP13 (FIT) és J7 1×9 (DNP, szaggatott él); a CSI él jelöli a Q24 pad-sorrend eltérést; státusz LED a MAIN-en (GPIO 6), a J5-ös él törölve; új csomópontok: J2 ESD, J1 shield RC, 100k lehúzások, Rd footprint (DNP), I2C felhúzás (DNP); TVS/ESD "MAIN rear"; nyers VBUS → CH224A VDD |
| 2. tápfa | az SDB csomópontból kivéve a TP6 (külön FIT pogo pad csomópont); az IR_SW_EN csomópont (ID: IRSWEN) DNP stílusú; a "LED-ek" → státusz LED (GPIO 6 hajtja, MAIN rear); NTC és VEML7700 3V3 él megrajzolva; CH224A VDD él; Rd és I2C felhúzás (DNP) |
| 3. net térkép | státusz LED a MAIN-en; J5.17 tartalék; lehúzások MAIN rear; J2 ESD, I2C felhúzás (DNP), shield RC, TP9a/b, TP16a/b, J7 1×9, nem használt padok (NC / GND); "GPIO 54 / C6_EN (P82)" |
| 4. J5 | J5.17 tartalék (NC), a státusz LED él és csomópont törölve |
| 5. CSI | a szöveg a G3-ba tett döntést és a 05 §13 kivétel-javaslatot tükrözi |
| 6. stack | státusz LED a MAIN hátoldalon; pogo csoport 18 pad + 2 GND; J2 ESD, 0 Ω jumperek a front oldalon; IR ág DNP |
| 7. programozás | "GPIO 54 / C6_EN (P82)" felirat |
| 8. kapuk | G5b hozzáadva; a CSI/J2 döntés G3-ban; a G2→G3 körkörösség és a "HIÁNYZIK" élek megszűntek |

**Ellenőrizve, eltérés nem volt:** a 05 §5 minden GPIO ↔ pad párja egyezik az E20-szal (GPIO 2–13 → P17–P28; GPIO 20–23 → P29–P32; GPIO 24/25 → P50/P51; GPIO 26–38 → P53–P65; GPIO 39–54 → P67–P82; GPIO 0 → P88, GPIO 1 → P16); a 06 §1 pad-oldal hozzárendelése (22 pad/oldal) konzisztens az E20-szal és a 05 §14-gyel; a J5 mind a 20 pinje kiosztott (a 17-es tartalék); az 05 §4.3 táblázat számai újraszámolva egyeznek; a 06 §2.1–§2.4 területösszegek (v0.3: 429,2 / 819 / 95,7 / 315 mm²) és a §3.1 vastagság-összegek helyesek; 07 S11 (9,45 V × 54/254 = 2,01 V) és S6 (47 µF × 30 mV/µs = 1,41 A) helyes.

### Diagram-javítások (v0.3, 2026-10-10 – GPIO v0.6 + as-built)

Forrás: a MAIN v0.6 NYÁK (U1 pad ↔ háló, a séma-szimbólum lábneveivel összevetve) és a `05` v0.6 as-built; a 7. kör review döntései (`05` §0.1).

| Diagram | Javítás |
|---|---|
| 1. blokkdiagram | CAM_3V3_EN GPIO 33 → **4 (P19)**; SD_EN GPIO 29 → **53 (P81)**; PDM DATA GPIO 13 → **30**; USER gomb GPIO 5 → **33**; új élek: EFUSE_FLT → GPIO 29 (P56), SD_CD → GPIO 52 (P80), CH224A I2C (GPIO 7/8, csak olvasás); a TP10–TP13 / TP14–TP15 csomópont törölve → J7 padsor (DNP header) + R40/R41; J2 vezérlő-ESD → rev B (szaggatott); supervisor rev B; új ESP_EN RC csomópont (R23/C25 FIT); lehúzások: 100k GPIO 26–28, 53 + 10k GPIO 4, MAIN front; MAIN 45×45, 4 réteg |
| 2. tápfa | CAMSW EN GPIO 4 (10k R28), SDSW EN GPIO 53 (100k R27); VBUS monitor: Zener D2 DNP; IR_SW_EN lehúzás MAIN front; TP6 külön pad; supervisor rev B; ESP_EN RC a felhúzás-csomópontban |
| 3. net térkép | TP9a/b törölve; CAMG: GPIO 4 / P19 → CAM_3V3_EN (10k), J2 ESD rev B; SDG: GPIO 53 / P81 SD_EN, GPIO 52 / P80 SD_CD; B2BG: GPIO 30 / P57 PDM DATA, R70 47R, lehúzások front; MON: GPIO 33 / P60 USER, új GPIO 29 / P56 EFUSE_FLT, ESP_EN RC FIT, CC1_ADC réz nincs; C6G: TP10–TP13 → J7.2–J7.6; STRP: UART0 → R40/R41 → J7.7/J7.8; RF: R34/J4 FIT; szabad padok v0.6 szerint (GPIO 0, 1, 2, 3, 5, 9–11, 13, 50, 51) |
| 4. J5 | PDM DATA GPIO 13 → 30 (P57); PDM CLK R70 47R → PDM_CLK_J5; az I2C közös busz (kamera + CH224A); J5 as-built pozíció |
| 6. stack | MAIN 45×45, 4 réteg, 0,97 mm (3313A); M2 raszter középpontja (22,5; 25,0); TP-k 12 pad; lehúzások a MAIN front oldalon; J2 ESD és supervisor rev B |
| 7. programozás | UART0 és C6 UART / IO9 / EN: J7 padok (TP10–TP15 törölve) |
| 8. kapuk | G4: 2026-10-10-én nyitott (0 MPN, helyőrző lábképek) |

**Nem változott (ellenőrizve):** 5. CSI diagram (a pad- és J2-lábkiosztás egyezik a NYÁK-kal); a J5 mind a 20 pinje a NYÁK-on is a §6 tábla szerint (J5.13 = PDM_CLK_J5, J5.17 NC). ~~**Tudatosan nem frissítve:** a TVS / USB ESD / shield RC oldal-feliratai (1., 2., 6. diagram „MAIN rear, J1 mellett”) … a layout-javító kör után igazítandó.~~ → a v0.4-ben javítva (lent).

### Diagram-javítások (v0.4, 2026-10-11 – végső rev A as-built, 9. kör)

Forrás: a `05` végső as-built (§0.1, §4.1, §15) és a `90-review-log.md` 9. kör. Csak a végső állapottal ellentmondó feliratok változtak.

| Diagram | Javítás |
|---|---|
| 1. blokkdiagram | TVS: „J1 mellett” → **D1, MAIN rear, az eFuse (U3) alatt**; USB ESD: „MAIN rear” → **U5, MAIN front, a J1 mellett**; a megjegyzés as-built-re javítva |
| 2. tápfa | TVS-csomópont: D1 (rear, U3 alatt) + U5 (front); **új C14 csomópont** (1 µF / 25 V az U3 OUT-on, FIT); bulk: „35–50 V” → as-built 25 V MLCC |
| 6. stack | MF4: eFuse blokk + C14 + 25 V bulk; **új MF13**: U5 + R1/C1 a front oldalon; MR3: D1 TVS az U3 alatt, 3 VBUS via |
| 8. kapuk | G4: rev A-ra lezárva (72/72 LCSC; Q6, Q17 nyitott); G5: rendelés előtti kapu; G5b: CSI soak teszt hibaszámlálókkal |

A kamera / SD / CC ESD a diagramokon eddig is rev B (szaggatott) – a CC clamp nem szerepel csomópontként, a `05` §0.1 rev B sora rögzíti.
