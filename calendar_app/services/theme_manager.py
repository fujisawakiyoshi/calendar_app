# ui/theme_manager.py

from ui.theme import LIGHT_THEME, DARK_THEME

class ThemeManager:
    _current_theme = LIGHT_THEME

    @classmethod
    def use_dark_mode(cls):
        cls._current_theme = DARK_THEME

    @classmethod
    def use_light_mode(cls):
        cls._current_theme = LIGHT_THEME

    @classmethod
    def get(cls, key):
        return cls._current_theme.get(key, "#000000")  # デフォルト黒
