# Verification evidence

This is a curated summary of recorded project checks, not a CI badge or a claim that tests run automatically on GitHub. Test source is included so the software checks can be repeated.

## Recorded software runs

The Phase 10 reruns completed on 2026-11-05 with JDK 17 and the existing Python 3.12 environment:

| Suite | Result | Scope |
| --- | --- | --- |
| Python vision/calibration/client | 73 tests passed | Geometry, pinch state, camera failure mocks, calibration metadata, live-client behavior and MediaPipe inference on blank frames |
| Python ↔ Java TCP | 16 tests passed | Actual loopback server/client communication, validation, duplicate handling and Swing dispatch |
| Presentation fixture | 32 checks passed | Resizing, coordinate hit testing, mouse dispatch, icon/font scaling and identity |
| Java serial controller | 20 checks passed | Hardware-free connection, command and error handling |
| Real Board + fake Arduino | 19 normal-mode checks; 22 presentation-mode checks passed | Real game actions, mouse/TCP routes, exactly-once feedback and all 24 cards reachable at tested sizes |
| Existing mapping/JSON/Swing harness | Passed | Mapping round-trips, strict parsing and hidden/disabled/covered controls |

Earlier Phase 5C-1 evidence records a successful Mega-target compile (3,478 bytes flash, 265 bytes SRAM) and 32 hardware-free firmware checks. See [the firmware test record](archive/phase5c1-test-results.txt). Those checks were not rerun for the portfolio documentation.

No new software feature or game logic changed in Phase 8. The portfolio work checked documentation links, image decoding and the proposed Git file set; it captured three real Swing views without opening a physical serial port or camera.

The new `AssetLoadingTest` decodes every PNG and WAV in `assets/`, checks loaded icons across the title, four introduction screens, game and both results, and exercises every character portrait variant. It runs through `build-phase7a.ps1 -Test`. The cleanup report records file preservation and native KiCad rechecks.

## Repeat the software checks

Complete [the setup guide](setup.md) first. Run from the root:

```powershell
.\build-phase7a.ps1 -Test
Push-Location computer-vision
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
Pop-Location
$env:JAVA_TEST_CLASSPATH = 'build-phase5b2;arduino\java\lib\jSerialComm-2.11.4.jar'
.\computer-vision\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

These desktop tests require an interactive Windows session and permission for local loopback TCP. They may briefly display game/test windows and play existing game audio. They use a fake Arduino. The vision tests do not acquire a camera stream. For temporary-directory restrictions, the Phase 7A guide supplies a project-local TEMP/TMP configuration.

The raw phase logs remain available locally; curated phase records and this summary are included in the proposed Git set. Re-running tests generates fresh local results. This repository has no configured hosted CI workflow.

## Physical and design evidence

The developer reported physically successful mouse/pinch gameplay and USB-serial Mega onboard LED feedback. These user-reported integration checks are distinct from automated tests run by the assistant.

The owner has confirmed successful PN2222 wiring and a working buzzer circuit. Fabrication and assembled-PCB testing have not been reported. The projector and external webcam have not been purchased/tested in this workflow. The Phase 9 native schematic/PCB checks are recorded separately; real mounting/optical validation remains outstanding. See [hardware validation](hardware-validation-status.md), [projector preparation](projector-setup.md) and [concept CAD](../hardware/concept-cad/README.md) for the precise boundaries. No frame-rate, latency, accuracy or usability benchmark is asserted.
