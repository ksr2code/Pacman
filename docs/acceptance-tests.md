# Acceptance Test Plan

Feature-level acceptance tests. Each row is a single test case with
reproducible steps and the current status. Statuses:

- **PASS** — verified working
- **FAIL** — known broken, with date discovered
- **FIXED** — was FAIL, now PASS, with date fixed

Manual tests are run via `make run` (or `make build` + browser for WASM).
Automated unit tests are out of scope for this project (no `test/` dir).

---

## CFG — Configuration

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| CFG-01 | Run with valid `config.json` | Game starts | PASS | |
| CFG-02 | Set `width: 0` | Starts, width clamped to 5, stderr warning | FIXED Jun 23 | Was FAIL: silently accepted |
| CFG-03 | Add unknown key `foo: 1` | Starts, key ignored, stderr warning | FIXED Jun 23 | Was FAIL: TypeError crash |
| CFG-04 | Set `width: "abc"` | Starts, width=14 default, stderr warning | FIXED Jun 23 | Was FAIL: TypeError crash |
| CFG-05 | Set `cheat: "yes"` (string for bool) | Starts, cheat=False default | FIXED Jun 23 | bool/int trap handled |
| CFG-06 | Set `lives: true` (bool for int) | Starts, lives=3 default | FIXED Jun 23 | bool rejected for int |
| CFG-07 | Run with missing file | Clean error, exit, no traceback | PASS | |
| CFG-08 | Run with malformed JSON | Clean error, no traceback | PASS | |
| CFG-09 | Config with `#` comment lines | Comments stripped, parses | PASS | |

## MAZE — Maze generation

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| MAZE-01 | Start level 1 twice with same seed | Identical maze | PASS | Seed = `cfg.seed` |
| MAZE-02 | Advance to level 2 | Different maze (seed+1) | PASS | |
| MAZE-03 | 4 corners reachable | Super-pacgum in each corner | PASS | BFS resolves nearest valid cell |
| MAZE-04 | Mazegenerator fails | Handled cleanly, no crash | PASS | Defensive adapter in `maze.py` |

## PLAYER — Player movement

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| PLR-01 | Press arrow / WASD | Pac-Man turns that direction | PASS | |
| PLR-02 | Hold into a wall | Stops at wall | PASS | |
| PLR-03 | Queue a turn before an intersection | Turns at the next valid cell | PASS | Direction queuing |
| PLR-04 | Touch a non-edible ghost | Lose a life, respawn center | PASS | |

## GHOST — Ghost AI

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| GHO-01 | Wait in scatter phase | Ghosts move to their corners | PASS | 7s scatter |
| GHO-02 | Enter chase phase | Ghosts pursue player | PASS | 20s chase, Euclidean |
| GHO-03 | Eat a super-pacgum | Ghosts turn edible (freight) | PASS | |
| GHO-04 | Eat an edible ghost | Ghost returns home (eyes), respawns | PASS | BFS pathfinding |
| GHO-05 | Two ghosts eaten same chain | 200, then 400 points | PASS | Score doubles per chain |

## PAC — Pacgums & super-pacgums

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| PAC-01 | Set `pacgum: 5` | 5 pacgums placed, level winnable | FIXED Jun 23 | Was N/A: count was ignored |
| PAC-02 | Set `pacgum: 0` | 4 supers only, level winnable | FIXED Jun 23 | Min 0 allowed |
| PAC-03 | Set `pacgum: 9999` on small maze | Clamped to corridor count | FIXED Jun 23 | No overflow |
| PAC-04 | Same seed → same pacgum layout | Deterministic | FIXED Jun 23 | Local seeded RNG |
| PAC-05 | 4 corners always have supers | Regardless of `pacgum` value | FIXED Jun 23 | Supers reserved first |

## SCORE — Scoring

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| SCR-01 | Eat pacgum | +`points_per_pacgum` | PASS | |
| SCR-02 | Eat super-pacgum | +`points_per_super_pacgum` + fright | PASS | |
| SCR-03 | Eat edible ghost | +`points_per_ghost`, doubles per chain | PASS | |
| SCR-04 | Score never decreases | Monotonic | PASS | |

## LVL — Level progression

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| LVL-01 | Eat all pacgums | Advance to next level | PASS | |
| LVL-02 | Complete level 10 | Victory screen | PASS | `NUM_LEVELS=10` |
| LVL-03 | Lose all lives | Game over screen | PASS | |
| LVL-04 | Score & lives carry between levels | Persisted | PASS | |
| LVL-05 | Timer reaches 0 | Game over | PASS | `level_max_time` per level |

## HS — Highscore

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| HS-01 | Win/lose → enter name → enter | Saved to JSON, shown in menu | PASS | |
| HS-02 | Enter name > 10 chars | Truncated to 10 | PASS | |
| HS-03 | Enter name with symbols | Symbols stripped, alnum+space only | PASS | |
| HS-04 | Corrupt `highscore.json` | Handled, resets to empty | PASS | |
| HS-05 | More than 10 entries | Top 10 kept, sorted desc | PASS | |

## UI — User interface

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| UI-01 | Launch game | Title screen with menu | PASS | |
| UI-02 | Press SPACE during game | Pause menu | PASS | |
| UI-03 | Resume from pause | Returns to game | PASS | |
| UI-04 | Return to menu from pause | Abandons game, back to title | PASS | |
| UI-05 | HUD shows score/level/lives/timer | Always visible | PASS | |
| UI-06 | Open Instructions | Shows controls and rules | PASS | |

## CHT — Cheat mode

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| CHT-01 | Press C (if `cheat: true`) | Cheat menu opens | PASS | |
| CHT-02 | Toggle invincibility | Ghosts can't kill player | PASS | |
| CHT-03 | Toggle ghost freeze | Ghosts stop moving | PASS | |
| CHT-04 | Toggle speed boost | Player moves faster | PASS | |
| CHT-05 | Level skip | Immediately wins level | PASS | |
| CHT-06 | Extra life | +1 life | PASS | |

## WASM — WebAssembly build

| ID | Steps | Expected | Status | Notes |
|----|-------|----------|--------|-------|
| WASM-01 | `make build` then open in browser | Game loads, runs | PASS | |
| WASM-02 | Play through in browser | No tab freeze | PASS | `asyncio.sleep(0)` per frame |
| WASM-03 | Audio in browser | Sounds play | PASS | `-pygbag.ogg` variants |
| WASM-04 | `make push` | Deploys to itch.io | PASS | butler |

---

## Known issues not covered above

- **R6 (open)**: `uv.lock` wheel filename mismatch for `mazegenerator`
  requires `UV_SKIP_WHEEL_FILENAME_CHECK=1`. Upstream issue.
- **Pre-existing mypy errors** in `screens.py`, `maze.py`, `font.py`,
  `main.py` (unannotated returns / unused ignores) — not blocking, flagged
  for a future cleanup pass.
