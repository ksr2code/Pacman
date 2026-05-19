from . import constants as const
from .config import Config
from .game import Game

import pygame
import time


def pacman(cfg_file_path: str) -> None:
    cfg = Config()

    if not cfg.read(cfg_file_path):
        exit()

    pygame.init()

    window_width = (cfg.width * 2 + 1) * const.TILE_SIZE
    window_height = (cfg.height * 2 + 1) * const.TILE_SIZE + const.HUD_HEIGHT
    window = pygame.display.set_mode((window_width, window_height), vsync=1)
    pygame.display.set_caption("Pac-Man")

    game = Game(cfg, window)

    fps = 60
    frame_cap = 1.0 / fps
    last_time = time.perf_counter()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        now = time.perf_counter()
        dt = now - last_time
        last_time = now

        if dt > frame_cap:
            dt = frame_cap
        game.update(dt)

        window.fill((0, 0, 0))
        game.draw()
        pygame.display.flip()

    pygame.quit()
