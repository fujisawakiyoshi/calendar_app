from ui.theme import LIGHT_THEME, DARK_THEME

class ThemeManager:
    """
    アプリ全体のテーマ状態（ライトテーマ／ダークテーマ）を管理するクラス。
    どのコンポーネントからでも現在のテーマにアクセスできるようにする。
    """

    _theme = LIGHT_THEME       # 現在使用中のテーマ（デフォルト: ライト）
    _is_dark = False           # 現在ダークモードかどうかのフラグ

    @classmethod
    def use_dark_mode(cls):
        """
        テーマをダークモードに切り替える。
        """
        cls._theme = DARK_THEME
        cls._is_dark = True

    @classmethod
    def use_light_mode(cls):
        """
        テーマをライトモードに切り替える。
        """
        cls._theme = LIGHT_THEME
        cls._is_dark = False

    @classmethod
    def toggle_theme(cls):
        """
        テーマを現在の状態に応じて切り替える（ライト↔ダーク）。
        """
        if cls._is_dark:
            cls.use_light_mode()
        else:
            cls.use_dark_mode()

    @classmethod
    def get(cls, key: str, fallback=None):
        """
        現在のテーマから色などの値を取得する。

        Args:
            key (str): 取得したい項目名（例: 'bg', 'text'）
            fallback (Any): 見つからなかった場合の代替値

        Returns:
            Any: テーマから取得した値
        """
        return cls._theme.get(key, fallback)

    @classmethod
    def is_dark_mode(cls) -> bool:
        """
        現在のモードがダークかどうかを返す。

        Returns:
            bool: True = ダークモード, False = ライトモード
        """
        return cls._is_dark
