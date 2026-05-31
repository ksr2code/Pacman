import os
from pygame import mixer


class Sound:
    def __init__(self, sound_file: str) -> None:
        self._path: str = self._set_path(sound_file)
        self._sound: mixer.SoundType = mixer.Sound(self._path)

    def _set_path(self, sound_file: str) -> str:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"../assets/sounds/{sound_file}",
        )

    def play(self, loops: int = 0) -> None:
        if self._sound:
            mixer.Sound.play(self._sound, loops=loops)
        else:
            raise FileNotFoundError(
                f"Missing sound file {self._path}"
            )

    def stop(self) -> None:
        if self._sound:
            mixer.Sound.stop(self._sound)
