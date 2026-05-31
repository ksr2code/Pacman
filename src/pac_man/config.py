from __future__ import annotations
import json
from dataclasses import dataclass


_CLAMPS: list[tuple[str, int]] = [
    ("width", 5),
    ("height", 5),
    ("lives", 1),
    ("pacgum", 1),
    ("points_per_pacgum", 1),
    ("points_per_super_pacgum", 1),
    ("points_per_ghost", 1),
    ("level_max_time", 10),
]


def _strip_comments(text: str) -> str:
    return "\n".join(
        line
        for line in text.split("\n")
        if not line.lstrip().startswith(("#", "//"))
    )


@dataclass
class ConfigData:
    highscore_filename: str = "highscore.json"
    width: int = 14
    height: int = 18
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90


class Config:
    def __init__(self) -> None:
        self.data: ConfigData | None = None

    def _clamp_values(self, data: ConfigData) -> ConfigData:
        for name, minimum in _CLAMPS:
            value = getattr(data, name)
            if value < minimum:
                print(f"Warning: clamping {name} from {value} to {minimum}")
                setattr(data, name, minimum)
        return data

    def read(self, file: str) -> bool:
        """Load and validate config file. Returns True on success."""
        try:
            with open(file) as fp:
                raw = fp.read()

            parsed = json.loads(_strip_comments(raw))

            # only accept known fields (equivalent to extra="ignore")
            allowed = ConfigData().__dict__.keys()
            filtered = {k: v for k, v in parsed.items() if k in allowed}

            data = ConfigData(**filtered)
            data = self._clamp_values(data)

            self.data = data
            return True

        except FileNotFoundError:
            print(f"Error: Config file '{file}' not found")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{file}': {e}")
            return False
        except Exception as e:
            print(f"Error: Invalid config - {e}")
            return False

    # ---------- property passthroughs ----------

    @property
    def width(self) -> int:
        return self.data.width  # type: ignore[union-attr]

    @property
    def height(self) -> int:
        return self.data.height  # type: ignore[union-attr]

    @property
    def seed(self) -> int:
        return self.data.seed  # type: ignore[union-attr]

    @property
    def lives(self) -> int:
        return self.data.lives  # type: ignore[union-attr]

    @property
    def highscore_filename(self) -> str:
        return self.data.highscore_filename  # type: ignore[union-attr]

    @property
    def pacgum(self) -> int:
        return self.data.pacgum  # type: ignore[union-attr]

    @property
    def points_per_pacgum(self) -> int:
        return self.data.points_per_pacgum  # type: ignore[union-attr]

    @property
    def points_per_super_pacgum(self) -> int:
        return self.data.points_per_super_pacgum  # type: ignore[union-attr]

    @property
    def points_per_ghost(self) -> int:
        return self.data.points_per_ghost  # type: ignore[union-attr]

    @property
    def level_max_time(self) -> int:
        return self.data.level_max_time  # type: ignore[union-attr]
