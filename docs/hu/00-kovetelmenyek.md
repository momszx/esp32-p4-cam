# 00 – Követelmények és döntések

Dátum: 2026-10-09 · Státusz: **tervezés / dokumentáció fázis**

## Cél
Kompakt, WiFi-n streamelő (RTSP/MJPEG, HW H.264) kamera ESP32-P4 alapon.

## Kötelező követelmények
| # | Követelmény | Megjegyzés |
|---|---|---|
| K1 | Fő MCU: ESP32-P4 | Bare chip vs modul: kutatás dönt (`01-esp32-p4.md`) |
| K2 | Vezeték nélküli: ESP32-C6 koprocesszor | P4-ben nincs rádió; esp-hosted (`02-...md`) |
| K3 | Kamera: OV5640 (vagy jobban támogatott alternatíva) | csatlakozó: `03-kamera-ov5640.md` |
| K4 | NYÁK: **MAIN 4 réteg, 45×45 mm** (v0.6, 2026-10-09 tulajdonosi döntés – kompakt kamera; a 2 rétegű 60×50 rev A huzalozása nem zárult: GND-feldarabolódás, telített modul-alatti zóna). FRONT: 2 réteg, ha elég | JLC04101H-3313A, L2 = folytonos GND → szabályos CSI/USB/RF impedancia |
| K5 | Kompakt: több egymásra rakott NYÁK | pin header / board-to-board |
| K6 | Programozható legyen mindkét chip | P4 + C6 flash út |
| K7 | Táp: **USB-C, PD sink (9 V), PC 5 V-on csökkentett mód** | nincs akku; részletek: `05` §4 |
| K8 | **OTA frissítés (P4 + C6)**, USB csak első flash-hez | `05` §9–10 |

## Extra funkciók (felhasználói döntés)
- microSD kártya
- Mikrofon (PDM MEMS)
- IR LED + IR-cut filter (éjjellátó)
- Gomb + státusz LED

> **Rev A:** bizonyító prototípus (MAIN először, kapuk G0–G6, DNP blokkok): `05` §0. A K-azonosítók ebben a fájlban **00-Kn** hivatkozásúak (pl. 00-K8 = OTA).

> **Ház: később.** Most csak a NYÁK-ok tervezése; ház-tételek: `05` §18.

## Felhasználás
WiFi élőkép stream (RTSP / MJPEG). Folyamatos táp → deep sleep nem prioritás, hőkezelés igen.

## Dokumentum térkép
| Fájl | Tartalom |
|---|---|
| `01-esp32-p4.md` | P4 pinout, táp, boot, kamera interfészek |
| `02-esp32-c6-es-programozas.md` | C6 modul, P4↔C6 link, programozás |
| `03-kamera-ov5640.md` | OV5640 interfész, csatlakozó, tápok |
| `04-periferiak.md` | microSD, mikrofon, IR, gomb/LED, USB-C táp |
| `05-architektura.md` | **Rev A terv (§0, kapuk G0–G6)**, NYÁK stack, tápfa, GPIO kiosztás (E20 pad-térkép), csatlakozók |
| `06-floorplan-vazlat.md` | Terület- és magasságköltségvetés (G = 7 mm), ASCII floorplan, konfliktusok (06-Kn) |
| `07-bom-terv.md` | BOM-váz (MPN/LCSC/tok/footprint/rev A fit-DNP), értékszámítási lap, USB-C pin map, CAM_3V3 CT |
| `90-review-log.md` | Review körök eredményei |
