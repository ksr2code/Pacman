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
        self.state: str = const.STATE_PLAYING
        self._invincible_timer: float = 0.0
        self._pause_timer: float = 0.0
        self._freight_timer: float = 0.0
        self._ghost_points: int = 200

        self.maze = Maze(screen, cfg)
        self.player = Player(self.maze)
        spawn = self.maze.center
        self._player_spawn: tuple[int, int] = self.maze.center
        self.pacgums = Pacgums(self.maze, {spawn})

        ghost_spawn = self._find_ghost_spawn()
        self._ghost_spawn: tuple[int, int] = ghost_spawn
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
        if (self.state == const.STATE_GAME_OVER
                and event.type == pygame.KEYDOWN):
            self._restart_game()
            return
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
        if self.state != const.STATE_PLAYING:
            return
        if self._pause_timer > 0:
            self._pause_timer = max(0.0, self._pause_timer - dt)
            return
        self._invincible_timer = max(0.0, self._invincible_timer - dt)
        if self._freight_timer > 0:
            self._freight_timer = max(0.0, self._freight_timer - dt)
            if self._freight_timer <= 0:
                self._end_freight()
        self.player.update(dt)
        self.pacgums.update(dt)
        self._check_eating()
        self._update_mode(dt)
        self._update_ghost_goal()
        self.ghost.update(dt)
        if (self.ghost.mode == "spawn"
                and self.ghost.direction is None):
            self.ghost.go_idle()
        self._check_ghost_collision()

    def _check_eating(self) -> None:
        kind = self.pacgums.eat(
            self.player.grid_row, self.player.grid_col
        )
        if kind == "pacgum":
            self.score += self.cfg.points_per_pacgum
        elif kind == "super":
            self.score += self.cfg.points_per_super_pacgum
            self._start_freight()

    def _start_freight(self) -> None:
        self._freight_timer = const.FREIGHT_TIME
        self._ghost_points = 200
        self.ghost.start_freight()

    def _end_freight(self) -> None:
        if (self.ghost.mode != "scatter"
                and self.ghost.mode != "chase"):
            self.ghost.go_normal(self._current_mode)

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
        if self._invincible_timer > 0:
            return
        if not (self.ghost.grid_row == self.player.grid_row
                and self.ghost.grid_col == self.player.grid_col):
            return
        if self.ghost.mode == "freight":
            self.score += self._ghost_points
            self._ghost_points *= 2
            self.ghost.start_spawn()
        elif self.ghost.mode in ("scatter", "chase"):
            self.lives -= 1
            if self.lives <= 0:
                self.state = const.STATE_GAME_OVER
            else:
                self._reset_positions()
                self._pause_timer = 1.0
                self._invincible_timer = const.INVINCIBLE_TIME

    def _reset_positions(self) -> None:
        self.player.reset(*self._player_spawn)
        ghost_spawn = self._ghost_spawn
        self.ghost.reset(ghost_spawn[0], ghost_spawn[1])
        self._mode_timer = 0.0
        self._current_mode = "scatter"
        self._freight_timer = 0.0
        cols = len(self.maze.out[0])
        self.ghost.set_goal(0, cols - 1)

    def _restart_game(self) -> None:
        self.score = 0
        self.lives = self.cfg.lives
        self.level_number = 1
        self.state = const.STATE_PLAYING
        self._invincible_timer = 0.0
        self._freight_timer = 0.0
        self._ghost_points = 200
        spawn = self._player_spawn
        self.player.reset(spawn[0], spawn[1])
        gs = self._ghost_spawn
        self.ghost.reset(gs[0], gs[1])
        self._mode_timer = 0.0
        self._current_mode = "scatter"
        self.ghost.set_goal(0, len(self.maze.out[0]) - 1)
        self.pacgums = Pacgums(self.maze, {spawn})

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
        if self.state == const.STATE_GAME_OVER:
            screen_w = self.screen.get_width()
            screen_h = self.screen.get_height()
            go_surf = self._font.render("GAME OVER")
            x = (screen_w - go_surf.get_width()) // 2
            y = (screen_h - go_surf.get_height()) // 2
            self.screen.blit(go_surf, (x, y))

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
