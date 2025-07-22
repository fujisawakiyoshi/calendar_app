# calendar_app/utils/resource.py

import os
import sys

def resource_path(relative_path: str) -> str:
    """
    開発中はリポジトリのルートから、
    PyInstaller 一発 exe 化後は _MEIPASS からリソースを参照します。
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # このファイルの一つ上 (calendar_app/calendar_app/) をルートとみなす
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, relative_path)
