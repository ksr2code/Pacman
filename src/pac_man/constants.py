from typing import Sequence

# Sprite and display constants
TILE_SIZE = 32  # pixels
HUD_HEIGHT = 40  # pixels above maze
PACMAN_SPEED = 5  # tiles per frame
GHOST_SPEED = 5

# Colors (RGB tuples)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_RED = (255, 0, 0)

SCATTER_TIME = 7.0
CHASE_TIME = 20.0
INVINCIBLE_TIME = 1.5

STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_PAUSE = "pause"

__all__: Sequence[str] = [
    "TILE_SIZE",
    "HUD_HEIGHT",
    "PACMAN_SPEED",
    "GHOST_SPEED",
    "SCATTER_TIME",
    "CHASE_TIME",
    "INVINCIBLE_TIME",
    "COLOR_BLACK",
    "COLOR_WHITE",
    "COLOR_YELLOW",
    "COLOR_RED",
    "STATE_PLAYING",
    "STATE_GAME_OVER",
    "STATE_PAUSE",
]
