# tests/test_calendar_controller.py

import pytest
from unittest.mock import patch
from datetime import date, datetime
import calendar

from calendar_app.controllers.calendar_controller import CalendarController


# UT-01: CalendarControllerのインスタンスを作成、current_yearとcurrent_monthが現在の年月であるか確認
def test_calendar_controller_initial_date():
    """
    CalendarControllerが現在の年と月で正しく初期化されることを確認する。
    """
    controller = CalendarController()
    today = datetime.today()
    assert controller.current_year == today.year
    assert controller.current_month == today.month
    

# UT-02: CalendarControllerのprev_month()が正しく動作することを確認
def test_calendar_controller_prev_month():
    """
    CalendarControllerのprev_month()メソッドが、
    月と年を正しく更新することを確認する。
    """
    controller = CalendarController()

    # 今月が1月の場合（年をまたぐケース）のテスト
    controller.current_year = 2025 # 例として2025年1月に設定
    controller.current_month = 1
    controller.prev_month()
    assert controller.current_year == 2024
    assert controller.current_month == 12

    # 今月が1月以外の場合（通常のケース）のテスト
    controller.current_year = 2025 # 例として2025年7月に設定
    controller.current_month = 7
    controller.prev_month()
    assert controller.current_year == 2025
    assert controller.current_month == 6
    

# UT-03: CalendarControllerのnext_month()が正しく動作することを確認
def test_calendar_controller_next_month():
    """
    CalendarControllerのnext_month()メソッドが、
    月と年を正しく更新することを確認する。
    """
    controller = CalendarController()

    # 今月が12月の場合（年をまたぐケース）のテスト
    controller.current_year = 2024 # 例として2024年12月に設定
    controller.current_month = 12
    controller.next_month()
    assert controller.current_year == 2025
    assert controller.current_month == 1

    # 今月が12月以外の場合（通常のケース）のテスト
    controller.current_year = 2025 # 例として2025年7月に設定
    controller.current_month = 7
    controller.next_month()
    assert controller.current_year == 2025
    assert controller.current_month == 8


# UT-12: get_events_for_date() 指定した日付のイベントリストが正しく取得される
def test_get_events_for_date():
    """
    指定した日付のイベントリストが CalendarController によって正しく取得されることを確認する。
    """
    # CalendarController の __init__ で datetime.today() が呼ばれるため、これをモック
    mock_today_date = date(2025, 7, 25) # コントローラ初期化時の日付
    
    # モックするイベントデータ
    mock_events = {
        "2025-07-25": [ # テスト対象日
            {"title": "会議", "start_time": "10:00", "end_time": "11:00", "memo": "プロジェクトミーティング"},
            {"title": "ランチ", "start_time": "12:00", "end_time": "13:00", "memo": "同僚と"}
        ],
        "2025-07-26": [ # 別の日のイベント
            {"title": "セミナー", "start_time": "14:00", "end_time": "16:00", "memo": "技術セミナー"}
        ],
        "2025-07-27": [], # イベントがない日（空リスト）
        "2025-07-28": [ # イベントがあるが取得しない日
             {"title": "別の日のイベント", "start_time": "09:00", "end_time": "10:00", "memo": "関係なし"}
        ]
    }
    
    # 期待される2025-07-25のイベントリスト
    expected_events_for_date = [
        {"title": "会議", "start_time": "10:00", "end_time": "11:00", "memo": "プロジェクトミーティング"},
        {"title": "ランチ", "start_time": "12:00", "end_time": "13:00", "memo": "同僚と"}
    ]
    
    # load_events と datetime.today() と CalendarController.load_data をモックする
    with patch('calendar_app.services.event_manager.load_events', return_value=mock_events), \
         patch('datetime.datetime') as mock_dt, \
         patch('calendar_app.controllers.calendar_controller.CalendarController.load_data') as mock_load_data: # ★ここを追加★
        
        mock_dt.today.return_value = mock_today_date # datetime.today() をモック
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        mock_dt.date = date

        # CalendarController の __init__ が呼び出された後、load_data はモックされているため、
        # 実際にイベントデータをコントローラにセットする
        controller = CalendarController()
        controller.events = mock_events # ★ここを追加★
        controller.holidays = {} # holidaysも必要に応じて設定（今回のテストでは使わないが、整合性のため）

        # 存在する日付のイベントを取得
        events_found = controller.get_events_for_date("2025-07-25")
        assert events_found == expected_events_for_date

        # イベントがない日付のイベントを取得
        events_not_found = controller.get_events_for_date("2025-07-27")
        assert events_not_found == [] # 空のリストが返ることを期待

        # イベントデータに存在しない日付のイベントを取得
        events_non_existent_date = controller.get_events_for_date("2025-07-01") # mock_eventsにこの日付はない
        assert events_non_existent_date == [] # 空のリストが返ることを期待

        # load_data が呼ばれたことを確認 (コンストラクタ内で呼ばれる想定)
        mock_load_data.assert_called_once()
        

# UT-13: add_event_to_date() 指定した日付にイベントが追加され、ファイルに保存される
def test_add_event_to_date():
    """
    add_event_to_date() が新しいイベントを CalendarController の内部データに追加し、
    event_manager.add_event() を呼び出して保存することを確認する。
    """
    # CalendarController の初期化時の日付をモック
    mock_today_date = date(2025, 7, 25)

    # コントローラ初期化時に load_events が返すダミーデータ
    initial_controller_events = {
        "2025-07-24": [
            {"title": "既存イベント", "start_time": "09:00", "end_time": "10:00", "memo": ""}
        ]
    }

    # add_event_to_date が呼び出された後に、コントローラが保持するであろうイベントデータ
    expected_controller_events_after_add = {
        "2025-07-24": [
            {"title": "既存イベント", "start_time": "09:00", "end_time": "10:00", "memo": ""}
        ],
        "2025-07-25": [
            {
                "title": "新規追加イベント",
                "start_time": "14:00",
                "end_time": "15:00",
                "memo": "新しい予定"
            }
        ]
    }

    # add_event_to_date が呼び出す add_event() の引数として期待されるもの
    # add_event(events_data, date_str, title, start_time, end_time, memo)
    expected_add_event_args_on_call = (
        expected_controller_events_after_add, # add_eventに渡されるイベント辞書
        "2025-07-25",
        "新規追加イベント",
        "14:00",
        "15:00",
        "新しい予定"
    )

    # event_manager.add_event をモックする (実際にイベントを追加する代わりに記録する)
    # CalendarController.load_data もモックして、controller.events を手動で設定できるようにする
    with patch('calendar_app.services.event_manager.load_events', return_value=initial_controller_events), \
         patch('calendar_app.services.event_manager.add_event') as mock_add_event, \
         patch('datetime.datetime') as mock_dt, \
         patch('calendar_app.controllers.calendar_controller.CalendarController.load_data'): # load_dataをモック

        mock_dt.today.return_value = mock_today_date
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        mock_dt.date = date

        controller = CalendarController()
        # CalendarControllerの初期化でload_dataがモックされているため、
        # self.eventsを手動で初期データに設定する必要がある
        controller.events = initial_controller_events.copy() # コピーを渡す

        # テスト対象の add_event_to_date を呼び出す
        controller.add_event_to_date("2025-07-25", "新規追加イベント", "14:00", "15:00", "新しい予定")

        # 検証 1: event_manager.add_event が正しく呼び出されたか
        mock_add_event.assert_called_once_with(*expected_add_event_args_on_call)

        # 検証 2: CalendarController 内部の events データが更新されているか
        # add_event 関数が events 辞書をインプレースで更新すると仮定
        assert controller.events == expected_controller_events_after_add