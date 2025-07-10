import json
import os
import requests

CACHE_FILE = "data/holidays.json"

def fetch_holidays_from_api(year):
    """祝日APIから取得"""
    url = f"https://holidays-jp.github.io/api/v1/{year}/date.json"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return data
    except Exception as e:
        print("API取得失敗:", e)
        return {}

def save_holiday_cache(data):
    """キャッシュファイル保存"""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    target_year = 2025
    holidays = fetch_holidays_from_api(target_year)
    if holidays:
        save_holiday_cache(holidays)
        print(f"{target_year}年の祝日を保存しました")
    else:
        print("祝日データ取得に失敗しました")