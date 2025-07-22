import tkinter as tk
from tkinter import ttk
from ui.theme import COLORS, FONTS, TITLE_CHOICES, TIME_CHOICES

class EditDialog:
    """予定の追加・編集用ダイアログウィンドウ"""
    def __init__(self, parent, title,
                 default_title="", default_start_time="",
                 default_end_time="", default_content=""):
        self.result = None
        self.window = tk.Toplevel(parent)
        self.window.withdraw()
        self.window.title(title)
        self.window.iconbitmap("event_icon.ico")
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(False, False)

        # サイズと中央表示
        w, h = 300, 270
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # 値の保持
        self.title_var = tk.StringVar(value=default_title)
        self.start_var = tk.StringVar(value=default_start_time)
        self.end_var = tk.StringVar(value=default_end_time)
        self.content_var = tk.StringVar(value=default_content)

        self.build_ui()

        self.ent_title.focus_set()
        self.window.transient(parent)
        self.window.grab_set()
        self.window.deiconify()

    def build_ui(self):
        pad = 8
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="both", expand=True, padx=pad, pady=pad)

        self.create_title_section(frame)
        self.create_time_section(frame)
        self.create_content_section(frame)
        self.create_button_section()

        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def create_title_section(self, parent):
        tk.Label(parent, text="タイトル：", font=FONTS["small"],
                 bg=COLORS["dialog_bg"], fg=COLORS["text"]
        ).pack(anchor="w", pady=(0, 2))
        self.ent_title = ttk.Combobox(
            parent, textvariable=self.title_var,
            values=TITLE_CHOICES,
            font=FONTS["small"], state="normal", takefocus=True
        )
        self.ent_title.pack(fill="x", pady=(0, 8))

    def create_time_section(self, parent):
        for label_text, var in [("開始時間：", self.start_var), ("終了時間：", self.end_var)]:
            tk.Label(parent, text=label_text, font=FONTS["small"],
                     bg=COLORS["dialog_bg"], fg=COLORS["text"]
            ).pack(anchor="w", pady=(0, 2))
            ttk.Combobox(
                parent, textvariable=var, values=TIME_CHOICES,
                font=FONTS["small"], state="normal", takefocus=True
            ).pack(fill="x", pady=(0, 8))

    def create_content_section(self, parent):
        tk.Label(parent, text="内容：", font=FONTS["small"],
                 bg=COLORS["dialog_bg"], fg=COLORS["text"]
        ).pack(anchor="w", pady=(0, 2))
        self.ent_content = tk.Entry(
            parent, textvariable=self.content_var,
            font=FONTS["small"], relief="groove", takefocus=True,
            bg="#FAFAFA", fg="#888888"  # 初期グレー
        )
        self.ent_content.pack(fill="x", pady=(0, 8))
        self._add_placeholder(self.ent_content, "メモを入力")

    def create_button_section(self):
        pad = 8
        btn_frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        btn_frame.pack(fill="x", padx=pad, pady=(0, pad))

        tk.Button(
            btn_frame, text="OK", command=self.on_ok,
            font=FONTS["base"], bg=COLORS["today"], fg=COLORS["text"],
            activebackground=COLORS["today"],
            relief="flat", borderwidth=0, padx=12, pady=5, takefocus=True
        ).pack(side="left", anchor="w")

        tk.Button(
            btn_frame, text="キャンセル", command=self.window.destroy,
            font=FONTS["base"], bg="#F7C6C7", fg=COLORS["text"],
            activebackground="#F4B6B7",
            relief="flat", borderwidth=0, padx=12, pady=5, takefocus=True
        ).pack(side="right", anchor="e")

    def _add_placeholder(self, widget, placeholder):
        def on_focus_in(event):
            if widget.get() == placeholder:
                widget.delete(0, tk.END)
                widget.config(fg=COLORS["text"])

        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, placeholder)
                widget.config(fg="#888888")

        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg="#888888")

        widget.bind('<FocusIn>', on_focus_in)
        widget.bind('<FocusOut>', on_focus_out)

    def on_ok(self):
        self.result = (
            self.title_var.get(),
            self.start_var.get(),
            self.end_var.get(),
            self.content_var.get()
        )
        self.window.destroy()
