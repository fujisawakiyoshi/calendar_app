import tkinter as tk
from datetime import datetime

from utils.calendar_utils import generate_calendar_matrix
from ui.theme import COLORS, FONTS
from ui.tooltip import ToolTip

class CalendarView:
    """カレンダー表示用のUIコンポーネント。"""
    def __init__(self, parent, year, month, holidays, events,
                 on_date_click, on_prev, on_next):

        """parent (tk.Widget): 親フレーム。
        year (int): 表示する年。
        month (int): 表示する月。
        holidays (dict): 祝日データ（YYYY-MM-DD: 名前）。
        events (dict): イベントデータ（YYYY-MM-DD: [予定リスト]）。
        on_date_click (Callable): 日付クリック時のコールバック関数。
        on_prev (Callable): 前月ボタンのコールバック。
        on_next (Callable): 次月ボタンのコールバック。
        """
        self.parent = parent
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.on_date_click = on_date_click
        self.on_prev = on_prev
        self.on_next = on_next

        # カレンダー表示用フレーム
        self.frame = tk.Frame(self.parent, bg=COLORS["header_bg"])
        self.frame.pack(pady=10)

        # 最初に描画
        self.render()
    
    def render(self):
        """
        カレンダー全体の描画を行う。
        - ナビゲーション行（前月・次月ボタン）
        - 曜日ラベル
        - 日付マス
        """
        self.clear()
        self.draw_header()
        self.draw_weekday_labels()
        self.draw_days()

    def clear(self):
        """前回の描画内容（子ウィジェット）を削除する"""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def draw_header(self):
        """月移動用のナビゲーション（＜ 年月 ＞）を描画する"""
        prev_button = tk.Button(
            self.frame, text="＜", command=self.on_prev,
            bg = COLORS["header_bg"], 
            fg = COLORS["button_fg"],
            relief="flat", font=FONTS["button"]
        )
        prev_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.header_label = tk.Label(
            self.frame,
            text=f"{self.year}年 {self.month}月",
            font=FONTS["header"],
            bg = COLORS["header_bg"],
            fg = COLORS["button_fg"],
            padx=20, pady=8
        )
        self.header_label.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky="nsew")

        next_button = tk.Button(
            self.frame, text="＞", command = self.on_next,
            bg = COLORS["header_bg"],
            fg = COLORS["button_fg"],
            relief = "flat", font = FONTS["button"]
        )
        next_button.grid(row=0, column=6, sticky="w", padx=5, pady=5)

    def draw_weekday_labels(self):
        """曜日（日〜土）のラベルを描画する"""
        weekday_names = ["日", "月", "火", "水", "木", "金", "土"]
        for idx, day in enumerate(weekday_names):
            day_label = tk.Label(
                self.frame,
                text=day,
                borderwidth=0,
                relief="flat",
                width=6, height=2,
                font=FONTS["bold"],
                bg=COLORS["weekday_header_bg"],
                fg=COLORS["text"],
                padx=3, pady=3
            )
            day_label.grid(row=1, column=idx, padx=1, pady=1)

    def draw_days(self):
        """
        実際の日付セル（1〜31）を描画する。

        - 日付セルクリックでイベントダイアログを開く
        - ツールチップで予定を表示（存在する場合）
        """
        today = datetime.today()
        matrix = generate_calendar_matrix(self.year, self.month)

        for row_idx, week in enumerate(matrix, start=2):
            for col_idx, day in enumerate(week):
                text = "" if day == 0 else str(day)
                date_key = f"{self.year}-{self.month:02d}-{day:02d}"

                # 背景色の決定
                bg_color = self.get_day_cell_color(day, col_idx, date_key, today)

                label = tk.Label(
                    self.frame,
                    text=text,
                    borderwidth=1,
                    relief="ridge",
                    width=6,
                    height=2,
                    font=FONTS["base"],
                    bg=bg_color,
                   fg=COLORS["text"],
                    padx=3,
                    pady=3
                )

                if day != 0:
                    label.bind("<Button-1>", lambda e, selected_date = date_key: self.on_date_click(selected_date))
                    # --- ツールチップ追加（予定がある場合） ---
                    if date_key in self.events:
                        event_texts = []
                        for ev in self.events[date_key]:
                            title = ev.get("title", "")
                            start = ev.get("start_time", "")
                            end = ev.get("end_time", "")
                            content = ev.get("content", "")
                            event_texts.append(f"{title}（{start} - {end}）: {content}")
                        tip_text = "\n".join(event_texts)
                        ToolTip(label, tip_text)

                label.grid(row=row_idx, column=col_idx, padx=1, pady=1)
             
    def get_day_cell_color(self, day, col_idx, date_key, today):
        """日付セルの背景色を条件に応じて決定する。"""
        # 最優先: イベントあり ---
        if day == 0:
            return COLORS["default_bg"]
        # 今日
        if date_key in self.events:
            return COLORS["event"]
        # 祝日
        if (self.year == today.year and self.month == today.month and day == today.day):
            return COLORS["today"]
        # 土日
        if date_key in self.holidays:
            return COLORS["holiday"]
        if col_idx == 0:
            return COLORS["sunday"]
        if col_idx == 6:
            return COLORS["saturday"]
        # 通常
        return COLORS["default_bg"]



