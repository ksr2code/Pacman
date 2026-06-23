import os
from pygame import font, Surface


class Text:
    """Text renderer wrapping a pygame Font with the PressStart2P font."""

    def __init__(self) -> None:
        """Initialize with default size 32 and white color."""
        self.size: int = 32
        self.path: str | None = self.set_path()
        self.color: tuple[int, int, int] = (255, 255, 255)
        self.font = font.Font(self.path, self.size)

    def set_path(self, path: str | None = None) -> str | None:
        """Set and return the font path, defaulting to PressStart2P."""
        if path is None:
            path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "assets/fonts/PressStart2P-Regular.ttf",
            )
        self.path = path
        return self.path

    def render(self, txt: str) -> Surface:
        """Render text as a non-antialiased pygame Surface."""
        return self.font.render(txt, False, self.color)
