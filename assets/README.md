# Original game assets

The original artwork and audio are preserved byte-for-byte. Run Java from the repository root; `Board.java` loads files from `assets/` through filesystem paths. No Maven/resource packaging is required.

- `buttons/`: every button/control background, including size variants, revoke, health toggles, clickable title/introduction and win/lose screens. Text on ordinary action buttons is drawn by Swing.
- `characters/`: all 37 character portraits with normal, excluded and target variants (111 PNGs). Names retain their character IDs.
- `interface/`: profile artwork, text panels, battery and the preserved unused disguise image.
- `audio/`: all four original WAV files.

`button-base.png`, `health-display.png` and `interface/AIDisguise.png` were not referenced by the original Board's string literals. They are retained as original artwork. Character portraits remain separate even though they are displayed on clickable cards.

See [credits](../docs/credits.md). The asset regression checks decode every PNG/WAV and exercise title, introduction, character variants, health controls and both result screens.
