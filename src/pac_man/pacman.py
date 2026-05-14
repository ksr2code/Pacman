from .config import Config


def pacman(cfg_file_path):
    cfg = Config()

    if not cfg.read(cfg_file_path):
        exit()

    print(f"{cfg.height=}")
    print(f"{cfg.width=}")
