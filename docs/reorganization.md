# Local cleanup review — Phase 10

Project: **Gesture-Controlled Tabletop Interface**. Proposed repository slug: `gesture-controlled-tabletop-interface`.

Proposed About: A camera-based tabletop interface using Python hand tracking, calibrated gesture input, Java Swing and Arduino feedback, demonstrated with Guess Who.

The [new README](../README.md) includes the supplied “Why I Built This” paragraph verbatim and preserves the original group credit. The owner approved publishing these changes and updating the existing repository on 2026-11-05.

## Folder layout

```text
src/                 Java application and integration
assets/buttons/      All button/control artwork
assets/characters/   Character portraits and variants
assets/interface/    Other interface artwork
assets/audio/        Original music and effects
computer-vision/     Tracking and calibration
arduino/             Firmware and standalone serial tooling
hardware/            Editable KiCad, PCB renders and concept CAD
screenshots/         Actual application captures
photos/              Instructions for future real photographs
tests/               Regression tests
docs/                Current guides
docs/archive/        Historical phase evidence
```

## Removed and consolidated

Only four files were removed: `docs/portfolio-preflight.md` (obsolete preparation checklist, replaced by this review) and the PNG copies of `arduino-wiring`, `buzzer-schematic` and `system-architecture` under `docs/images/`. Their SVG originals remain, with references updated. Local backups are in ignored `tmp/phase10/removed/`.

Historical phase records moved to `docs/archive/`; current guides have descriptive names. All three real screenshots remain available, while only one appears in the main README. Unused original artwork remains preserved. Dependencies, temporary logs and build outputs are ignored rather than published.

## Validation

- Java build passed: serial 20 checks, feedback 19 normal/22 presentation checks, presentation 32 checks, plus mapping/JSON/Swing harnesses. An initial sandbox run was blocked from localhost; the rerun with loopback access passed.
- Asset loading regression passed: 137 PNGs, 4 WAVs and 6,963 screen-icon checks. All 141 original media files are byte-identical after moving. The rendered game screen was also visually inspected.
- Python vision: 73 tests passed. Python-to-Java TCP: 16 tests passed.
- Snapshot comparison found no unexpectedly missing files; Python production, Arduino firmware and native KiCad files are unchanged.
- No physical camera, projector, Arduino or buzzer test was performed for this cleanup.
- The buzzer wiring is now owner-tested; PCB fabrication and assembled-board validation remain separate; see the hardware notes.

Run commands are in [testing](testing.md). Launch from the repository root so filesystem asset paths resolve. KiCad 10.0.8 rechecked the PCB project: ERC 0 violations; DRC 0 violations, 0 unconnected items and 0 schematic parity issues. The earlier system schematic also exported a netlist successfully. Neither design was modified. Documentation relative links were checked (example photo code is intentionally a placeholder). The existing ignore rules exclude environments, build output, secrets, local calibration and temporary files.

## Exact move list

Git recognizes the byte-preserving media moves when staged.

| Previous path | New path |
| --- | --- |
| `100x100Button.png` | `assets/buttons/button-100x100.png` |
| `166x100Button.png` | `assets/buttons/button-166x100.png` |
| `250x100Button.png` | `assets/buttons/button-250x100.png` |
| `300x100Button.png` | `assets/buttons/button-300x100.png` |
| `600x100Button.png` | `assets/buttons/button-600x100.png` |
| `62x100Button.png` | `assets/buttons/button-62x100.png` |
| `83x100Button.png` | `assets/buttons/button-83x100.png` |
| `AA04.png` | `assets/characters/AA04.png` |
| `AA04exclude.png` | `assets/characters/AA04exclude.png` |
| `AA04target.png` | `assets/characters/AA04target.png` |
| `AD01.png` | `assets/characters/AD01.png` |
| `AD01exclude.png` | `assets/characters/AD01exclude.png` |
| `AD01target.png` | `assets/characters/AD01target.png` |
| `AE05.png` | `assets/characters/AE05.png` |
| `AE05exclude.png` | `assets/characters/AE05exclude.png` |
| `AE05target.png` | `assets/characters/AE05target.png` |
| `AIDisguise.png` | `assets/interface/AIDisguise.png` |
| `AIProfile.png` | `assets/interface/AIProfile.png` |
| `AIText.png` | `assets/interface/AIText.png` |
| `AX02.png` | `assets/characters/AX02.png` |
| `AX02exclude.png` | `assets/characters/AX02exclude.png` |
| `AX02target.png` | `assets/characters/AX02target.png` |
| `AY03.png` | `assets/characters/AY03.png` |
| `AY03exclude.png` | `assets/characters/AY03exclude.png` |
| `AY03target.png` | `assets/characters/AY03target.png` |
| `battery.png` | `assets/interface/battery.png` |
| `BD07.png` | `assets/characters/BD07.png` |
| `BD07exclude.png` | `assets/characters/BD07exclude.png` |
| `BD07target.png` | `assets/characters/BD07target.png` |
| `BL09.png` | `assets/characters/BL09.png` |
| `BL09exclude.png` | `assets/characters/BL09exclude.png` |
| `BL09target.png` | `assets/characters/BL09target.png` |
| `BN06.png` | `assets/characters/BN06.png` |
| `BN06exclude.png` | `assets/characters/BN06exclude.png` |
| `BN06target.png` | `assets/characters/BN06target.png` |
| `buttonBase.png` | `assets/buttons/button-base.png` |
| `BY08.png` | `assets/characters/BY08.png` |
| `BY08exclude.png` | `assets/characters/BY08exclude.png` |
| `BY08target.png` | `assets/characters/BY08target.png` |
| `CE12.png` | `assets/characters/CE12.png` |
| `CE12exclude.png` | `assets/characters/CE12exclude.png` |
| `CE12target.png` | `assets/characters/CE12target.png` |
| `CN10.png` | `assets/characters/CN10.png` |
| `CN10exclude.png` | `assets/characters/CN10exclude.png` |
| `CN10target.png` | `assets/characters/CN10target.png` |
| `CS11.png` | `assets/characters/CS11.png` |
| `CS11exclude.png` | `assets/characters/CS11exclude.png` |
| `CS11target.png` | `assets/characters/CS11target.png` |
| `DD14.png` | `assets/characters/DD14.png` |
| `DD14exclude.png` | `assets/characters/DD14exclude.png` |
| `DD14target.png` | `assets/characters/DD14target.png` |
| `DL13.png` | `assets/characters/DL13.png` |
| `DL13exclude.png` | `assets/characters/DL13exclude.png` |
| `DL13target.png` | `assets/characters/DL13target.png` |
| `EA15.png` | `assets/characters/EA15.png` |
| `EA15exclude.png` | `assets/characters/EA15exclude.png` |
| `EA15target.png` | `assets/characters/EA15target.png` |
| `EC16.png` | `assets/characters/EC16.png` |
| `EC16exclude.png` | `assets/characters/EC16exclude.png` |
| `EC16target.png` | `assets/characters/EC16target.png` |
| `FH17.png` | `assets/characters/FH17.png` |
| `FH17exclude.png` | `assets/characters/FH17exclude.png` |
| `FH17target.png` | `assets/characters/FH17target.png` |
| `FS18.png` | `assets/characters/FS18.png` |
| `FS18exclude.png` | `assets/characters/FS18exclude.png` |
| `FS18target.png` | `assets/characters/FS18target.png` |
| `GE19.png` | `assets/characters/GE19.png` |
| `GE19exclude.png` | `assets/characters/GE19exclude.png` |
| `GE19target.png` | `assets/characters/GE19target.png` |
| `GE20.png` | `assets/characters/GE20.png` |
| `GE20exclude.png` | `assets/characters/GE20exclude.png` |
| `GE20target.png` | `assets/characters/GE20target.png` |
| `healthDisplay.png` | `assets/buttons/health-display.png` |
| `healthDisplayOff.png` | `assets/buttons/health-display-off.png` |
| `healthDisplayOn.png` | `assets/buttons/health-display-on.png` |
| `HN21.png` | `assets/characters/HN21.png` |
| `HN21exclude.png` | `assets/characters/HN21exclude.png` |
| `HN21target.png` | `assets/characters/HN21target.png` |
| `HY22.png` | `assets/characters/HY22.png` |
| `HY22exclude.png` | `assets/characters/HY22exclude.png` |
| `HY22target.png` | `assets/characters/HY22target.png` |
| `Intro1.png` | `assets/buttons/intro-1.png` |
| `Intro2.png` | `assets/buttons/intro-2.png` |
| `Intro3.png` | `assets/buttons/intro-3.png` |
| `Intro4.png` | `assets/buttons/intro-4.png` |
| `JE23.png` | `assets/characters/JE23.png` |
| `JE23exclude.png` | `assets/characters/JE23exclude.png` |
| `JE23target.png` | `assets/characters/JE23target.png` |
| `KE25.png` | `assets/characters/KE25.png` |
| `KE25exclude.png` | `assets/characters/KE25exclude.png` |
| `KE25target.png` | `assets/characters/KE25target.png` |
| `LA26.png` | `assets/characters/LA26.png` |
| `LA26exclude.png` | `assets/characters/LA26exclude.png` |
| `LA26target.png` | `assets/characters/LA26target.png` |
| `LO27.png` | `assets/characters/LO27.png` |
| `LO27exclude.png` | `assets/characters/LO27exclude.png` |
| `LO27target.png` | `assets/characters/LO27target.png` |
| `lose.png` | `assets/buttons/lose.png` |
| `LY28.png` | `assets/characters/LY28.png` |
| `LY28exclude.png` | `assets/characters/LY28exclude.png` |
| `LY28target.png` | `assets/characters/LY28target.png` |
| `LZ29.png` | `assets/characters/LZ29.png` |
| `LZ29exclude.png` | `assets/characters/LZ29exclude.png` |
| `LZ29target.png` | `assets/characters/LZ29target.png` |
| `MA30.png` | `assets/characters/MA30.png` |
| `MA30exclude.png` | `assets/characters/MA30exclude.png` |
| `MA30target.png` | `assets/characters/MA30target.png` |
| `MA32.png` | `assets/characters/MA32.png` |
| `MA32exclude.png` | `assets/characters/MA32exclude.png` |
| `MA32target.png` | `assets/characters/MA32target.png` |
| `ME33.png` | `assets/characters/ME33.png` |
| `ME33exclude.png` | `assets/characters/ME33exclude.png` |
| `ME33target.png` | `assets/characters/ME33target.png` |
| `MX31.png` | `assets/characters/MX31.png` |
| `MX31exclude.png` | `assets/characters/MX31exclude.png` |
| `MX31target.png` | `assets/characters/MX31target.png` |
| `NK34.png` | `assets/characters/NK34.png` |
| `NK34exclude.png` | `assets/characters/NK34exclude.png` |
| `NK34target.png` | `assets/characters/NK34target.png` |
| `PL36.png` | `assets/characters/PL36.png` |
| `PL36exclude.png` | `assets/characters/PL36exclude.png` |
| `PL36target.png` | `assets/characters/PL36target.png` |
| `playerProfile.png` | `assets/interface/playerProfile.png` |
| `playerTextLong.png` | `assets/interface/playerTextLong.png` |
| `playerTextShort.png` | `assets/interface/playerTextShort.png` |
| `PR37.png` | `assets/characters/PR37.png` |
| `PR37exclude.png` | `assets/characters/PR37exclude.png` |
| `PR37target.png` | `assets/characters/PR37target.png` |
| `QA35.png` | `assets/characters/QA35.png` |
| `QA35exclude.png` | `assets/characters/QA35exclude.png` |
| `QA35target.png` | `assets/characters/QA35target.png` |
| `RC24.png` | `assets/characters/RC24.png` |
| `RC24exclude.png` | `assets/characters/RC24exclude.png` |
| `RC24target.png` | `assets/characters/RC24target.png` |
| `revoke.png` | `assets/buttons/revoke.png` |
| `title.png` | `assets/buttons/title.png` |
| `win.png` | `assets/buttons/win.png` |
| `buttonClick.wav` | `assets/audio/buttonClick.wav` |
| `characterClick.wav` | `assets/audio/characterClick.wav` |
| `Intro.wav` | `assets/audio/Intro.wav` |
| `Suspicion_Matrix.wav` | `assets/audio/Suspicion_Matrix.wav` |
| `docs/images/screenshots/game-board.png` | `screenshots/game-board.png` |
| `docs/images/screenshots/game-selection.png` | `screenshots/game-selection.png` |
| `docs/images/screenshots/game-title.png` | `screenshots/game-title.png` |
| `docs/images/screenshots/README.md` | `screenshots/README.md` |
| `docs/existing-game-analysis.md` | `docs/archive/existing-game-analysis.md` |
| `docs/phase4a-java-verification.md` | `docs/archive/phase4a-java-verification.md` |
| `docs/phase4c-live-control.md` | `docs/archive/phase4c-live-control.md` |
| `docs/phase5b2-game-arduino-feedback.md` | `docs/archive/phase5b2-game-arduino-feedback.md` |
| `docs/phase5c1-uln2003-review.md` | `docs/archive/phase5c1-uln2003-review.md` |
| `docs/phase5c1-test-results.txt` | `docs/archive/phase5c1-test-results.txt` |
| `docs/phase4b-communication.md` | `docs/protocol.md` |
| `docs/phase5a-arduino-test.md` | `docs/arduino-setup.md` |
| `docs/phase5b1-java-arduino-test.md` | `docs/serial-test.md` |
| `docs/phase5c1-active-buzzer.md` | `docs/buzzer-design.md` |
| `docs/phase7a-projector-ready.md` | `docs/projector-setup.md` |
| `docs/images/phase5c1-breadboard.png` | `docs/archive/images/phase5c1-breadboard.png` |
| `docs/images/phase5c1-breadboard.svg` | `docs/archive/images/phase5c1-breadboard.svg` |
| `docs/images/phase5c1-buzzer-wiring.png` | `docs/archive/images/phase5c1-buzzer-wiring.png` |
| `docs/images/phase5c1-buzzer-wiring.svg` | `docs/archive/images/phase5c1-buzzer-wiring.svg` |
