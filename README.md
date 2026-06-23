*This project has been created as part of the 42 curriculum by ksmailov, abalcu*

# Pac-Man

## Description

A Pac-Man clone built in Python using Pygame, with procedurally generated mazes, ghost AI (scatter/chase modes, goal-based direction), death/lives system, scoring, and highscore persistence.

## Instructions

### Install dependencies

```bash
make install
```

### Run the game

```bash
make run
# or directly:
python3 pac-man.py config.json
```

### Other commands

```bash
make lint        # flake8 + mypy
make debug       # run with pdb
make clean       # remove caches
make push        # push the build to ithc.io
```

### Packaging for Itch.io

Pygbag compiles the game to WebAssembly for browser play:

```bash
make build
```

## Resources

- [Pacmancode](https://pacmancode.com/) — Pac-Man game development tutorial

## Configuration

The game is configured via a JSON file passed as a command-line argument:

```bash
python3 pac-man.py config.json
```

The config file supports standard JSON with comment lines starting with `#` or `//`.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `highscore_filename` | string | `"highscore.json"` | Path to highscore file |
| `width` | int | `14` | Maze width (min 5) |
| `height` | int | `18` | Maze height (min 5) |
| `lives` | int | `3` | Starting lives (min 1) |
| `pacgum` | int | `42` | Pacgum count per level (min 0; clamped to corridors) |
| `points_per_pacgum` | int | `10` | Points per pacgum (min 1) |
| `points_per_super_pacgum` | int | `50` | Points per super-pacgum (min 1) |
| `points_per_ghost` | int | `200` | Points per eaten ghost (min 1) |
| `seed` | int | `42` | Base seed for level 1 maze |
| `level_max_time` | int | `90` | Seconds per level (min 10) |

- The game has 10 levels; each level uses `seed = base_seed + level - 1` for maze generation.
- Missing keys fall back to dataclass defaults above (the shipped `config.json` is a sample override).
- Invalid values are clamped to safe minimums and logged to stderr.
- Unknown keys are silently ignored.
- Wrong types (e.g. `width: "abc"`, `cheat: "yes"`, `lives: true`) fall back to defaults; `bool` is rejected for `int` fields.

## Highscore

Highscores are stored in a JSON file (path configured via `highscore_filename`). The system keeps the top 10 entries sorted by score (descending).

- Player names: max 10 characters, alphanumeric and spaces only.
- Scores: non-negative integers.
- Missing or corrupt files are handled gracefully — the list resets to empty.
- Highscores are loaded at game start and saved when a new entry is added.

## Maze Generation

Per subject §V.4, this project does **not** implement its own generator. The maze
is produced by the assigned `A-Maze-ing` package (`mazegenerator`, v2.0.1) from
another group, consumed unmodified.

- **Vendoring**: the wheel ships at `packages/mazegenerator-*.whl` and is declared
  as a local source via `[tool.uv.sources]` in `pyproject.toml`. It will be
  re-installed during peer review.
- **Interface used**: `MazeGenerator(size=(width, height), perfect=False)` →
  `.generate(seed)` → `.maze` property returns a `list[list[int]]` bitmask grid.
- **PERFECT=False**: subject §V.4 mandates this so the generator produces
  Pac-Man-compatible corridors (loops/open rooms rather than perfect mazes). We
  pass it explicitly at `maze.py:27` for self-documentation.
- **Bitmask encoding**: `N=1, E=2, S=4, W=8`; a bit set means the wall is present
  on that side of the cell.
- **Grid adaptation** (`maze.py:_build_maze`): the package's cell grid is doubled
  to a `(2h+1)×(2w+1)` render grid — odd rows/cols are corridors, even indices
  are walls/corners. Walls are placed per neighbor bits; corners are selected
  from 15 sprite variants indexed by a 4-bit neighbor-wall mask.
- **Rendering**: the full maze is pre-rendered once per level to a single
  `pygame.Surface` (`_render_maze_to_surface`) so each frame is a single blit.
- **Seeds**: level 1 uses `cfg.seed`; each subsequent level uses
  `cfg.seed + level - 1` (deterministic mazes for reproducible playtests).
- **Error handling**: maze construction is wrapped in `try/except`, logged to
  stderr, and re-raised so the game fails cleanly rather than silently (§V.4).

## Implementation

### Core modules

- **`config.py`** — Loads JSON config with stdlib `dataclass` validation, comment stripping, value clamping, type checking, and default fallbacks.
- **`maze.py`** — Generates and renders the maze. Provides `is_walkable()` for collision and `center` property (BFS) for spawn point.
- **`player.py`** — Grid-based movement with direction queuing, sprite rotation for facing direction, and smooth pixel interpolation.
- **`ghost.py`** — Ghost AI with goal-based direction choosing at intersections, no-U-turn rule, and scatter/chase modes.
- **`pacgums.py`** — Places up to `cfg.pacgum` pacgums as a seeded random subset of corridors (clamped to corridor count); super-pacgums always placed in 4 corners (BFS). Tracks remaining count for level completion.
- **`highscore.py`** — Persistent JSON highscore storage with name validation, top 10 ranking, and error resilience.
- **`game.py`** — Game state manager: owns score, lives, level, player, ghost, pacgums. Handles events, updates, drawing, HUD, death/lives, invincibility, and game over.
- **`main.py`** — App class and async game loop (pygbag/WASM entry point).
- **`screens.py`** — All UI screens: title menu, pause, game over, victory, name entry, highscores, instructions, cheat menu.
- **`sound.py`** — Sound wrapper; missing-file tolerant (silent fallback + stderr warning).
- **`pac-man.py`** — Repo-root entry point: parses CLI args, loads config, runs the async loop.

### Key design decisions

- **Movement**: Grid-based with direction queuing. Player moves continuously until hitting a wall. Queued direction executes at the next valid intersection.
- **Ghost AI**: Goal-based direction choosing at intersections using Euclidean distance. Modes alternate between scatter (7s, targets corner) and chase (20s, targets Pac-Man). Ghosts cannot U-turn.
- **Death/Lives**: Ghost collision costs a life. 1.5s invincibility after reset. Game over at 0 lives → game over screen → name entry → title menu.
- **Collision**: Grid position matching for pacgum eating (tile-based, not circle collision).
- **Rendering**: Maze is pre-rendered to a surface for fast blitting. Pacgums drawn as circles each frame. HUD is a 40px bar above the maze.

## General Software Architecture

```
pac-man.py              → repo-root entry point (CLI args, config load)
src/
├── __init__.py          → package init
├── config.py            → ConfigData (dataclass) + Config wrapper
├── constants.py         → shared constants (tile size, speeds, colors)
├── font.py              → Text rendering (PressStart2P font)
├── game.py              → Game class (state, update, draw, HUD)
├── ghost.py             → Ghost AI, goal-based movement, scatter/chase
├── highscore.py         → Highscore load/save/validate
├── maze.py              → Maze generation, rendering, collision
├── main.py              → App class + async game loop (pygbag entry)
├── pacgums.py           → Pacgum/super-pacgum placement and rendering
├── player.py            → Player movement, animation, direction queue
├── screens.py           → All UI screens (title, pause, game over, etc.)
├── sound.py             → Sound wrapper (missing-file tolerant)
└── sprites.py           → Spritesheet loader
```

### Class relationships

- `Game` owns `Maze`, `Player`, `Ghost`, `Pacgums`, and reads `Config`
- `Player` references `Maze` for `is_walkable()` and `center`
- `Pacgums` references `Maze.out` grid for placement
- `Highscore` is standalone; wired into game-over/victory screens and title menu

## Project Management

Project management documents are in the [`docs/`](docs/README.md) directory:
methodology, team organization, timeline (with Gantt chart), risk register,
technical decisions, and an acceptance test plan.
