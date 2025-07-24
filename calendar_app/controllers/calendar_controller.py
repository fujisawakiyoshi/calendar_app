from datetime import datetime
from services.holiday_service import get_holidays_for_year
from services.event_manager import load_events

class CalendarController:
    """
    カレンダーの状態（表示する年・月）を管理するコントローラークラス。
    - 表示中の年月に応じた祝日データ・イベントデータを保持
    - 「前月」「次月」への移動機能を提供
    """

    def __init__(self):
        """
        初期化処理。
        現在の日付をもとに表示する年月を決定し、
        それに応じた祝日・イベントを読み込む。
        """
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month
        self.load_data()

    def load_data(self):
        """
        現在の表示年月に基づいて、
        - 該当年の祝日データを取得
        - イベントデータをロード
        """
        self.holidays = get_holidays_for_year(self.current_year)
        self.events = load_events()

    def prev_month(self):
        """
        前月へ移動し、祝日・イベントデータを再読み込みする。
        1月のときは前年12月に切り替える。
        """
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.load_data()

    def next_month(self):
        """
        次月へ移動し、祝日・イベントデータを再読み込みする。
        12月のときは翌年1月に切り替える。
        """
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.load_data()
