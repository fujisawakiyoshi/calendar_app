import tkinter as tk
from datetime import datetime

from calendar_renderer import generate_calendar_matrix
from holiday_service import get_holidays_for_year
from event_manager import load_events

from clock_widget import ClockWidget
from event_dialog import EventDialog
from calendar_view import CalendarView

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Calendar")
        self.root.geometry("480x520")
        self.root.configure(bg="#F7F7F7")

        # 今日の日付
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month

        # 祝日データ
        self.holidays = get_holidays_for_year(self.current_year)
        # 予定データ
        self.events = load_events()

        # 画面レイアウト
        self.setup_ui()

    def setup_ui(self):
        # -------------------- メインレイアウト --------------------
        main_frame = tk.Frame(self.root, bg="#F7F7F7")
        main_frame.pack(fill="both", expand=True)

        # -------------------- カレンダービュー --------------------
        self.calendar_container = tk.Frame(main_frame, bg="#F7F7F7")
        self.calendar_container.pack(pady=10)

        self.show_calendar()

        # -------------------- 時計 --------------------
        clock_frame = tk.Frame(main_frame, bg="#F7F7F7")
        clock_frame.pack(fill="both", expand=True)
        self.clock = ClockWidget(clock_frame)

    def show_calendar(self):
        # 既存をクリア
        for widget in self.calendar_container.winfo_children():
            widget.destroy()

        # CalendarViewを生成
        self.calendar_view = CalendarView(
            parent=self.calendar_container,
            year=self.current_year,
            month=self.current_month,
            holidays=self.holidays,
            events=self.events,
            on_date_click=self.open_event_dialog,
            on_prev=self.go_prev_month,
            on_next=self.go_next_month
        )

    def go_prev_month(self):
        # 月を減算
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

        # 年が変わったら祝日データを再取得
        self.holidays = get_holidays_for_year(self.current_year)

        # 再描画
        self.show_calendar()

    def go_next_month(self):
        # 月を加算
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

        # 年が変わったら祝日データを再取得
        self.holidays = get_holidays_for_year(self.current_year)

        # 再描画
        self.show_calendar()

    def open_event_dialog(self, date_key):
        # 予定ダイアログを開く
        EventDialog(self.root, date_key, self.events, self.show_calendar)

    def run(self):
        self.root.mainloop()
