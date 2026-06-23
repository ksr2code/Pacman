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

## Velocity

- **Active development days**: ~12 (commits present)
- **Calendar span**: 7 weeks (May 5 – Jun 23), with gaps for other coursework
- **Total commits**: ~65

See [gantt.md](gantt.md) for the visual timeline.
