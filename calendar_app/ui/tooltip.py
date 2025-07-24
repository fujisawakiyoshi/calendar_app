import tkinter as tk

class ToolTip:
    """
    任意の Tkinter ウィジェットにマウスホバー時のツールチップ（吹き出し）を表示するクラス。
    """

    def __init__(self, widget: tk.Widget, text: str):
        """
        初期化メソッド。

        Args:
            widget (tk.Widget): ツールチップを表示する対象ウィジェット
            text (str): ツールチップに表示する文字列
        """
        self.widget = widget
        self.text = text
        self.tip_window = None  # ツールチップ表示用の小ウィンドウ

        # ウィジェットにマウスイベントを関連付け
        widget.bind("<Enter>", self.show_tip)  # マウスが乗った時に表示
        widget.bind("<Leave>", self.hide_tip)  # マウスが離れた時に非表示

    def show_tip(self, event=None):
        """
        ツールチップを表示する処理。
        表示位置はウィジェットのキャレット位置から算出。
        """
        if self.tip_window or not self.text:
            return  # すでに表示されている、または空文字の場合は無視

        # ウィジェット内の相対座標（キャレット）を取得
        x, y, _, cy = self.widget.bbox("insert") or (0, 0, 0, 0)

        # 実際の画面位置（スクリーン座標）に変換し、表示位置を少しずらす
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + cy + 10

        # 枠なしの小ウィンドウ（Toplevel）を作成
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # 枠やタイトルバーを消す
        tw.wm_geometry(f"+{x}+{y}")   # 表示位置を設定

        # ラベルでテキストを表示
        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",  # 淡い黄色の背景
            relief="solid",
            borderwidth=1,
            font=("Arial", 10)
        )
        label.pack(ipadx=4, ipady=2)

    def hide_tip(self, event=None):
        """
        ツールチップを非表示にする処理。
        """
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
