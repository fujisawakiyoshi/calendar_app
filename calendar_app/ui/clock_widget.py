import tkinter as tk
from datetime import datetime
from ui.theme import COLORS
from services.theme_manager import ThemeManager

class ClockWidget:
    """
    右下に現在時刻を表示するウィジェット。

    ・親ウィジェットにフィットするフレームを作成
    ・1秒ごとに時刻を更新
    """
    def __init__(self, parent):
            self.parent = parent

            self.frame = tk.Frame(parent, bg=ThemeManager.get('header_bg'))
            self.frame.pack(fill="both", expand=True)

            self.label = tk.Label(
                self.frame,
                text="",
                font=("Segoe UI", 11),
                bg=ThemeManager.get('header_bg'),
                fg="#555555",
                anchor="se",
                padx=8,
                pady=5
            )
            self.label.pack(anchor="se", padx=10, pady=8)

            self._update_clock()

    def _update_clock(self):
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.label.config(text=f"🕒 {now_str}")
            self.label.after(1000, self._update_clock)

    def update_theme(self):
        """
        テーマ切り替え時に呼び出し、背景・文字色を更新する。
        """
        new_bg = ThemeManager.get('header_bg')
        new_fg = ThemeManager.get('clock_fg', fallback="#555555")  # フォント色もテーマ化
        self.frame.config(bg=new_bg)
        self.label.config(bg=new_bg, fg=new_fg)