# ui/main_window.py

import tkinter as tk
from datetime import datetime

from controllers.calendar_controller import CalendarController
from ui.calendar_view import CalendarView
from ui.clock_widget import ClockWidget
from ui.theme import COLORS


class MainWindow:
    """アプリケーションのメインウィンドウを構成するクラス"""

    def __init__(self):
        # Tkinterルートウィンドウの作成と初期設定
        self.root = tk.Tk()
        self.root.withdraw()  # チラつき防止のため最初は非表示

        self.root.title("Desktop Calendar")
        self.root.iconbitmap("event_icon.ico")
        self.root.configure(bg=COLORS["header_bg"])
        self.root.resizable(True, True)
        self.root.attributes("-topmost", False)

        # ウィンドウサイズと位置の設定
        self.configure_window_position()

        # カレンダー管理用コントローラーの初期化
        self.controller = CalendarController()

        # カレンダーや時計などのUI構築
        self.setup_ui()

        # UI構築完了後にウィンドウを表示
        self.root.after(0, self.root.deiconify)

    def configure_window_position(self):
        """画面サイズを取得し、ウィンドウを少し右上に寄せて表示"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 550
        window_height = 480

        # 中央から +100px 右、-80px 上にずらす
        x = (screen_width - window_width) // 2 + 100
        y = (screen_height - window_height) // 2 - 80

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def setup_ui(self):
        """UIコンポーネント（カレンダー・時計）をセットアップ"""

        # カレンダーの表示部分を作成
        self.calendar_view = CalendarView(
            self.root,
            self.controller.current_year,
            self.controller.current_month,
            self.controller.holidays,
            self.controller.events,
            on_date_click=self.open_event_dialog,  # 日付クリック時の動作
            on_prev=self.on_prev_month,           # 前月ボタン
            on_next=self.on_next_month            # 次月ボタン
        )

        # 右下に現在時刻を表示するウィジェット
        ClockWidget(self.root)

    def on_prev_month(self):
        """前月に移動してカレンダーを更新"""
        self.controller.prev_month()
        self.update_calendar()

    def on_next_month(self):
        """次月に移動してカレンダーを更新"""
        self.controller.next_month()
        self.update_calendar()

    def update_calendar(self):
        """カレンダーUIを最新の状態に再描画"""
        self.calendar_view.update(
            self.controller.current_year,
            self.controller.current_month,
            self.controller.holidays,
            self.controller.events
        )

    def open_event_dialog(self, date_key):
        """指定された日付のイベント一覧ダイアログを開く"""
        from ui.event_dialog import EventDialog
        EventDialog(self.root, date_key, self.controller.events, self.update_calendar)

    def run(self):
        """アプリケーションを開始するメインループ"""
        self.root.mainloop()
