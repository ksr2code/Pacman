import os
import sys

from pygame import mixer


class Sound:
    def __init__(self, sound_file: str) -> None:
        self._path: str = self._set_path(sound_file)
        self._sound: mixer.Sound | None
        try:
            self._sound = mixer.Sound(self._path)
        except FileNotFoundError:
            print(
                f"Warning: missing sound file {self._path}",
                file=sys.stderr,
            )
            self._sound = None

    def _set_path(self, sound_file: str) -> str:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"assets/sounds/{sound_file}",
        )

    def play(self, loops: int = 0) -> None:
        if self._sound is not None:
            mixer.Sound.play(self._sound, loops=loops)

    def stop(self) -> None:
        if self._sound is not None:
            mixer.Sound.stop(self._sound)
