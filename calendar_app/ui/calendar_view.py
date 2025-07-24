import tkinter as tk
from datetime import datetime
from utils.calendar_utils import generate_calendar_matrix
from ui.theme import COLORS, FONTS
from services.theme_manager import ThemeManager
from ui.tooltip import ToolTip


class CalendarView:
    """カレンダー表示用の UI コンポーネント"""

    def __init__(
        self,
        parent,
        year: int,
        month: int,
        holidays: dict,
        events: dict,
        on_date_click,
        on_prev,
        on_next
    ):
        self.parent = parent
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.on_date_click = on_date_click
        self.on_prev = on_prev
        self.on_next = on_next

        self.frame = tk.Frame(self.parent, bg=ThemeManager.get('bg'))
        self.frame.pack(padx=15, pady=15)

        self.render()

    def update(self, year, month, holidays, events):
        """年月・祝日・イベントを更新し再描画"""
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.render()

    def render(self):
        """カレンダー全体を描画（ヘッダー・曜日・日付）"""
        self._clear()
        self._draw_header()
        self._draw_weekday_labels()
        self._draw_days()

    def _clear(self):
        """ウィジェットをすべて破棄（再描画前の初期化）"""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def _draw_header(self):
        """年・月と前後ボタンを表示"""
        header = tk.Frame(self.frame, bg=ThemeManager.get('header_bg'))
        header.grid(row=0, column=0, columnspan=7, sticky='nsew')
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(3, weight=1)

        prev_btn = tk.Button(
            header,
            text='＜',
            command=self.on_prev,
            bg=ThemeManager.get('header_bg'),
            fg=ThemeManager.get('text'),
            relief='flat',
            font=FONTS['header'],
            width=3,
            cursor='hand2'
        )
        prev_btn.grid(row=0, column=0, padx=6, pady=6)
        self._add_button_hover(prev_btn, ThemeManager.get('header_bg'))

        tk.Label(
            header,
            text=f"{self.year}年 {self.month}月",
            font=FONTS['header'],
            bg=ThemeManager.get("header_bg"),
            fg=ThemeManager.get('text'),
            padx=12,
            pady=6
        ).grid(row=0, column=2, padx=6, pady=6)

        next_btn = tk.Button(
            header,
            text='＞',
            command=self.on_next,
            bg=ThemeManager.get('header_bg'),
            fg=ThemeManager.get('text'),
            relief='flat',
            font=FONTS['header'],
            width=3,
            cursor='hand2'
        )
        next_btn.grid(row=0, column=4, padx=6, pady=6)
        self._add_button_hover(next_btn, ThemeManager.get('header_bg'))

    def _draw_weekday_labels(self):
        """曜日（日〜土）を表示"""
        days = ['日', '月', '火', '水', '木', '金', '土']
        for idx, wd in enumerate(days):
            fg = '#9D5C64' if wd in ('日', '土') else ThemeManager.get('text')
            tk.Label(
                self.frame,
                text=wd,
                font=FONTS['base'],
                bg=ThemeManager.get('header_bg'),
                fg=fg,
                width=6,
                pady=4
            ).grid(row=1, column=idx, padx=1, pady=4)

    def _draw_days(self):
        """日付セルを描画（祝日・イベント・今日の表示含む）"""
        matrix = generate_calendar_matrix(self.year, self.month)

        for row_index, week in enumerate(matrix, start=2):
            for col_index, day in enumerate(week):
                if not day:
                    lbl = tk.Label(
                        self.frame,
                        text='',
                        bg=ThemeManager.get('bg'),
                        width=6,
                        height=2,
                        bd=1,
                        relief='ridge'
                    )
                    lbl.grid(row=row_index, column=col_index, padx=1, pady=1)
                    continue

                key = f"{self.year}-{self.month:02d}-{day:02d}"
                text = f"  {day} °" if self._is_today(day) else str(day)
                bg = self._get_day_bg(day, col_index, key)

                lbl = tk.Label(
                    self.frame,
                    text=text,
                    font=FONTS['base'],
                    bg=bg,
                    fg=ThemeManager.get('text'),
                    width=6,
                    height=2,
                    bd=1,
                    relief='ridge'
                )
                lbl.grid(row=row_index, column=col_index, padx=1, pady=1)

                lbl.bind('<Button-1>', lambda e, d=key: self.on_date_click(d))
                self._add_hover_effect(lbl, bg)

                if key in self.events:
                    ToolTip(lbl, self._make_event_summary(self.events[key]))

    def _get_day_bg(self, day, col, key) -> str:
        """日付セルの背景色を決定（優先順あり）"""
        if not day:
            return ThemeManager.get('bg')
        if key in self.events:
            return ThemeManager.get('highlight')
        if key in self.holidays:
            return ThemeManager.get('accent')
        if self._is_today(day):
            return ThemeManager.get('today')
        if col in (0, 6):
            return ThemeManager.get('weekend')
        return ThemeManager.get('bg')

    def _is_today(self, day) -> bool:
        """その日が今日かどうかを判定"""
        now = datetime.today()
        return now.year == self.year and now.month == self.month and now.day == day

    def _add_hover_effect(self, widget, orig_bg):
        """マウスホバー時に背景を変更"""
        hover_bg = '#D0EBFF'
        widget.bind('<Enter>', lambda e: widget.config(bg=hover_bg))
        widget.bind('<Leave>', lambda e: widget.config(bg=orig_bg))

    def _add_button_hover(self, button, orig_bg, hover_bg='#F0F0F0'):
        """前月・次月ボタンにホバー効果を付加"""
        button.bind('<Enter>', lambda e: button.config(bg=hover_bg))
        button.bind('<Leave>', lambda e: button.config(bg=orig_bg))

    def _make_event_summary(self, events_list) -> str:
        """イベント情報を整形してツールチップに表示"""
        lines = []
        for ev in events_list:
            times = f"{ev['start_time']}〜{ev['end_time']}"
            line = f"{times} {ev['title']}"
            if ev.get('memo'):
                line += f" - {ev['memo']}"
            lines.append(line)
        return '\n'.join(lines)
