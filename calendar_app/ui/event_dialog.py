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
        # 親ウィンドウ参照、日付キー、イベントデータ、更新コールバックを保持
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        # Toplevel を作成し、まず非表示にしてチラつきを防止
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        self.window.title(f"予定一覧：{self.date_key}")
        self.window.iconbitmap("event_icon.ico")
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(False, False)

        # ウィンドウサイズ＆表示位置を計算して設定（中央寄せ→微調整可）
        w, h = 380, 260
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w)//2, (sh - h)//2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # 各種 UI パーツを構築
        self._build_ui()

        # モーダル設定：親ウィンドウが操作できないように
        self.window.transient(self.parent)
        self.window.grab_set()
        # UI 完成後に表示
        self.window.deiconify()

    def _build_ui(self):
        """ダイアログ全体のレイアウトを組み立て"""
        self._create_header()
        self._create_list_area()
        self._create_button_area()
        self._bind_shortcuts()

    def _create_header(self):
        """ヘッダーラベル（タイトル）を作成"""
        header = tk.Label(
            self.window,
            text=f"予定一覧（{self.date_key}）",
            font=(FONTS["base"][0], 13, "bold"),
            bg=COLORS["header_bg"],
            fg=COLORS["text"],
            pady=6
        )
        header.pack(fill="x")

    def _create_list_area(self):
        """リストボックスとスクロールバーを配置"""
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="both", expand=True, padx=14, pady=8)

        # イベント一覧用 Listbox
        self.listbox = tk.Listbox(
            frame,
            font=FONTS["base"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            bd=1, relief="flat",                # 枠線を表示
            selectbackground="#D0EBFF",       # 選択時背景色
            selectforeground="#000000",       # 選択時文字色
            activestyle="none",
            exportselection=False,              # フォーカス以外でも選択保持
            height=6, width=35
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        # ダブルクリックで編集
        self.listbox.bind("<Double-Button-1>", lambda e: self.edit_event())

        # 縦スクロールバー
        scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # リスト内容を初期表示
        self.refresh_list()

    def _create_button_area(self):
        """追加・編集・削除ボタンを左右に配置"""
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="x", padx=14, pady=(0, 14))

        # ─── 左側：予定追加 ─────────────────────────
        self._plus_icon = tk.PhotoImage(file="plus_insert_icon.png").subsample(3,3)
        add_btn = tk.Button(
            frame,
            text="予定追加",
            image=self._plus_icon, compound="right",
            command=self.add_event,
            font=FONTS["base"],
            bg=COLORS["today"],               # today 色を活用
            fg=COLORS["text"],
            relief="flat",
            padx=8, pady=4,
            cursor="hand2"                    # マウスカーソルを手形に
        )
        add_btn.pack(side="left")
        ToolTip(add_btn, "新しい予定を追加")

        # ─── 右側：編集・削除 ────────────────────────
        right = tk.Frame(frame, bg=COLORS["dialog_bg"])
        right.pack(side="right")

        # 編集ボタン
        self._edit_icon = tk.PhotoImage(file="notes_edit_icon.png").subsample(3,3)
        edit_btn = tk.Button(
            right,
            text="編集",
            image=self._edit_icon, compound="right",
            command=self.edit_event,
            font=FONTS["base"],
            bg="#FFE7C1",                     # パステルオレンジ
            fg=COLORS["text"],
            relief="flat",
            padx=8, pady=4,
            cursor="hand2"
        )
        edit_btn.pack(side="left", padx=4)
        ToolTip(edit_btn, "選択中の予定を編集")

        # 削除ボタン
        self._delete_icon = tk.PhotoImage(file="delete-trash_icon3.png").subsample(3,3)
        del_btn = tk.Button(
            right,
            text="削除",
            image=self._delete_icon, compound="right",
            command=self.delete_event,
            font=FONTS["base"],
            bg="#F7C6C7",                     # パステルレッド
            activebackground="#F4B6B7",
            fg=COLORS["text"],
            relief="flat",
            padx=8, pady=4,
            cursor="hand2"
        )
        del_btn.pack(side="left", padx=4)
        ToolTip(del_btn, "選択中の予定を削除")

    def _bind_shortcuts(self):
        """キーボードショートカットを設定"""
        # Enter：選択中を編集
        self.listbox.bind("<Return>", lambda e: self.edit_event())
        # Delete：選択中を削除
        self.listbox.bind("<Delete>", lambda e: self.delete_event())
        # Esc：ダイアログを閉じる
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def refresh_list(self):
        """リストボックスの中身を再表示"""
        self.listbox.delete(0, tk.END)
        for ev in self.events.get(self.date_key, []):
            line = f"{ev['start_time']}-{ev['end_time']}  {ev['title']}"
            if ev.get("memo"):
                line += f"  - {ev['memo']}"
            self.listbox.insert(tk.END, line)

    def add_event(self):
        """「追加」ボタン押下時の処理"""
        dlg = EditDialog(self.window, "予定の追加")
        # ダイアログが閉じるまで待機
        dlg.window.wait_window()
        if dlg.result:
            title, st, et, memo = dlg.result
            self.events.setdefault(self.date_key, []).append({
                "title": title, "start_time": st, "end_time": et, "memo": memo
            })
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()

    def edit_event(self):
        """「編集」操作：選択項目を EditDialog で編集"""
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("警告", "編集する予定を選択してください")
            return
        idx = sel[0]
        ev = self.events[self.date_key][idx]
        dlg = EditDialog(
            self.window, "予定の編集",
            default_title=ev["title"],
            default_start_time=ev["start_time"],
            default_end_time=ev["end_time"],
            default_content=ev.get("memo", "")
        )
        dlg.window.wait_window()
        if dlg.result:
            self.events[self.date_key][idx] = {
                "title": dlg.result[0],
                "start_time": dlg.result[1],
                "end_time": dlg.result[2],
                "memo": dlg.result[3]
            }
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()

    def delete_event(self):
        """「削除」操作：選択項目をリストとデータから削除"""
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
