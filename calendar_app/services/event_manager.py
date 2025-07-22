import json
import os
from utils.resource import resource_path

EVENTS_FILE = resource_path("data/events.json")

def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_events(data):
    os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_event(events, date_str, title, time="", memo=""):
    if date_str not in events:
        events[date_str] = []
    new_event = {
        "title": title,
        "time": time,
        "memo": memo
    }
    events[date_str].append(new_event)
    save_events(events)

def delete_event(events, date_str, index):
    if date_str in events and 0 <= index < len(events[date_str]):
        events[date_str].pop(index)
        if not events[date_str]:
            del events[date_str]
        save_events(events)

