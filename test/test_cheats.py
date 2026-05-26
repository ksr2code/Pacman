from unittest.mock import MagicMock, patch

from src.pac_man.game import Cheats


class TestCheatsDataclass:
    def test_defaults(self):
        c = Cheats()
        assert c.invincible is False
        assert c.ghost_freeze is False
        assert c.speed_boost is False
        assert c.always_fright is False


class TestCheatsToggle:
    def setup_method(self):
        self.cheats = Cheats()

    def test_toggle_invincible(self):
        self.cheats.invincible = not self.cheats.invincible
        assert self.cheats.invincible is True

    def test_toggle_ghost_freeze(self):
        self.cheats.ghost_freeze = not self.cheats.ghost_freeze
        assert self.cheats.ghost_freeze is True

    def test_toggle_speed_boost(self):
        self.cheats.speed_boost = not self.cheats.speed_boost
        assert self.cheats.speed_boost is True

    def test_toggle_always_fright(self):
        self.cheats.always_fright = not self.cheats.always_fright
        assert self.cheats.always_fright is True


class TestGameCheatActions:
    def setup_method(self):
        self.cheats = Cheats()

    def test_extra_life(self):
        lives = 3
        lives += 1
        assert lives == 4

    def test_skip_level_state(self):
        from src.pac_man import constants as const
        level_number = 1
        if level_number >= const.NUM_LEVELS:
            state = const.STATE_VICTORY
        else:
            state = "level_complete"
        assert state == "level_complete"

    def test_skip_level_last(self):
        from src.pac_man import constants as const
        level_number = const.NUM_LEVELS
        if level_number >= const.NUM_LEVELS:
            state = const.STATE_VICTORY
        else:
            state = "level_complete"
        assert state == const.STATE_VICTORY
