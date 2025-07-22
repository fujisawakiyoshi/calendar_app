# ui/main_window.py

import tkinter as tk
from controllers.calendar_controller import CalendarController
from ui.calendar_view import CalendarView
from ui.clock_widget import ClockWidget
from ui.theme import COLORS
from datetime import datetime


class MainWindow:
    """アプリケーションのメインウィンドウ。"""
    def __init__(self):
        # Tkルートウィンドウの初期設定
        self.root = tk.Tk()
        self.root.withdraw()  # 一旦非表示（ちらつき防止）
        self.root.title("Desktop Calendar")
        self.root.iconbitmap("event_icon.ico")
        self.root.geometry("580x530")
        self.root.configure(bg=COLORS["header_bg"])
        self.root.resizable(True, True)
        self.root.attributes("-topmost", False)

        # コントローラーとUIのセットアップ
        self.controller = CalendarController()
        self.setup_ui()

        # UI構築後に表示（ちらつき防止）
        self.root.after(0, self.root.deiconify)

    def setup_ui(self):
        # カレンダー表示部
        self.calendar_view = CalendarView(
            self.root,
            self.controller.current_year,
            self.controller.current_month,
            self.controller.holidays,
            self.controller.events,
            on_date_click=self.open_event_dialog,
            on_prev=self.on_prev_month,
            on_next=self.on_next_month
        )

        # 時計ウィジェット（右下）
        ClockWidget(self.root)

    def on_prev_month(self):
        self.controller.prev_month()
        self.update_calendar()

    def on_next_month(self):
        self.controller.next_month()
        self.update_calendar()

    def update_calendar(self):
        self.calendar_view.update(
            self.controller.current_year,
            self.controller.current_month,
            self.controller.holidays,
            self.controller.events
        )

    def open_event_dialog(self, date_key):
        from ui.event_dialog import EventDialog
        EventDialog(self.root, date_key, self.controller.events, self.update_calendar)

    def run(self):
        self.root.mainloop()
