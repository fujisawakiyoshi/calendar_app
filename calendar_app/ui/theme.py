
# 色
COLORS = {
    "default_bg": "#FFFFFF",
    "header_bg": "#F7F7F7",
    "weekday_header_bg": "#EAF6ED",
    "text": "#333333",
    "sunday": "#FADCD9",
    "saturday": "#DCEEF9",
    "holiday": "#F6CACA",
    "today": "#C8E4F7",
    "event": "#FFF4CC",
    "button_bg": "#FFFFFF",
    "button_fg": "#444444",
    "dialog_bg": "#FFFFFF",
    "dialog_section_bg": "#EAF6ED",
    "highlight": "#FFF4CC",
    "accent": "#C8E4F7",
    "bg": "#FFFFFF",
    
}

# 個別の定数
DIALOG_BG_COLOR = COLORS["dialog_bg"]
BUTTON_BG_COLOR = COLORS["button_bg"]
BUTTON_FG_COLOR = COLORS["button_fg"]

# フォント（Font Styles）
FONTS = {
    "base": ("Arial", 11),
    "bold": ("Arial", 11, "bold"),
    "header": ("Arial", 14, "bold"),
    "dialog_title": ("Arial", 13, "bold"),
    "button": ("Arial", 12),
    "header": ("游ゴシック", 14, "bold"),
    "base":   ("游ゴシック", 12),
    "small":  ("游ゴシック", 10),
}

# 定数リスト（選択肢）
TITLE_CHOICES = [
    "会議/打合せ", "来客", "外出", "出張", "休暇", "私用", "その他"
]

TIME_CHOICES = [
    f"{h:02d}:{m:02d}"
    for h in range(7, 22)
    for m in (0, 30)
]
