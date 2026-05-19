*This project has been created as part of the 42 curriculum by ksmailov, abalcu*

# Pacman

## Description

## Instructions

After installation (with pip/uv/poetry), the program can be executed in two ways:

- **scipt mode** 
```bash 
$> pac-man config.json
```

- **calling the python interpretor**
```bash 
$> python3 pac-man.py config.json
```

### Packaging for Itch.io

Pygbag compiles the Python game to WebAssembly, so it runs directly in the 
browser on Itch.io.

Pygbag is ideal because:
- Itch.io has native web support
- No download needed
- Can be private/unlisted easily
- Single packaging workflow


## Resources
- [Pacmancode](https://pacmancode.com/)
- 

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
| `points_per_pacgum` | int | `10` | Points per pacgum |
| `points_per_super_pacgum` | int | `50` | Points per super-pacgum |
| `points_per_ghost` | int | `200` | Points per eaten ghost |
| `seed` | int | `42` | Base seed for level 1 maze |
| `level_max_time` | int | `90` | Seconds per level (min 10) |

- Missing keys fall back to defaults.
- Invalid values are clamped to safe minimums.
- Unknown keys are silently ignored.
- Each level uses `seed + level_index` for maze generation (levels are infinite).

## Highscore

## Maze Generation

## Implementation

## General software architecture

## Project Management

