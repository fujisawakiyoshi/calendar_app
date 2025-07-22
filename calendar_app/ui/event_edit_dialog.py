
# ui/event_edit_dialog.py

import tkinter as tk
from tkinter import ttk
from ui.theme import COLORS, FONTS, TITLE_CHOICES, TIME_CHOICES

class EditDialog:
    """イベントのタイトル・時間・内容を編集するためのダイアログ"""
    def __init__(self, parent, title,
                 default_title="", default_start_time="",
                 default_end_time="", default_content=""):  
        self.result = None
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.iconbitmap("event_icon.ico")
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(False, False)

        # サイズ調整 & 中央表示
        w, h = 280, 260
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w)//2, (sh - h)//2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # 変数
        self.title_var = tk.StringVar(value=default_title)
        self.start_var = tk.StringVar(value=default_start_time)
        self.end_var   = tk.StringVar(value=default_end_time)
        self.content_var = tk.StringVar(value=default_content)

        self.create_widgets()
        # 初期フォーカス
        self.ent_title.focus_set()
        self.window.transient(parent)
        self.window.grab_set()
        self.window.wait_window()

    def _add_placeholder(self, widget, placeholder):
        def on_focus_in(event):
            if widget.get() == placeholder:
                widget.delete(0, tk.END)
                widget.config(fg=COLORS["text"])
        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, placeholder)
                widget.config(fg="#888888")
        widget.insert(0, placeholder)
        widget.config(fg="#888888")
        widget.bind('<FocusIn>', on_focus_in)
        widget.bind('<FocusOut>', on_focus_out)

    def create_widgets(self):
        pad = 6
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="both", expand=True, padx=pad, pady=pad)

        # タイトル
        tk.Label(
            frame, text="タイトル：", font=FONTS["small"],
            bg=COLORS["dialog_bg"], fg=COLORS["text"]
        ).pack(anchor="w", pady=(0,2))
        self.ent_title = ttk.Combobox(
            frame, textvariable=self.title_var,
            values=TITLE_CHOICES,
            font=FONTS["small"], state="normal", takefocus=True
        )
        self.ent_title.pack(fill="x", pady=(0,6))

        # 開始時間
        tk.Label(
            frame, text="開始時間：", font=FONTS["small"],
            bg=COLORS["dialog_bg"], fg=COLORS["text"]
        ).pack(anchor="w", pady=(0,2))
        self.ent_start = ttk.Combobox(
            frame, textvariable=self.start_var,
            values=TIME_CHOICES,
            font=FONTS["small"], state="normal", takefocus=True
        )
        self.ent_start.pack(fill="x", pady=(0,6))

        # 終了時間
        tk.Label(
            frame, text="終了時間：", font=FONTS["small"],
            bg=COLORS["dialog_bg"], fg=COLORS["text"]
        ).pack(anchor="w", pady=(0,2))
        self.ent_end = ttk.Combobox(
            frame, textvariable=self.end_var,
            values=TIME_CHOICES,
            font=FONTS["small"], state="normal", takefocus=True
        )
        self.ent_end.pack(fill="x", pady=(0,6))

        # 内容
        tk.Label(
            frame, text="内容：", font=FONTS["small"],
            bg=COLORS["dialog_bg"], fg=COLORS["text"]
        ).pack(anchor="w", pady=(0,2))
        self.ent_content = tk.Entry(
            frame, textvariable=self.content_var,
            font=FONTS["small"], relief="flat", takefocus=True,
            bg=COLORS["dialog_bg"], fg=COLORS["text"]
        )
        self.ent_content.pack(fill="x", pady=(0,6))
        # コンテンツのみプレースホルダー設定
        self._add_placeholder(self.ent_content, "メモを入力")

        # ボタン
        btn_frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        btn_frame.pack(fill="x", padx=pad, pady=(0,pad))
        tk.Button(
            btn_frame, text="OK", command=self.on_ok,
            font=FONTS["base"], bg=COLORS["dialog_bg"], fg=COLORS["text"],
            relief="flat", borderwidth=0, padx=10, pady=4, takefocus=True
        ).pack(side="left", expand=True, padx=4)
        tk.Button(
            btn_frame, text="キャンセル", command=self.window.destroy,
            font=FONTS["base"], bg=COLORS["dialog_bg"], fg=COLORS["text"],
            relief="flat", borderwidth=0, padx=10, pady=4, takefocus=True
        ).pack(side="right", expand=True, padx=4)
        
        self.window.bind("<Escape>", lambda e: self.window.destroy())  # Escで閉じる

    def on_ok(self):
        self.result = (
            self.title_var.get(),
            self.start_var.get(),
            self.end_var.get(),
            self.content_var.get()
        )
        self.window.destroy()