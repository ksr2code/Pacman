"""
---
requires-python = ">=3.12"
dependencies = [
    "pygame-ce",
    "mazegenerator",
]
---
"""

import time
import asyncio
from typing import Any
import pygame

import constants as const
from config import Config
from font import Text
from game import Game
from highscore import Highscore
from sound import Sound
from screens import (
    CheatMenuScreen,
    GameOverScreen,
    HighscoresScreen,
    InstructionsScreen,
    NameEntryScreen,
    PauseScreen,
    Screen,
    TitleScreen,
    VictoryScreen,
    WaitingScreen,
)

STATE_LEVEL_COMPLETE = "level_complete"
STATE_DYING = "dying"


class App:
    def __init__(self, cfg: Config, screen: Any) -> None:
        self.cfg = cfg
        self.screen = screen

        self.font = Text()
        self.small_font = Text()
        self.small_font.size = 16
        self.small_font.font = pygame.font.Font(self.small_font.path, 16)

        self.sound: Sound = Sound("start.ogg")

        self.highscore = Highscore(cfg.highscore_filename)
        self.highscore.load()

        self.game: Game = None  # type: ignore
        self._screen: Screen = None  # type: ignore
        self._state: str = const.STATE_TITLE

        self._transition(const.STATE_TITLE)

    def _transition(self, new_state: str) -> None:
        if new_state == const.STATE_TITLE:
            self._screen = TitleScreen(
                self.screen,
                self.font,
                self.small_font,
                self.highscore,
            )
            self.sound.play()

        elif new_state == const.STATE_WAITING:
            if self.game is None:
                self.game = Game(self.cfg, self.screen)

            self._screen = WaitingScreen(
                self.screen,
                self.font,
                self.game,
            )

        elif new_state == const.STATE_PLAYING:
            self.game.state = const.STATE_PLAYING
            self._screen = _GameScreen(self.game)

        elif new_state == const.STATE_PAUSE:
            self._screen = PauseScreen(
                self.screen,
                self.small_font,
                self.game,
                self.cfg,
            )

        elif new_state == const.STATE_CHEAT_MENU:
            self._screen = CheatMenuScreen(
                self.screen,
                self.font,
                self.small_font,
                self.game,
            )

        elif new_state == const.STATE_GAME_OVER:
            self._screen = GameOverScreen(
                self.screen,
                self.font,
                self.game,
            )

        elif new_state == const.STATE_VICTORY:
            self._screen = VictoryScreen(
                self.screen,
                self.font,
                self.game,
            )

        elif new_state == const.STATE_NAME_ENTRY:
            self._screen = NameEntryScreen(
                self.screen,
                self.font,
                self.small_font,
                self.highscore,
                self.game.score,
            )

        elif new_state == const.STATE_HIGHSCORES:
            self._screen = HighscoresScreen(
                self.screen,
                self.small_font,
                self.highscore,
            )

        elif new_state == const.STATE_INSTRUCTIONS:
            self._screen = InstructionsScreen(
                self.screen,
                self.small_font,
            )

        self._state = new_state

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if self._state == const.STATE_PLAYING:
            self.game.handle_event(event)
            self._check_game_state()

        elif self._state in (STATE_LEVEL_COMPLETE, STATE_DYING):
            pass

        elif self._state == const.STATE_CHEAT_MENU:
            result = self._screen.handle_event(event)
            if result is not None:
                self._transition(result)
            self._check_game_state()

        else:
            result = self._screen.handle_event(event)

            if result == const.STATE_WAITING:
                self.game = Game(self.cfg, self.screen)
                self._transition(const.STATE_WAITING)

            elif result is not None:
                self._transition(result)

    def update(self, dt: float) -> None:
        if self._state == const.STATE_PLAYING:
            self.game.update(dt)
            self._check_game_state()

        elif self._state in (STATE_LEVEL_COMPLETE, STATE_DYING):
            self.game.update(dt)
            self._check_game_state()

        elif self._state == const.STATE_CHEAT_MENU:
            self._check_game_state()

        else:
            result = self._screen.update(dt)
            if result is not None:
                self._transition(result)

    def _check_game_state(self) -> None:
        s = self.game.state

        if s == const.STATE_PAUSE:
            self._transition(const.STATE_PAUSE)

        elif s == const.STATE_CHEAT_MENU:
            self._transition(const.STATE_CHEAT_MENU)

        elif s == const.STATE_GAME_OVER:
            self._transition(const.STATE_GAME_OVER)

        elif s == const.STATE_VICTORY:
            self._transition(const.STATE_VICTORY)

        elif s == STATE_LEVEL_COMPLETE:
            if self._state != STATE_LEVEL_COMPLETE:
                self._state = STATE_LEVEL_COMPLETE

        elif s == STATE_DYING:
            if self._state != STATE_DYING:
                self._state = STATE_DYING

        elif s == const.STATE_PLAYING:
            if self._state in (STATE_LEVEL_COMPLETE, STATE_DYING):
                self._transition(const.STATE_PLAYING)

    def draw(self) -> None:
        self._screen.draw()


class _GameScreen(Screen):
    def __init__(self, game: Game) -> None:
        self.game = game

    def handle_event(self, event: pygame.event.Event) -> str | None:
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self) -> None:
        self.game.draw()


# ---------------------------
# pygbag ENTRY POINT
# ---------------------------


async def pacman(cfg_file_path: str) -> None:
    cfg = Config()

    if not cfg.read(cfg_file_path):
        raise SystemExit("Config not found or invalid")

    pygame.init()

    w = (cfg.width * 2 + 1) * const.TILE_SIZE
    h = (cfg.height * 2 + 1) * const.TILE_SIZE + const.HUD_HEIGHT

    screen = pygame.display.set_mode((w, h), vsync=1)
    pygame.display.set_caption("Pac-Man")

    app = App(cfg, screen)

    fps = 60
    cap = 1.0 / fps
    last = time.perf_counter()

    while True:
        for event in pygame.event.get():
            app.handle_event(event)

        now = time.perf_counter()
        dt = min(now - last, cap)
        last = now

        app.update(dt)

        screen.fill((0, 0, 0))
        app.draw()
        pygame.display.flip()

        # 🔴 CRITICAL for pygbag responsiveness
        await asyncio.sleep(0)


# ---------------------------
# pygbag-safe main
# ---------------------------


async def main():
    from os import path

    def_config = path.join(path.dirname(path.abspath(__file__)), "config.json")
    await pacman(def_config)


if __name__ == "__main__":
    asyncio.run(main())
