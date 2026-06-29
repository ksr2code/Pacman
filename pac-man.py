from os import path
from sys import path as sys_path

src_dir = path.join(path.dirname(path.abspath(__file__)), "src")
if src_dir not in sys_path:
    sys_path.insert(0, src_dir)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit(
            f"Usage: python3 {path.basename(__file__)} <config.json>"
        )

    import asyncio
    from src.main import pacman

    asyncio.run(pacman(sys.argv[1]))
