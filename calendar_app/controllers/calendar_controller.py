from datetime import datetime
from services.holiday_service import get_holidays_for_year
from services.event_manager import load_events

class CalendarController:
    """カレンダーの状態（年月・祝日・イベント）を管理し、移動操作を提供する"""
    def __init__(self):
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month
        self.load_data()

    def load_data(self):
        """祝日とイベントデータをロードして属性にセット"""
        self.holidays = get_holidays_for_year(self.current_year)
        self.events = load_events()

    def prev_month(self):
        """前月に移動してデータを再ロード"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.load_data()

    def next_month(self):
        """次月に移動してデータを再ロード"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.load_data()
        
    def go_to_today(self):
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month
