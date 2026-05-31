#!/usr/bin/env python3

from sys import argv
from os import path
from shutil import copy
from src.pac_man.main import pacman


if __name__ == "__main__":
    base_dir = path.dirname(__file__)

    default_config = path.abspath(
        path.join(base_dir, "src", "pac_man", "config.json")
    )

    local_config = path.join(base_dir, "config.json")

    if len(argv) > 2:
        print("Error: Too many arguments")
        print(f"Expected: python3 {path.basename(__file__)} config.json")
        exit(1)

    elif len(argv) == 2:
        pacman(argv[1])

    else:
        if path.exists(local_config):
            pacman(local_config)
        else:
            print("Missing 'config.json', loading defaults...")
            ans = input("Do you want to save defaults to config.json (y/n): ")

            if ans.lower() == "y":
                copy(default_config, local_config)
                pacman(local_config)
            else:
                pacman(default_config)
