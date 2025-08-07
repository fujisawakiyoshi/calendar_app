#ui/status_bar_widget.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import os
import sys

from ui.theme import FONTS
from services.theme_manager import ThemeManager
from utils.resource import resource_path


class StatusBarWidget:
    def __init__(self, parent, on_theme_toggle=None):
        self.parent = parent
        self.on_theme_toggle = on_theme_toggle

        # 色設定（統一）
        bg = ThemeManager.get("header_bg")
        fg = ThemeManager.get("text")
        clock_fg = ThemeManager.get("clock_fg")

        # === メインフレーム ===
        self.frame = tk.Frame(parent, bg=bg)
        self.frame.pack(fill="x", padx=10, pady=(0, 0))

        # === 左側: 天気表示 ===
        self.left_frame = tk.Frame(self.frame, bg=bg)
        self.left_frame.pack(side="left", anchor="w")

        self.icon_images = {}
        self.icon_widgets = []
        self.icon_frame = tk.Frame(self.left_frame, bg=bg)
        self.icon_frame.pack(side="left", padx=(0, 3), anchor="w")

        self.weather_label = tk.Label(
            self.left_frame,
            text="",
            font=FONTS["weather_text"],
            bg=bg,
            fg=fg,
            anchor="w",
            justify="left",
            wraplength=200
        )
        self.weather_label.pack(side="left", anchor="w")

        self._load_icons()

        # === 右側: 時計 + メッセージ ===
        self.right_frame = tk.Frame(self.frame, bg=bg)
        self.right_frame.pack(side="right", anchor="e")

        # メッセージラベル（時計の上）
        self.flash_label = tk.Label(
            self.right_frame,
            text="",
            font=("Segoe UI Emoji", 10, "italic"),
            bg=bg,
            fg=clock_fg,  # アクセントカラー（ピンク系）
            anchor="e",
            justify="right",
            wraplength=200
        )
        self.flash_label.pack(side="top", anchor="e", pady=(0, 2))

        # 時計（絵文字付き、テーマ切替ボタン）
        self.clock_btn = tk.Button(
            self.right_frame,
            text=self._get_time_str(),  # 🕒 をここで付けると2重になるので除去
            font=FONTS["small"],
            bg=bg,
            fg=clock_fg,
            cursor="hand2",
            relief="flat",  # 罫線なし
            bd=0,           # ボーダーサイズなし
            command=self._on_toggle_clicked  # ここだけでOK！
        )
        self.clock_btn.pack(side="top", anchor="e")

        # ホバー効果（色とカーソル変更）
        def _on_enter(e):
            self.clock_btn.config(fg=ThemeManager.get("clock_fg"), cursor="hand2")
        def _on_leave(e):
            self.clock_btn.config(fg=ThemeManager.get("clock_fg"))

        self.clock_btn.bind("<Enter>", _on_enter)
        self.clock_btn.bind("<Leave>", _on_leave)

        self._update_clock()

    def _load_icons(self):
        icon_names = [
            "sun_icon.png", "cloudy_icon.png", "rain_icon.png",
            "snow_icon.png", "thunder_icon.png", "wind_icon.png"
        ]
        for name in icon_names:
            try:
                img_path = resource_path(os.path.join("ui", "icons", name))
                img = Image.open(img_path).resize((24, 24), Image.LANCZOS)
                self.icon_images[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"[ERROR] アイコン読み込み失敗: {name} - {e}", file=sys.stderr)

        if not self.icon_images:
            self.icon_images["default"] = ImageTk.PhotoImage(
                Image.new("RGBA", (24, 24), (0, 0, 0, 0))
            )

    def _get_time_str(self):
        return "🕒 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _update_clock(self):
        self.clock_btn.config(text=self._get_time_str())
        self.clock_btn.after(1000, self._update_clock)

    def _on_toggle_clicked(self, event=None):
        if self.on_theme_toggle:
            self.on_theme_toggle()
        self.flash_message_for_seconds("₊✩‧₊かわいくなったよ〜💖₊✩‧₊", 3)

    def update_weather(self, weather_info: dict | None):
        # アイコン初期化
        for widget in self.icon_widgets:
            widget.destroy()
        self.icon_widgets.clear()

        if weather_info:
            icon_files = weather_info.get("icon", [])
            for icon_file in icon_files:
                img = self.icon_images.get(icon_file, self.icon_images.get("default"))
                lbl = tk.Label(self.icon_frame, image=img, bg=ThemeManager.get("footer_bg"))
                lbl.pack(side="left", padx=2)
                self.icon_widgets.append(lbl)

            self.weather_label.config(text=weather_info.get("description", "情報なし"))
        else:
            self.weather_label.config(text="")

    def set_flash_message(self, text):
        self.flash_label.config(text=text)

    def update_theme(self):
        bg = ThemeManager.get("header_bg")
        fg = ThemeManager.get("text")
        clock_fg = ThemeManager.get("clock_fg")

        for widget in [
            self.frame, self.left_frame, self.right_frame,
            self.icon_frame, self.weather_label,
            self.flash_label, self.clock_btn
        ]:
            widget.config(bg=bg)

        self.weather_label.config(fg=fg)
        self.flash_label.config(fg=clock_fg)
        self.clock_btn.config(
            fg=clock_fg, 
            activebackground=bg,
            activeforeground=clock_fg
        )

        for icon_widget in self.icon_widgets:
            icon_widget.config(bg=bg)
    
    def flash_message_for_seconds(self, message: str, seconds: int = 3):
        self.set_flash_message(message)
        self.frame.after(seconds * 1000, lambda: self.set_flash_message(""))
