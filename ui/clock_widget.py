import tkinter as tk
from datetime import datetime
from ui.theme import COLORS
from services.theme_manager import ThemeManager

class ClockWidget:
    def __init__(self, root, parent, on_theme_toggle=None):
        self.root = root 
        self.parent = parent
        self.on_theme_toggle = on_theme_toggle

        bg = ThemeManager.get('header_bg')
        fg = ThemeManager.get('clock_fg', "#555")

        self.frame = tk.Frame(parent, bg=bg)
        self.frame.pack(fill="both", expand=True)

        # 「かわいくなったよ〜💖」一時表示ラベル（最初は非表示）
        self.flash_label = tk.Label(
            self.parent,  # ← self.frame ではなく self.parent に配置
            text="₊✩‧₊かわいくなったよ〜💖₊✩‧₊",
            font=("Helvetica", 9, "italic"),
            bg=bg,
            fg=fg
        )
        self.flash_label.place_forget()

        # 時計ボタン（ラベル風）
        self.clock_btn = tk.Button(
            self.frame,
            text="",  # 後でセット
            font=("Segoe UI", 11),
            bg=bg,
            fg=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=bg,
            activeforeground=fg,
            command=self._on_toggle_clicked  # クリック時の動作
        )
        self.clock_btn.pack(fill="both", expand=True)

        self.clock_btn.bind("<Enter>", lambda e: self.clock_btn.config(fg="#AA77AA"))
        self.clock_btn.bind("<Leave>", lambda e: self.update_theme())

        self._update_clock()

    def _update_clock(self):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_btn.config(text=f"\U0001F552 {now_str}")
        self.clock_btn.after(1000, self._update_clock)

    def _on_toggle_clicked(self):
        if self.on_theme_toggle:
            self.on_theme_toggle()
            if ThemeManager.is_dark_mode():
                self._show_flash_message()
            # メッセージを3秒表示
            self.flash_message_for_seconds("₊✩‧₊かわいくなったよ〜💖₊✩‧₊", 3)

        self.update_theme()

    def update_theme(self):
        bg = ThemeManager.get('header_bg')
        fg = ThemeManager.get('clock_fg', "#555")

        self.parent.config(bg=bg)  # ← 追加：親背景も更新
        self.frame.config(bg=bg)
        self.clock_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=fg)
        self.flash_label.config(bg=bg, fg=fg)

    def _show_flash_message(self):
        self.flash_label.place(relx=0.5, rely=0.5, anchor="center")
        self.flash_label.lift()
        self.frame.after(3000, self.flash_label.place_forget)
