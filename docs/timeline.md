# Timeline

Reconstructed from `git log` (commit dates only). Day-to-day progress was
tracked informally; this is the retrospective record. Dates are commit
dates, not necessarily the date work started.

## Phases

### Phase 1 — Project bootstrap (May 5 – May 14)
Repo creation, uv environment, initial structure.
- `2026-05-05`: initial commit
- `2026-05-10`: environment setup
- `2026-05-14`: skeleton

### Phase 2 — Core engine (May 15 – May 22)
Maze integration with the assigned `mazegenerator` wheel, player movement,
ghost AI, collision detection.
- `2026-05-15` – `2026-05-16`: maze + player
- `2026-05-19` (8 commits): ghost AI mode state machine
- `2026-05-21` (9 commits): collision, lives, scoring
- `2026-05-22`: polish

### Phase 3 — Game systems (May 24 – May 28)
Pacgums, super-pacgums, level progression, highscore, UI screens.
- `2026-05-24` – `2026-05-26`: pacgums, screens, HUD
- `2026-05-28`: highscore, menus

### Phase 4 — WASM & packaging (May 31 – Jun 4)
pygbag build pipeline, itch.io/butler deploy, freeze workflow during
stabilization.
- `2026-05-31` (11 commits): WASM compatibility (async main, audio variants)
- `2026-06-03` – `2026-06-04`: itch.io deploy, freeze workflow

### Phase 5 — Hardening (Jun 22 – Jun 23)
Lint cleanup, config validation overhaul, documentation.
- `2026-06-22`: Makefile/flake8 cleanup
- `2026-06-23`: config clamping + pacgum count wiring; PM docs

### Phase 6 — Linux downloadable build (Oct 18)
PyInstaller packaging and second itch.io channel for the evaluation
requirement "package available for download".
- `2026-10-18`: frozen-aware entry point, `pac-man.spec`, `make pack`
  and `make push-linux`, live on itch `:linux` (branch
  `packaging/linux-download`, merged same day)

## Velocity

- **Active development days**: ~13 (commits present)
- **Calendar span**: May 5 – Oct 18, with gaps for other coursework
- **Total commits**: 88

See [gantt.md](gantt.md) for the visual timeline.
