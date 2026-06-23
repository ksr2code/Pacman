from __future__ import annotations

import json
import sys
from dataclasses import dataclass, fields
from typing import Any, get_type_hints


_CLAMPS: list[tuple[str, int]] = [
    ("width", 5),
    ("height", 5),
    ("lives", 1),
    ("pacgum", 0),
    ("points_per_pacgum", 1),
    ("points_per_super_pacgum", 1),
    ("points_per_ghost", 1),
    ("level_max_time", 10),
]


def _warn(msg: str) -> None:
    """Emit a config warning to stderr (visible in pygbag browser console)."""
    print(f"Warning: {msg}", file=sys.stderr)


def _strip_comments(text: str) -> str:
    """Drop full-line comments starting with # or //."""
    kept: list[str] = []
    for ln in text.splitlines():
        if not ln.lstrip().startswith(("#", "//")):
            kept.append(ln)
    return "\n".join(kept)


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
    cheat: bool = False


# Resolved once at module load.
_FIELD_NAMES = {f.name for f in fields(ConfigData)}
_TYPES = get_type_hints(ConfigData)
_CLAMPS_MAP = dict(_CLAMPS)


def _is_valid_type(value: Any, expected: Any) -> bool:
    """True if value matches expected.

    Rejects bool for int fields: bool is an int subclass in Python, so a
    naive isinstance check would silently accept `width: true` as `1`.
    """
    if expected is int:
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, expected)


def _sanitize(parsed: dict[str, Any]) -> dict[str, Any]:
    """Filter unknown keys, drop mistyped values, clamp numerics.

    Returns a dict safe to pass to ConfigData(**...). Unknown or invalid
    keys fall back to dataclass defaults; clamps enforce safe minimums.
    """
    clean: dict[str, Any] = {}
    for key, value in parsed.items():
        if key not in _FIELD_NAMES:
            _warn(f"unknown config key '{key}' ignored")
            continue
        expected = _TYPES.get(key)
        if expected is None or not _is_valid_type(value, expected):
            _warn(
                f"invalid type for '{key}' "
                f"(expected {getattr(expected, '__name__', expected)}); "
                f"using default"
            )
            continue
        minimum = _CLAMPS_MAP.get(key)
        if minimum is not None and isinstance(value, int) and value < minimum:
            _warn(f"'{key}'={value} below minimum {minimum}; clamped")
            value = minimum
        clean[key] = value
    return clean


class Config:
    def __init__(self) -> None:
        self.data: ConfigData

    def read(self, file: str) -> bool:
        """Load and validate config file. Returns True on success.

        On missing/invalid values, clamps to safe defaults and logs to stderr.
        Unknown keys are ignored. Never raises on user content.
        """
        try:
            with open(file) as fp:
                raw = fp.read()
            parsed = json.loads(_strip_comments(raw))
            if not isinstance(parsed, dict):
                _warn("config root must be a JSON object; using defaults")
                self.data = ConfigData()
                return True
            self.data = ConfigData(**_sanitize(parsed))
            return True
        except FileNotFoundError:
            print(f"Error: Config file '{file}' not found", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{file}': {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Error: Invalid config - {e}", file=sys.stderr)
            return False

    @property
    def width(self) -> int:
        return self.data.width

    @property
    def height(self) -> int:
        return self.data.height

    @property
    def seed(self) -> int:
        return self.data.seed

    @property
    def lives(self) -> int:
        return self.data.lives

    @property
    def highscore_filename(self) -> str:
        return self.data.highscore_filename

    @property
    def pacgum(self) -> int:
        return self.data.pacgum

    @property
    def points_per_pacgum(self) -> int:
        return self.data.points_per_pacgum

    @property
    def points_per_super_pacgum(self) -> int:
        return self.data.points_per_super_pacgum

    @property
    def points_per_ghost(self) -> int:
        return self.data.points_per_ghost

    @property
    def level_max_time(self) -> int:
        return self.data.level_max_time

    @property
    def cheat(self) -> bool:
        return self.data.cheat
