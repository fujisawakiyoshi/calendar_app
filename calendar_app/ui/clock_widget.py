import tkinter as tk
from datetime import datetime

class ClockWidget:
    def __init__(self, parent):
        # 時計用のフレーム
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True)

        # 右下にラベルを配置
        self.label = tk.Label(frame, font=("Arial", 12))
        self.label.pack(anchor="se", padx=10, pady=10)

        self.update_clock()

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label.config(text=f"現在時刻: {now}")
        self.label.after(1000, self.update_clock)

