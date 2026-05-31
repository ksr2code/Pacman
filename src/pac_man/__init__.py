from os import path
from .main import pacman
import asyncio


async def main_async():
    """Async entry point for pygbag"""
    await asyncio.sleep(0)
    base_dir = path.dirname(__file__)
    default_config = path.abspath(path.join(base_dir, "config.json"))
    await pacman(default_config)


def main():
    """Sync entry point for script execution"""
    asyncio.run(main_async())
