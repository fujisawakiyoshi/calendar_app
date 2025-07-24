import tkinter as tk
from tkinter import ttk
from ui.theme import COLORS, FONTS, TITLE_CHOICES, TIME_CHOICES
from services.theme_manager import ThemeManager
from utils.resource import resource_path


class EditDialog:
    """
    イベントの「追加」または「編集」を行うための入力ダイアログ。
    タイトル・開始時間・終了時間・内容（メモ）を入力できる。
    """

    def __init__(
        self, parent, title,
        default_title="", default_start_time="",
        default_end_time="", default_content=""
    ):
        """
        ダイアログ初期化。

        Args:
            parent: 親ウィンドウ
            title: ダイアログタイトル（ウィンドウ上部に表示される）
            default_title: 初期のタイトル文字列（編集時用）
            default_start_time: 初期の開始時間（"HH:MM"）
            default_end_time: 初期の終了時間（"HH:MM"）
            default_content: 初期のメモ内容
        """
        self.result = None  # OKボタンで返す結果用（None or タプル）

        # Toplevelウィンドウ（サブウィンドウ）を作成し、まず非表示
        self.window = tk.Toplevel(parent)
        self.window.withdraw()
        self.window.title(title)
        self.window.iconbitmap(resource_path("ui/icons/event_icon.ico"))
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(False, False)

        # ウィンドウの中央表示設定
        w, h = 300, 270
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # 初期入力値を保持する StringVar
        self.title_var = tk.StringVar(value=default_title)
        self.start_var = tk.StringVar(value=default_start_time)
        self.end_var = tk.StringVar(value=default_end_time)
        self.content_var = tk.StringVar(value=default_content)

        # UI構築
        self._build_ui()

        # モーダル化（他の操作をブロック）
        self.window.transient(parent)
        self.window.grab_set()

        # フォーカス設定 & 表示
        self.ent_title.focus_set()
        self.window.deiconify()

    def _build_ui(self):
        """全体のUIレイアウトを構築（各セクションの呼び出し）"""
        pad = 8
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="both", expand=True, padx=pad, pady=pad)

        self._create_title_section(frame)
        self._create_time_section(frame)
        self._create_content_section(frame)
        self._create_button_section()

        # Escキーでダイアログを閉じる
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def _create_title_section(self, parent):
        """イベントタイトル入力（ラベル＋コンボボックス）"""
        tk.Label(
            parent,
            text="タイトル：",
            font=FONTS["small"],
            bg=COLORS["dialog_bg"],
            fg=ThemeManager.get("text")
        ).pack(anchor="w", pady=(0, 2))

        self.ent_title = ttk.Combobox(
            parent,
            textvariable=self.title_var,
            values=TITLE_CHOICES,
            font=FONTS["small"],
            state="normal",  # 入力可かつ選択候補付き
            takefocus=True
        )
        self.ent_title.pack(fill="x", pady=(0, 8))

    def _create_time_section(self, parent):
        """開始・終了時間の入力欄を2つ縦に配置"""
        for label_text, var in [("開始時間：", self.start_var), ("終了時間：", self.end_var)]:
            tk.Label(
                parent,
                text=label_text,
                font=FONTS["small"],
                bg=COLORS["dialog_bg"],
                fg=ThemeManager.get("text")
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
        """メモ入力欄（Entry）とプレースホルダー表示"""
        tk.Label(
            parent,
            text="内容：",
            font=FONTS["small"],
            bg=COLORS["dialog_bg"],
            fg=ThemeManager.get("text")
        ).pack(anchor="w", pady=(0, 2))

        self.ent_content = tk.Entry(
            parent,
            textvariable=self.content_var,
            font=FONTS["small"],
            relief="groove",
            takefocus=True,
            bg="#FAFAFA",
            fg="#888888"  # placeholder 初期色
        )
        self.ent_content.pack(fill="x", pady=(0, 8))

        self._add_placeholder(self.ent_content, "メモを入力")

    def _create_button_section(self, parent=None):
        """OK / キャンセルボタンの配置"""
        pad = 8
        btn_frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        btn_frame.pack(fill="x", padx=pad, pady=(0, pad))

        # OKボタン（accentカラー）
        ok_btn = tk.Button(
            btn_frame,
            text="    OK    ",
            command=self.on_ok,
            font=FONTS["base_minus"],
            bg=COLORS["today"],
            fg=ThemeManager.get("text"),
            activebackground=COLORS["today"],
            relief="flat",
            padx=14, pady=4,
            cursor="hand2"
        )
        ok_btn.pack(side="left", anchor="w")
        self.add_button_hover(ok_btn, original_bg=COLORS["today"])

        # キャンセルボタン（ピンク系）
        cancel_btn = tk.Button(
            btn_frame,
            text="キャンセル",
            command=self.window.destroy,
            font=FONTS["base_minus"],
            bg="#F7C6C7",
            fg=ThemeManager.get("text"),
            activebackground="#F4B6B7",
            relief="flat",
            padx=11, pady=4,
            cursor="hand2"
        )
        cancel_btn.pack(side="right", anchor="e")
        self.add_button_hover(cancel_btn, original_bg="#F7C6C7")

    def _add_placeholder(self, widget, placeholder: str):
        """
        Entryウィジェットにプレースホルダー（薄い文字）を表示する。
        フォーカスインで消え、未入力なら再表示。

        Args:
            widget (tk.Entry): 対象のエントリ
            placeholder (str): 表示するプレースホルダーテキスト
        """
        def on_focus_in(event):
            if widget.get() == placeholder:
                widget.delete(0, tk.END)
                widget.config(fg=ThemeManager.get("text"))

        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, placeholder)
                widget.config(fg="#888888")

        if not widget.get():
            widget.insert(0, placeholder)

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)

    def on_ok(self):
        """
        OKボタンが押されたときに呼ばれる。
        入力内容を self.result に格納し、ウィンドウを閉じる。
        """
        self.result = (
            self.title_var.get(),
            self.start_var.get(),
            self.end_var.get(),
            self.content_var.get()
        )
        self.window.destroy()

    def add_button_hover(self, button, original_bg, hover_bg=None):
        """
        ボタンにマウスホバー時の背景色変化を設定。

        Args:
            button: 対象のボタン
            original_bg: 通常時の背景色
            hover_bg: ホバー時の背景色（指定がなければテーマから取得）
        """
        if hover_bg is None:
            hover_bg = COLORS["button_hover"]

        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=original_bg))
