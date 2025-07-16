import tkinter as tk
from datetime import datetime

from calendar_renderer import generate_calendar_matrix
from holiday_service import get_holidays_for_year
from event_manager import load_events

from clock_widget import ClockWidget
from event_dialog import EventDialog

COLOR_DEFAULT = "#FFFFFF"
COLOR_SUNDAY = "#FADCD9"
COLOR_SATURDAY = "#DCEEF9"
COLOR_HOLIDAY = "#F6CACA"
COLOR_TODAY = "#C8E4F7"
COLOR_EVENT = "#FFF4CC"

COLOR_HEADER_BG = "#CFE9D6"
COLOR_WEEKDAY_HEADER_BG = "#EAF6ED"

BUTTON_BG_COLOR = "#FFFFFF"
BUTTON_FG_COLOR = "#444444"

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Calendar")
        self.root.geometry("600x600") 

        # 現在年月日
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month

        # データ読み込み
        self.holidays = get_holidays_for_year(self.current_year)
        self.events = load_events()

        # UIセットアップ
        self.setup_ui()

    def setup_ui(self):
        # メイン全体レイアウト用フレーム
        main_frame = tk.Frame(self.root, bg="#F7F7F7")
        main_frame.pack(fill="both", expand=True)

        # -------------------- カレンダー本体 --------------------
        self.calendar_frame = tk.Frame(main_frame, bg="#F7F7F7")
        self.calendar_frame.pack(pady=10)

        self.show_calendar()

        # -------------------- 時計を右下に --------------------
        clock_frame = tk.Frame(main_frame, bg="#F7F7F7")
        clock_frame.pack(fill="both", expand=True)
        self.clock = ClockWidget(clock_frame)

    def show_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        today = datetime.today()
        today_year = today.year
        today_month = today.month
        today_day = today.day

        # -------------------- カレンダーヘッダー行（前月/年月/次月） --------------------
        prev_button = tk.Button(
            self.calendar_frame,
            text="＜",
            command=self.go_prev_month,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 12)
        )
        prev_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.header_label = tk.Label(
            self.calendar_frame,
            text=f"{self.current_year}年 {self.current_month}月",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg=BUTTON_FG_COLOR,
            pady=5
        )
        self.header_label.grid(row=0, column=1, columnspan=5, padx=5, pady=5)

        next_button = tk.Button(
            self.calendar_frame,
            text="＞",
            command=self.go_next_month,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 12)
        )
        next_button.grid(row=0, column=6, sticky="w", padx=5, pady=5)

        # -------------- 曜日ヘッダ --------------
        days = ["日", "月", "火", "水", "木", "金", "土"]
        for idx, day in enumerate(days):
            label = tk.Label(
                self.calendar_frame,
                text=day,
                borderwidth=1,
                relief="ridge",
                width=8,
                height=2,
                font=("Arial", 12, "bold"),
                bg=COLOR_WEEKDAY_HEADER_BG,
                fg="#444444"
            )
            label.grid(row=1, column=idx, padx=1, pady=1)


        # -------------- カレンダーマス目 --------------
        matrix = generate_calendar_matrix(self.current_year, self.current_month)
        for row_idx, week in enumerate(matrix, start=2):
            for col_idx, day in enumerate(week):
                text = "" if day == 0 else str(day)
                date_key = f"{self.current_year}-{self.current_month:02d}-{day:02d}"

                is_holiday = day != 0 and date_key in self.holidays
                has_event = day != 0 and date_key in self.events

                is_sunday = (col_idx == 0)
                is_saturday = (col_idx == 6)

                # 背景色優先順位
                if has_event:
                    bg_color = COLOR_EVENT
                elif (
                    day != 0
                    and self.current_year == today_year
                    and self.current_month == today_month
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

                # セル作成
                label = tk.Label(
                    self.calendar_frame,
                    text=text,
                    borderwidth=1,
                    relief="ridge",
                    width=8,
                    height=3,
                    font=("Arial", 12),
                    bg=bg_color,
                    fg="#333333"
                )

                if day != 0:
                    label.bind("<Button-1>", lambda e, d=date_key: self.open_event_dialog(d))

                label.grid(row=row_idx, column=col_idx, padx=1, pady=1)

        # ヘッダー年月を更新
        self.header_label.config(text=f"{self.current_year}年 {self.current_month}月")

    def go_prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.holidays = get_holidays_for_year(self.current_year)
        self.show_calendar()

    def go_next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.holidays = get_holidays_for_year(self.current_year)
        self.show_calendar()

    def open_event_dialog(self, date_key):
        EventDialog(self.root, date_key, self.events, self.show_calendar)

    def run(self):
        self.root.mainloop()
