import tkinter as tk
from datetime import datetime
from services.theme_manager import ThemeManager

class ClockWidget:
    """
    アプリ画面の右下に表示される時計ウィジェット。
    時計としての機能に加え、クリックでテーマ切り替えも行える。
    """

    def __init__(self, parent, on_theme_toggle=None):
        """
        初期化メソッド。

        Args:
            parent (tk.Widget): 親ウィジェット
            on_theme_toggle (Callable): テーマ切替時に呼び出されるコールバック関数
        """
        self.parent = parent
        self.on_theme_toggle = on_theme_toggle

        # フレームの作成（背景色はテーマに応じて設定）
        self.frame = tk.Frame(parent, bg=ThemeManager.get("header_bg"))
        self.frame.pack(fill="both", expand=True)

        # 「かわいくなったよ〜💖」と表示するラベル（初期状態は非表示）
        self.flash_label = tk.Label(
            self.frame,
            text="₊✩‧₊かわいくなったよ〜💖₊✩‧₊",
            font=("Helvetica", 9, "italic"),
            bg=ThemeManager.get("header_bg"),
            fg=ThemeManager.get("clock_fg", "#555")
        )
        self.flash_label.place_forget()

        # 時計ボタン（テキストが毎秒更新される）
        self.clock_btn = tk.Button(
            self.frame,
            text="",
            font=("Segoe UI", 11),
            bg=ThemeManager.get("header_bg"),
            fg=ThemeManager.get("clock_fg", "#555"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=ThemeManager.get("header_bg"),
            activeforeground=ThemeManager.get("clock_fg", "#555"),
            command=self._on_toggle_clicked
        )
        self.clock_btn.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        # マウスホバー時に色を変える
        self.clock_btn.bind("<Enter>", lambda e: self.clock_btn.config(fg="#AA77AA"))
        self.clock_btn.bind("<Leave>", lambda e: self.update_theme())

        # 時計の初回更新を開始（以後1秒ごとに自動更新）
        self._update_clock()

    def _update_clock(self):
        """
        現在時刻を取得し、ボタンのテキストに反映。
        この処理は毎秒呼び出される。
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_btn.config(text=f"🕒 {now_str}")
        self.clock_btn.after(1000, self._update_clock)

    def _on_toggle_clicked(self):
        """
        時計ボタンがクリックされたときの処理。
        テーマを切り替え、必要ならメッセージを表示。
        """
        if self.on_theme_toggle:
            self.on_theme_toggle()
            if ThemeManager.is_dark_mode():
                self._show_flash_message()
        self.update_theme()

    def update_theme(self):
        """
        現在のテーマに応じてウィジェットの色を更新。
        """
        bg = ThemeManager.get("header_bg")
        fg = ThemeManager.get("clock_fg", "#555")

        self.frame.config(bg=bg)
        self.clock_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=fg)
        self.flash_label.config(bg=bg, fg=fg)

    def _show_flash_message(self):
        """
        ダークモードに切り替えたとき、一時的にメッセージを表示。
        """
        self.flash_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-40)
        self.flash_label.lift()  # ラベルを最前面に
        self.frame.after(4000, self.flash_label.place_forget)  # 4秒後に非表示
