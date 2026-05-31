from __future__ import annotations

import os
from typing import Any


class SpriteSheet:
    DIR_ROW = {
        (-1, 0): 2,
        (1, 0): 3,
        (0, -1): 4,
        (0, 1): 5,
    }

    def __init__(self, filename: str = "pacman.png") -> None:
        import pygame

        sprite_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"../assets/sprites/{filename}",
        )
        self.sheet: Any = pygame.image.load(sprite_path).convert_alpha()

    def getImage(self, x: int, y: int):
        import pygame

        self.sheet.set_clip(pygame.Rect(x, y, 32, 32))
        return self.sheet.subsurface(self.sheet.get_clip()).copy()

    def getImageGrid(self, col: int, row: int):
        import pygame

        return self.sheet.subsurface(
            pygame.Rect(col * 32, row * 32, 32, 32)
        ).copy()

    def ghost_frame(
        self,
        col: int,
        direction: tuple[int, int],
    ):
        return self.getImageGrid(col, self.DIR_ROW[direction])

    def eyes_frame(self, direction: tuple[int, int]):
        return self.getImageGrid(4, self.DIR_ROW[direction])

    def freight_blue(self):
        return self.getImageGrid(5, 2)

    def freight_white(self):
        return self.getImageGrid(5, 3)
