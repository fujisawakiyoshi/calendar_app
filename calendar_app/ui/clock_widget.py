import tkinter as tk
from datetime import datetime
from ui.theme import COLORS
from services.theme_manager import ThemeManager

class ClockWidget:
    def __init__(self, parent, on_theme_toggle=None):
        self.parent = parent
        self.on_theme_toggle = on_theme_toggle  # ← トグル関数を受け取る

        self.frame = tk.Frame(parent, bg=ThemeManager.get('header_bg'))
        self.frame.pack(fill="both", expand=True)

        self.label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI", 11),
            bg=ThemeManager.get('header_bg'),
            fg=ThemeManager.get('clock_fg', '#555555'),
            anchor="se",
            padx=8,
            pady=5
        )
        self.label.pack(anchor="se", padx=10, pady=0)

        # ▼ 小さな「テーマ切り替え」ボタン（イースターエッグ風）
        self.toggle_label = tk.Label(
            self.frame,
            text=self._get_toggle_text(),
            font=("Helvetica", 9),
            fg="#8888aa",
            bg=ThemeManager.get('header_bg'),
            cursor="hand2"
        )
        self.toggle_label.pack(anchor="se", padx=10, pady=(0, 8))
        self.toggle_label.bind("<Button-1>", self._on_toggle_clicked)

        self._update_clock()

    def _update_clock(self):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label.config(text=f"🕒 {now_str}")
        self.label.after(1000, self._update_clock)

    def _on_toggle_clicked(self, event):
        if self.on_theme_toggle:
            self.on_theme_toggle()  # メイン側の toggle_theme を呼び出す
            # テキストを更新
            self.toggle_label.config(
                text=self._get_toggle_text(),
                bg=ThemeManager.get('header_bg'),
                fg=ThemeManager.get('clock_fg', '#555555')
            )

    def _get_toggle_text(self):
        return "☀ レギュラーモードへ" if ThemeManager.is_dark_mode() else "✨ かわいいモードへ"

    def update_theme(self):
        new_bg = ThemeManager.get('header_bg')
        new_fg = ThemeManager.get('clock_fg', "#555555")
        self.frame.config(bg=new_bg)
        self.label.config(bg=new_bg, fg=new_fg)
        self.toggle_label.config(
            bg=new_bg,
            fg=ThemeManager.get('clock_fg', "#555555"),
            text=self._get_toggle_text()
        )
