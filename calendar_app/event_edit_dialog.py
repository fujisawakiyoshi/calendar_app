import tkinter as tk
from tkinter import ttk

TITLE_CHOICES = [
    "会議/打合せ",
    "来客",
    "外出",
    "出張",
    "休暇",
    "私用",
    "その他"
]

TIME_CHOICES = [
    "07:00", "07:30",
    "08:00", "08:30",
    "09:00", "09:30",
    "10:00", "10:30",
    "11:00", "11:30",
    "12:00", "12:30",
    "13:00", "13:30",
    "14:00", "14:30",
    "15:00", "15:30",
    "16:00", "16:30",
    "17:00", "17:30",
    "18:00", "18:30",
    "19:00", "19:30",
    "20:00", "20:30",
    "21:00", "21:30",
]

# 色コード定義（上品ペールカラー統一テーマ）
DIALOG_BG_COLOR = "#FFFFFF"
BUTTON_BG_COLOR = "#FFFFFF"
BUTTON_FG_COLOR = "#444444"

class EditDialog:
    def __init__(self, parent, title, default_title="", default_start_time="", default_end_time="", default_content=""):
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
        # -------------------- フォームフレーム --------------------
        form_frame = tk.Frame(self.window, bg=DIALOG_BG_COLOR)
        form_frame.pack(padx=20, pady=15, fill="x")

        # --- タイトルラベル+入力 ---
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

        # --- 開始時間 ---
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

        # --- 終了時間 ---
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

        # --- 内容 ---
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

        # -------------------- ボタン --------------------
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
        self.result = (
            self.title_entry.get(),
            f"{self.start_time_var.get()} - {self.end_time_var.get()}",
            self.content_entry.get()
        )

        self.window.destroy()
