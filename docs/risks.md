# Risk Register

Top risks encountered or anticipated during the project, with the mitigation
applied. Risks are informal — this is the retrospective record, not a
living tracker.

| # | Risk | Impact | Likelihood | Mitigation | Status |
|---|------|--------|------------|------------|--------|
| R1 | **WASM/async incompatibility** — blocking pygame calls crash pygbag in the browser | High | High | Async main loop with `await asyncio.sleep(0)`; dual `.ogg` audio variants (`*-pygbag.ogg`); repo freeze workflow during stabilization | Closed |
| R2 | **External `mazegenerator` dependency** — wheel from another group, interface uncontrolled | High | Medium | Vendored via `[tool.uv.sources]` in `pyproject.toml`; defensive BFS adapter in `maze.py` decouples grid encoding from rendering | Closed |
| R3 | **Config brittleness** — bad user input crashes the game on start (spec §V.3 violation) | High | Medium | Clamping + type validation pipeline in `config.py` (Jun 23 fix); warnings to stderr; non-dict root falls back to defaults | Closed |
| R4 | **Level unsolvability** — random pacgum placement could exceed corridor cells or block completion | Medium | Medium | Local seeded `random.Random`; `count` clamped to `len(candidates)`; 4 super-pacgums reserved in corners before random selection (Jun 23 fix) | Closed |
| R5 | **Cross-platform audio codecs** — desktop vs browser `.ogg` support differs | Medium | Medium | Per-target asset variants shipped under `src/assets/sounds/`; runtime picks the platform-appropriate file | Closed |
| R6 | **`uv.lock` wheel filename mismatch** — wheel file named `mazegenerator-1` reports version `2.0.1`, breaking strict uv checks | Low | High | Documented; `UV_SKIP_WHEEL_FILENAME_CHECK=1` workaround in CI/dev workflow | Open (upstream) |

## Risk process

- Risks were identified reactively during development (a problem surfaced →
  logged here with its mitigation), not via a forward-looking exercise.
- Each "Closed" risk has a concrete code/config artifact as evidence (see
  file references in the table).
- R6 remains open because the fix belongs to the upstream `mazegenerator`
  wheel, not this project.
