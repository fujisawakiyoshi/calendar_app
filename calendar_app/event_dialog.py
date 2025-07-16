import tkinter as tk
from tkinter import messagebox
from event_manager import save_events
from event_edit_dialog import EditDialog

# 色コード
DIALOG_BG_COLOR = "#FFFFFF"
DIALOG_SECTION_BG = "#EAF6ED"
BUTTON_BG_COLOR = "#FFFFFF"
BUTTON_FG_COLOR = "#444444"

class EventDialog:
    def __init__(self, parent, date_key, events, on_update_callback):
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        # ウィンドウ設定
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.date_key)
        self.window.configure(bg=DIALOG_BG_COLOR)
        self.window.resizable(False, False)

        # UI構築
        self.create_widgets()
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.wait_window()

    def create_widgets(self):
        # -------------------- 見出し（薄緑帯） --------------------
        section_label = tk.Label(
            self.window,
            text=f"予定一覧（{self.date_key}）",
            font=("Arial", 13, "bold"),
            bg=DIALOG_SECTION_BG,
            fg=BUTTON_FG_COLOR,
            pady=8
        )
        section_label.pack(fill="x", pady=(5, 0))

        # -------------------- 予定リスト --------------------
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

        # イベントデータ読み込み
        events_list = self.events.get(self.date_key, [])
        for item in events_list:
            self.listbox.insert(tk.END, item)

        # -------------------- 下部ボタン群 --------------------
        button_frame = tk.Frame(self.window, bg=DIALOG_BG_COLOR)
        button_frame.pack(pady=10, padx=10)

        # 追加ボタン（左側、縦に大きめ）
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

        # 右側の削除・編集ボタンを上下に
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

    # -------------------- 予定を追加 --------------------
    def add_event(self):
        dialog = EditDialog(self.window, "予定の追加")
        if dialog.result:
            title, time, content = dialog.result
            new_text = f"{title}（{time}）" if time else title
            if self.date_key not in self.events:
                self.events[self.date_key] = []
            self.events[self.date_key].append(new_text)
            save_events(self.events)
            self.listbox.insert(tk.END, new_text)
            self.on_update_callback()

    # -------------------- 予定を削除 --------------------
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

    # -------------------- 予定を編集 --------------------
    def edit_event(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("警告", "編集する予定を選択してください")
            return

        index = selected[0]
        current_text = self.events[self.date_key][index]

        # --- タイトル（時間）をパース ---
        if "（" in current_text and "）" in current_text:
            title = current_text.split("（")[0]
            time_part = current_text.split("（")[1].replace("）", "")
        else:
            title = current_text
            time_part = ""

        # --- 時間帯を「開始 - 終了」に分割 ---
        if " - " in time_part:
            start_time, end_time = time_part.split(" - ")
        else:
            start_time = time_part
            end_time = ""

        # --- ダイアログ呼び出し ---
        dialog = EditDialog(
            self.window,
            "予定の編集",
            default_title=title,
            default_start_time=start_time,
            default_end_time=end_time,
            default_content=""
        )

        if dialog.result:
            new_title, new_time, new_content = dialog.result
            new_text = f"{new_title}（{new_time}）" if new_time else new_title
            self.events[self.date_key][index] = new_text
            save_events(self.events)
            self.listbox.delete(index)
            self.listbox.insert(index, new_text)
            self.on_update_callback()
