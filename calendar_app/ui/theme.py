# ui/theme.py

# ──────────────────────────────
# 色設定（テーマに使用）
# ──────────────────────────────

# 共通カラー（旧定義／現在未使用の場合あり）
COLORS = {
    "bg":           "#FFFFFF",  # メイン背景
    "dialog_bg":    "#FFFFFF",  # ダイアログ背景
    "header_bg":    "#FAFAFA",  # ヘッダー背景
    "text":         "#333333",  # 標準テキスト
    "weekend":      "#FFC1DA",  # 土日背景
    "sunday":       "#FADCD9",  # 日曜
    "saturday":     "#DCEEF9",  # 土曜
    "holiday":      "#F6CACA",  # 祝日（旧設定）
    "today":        "#B7DCF5",  # 今日セルの色
    "highlight":    "#FFF4CC",  # イベント付き日
    "accent":       "#FFC0CB",  # 強調色（祝日など）
    "button_bg":    "#FFFFFF",
    "button_fg":    "#444444",
    "button_hover": "#F0F0F0",
}

# ──────────────────────────────
# ライトテーマ定義
# ──────────────────────────────
LIGHT_THEME = {
    "bg": "#FFFFFF",                  # 全体背景
    "dialog_bg": "#FFFFFF",          # ダイアログ背景
    "header_bg": "#FAFAFA",          # ヘッダー背景
    "text": "#333333",               # 文字色
    "weekend": "#FFC1DA",            # 土日
    "today": "#B7DCF5",              # 今日
    "highlight": "#FFF4CC",          # イベントあり
    "accent": "#FFC0CB",             # 強調セル
    "button_bg": "#FFFFFF",
    "button_fg": "#444444",
    "button_hover": "#F0F0F0",
    "button_bg_add": "#B7DCF5",      # 追加ボタン
    "button_bg_edit": "#FFE7C1",     # 編集ボタン
    "button_bg_delete": "#F7C6C7",   # 削除ボタン
    "clock_fg": "#555555"            # 時計テキスト
}

# ──────────────────────────────
# ダークテーマ定義（かわいい系配色）
# ──────────────────────────────
DARK_THEME = {
    "bg": "#FFF7F9",                # ベース背景（ピンク系）
    "header_bg": "#FEEEF3",
    "dialog_bg": "#FFF7F9",
    "text": "#7D4B6C",              # ローズブラウン
    "weekend": "#FADAE1",
    "sunday": "#FFD1DC",
    "saturday": "#D5F5F6",
    "holiday": "#FFD3E0",
    "today": "#FBD0D9",
    "highlight": "#FFF4CC",
    "accent": "#FFC1E3",
    "button_bg": "#FFF0F5",
    "button_fg": "#7D4B6C",
    "button_hover": "#FFE4EC",
    "button_bg_add": "#FFD6F0",
    "button_bg_edit": "#FFECB3",
    "button_bg_delete": "#FFCDD2",
    "clock_fg": "#AA77AA"
}

# 現在のテーマ（初期値はライト）
COLORS = LIGHT_THEME

# ──────────────────────────────
# フォント定義（サイズ・太字など）
# ──────────────────────────────
FONTS = {
    "base":         ("Helvetica", 12),            # 標準テキスト
    "base_minus":   ("Helvetica", 11),            # やや小さめ
    "bold":         ("Helvetica", 12, "bold"),    # 太字
    "small":        ("Helvetica", 10),            # ラベルなど補助用
    "header":       ("Helvetica", 14, "bold"),    # カレンダーの年月表示
    "dialog_title": ("Helvetica", 13, "bold"),    # ダイアログのタイトル
    "button":       ("Helvetica", 12),            # ボタン文字
}

# ──────────────────────────────
# イベントタイトルの選択肢
# ──────────────────────────────
TITLE_CHOICES = [
    "会議/打合せ", "来客", "外出", "出張", "休暇", "私用", "その他"
]

# ──────────────────────────────
# 時間選択肢（07:00〜21:30まで30分刻み）
# ──────────────────────────────
TIME_CHOICES = [
    f"{h:02d}:{m:02d}"
    for h in range(7, 22)  # 7時〜21時
    for m in (0, 30)       # 00分・30分
]
