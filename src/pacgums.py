import random
from typing import Any

import pygame

import constants as const
from maze import Maze
from sound import Sound
from sprites import SpriteSheet

FRUIT_COLS = [8, 9, 10]
FRUIT_ROWS = [4, 5]


class Pacgums:
    def __init__(
        self,
        maze: Maze,
        exclude: set[tuple[int, int]],
        spritesheet: SpriteSheet | None = None,
        count: int = 0,
        seed: int = 0,
    ) -> None:
        """Place up to `count` pacgums on random corridors, plus 4 supers. """
        self.pacgums: dict[tuple[int, int], str] = {}
        self._blink_timer: float = 0.0
        self._blink_visible: bool = True
        self._eat_sounds: list[Sound] = [
            Sound("eat_dot_0.ogg"),
            Sound("eat_dot_1.ogg"),
        ]
        self._eat_idx: int = 0
        self._fruit_sprites: dict[tuple[int, int], Any] = {}
        self._ss = spritesheet

        super_cells = self._resolve_supers(maze)
        super_set = set(super_cells)

        candidates = [
            (r, c)
            for r in range(1, len(maze.out), 2)
            for c in range(1, len(maze.out[0]), 2)
            if (r, c) not in exclude
            and (r, c) not in super_set
            and maze.out[r][c] is None
            and self._has_exit(maze, r, c)
        ]

        rng = random.Random(seed)
        count = max(0, min(count, len(candidates)))
        if count < len(candidates):
            chosen = set(rng.sample(candidates, count))
        else:
            chosen = set(candidates)

        for pos in chosen:
            self.pacgums[pos] = "pacgum"
        for pos in super_cells:
            self.pacgums[pos] = "super"
            if self._ss is not None:
                col = rng.choice(FRUIT_COLS)
                row = rng.choice(FRUIT_ROWS)
                self._fruit_sprites[pos] = self._ss.getImageGrid(col, row)

    def _has_exit(self, maze: Maze, r: int, c: int) -> bool:
        return any(
            maze.is_walkable(r + dr, c + dc)
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))
        )

    def _resolve_supers(self, maze: Maze) -> list[tuple[int, int]]:
        """BFS from each of the 4 maze corners to the nearest valid cell. """
        corners = [
            (1, 1),
            (1, len(maze.out[0]) - 2),
            (len(maze.out) - 2, 1),
            (len(maze.out) - 2, len(maze.out[0]) - 2),
        ]
        cells: list[tuple[int, int]] = []
        for cr, cc in corners:
            pos = self._bfs_walkable(maze, cr | 1, cc | 1)
            if pos is not None:
                cells.append(pos)
        return cells

    def _bfs_walkable(
        self, maze: Maze, sr: int, sc: int
    ) -> tuple[int, int] | None:
        rows = len(maze.out)
        cols = len(maze.out[0])
        visited: set[tuple[int, int]] = set()
        queue: list[tuple[int, int]] = [(sr, sc)]
        while queue:
            r, c = queue.pop(0)
            if (r, c) in visited:
                continue
            visited.add((r, c))
            if r % 2 == 1 and c % 2 == 1 and maze.out[r][c] is None:
                if self._has_exit(maze, r, c):
                    return (r, c)
            for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if (nr, nc) not in visited:
                        queue.append((nr, nc))
        return None

    def eat(self, row: int, col: int) -> str | None:
        return self.pacgums.pop((row, col), None)

    def eat_sound(self) -> None:
        self._eat_sounds[self._eat_idx].play()
        self._eat_idx = 1 - self._eat_idx

    @property
    def remaining(self) -> int:
        return len(self.pacgums)

    def update(self, dt: float) -> None:
        self._blink_timer += dt
        if self._blink_timer >= 0.2:
            self._blink_timer = 0.0
            self._blink_visible = not self._blink_visible

    def draw(self, screen: Any, offset_y: int = 0) -> None:

        half = const.TILE_SIZE // 2
        for (r, c), kind in self.pacgums.items():
            cx = c * const.TILE_SIZE + half
            cy = r * const.TILE_SIZE + half + offset_y
            if kind == "super":
                if self._blink_visible:
                    sprite = self._fruit_sprites.get((r, c))
                    if sprite:
                        screen.blit(
                            sprite,
                            (
                                c * const.TILE_SIZE,
                                r * const.TILE_SIZE + offset_y,
                            ),
                        )
                    else:
                        pygame.draw.circle(
                            screen,
                            (255, 255, 255),
                            (cx, cy),
                            8,
                        )
            else:
                pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 3)
