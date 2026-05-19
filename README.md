*This project has been created as part of the 42 curriculum by ksmailov, abalcu*

# Pac-Man

## Description

A Pac-Man clone built in Python using Pygame, with procedurally generated mazes, ghost AI, scoring, and highscore persistence. The game is deployed as a WebAssembly build playable in the browser via Itch.io.

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
```

### Packaging for Itch.io

Pygbag compiles the game to WebAssembly for browser play:

```bash
make build
```

Serve locally: `python3 -m http.server 8000 --directory build/web`

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
| `pacgum` | int | `42` | Pacgum count |
| `points_per_pacgum` | int | `10` | Points per pacgum (min 1) |
| `points_per_super_pacgum` | int | `50` | Points per super-pacgum (min 1) |
| `points_per_ghost` | int | `200` | Points per eaten ghost (min 1) |
| `seed` | int | `42` | Base seed for level 1 maze |
| `level_max_time` | int | `90` | Seconds per level (min 10) |

- Missing keys fall back to defaults.
- Invalid values are clamped to safe minimums.
- Unknown keys are silently ignored.
- Levels are infinite — each level uses `seed + level_index` for maze generation.

## Highscore

Highscores are stored in a JSON file (path configured via `highscore_filename`). The system keeps the top 10 entries sorted by score (descending).

- Player names: max 10 characters, alphanumeric and spaces only.
- Scores: non-negative integers.
- Missing or corrupt files are handled gracefully — the list resets to empty.
- Highscores are loaded at game start and saved when a new entry is added.

## Maze Generation

## Implementation

### Core modules

- **`config.py`** — Loads JSON config with pydantic validation, comment stripping, value clamping, and default fallbacks.
- **`maze.py`** — Generates and renders the maze. Provides `is_walkable()` for collision and `center` property (BFS) for spawn point.
- **`player.py`** — Grid-based movement with direction queuing, sprite rotation for facing direction, and smooth pixel interpolation.
- **`pacgums.py`** — Places pacgums on all walkable corridors, super-pacgums in 4 corners (BFS). Tracks remaining count for level completion.
- **`highscore.py`** — Persistent JSON highscore storage with name validation, top 10 ranking, and error resilience.
- **`game.py`** — Game state manager: owns score, lives, level, player, pacgums. Handles events, updates, drawing, and HUD.
- **`pacman.py`** — Entry point: loads config, initializes pygame, runs the game loop.

### Key design decisions

- **Movement**: Grid-based with direction queuing. Player moves continuously until hitting a wall. Queued direction executes at the next valid intersection.
- **Ghost AI** (planned): Goal-based direction choosing at intersections using Euclidean distance — no A* needed.
- **Collision**: Grid position matching for pacgum eating (tile-based, not circle collision).
- **Rendering**: Maze is pre-rendered to a surface for fast blitting. Pacgums drawn as circles each frame. HUD is a 40px bar above the maze.

## General Software Architecture

```
pac-man.py              → entry point
src/pac_man/
├── __init__.py          → package init
├── config.py            → ConfigData (pydantic) + Config wrapper
├── constants.py         → shared constants (tile size, speeds, colors)
├── font.py              → Text rendering (PressStart2P font)
├── game.py              → Game class (state, update, draw, HUD)
├── highscore.py         → Highscore load/save/validate
├── maze.py              → Maze generation, rendering, collision
├── pacgums.py           → Pacgum/super-pacgum placement and rendering
├── pacman.py            → Main game loop
├── player.py            → Player movement, animation, direction queue
└── sprites.py           → Spritesheet loader
```

### Class relationships

- `Game` owns `Maze`, `Player`, `Pacgums`, and reads `Config`
- `Player` references `Maze` for `is_walkable()` and `center`
- `Pacgums` references `Maze.out` grid for placement
- `Highscore` is standalone, used by game-over/victory screens (planned)

## Project Management

Project management documents are available in the `docs/` directory (planned).
