# ui/main_window.py

import tkinter as tk
from datetime import datetime
import os

from controllers.calendar_controller import CalendarController
from ui.calendar_view import CalendarView
from ui.clock_widget import ClockWidget
from ui.theme import COLORS
from services.theme_manager import ThemeManager
from utils.resource import resource_path


class MainWindow:
    """アプリケーションのメインウィンドウを構成するクラス"""

    def __init__(self):
        # 1) Tkinter ルートウィンドウをいったん隠して構築（ちらつき防止）
        self.root = tk.Tk()
        self.root.withdraw()

        # 2) ウィンドウタイトル
        self.root.title("Desktop Calendar")

        # 3) アイコンを ICO で設定
        ico_path = resource_path("ui/icons/event_icon.ico")
        print(f"Generated icon path: {ico_path}")
        if os.path.exists(ico_path):
            print(f"Icon file exists at: {ico_path}") # これを追加
            try:
                self.root.iconbitmap(ico_path)
            except tk.TclError as e:
                print(f"Tkinter TclError when setting icon: {e}") # これを追加
        else:
            print(f"[ERROR] icon not found: {ico_path}")

        # 4) 背景色・リサイズ制御
        self.root.configure(bg=ThemeManager.get("header_bg"))
        self.root.resizable(True, True)
        self.root.attributes("-topmost", False)

        # 5) 位置・サイズを調整して少し右上に寄せる
        self._configure_window_position()

        # 6) カレンダー制御用コントローラー
        self.controller = CalendarController()

        # 7) カレンダー＆時計ウィジェットを組み立て
        self._setup_ui()

        # 8) 完成後に表示
        self.root.after(0, self.root.deiconify)

    def _configure_window_position(self):
        """ウィンドウを画面中央から少し右上に寄せる"""
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        ww, wh = 540, 430
        x = (sw - ww)//2 + 100
        y = (sh - wh)//2 - 80
        self.root.geometry(f"{ww}x{wh}+{x}+{y}")

    def _setup_ui(self):
        """カレンダーと時計のウィジェットを配置"""
        # カレンダー
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

        # 時計
        self.clock_widget = ClockWidget(self.root, on_theme_toggle=self.toggle_theme)

    def on_prev_month(self):
        """＜ボタンで前月へ"""
        self.controller.prev_month()
        self._refresh_calendar()

    def on_next_month(self):
        """＞ボタンで次月へ"""
        self.controller.next_month()
        self._refresh_calendar()

    def _refresh_calendar(self):
        """カレンダーを最新データで再描画"""
        self.calendar_view.update(
            self.controller.current_year,
            self.controller.current_month,
            self.controller.holidays,
            self.controller.events
        )

    def open_event_dialog(self, date_key):
        """日付クリックでイベントダイアログを開く"""
        try:
            from ui.event_dialog import EventDialog
            EventDialog(self.root, date_key, self.controller.events, self._refresh_calendar)
        except Exception as e:
            print(f"イベントダイアログでエラー発生: {e}")

    def toggle_theme(self):
        ThemeManager.toggle_theme()

        self.root.configure(bg=ThemeManager.get("header_bg"))  # ウィンドウ背景を更新
        self._refresh_calendar()                               # カレンダー再描画
        self.clock_widget.update_theme()                       # 時計のテーマ更新
        
    def run(self):
        """メインループ開始"""
        self.root.mainloop()