# Validation record — 2026-10-31

**PCB Design — Working Wired Circuit; PCB Fabrication Not Reported**

Installed KiCad version: **10.0.8**, with standard symbol, footprint and STEP model libraries found under the installation's `share/kicad` directory. The native schematic was parsed and exported by Eeschema CLI; the board was loaded, zone-filled, checked and rendered by KiCad CLI.

| Check | Actual result |
| --- | --- |
| Native schematic ERC | 0 errors, 0 warnings |
| Native PCB DRC | 0 violations |
| Unconnected pads | 0 |
| Schematic/PCB parity | 0 footprint or net mismatches |
| Ground zone | Refilled and saved by KiCad before final DRC and exports |
| Short circuits and clearances | No reported violations under the configured rules |
| Native editor inspection | Board opened successfully in PCB Editor; actual window screenshot saved |
| STEP export | Completed successfully, with board and components |
| Visual inspection | Isometric, top and bottom renders inspected; complete board visible and component models present |

Raw ERC/DRC reports retain KiCad's own timestamps and localized messages. The reports explicitly list checks ignored by KiCad defaults. ERC's ignored checks include footprint-filter matching, SPICE issues, single-use global labels and four-way joins. DRC's ignored checks include missing courtyard, footprint-filter matching, footprint-type/pad compatibility, track endpoints off via centers and tuning profiles. No violation exclusions were added to hide findings. This is not a claim that every optional check is enabled.

The five net memberships must remain:

| Net | Pads |
| --- | --- |
| `/D8` | J1.1, R1.1 |
| `/+5V` | J1.2, BZ1.1, D1.1 |
| `/BASE` | R1.2, R2.1, Q1.1 (B) |
| `/SWITCHED` | BZ1.2, D1.2, Q1.2 (C) |
| `/GND` | J1.3, R2.2, Q1.3 (E) |

These preserve the Phase 6A electrical functions. The PCB uses pad 1=B, 2=C, 3=E. The owner confirmed the PN2222 wiring works; matching that tested arrangement to the selected PCB footprint is a separate assembly check. ERC/DRC cannot establish package identity, actual fit, sound output, saturation, diode behavior under the actual load, or power integrity. No hardware tests were performed by the assistant during that design phase. The owner has since reported successful testing of the transistor buzzer circuit. Existing Java, vision and Arduino functionality was not changed or retested for this documentation/design phase.

## Repeat the native checks

Open PowerShell in this folder:

```powershell
$kicadCli = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
& $kicadCli version
& $kicadCli sch erc .\buzzer-driver.kicad_sch --output .\reports\erc.rpt
& $kicadCli pcb drc .\buzzer-driver.kicad_pcb --refill-zones --save-board --schematic-parity --output .\reports\drc.rpt
& $kicadCli sch export netlist .\buzzer-driver.kicad_sch --output .\reports\netlist.net
```

## Repeat native rendering and STEP export

```powershell
& $kicadCli pcb render .\buzzer-driver.kicad_pcb --output .\images\pcb-isometric.png --width 2400 --height 1800 --quality high --background opaque --rotate '325,0,30' --zoom 0.85 --floor
& $kicadCli pcb render .\buzzer-driver.kicad_pcb --output .\images\pcb-top.png --width 2400 --height 1800 --quality high --background opaque --side top --zoom 0.85
& $kicadCli pcb render .\buzzer-driver.kicad_pcb --output .\images\pcb-bottom.png --width 2400 --height 1800 --quality high --background opaque --side bottom --zoom 0.85
& $kicadCli pcb export svg .\buzzer-driver.kicad_pcb --output .\images\pcb-layout.svg --layers F.Cu,F.Silkscreen,Edge.Cuts --mode-single --fit-page-to-board --exclude-drawing-sheet
& $kicadCli pcb export svg .\buzzer-driver.kicad_pcb --output .\images\pcb-bottom-copper.svg --layers B.Cu,B.Silkscreen,Edge.Cuts --mode-single --fit-page-to-board --exclude-drawing-sheet
& $kicadCli sch export svg .\buzzer-driver.kicad_sch --output .\images\
& $kicadCli pcb export step .\buzzer-driver.kicad_pcb --output .\buzzer-driver.step --include-pads --include-tracks --force
```

KiCad's renderer was requested at 2400 × 1800; this installed Windows build produced 2384 × 1768 PNG files. No synthetic component images were substituted. STEP is an optional visualization exchange file, not a fabrication deliverable. No Gerbers were created.

The exported netlist retains its native connectivity; its source filename was normalized to a relative name to omit the local account path. The raw ERC/DRC reports were not edited.

## Status and label update — 2026-11-05

The owner confirmed the PN2222 wiring pattern and working buzzer circuit. Updated schematic notes, Q1 value and PCB silkscreen remove obsolete concept/pinout warnings. Connectivity and routing are unchanged. KiCad 10.0.8 recheck: ERC 0 violations; DRC 0 violations, 0 unconnected items and 0 schematic parity issues. Native schematic/layout exports, three PCB renders and STEP were regenerated. New renders requested 1600 × 1200; actual image dimensions are 1568 × 1176. Exported diagrams and all three renders were visually inspected; labels and geometry render correctly. The obsolete editor screenshot was removed during final cleanup; current native renders are retained. Fabrication, footprint fit and assembled-PCB tests have not been reported.
