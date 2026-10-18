# Pac-Man — Linux package

## Run

1. Make the file executable: `chmod +x Pac-Man`
2. Run it: `./Pac-Man`

No Python or other dependencies required.

## Controls

- Arrow keys / WASD — move
- Up / Down / W / S — navigate menus
- Enter / Space — confirm
- Esc — pause / back
- C — cheat menu (only if `cheat: true` in the config)
- Backspace — delete character when entering your name

## Configuration

The game starts with built-in defaults. To customize, create a
`config.json` file **next to the executable** (same folder) with any of:

`highscore_filename`, `width`, `height`, `lives`, `pacgum`,
`points_per_pacgum`, `points_per_super_pacgum`, `points_per_ghost`,
`seed`, `level_max_time`, `cheat`

Lines starting with `#` or `//` are treated as comments. Invalid values
are clamped to safe defaults with a warning.

## Saves

Highscores persist in `highscore.json` next to the executable.
