import tkinter as tk
from tkinter import simpledialog, messagebox
from event_manager import save_events

DIALOG_BG_COLOR = "#FFFFFF"
DIALOG_HEADER_BG = "#CFE9D6"
DIALOG_SECTION_BG = "#EAF6ED"
BUTTON_BG_COLOR = "#FFFFFF"
BUTTON_FG_COLOR = "#444444"

class EventDialog:
    def __init__(self, parent, date_key, events, on_update_callback):
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        self.window = tk.Toplevel(self.parent)
        self.window.title(f"{self.date_key} の予定")

        self.create_widgets()
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.wait_window()

    def create_widgets(self):
        self.window.configure(bg=DIALOG_BG_COLOR)

        # -------------------- 見出し --------------------
        section_label = tk.Label(
            self.window,
            text="本日の予定一覧",
            font=("Arial", 12, "bold"),
            bg=DIALOG_SECTION_BG,
            fg=BUTTON_FG_COLOR,
            pady=5
        )
        section_label.pack(fill="x", pady=(5, 0))

        # -------------------- 予定リスト --------------------
        self.listbox = tk.Listbox(
            self.window,
            width=40,
            height=8,
            font=("Arial", 11),
            bg="#FFFFFF",
            fg="#333333",
            relief="ridge",
            borderwidth=1
        )
        self.listbox.pack(padx=10, pady=5)

        events_list = self.events.get(self.date_key, [])
        for item in events_list:
            self.listbox.insert(tk.END, item)

        # -------------------- 下部ボタン --------------------
        button_frame = tk.Frame(self.window, bg=DIALOG_BG_COLOR)
        button_frame.pack(pady=5)

        add_button = tk.Button(
            button_frame,
            text="予定を追加 ⊕",
            command=self.add_event,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11)
        )
        add_button.grid(row=0, column=0, padx=5, pady=5)

        delete_button = tk.Button(
            button_frame,
            text="選択した予定を削除",
            command=self.delete_event,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11)
        )
        delete_button.grid(row=0, column=1, padx=5, pady=5)

        edit_button = tk.Button(
            button_frame,
            text="選択した予定を編集",
            command=self.edit_event,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11)
        )
        edit_button.grid(row=1, column=1, padx=5, pady=5)


    def add_event(self):
        title = simpledialog.askstring("予定のタイトル", "タイトルを入力してください")
        if not title:
            return

        time = simpledialog.askstring("予定の時間", "時間を入力してください（例: 14:00）")
        if time is None:
            time = ""

        memo = simpledialog.askstring("メモ", "メモを入力してください")
        if memo is None:
            memo = ""

        new_event = {
            "title": title,
            "time": time,
            "memo": memo
        }

        if self.date_key not in self.events:
            self.events[self.date_key] = []

        self.events[self.date_key].append(new_event)
        save_events(self.events)
        self.listbox.insert(tk.END, f"{title} ({time})")
        self.on_update_callback()

    def delete_event(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("警告", "削除する予定を選択してください")
            return

        index = selected[0]
        del self.events[self.date_key][index]
        if not self.events[self.date_key]:
            del self.events[self.date_key]
        save_events(self.events)
        self.listbox.delete(index)
        self.on_update_callback()

    def edit_event(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("警告", "編集する予定を選択してください")
            return

        index = selected[0]
        current_text = self.events[self.date_key][index]

        new_event = simpledialog.askstring("予定編集", "予定を編集してください", initialvalue=current_text)
        if new_event:
            self.events[self.date_key][index] = new_event
            save_events(self.events)
            self.listbox.delete(index)
            self.listbox.insert(index, new_event)
            self.on_update_callback()
