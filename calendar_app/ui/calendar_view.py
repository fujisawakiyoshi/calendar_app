import tkinter as tk
from datetime import datetime

from utils.calendar_utils import generate_calendar_matrix
from ui.theme import COLORS, FONTS
from ui.tooltip import ToolTip


class CalendarView:
    """カレンダー表示用のUIコンポーネント。"""
    def __init__(
        self, parent,
        year, month,            # 表示対象の年と月
        holidays, events,       # 祝日データとイベントデータ
        on_date_click,          # 日付クリック時のコールバック
        on_prev, on_next        # 前月／次月ボタンのコールバック
    ):
        self.parent = parent
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.on_date_click = on_date_click
        self.on_prev = on_prev
        self.on_next = on_next

        # カレンダー全体を表示するフレームを作成
        self.frame = tk.Frame(self.parent, bg=COLORS['bg'])
        self.frame.pack(pady=10)

        # 初回描画
        self.render()

    def update(self, year, month, holidays, events):
        """外部からの更新要求に応じてカレンダー内容を再描画"""
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.render()

    def render(self):
        """ヘッダー・曜日ラベル・日付セルを再構築"""
        self.clear()
        self.draw_header()
        self.draw_weekday_labels()
        self.draw_days()

    def clear(self):
        """フレーム内の全ウィジェットを削除"""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def draw_header(self):
        """年・月表示と前後移動ボタンを配置するヘッダー"""
        header = tk.Frame(self.frame, bg=COLORS['header_bg'])
        header.grid(row=0, column=0, columnspan=7, sticky='nsew')

        # ボタン間のスペースを確保
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(3, weight=1)

        # 前月ボタン
        tk.Button(
            header, text='＜', command=self.on_prev,
            bg=COLORS['header_bg'], fg=COLORS['text'], relief='flat',
            font=FONTS['header'], width=3
        ).grid(row=0, column=0, padx=6, pady=6)

        # 年月ラベル
        tk.Label(
            header, text=f"{self.year}年 {self.month}月",
            font=FONTS['header'], bg=COLORS['header_bg'], fg=COLORS['text'],
            bd=0, padx=12, pady=6
        ).grid(row=0, column=2, padx=6, pady=6)

        # 翌月ボタン
        tk.Button(
            header, text='＞', command=self.on_next,
            bg=COLORS['header_bg'], fg=COLORS['text'], relief='flat',
            font=FONTS['header'], width=3
        ).grid(row=0, column=4, padx=6, pady=6)

    def draw_weekday_labels(self):
        """曜日名（日～土）を表示"""
        labels = ['日', '月', '火', '水', '木', '金', '土']
        for idx, wd in enumerate(labels):
            color = COLORS['text']
            if wd == '日': color = '#D14'  # 日曜は赤みを強調
            if wd == '土': color = '#449'  # 土曜は青みを強調

            tk.Label(
                self.frame, text=wd, font=FONTS['base'],
                bg=COLORS['header_bg'], fg=color,
                width=6, pady=4, bd=0
            ).grid(row=1, column=idx, padx=4, pady=4)

    def draw_days(self):
        """日付セルを生成し、イベントや祝日を反映"""
        matrix = generate_calendar_matrix(self.year, self.month)

        for row, week in enumerate(matrix, start=2):
            for col, day in enumerate(week):
                text = str(day) if day else ''
                key = f"{self.year}-{self.month:02d}-{day:02d}" if day else None

                # 背景色の決定
                bg = self.get_day_background(day, col, key)

                lbl = tk.Label(
                    self.frame, text=text, font=FONTS['base'],
                    bg=bg, fg=COLORS['text'],
                    width=6, height=2, bd=1, relief='ridge'
                )
                lbl.grid(row=row, column=col, padx=1, pady=1)

                if day:
                    # クリックでイベントダイアログを開く
                    lbl.bind('<Button-1>', lambda e, d=key: self.on_date_click(d))

                    # ホバーで色変化
                    self.add_hover_effect(lbl, bg)

                    # イベントがある日のみツールチップ追加
                    if key in self.events:
                        tip = self.generate_event_summary(self.events[key])
                        ToolTip(lbl, tip)

    def get_day_background(self, day, col, key):
        """日セルの背景色を優先順位に従い返す"""
        if not day:
            return COLORS['bg']
        if key in self.events:
            return COLORS['highlight']
        if key in self.holidays:
            return COLORS['accent']
        if self.is_today(day):
            return COLORS['today']
        if col == 0:
            return COLORS['sunday']
        if col == 6:
            return COLORS['saturday']
        return COLORS['bg']

    def is_today(self, day):
        """日付が本日かどうか判定"""
        now = datetime.today()
        return day == now.day and self.month == now.month and self.year == now.year

    def add_hover_effect(self, widget, orig_bg):
        """ホバー時に背景色を変える"""
        hover_bg = '#D0EBFF'
        widget.bind('<Enter>', lambda e: widget.config(bg=hover_bg))
        widget.bind('<Leave>', lambda e: widget.config(bg=orig_bg))

    def generate_event_summary(self, events):
        """イベントリストをツールチップ用テキストに変換"""
        lines = []
        for ev in events:
            rng = f"{ev['start_time']}〜{ev['end_time']}"
            line = f"{rng} {ev['title']}"
            if ev.get('memo'):
                line += f" - {ev['memo']}"
            lines.append(line)
        return '\n'.join(lines)
