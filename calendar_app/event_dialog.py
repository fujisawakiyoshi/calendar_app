import tkinter as tk
from tkinter import simpledialog, messagebox
from event_manager import save_events

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
        events_list = self.events.get(self.date_key, [])

        tk.Label(self.window, text=f"{self.date_key} の予定一覧").pack(pady=5)

        self.listbox = tk.Listbox(self.window, width=40)
        self.listbox.pack()
        for item in events_list:
            self.listbox.insert(tk.END, item)

        add_button = tk.Button(self.window, text="予定を追加", command=self.add_event)
        add_button.pack(pady=5)

        delete_button = tk.Button(self.window, text="選択した予定を削除", command=self.delete_event)
        delete_button.pack(pady=5)

    def add_event(self):
        new_event = simpledialog.askstring("予定追加", "新しい予定を入力してください")
        if new_event:
            if self.date_key not in self.events:
                self.events[self.date_key] = []
            self.events[self.date_key].append(new_event)
            save_events(self.events)
            self.listbox.insert(tk.END, new_event)
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
