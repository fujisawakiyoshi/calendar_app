import tkinter as tk
from datetime import datetime
from ui.theme import COLORS

class ClockWidget:
    """
    右下に現在時刻を表示するウィジェット。

    ・親ウィジェットにフィットするフレームを作成
    ・1秒ごとに時刻を更新
    """
    def __init__(self, parent):
        # ─── フレームの作成 ────────────────────────────
        # 背景色はヘッダーと合わせるか、デフォルトを使う
        bg_color = COLORS.get("header_bg", "#F9F9F9")
        self.frame = tk.Frame(parent, bg=bg_color)
        # 余白を詰めずに伸縮させる
        self.frame.pack(fill="both", expand=True)

        # ─── 時計ラベルの作成 ─────────────────────────
        # フォントは軽やかなセゴエUI、色は薄いグレー
        self.label = tk.Label(
            self.frame,
            text="",                # 初期テキストは空
            font=("Segoe UI", 11),  # フォントサイズ11pt
            bg=bg_color,            # フレームと同じ背景
            fg="#555555",           # 薄いグレー文字
            anchor="se",            # 右下寄せ
            padx=8,                 # 内側余白左右8px
            pady=5                  # 内側余白上下5px
        )
        # 右下にパディングを取りながら配置
        self.label.pack(anchor="se", padx=10, pady=8)

        # ─── 時刻更新ループ開始 ────────────────────────
        self._update_clock()

    def _update_clock(self):
        """
        ラベルに現在時刻を設定し、1秒後に再度自分を呼び出す。
        """
        # 現在日時をフォーマット
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # ラベルに日時をセット（先頭にアイコン＋スペース）
        self.label.config(text=f"🕒 {now_str}")
        # 1,000ミリ秒後に再実行
        self.label.after(1000, self._update_clock)
