# ui/event_dialog.py

import tkinter as tk
from tkinter import messagebox
from services.event_manager import save_events
from ui.event_edit_dialog import EditDialog
from ui.theme import COLORS, FONTS
from ui.tooltip import ToolTip
from utils.resource import resource_path  # ← 追加

class EventDialog:
    """指定された日付のイベント一覧を表示・編集するダイアログ"""

    def __init__(self, parent, date_key, events, on_update_callback):
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        # モーダルウィンドウを非表示で構築（ちらつき防止）
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        self.window.title(f"予定一覧 {self.date_key}")
        # resource_path を使ってアイコンを指定
        self.window.iconbitmap(resource_path("ui/icons/event_icon.ico"))
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(True, False)

        # ウィンドウサイズ & 中央配置
        w, h = 380, 260
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # UI構築
        self.build_ui()

        # モーダル設定 & 表示
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.deiconify()

    def build_ui(self):
        """ヘッダー、リスト、ボタン、ショートカットをまとめて生成"""
        self.create_header()
        self.create_listbox_area()
        self.create_button_area()
        self.bind_shortcuts()

    def create_header(self):
        """ヘッダーラベルを生成"""
        tk.Label(
            self.window,
            text=f"予定一覧（{self.date_key}）",
            font=(FONTS["base"][0], 13, "bold"),
            bg=COLORS["header_bg"],
            fg=COLORS["text"],
            pady=6
        ).pack(fill="x")

    def create_listbox_area(self):
        """イベント一覧用の Listbox とスクロールバー"""
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="both", expand=True, padx=12, pady=6)

        self.listbox = tk.Listbox(
            frame,
            font=FONTS["base"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            bd=0,
            relief="flat",
            selectbackground="#CCE8FF",
            selectforeground="#000000",
            activestyle="none",
            height=6,
            width=35,
            cursor="arrow"  # デフォルト矢印カーソル
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: self.edit_event())

        scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_list()

    def create_button_area(self):
        """追加／編集／削除ボタンを生成し配置、カーソルを手の形に設定"""
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="x", padx=14, pady=(0, 14))

        # 予定追加ボタン
        self.add_icon = tk.PhotoImage(
            file=resource_path("ui/icons/plus_insert_icon.png")
        ).subsample(3, 3)
        add_btn = tk.Button(
            frame,
            text="予定追加",
            image=self.add_icon,
            compound="right",
            command=self.add_event,
            font=FONTS["base"],
            bg=COLORS["today"],
            fg=COLORS["text"],
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2"  # 手の形カーソル
        )
        add_btn.pack(side="left")
        self.add_button_hover(add_btn, original_bg=COLORS["today"])

        # 編集・削除ボタン用フレーム
        right_frame = tk.Frame(frame, bg=COLORS["dialog_bg"])
        right_frame.pack(side="right")

        # 編集ボタン
        self.edit_icon = tk.PhotoImage(
            file=resource_path("ui/icons/notes_edit_icon.png")
        ).subsample(3, 3)
        edit_btn = tk.Button(
            right_frame,
            text="編集",
            image=self.edit_icon,
            compound="right",
            command=self.edit_event,
            font=FONTS["base"],
            bg="#FFE7C1",
            fg=COLORS["text"],
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2"
        )
        edit_btn.pack(side="left", padx=4)
        self.add_button_hover(edit_btn, original_bg="#FFE7C1")

        # 削除ボタン
        self.delete_icon = tk.PhotoImage(
            file=resource_path("ui/icons/delete-trash_icon3.png")
        ).subsample(3, 3)
        del_btn = tk.Button(
            right_frame,
            text="削除",
            image=self.delete_icon,
            compound="right",
            command=self.delete_event,
            font=FONTS["base"],
            bg="#F7C6C7",
            activebackground="#F4B6B7",
            fg=COLORS["text"],
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2"
        )
        del_btn.pack(side="left", padx=4)
        self.add_button_hover(del_btn, original_bg="#F7C6C7")

    def bind_shortcuts(self):
        """キーボードショートカット（Enter: 編集, Delete: 削除, Esc: 閉じる）"""
        self.listbox.bind("<Return>", lambda e: self.edit_event())
        self.listbox.bind("<Delete>", lambda e: self.delete_event())
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def refresh_list(self):
        """Listbox の中身を再描画"""
        self.listbox.delete(0, tk.END)
        for ev in self.events.get(self.date_key, []):
            item = f"{ev['start_time']}-{ev['end_time']}  {ev['title']}"
            if ev.get("memo"):
                item += f"  - {ev['memo']}"
            self.listbox.insert(tk.END, item)

    def add_event(self):
        """追加ダイアログを開いて予定を追加"""
        dialog = EditDialog(self.window, "予定の追加")
        dialog.window.wait_window()
        if dialog.result:
            title, st, et, memo = dialog.result
            self.events.setdefault(self.date_key, []).append({
                "title": title, "start_time": st, "end_time": et, "memo": memo
            })
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()

    def edit_event(self):
        """選択された予定を編集ダイアログで更新"""
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("警告", "編集する予定を選択してください")
            return
        idx = sel[0]
        ev = self.events[self.date_key][idx]
        dialog = EditDialog(
            self.window,
            "予定の編集",
            default_title=ev["title"],
            default_start_time=ev["start_time"],
            default_end_time=ev["end_time"],
            default_content=ev.get("memo", "")
        )
        dialog.window.wait_window()
        if dialog.result:
            self.events[self.date_key][idx] = {
                "title": dialog.result[0],
                "start_time": dialog.result[1],
                "end_time": dialog.result[2],
                "memo": dialog.result[3]
            }
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()

    def delete_event(self):
        """選択された予定を削除"""
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
        
    def add_button_hover(self, button, original_bg, hover_bg=None):
        """ボタンにホバー時の色変化効果を追加する"""
        if hover_bg is None:
            hover_bg = COLORS["button_hover"]

        def on_enter(event):
            button.config(bg=hover_bg)

        def on_leave(event):
            button.config(bg=original_bg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
