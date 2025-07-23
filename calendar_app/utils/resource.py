# calendar_app/utils/resource.py

import os
import sys
import shutil

def resource_path(relative_path: str, writable: bool = False) -> str:
    """
    - 読み取り専用のリソースは PyInstaller の _MEIPASS またはローカルから取得。
    - 書き込み可能なファイル（JSONなど）はユーザーディレクトリに退避させる。
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    full_path = os.path.join(base, relative_path)

    if writable:
        # ユーザーのホームディレクトリに保存（例: C:\Users\あなた\.calendar_app\events.json）
        user_dir = os.path.join(os.path.expanduser("~"), ".calendar_app")
        os.makedirs(user_dir, exist_ok=True)

        dest_path = os.path.join(user_dir, os.path.basename(relative_path))

        if not os.path.exists(dest_path):
            try:
                shutil.copy(full_path, dest_path)
            except FileNotFoundError:
                # 開発初期など、元ファイルが存在しない場合は空ファイルを作成
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write("[]")  # 空のリストとして初期化（予定が空）

        return dest_path

    return full_path
