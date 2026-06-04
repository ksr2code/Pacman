from src.main import pacman
from os import path
from sys import argv
import asyncio

if __name__ == "__main__":
    default_config = path.join(path.dirname(path.abspath(__file__)), "src/config.json")
    asyncio.run(pacman(default_config))
