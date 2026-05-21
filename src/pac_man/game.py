import pygame

from . import constants as const
from .config import Config
from .font import Text
from .maze import Maze
from .ghost import Ghost
from .pacgums import Pacgums
from .player import Player


class Game:
    def __init__(self, cfg: Config, screen: pygame.SurfaceType) -> None:
        self.cfg = cfg
        self.screen = screen
        self.score: int = 0
        self.lives: int = cfg.lives
        self.level_number: int = 1
        self.hud_offset = const.HUD_HEIGHT

        self.maze = Maze(screen, cfg)
        self.player = Player(self.maze)
        spawn = self.maze.center
        self.pacgums = Pacgums(self.maze, {spawn})

        ghost_spawn = self._find_ghost_spawn()
        self.ghost = Ghost(
            self.maze, ghost_spawn[0], ghost_spawn[1], const.COLOR_RED
        )
        self._mode_timer: float = 0.0
        self._current_mode: str = "scatter"
        cols = len(self.maze.out[0])
        self.ghost.set_goal(0, cols - 1)

        self._font = Text()
        self._life_icon = pygame.transform.scale(
            self.player.frames["right"][1], (24, 24)
        )

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
        self._update_mode(dt)
        self._update_ghost_goal()
        self.ghost.update(dt)
        self._check_ghost_collision()

    def _check_eating(self) -> None:
        kind = self.pacgums.eat(self.player.grid_row, self.player.grid_col)
        if kind == "pacgum":
            self.score += self.cfg.points_per_pacgum
        elif kind == "super":
            self.score += self.cfg.points_per_super_pacgum

    def _update_mode(self, dt: float) -> None:
        self._mode_timer += dt
        if (self._current_mode == "scatter"
                and self._mode_timer >= const.SCATTER_TIME):
            self._current_mode = "chase"
            self._mode_timer = 0.0
        elif (self._current_mode == "chase"
                and self._mode_timer >= const.CHASE_TIME):
            self._current_mode = "scatter"
            self._mode_timer = 0.0

    def _update_ghost_goal(self) -> None:
        if self._current_mode == "scatter":
            cols = len(self.maze.out[0])
            self.ghost.set_goal(0, cols - 1)
        else:
            self.ghost.set_goal(self.player.grid_row, self.player.grid_col)

    def _check_ghost_collision(self) -> None:
        if (self.ghost.grid_row == self.player.grid_row
                and self.ghost.grid_col == self.player.grid_col):
            print("Ghost caught Pac-Man!")

    def _find_ghost_spawn(self) -> tuple[int, int]:
        rows = len(self.maze.out)
        cols = len(self.maze.out[0])
        for r in range(1, rows // 2 + 1):
            for c in range(1, cols // 2 + 1):
                if (r % 2 == 1 and c % 2 == 1
                        and self.maze.is_walkable(r, c)):
                    return (r, c)
        return (1, 1)

    def draw(self) -> None:
        self.maze.draw(self.hud_offset)
        self.pacgums.draw(self.screen, self.hud_offset)
        self.player.draw(self.screen, self.hud_offset)
        self.ghost.draw(self.screen, self.hud_offset)
        self._draw_hud()

    def _draw_hud(self) -> None:
        screen_w = self.screen.get_width()

        score_surf = self._font.render(f"{self.score}")
        self.screen.blit(score_surf, (8, 8))

        level_surf = self._font.render(f"Lv.{self.level_number}")
        level_x = (screen_w - level_surf.get_width()) // 2
        self.screen.blit(level_surf, (level_x, 8))

        icon_w = self._life_icon.get_width()
        start_x = screen_w - (self.lives * (icon_w + 4)) - 4
        for i in range(self.lives):
            self.screen.blit(
                self._life_icon, (start_x + i * (icon_w + 4), 8)
            )
