import sys
from os import chdir, path
from sys import path as sys_path


def is_frozen() -> bool:
    """True when running from a PyInstaller bundle."""
    return bool(getattr(sys, "frozen", False))


def resolve_configs(base_dir: str, bundle_dir: str) -> tuple[str, str]:
    """Return (local_config, bundled_config) paths.

    bundled_config ships inside the package; local_config is the optional
    user override next to the executable (or next to the script in dev).
    """
    bundled_config = path.abspath(path.join(bundle_dir, "src", "config.json"))
    local_config = path.join(base_dir, "config.json")
    return local_config, bundled_config


if is_frozen():
    # Frozen app: writable files (config override, highscore.json) live
    # next to the executable, not inside the temp-extracted bundle.
    base_dir = path.dirname(path.abspath(sys.executable))
    bundle_dir = path.dirname(path.abspath(__file__))
    chdir(base_dir)
else:
    base_dir = path.dirname(path.abspath(__file__))
    bundle_dir = base_dir
    src_dir = path.join(base_dir, "src")
    if src_dir not in sys_path:
        sys_path.insert(0, src_dir)


if __name__ == "__main__":
    import asyncio

    from src.main import pacman

    if len(sys.argv) == 2:
        asyncio.run(pacman(sys.argv[1]))
    elif is_frozen():
        # Windowed exe has no console: no usage message can be shown.
        # Prefer a user config next to the executable, else bundled defaults.
        local_config, bundled_config = resolve_configs(base_dir, bundle_dir)
        cfg = local_config if path.exists(local_config) else bundled_config
        asyncio.run(pacman(cfg))
    else:
        sys.exit(f"Usage: python3 {path.basename(__file__)} <config.json>")
