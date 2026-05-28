import pygame
import os


class Spritesheet(object):
    def __init__(self, filename: str = "pacman.png"):

        sprite_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"../../assets/sprites/{filename}",
        )
        self.sheet = pygame.image.load(sprite_path).convert()

    def getImage(self, x: int, y: int) -> pygame.SurfaceType:
        self.sheet.set_clip(pygame.Rect(x, y, 32, 32))
        # Copy the subsurface instead of returning a view
        return self.sheet.subsurface(self.sheet.get_clip()).copy()


class GhostSpritesheet:
    DIR_ROW = {
        (-1, 0): 2,
        (1, 0): 3,
        (0, -1): 4,
        (0, 1): 5,
    }

    def __init__(self) -> None:
        sprite_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../assets/sprites/spritesheet_nopink.png",
        )
        raw = pygame.image.load(sprite_path).convert_alpha()
        self.sheet: pygame.SurfaceType = raw

    def _get(self, col: int, row: int) -> pygame.SurfaceType:
        x, y = col * 32, row * 32
        return self.sheet.subsurface(
            pygame.Rect(x, y, 32, 32)
        ).copy()

    def ghost_frame(
        self, col: int, direction: tuple[int, int]
    ) -> pygame.SurfaceType:
        return self._get(col, self.DIR_ROW[direction])

    def eyes_frame(
        self, direction: tuple[int, int]
    ) -> pygame.SurfaceType:
        return self._get(4, self.DIR_ROW[direction])

    def freight_blue(self) -> pygame.SurfaceType:
        return self._get(5, 2)

    def freight_white(self) -> pygame.SurfaceType:
        return self._get(5, 3)
