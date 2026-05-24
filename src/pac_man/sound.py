import os
from pygame import mixer


class Sound:
    def __init__(self) -> None:
        self._path: str = self._set_path()
        self._sound: mixer.SoundType | None = None

    def _set_path(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../assets/sounds/",
        )

    def load(self, sound_file: str):
        path = os.path.join(self._path, sound_file)
        self._sound = mixer.Sound(path)

    def play(self):
        if self._sound:
            mixer.Sound.play(self._sound)
        else:
            raise FileNotFoundError(f"Missing sound file {self._sound}")
