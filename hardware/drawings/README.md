# Documentation drawings

The portfolio uses three drawings with consistent sheet borders, reference designators and restrained colors:

| Sheet | SVG and PNG basename | Content |
| --- | --- | --- |
| SYS-01 | `docs/images/system-architecture` | Software and hardware interfaces |
| EE-01 | `docs/images/buzzer-schematic` | NPN buzzer circuit and polarity |
| EE-02 | `docs/images/arduino-wiring` | Functional connection schedule |

Run from the repository root with Python 3:

```powershell
py -3.12 hardware/drawings/generate.py
```

This standard-library script creates SVG files. Open them in a browser or vector editor. PNG previews can be exported with Inkscape, for example:

```powershell
inkscape docs/images/buzzer-schematic.svg --export-type=png --export-filename=docs/images/buzzer-schematic.png
```

Repeat for the other two basenames. PNG previews can be rendered with Sharp; the current documentation keeps SVG sources. They are not native KiCad exports. Editable KiCad source is kept separately in `hardware/kicad/` and has been parsed by KiCad; the PCB project includes ERC/DRC records.

## Revision B checks (2026-10-30)

All three SVG files were parsed as XML, rendered to PNG and visually inspected for clipping, label overlap and unintended wire crossings. Circuit connections were manually compared with `hardware/kicad/intended-nets.json`: +5V, D8, BASE, SWITCHED RETURN and GND. The current drawing assigns no physical Q1 lead order or breadboard holes. No hardware, application or firmware tests were rerun for this documentation-only revision.

The portfolio organization was informed by [Morgan's Metronome](https://github.com/morganwang7777-ux/Morgan-s-Metronome-v1.0): a concise development story, engineering artifacts and a separate hardware section. No project images or CAD files were copied. The project now includes a routed KiCad PCB design. Its native renders show the design, not a fabricated prototype.
