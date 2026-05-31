import os


class Sound:
    _mixer_ready = False

    def __init__(self, sound_file: str) -> None:
        self._path = self._set_path(sound_file)
        self._sound = None

    def _set_path(self, sound_file: str) -> str:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../assets/sounds",
            sound_file,
        )

    @classmethod
    def init_mixer(cls) -> None:
        if cls._mixer_ready:
            return

        try:
            import pygame

            pygame.mixer.init()
            cls._mixer_ready = True

        except Exception as e:
            print(f"Could not initialize mixer: {e}")

    def _load(self) -> None:
        if self._sound is not None:
            return

        try:
            from pygame import mixer

            self._sound = mixer.Sound(self._path)

        except Exception as e:
            print(f"Could not load sound {self._path}: {e}")

    def play(self) -> None:
        self.init_mixer()

        if not self._mixer_ready:
            return

        self._load()

        if self._sound is not None:
            try:
                self._sound.play()

            except Exception as e:
                print(f"Could not play sound: {e}")
