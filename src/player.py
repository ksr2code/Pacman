from __future__ import annotations


import pygame

import constants as const
from maze import Maze
from sprites import SpriteSheet

DIRECTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}

DIR_NAMES = {v: k for k, v in DIRECTIONS.items()}


class Player:
    """Grid-based player movement with direction queuing and animation."""

    def __init__(self, maze: Maze) -> None:
        """Place player at maze center, load animation frames."""
        self.maze = maze
        self.speed: float = const.PACMAN_SPEED * const.TILE_SIZE

        row, col = maze.center
        self.grid_row = row
        self.grid_col = col
        self._prev_row: int = row
        self._prev_col: int = col
        self.px: float = col * const.TILE_SIZE
        self.py: float = row * const.TILE_SIZE

        self.direction: tuple[int, int] | None = None
        self.next_direction: tuple[int, int] | None = None

        ss = SpriteSheet("spritesheet_nopink.png")
        closed = ss.getImageGrid(4, 0)
        self.frames: dict[str, list[pygame.Surface]] = {
            "left": [
                closed,
                ss.getImageGrid(0, 0),
                ss.getImageGrid(0, 1),
            ],
            "right": [
                closed,
                ss.getImageGrid(1, 0),
                ss.getImageGrid(1, 1),
            ],
            "down": [
                closed,
                ss.getImageGrid(2, 0),
                ss.getImageGrid(2, 1),
            ],
            "up": [
                closed,
                ss.getImageGrid(3, 0),
                ss.getImageGrid(3, 1),
            ],
        }
        self.last_dir: str = "right"
        self.anim_time: float = 0.0
        self.death_frames: list[pygame.Surface] = [
            ss.getImageGrid(col, 6) for col in range(11)
        ]

    def set_direction(self, name: str) -> None:
        """Queue the next direction; applied at the next walkable cell."""
        d = DIRECTIONS.get(name)
        if d:
            self.next_direction = d

    def _try_queued_direction(self) -> None:
        """Apply queued direction if next cell walkable."""
        if self.next_direction and self.maze.is_walkable(
            self.grid_row + self.next_direction[0],
            self.grid_col + self.next_direction[1],
        ):
            self.direction = self.next_direction
            self.next_direction = None

    def update(self, dt: float) -> None:
        """Move toward the target cell; stop on walls, apply queued turns."""
        self._prev_row = self.grid_row
        self._prev_col = self.grid_col
        if not self.direction:
            self._try_queued_direction()
            if not self.direction:
                return

        move = self.speed * dt
        dr, dc = self.direction

        target_px = (self.grid_col + dc) * const.TILE_SIZE
        target_py = (self.grid_row + dr) * const.TILE_SIZE

        dx = target_px - self.px
        dy = target_py - self.py
        dist = (dx * dx + dy * dy) ** 0.5

        if dist <= move:
            self.px = target_px
            self.py = target_py
            self.grid_row += dr
            self.grid_col += dc
            self._try_queued_direction()
            if self.direction and not self.maze.is_walkable(
                self.grid_row + self.direction[0],
                self.grid_col + self.direction[1],
            ):
                self.direction = None
        else:
            self.px += (dx / dist) * move
            self.py += (dy / dist) * move

        self.anim_time += dt

    def reset(self, row: int, col: int) -> None:
        """Reset position and clear direction state."""
        self.grid_row = row
        self.grid_col = col
        self._prev_row = row
        self._prev_col = col
        self.px = col * const.TILE_SIZE
        self.py = row * const.TILE_SIZE
        self.direction = None
        self.next_direction = None

    def draw(self, screen: pygame.Surface, offset_y: int = 0) -> None:
        """Render the current animation frame for the facing direction."""
        if self.direction:
            self.last_dir = DIR_NAMES.get(self.direction, self.last_dir)
        idx = int(self.anim_time * 10) % len(self.frames[self.last_dir])
        frame = self.frames[self.last_dir][idx]
        screen.blit(frame, (self.px, self.py + offset_y))

    def draw_death(
        self,
        screen: pygame.Surface,
        offset_y: int,
        progress: float,
    ) -> None:
        """Render the death animation frame at the given progress (0..1)."""
        idx = min(int(progress * len(self.death_frames)), 10)
        frame = self.death_frames[idx]
        screen.blit(frame, (self.px, self.py + offset_y))
