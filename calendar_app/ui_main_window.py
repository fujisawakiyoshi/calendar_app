import tkinter as tk
from datetime import datetime
from calendar_renderer import generate_calendar_matrix
from holiday_service import load_holiday_cache
from event_manager import load_events
from tkinter import simpledialog, messagebox
from event_manager import save_events
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("カレンダーアプリ")
        self.root.geometry("400x400")
        self.holidays = load_holiday_cache()
        self.events = load_events()

        # 現在月
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month

        self.setup_ui()

    def setup_ui(self):
        # ヘッダー：前月・次月ボタン
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=10)

        prev_button = tk.Button(header_frame, text="＜ 前月", command=self.go_prev_month)
        prev_button.pack(side="left")

        self.header_label = tk.Label(header_frame, text=f"{self.current_year}年 {self.current_month}月")
        self.header_label.pack(side="left", padx=10)

        next_button = tk.Button(header_frame, text="次月 ＞", command=self.go_next_month)
        next_button.pack(side="left")

        # ⭐ 時刻ラベルを追加
        self.clock_label = tk.Label(self.root, font=("Arial", 12))
        self.clock_label.pack()

        # カレンダーフレーム
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.show_calendar()

        # 時刻更新を開始
        self.update_clock()

    def show_calendar(self):
        # カレンダークリア
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # 今日の日付情報
        today = datetime.today()
        today_year = today.year
        today_month = today.month
        today_day = today.day

        # 曜日ヘッダ
        days = ["日", "月", "火", "水", "木", "金", "土"]
        for idx, day in enumerate(days):
            label = tk.Label(self.calendar_frame, text=day, borderwidth=1, relief="solid", width=5)
            label.grid(row=0, column=idx)

        # カレンダー本体
        matrix = generate_calendar_matrix(self.current_year, self.current_month)
        for row_idx, week in enumerate(matrix, start=1):
            for col_idx, day in enumerate(week):
                text = "" if day == 0 else str(day)

                date_key = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                is_holiday = day != 0 and date_key in self.holidays
                has_event = day != 0 and date_key in self.events


                # デフォルト背景
                bg_color = "white"

                # 今日の日付をハイライト
                if (
                    day != 0
                    and self.current_year == today_year
                    and self.current_month == today_month
                    and day == today_day
                ):
                    bg_color = "lightblue"

                # 祝日は赤に
                if is_holiday:
                    bg_color = "pink"
                
                # 予定
                if has_event:
                    bg_color = "yellow"

                label = tk.Label(
                    self.calendar_frame,
                    text=text,
                    borderwidth=1,
                    relief="solid",
                    width=5,
                    height=2,
                    bg=bg_color
                )
                # ⭐ クリックイベントをバインド
                if day != 0:
                    label.bind("<Button-1>", lambda e, d=date_key: self.open_event_dialog(d))
                label.grid(row=row_idx, column=col_idx)

        # ヘッダー年月を更新
        self.header_label.config(text=f"{self.current_year}年 {self.current_month}月")

    def go_prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_calendar()

    def go_next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar()

    def open_event_dialog(self, date_key):
        window = tk.Toplevel(self.root)         #新しい小ウィンドウを開く       
        window.title(f"{date_key} の予定")

        # 既存予定
        events_list = self.events.get(date_key, [])

        tk.Label(window, text=f"{date_key} の予定一覧").pack(pady=5)

        listbox = tk.Listbox(window, width=40)  #Listboxで予定を一覧表示
        listbox.pack()

        for item in events_list:
            listbox.insert(tk.END, item)

        # 予定追加
        def add_event_action():
            new_event = simpledialog.askstring("予定追加", "新しい予定を入力してください") #追加ボタン
            if new_event:
                if date_key not in self.events:
                    self.events[date_key] = []
                self.events[date_key].append(new_event)
                save_events(self.events)
                listbox.insert(tk.END, new_event)
                self.show_calendar()

        add_button = tk.Button(window, text="予定を追加", command=add_event_action)
        add_button.pack(pady=5)

        # 予定削除
        def delete_event_action():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("警告", "削除する予定を選択してください")
                return

            index = selected[0]
            del self.events[date_key][index]
            if not self.events[date_key]:
                del self.events[date_key]
            save_events(self.events)
            listbox.delete(index)
            self.show_calendar()

        delete_button = tk.Button(window, text="選択した予定を削除", command=delete_event_action) #削除ボタン
        delete_button.pack(pady=5)

        window.transient(self.root)
        window.grab_set()
        window.wait_window()
        
    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=f"現在時刻: {now}")
        self.root.after(1000, self.update_clock)
    
    def run(self):
        self.root.mainloop()
