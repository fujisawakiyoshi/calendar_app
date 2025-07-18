import tkinter as tk
from tkinter import messagebox
from services.event_manager import save_events
from ui.event_edit_dialog import EditDialog
from ui.theme import COLORS, FONTS  # FONTSを使っていない場合は除外可

class EventDialog:
    """指定された日付のイベント一覧を表示・編集するダイアログ"""

    def __init__(self, parent, date_key, events, on_update_callback):
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        self.window = tk.Toplevel(self.parent)
        self.window.title(f"予定一覧 {self.date_key}")
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(True, True)

        # ウィンドウ中央に配置
        w, h = 440, 320
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        self.create_widgets()

        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.wait_window()

    def create_widgets(self):
        # タイトルラベル
        section_label = tk.Label(
            self.window,
            text=f"予定一覧（{self.date_key}）",
            font=("ヒラギノ角ゴ ProN W3", 14, "bold"),  # 上品な日本語フォント
            bg=COLORS["dialog_section_bg"],
            fg=COLORS["button_fg"],
            pady=8
        )
        section_label.pack(fill="x", pady=(5, 0))

        # イベント一覧 Listbox
        list_frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        list_frame.pack(fill="both", expand=True, padx=15, pady=(10, 5))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            width=42,
            height=8,
            font=("游ゴシック", 11),
            bg="#FFFFFF",
            fg=COLORS["text"],
            relief="ridge",
            borderwidth=2,
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.refresh_list()

        # 操作ボタンフレーム（2カラム構成）
        button_frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        button_frame.pack(pady=(3, 10), padx=10, fill="x")

        # 左側：予定追加
        add_button = tk.Button(
            button_frame,
            text="予定追加 ⊕",
            command=self.add_event,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            relief="flat",
            font=("游ゴシック", 11),
            width=18,
            height=2
        )
        add_button.pack(side="left", padx=5)

        # 右側：編集・削除（縦配置）
        right_buttons = tk.Frame(button_frame, bg=COLORS["dialog_bg"])
        right_buttons.pack(side="right")

        edit_button = tk.Button(
            right_buttons,
            text="編集",
            command=self.edit_event,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            relief="flat",
            font=("游ゴシック", 11),
            width=15,
            height=1
        )
        edit_button.pack(padx=3, pady=3)

        delete_button = tk.Button(
            right_buttons,
            text="削除",
            command=self.delete_event,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            relief="flat",
            font=("游ゴシック", 11),
            width=15,
            height=1
        )
        delete_button.pack(padx=5, pady=3)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for item in self.events.get(self.date_key, []):
            text = f"{item['title']}（{item['start_time']} - {item['end_time']}） - {item['content']}"
            self.listbox.insert(tk.END, text)

    def add_event(self):
        dialog = EditDialog(self.window, "予定の追加")
        if dialog.result:
            title, start_time, end_time, content = dialog.result
            new_event = {
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "content": content
            }
            if self.date_key not in self.events:
                self.events[self.date_key] = []
            self.events[self.date_key].append(new_event)
            save_events(self.events)
            self.refresh_list()
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
        self.refresh_list()
        self.on_update_callback()

    def edit_event(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("警告", "編集する予定を選択してください")
            return

        index = selected[0]
        current_event = self.events[self.date_key][index]

        dialog = EditDialog(
            self.window,
            "予定の編集",
            default_title=current_event["title"],
            default_start_time=current_event["start_time"],
            default_end_time=current_event["end_time"],
            default_content=current_event["content"]
        )

        if dialog.result:
            new_title, new_start_time, new_end_time, new_content = dialog.result
            updated_event = {
                "title": new_title,
                "start_time": new_start_time,
                "end_time": new_end_time,
                "content": new_content
            }
            self.events[self.date_key][index] = updated_event
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()
