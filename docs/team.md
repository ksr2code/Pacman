# Team Organization

Team of two, 42 curriculum. Work was split by area of ownership with heavy
overlap on architecture decisions.

## Ownership

| Area | Primary | Notes |
|------|---------|-------|
| Project setup, uv, Makefile, CI | `<abalcu>` | |
| Maze integration (`maze.py`, mazegenerator adapter) | `<abalcu>` | |
| Player movement & animation (`player.py`) | `<ksmailov>` | |
| Ghost AI (`ghost.py`) | `<ksmailov>` | Pair-designed the mode state machine |
| Game engine (`game.py`) | `<ksmailov>` | |
| UI / screens (`screens.py`) | `<ksmailov>` | |
| Config system (`config.py`) | `<ksmailov>` | |
| Highscore (`highscore.py`) | `<ksmailov>` | |
| WASM / pygbag packaging, itch.io deploy | `<abalcu>` | |
| Sound & sprites (`sound.py`, `sprites.py`) | `<abalcu>` | |
| Documentation, README | `<abalcu>` | |

## Decision-making

- **Architecture**: decided jointly in design sessions; consensus required
  for module boundaries and the game-loop structure.
- **Implementation**: primary owner proposes; the other reviews via code
  review before merge.
- **Blocking issues**: escalated to a sync session; if unresolved, the
  smallest reversible option was chosen and revisited later (see
  [risks.md](risks.md) for concrete cases).
- **Tooling choices** (uv, pygbag, pygame-ce): decided once at project
  start, documented in [decisions.md](decisions.md).

## Conflicts & resolutions

_None recorded during development._ If any occurred, list them here with the
chosen resolution and rationale.
