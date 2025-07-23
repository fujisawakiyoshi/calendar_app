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
        on_date_click,  # 日付クリック時コールバック
        on_prev,        # 前月ボタンコールバック
        on_next         # 次月ボタンコールバック
    ):
        self.parent = parent
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.on_date_click = on_date_click
        self.on_prev = on_prev
        self.on_next = on_next

        # カレンダー全体を入れるフレームを作成
        self.frame = tk.Frame(self.parent, bg=ThemeManager.get('bg'))
        self.frame.pack(padx=15, pady=15)

        # 初回描画
        self.render()

    def update(self, year, month, holidays, events):
        """
        外部から年月・祝日・イベントを更新したいときに呼ぶ。
        再描画を行う。
        """
        self.year = year
        self.month = month
        self.holidays = holidays
        self.events = events
        self.render()

    def render(self):
        """ヘッダー／曜日ラベル／日付セルを再構築"""
        self._clear()
        self._draw_header()
        self._draw_weekday_labels()
        self._draw_days()

    def _clear(self):
        """前回描画したウィジェットをすべて破棄"""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def _draw_header(self):
        """年・月と前後移動ボタンを表示するヘッダーを作成"""
        header = tk.Frame(self.frame, bg=ThemeManager.get('header_bg'))
        header.grid(row=0, column=0, columnspan=7, sticky='nsew')

        # 両ボタンの間にスペース
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(3, weight=1)

        # 前月ボタン
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

        # 年月ラベル
        tk.Label(
            header,
            text=f"{self.year}年 {self.month}月",
            font=FONTS['header'],
            bg=COLORS['header_bg'],
            fg=COLORS['text'],
            padx=12,
            pady=6
        ).grid(row=0, column=2, padx=6, pady=6)

        # 次月ボタン
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
        """日～土の曜日ラベルを表示"""
        days = ['日', '月', '火', '水', '木', '金', '土']
        for idx, wd in enumerate(days):
            fg = COLORS['text']
            if wd in ('日', '土'):
                fg = '#9D5C64'  

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
        """各日付セルを生成し、イベントや祝日を反映"""
        matrix = generate_calendar_matrix(self.year, self.month)

        for row_index, week in enumerate(matrix, start=2):
            for col_index, day in enumerate(week):
                if not day:
                    text, key = '', None
                else:
                    key = f"{self.year}-{self.month:02d}-{day:02d}"
                    # 今日を強調
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

                if day:
                    # クリック時の挙動設定
                    lbl.bind('<Button-1>', lambda e, d=key: self.on_date_click(d))
                    # ホバー時の背景変化
                    self._add_hover_effect(lbl, bg)
                    # イベントがある日はツールチップ表示
                    if key in self.events:
                        tip_text = self._make_event_summary(self.events[key])
                        ToolTip(lbl, tip_text)

    def _get_day_bg(self, day, col, key) -> str:
        """
        日付セルの背景色を決定。
        優先度：空セル → イベント → 祝日 → 今日 → 日曜 → 土曜 → 通常
        """
        if not day:
            return ThemeManager.get('bg')
        if key in self.events:
            return ThemeManager.get('highlight')
        if key in self.holidays:
            return ThemeManager.get('accent')
        if self._is_today(day):
            return ThemeManager.get('today')
        if col in (0, 6):  # 土日どちらも
            return ThemeManager.get('weekend')
        return ThemeManager.get('bg')

    def _is_today(self, day) -> bool:
        """指定した日付が「今日」であるかを判定"""
        now = datetime.today()
        return (
            now.year == self.year and
            now.month == self.month and
            now.day == day
        )

    def _add_hover_effect(self, widget, orig_bg):
        """日付セルにマウスホバーで背景色を変える効果を追加"""
        hover_bg = '#D0EBFF'
        widget.bind('<Enter>', lambda e: widget.config(bg=hover_bg))
        widget.bind('<Leave>', lambda e: widget.config(bg=orig_bg))

    def _add_button_hover(self, button, orig_bg, hover_bg='#F0F0F0'):
        """ナビゲーションボタンにホバー効果を追加"""
        button.bind('<Enter>', lambda e: button.config(bg=hover_bg))
        button.bind('<Leave>', lambda e: button.config(bg=orig_bg))

    def _make_event_summary(self, events_list) -> str:
        """
        ツールチップ用に、複数イベントを「時刻〜タイトル（メモ）」形式で整形
        改行区切りで返す
        """
        lines = []
        for ev in events_list:
            times = f"{ev['start_time']}〜{ev['end_time']}"
            line = f"{times} {ev['title']}"
            if ev.get('memo'):
                line += f" - {ev['memo']}"
            lines.append(line)
        return '\n'.join(lines)
