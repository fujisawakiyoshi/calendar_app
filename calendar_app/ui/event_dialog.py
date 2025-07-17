import tkinter as tk
from tkinter import messagebox
from services.event_manager import save_events
from ui.event_edit_dialog import EditDialog

# 色コード
DIALOG_BG_COLOR = "#FFFFFF"
DIALOG_SECTION_BG = "#EAF6ED"
BUTTON_BG_COLOR = "#FFFFFF"
BUTTON_FG_COLOR = "#444444"

class EventDialog:
    """指定された日付のイベント一覧を表示・編集するダイアログ"""
    
    def __init__(self, parent, date_key, events, on_update_callback):
        """parent (tk.Widget): 親ウィンドウ
        date_key (str): 対象日付（例: '2025-07-17'）
        events (dict): イベントデータ（YYYY-MM-DD: [イベントリスト]）
        on_update_callback (Callable): 更新後にカレンダー再描画用の関数
        """
        
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        self.window = tk.Toplevel(self.parent)
        self.window.title(self.date_key)
        self.window.configure(bg=DIALOG_BG_COLOR)
        self.window.resizable(False, False)

        self.create_widgets()

        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.wait_window()

    def create_widgets(self):
        """ダイアログ内のウィジェット（リスト・ボタン類）を作成する"""
        
        # --- 上部タイトルラベル ---
        section_label = tk.Label(
            self.window,
            text=f"予定一覧（{self.date_key}）",
            font=("Arial", 13, "bold"),
            bg=DIALOG_SECTION_BG,
            fg=BUTTON_FG_COLOR,
            pady=8
        )
        section_label.pack(fill="x", pady=(5, 0))

        # --- イベント一覧（Listbox） ---
        self.listbox = tk.Listbox(
            self.window,
            width=45,
            height=10,
            font=("Arial", 11),
            bg="#FFFFFF",
            fg="#333333",
            relief="ridge",
            borderwidth=2
        )
        self.listbox.pack(padx=15, pady=10)

        self.refresh_list()

        # --- 操作ボタン群（追加・削除・編集）---
        button_frame = tk.Frame(self.window, bg=DIALOG_BG_COLOR)
        button_frame.pack(pady=10, padx=10)

        add_button = tk.Button(
            button_frame,
            text="予定追加 ⊕",
            command=self.add_event,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 12),
            width=20,
            height=3
        )
        add_button.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="nsew")

        delete_button = tk.Button(
            button_frame,
            text="削除",
            command=self.delete_event,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11),
            width=15,
            height=2
        )
        delete_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        edit_button = tk.Button(
            button_frame,
            text="編集",
            command=self.edit_event,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11),
            width=15,
            height=2
        )
        edit_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    def refresh_list(self):
        """Listbox に現在のイベントリストを再描画する"""
        self.listbox.delete(0, tk.END)
        for item in self.events.get(self.date_key, []):
            text = f"{item['title']}（{item['start_time']} - {item['end_time']}） - {item['content']}"
            self.listbox.insert(tk.END, text)

    def add_event(self):
        """新しい予定を追加するダイアログを開き、結果を保存する"""
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
        """選択された予定を削除する
        ユーザーが選択していない場合は警告ダイアログを表示する
        """
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
        """選択された予定を編集するためのダイアログを開く
        ユーザーが選択していない場合は警告を表示する
        """
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
