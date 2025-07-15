import tkinter as tk
from datetime import datetime

from calendar_renderer import generate_calendar_matrix
from holiday_service import get_holidays_for_year
from event_manager import load_events

from clock_widget import ClockWidget
from event_dialog import EventDialog


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Calendar")
        self.root.geometry("400x400")
        
        # 現在年月日
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month
        
        # 祝日データを読み込む"
        self.holidays = get_holidays_for_year(self.current_year)
        # 予定データをファイルから読み込む"
        self.events = load_events()
        # 画面をレイアウトする処理へ
        self.setup_ui()

    def setup_ui(self):
        # ヘッダー：前月・次月ボタン
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=10, anchor="center")
        
        # 前月ボタン → クリックで go_prev_month
        prev_button = tk.Button(header_frame, text="＜ 前月", command=self.go_prev_month)
        prev_button.grid(row=0, column=0, padx=10)
        
        # 今表示中の「年月」を大きく表示
        self.header_label = tk.Label(
            header_frame,
            text=f"{self.current_year}年 {self.current_month}月",
            font=("Helvetica", 16, "bold")
        )
        self.header_label.grid(row=0, column=1, padx=20)
        
        #次月ボタン → クリックで go_next_month
        next_button = tk.Button(header_frame, text="次月 ＞", command=self.go_next_month)
        next_button.grid(row=0, column=2, padx=10)
        
        # カレンダーのマス目を入れるフレーム
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        # カレンダーを最初に描画
        self.show_calendar()
        #時計を取り込む
        self.clock = ClockWidget(self.root)

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

        # カレンダーの行列を生成
        matrix = generate_calendar_matrix(self.current_year, self.current_month)
        # 描画ループ
        for row_idx, week in enumerate(matrix, start=1):
            for col_idx, day in enumerate(week):
                text = "" if day == 0 else str(day)

                date_key = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                is_holiday = day != 0 and date_key in self.holidays
                has_event = day != 0 and date_key in self.events

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

                # 祝日は赤に
                if is_holiday:
                    bg_color = "pink"
                
                # 予定
                if has_event:
                    bg_color = "yellow"

                label = tk.Label(
                    self.calendar_frame,
                    text=text,
                    borderwidth=1,
                    relief="solid",
                    width=5,
                    height=2,
                    bg=bg_color
                )
                # ⭐ 日付をクリックで予定ダイアログを開く
                if day != 0:
                    label.bind("<Button-1>", lambda e, d=date_key: self.open_event_dialog(d))
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
        # 年が変わったら祝日データも取る
        self.holidays = get_holidays_for_year(self.current_year)
        self.show_calendar()
        
    def go_next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar()
        # 年が変わったら祝日データも取る
        self.holidays = get_holidays_for_year(self.current_year)
        self.show_calendar()

    def open_event_dialog(self, date_key):
        EventDialog(self.root, date_key, self.events, self.show_calendar)
    
    def run(self):
        self.root.mainloop()