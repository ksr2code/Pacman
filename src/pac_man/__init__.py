from os import path
from .main import pacman


def main():
    base_dir = path.dirname(__file__)
    default_config = path.abspath(path.join(base_dir, "config.json"))
    pacman(default_config)
