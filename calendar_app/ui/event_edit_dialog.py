import tkinter as tk
from tkinter import ttk
from ui.theme import (
    TITLE_CHOICES, TIME_CHOICES, DIALOG_BG_COLOR, BUTTON_BG_COLOR, BUTTON_FG_COLOR
)

class EditDialog:
    """イベントのタイトル・時間・内容を編集するためのダイアログ"""
    def __init__(
        self, 
        parent, 
        title, 
        default_title="", 
        default_start_time="", 
        default_end_time="", 
        default_content=""
        ):
        """
        parent (tk.Widget): 親ウィンドウ。
        title (str): ダイアログのタイトル。
        default_title (str, optional): 初期タイトル値。
        default_start_time (str, optional): 初期開始時間。
        default_end_time (str, optional): 初期終了時間。
        default_content (str, optional): 初期内容。
        """
        self.result = None

        self.start_time_var = tk.StringVar(value=default_start_time)
        self.end_time_var = tk.StringVar(value=default_end_time)

        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.configure(bg=DIALOG_BG_COLOR)
        self.window.resizable(False, False)

        # ウィジェットを生成
        self.create_widgets(default_title, default_content)

        self.window.transient(parent)
        self.window.grab_set()
        self.window.wait_window()

    def create_widgets(self, default_title, default_content):
        """入力フィールド（タイトル、時間、内容）と操作ボタンを作成する。"""
        # --- 入力フォームの外枠 ---
        form_frame = tk.Frame(self.window, bg=DIALOG_BG_COLOR)
        form_frame.pack(padx=20, pady=15, fill="x")

        # --- タイトル選択欄（コンボボックス） ---
        tk.Label(
            form_frame, text="タイトル（選択または入力）：", 
            bg=DIALOG_BG_COLOR,
            anchor="w", font=("Arial", 11)
        ).pack(fill="x", pady=(0,2))

        self.title_var = tk.StringVar(value=default_title)
        self.title_entry = ttk.Combobox(
            form_frame,
            textvariable=self.title_var,
            values=TITLE_CHOICES,
            state="normal",
            font=("Arial", 11)
        )
        self.title_entry.pack(fill="x", pady=(0,8))

        # --- 開始時間選択欄 ---
        tk.Label(
            form_frame, text="開始時間（選択または入力）：",
            bg=DIALOG_BG_COLOR,
            anchor="w", font=("Arial", 11)
        ).pack(fill="x", pady=(0,2))

        self.start_time_entry = ttk.Combobox(
            form_frame,
            textvariable=self.start_time_var,
            values=TIME_CHOICES,
            state="normal",
            font=("Arial", 11)
        )
        self.start_time_entry.pack(fill="x", pady=(0,8))

        # --- 終了時間選択欄 ---
        tk.Label(
            form_frame, text="終了時間（選択または入力）：",
            bg=DIALOG_BG_COLOR,
            anchor="w", font=("Arial", 11)
        ).pack(fill="x", pady=(0,2))

        self.end_time_entry = ttk.Combobox(
            form_frame,
            textvariable=self.end_time_var,
            values=TIME_CHOICES,
            state="normal",
            font=("Arial", 11)
        )
        self.end_time_entry.pack(fill="x", pady=(0,8))

        # --- 内容入力欄 ---
        tk.Label(
            form_frame, text="内容：", bg=DIALOG_BG_COLOR,
            anchor="w", font=("Arial", 11)
        ).pack(fill="x", pady=(0,2))

        self.content_entry = tk.Entry(
            form_frame, font=("Arial", 11),
            relief="ridge", bd=1
        )
        self.content_entry.insert(0, default_content)
        self.content_entry.pack(fill="x", pady=(0,8))

        # --- OK / Cancel ボタン ---
        button_frame = tk.Frame(self.window, bg=DIALOG_BG_COLOR)
        button_frame.pack(pady=10)

        ok_button = tk.Button(
            button_frame,
            text="OK",
            command=self.on_ok,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11),
            width=10
        )
        ok_button.pack(side="left", padx=10)

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11),
            width=10
        )
        cancel_button.pack(side="left", padx=10)

    def on_ok(self):
        """ユーザーが入力したデータを result に格納し、ダイアログを閉じる。"""
        title = self.title_var.get()
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        content = self.content_entry.get()

        self.result = (title, start_time, end_time, content)
        self.window.destroy()
