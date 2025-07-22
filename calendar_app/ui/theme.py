
# 色
COLORS = {
    # 背景
    "bg": "#FFFFFF",
    "dialog_bg": "#FFFFFF",
    "header_bg": "#F7F7F7",

    # テキスト
    "text": "#333333",

    # 特殊背景
    "sunday": "#FADCD9",
    "saturday": "#DCEEF9",
    "holiday": "#F6CACA",
    "today": "#B7DCF5",
    "highlight": "#FFF4CC",
    "accent": "#FFC0CB",  # 祝日

    # ボタン
    "button_bg": "#FFFFFF",
    "button_fg": "#444444",
}


# 個別の定数
DIALOG_BG_COLOR = COLORS["dialog_bg"]
BUTTON_BG_COLOR = COLORS["button_bg"]
BUTTON_FG_COLOR = COLORS["button_fg"]

# フォント（Font Styles）
FONTS = {
    "base": ("游ゴシック", 12),
    "bold": ("游ゴシック", 12, "bold"),
    "small": ("游ゴシック", 10),
    "header": ("游ゴシック", 14, "bold"),
    "dialog_title": ("游ゴシック", 13, "bold"),
    "button": ("游ゴシック", 12)
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
