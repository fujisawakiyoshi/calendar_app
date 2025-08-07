# ui/weather_widget.py
import os
import tkinter as tk
from ui.theme import FONTS
from services.theme_manager import ThemeManager
from utils.resource import resource_path
from PIL import Image, ImageTk
import sys

class WeatherWidget:
    """
    天気情報（アイコン、概況）を表示するウィジェット
    """
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=ThemeManager.get('header_bg'))
        self.frame.pack(side="left", anchor="w", padx=(25, 0), pady=0)
        self.parent.config(bg=ThemeManager.get("weather_bg"))
        
        # アイコンを格納するフレーム
        self.icon_frame = tk.Frame(self.frame, bg=ThemeManager.get('header_bg'))
        self.icon_frame.pack(side="left", padx=(0, 3), anchor="w") #アイコンと文字との間隔
        self.icon_widgets = []
        
        # 天気概況用ラベル
        self.desc_label = tk.Label(
            self.frame,
            text="",
            font=FONTS['weather_text'],
            bg=ThemeManager.get('header_bg'),
            fg=ThemeManager.get('footer_fg'),
            anchor="w",
            justify="left",
            wraplength=180
        )
        self.desc_label.pack(side="left", anchor="w", padx=(0, 5), pady=0)
        
        self.icon_images = {}
        self._load_icons()
        
        self.update_theme()
    
    def _load_icons(self):
        icon_names = ["sun_icon.png", "cloudy_icon.png", "rain_icon.png", "snow_icon.png", "thunder_icon.png", "wind_icon.png"]
        for name in icon_names:
            try:
                img_path = resource_path(os.path.join("ui", "icons", name))
                img = Image.open(img_path)
                img = img.resize((24, 24), Image.LANCZOS)
                photo_img = ImageTk.PhotoImage(img)
                self.icon_images[name] = photo_img
            except Exception as e:
                print(f"[ERROR] アイコン画像の読み込みに失敗しました: {name} - {e}", file=sys.stderr)
        
        if not self.icon_images:
            self.icon_images["default"] = ImageTk.PhotoImage(Image.new('RGBA', (24, 24), (0, 0, 0, 0)))

    def update_weather(self, weather_info: dict | None):
        if weather_info:
            for widget in self.icon_widgets:
                widget.destroy()
            self.icon_widgets = []
            
            icon_files = weather_info.get("icon", ["sun_icon.png"])
            for icon_file in icon_files:
                photo_img = self.icon_images.get(icon_file, self.icon_images.get("default"))
                
                icon_label = tk.Label(
                    self.icon_frame,
                    image=photo_img,
                    bg=ThemeManager.get('header_bg')
                )
                icon_label.pack(side="left", padx=2)
                self.icon_widgets.append(icon_label)
            
            self.desc_label.config(text=weather_info.get("description", "情報なし"))
        else:
            for widget in self.icon_widgets:
                widget.destroy()
            self.icon_widgets = []
            self.desc_label.config(text="")

    def update_theme(self):
        bg = ThemeManager.get('weather_bg')
        fg = ThemeManager.get('footer_fg')
        
        self.frame.config(bg=bg)
        self.icon_frame.config(bg=bg)
        for widget in self.icon_widgets:
            widget.config(bg=bg)
        
        self.desc_label.config(bg=bg, fg=fg)
        
    def on_hover(self, event):
        self.parent.config(cursor="arrow")

    def on_leave(self, event):
        self.parent.config(cursor="")