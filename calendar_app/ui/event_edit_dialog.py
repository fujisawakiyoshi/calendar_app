import tkinter as tk
from tkinter import ttk
from ui.theme import COLORS, FONTS, TITLE_CHOICES, TIME_CHOICES

class EditDialog:
    """予定の追加・編集用ダイアログウィンドウ"""
    def __init__(self, parent, title,
                 default_title="", default_start_time="",
                 default_end_time="", default_content=""):
        # ダイアログ結果を格納する変数
        self.result = None

        # Toplevel を作成し一時的に非表示化（構築時のちらつき防止）
        self.window = tk.Toplevel(parent)
        self.window.withdraw()
        self.window.title(title)
        self.window.iconbitmap("event_icon.ico")
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(False, False)

        # ウィンドウのサイズと表示位置を設定
        w, h = 300, 270
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # デフォルト値を保持する StringVar
        self.title_var = tk.StringVar(value=default_title)
        self.start_var = tk.StringVar(value=default_start_time)
        self.end_var = tk.StringVar(value=default_end_time)
        self.content_var = tk.StringVar(value=default_content)

        # UI を構築
        self._build_ui()

        # 初期フォーカスをタイトル入力に移動
        self.ent_title.focus_set()
        # モーダル化
        self.window.transient(parent)
        self.window.grab_set()
        # 構築後に表示
        self.window.deiconify()

    def _build_ui(self):
        """ダイアログ内の各セクションを配置"""
        pad = 8
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="both", expand=True, padx=pad, pady=pad)

        # 各入力セクションを個別メソッドで作成
        self._create_title_section(frame)
        self._create_time_section(frame)
        self._create_content_section(frame)
        self._create_button_section()

        # Escキーで閉じる
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def _create_title_section(self, parent):
        """タイトル入力部分を作成"""
        tk.Label(
            parent,
            text="タイトル：",
            font=FONTS["small"],
            bg=COLORS["dialog_bg"],
            fg=COLORS["text"]
        ).pack(anchor="w", pady=(0, 2))

        self.ent_title = ttk.Combobox(
            parent,
            textvariable=self.title_var,
            values=TITLE_CHOICES,
            font=FONTS["small"],
            state="normal",
            takefocus=True
        )
        self.ent_title.pack(fill="x", pady=(0, 8))

    def _create_time_section(self, parent):
        """開始・終了時間の入力部分を作成"""
        for label_text, var in [("開始時間：", self.start_var), ("終了時間：", self.end_var)]:
            tk.Label(
                parent,
                text=label_text,
                font=FONTS["small"],
                bg=COLORS["dialog_bg"],
                fg=COLORS["text"]
            ).pack(anchor="w", pady=(0, 2))

            ttk.Combobox(
                parent,
                textvariable=var,
                values=TIME_CHOICES,
                font=FONTS["small"],
                state="normal",
                takefocus=True
            ).pack(fill="x", pady=(0, 8))

    def _create_content_section(self, parent):
        """メモ入力部分を作成（プレースホルダー付き）"""
        tk.Label(
            parent,
            text="内容：",
            font=FONTS["small"],
            bg=COLORS["dialog_bg"],
            fg=COLORS["text"]
        ).pack(anchor="w", pady=(0, 2))

        self.ent_content = tk.Entry(
            parent,
            textvariable=self.content_var,
            font=FONTS["small"],
            relief="groove",
            takefocus=True,
            bg="#FAFAFA",  # 薄い背景
            fg="#888888"   # 初期グレー文字
        )
        self.ent_content.pack(fill="x", pady=(0, 8))
        self._add_placeholder(self.ent_content, "メモを入力")

    def _create_button_section(self):
        """OK / キャンセルボタンを配置"""
        pad = 8
        btn_frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        btn_frame.pack(fill="x", padx=pad, pady=(0, pad))

        # OK ボタン（today カラーをアクセントに）
        tk.Button(
            btn_frame,
            text="   OK   ",
            command=self.on_ok,
            font=FONTS["base"],
            bg=COLORS["today"],
            fg=COLORS["text"],
            activebackground=COLORS["today"],
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=5,
            takefocus=True,
            cursor="hand2"
        ).pack(side="left", anchor="w")

        # キャンセルボタン（赤系で識別しやすく）
        tk.Button(
            btn_frame,
            text="キャンセル",
            command=self.window.destroy,
            font=FONTS["base"],
            bg="#F7C6C7",
            fg=COLORS["text"],
            activebackground="#F4B6B7",
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=5,
            takefocus=True,
            cursor="hand2"
        ).pack(side="right", anchor="e")

    def _add_placeholder(self, widget, placeholder):
        """Entryにプレースホルダー機能を追加"""
        def on_focus_in(event):
            if widget.get() == placeholder:
                widget.delete(0, tk.END)
                widget.config(fg=COLORS["text"])

        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, placeholder)
                widget.config(fg="#888888")

        # 初期状態で placeholder を挿入
        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg="#888888")

        widget.bind('<FocusIn>', on_focus_in)
        widget.bind('<FocusOut>', on_focus_out)

    def on_ok(self):
        """OK ボタン押下時に結果を取得してダイアログを閉じる"""
        self.result = (
            self.title_var.get(),
            self.start_var.get(),
            self.end_var.get(),
            self.content_var.get()
        )
        self.window.destroy()
