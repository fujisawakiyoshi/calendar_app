import tkinter as tk

# 色コード定義（上品ペールカラー統一テーマ）
DIALOG_BG_COLOR = "#FFFFFF"
DIALOG_HEADER_BG = "#CFE9D6"
BUTTON_BG_COLOR = "#FFFFFF"
BUTTON_FG_COLOR = "#444444"
ENTRY_BORDER_COLOR = "#CCCCCC"

class EditDialog:
    def __init__(self, parent, title, default_title="", default_time="", default_content=""):
        self.result = None
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.configure(bg=DIALOG_BG_COLOR)
        self.window.resizable(False, False)

        self.create_widgets(title, default_title, default_time, default_content)
        self.window.transient(parent)
        self.window.grab_set()
        self.window.wait_window()

    def create_widgets(self, header_text, default_title, default_time, default_content):

        # -------------------- フォーム --------------------
        form_frame = tk.Frame(self.window, bg=DIALOG_BG_COLOR)
        form_frame.pack(padx=20, pady=10)

        # タイトル
        tk.Label(form_frame, text="タイトルを入力してください", bg=DIALOG_BG_COLOR, fg=BUTTON_FG_COLOR,
                 font=("Arial", 11)).pack(anchor="w", pady=(5, 0))
        self.title_entry = tk.Entry(form_frame, font=("Arial", 11), relief="ridge", bd=1)
        self.title_entry.insert(0, default_title)
        self.title_entry.pack(fill="x", pady=5)

        # 時間
        tk.Label(form_frame, text="時間を入力してください", bg=DIALOG_BG_COLOR, fg=BUTTON_FG_COLOR,
                 font=("Arial", 11)).pack(anchor="w", pady=(5, 0))
        self.time_entry = tk.Entry(form_frame, font=("Arial", 11), relief="ridge", bd=1)
        self.time_entry.insert(0, default_time)
        self.time_entry.pack(fill="x", pady=5)

        # 内容
        tk.Label(form_frame, text="内容を入力してください", bg=DIALOG_BG_COLOR, fg=BUTTON_FG_COLOR,
                 font=("Arial", 11)).pack(anchor="w", pady=(5, 0))
        self.content_entry = tk.Entry(form_frame, font=("Arial", 11), relief="ridge", bd=1)
        self.content_entry.insert(0, default_content)
        self.content_entry.pack(fill="x", pady=5)

        # -------------------- ボタン --------------------
        button_frame = tk.Frame(self.window, bg=DIALOG_BG_COLOR)
        button_frame.pack(pady=10)

        ok_button = tk.Button(
            button_frame,
            text="OK",
            command=self.on_ok,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11),
            width=10
        )
        ok_button.pack(side="left", padx=10)

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            relief="flat",
            font=("Arial", 11),
            width=10
        )
        cancel_button.pack(side="left", padx=10)

    def on_ok(self):
        self.result = (
            self.title_entry.get(),
            self.time_entry.get(),
            self.content_entry.get()
        )
        self.window.destroy()
