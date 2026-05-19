import pygame

from .config import Config
from .font import Text
from .maze import Maze
from .pacgums import Pacgums
from .player import Player


class Game:
    def __init__(self, cfg: Config, screen: pygame.SurfaceType) -> None:
        self.cfg = cfg
        self.screen = screen
        self.score: int = 0
        self.lives: int = cfg.lives
        self.level_number: int = 1

        self.maze = Maze(screen, cfg)
        self.player = Player(self.maze)
        spawn = self.maze.center
        self.pacgums = Pacgums(self.maze, {spawn})

        self._font = Text()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        key_map = {
            pygame.K_UP: "up", pygame.K_w: "up",
            pygame.K_DOWN: "down", pygame.K_s: "down",
            pygame.K_LEFT: "left", pygame.K_a: "left",
            pygame.K_RIGHT: "right", pygame.K_d: "right",
        }
        direction = key_map.get(event.key)
        if direction:
            self.player.set_direction(direction)

    def update(self, dt: float) -> None:
        self.player.update(dt)
        self.pacgums.update(dt)
        self._check_eating()

    def _check_eating(self) -> None:
        kind = self.pacgums.eat(self.player.grid_row, self.player.grid_col)
        if kind == "pacgum":
            self.score += self.cfg.points_per_pacgum
        elif kind == "super":
            self.score += self.cfg.points_per_super_pacgum

    def draw(self) -> None:
        self.maze.draw()
        self.pacgums.draw(self.screen)
        self.player.draw(self.screen)
        self._draw_hud()

    def _draw_hud(self) -> None:
        score_surf = self._font.render(f"Score: {self.score}")
        level_surf = self._font.render(f"Level: {self.level_number}")
        lives_surf = self._font.render(f"Lives: {self.lives}")
        self.screen.blit(score_surf, (10, 4))
        screen_w = self.screen.get_width()
        level_x = (screen_w - level_surf.get_width()) // 2
        self.screen.blit(level_surf, (level_x, 4))
        self.screen.blit(
            lives_surf, (screen_w - lives_surf.get_width() - 10, 4)
        )
