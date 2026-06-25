import os
import sys

from pygame import mixer


class Sound:
    """Sound wrapper; silently degrades if the file is missing."""

    def __init__(self, sound_file: str) -> None:
        """Load the sound file; fall back to None if missing."""
        self._path: str = self._set_path(sound_file)
        self._sound: mixer.Sound | None
        try:
            self._sound = mixer.Sound(self._path)
        except Exception:
            print(
                f"Warning: missing sound file {self._path}",
                file=sys.stderr,
            )
            self._sound = None

    def _set_path(self, sound_file: str) -> str:
        """Resolve the sound file path under assets/sounds/."""
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"assets/sounds/{sound_file}",
        )

    def play(self, loops: int = 0) -> None:
        """Play the sound; silent no-op if the file was missing."""
        if self._sound is not None:
            mixer.Sound.play(self._sound, loops=loops)

    def stop(self) -> None:
        """Stop the sound; silent no-op if the file was missing."""
        if self._sound is not None:
            mixer.Sound.stop(self._sound)
