import tkinter as tk
from datetime import datetime

from utils.calendar_utils import generate_calendar_matrix
from ui.theme import COLORS, FONTS
from ui.tooltip import ToolTip

class CalendarView:
    """カレンダー表示用のUIコンポーネント。"""
    def __init__(self, parent, year, month, holidays, events,
                 on_date_click, on_prev, on_next):
        self.parent = parent
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.on_date_click = on_date_click
        self.on_prev = on_prev
        self.on_next = on_next

        # カレンダー表示用フレーム
        self.frame = tk.Frame(self.parent, bg=COLORS["bg"])
        self.frame.pack(pady=10)

        self.render()

    def update(self, year, month, holidays, events):
        """カレンダー内容を更新して再描画する"""
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.render()

    def render(self):
        self.clear()
        self.draw_header()
        self.draw_weekday_labels()
        self.draw_days()

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def draw_header(self):
        header_frame = tk.Frame(self.frame, bg=COLORS["header_bg"])
        header_frame.grid(row=0, column=0, columnspan=7, sticky="nsew")

        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(3, weight=1)

        prev = tk.Button(
            header_frame, text="＜", command=self.on_prev,
            bg=COLORS["header_bg"], fg=COLORS["text"],
            relief="flat", font=FONTS["header"], width=3
        )
        prev.grid(row=0, column=0, padx=6, pady=6)

        label = tk.Label(
            header_frame, text=f"{self.year}年 {self.month}月",
            font=FONTS["header"], bg=COLORS["header_bg"], fg=COLORS["text"],
            bd=0, padx=12, pady=6
        )
        label.grid(row=0, column=2, padx=6, pady=6)

        nxt = tk.Button(
            header_frame, text="＞", command=self.on_next,
            bg=COLORS["header_bg"], fg=COLORS["text"],
            relief="flat", font=FONTS["header"], width=3
        )
        nxt.grid(row=0, column=4, padx=6, pady=6)

    def draw_weekday_labels(self):
        weekdays = ["日", "月", "火", "水", "木", "金", "土"]
        for i, wd in enumerate(weekdays):
            fg = COLORS["text"]
            if wd == "日":
                fg = "#D14"
            if wd == "土":
                fg = "#449"
            lbl = tk.Label(
                self.frame, text=wd, font=FONTS["base"],
                bg=COLORS["header_bg"], fg=fg,
                width=6, pady=4, bd=0
            )
            lbl.grid(row=1, column=i, padx=4, pady=4)

    def draw_days(self):
        matrix = generate_calendar_matrix(self.year, self.month)

        for r, week in enumerate(matrix, start=2):
            for c, day in enumerate(week):
                txt = str(day) if day else ""
                key = f"{self.year}-{self.month:02d}-{day:02d}" if day else None
                bgc = self.get_day_background(day, c, key)

                lbl = tk.Label(
                    self.frame, text=txt, font=FONTS["base"],
                    bg=bgc, fg=COLORS["text"],
                    width=6, height=2, bd=1, relief="ridge"
                )

                if day:
                    lbl.bind("<Button-1>", lambda e, d=key: self.on_date_click(d))
                    if key in self.events:
                        ToolTip(lbl, "".join(
                            [f"{ev['title']} {ev['start_time']}-{ev['end_time']}" for ev in self.events[key]]
                        ))
                lbl.grid(row=r, column=c, padx=4, pady=4)

    def get_day_background(self, day, col_index, key):
        if not day:
            return COLORS["bg"]
        if key in self.events:
            return COLORS["highlight"]
        if key in self.holidays:
            return COLORS["accent"]
        if self.is_today(day):
            return COLORS["today"]
        if col_index == 0:
            return COLORS["sunday"]
        if col_index == 6:
            return COLORS["saturday"]
        return COLORS["bg"]

    def is_today(self, day):
        today = datetime.today()
        return (
            day == today.day and
            self.month == today.month and
            self.year == today.year
        )
