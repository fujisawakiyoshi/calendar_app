# C:\work_202507\calendar_app\tests\test_event_edit_dialog.py

import pytest
import tkinter as tk
from tkinter import ttk # ttk.Combobox をモックするため
from unittest.mock import MagicMock, patch

# テスト対象のクラスと依存モジュールをインポート
from ui.event_edit_dialog import EditDialog
from ui.theme import COLORS, FONTS, TITLE_CHOICES, TIME_CHOICES # 定数が必要な場合
from services.theme_manager import ThemeManager # ThemeManager をモックするため
from utils.resource import resource_path # resource_path をモックするため


# UT-17: EditDialog のデータ取得
def test_edit_dialog_data_acquisition(mocker):
    """
    EditDialog がユーザー入力（タイトル、時間、内容）を正しく取得し、
    result 属性に格納することを確認する。
    """
    # --- 準備 ---
    # Tkinter のルートウィンドウや Toplevel をモックし、GUIが表示されないようにする
    mocker.patch('tkinter.Toplevel')
    mocker.patch.object(tk, 'Label')
    mocker.patch.object(tk, 'Frame')
    mocker.patch.object(tk, 'Button')
    mocker.patch.object(ttk, 'Combobox') # ttk.Combobox をモック

    # EditDialogが依存する ThemeManager, resource_path をモック
    mocker.patch('services.theme_manager.ThemeManager.get', return_value='mock_color')
    mocker.patch('utils.resource.resource_path', return_value='mocked_icon_path')

    # EditDialog の __init__ が tk.StringVar を使うため、これもモックする
    # MagicMock は属性へのアクセスも記録できるので、ここでは tk.StringVar を直接モックしない

    # --- テスト実行 ---
    # EditDialog のインスタンスを生成（親はモックでOK）
    dialog = EditDialog(
        parent=MagicMock(),
        title="テストダイアログ",
        default_title="デフォルトタイトル",
        default_start_time="09:00",
        default_end_time="10:00",
        default_content="デフォルト内容"
    )

    # ユーザーが入力したかのように値を設定する
    # EditDialog 内の StringVar に直接値を設定することで、ユーザー入力をシミュレート
    dialog.title_var.set("新しいタイトル")
    dialog.start_var.set("11:00")
    dialog.end_var.set("12:00")
    dialog.content_var.set("新しい内容")

    # OKボタンがクリックされたことをシミュレートするために、
    # EditDialog の ok_clicked メソッド（存在すると仮定）を呼び出すか、
    # あるいは直接 dialog.result に値をセットするロジックをテストする。
    # EditDialog の __init__ で build_ui が呼ばれ、その中でボタンが作成されるはず。
    # EditDialog が OK ボタンを押したときに self.result にタプルを設定するロジックをテスト。

    # EditDialog の build_ui() が呼ばれた後、ok_clicked() が呼ばれることを想定
    # OKボタンのコマンド関数を直接呼び出すか、
    # あるいは EditDialog 内で self.result に設定されるロジックを直接実行します。

    # EditDialog の ok_clicked メソッドが result をセットする想定
    # (EditDialog に ok_clicked メソッドがあることを前提とする)
    # もし `ok_clicked` メソッドが存在しなければ、`EditDialog` クラスにそれを追加してください。
    # 例:
    # def ok_clicked(self):
    #     self.result = (self.title_var.get(), self.start_var.get(), self.end_var.get(), self.content_var.get())
    #     self.window.destroy()

    dialog.ok_clicked() # OKボタンがクリックされたことをシミュレート

    # --- 検証 ---
    expected_result = ("新しいタイトル", "11:00", "12:00", "新しい内容")
    assert dialog.result == expected_result

    # キャンセル時のテスト（オプション）
    dialog_cancel = EditDialog(parent=MagicMock(), title="キャンセルテスト")
    # キャンセルボタンがクリックされたことをシミュレート
    # (EditDialog に cancel_clicked メソッドがあることを前提とする)
    # 例:
    # def cancel_clicked(self):
    #     self.result = None
    #     self.window.destroy()
    dialog_cancel.cancel_clicked() # キャンセルボタンがクリックされたことをシミュレート
    assert dialog_cancel.result is None