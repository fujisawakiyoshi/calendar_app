
# ui/event_dialog.py

import tkinter as tk
from tkinter import messagebox
from services.event_manager import save_events
from ui.event_edit_dialog import EditDialog
from ui.theme import COLORS, FONTS
from ui.tooltip import ToolTip

class EventDialog:
    """指定された日付のイベント一覧を表示・編集するダイアログ"""
    def __init__(self, parent, date_key, events, on_update_callback):
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        # モーダルウィンドウ設定
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"予定一覧 {self.date_key}")
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(False, False)

        # サイズ調整 & 中央表示（メイン画面に合わせて小さめ）
        w, h = 380, 260
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w)//2, (sh - h)//2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        self.create_widgets()
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.wait_window()

    def create_widgets(self):
        # ヘッダー（文字サイズを少し小さめに）
        header = tk.Label(
            self.window,
            text=f"予定一覧（{self.date_key}）",
            font=(FONTS["base"][0], 13, "bold"),  # 13ptに調整
            bg=COLORS["header_bg"],
            fg=COLORS["text"],
            pady=6
        )
        header.pack(fill="x")

        # イベントリスト領域（枠線なし、選択色を変更）
        frame_list = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame_list.pack(fill="both", expand=True, padx=14, pady=8)

        self.listbox = tk.Listbox(
            frame_list,
            font=FONTS["base"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            bd=0,
            relief="flat",
            selectbackground="#CCE8FF",  # 新しい選択色（パステルブルー系）
            activestyle="none",
            height=6,
            width=35
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: self.edit_event())

        scrollbar = tk.Scrollbar(frame_list, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.refresh_list()

        # ボタンフレーム
        btn_frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        btn_frame.pack(fill="x", padx=14, pady=(0,14))

        # 追加ボタン (左)
        add_btn = tk.Button(
            btn_frame, text="予定追加 ＋", command=self.add_event,
            font=FONTS["base"],
            bg="#AEDFF7", fg=COLORS["text"],  # パステルブルー
            relief="flat", padx=8, pady=4
        )
        add_btn.pack(side="left")
        ToolTip(add_btn, "新しい予定を追加")

        # 編集・削除ボタン (右)
        right_frame = tk.Frame(btn_frame, bg=COLORS["dialog_bg"])
        right_frame.pack(side="right")

        edit_btn = tk.Button(
            right_frame, text="編集 ✎", command=self.edit_event,
            font=FONTS["base"],
            bg="#FFDDAA", fg=COLORS["text"],  # パステルオレンジ
            relief="flat", padx=8, pady=4
        )
        edit_btn.pack(side="left", padx=4)
        ToolTip(edit_btn, "選択中の予定を編集")

        del_btn = tk.Button(
            right_frame, text="削除 🗑", command=self.delete_event,
            font=FONTS["base"],
            bg="#F7C6C7", fg=COLORS["text"],  # パステルレッド
            relief="flat", padx=8, pady=4
        )
        del_btn.pack(side="left", padx=4)
        ToolTip(del_btn, "選択中の予定を削除")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for ev in self.events.get(self.date_key, []):
            # タイトルの後ろにメモ内容を追加表示
            memo = ev.get("memo", "")
            item = f"{ev['start_time']}-{ev['end_time']}  {ev['title']}"
            if memo:
                item += f"  - {memo}"
            self.listbox.insert(tk.END, item)

    def add_event(self):
        dialog = EditDialog(self.window, "予定の追加")
        if dialog.result:
            title, st, et, memo = dialog.result
            self.events.setdefault(self.date_key, []).append({
                "title": title, "start_time": st, "end_time": et, "memo": memo
            })
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()

    def edit_event(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("警告", "編集する予定を選択してください")
            return
        idx = sel[0]
        cur = self.events[self.date_key][idx]
        dialog = EditDialog(
            self.window, "予定の編集",
            default_title=cur["title"], default_start_time=cur["start_time"],
            default_end_time=cur["end_time"], default_content=cur.get("memo", "")
        )
        if dialog.result:
            title, st, et, memo = dialog.result
            self.events[self.date_key][idx] = {
                "title": title, "start_time": st, "end_time": et, "memo": memo
            }
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()

    def delete_event(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("警告", "削除する予定を選択してください")
            return
        idx = sel[0]
        del self.events[self.date_key][idx]
        if not self.events[self.date_key]:
            del self.events[self.date_key]
        save_events(self.events)
        self.refresh_list()
        self.on_update_callback()

