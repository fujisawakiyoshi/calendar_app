import tkinter as tk
from datetime import datetime

from calendar_renderer import generate_calendar_matrix
from ui.constants import (
    COLOR_DEFAULT, COLOR_SUNDAY, COLOR_SATURDAY, COLOR_HOLIDAY, COLOR_TODAY, COLOR_EVENT,
    COLOR_HEADER_BG, COLOR_WEEKDAY_HEADER_BG,
    BUTTON_BG_COLOR, BUTTON_FG_COLOR
)

class CalendarView:
    def __init__(self, parent, year, month, holidays, events,
                 on_date_click, on_prev, on_next):
        """
        parent: 親フレーム
        year, month: 表示する年月
        holidays: 祝日データ
        events: 予定データ
        on_date_click: 日付クリック時のコールバック
        on_prev, on_next: 前月/次月ボタンのコールバック
        """
        self.parent = parent
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.on_date_click = on_date_click
        self.on_prev = on_prev
        self.on_next = on_next

        # カレンダー表示用フレーム
        self.frame = tk.Frame(self.parent, bg=COLOR_HEADER_BG)
        self.frame.pack(pady=10)

        # 最初に描画
        self.render()

    
    def render(self):
        self.clear()
        self.draw_header()
        self.draw_weekday_labels()
        self.draw_days()

    def clear(self):
        """前回の描画をクリア"""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def draw_header(self):
        """前月・次月ボタンと年月ラベル"""
        prev_button = tk.Button(
            self.frame, text="＜", command=self.on_prev,
            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
            relief="flat", font=("Arial", 12)
        )
        prev_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.header_label = tk.Label(
            self.frame,
            text=f"{self.year}年 {self.month}月",
            font=("Arial", 14, "bold"),
            bg=COLOR_HEADER_BG,
            fg=BUTTON_FG_COLOR,
            padx=20, pady=8
        )
        self.header_label.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")

        next_button = tk.Button(
            self.frame, text="＞", command=self.on_next,
            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
            relief="flat", font=("Arial", 12)
        )
        next_button.grid(row=0, column=6, sticky="w", padx=5, pady=5)

    def draw_weekday_labels(self):
        """曜日のラベル行"""
        days = ["日", "月", "火", "水", "木", "金", "土"]
        for idx, day in enumerate(days):
            label = tk.Label(
                self.frame,
                text=day,
                borderwidth=0,
                relief="flat",
                width=6, height=2,
                font=("Arial", 11, "bold"),
                bg=COLOR_WEEKDAY_HEADER_BG,
                fg="#333333",
                padx=3, pady=3
            )
            label.grid(row=1, column=idx, padx=1, pady=1)

    def draw_days(self):
        """日付のマスを描画"""
        today = datetime.today()
        matrix = generate_calendar_matrix(self.year, self.month)

        for row_idx, week in enumerate(matrix, start=2):
            for col_idx, day in enumerate(week):
                text = "" if day == 0 else str(day)
                date_key = f"{self.year}-{self.month:02d}-{day:02d}"

                # 背景色の決定
                bg_color = self.get_cell_bg_color(day, col_idx, date_key, today)

                label = tk.Label(
                    self.frame,
                    text=text,
                    borderwidth=1,
                    relief="ridge",
                    width=6,
                    height=2,
                    font=("Arial", 11),
                    bg=bg_color,
                    fg="#333333",
                    padx=3,
                    pady=3
                )

                if day != 0:
                    label.bind("<Button-1>", lambda e, d=date_key: self.on_date_click(d))
                
                label.grid(row=row_idx, column=col_idx, padx=1, pady=1)
                
    def get_cell_bg_color(self, day, col_idx, date_key, today):
        """日付セルの背景色を返す"""
        if day == 0:
            return COLOR_DEFAULT
        if date_key in self.events:
            return COLOR_EVENT
        if (self.year == today.year and self.month == today.month and day == today.day):
            return COLOR_TODAY
        if date_key in self.holidays:
            return COLOR_HOLIDAY
        if col_idx == 0:
            return COLOR_SUNDAY
        if col_idx == 6:
            return COLOR_SATURDAY
        return COLOR_DEFAULT

