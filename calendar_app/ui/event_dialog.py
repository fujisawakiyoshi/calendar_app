import tkinter as tk
from tkinter import messagebox

from services.event_manager import save_events
from ui.event_edit_dialog import EditDialog
from ui.theme import COLORS, FONTS
from services.theme_manager import ThemeManager
from ui.tooltip import ToolTip
from utils.resource import resource_path


class EventDialog:
    """
    指定された日付（date_key）のイベントを一覧表示し、
    新規追加・編集・削除ができるポップアップ型ダイアログ。
    """

    def __init__(self, parent, date_key, events, on_update_callback):
        """
        イベントダイアログの初期化。

        Args:
            parent: 親ウィンドウ（Tk or Toplevel）
            date_key (str): "YYYY-MM-DD" の日付文字列
            events (dict): イベント辞書（全日付の予定）
            on_update_callback (Callable): イベント変更後に呼ばれるカレンダー更新関数
        """
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        # --- ダイアログウィンドウの作成（最初は非表示） ---
        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()
        self.window.title(f"予定一覧 {self.date_key}")
        self.window.iconbitmap(resource_path("ui/icons/event_icon.ico"))
        self.window.configure(bg=ThemeManager.get("dialog_bg"))
        self.window.resizable(True, False)

        # --- ウィンドウの中央配置 ---
        w, h = 380, 260
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # --- UIの構築と表示 ---
        self.build_ui()

        # --- モーダル表示（親画面をブロック） ---
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.deiconify()

    def build_ui(self):
        """UI全体（ヘッダー・リスト・ボタン・ショートカット）の構築"""
        self.create_header()
        self.create_listbox_area()
        self.create_button_area()
        self.bind_shortcuts()

    def create_header(self):
        """上部ヘッダーに日付タイトルを表示"""
        tk.Label(
            self.window,
            text=f"予定一覧（{self.date_key}）",
            font=(FONTS["base"][0], 13, "bold"),
            bg=ThemeManager.get("header_bg"),
            fg=ThemeManager.get("text"),
            pady=6
        ).pack(fill="x")

    def create_listbox_area(self):
        """イベント一覧を表示するリストボックス + スクロールバーの構築"""
        frame = tk.Frame(self.window, bg=ThemeManager.get("dialog_bg"))
        frame.pack(fill="both", expand=True, padx=12, pady=6)

        self.listbox = tk.Listbox(
            frame,
            font=FONTS["base"],
            bg=ThemeManager.get("bg"),
            fg=ThemeManager.get("text"),
            bd=0,
            relief="flat",
            selectbackground="#CCE8FF",
            selectforeground="#000000",
            activestyle="none",
            height=6,
            width=35,
            cursor="arrow"
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        # イベント編集：ダブルクリック対応
        self.listbox.bind("<Double-Button-1>", lambda e: self.edit_event())

        # スクロールバー追加
        scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_list()

    def create_button_area(self):
        """下部に追加・編集・削除ボタンを作成して配置"""
        frame = tk.Frame(self.window, bg=ThemeManager.get("dialog_bg"))
        frame.pack(fill="x", padx=14, pady=(0, 14))

        # 予定追加ボタン（左寄せ）
        self.add_icon = tk.PhotoImage(file=resource_path("ui/icons/plus_insert_icon.png")).subsample(3, 3)
        add_btn = tk.Button(
            frame,
            text="予定追加",
            image=self.add_icon,
            compound="right",
            command=self.add_event,
            font=FONTS["base_minus"],
            bg=ThemeManager.get("button_bg_add"),
            fg=ThemeManager.get("text"),
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2"
        )
        add_btn.pack(side="left")
        self.add_button_hover(add_btn, original_bg=ThemeManager.get("button_bg_add"))

        # 編集・削除ボタン（右寄せ）
        right_frame = tk.Frame(frame, bg=ThemeManager.get("dialog_bg"))
        right_frame.pack(side="right")

        # 編集ボタン
        self.edit_icon = tk.PhotoImage(file=resource_path("ui/icons/notes_edit_icon.png")).subsample(3, 3)
        edit_btn = tk.Button(
            right_frame,
            text="編集",
            image=self.edit_icon,
            compound="right",
            command=self.edit_event,
            font=FONTS["base_minus"],
            bg=ThemeManager.get("button_bg_edit"),
            fg=ThemeManager.get("text"),
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2"
        )
        edit_btn.pack(side="left", padx=4)
        self.add_button_hover(edit_btn, original_bg="#FFE7C1")

        # 削除ボタン
        self.delete_icon = tk.PhotoImage(file=resource_path("ui/icons/trash_icon.png")).subsample(3, 3)
        del_btn = tk.Button(
            right_frame,
            text="削除",
            image=self.delete_icon,
            compound="right",
            command=self.delete_event,
            font=FONTS["base_minus"],
            bg=ThemeManager.get("button_bg_delete"),
            fg=ThemeManager.get("text"),
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2",
            activebackground="#F4B6B7"
        )
        del_btn.pack(side="left", padx=4)
        self.add_button_hover(del_btn, original_bg="#F7C6C7")

    def bind_shortcuts(self):
        """キーボードショートカットをバインド"""
        self.listbox.bind("<Return>", lambda e: self.edit_event())
        self.listbox.bind("<Delete>", lambda e: self.delete_event())
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def refresh_list(self):
        """イベント一覧を再描画"""
        self.listbox.delete(0, tk.END)
        for ev in self.events.get(self.date_key, []):
            text = f"{ev['start_time']}-{ev['end_time']}  {ev['title']}"
            if ev.get("memo"):
                text += f"  - {ev['memo']}"
            self.listbox.insert(tk.END, text)

    def add_event(self):
        """新しい予定を作成して保存＆再描画"""
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
        """選択された予定を編集する"""
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("警告", "編集する予定を選択してください")
            return
        idx = sel[0]
        ev = self.events[self.date_key][idx]
        dialog = EditDialog(
            self.window, "予定の編集",
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
        """
        ボタンにホバー効果を追加。
        
        Args:
            button (tk.Button): 対象ボタン
            original_bg (str): 元の背景色
            hover_bg (str): ホバー時の色（未指定ならデフォルト）
        """
        if hover_bg is None:
            hover_bg = COLORS["button_hover"]

        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=original_bg))
