import os
import sys
import shutil

def resource_path(relative_path: str, writable: bool = False) -> str:
    """
    リソースファイルのパスを解決する。

    読み取り専用ファイル（例: アイコン画像、テンプレートなど）は PyInstaller の _MEIPASS かローカルから取得。
    書き込み可能ファイル（例: JSONデータなど）はユーザーディレクトリ配下にコピー・退避させる。

    Args:
        relative_path (str): 相対パス（プロジェクト内でのリソース位置）
        writable (bool): 書き込みが必要なファイルかどうか（例: events.json）

    Returns:
        str: 解決されたファイルパス
    """
    # PyInstaller 実行時は _MEIPASS に展開される
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # 開発環境では現在のスクリプト位置から解決
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    full_path = os.path.join(base, relative_path)

    if writable:
        # 書き込み先はユーザーのホームディレクトリ配下（例: ~/.calendar_app/events.json）
        user_dir = os.path.join(os.path.expanduser("~"), ".calendar_app")
        os.makedirs(user_dir, exist_ok=True)

        dest_path = os.path.join(user_dir, os.path.basename(relative_path))

        # 初回はリソースからコピー、または空ファイルを作成
        if not os.path.exists(dest_path):
            try:
                shutil.copy(full_path, dest_path)
            except FileNotFoundError:
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write("[]")  # 空リストで初期化

        return dest_path

    return full_path
