from datetime import datetime # datetimeをインポート済み
import calendar # calendarモジュールをインポート済み
from services.holiday_service import get_holidays_for_year # インポート済み
from services.event_manager import load_events # インポート済み
from services.event_manager import add_event # add_event関数をインポート


class CalendarController:
    """カレンダーの状態（年月・祝日・イベント）を管理し、移動操作を提供する"""
    def __init__(self):
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month
        self.holidays = {} # 初期化
        self.events = {}   # 初期化
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
        self.load_data() # 日付変更後にデータを再ロード

    # ★★★ ここに get_events_for_date メソッドを追加 ★★★
    def get_events_for_date(self, date_str: str) -> list[dict]:
        """
        指定された日付のイベントリストを取得します。
        このコントローラが保持するイベントデータを使用します。
        """
        return self.events.get(date_str, []) # self.eventsから取得
    
    # ★★★ ここに add_event_to_date メソッドを追加 ★★★
    # get_events_for_date と同じインデントレベルになるように修正してください
    def add_event_to_date(self, date_str: str, title: str,
                          start_time: str = "", end_time: str = "", memo: str = "") -> None:
        """
        指定された日付に新しいイベントを追加し、保存します。
        """
        add_event(self.events, date_str, title, start_time, end_time, memo)
        # add_event が self.events をインプレースで更新するので、
        # ここで self.events を再ロードする必要はありません。