# 08 – Diagrams (Mermaid, v0.4)

Date: 2026-10-09 · **v0.4 (2026-10-11): final rev A as-built – D1 TVS under U3, U5 / R1 / C1 on the front side, new C14, G4 closed, G5 pre-order gate, G5b CSI soak** – see "Diagram corrections (v0.4)" at the end · **v0.3 (2026-10-10): GPIO assignment v0.6 (SD_EN 53, SD_CD 52, CAM_3V3_EN 4, USER 33, EFUSE_FLT 29, PDM_DATA 30), MAIN 45×45 / 4 layers, as-built TPs (TP9–TP15 deleted, C6/UART0 on the J7 pad row), 2026-10-10 decisions (R23/C25 FIT, D2 DNP, R28 10k, camera control-signal ESD → rev B)** – see "Diagram corrections (v0.3)" at the end · Source: `05-architecture.md` v0.5 (authoritative), `06-floorplan.md` v0.3, `07-bom-plan.md` v0.2 · **v0.2 (R4): the issue list has been fixed, the diagrams show the corrected state of 05/06/07** (see "Diagram corrections" at the end) · The diagrams are built **exclusively** from the tables / text of 05; 06 and 07 serve only to supplement the board side (front / rear) and the pin map where 05 is silent (this is indicated by the edge label).

## Legend (for all diagrams)

| Notation | Meaning |
|---|---|
| Solid arrow, `§n` on the edge label | the connection appears in the given section of 05 (`E20` = 05 §1 pad map, `07 §3` = USB-C pin map) |
| Dashed arrow | DNP branch or optional connection (the v0.1 "MISSING FROM 05" edges have all been recorded after the fixes, see the issue list) |
| Node with a dashed **red** border | rev A **DNP** (05 §0.1; footprint present, not fitted) |
| Node with a dashed **blue** border | **later (G6)**, on the FRONT board (05 §0.1, §0.2) |
| Plain border | rev A **FIT** |

Module pad = `P` number, processor pin = `GPIO n` (05 notation rule). The spatial arrangement of the pin numbering is **[F]** (assumption) until the footprint import (05 §14, 06 §1) – **v0.3: the footprint has been imported and matches the DXF; the GPIO ↔ pad ↔ net assignment has been checked against the U1 pads of the PCB (05 §5).**

---

## 1. System block diagram

```mermaid
flowchart LR
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  subgraph MAINL["MAIN board 45x45, 4 layers (05 §3, §3.1a)"]
    J1["J1 USB-C 16 pin<br/>USB 2.0 (§6)"]
    TVS["TVS SMAJ10A (D1)<br/>MAIN rear, as-built: under eFuse U3 (§0.1, §4.1)"]
    ESD["USB ESD 3.3 V array (U5)<br/>MAIN front, next to J1 (§0.1, §5)"]
    PD["CH224A PD sink<br/>internal Rd, PG, strap (§4.1)"]
    EF["eFuse: OVP / UVLO / ILIM<br/>reverse-blocking, MAIN front (§4.1)"]
    BUCK["Buck 3V3<br/>forced-PWM, 2 A+ (§4.1)"]
    VDIV["VBUS_SW ADC divider<br/>(§4.1)"]
    CAMSW["CAM_3V3 load switch<br/>(§4.1)"]
    SDSW["SD_3V3 load switch<br/>(§4.1)"]:::dnp
    IREF["IR branch (rev A: DNP): 2nd eFuse + high-side<br/>+ shunt TP8 + IR_SW_EN pull-down (§4.2)"]:::dnp
    J2["J2 FPC 15 pin 1.0 mm<br/>(§6)"]
    J3["J3 microSD<br/>(§6)"]:::dnp
    J5["J5 B2B 2x10 1.27 mm<br/>7 mm (§6)"]
    BTN["BOOT / RESET / USER<br/>SW1-SW3 (§6)"]
    NTC["NTC divider<br/>(§11)"]
    J7["J7 SMD pad row 1x9, 1.27 mm (DNP header)<br/>GND, TXD, RXD, IO9, IO8, GPIO 54 / C6_EN, UART0 TX/RX, 3V3-ref (§6)<br/>TP10-TP15 deleted"]:::dnp
    TPU0["UART0 series R40/R41 1k<br/>-> J7.7 / J7.8 (§5.1)"]
    J4["J4 u.FL + pi-network + CPWG<br/>(§6, §13)"]
    SUP["Supervisor + 0R -> ESP_EN<br/>rev B, not drawn (§5)"]:::dnp
    ENRC["ESP_EN RC: R23 10k + C25 1 uF<br/>FIT 2026-10-10 (§0.1, §5)"]
    SLED["Status LED 0603 + series R<br/>MAIN rear, GPIO 6 (§5)"]
    ESDC["J2 control-signal ESD<br/>CAM_IO0, SCL, SDA - rev B (07 #38)"]:::dnp
    SHRC["J1 shield: 1 MOhm || 4.7 nF<br/>(§5, 07 #53)"]
    PDN["Pull-downs: 100k GPIO 26-28, 53; 10k GPIO 4 (FIT)<br/>GPIO 32 (DNP), MAIN front (§5, K-7)"]
    RDF["2x 5.1k Rd footprint<br/>only without CH224A (K-1)"]:::dnp
    I2CPU["I2C pull-up SDA/SCL (MAIN)<br/>to camera I/O level (§5)"]:::dnp

    subgraph MOD["P4 module: Waveshare ESP32-P4-Module (E1)"]
      P4["ESP32-P4NRW32<br/>32 MB PSRAM + 16 MB flash"]
      C6["ESP32-C6H8 (internal)<br/>WiFi, esp-hosted"]
      P4 ---|"SDIO slot1 internal, GPIO 14-19 (E5, E18)"| C6
    end
  end

  CAM["Camera module OV5640<br/>MIPI 2-lane, onboard osc+LDO (§7)"]

  subgraph FRONTL["FRONT board 45x45 (05 §3)"]
    IRD["IR CC driver x2 + AO3400 x2<br/>(§4.2)"]:::g6
    IRL["IR LED 850 nm x4 (3535)<br/>(D9)"]:::g6
    MIC["PDM microphone + LC<br/>(D7, §4.1)"]:::g6
    VEML["VEML7700<br/>(D7)"]:::dnp
    ICR["ICR H-bridge DRV8837 + J6<br/>from 3V3 (§4.2)"]:::dnp
  end

  J1 -->|"VBUS §4.1"| TVS
  TVS -->|"VBUS >=2 vias rear->front §4.1"| EF
  TVS -->|"raw VBUS -> CH224A VDD §4.1"| PD
  J1 -->|"shield §5"| SHRC
  ESDC -.->|"CAM_IO0, SCL, SDA §6 (rev B)"| J2
  PDN ---|"pull-down §5"| P4
  ENRC ---|"ESP_EN P87 §5"| P4
  RDF -.->|"CC1/CC2, never together with CH224A K-1"| PD
  I2CPU -.->|"SDA/SCL §5"| J2
  J1 <-->|"CC1 / CC2 §4.1"| PD
  PD -->|"PG -> GPIO 31 (P58) §5"| P4
  PD <-->|"I2C 0x22/0x23 CFG2/CFG3 = GPIO 8/7, FW: read only §5"| P4
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
  P4 ==>|"MIPI-CSI 2-lane P41-P46 E20 -> J2 §6 - pad order differs (Q24, G3)"| J2
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
  P4 -->|"GPIO 6 (P21) -> series R -> LED §5"| SLED
  J5 -->|"IR_VIN, IR_PWM §4.2"| IRD
  IRD -->|"per-branch CC §4.2"| IRL
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

Notes: the status LED is on the back side of MAIN (driven by GPIO 6), J5.17 is spare (NC). ~~The TVS + USB ESD sit on the MAIN back side~~ → **as-built (2026-10-11): the D1 TVS is on the back side, under the eFuse (U3) (6.8 mm from J1, accepted deviation); the U5 USB ESD and the R1/C1 shield RC are on the front side, next to J1**; VBUS reaches the front-side eFuse IN through 3 vias. The "SDIO internal" link is inside the module (E5: GPIO 14–19 are not brought out, **inference**); there is no MAIN routing between P4 and C6 (D2). The camera 3V3 is supplied by the CAM_3V3 load switch (not directly by the main 3V3 rail, §7).

---

## 2. Power tree

```mermaid
flowchart LR
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  subgraph LEG["Legend"]
    L1["FIT rev A"]
    L2["DNP rev A"]:::dnp
    L3["FRONT, G6"]:::g6
  end

  VBUS["VBUS max 9 V<br/>J1 A4,B9,B4,A9 (07 §3)"]
  TVS["TVS SMAJ10A (D1, rear, under U3)<br/>+ USB ESD (U5, front) - BEFORE the eFuse (§0.1, §4.1)"]
  CEFF["pre-eFuse C max 10 uF eff<br/>CH224 caps + TVS Cj (§4.1)"]
  EF["eFuse: OVP 10.5-11 V, UVLO 4.4/3.9 V<br/>ILIM ~2 A, auto-retry (§4.1)"]
  BYP["VBUS -> VBUS_SW 0R / solder bridge<br/>bypass (K-1)"]:::dnp
  VSW["VBUS_SW"]
  BULK["bulk max 47 uF eff<br/>as-built 25 V MLCC: C5/C6 22 uF, C8 10 uF (§4.1)"]
  C14N["C14 1 uF 25 V X7R on U3 OUT<br/>FIT, new 2026-10-11 (§0.1, §4.1)"]
  BUCK["Buck 3V3 forced-PWM 2 A+<br/>2.2 uH Isat 3.5 A+ (§4.1)"]
  R0["0R at the buck output<br/>(§4.1, §12 TP4)"]
  TP4["TP4 pad (rear pogo): bench power feed<br/>if the 0R is open (K-1)"]
  V3["3V3 rail"]
  VDIV["VBUS monitor divider 200k/54.9k + 100 nF<br/>3.6 V Zener D2: DNP 2026-10-10 (§4.1)"]
  ADC20["GPIO 20 (P29) ADC1"]

  IRSW["IR branch (rev A: DNP, footprint stays):<br/>2nd eFuse 18 V+, ILIM 0.5-0.7 A (rev B alt.: fused 0R) (§4.2, D9)"]:::dnp
  SHUNT["shunt + TP8<br/>MAIN front side (§4.2, §12)"]:::dnp
  IRVIN["IR_VIN -> J5 pin 1-2 (§6)"]:::dnp
  FIR["FRONT: IR CC driver x2 -> AO3400 x2 -> IR LED x4 (§4.2)"]:::g6
  IRSWEN["IR_SW_EN GPIO 32 (P59)<br/>100k pull-down MAIN front, DNP with the IR branch (§5)"]:::dnp

  J1CC["J1 CC1 A5 / CC2 B5 (07 §3)"]
  PDI["CH224A<br/>internal Rd, DP/DM NC (§4.1)"]
  STRAP["voltage strap fixed R<br/>never floating (§4.1)"]
  PGN["PG -> GPIO 31 (P58)<br/>pull-up 3V3 + TP17 (§5, §12)"]
  CCTAP["CC tap 100k+ series, 10 nF, 3.6 V Zener x2<br/>-> GPIO 21/22 (§4.1, §5)"]:::dnp

  MODP["P4 module: P84 VBAT, P85/P86 ESP_3V3<br/>47 uF + 10 uF + 100 nF (E3, §4.1)"]
  CAMSW["CAM_3V3 load switch TPS22917 (TPS22918 class)<br/>EN GPIO 4 (P19), 10k pull-down R28 (§4.1, §5)"]
  TP5["0R measurement jumper + TP5 (§4.1, §12)"]
  J2P["J2 pin 15 CAM_3V3 (§6)"]
  CAMM["Camera module (§7)"]
  SDSW["SD_3V3 load switch with discharge<br/>EN GPIO 53 (P81), 100k pull-down R27 (§4.1, §5)"]:::dnp
  SDB["J3 microSD + pull-ups + ESD (§5)"]:::dnp
  TP6["TP6 SD_3V3 pad (FIT, rear, separate)<br/>(§12)"]
  MICLC["FRONT: microphone LC (J5 3V3) (§4.1)"]:::g6
  ICRH["ICR H-bridge FRONT, from 3V3 only (§4.1, §4.2)"]:::dnp
  SLED["Status LED 0603 + series R<br/>MAIN rear, driven by GPIO 6 (§4.1, §5)"]
  RDF["2x 5.1k Rd footprint<br/>only without CH224A (K-1)"]:::dnp
  I2CPU["I2C pull-up (MAIN)<br/>to camera I/O level (§5)"]:::dnp
  SUP["Supervisor TPS3840 class<br/>-> 0R -> ESP_EN, rev B (§4.1, §5)"]:::dnp
  PU["10k pull-up: GPIO 36, C6_IO9, C6_IO8 (§5)<br/>+ ESP_EN R23 10k / C25 1 uF FIT (2026-10-10)"]
  PGPU["PG pull-up to 3V3 (§5)"]
  NTCN["NTC divider + 100 nF -> GPIO 49 ADC2 (§5, §11)"]
  VEML["VEML7700 DNP (FRONT, J5 3V3) (D7)"]:::dnp
  VO4["P66 ESP_LDO_VO4: 1 uF + TP7<br/>external source forbidden (§5)"]
  MODI["P4 module internal LDO"]

  VBUS -->|"§4.1"| TVS
  TVS -->|"VBUS >=2 vias rear->front §4.1"| CEFF
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
  IRSWEN -->|"enable §5"| IRSW

  J1CC <-->|"§4.1"| PDI
  STRAP -->|"§4.1"| PDI
  PDI -->|"PG §4.1"| PGN
  J1CC -->|"CC tap §4.1"| CCTAP
  TVS -->|"raw VBUS -> CH224A VDD (after TVS, before eFuse) §4.1"| PDI
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
  V3 -->|"3V3 logic; driven by GPIO 6 §4.1, §5"| SLED
  V3 -.->|"§5"| I2CPU
  V3 -.->|"§4.1 (rev B)"| SUP
  V3 -->|"§5"| PU
  MODI -->|"internal (E9)"| VO4
  V3 -->|"NTC divider supply 3V3 §4.1, 07 S13"| NTCN
  V3 -->|"3V3 via J5 pin 10-11 (FRONT) §4.1, §6"| VEML
```

Note: the supervisor, ICR, VEML7700, NTC and status LED branches come from the list under 3V3 in the 05 §4.1 tree (the "LEDs" row narrowed down to the status LED: MAIN back side, GPIO 6); the FRONT-side loads receive 3V3 through J5 pins 10–11 (§6).

---

## 3. Signal / net map from the P4 module pads

```mermaid
flowchart LR
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  subgraph USB["USB-Serial-JTAG (§5, E10)"]
    A24["GPIO 24 / P50"]
    A25["GPIO 25 / P51"]
    A4849["P48 / P49 USB HS PHY"]
    AJ1["J1 A7+B7 D-<br/>ESD 3.3 V array (07 §3)"]
    AJ2["J1 A6+B6 D+<br/>ESD 3.3 V array (07 §3)"]
    ANC["NC - not used (§5)"]
    A24 -->|"USB_DM"| AJ1
    A25 -->|"USB_DP"| AJ2
    A4849 -->|"NC"| ANC
    ASH["J1 shield 4 THT pins<br/>1 MOhm || 4.7 nF -> GND (07 #53)"]
  end

  subgraph CAMG["Camera J2 (§5, §6)"]
    BCSI["P41-P46 CSI D0N D0P CLKP CLKN D1N D1P"]
    BJ2CSI["J2 pin 2,3,5,6,8,9<br/>(diagram 5)"]
    B7["GPIO 7 / P22"]
    B8["GPIO 8 / P23"]
    B23["GPIO 23 / P32"]
    B4["GPIO 4 / P19"]
    BSDA["J2 pin 14 SDA"]
    BSCL["J2 pin 13 SCL"]
    BIO0["J2 pin 11 CAM_IO0 PWDN/EN<br/>pull = TBD Q5"]
    BSW["CAM_3V3 load switch EN<br/>10k pull-down R28 MAIN front"]
    BESD["J2 control-signal ESD<br/>CAM_IO0, SCL, SDA - rev B (07 #38)"]:::dnp
    BI2CPU["I2C pull-up SDA/SCL (MAIN)<br/>DNP, to camera I/O level (§5)"]:::dnp
    BP15["J2 pin 15 CAM_3V3"]
    BP12["J2 pin 12 CAM_IO1"]
    BNC["NC (§6)"]
    BCSI ==>|"MIPI-CSI 2-lane; pad order differs (Q24, G3; diagram 5)"| BJ2CSI
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
    CJ3["J3 DAT0 DAT1 DAT2 DAT3 CLK CMD<br/>pull-up to SD_3V3, ESD: rev B"]:::dnp
    CSW["SD_3V3 load switch EN<br/>100k pull-down R27 (FIT)"]:::dnp
    CCD["J3 CD pull-up to the main 3V3"]:::dnp
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
    D78["GPIO 7 / P22 and GPIO 8 / P23"]
    DJ5["J5 pin 5 IR_PWM<br/>100k pull-down MAIN front"]
    DJ7["J5 pin 7 ICR_IN1 (ICR DNP)<br/>100k pull-down MAIN front, FIT"]:::dnp
    DJ8["J5 pin 8 ICR_IN2 (ICR DNP)<br/>100k pull-down MAIN front, FIT"]:::dnp
    DJ13["J5 pin 13 PDM_CLK_J5<br/>series R70 47R at the source"]
    DJ16["J5 pin 16 PDM_DAT"]
    DJ17["J5 pin 17 spare (NC)"]
    DJ1920["J5 pin 19 SDA / pin 20 SCL<br/>-> VEML7700 DNP"]
    D26 -->|"IR_PWM LEDC 40 kHz+"| DJ5
    D27 -->|"ICR_IN1"| DJ7
    D28 -->|"ICR_IN2"| DJ8
    D12 -->|"PDM CLK I2S0"| DJ13
    D30 -->|"PDM DATA"| DJ16
      D78 -->|"I2C"| DJ1920
  end

  subgraph MON["Measurement / control (§5)"]
    E20["GPIO 20 / P29"]
    E21["GPIO 21 / P30"]
    E22["GPIO 22 / P31"]
    E31["GPIO 31 / P58"]
    E32["GPIO 32 / P59"]
    E49["GPIO 49 / P77"]
    E33["GPIO 33 / P60"]
    E29["GPIO 29 / P56"]
    EEN["ESP_EN / P87"]
    EVB["VBUS_SW divider 200k/54.9k + 100 nF<br/>Zener D2 DNP"]
    ECC1["CC1 tap 100k+ + 10 nF + Zener<br/>rev A: the CC1_ADC net has no copper"]:::dnp
    ECC2["CC2 tap 100k+ + 10 nF + Zener"]:::dnp
    EPG["CH224A PG, pull-up 3V3, TP17"]
    EIR["IR eFuse2 / switch EN<br/>100k pull-down MAIN front, DNP with the IR branch"]:::dnp
    E6["GPIO 6 / P21"]
    ELED["Status LED 0603 + series R<br/>MAIN rear (FIT)"]
    EPD["Pull-downs: 100k GPIO 26-28, 53; 10k GPIO 4 - FIT;<br/>GPIO 32 DNP; MAIN front (K-7)"]
    ENTC["NTC divider + 100 nF, ADC2"]
    EUSR["USER button SW3 to GND<br/>internal pull-up + C40 100 nF"]
    EFLT["eFuse ~FLT (TPS259470A)<br/>open-drain, 10k pull-up R11"]
    ERST["RESET button SW2 + R23 10k / C25 1 uF FIT<br/>supervisor rev B; TP16A ESP_EN"]
    E20 -->|"ADC1"| EVB
    E21 -->|"ADC1"| ECC1
    E22 -->|"ADC1"| ECC2
    E31 -->|"PD PG"| EPG
    E32 -->|"IR_SW_EN"| EIR
    E49 -->|"NTC ADC2"| ENTC
    E6 -->|"status LED"| ELED
    E33 -->|"User button"| EUSR
    EFLT -->|"EFUSE_FLT"| E29
    EEN -->|"reset"| ERST
  end

  subgraph C6G["C6 programming header / pogo (§10, §12, E6)"]
    F5["P5 C6_U0TXD"]
    F4["P4 C6_U0RXD"]
    F9["P9 C6_IO9"]
    F10["P10 C6_IO8"]
    F82["GPIO 54 / C6_EN (P82) - Q2"]
    FJTAG["P11-P14 C6 JTAG IO7..IO4"]
    FTP10["J7.2 C6_TXD (TP10 deleted)"]
    FTP11["J7.3 C6_RXD (TP11 deleted)"]
    FTP12["J7.4 C6_IO9<br/>10k pull-up R21, jumper to GND (TP12 deleted)"]
    FPU8["10k pull-up R22 to 3V3, mandatory; J7.5"]
    FTP13["J7.6 GPIO 54 / C6_EN (P82; Q2) (TP13 deleted)"]
    FJ7["J7 SMD pad row 1x9, 1.27 mm, DNP header: GND, TXD, RXD, IO9, IO8,<br/>GPIO 54 / C6_EN, UART0 TX/RX, 3V3-ref (§6)"]:::dnp
    FNC["not brought out in v1 (F-25)"]
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
    G34N["NC, no load"]
    G35B["BOOT button SW1 to GND<br/>+ TP16B GPIO 35"]
    G36P["10k pull-up 3V3"]
    G37T["R40 1k -> J7.7 UART0 TX (TP14 deleted)"]
    G38T["R41 1k -> J7.8 UART0 RX (TP15 deleted)"]
    G34 -->|"NC"| G34N
    G35 -->|"BOOT"| G35B
    G36 -->|"BOOT_EN"| G36P
    G37 -->|"UART0 TX"| G37T
    G38 -->|"UART0 RX"| G38T
  end

  subgraph RFP["RF and power pads (E3, E7, E20)"]
    H2["P2 LNA_OUT"]
    H84["P84 VBAT"]
    H85["P85 / P86 ESP_3V3"]
    H66["P66 ESP_LDO_VO4"]
    HRF["pi-network: R34 0R FIT, C27/C28 DNP -> 50 Ohm line -> J4 u.FL (FIT)<br/>or the module's IPEX (G2)"]
    H3V3["3V3 rail<br/>47 uF + 10 uF + 100 nF"]
    HVO["1 uF + TP7, external source forbidden"]
    H2 -->|"RF"| HRF
    H84 -->|"3V3"| H3V3
    H85 -->|"3V3"| H3V3
    H66 -->|"VO4"| HVO
  end

  subgraph FREE["Free / unused (§5)"]
    Z1["GPIO 0 P88, GPIO 1 P16, GPIO 2, 3, 5 P17, P18, P20, GPIO 13 P28<br/>GPIO 9-11 P24-P26, GPIO 50-51 P78-P79<br/>-> free (v0.6)"]
    Z2["GPIO 45-48 P73-P76 -> NC, VO4 domain<br/>(GPIO 45: sdkconfig SD power-reset must be overridden)"]
    Z3["P6-P8 C6_IO15..13 NC; P11-P14 C6 JTAG NC (rev A);<br/>P34-P39 DSI NC (§5)"]
    Z4["GND pads P1, P3, P15, P33, P40, P47, P52, P83 -> GND (§5)"]
  end
```

Note: the pad number in every row follows 05 §5 / E20; I checked the GPIO ↔ pad mapping (no discrepancy, see the end).

---

## 4. B2B J5 2×10 pinout (MAIN → FRONT)

```mermaid
flowchart LR
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  subgraph SRC["MAIN-side source (§5, §4.1, §4.2)"]
    SIR["IR_VIN: IR eFuse2 / fused 0R output<br/>rev A DNP (§4.2)"]:::dnp
    SGND["MAIN GND"]
    S26["GPIO 26 / P53 IR_PWM"]
    S27["GPIO 27 / P54 ICR_IN1"]:::dnp
    S28["GPIO 28 / P55 ICR_IN2"]:::dnp
    S3V3["MAIN 3V3 rail (buck)"]
    S12["GPIO 12 / P27 PDM CLK<br/>R70 47R -> PDM_CLK_J5"]
    S30["GPIO 30 / P57 PDM DATA"]
    S7["GPIO 7 / P22 SDA<br/>shared bus: camera + CH224A"]
    S8["GPIO 8 / P23 SCL<br/>shared bus: camera + CH224A"]
  end

  subgraph PINS["J5 pins (§6 table: row, odd / even)"]
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
    P17["J5.17 spare (NC)"]
    P18["J5.18 GND"]
    P19["J5.19 SDA"]
    P20["J5.20 SCL"]
  end

  subgraph DST["FRONT-side target (§4.2, §6, D7)"]
    TIR["IR CC driver x2 input<br/>+ local 10 uF + 100 nF"]:::g6
    TGND["FRONT GND"]
    TPWM["AO3400 x2 (series NFET dimming)<br/>PWM input"]:::g6
    TIN1["DRV8837 IN1 (J6 ICR)"]:::dnp
    TIN2["DRV8837 IN2 (J6 ICR)"]:::dnp
    T3V3["FRONT 3V3: ICR H-bridge supply, microphone LC"]:::g6
    TCLK["PDM microphone CLK<br/>series 33-100 R"]:::g6
    TDAT["PDM microphone DATA"]:::g6
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

Notes (per 05 §6): **as-built: J5 on the bottom edge of the F side, (22.5; 40.2), pin 1 (16.785; 42.15) – the FRONT mate at the same X/Y (05 §3.1a)**; logic + power only; GND around PDM CLK and IR PWM; ≥2 pins per rail (IR_VIN 2, 3V3 2, GND 8); J5.17 is spare (NC) – the status LED is on the back side of MAIN (GPIO 6); pin 1 / mirroring in the paper test (P-22). The **VEML INT has no J5 pin** (05 §5, GPIO 0 free), so it is not assigned.

---

## 5. Camera J2 15 pin – CSI pad order and the Q24 discrepancy

Red / orange edge = the discrepancy between the pad order and the J2 order (05 E20, §6 "CSI pad order vs J2", Q24, 06-K14). **Red**: the P/N order of the CLK pair is reversed (P,N on the module; N,P on J2) **and** the position of the pair is also swapped; **orange**: the position of the D1 pair is swapped with the CLK pair (D0–CLK–D1 vs D0–D1–CLK).

```mermaid
flowchart LR
  subgraph MODPADS["P4 module CSI pads - E20 order"]
    M41["P41 CSI_D0N"]
    M42["P42 CSI_D0P"]
    M43["P43 CSI_CLKP"]
    M44["P44 CSI_CLKN"]
    M45["P45 CSI_D1N"]
    M46["P46 CSI_D1P"]
  end

  subgraph J2PINS["J2 FPC 15 pin - RPi order (§6)"]
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
  M43 ==>|"CLK_P -> J2.9: position + P/N swap (Q24)"| J9
  M44 ==>|"CLK_N -> J2.8: position + P/N swap (Q24)"| J8
  M45 ==>|"D1_N -> J2.5: pair crossover (Q24)"| J5
  M46 ==>|"D1_P -> J2.6: pair crossover (Q24)"| J6

  GNDN["GND (P40, P47 pads E20; GND plane)"]
  GNDN --> J1
  GNDN --> J4
  GNDN --> J7
  GNDN --> J10

  G8["GPIO 8 / P23 I2C SCL"] --> J13
  G7["GPIO 7 / P22 I2C SDA"] --> J14
  G23["GPIO 23 / P32 CAM_IO0"] --> J11
  NC12["NC (§6)"] --> J12
  CAMSW["CAM_3V3 load switch output + TP5"] --> J15

  linkStyle 2,3 stroke:#d00000,stroke-width:4px
  linkStyle 4,5 stroke:#e67e00,stroke-width:4px
```

Options for the crossover (05 §6): (a) a camera / FFC adapter matching the module order; (b) CSI lane / polarity swap inside the P4 (TRM, **[UNVERIFIED]**, we do not rely on it); (c) symmetric via crossover at the J2 pads (rev A measurement). The 05 §13 rule ("max 1 layer change per signal") and the crossover would conflict: 05 §13 records an exception proposal (+1 symmetric via pair at the J2 pads; issue list item 15 ✅). The final decision is made in **G3** (camera selected); G2 only provides the spatial order of the footprint (issue list item 16 ✅).

---

## 6. PCB stack side view (front to back)

```mermaid
flowchart TB
  classDef dnp fill:#fdecea,stroke:#c0392b,stroke-width:2px,stroke-dasharray:5 5,color:#000
  classDef g6 fill:#eaf2ff,stroke:#1f6feb,stroke-width:2px,stroke-dasharray:2 3,color:#000

  FWD(["FORWARD: lens direction"])

  subgraph FE["FRONT front face (05 §3, 06 §2.3)"]
    FE0["Lens cutout 16x16 mm, R1 corner<br/>holder 14x14 + barrel passes through (variant A)"]
    FE1["IR LED x4 3535 (2.0 mm)"]:::g6
    FE3["PDM microphone, right strip + acoustic port"]:::g6
    FE4["VEML7700 DNP + IR-shielding Cu ring"]:::dnp
  end

  FPCB["FRONT PCB 1.0 mm, 2 layers (if sufficient)"]

  subgraph FB["FRONT back face (05 §3, 06 §2.4)"]
    FB1["B2B 2x10 header + 10 uF + 100 nF"]:::g6
    FB2["IR CC driver x2 + AO3400 x2 (2.1 mm)"]:::g6
    FB3["DRV8837 + J6 ICR"]:::dnp
    FB4["Microphone LC + CLK series R"]:::g6
  end

  subgraph GAP["Gap G = 7.0 mm (05 §3)"]
    CAM["Camera module PCB 1.2 + back-side components 2.0 = 3.2 mm<br/>lies against the rear plane of FRONT"]
    SP["M2 standoff x4, 33.5 mm grid (structural element)<br/>centre (22.5; 25.0) - 2.5 mm below the board centre (05 §3.1a)"]
    B2B["J5 B2B mated height 7 mm"]
    FFC["Camera FPC: closed stack 25-30 mm<br/>bring-up 50-100 mm FFC, open stack"]
    LIM["MAIN component under the camera max 3.3 mm = G - 3.2 - 0.5"]
  end

  subgraph MF["MAIN front side (05 §3, 06 §2.2)"]
    MF1["J2 FPC 15 pin"]
    MF2["J5 B2B socket (3.5 mm)"]
    MF3["CH224A PD block"]
    MF4["eFuse block + C14 + bulk (as-built 25 V)"]
    MF13["USB ESD U5 + shield RC R1/C1 (near J1)"]
    MF5["Buck + inductor 2.8 mm"]
    MF6["VBUS_SW divider, NTC"]
    MF7["CAM_3V3 load switch"]
    MF8["IR branch: 2nd eFuse + shunt + TP8 (rev A DNP; TP8 front)"]:::dnp
    MF9["microSD J3 + SD_3V3 block"]:::dnp
    MF10["J2 control-signal ESD - rev B"]:::dnp
    MF11["0 Ohm measurement jumpers (R16 3V3, R50 CAM_3V3; the TP pad on the back)"]
    MF12["GPIO pull-downs: 100k GPIO 26-28, 53; 10k GPIO 4<br/>(GPIO 32 DNP)"]
  end

  MPCB["MAIN PCB 45x45, 4 layers, 0.97 mm<br/>JLC04101H-3313A"]

  subgraph MR["MAIN back side REAR (05 §3, 06 §2.1)"]
    MR1["P4 module 3.3 mm + 3V3 bulk 47+10 uF + 100 nF"]
    MR2["USB-C J1 3.2 mm"]
    MR3["D1 TVS under the U3 eFuse, 6.8 mm from J1 (as-built, 05 §0.1, §4.1); VBUS 3 vias to U3 IN"]
    MR4["u.FL J4 + pi-network"]
    MR5["BOOT / RESET / USER 2.0 mm"]
    MR6["TPs: TP1-TP7, TP16A/B, TP17-TP19 = 12 pads, 3 GND (TP8 front, DNP)"]
    MR9["Status LED 0603 + R (GPIO 6)"]
    MR7["C6 / UART0 pad row J7 (DNP header)"]:::dnp
    MR8["Supervisor + 0R (rev B)"]:::dnp
  end

  BACK(["BACKWARD"])

  FWD --> FE
  FE -->|"+ 1.0 mm"| FPCB
  FPCB -->|"rear plane"| FB
  FB -->|"7.0 mm"| GAP
  GAP -->|"under the camera max 3.3 mm"| MF
  MF -->|"+ 1.0 mm"| MPCB
  MPCB --> MR
  MR --> BACK
```

Total thickness (06 §3.1): without lens 2.0 + 1.0 + 7.0 + 1.0 + 3.3 = **14.3 mm**; with M12 lens **29.3 mm**; with Ø8 AF barrel **17.8 mm**.

---

## 7. Programming and recovery

```mermaid
flowchart TD
  S0(["Start: new MAIN, P4 module soldered in"])

  subgraph P4F["P4 first flash (05 §10, E10)"]
    A1["USB-C J1 -> USB-Serial-JTAG GPIO 24/25 (P50/P51)<br/>esptool flash, console, JTAG - no USB-UART chip"]
    A2{"USB enumerates and the eFuse allows it?"}
    A3["BOOT button: GPIO 35 low, GPIO 36 10k pulled up<br/>+ RESET (ESP_EN P87) -> download mode (E8)"]
    A4{"successful?"}
    A5["UART0: GPIO 37 TX / GPIO 38 RX<br/>J7.7 / J7.8 pads, series R40/R41 1k (E-25; TP14/TP15 deleted)"]
    A6(["P4 flash done"])
  end

  subgraph C6F["C6 first flash (05 §10, F-21 / F-22)"]
    C1["1. Hold the P4 in reset (ESP_EN pulled low)<br/>GPIO 54 / C6_EN (P82) does not drive C6_EN (Q2 open)"]
    C2["2. USB-UART 3.3 V: C6_U0TXD P5 / C6_U0RXD P4 / GND<br/>J7.2 / J7.3 / J7.1 (SMD pad row 1.27 mm; TP10-TP11 deleted)"]
    C3["3. C6_IO9 (P9, J7.4) -> GND jumper/pogo<br/>GPIO 54 / C6_EN (P82, J7.6; Q2) short pull-down -> release: download mode"]
    C4["4. esptool chip-id + flash-id<br/>query / save the factory FW version before flashing"]
    C5["5. write slave FW, remove IO9 jumper, reset"]
    C6OK(["C6 slave FW done"])
  end

  subgraph OTA["Further updates (05 §9, D8)"]
    O1["P4 OTA: HTTPS -> inactive OTA partition (ota_0 / ota_1)<br/>otadata switch is the last step, rollback"]
    O2{"C6 factory FW OTA-capable? (Q16, 00-K8 gate)"}
    O3["C6 OTA esp-hosted slave OTA from the P4<br/>c6fw partition or HTTPS"]
    O4["Not updatable in the field without USB/UART:<br/>C6 FW version pinned, P4 app runs only with a compatible C6"]
    O5["Bring-up step 11: OTA + rollback + PD hard reset during OTA"]
  end

  REC["P4 recovery: BOOT / RESET on the back side reachable even when enclosed<br/>UART0 spare pad (05 §10)"]

  S0 --> A1
  A1 --> A2
  A2 -->|"yes"| A6
  A2 -->|"no"| A3
  A3 --> A4
  A4 -->|"yes"| A6
  A4 -->|"no"| A5
  A5 --> A6
  A6 -->|"C6 still empty or unknown FW"| C1
  C1 --> C2
  C2 --> C3
  C3 --> C4
  C4 --> C5
  C5 --> C6OK
  C6OK --> O1
  O1 --> O2
  O2 -->|"yes"| O3
  O2 -->|"no"| O4
  O3 --> O5
  O4 --> O5
  A6 -.->|"on error"| REC
  REC -.-> A3
```

---

## 8. Bring-up gates G0–G6 (with G5b; 05 §0.2)

```mermaid
flowchart TD
  classDef gate fill:#f6f8fa,stroke:#57606a,stroke-width:2px,color:#000

  G0["G0 Dev-kit stream + current (K-2)<br/>OV5640 MIPI -> ISP -> H.264 -> RTSP over esp-hosted C6 WiFi<br/>24 h soak, current per state, RSSI, freeze sdkconfig + versions<br/>Exit: stable stream 24 h, measured table replaces the 4.3 estimates"]:::gate
  G1["G1 CH224A breakout bench test (K-4)<br/>MacBook, cheap PD charger, USB-A->C cable<br/>Exit: 9 V stable, PG level known, no 20 V, strap table confirmed (Q13)"]:::gate
  G2["G2 Module schematic + footprint + antenna decision<br/>Q1-Q3, Q9-Q11, footprint import (G2 only delivers the module footprint / schematic), antenna (K-6)<br/>Exit: footprint + 1:1 paper test, antenna decision, supervisor fitting decision"]:::gate
  G3["G3 Camera module frozen + CSI / J2 decision (Q24)<br/>NoIR / fixed lens, 15 pin, onboard osc + LDO, CAM_IO0 polarity, I/O level, STEP, FFC lengths<br/>final CSI pad order / J2 pinout (camera + G2 footprint + TRM lane-swap check + via crossover)<br/>Exit: one module selected, GPIO 23 pull (Q5) and the CSI / J2 order decided"]:::gate
  G4["G4 BOM sheet done (07), resistor calculations before the schematic (K-8)<br/>Exit: no TBD in the rev A FIT rows<br/>2026-10-11: CLOSED for rev A (72/72 LCSC; Q6, Q17 open)"]:::gate
  G5["G5 MAIN schematic -> layout -> DRC -> 1:1 print -> order (JLC, module last, by hand)<br/>only after the pre-order gate: refill + save, DRC 0, Gerber check-zones (05 §3.1)<br/>Exit: MAIN ordered"]:::gate
  G5B["G5b Bring-up - MAIN standalone, camera on 50-100 mm FFC (05 §15, steps 0-7a, open stack, K-7)<br/>+ CSI soak test with error counters, min. 1 h<br/>Exit: stable stream, 24 h without reset, 9 V PD + PG correct, PD hard reset x20"]:::gate
  G6["G6 FRONT (IR, microphone; ICR rev B)<br/>after G5b is closed, with camera STEP, IR bench with shielding tube (K-19)<br/>Exit: FRONT ordered"]:::gate

  G0 -->|"the next one only after the previous one is closed §0.2"| G1
  G1 --> G2
  G2 --> G3
  G3 --> G4
  G4 --> G5
  G5 --> G5B
  G5B --> G6
  G2 -.->|"spatial CSI order of the footprint (input only)"| G3
```

---

## Discrepancies found while drawing (fixed: 2026-10-09, review round 4)

Notation: ✅ fixed · ❌ incorrect (refuted by the reverse check) · ⏳ open. The reverse check (R4) confirmed items 1–8, 10–17 and 19–22; #9 was partly true, #23 partly true, #18 was incorrect. The fixes are in the 05 v0.5 / 06 v0.3 / 07 v0.2 documents; the diagrams show this. Severity: **H** = affects a design decision, **M** = document error, **L** = cosmetic.

| # | Sev. | Discrepancy (v0.1) | Fix (where) | St. |
|---|---|---|---|---|
| 1 | H | TP8 FIT vs DNP (05 §0.1 "TP1–TP17 FIT" vs "TP8 DNP"; 07 #33 vs #20) | 05 §0.1: "TP1–TP7, TP9–TP17" FIT, TP8 separately DNP; 07 #33 | ✅ |
| 2 | M | Side of TP4 / TP5 / TP6 (05 §12 back-side group vs 06 §4.2 front) | decision: the TP pads in the back-side pogo group, the 0 Ω jumpers on the front, brought out through vias (05 §12; 06 §2.1/§2.2/§4.2) | ✅ |
| 3 | M | TP9 and TP16 carry two signals → pad count | TP9a/b (D+/D−), TP16a/b (ESP_EN/GPIO 35); 18 pads (17 signals + TP3 GND) + 2 GND pads = 20 (05 §12; 06 §2.1: 95 mm²) | ✅ |
| 4 | H | C6_EN is not a separate pad (E20: P82 = GPIO 54) | label everywhere "GPIO 54 / C6_EN (P82)" + Q2 (05 §5, §6, §10, §12; 08); Q2 itself is still open | ✅ label ⏳ Q2 (G2) |
| 5 | M | The CH224A supply pin is not in the tree | 05 §4.1: raw VBUS (after the TVS, before the eFuse) → CH224A VDD; edge on the diagrams | ✅ |
| 6 | M | NTC divider and VEML7700 supply not in the tree | 05 §4.1 3V3 list: NTC divider (MAIN), VEML7700 (FRONT, J5 3V3, DNP) | ✅ |
| 7 | M | Status LED assignment inferred; "LEDs" on the 3V3 list | LED on the MAIN back side, GPIO 6 → series R → LED; J5.17 spare (NC); the list refined (05 §4.1, §5, §6) | ✅ |
| 8 | H | Location of the 100k pull-downs contradictory | all 100k pull-downs on the MAIN back side, near the module (05 §4.2, §5; 06 §2.1; 06 §2.4 row deleted) | ✅ |
| 9 | M | J2 control-signal ESD missing from the rev A design and the budget | **07 #38 was already FIT** (the claim was incorrect there); fixed: 05 §0.1 row, 06 §2.2 row (8 mm²) | ✅ (was partly incorrect) |
| 10 | M | 05 §0.1 does not cover the 07 FIT/DNP rows | 05 §0.1: VO4 + TP7, strap, 100k pull-down, UART0 R + GPIO 5, I2C (DNP), J2 ESD, J1 shield RC, Rd (DNP) rows | ✅ |
| 11 | M | IR branch "rev A" status: D9/tree vs §0.1 | rev A: the whole IR branch DNP, footprint stays (05 D9, §4.1, §4.2, §0.1) | ✅ |
| 12 | M | CC ADC is DNP in rev A, yet it is in the boot sequence | 05 §4.3 rule 4, §15 step 6: "rev B / if CC tap fitted" | ✅ |
| 13 | M | J7 header pin count (7 signals vs 07 "1×9") | J7 = 1×9 (+ C6_IO8, 3V3-ref); pin table 05 §6; 07 #32 | ✅ |
| 14 | M | Passive groups missing from the 07 BOM | 07 #53–#60 (shield RC, 100k pull-down nets, UART0 R, GPIO 5 100 nF, CH224A supply caps, CAM_3V3 0 Ω, buck FB, eFuse OVP/UVLO/ILIM) | ✅ |
| 15 | H | CSI crossover vs "max 1 layer change" | 05 §13: exception proposal (+1 via pair at the J2 pads, G3 decides, [UNVERIFIED]) | ✅ rule ⏳ Q24 (G3) |
| 16 | H | G2 and G3 circular | the CSI/J2 decision moved to G3; G2 only delivers the footprint / schematic (05 §0.2, §6, §14, Q24; 06 K12/K14) | ✅ |
| 17 | H | No gate between bring-up and G6 | new G5b gate (05 §0.2); G6 after G5b is closed | ✅ |
| 18 | L | J5 adjacency vs EMC rule | **incorrect**: next to IR_PWM (J5.5) there is GND (row pair J5.6, column neighbor J5.3), and next to PDM_CLK (J5.13) as well (row pair J5.14, column neighbor J5.15) → the "separated by GND" rule is satisfied | ❌ incorrect |
| 19 | M | Pin map missing for several connectors | 05 §6: J3 (microSD), J4 (u.FL), J6 (ICR), J7 pin tables | ✅ |
| 20 | L | Unreferenced module pads | 05 §5: P6–P8 NC, P11–P14 NC, P34–P39 NC, GND pads P1/P3/P15/P33/P40/P47/P52/P83 → GND | ✅ |
| 21 | M | TVS / USB ESD side not in 05 | 05 §3, §4.1: on the MAIN back side next to J1; VBUS through ≥2 vias to the front eFuse | ✅ |
| 22 | L | 06-K5 arithmetic | 06 K5: net 242 mm² (PD 80 + eFuse 76 + buck 86); with the IR branch (52) ≈ 294 ≈ 295 | ✅ |
| 23 | L | Document reference (Q26 / Q15 in §0.4) | only **Q26** was missing from 05 §0.4; added, the Q15 👤 marker filled in | ✅ (was partly incorrect) |

### Diagram corrections (R4)

| Diagram | Fix |
|---|---|
| 1. block diagram | the TPC6 node split up: C6 pogo pads TP10–TP13 (FIT) and J7 1×9 (DNP, dashed edge); the CSI edge marks the Q24 pad-order discrepancy; status LED on MAIN (GPIO 6), the J5 edge deleted; new nodes: J2 ESD, J1 shield RC, 100k pull-downs, Rd footprint (DNP), I2C pull-up (DNP); TVS/ESD "MAIN rear"; raw VBUS → CH224A VDD |
| 2. power tree | TP6 taken out of the SDB node (separate FIT pogo pad node); the IR_SW_EN node (ID: IRSWEN) in DNP style; "LEDs" → status LED (driven by GPIO 6, MAIN rear); NTC and VEML7700 3V3 edges drawn; CH224A VDD edge; Rd and I2C pull-up (DNP) |
| 3. net map | status LED on MAIN; J5.17 spare; pull-downs MAIN rear; J2 ESD, I2C pull-up (DNP), shield RC, TP9a/b, TP16a/b, J7 1×9, unused pads (NC / GND); "GPIO 54 / C6_EN (P82)" |
| 4. J5 | J5.17 spare (NC), the status LED edge and node deleted |
| 5. CSI | the text reflects the decision moved to G3 and the 05 §13 exception proposal |
| 6. stack | status LED on the MAIN back side; pogo group 18 pads + 2 GND; J2 ESD, 0 Ω jumpers on the front side; IR branch DNP |
| 7. programming | "GPIO 54 / C6_EN (P82)" label |
| 8. gates | G5b added; the CSI/J2 decision in G3; the G2→G3 circularity and the "MISSING" edges are gone |

**Checked, no discrepancy found:** every GPIO ↔ pad pair of 05 §5 matches E20 (GPIO 2–13 → P17–P28; GPIO 20–23 → P29–P32; GPIO 24/25 → P50/P51; GPIO 26–38 → P53–P65; GPIO 39–54 → P67–P82; GPIO 0 → P88, GPIO 1 → P16); the pad-side assignment of 06 §1 (22 pads/side) is consistent with E20 and 05 §14; all 20 pins of J5 are assigned (pin 17 is spare); the numbers in the 05 §4.3 table match when recalculated; the 06 §2.1–§2.4 area totals (v0.3: 429.2 / 819 / 95.7 / 315 mm²) and the §3.1 thickness totals are correct; 07 S11 (9.45 V × 54/254 = 2.01 V) and S6 (47 µF × 30 mV/µs = 1.41 A) are correct.

### Diagram corrections (v0.3, 2026-10-10 – GPIO v0.6 + as-built)

Source: the MAIN v0.6 PCB (U1 pad ↔ net, compared against the pin names of the schematic symbol) and `05` v0.6 as-built; the review decisions of round 7 (`05` §0.1).

| Diagram | Fix |
|---|---|
| 1. block diagram | CAM_3V3_EN GPIO 33 → **4 (P19)**; SD_EN GPIO 29 → **53 (P81)**; PDM DATA GPIO 13 → **30**; USER button GPIO 5 → **33**; new edges: EFUSE_FLT → GPIO 29 (P56), SD_CD → GPIO 52 (P80), CH224A I2C (GPIO 7/8, read only); the TP10–TP13 / TP14–TP15 node deleted → J7 pad row (DNP header) + R40/R41; J2 control-signal ESD → rev B (dashed); supervisor rev B; new ESP_EN RC node (R23/C25 FIT); pull-downs: 100k GPIO 26–28, 53 + 10k GPIO 4, MAIN front; MAIN 45×45, 4 layers |
| 2. power tree | CAMSW EN GPIO 4 (10k R28), SDSW EN GPIO 53 (100k R27); VBUS monitor: Zener D2 DNP; IR_SW_EN pull-down MAIN front; TP6 separate pad; supervisor rev B; ESP_EN RC in the pull-up node |
| 3. net map | TP9a/b deleted; CAMG: GPIO 4 / P19 → CAM_3V3_EN (10k), J2 ESD rev B; SDG: GPIO 53 / P81 SD_EN, GPIO 52 / P80 SD_CD; B2BG: GPIO 30 / P57 PDM DATA, R70 47R, pull-downs front; MON: GPIO 33 / P60 USER, new GPIO 29 / P56 EFUSE_FLT, ESP_EN RC FIT, no CC1_ADC copper; C6G: TP10–TP13 → J7.2–J7.6; STRP: UART0 → R40/R41 → J7.7/J7.8; RF: R34/J4 FIT; free pads per v0.6 (GPIO 0, 1, 2, 3, 5, 9–11, 13, 50, 51) |
| 4. J5 | PDM DATA GPIO 13 → 30 (P57); PDM CLK R70 47R → PDM_CLK_J5; the I2C shared bus (camera + CH224A); J5 as-built position |
| 6. stack | MAIN 45×45, 4 layers, 0.97 mm (3313A); M2 grid centre (22.5; 25.0); TPs 12 pads; pull-downs on the MAIN front side; J2 ESD and supervisor rev B |
| 7. programming | UART0 and C6 UART / IO9 / EN: J7 pads (TP10–TP15 deleted) |
| 8. gates | G4: open on 2026-10-10 (0 MPN, placeholder footprints) |

**Not changed (checked):** diagram 5 CSI (the pad and J2 pin assignment matches the PCB); all 20 pins of J5 on the PCB also follow the §6 table (J5.13 = PDM_CLK_J5, J5.17 NC). ~~**Deliberately not updated:** the side labels of the TVS / USB ESD / shield RC (diagrams 1, 2, 6 "MAIN rear, next to J1") … to be aligned after the layout fix passes.~~ → fixed in v0.4 (below).

### Diagram corrections (v0.4, 2026-10-11 – final rev A as-built, round 9)

Source: the final as-built of `05` (§0.1, §4.1, §15) and round 9 of `90-review-log.md`. Only the labels contradicting the final state were changed.

| Diagram | Fix |
|---|---|
| 1. block diagram | TVS: "next to J1" → **D1, MAIN rear, under the eFuse (U3)**; USB ESD: "MAIN rear" → **U5, MAIN front, next to J1**; the note corrected to as-built |
| 2. power tree | TVS node: D1 (rear, under U3) + U5 (front); **new C14 node** (1 µF / 25 V on U3 OUT, FIT); bulk: "35–50 V" → as-built 25 V MLCC |
| 6. stack | MF4: eFuse block + C14 + 25 V bulk; **new MF13**: U5 + R1/C1 on the front side; MR3: D1 TVS under U3, 3 VBUS vias |
| 8. gates | G4: closed for rev A (72/72 LCSC; Q6, Q17 open); G5: pre-order gate; G5b: CSI soak test with error counters |

The camera / SD / CC ESD has been rev B (dashed) on the diagrams all along – the CC clamp does not appear as a node; the rev B row of `05` §0.1 records it.
