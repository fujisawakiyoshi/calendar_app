import tkinter as tk
from controllers.calendar_controller import CalendarController
from ui.calendar_view import CalendarView
from ui.clock_widget import ClockWidget
from ui.theme import COLORS

class MainWindow:
    """アプリケーションのメインウィンドウ。"""
    def __init__(self):
        # Tkルートウィンドウの初期設定
        self.root = tk.Tk()
        self.root.title("Desktop Calendar")
        self.root.geometry("480x520")
        self.root.configure(bg=COLORS["header_bg"])

        # カレンダーの状態管理用 Controller を生成
        self.controller = CalendarController()

        # UI部品を組み立て
        self.setup_ui()

    def setup_ui(self):
        """全体レイアウト（カレンダー＋時計）の構築"""
        main_frame = tk.Frame(self.root, bg=COLORS["header_bg"])
        main_frame.pack(fill="both", expand=True)

        # カレンダー表示領域
        self.calendar_container = tk.Frame(main_frame, bg=COLORS["header_bg"])
        self.calendar_container.pack(pady=10)
        self.show_calendar()

        # 時計ウィジェット
        clock_frame = tk.Frame(main_frame, bg=COLORS["header_bg"])
        clock_frame.pack(fill="both", expand=True)
        ClockWidget(clock_frame)

    def show_calendar(self):
        """Controller から最新データを取得し、CalendarView を描画"""
        # 既存のカレンダーウィジェットをクリア
        for w in self.calendar_container.winfo_children():
            w.destroy()

        year    = self.controller.current_year
        month   = self.controller.current_month
        holidays = self.controller.holidays
        events   = self.controller.events

        # カレンダー表示用コンポーネントに状態を渡す
        CalendarView(
            parent=self.calendar_container,
            year=year,
            month=month,
            holidays=holidays,
            events=events,
            on_date_click=self.open_event_dialog,
            on_prev=self.on_prev_click,
            on_next=self.on_next_click
        )

    def on_prev_click(self):
        """＜ボタン押下時：Controller で前月に移動し再描画"""
        self.controller.prev_month()
        self.show_calendar()

    def on_next_click(self):
        """＞ボタン押下時：Controller で次月に移動し再描画"""
        self.controller.next_month()
        self.show_calendar()

    def open_event_dialog(self, date_key: str):
        """日付セルクリック時：EventDialog を開き、更新後にカレンダー再描画"""
        from ui.event_dialog import EventDialog  # 循環インポート回避
        EventDialog(self.root, date_key, self.controller.events, self.show_calendar)

    def run(self):
        """アプリ起動"""
        self.root.mainloop()


if __name__ == "__main__":
    MainWindow().run()
