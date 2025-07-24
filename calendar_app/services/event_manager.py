import json
import os
import sys
from threading import Lock
from utils.resource import resource_path

# 保存用JSONファイルのパスを取得（書き込み可能モードで取得）
EVENTS_FILE = resource_path("data/events.json", writable=True)

# 複数スレッドからの同時アクセスを防ぐためのロック
_FILE_LOCK = Lock()


def load_events() -> dict:
    """
    イベントデータを JSON ファイルから読み込んで返す。

    Returns:
        dict: {日付: [予定リスト]} 形式の辞書。エラー時は空の dict。
    """
    try:
        with open(EVENTS_FILE, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}  # dict 以外の形式だった場合も安全に空辞書を返す
    except FileNotFoundError:
        return {}  # ファイルが存在しない場合は空データで開始
    except json.JSONDecodeError:
        # JSON構文エラー：データ破損の可能性
        print(f"[warning] イベントファイルの読み込みに失敗しました: {EVENTS_FILE}", file=sys.stderr)
        return {}


def save_events(events: dict) -> None:
    """
    イベントデータを JSON ファイルに保存する。

    Args:
        events (dict): 保存するイベントデータ

    ※ 書き込み前に必要なディレクトリを自動作成
    ※ 排他ロックを使用して thread-safe に動作
    """
    os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
    with _FILE_LOCK:
        with open(EVENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(events, f, ensure_ascii=False, indent=2)


def add_event(events: dict,
              date_str: str,
              title: str,
              start_time: str = "",
              end_time: str = "",
              memo: str = "") -> None:
    """
    新しいイベントを指定日のリストに追加し、保存する。

    Args:
        events (dict): 現在のイベント辞書
        date_str (str): "YYYY-MM-DD" 形式の日付
        title (str): タイトル
        start_time (str): 開始時間（例: "10:00"）
        end_time (str): 終了時間（例: "11:00"）
        memo (str): メモ
    """
    events.setdefault(date_str, []).append({
        "title":       title,
        "start_time":  start_time,
        "end_time":    end_time,
        "memo":        memo
    })
    save_events(events)


def delete_event(events: dict, date_str: str, index: int) -> None:
    """
    指定日のイベントから指定インデックスの予定を削除する。

    Args:
        events (dict): イベント辞書
        date_str (str): 日付（"YYYY-MM-DD"）
        index (int): 削除したいイベントのインデックス
    """
    if date_str in events and 0 <= index < len(events[date_str]):
        events[date_str].pop(index)
        # その日が空になったら日付ごと削除
        if not events[date_str]:
            del events[date_str]
        save_events(events)
