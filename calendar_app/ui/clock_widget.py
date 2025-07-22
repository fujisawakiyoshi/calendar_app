import tkinter as tk
from datetime import datetime
from ui.theme import COLORS  # もし共通のテーマ定義を使っているなら（なければ削除）

class ClockWidget:
    def __init__(self, parent):
        # 時計用フレーム（背景色を統一感のある色に）
        self.frame = tk.Frame(parent, bg=COLORS.get("dialog_bg", "#F9F9F9"))
        self.frame.pack(fill="both", expand=True)

        # 時計ラベル（角丸風マージン＋控えめカラー＋柔らかフォント）
        self.label = tk.Label(
            self.frame,
            font=("Segoe UI", 11),
            bg=self.frame["bg"],
            fg="#555555",  # 薄いグレー
            anchor="se",
            padx=8,
            pady=5
        )
        self.label.pack(anchor="se", padx=10, pady=8)

        self.update_clock()

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label.config(text=f"🕒 {now}")
        self.label.after(1000, self.update_clock)
