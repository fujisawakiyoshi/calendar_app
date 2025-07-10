import tkinter as tk
from datetime import datetime
from calendar_renderer import generate_calendar_matrix
from holiday_service import load_holiday_cache

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("カレンダーアプリ")
        self.root.geometry("400x400")
        self.holidays = load_holiday_cache()

        # 現在月
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month

        self.setup_ui()

    def setup_ui(self):
        # ヘッダー：前月・次月ボタン
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=10)

        prev_button = tk.Button(header_frame, text="＜ 前月", command=self.go_prev_month)
        prev_button.pack(side="left")

        self.header_label = tk.Label(header_frame, text=f"{self.current_year}年 {self.current_month}月")
        self.header_label.pack(side="left", padx=10)

        next_button = tk.Button(header_frame, text="次月 ＞", command=self.go_next_month)
        next_button.pack(side="left")

        # カレンダーフレーム
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.show_calendar()

    def show_calendar(self):
        # カレンダークリア
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # 今日の日付情報
        today = datetime.today()
        today_year = today.year
        today_month = today.month
        today_day = today.day

        # 曜日ヘッダ
        days = ["日", "月", "火", "水", "木", "金", "土"]
        for idx, day in enumerate(days):
            label = tk.Label(self.calendar_frame, text=day, borderwidth=1, relief="solid", width=5)
            label.grid(row=0, column=idx)

        # カレンダー本体
        matrix = generate_calendar_matrix(self.current_year, self.current_month)
        for row_idx, week in enumerate(matrix, start=1):
            for col_idx, day in enumerate(week):
                text = "" if day == 0 else str(day)

                # デフォルト背景
                bg_color = "white"

                # 今日の日付をハイライト
                if (
                    day != 0
                    and self.current_year == today_year
                    and self.current_month == today_month
                    and day == today_day
                ):
                    bg_color = "lightblue"

                label = tk.Label(
                    self.calendar_frame,
                    text=text,
                    borderwidth=1,
                    relief="solid",
                    width=5,
                    height=2,
                    bg=bg_color
                )
                label.grid(row=row_idx, column=col_idx)

        # ヘッダー年月を更新
        self.header_label.config(text=f"{self.current_year}年 {self.current_month}月")


    def go_prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_calendar()

    def go_next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar()

    def run(self):
        self.root.mainloop()
