import tkinter as tk
from datetime import datetime

class ClockWidget:
    def __init__(self, parent):
        self.label = tk.Label(parent, font=("Arial", 12))
        self.label.pack()
        self.update_clock()

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label.config(text=f"現在時刻: {now}")
        self.label.after(1000, self.update_clock)
