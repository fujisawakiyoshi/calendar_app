import tkinter as tk
from datetime import datetime

from calendar_renderer import generate_calendar_matrix

# 色定義
COLOR_DEFAULT = "#FFFFFF"

COLOR_SUNDAY = "#FADCD9"
COLOR_SATURDAY = "#DCEEF9"
COLOR_HOLIDAY = "#F6CACA"
COLOR_TODAY = "#C8E4F7"
COLOR_EVENT = "#FFF4CC"

COLOR_WEEKDAY_HEADER_BG = "#EAF6ED"
COLOR_HEADER_BG = "#F7F7F7"

BUTTON_BG_COLOR = "#F7F7F7"
BUTTON_FG_COLOR = "#444444"

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
        
        self.frame = tk.Frame(self.parent, bg="#F7F7F7")
        self.frame.pack(pady=10)

        # 最初に描画
        self.render()

    def render(self):
        # 前回の内容をクリア
        for widget in self.frame.winfo_children():
            widget.destroy()

        today = datetime.today()
        today_year = today.year
        today_month = today.month
        today_day = today.day

        # -------------------- ヘッダー行（前月/年月/次月） --------------------
        prev_button = tk.Button(
            self.frame,
            text="＜",
            command=self.on_prev,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 12)
        )
        prev_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.header_label = tk.Label(
            self.frame,
            text=f"{self.year}年 {self.month}月",
            font=("Arial", 14, "bold"),
            bg=COLOR_HEADER_BG,
            fg=BUTTON_FG_COLOR,
            padx=20,
            pady=8
        )
        self.header_label.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")

        next_button = tk.Button(
            self.frame,
            text="＞",
            command=self.on_next,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 12)
        )
        next_button.grid(row=0, column=6, sticky="w", padx=5, pady=5)

        # -------------------- 曜日ヘッダ --------------------
        days = ["日", "月", "火", "水", "木", "金", "土"]
        for idx, day in enumerate(days):
            label = tk.Label(
                self.frame,
                text=day,
                borderwidth=0,
                relief="flat",
                width=6,
                height=2,
                font=("Arial", 11, "bold"),
                bg=COLOR_WEEKDAY_HEADER_BG,
                fg="#333333",
                padx=3,
                pady=3
            )
            label.grid(row=1, column=idx, padx=1, pady=1)

        # -------------------- 日付マス --------------------
        matrix = generate_calendar_matrix(self.year, self.month)
        for row_idx, week in enumerate(matrix, start=2):
            for col_idx, day in enumerate(week):
                text = "" if day == 0 else str(day)
                date_key = f"{self.year}-{self.month:02d}-{day:02d}"

                is_holiday = day != 0 and date_key in self.holidays
                has_event = day != 0 and date_key in self.events

                is_sunday = (col_idx == 0)
                is_saturday = (col_idx == 6)

                # 背景色優先順位
                if has_event:
                    bg_color = COLOR_EVENT
                elif (
                    day != 0
                    and self.year == today_year
                    and self.month == today_month
                    and day == today_day
                ):
                    bg_color = COLOR_TODAY
                elif is_holiday:
                    bg_color = COLOR_HOLIDAY
                elif is_sunday:
                    bg_color = COLOR_SUNDAY
                elif is_saturday:
                    bg_color = COLOR_SATURDAY
                else:
                    bg_color = COLOR_DEFAULT

                # 日付セル
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
