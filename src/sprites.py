from __future__ import annotations

import os
import sys

import pygame


class SpriteSheet:
    """Loads a spritesheet PNG and extracts 32x32 cell subsurfaces."""

    DIR_ROW = {
        (-1, 0): 2,
        (1, 0): 3,
        (0, -1): 4,
        (0, 1): 5,
    }

    def __init__(self, filename: str = "pacman.png") -> None:
        """Load and convert the spritesheet PNG."""
        sprite_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"assets/sprites/{filename}",
        )
        try:
            self.sheet: pygame.Surface = pygame.image.load(
                sprite_path,
            ).convert_alpha()
        except Exception as e:
            print(
                f"Warning: missing sprite {sprite_path}: {e}",
                file=sys.stderr,
            )
            self.sheet = pygame.Surface((32, 32))
            self.sheet.fill((255, 0, 255))

    def getImage(self, x: int, y: int) -> pygame.Surface:
        """Extract a 32x32 subsurface at pixel (x, y)."""
        self.sheet.set_clip(pygame.Rect(x, y, 32, 32))
        return self.sheet.subsurface(self.sheet.get_clip()).copy()

    def getImageGrid(self, col: int, row: int) -> pygame.Surface:
        """Extract a 32x32 subsurface at grid (col, row)."""
        return self.sheet.subsurface(
            pygame.Rect(col * 32, row * 32, 32, 32),
        ).copy()

    def ghost_frame(
        self,
        col: int,
        direction: tuple[int, int],
    ) -> pygame.Surface:
        """Extract a ghost sprite for the given animation col and direction."""
        return self.getImageGrid(col, self.DIR_ROW[direction])

    def eyes_frame(self, direction: tuple[int, int]) -> pygame.Surface:
        """Extract the eyes-only sprite for a direction."""
        return self.getImageGrid(4, self.DIR_ROW[direction])

    def freight_blue(self) -> pygame.Surface:
        """Extract the blue frightened-ghost sprite."""
        return self.getImageGrid(5, 2)

    def freight_white(self) -> pygame.Surface:
        """Extract the white flashing frightened-ghost sprite."""
        return self.getImageGrid(5, 3)
