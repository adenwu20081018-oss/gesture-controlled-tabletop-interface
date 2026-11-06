# Hardware validation status

## Current evidence

| Subsystem | Status | Evidence / boundary |
| --- | --- | --- |
| Webcam gestures and Java | Physically tested | Owner confirmed mouse and pinch gameplay |
| Mega USB serial and onboard LED | Physically tested | Owner confirmed commands and game-triggered LED feedback |
| PN2222 active-buzzer circuit | **Working — owner tested** | Owner confirmed the previously discussed transistor wiring pattern works; supersedes Phase 5C-1 pending status |
| BUZZ firmware | Implemented | Standalone command; no automatic Java game sound integration |
| KiCad buzzer PCB | **Editable, routed PCB design** | Components, footprints, copper traces, ground zone and board outline; native ERC/DRC records available |
| Manufactured/assembled PCB | Not reported | Working wired circuit does not establish PCB fabrication, footprint fit or assembled-board operation |
| Projector / external webcam | Planned; physical testing not reported | Laptop workflow exists |
| WS2812B strip | Planned | No circuit or firmware integration |

The working circuit uses D8, a PN2222/2N2222A transistor, 470 Ω base resistor, 10 kΩ pull-down, 1N4007 and active buzzer. Functional E/B/C labels remain useful. The owner's successful test is accepted as current evidence; no new physical lead ordering or measured current is inferred from it.

## Design checks and history

See [PCB validation](../hardware/kicad/buzzer-driver-pcb/VALIDATION.md) for native KiCad checks and [connections](pin-connections.md) for the working circuit. KiCad 10.0.8 is installed; both schematics parsed successfully in the Phase 10 checks. The earlier Phase 6A lack of KiCad is historical, not current status.

Archived Phase 5C-1 records describe what was known then. Their unverified/pending statements are superseded by the owner's latest successful circuit test. No new physical test was performed by the assistant. PCB renders are CAD outputs, not photographs of fabricated hardware. The separate desk/optics concept CAD remains unbuilt and unvalidated.
