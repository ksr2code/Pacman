import os
from pygame import font, Surface


class Text:
    """Text renderer wrapping a pygame Font with the PressStart2P font."""

    def __init__(
        self,
        size: int = 32,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """Initialize with given size and color."""
        self.size = size
        self.path: str = self._resolve_path()
        self.color = color
        self.font = font.Font(self.path, self.size)

    def _resolve_path(self) -> str:
        """Return the PressStart2P font path."""
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets/fonts/PressStart2P-Regular.ttf",
        )

    def render(
        self, txt: str, color: tuple[int, int, int] | None = None,
    ) -> Surface:
        """Render text as a non-antialiased pygame Surface."""
        return self.font.render(txt, False, color or self.color)
