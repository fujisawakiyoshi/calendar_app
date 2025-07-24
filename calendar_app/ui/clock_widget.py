import tkinter as tk
from datetime import datetime
from ui.theme import COLORS
from services.theme_manager import ThemeManager

class ClockWidget:
    def __init__(self, parent, on_theme_toggle=None):
        self.parent = parent
        self.on_theme_toggle = on_theme_toggle  # ← トグル関数を受け取る

        bg = ThemeManager.get("header_bg")
        fg = ThemeManager.get("clock_fg", "#555")

        self.frame = tk.Frame(parent, bg=bg)
        self.frame.pack(fill="both", expand=True)

        self.label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI", 11),
            bg=bg,
            fg=fg,
            anchor="se",
            padx=8,
            pady=5
        )
        self.label.pack(anchor="se", padx=10, pady=(8, 2))

        # テーマ切り替えラベル（最初から色をテーマに合わせる）
        self.theme_toggle_label = tk.Label(
            self.frame,
            text="✨ かわいいモードへ" if not ThemeManager.is_dark_mode() else "☀ レギュラーモードへ",
            font=("Helvetica", 9),
            bg=bg,
            fg=fg,
            cursor="hand2"
        )
        self.theme_toggle_label.pack(anchor="se", padx=12, pady=(0, 6))
        self.theme_toggle_label.bind("<Button-1>", self._on_toggle_clicked)

        # モード切り替え後の一瞬だけ表示するラベル（最初は非表示）
        new_fg = ThemeManager.get('clock_fg', '#555555')
        self.flash_label = tk.Label(
            self.frame,
            text="かわいくなったよ〜💖",
            font=("Helvetica", 9, "italic"),
            bg=bg,
            fg=new_fg
        )
        self.flash_label.pack(anchor="se", padx=12, pady=(0, 4))
        self.flash_label.pack_forget()  # 最初は非表示
        
        self._update_clock()

    def _update_clock(self):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label.config(text=f"🕒 {now_str}")
        self.label.after(1000, self._update_clock)

    def _on_toggle_clicked(self, event):
        if self.on_theme_toggle:
            self.on_theme_toggle()
            # ラベル更新
            self.theme_toggle_label.config(
                text=self._get_toggle_text(),
                bg=ThemeManager.get('header_bg'),
                fg=ThemeManager.get('clock_fg', '#555555')
            )

            # 一時的な「かわいくなったよ〜」表示
            if ThemeManager.is_dark_mode():
                self._show_flash_message()

    def _get_toggle_text(self):
        return "☀ レギュラーモードへ" if ThemeManager.is_dark_mode() else "✨ かわいいモードへ"

    def update_theme(self):
        new_bg = ThemeManager.get("header_bg")
        new_fg = ThemeManager.get("clock_fg", "#555")

        self.frame.config(bg=new_bg)
        self.label.config(bg=new_bg, fg=new_fg)
        self.theme_toggle_label.config(
            bg=new_bg,
            fg=new_fg,
            text="✨ かわいいモードへ" if not ThemeManager.is_dark_mode() else "☀ レギュラーモードへ"
        )
        self.flash_label.config(bg=new_bg, fg=new_fg)
        
    def _show_flash_message(self):
        self.flash_label.config(
            text="₊✩‧₊かわいくなったよ〜💖₊✩‧₊",
            bg=ThemeManager.get('header_bg'),
            fg=ThemeManager.get('clock_fg', '#555555')
        )
        self.flash_label.pack(anchor="se", padx=12, pady=(0, 4))
        # 4秒後に非表示
        self.frame.after(4000, self.flash_label.pack_forget)