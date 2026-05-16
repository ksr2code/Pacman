"""
The original Pacman had 28x36 cells (including the walls)
"""

from typing import TYPE_CHECKING
from pygame import SurfaceType
from mazegenerator.mazegenerator import MazeGenerator  # type: ignore[import]
from .sprites import Spritesheet

if TYPE_CHECKING:
    from .config import Config


class Maze:
    """
    Maze render class
    """
    def __init__(self, screen: SurfaceType, conf: "Config") -> None:
        self.screen = screen
        self.maze = MazeGenerator().generate(conf.seed)

    def draw(self) -> None:
        # TODO
        # set up the sprites for the maze
        # do the drawing of the maze
        self.screen.blit(Spritesheet().getImage(0, 0), (0, 0))
