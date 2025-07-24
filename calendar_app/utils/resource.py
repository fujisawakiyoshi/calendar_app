import os
import sys
import shutil


def resource_path(relative_path: str, writable: bool = False) -> str:
    """
    ファイルパスを解決するユーティリティ関数。

    読み取り専用 → 開発環境 or PyInstallerの実行環境から取得  
    書き込み可能 → ユーザーのホームディレクトリ（~/.calendar_app）に保存

    Args:
        relative_path (str): 相対パス（例: "data/events.json"）
        writable (bool): 書き込み先として扱うか（Trueならユーザーディレクトリ）

    Returns:
        str: 実際のファイルパス
    """
    # PyInstallerでビルドされた場合の実行パス
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # 通常のスクリプト実行時：プロジェクトルートを基準とする
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    full_path = os.path.join(base, relative_path)

    if writable:
        # 書き込み用ディレクトリ（~/.calendar_app）にコピー・保存
        user_dir = os.path.join(os.path.expanduser("~"), ".calendar_app")
        os.makedirs(user_dir, exist_ok=True)

        dest_path = os.path.join(user_dir, os.path.basename(relative_path))

        if not os.path.exists(dest_path):
            try:
                shutil.copy(full_path, dest_path)  # 初期ファイルをコピー
            except FileNotFoundError:
                # コピー元がない場合は空ファイルを作成（開発初期など）
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write("[]")  # 空のリストとして初期化

        return dest_path

    return full_path
