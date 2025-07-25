# ui/event_edit_dialog.py

import tkinter as tk
import sys
import os
from tkinter import ttk
from ui.theme import COLORS, FONTS, TITLE_CHOICES, TIME_CHOICES
from services.theme_manager import ThemeManager
from utils.resource import resource_path

class EditDialog:
    """予定の追加・編集用ダイアログウィンドウ"""

    def __init__(
        self, parent, title,
        default_title="", default_start_time="",
        default_end_time="", default_content=""
    ):
        # ダイアログから返す結果（OK 押下時にタプルで設定）
        self.result = None

        # Toplevel を作成 → まず非表示化（UI構築中のちらつき防止）
        self.window = tk.Toplevel(parent)
        self.window.withdraw()
        self.window.title(title)
        # アイコンを resource_path 経由で読み込み
        self.window.iconbitmap(resource_path("ui/icons/event_icon.ico"))
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(False, False)

        # ウィンドウのサイズと中央配置
        w, h = 300, 270
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # 初期値を StringVar にセット
        self.title_var   = tk.StringVar(value=default_title)
        self.start_var   = tk.StringVar(value=default_start_time)
        self.end_var     = tk.StringVar(value=default_end_time)
        self.content_var = tk.StringVar(value=default_content)

        # UI 構築
        self._build_ui()

        # モーダル設定：親の上に表示 & 他操作をブロック
        self.window.transient(parent)
        self.window.grab_set()

        # 初期フォーカス
        self.ent_title.focus_set()
        # UI 完成後に表示
        self.window.deiconify()

    def _build_ui(self):
        """ダイアログ内のフレームと各入力セクションを配置"""
        pad = 8
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="both", expand=True, padx=pad, pady=pad)

        # 各セクション
        self._create_title_section(frame)
        self._create_time_section(frame)
        self._create_content_section(frame)
        self._create_button_section()

        # Esc キーで閉じる
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def _create_title_section(self, parent):
        """タイトル入力用のラベル+Combobox"""
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
            state="normal",   # 自由入力＋候補あり
            takefocus=True
        )
        self.ent_title.pack(fill="x", pady=(0, 8))

    def _create_time_section(self, parent):
        """開始・終了時間入力用のラベル＋Combobox（2つ並べる）"""
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
        """メモ用の Entry とプレースホルダー機能"""
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
            bg="#FAFAFA",  # 薄い背景
            fg="#888888"   # 初期文字色グレー
        )
        self.ent_content.pack(fill="x", pady=(0, 8))

        # プレースホルダー挿入
        self._add_placeholder(self.ent_content, "メモを入力")

    def _create_button_section(self, parent=None):
        """OK / キャンセル ボタン配置"""
        pad = 8
        btn_frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        btn_frame.pack(fill="x", padx=pad, pady=(0, pad))

        # OK ボタン（アクセントカラー：today）
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

        # キャンセル ボタン（目立つ赤系）
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

    def _add_placeholder(self, widget, placeholder):
        """Entry に簡易プレースホルダー機能を追加"""
        def on_focus_in(event):
            if widget.get() == placeholder:
                widget.delete(0, tk.END)
                widget.config(fg=ThemeManager.get("text"))
        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, placeholder)
                widget.config(fg="#888888")

        # 初期状態で placeholder を挿入
        if not widget.get():
            widget.insert(0, placeholder)

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)

    def on_ok(self):
        """OK 押下で StringVar から値を回収し、result に格納 → ウィンドウを閉じる"""
        self.result = (
            self.title_var.get(),
            self.start_var.get(),
            self.end_var.get(),
            self.content_var.get()
        )
        self.window.destroy()

    def add_button_hover(self, button, original_bg, hover_bg=None):
        """ボタンにホバー時の背景色変化を追加"""
        if hover_bg is None:
            hover_bg = COLORS["button_hover"]

        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=original_bg))

    def resource_path(relative_path):
        """PyInstaller 対応のリソース取得関数"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)