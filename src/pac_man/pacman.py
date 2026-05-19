from .config import Config
from .maze import Maze
from .player import Player

import pygame
import time


def pacman(cfg_file_path: str) -> None:
    cfg = Config()

    if not cfg.read(cfg_file_path):
        exit()

    pygame.init()

    TILE_SIZE = 32
    window_width = (cfg.width * 2 + 1) * TILE_SIZE
    window_height = (cfg.height * 2 + 1) * TILE_SIZE
    window = pygame.display.set_mode((window_width, window_height), vsync=1)
    pygame.display.set_caption("Pac-Man")

    maze = Maze(window, cfg)
    player = Player(maze)

    fps = 60
    frame_cap = 1.0 / fps
    last_time = time.perf_counter()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_map = {
                    pygame.K_UP: "up", pygame.K_w: "up",
                    pygame.K_DOWN: "down", pygame.K_s: "down",
                    pygame.K_LEFT: "left", pygame.K_a: "left",
                    pygame.K_RIGHT: "right", pygame.K_d: "right",
                }
                direction = key_map.get(event.key)
                if direction:
                    player.set_direction(direction)

        now = time.perf_counter()
        dt = now - last_time
        last_time = now

        if dt > frame_cap:
            dt = frame_cap
        player.update(dt)

        window.fill((0, 0, 0))
        maze.draw()
        player.draw(window)
        pygame.display.flip()

    pygame.quit()
