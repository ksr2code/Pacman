import os


class Text:
    def __init__(self) -> None:
        from pygame import font

        self.size: int = 32
        self.path: str | None = self.set_path()
        self.color: tuple[int, int, int] = (255, 255, 255)
        self.font = font.Font(self.path, self.size)

    def set_path(self, path: str | None = None) -> str | None:
        if path is None:
            path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../assets/fonts/PressStart2P-Regular.ttf",
            )
        self.path = path
        return self.path

    def render(self, txt: str):
        return self.font.render(txt, False, self.color)
