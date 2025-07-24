# ui/main_window.py

import tkinter as tk
from typing import Optional

from controllers.calendar_controller import CalendarController
from ui.calendar_view import CalendarView
from ui.clock_widget import ClockWidget
from services.theme_manager import ThemeManager
from utils.resource import resource_path


class MainWindow:
    """
    アプリケーションのメインウィンドウを構成するクラス。
    カレンダー表示・時計・テーマ切替などのUI要素を統合します。
    """

    def __init__(self) -> None:
        self._init_root_window()
        self.controller = CalendarController()
        self._setup_ui()
        self.root.after(0, self.root.deiconify)

    def _init_root_window(self) -> None:
        """Tkinterルートウィンドウの基本設定"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("Desktop Calendar")
        self.root.iconbitmap(resource_path("ui/icons/event_icon.ico"))
        self.root.configure(bg=ThemeManager.get("header_bg"))
        self.root.resizable(True, True)
        self.root.attributes("-topmost", False)
        self._set_window_position()

    def _set_window_position(self) -> None:
        """ウィンドウの表示位置・サイズを設定"""
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        ww, wh = 540, 430
        x = (sw - ww) // 2 + 100
        y = (sh - wh) // 2 - 80
        self.root.geometry(f"{ww}x{wh}+{x}+{y}")

    def _setup_ui(self) -> None:
        """カレンダーと時計ウィジェットを配置"""
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
        self.clock_widget = ClockWidget(
            self.root,
            on_theme_toggle=self.toggle_theme
        )

    def on_prev_month(self) -> None:
        """前月に移動し、カレンダーを更新"""
        self.controller.prev_month()
        self._refresh_calendar()

    def on_next_month(self) -> None:
        """翌月に移動し、カレンダーを更新"""
        self.controller.next_month()
        self._refresh_calendar()

    def _refresh_calendar(self) -> None:
        """カレンダーを再描画"""
        self.calendar_view.update(
            self.controller.current_year,
            self.controller.current_month,
            self.controller.holidays,
            self.controller.events
        )

    def open_event_dialog(self, date_key: str) -> None:
        """日付クリック時にイベントダイアログを開く"""
        try:
            from ui.event_dialog import EventDialog
            EventDialog(
                self.root,
                date_key,
                self.controller.events,
                self._refresh_calendar
            )
        except Exception as e:
            print(f"[Error] イベントダイアログの表示に失敗: {e}")

    def toggle_theme(self) -> None:
        """テーマを切り替えてUIに反映"""
        ThemeManager.toggle_theme()
        self.root.configure(bg=ThemeManager.get("header_bg"))
        self._refresh_calendar()
        self.clock_widget.update_theme()

    def run(self) -> None:
        """メインループを開始"""
        self.root.mainloop()
