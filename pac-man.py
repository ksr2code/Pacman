from os import path
from sys import path as sys_path

src_dir = path.join(path.dirname(path.abspath(__file__)), "src")
if src_dir not in sys_path:
    sys_path.insert(0, src_dir)


if __name__ == "__main__":
    import asyncio
    from src.main import pacman
    from sys import argv
    from shutil import copy

    base_dir = path.dirname(__file__)

    default_config = path.abspath(
        path.join(base_dir, "src", "config.json")
    )

    local_config = path.join(base_dir, "config.json")

    if len(argv) > 2:
        print("Error: Too many arguments")
        print(f"Expected: python3 {path.basename(__file__)} config.json")
        exit(1)

    elif len(argv) == 2:
        asyncio.run(pacman(argv[1]))

    else:
        if path.exists(local_config):
            asyncio.run(pacman(local_config))
        else:
            print("Missing 'config.json', loading defaults...")
            ans = input("Do you want to save defaults to config.json (y/n): ")

            if ans.lower() == "y":
                copy(default_config, local_config)
                asyncio.run(pacman(local_config))
            else:
                asyncio.run(pacman(default_config))
