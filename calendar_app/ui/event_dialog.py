# ui/event_dialog.py

import tkinter as tk
from tkinter import messagebox
from services.event_manager import save_events
from ui.event_edit_dialog import EditDialog
from ui.theme import COLORS, FONTS
from ui.tooltip import ToolTip


class EventDialog:
    """指定された日付のイベント一覧を表示・編集するダイアログ"""
    def __init__(self, parent, date_key, events, on_update_callback):
        self.parent = parent
        self.date_key = date_key
        self.events = events
        self.on_update_callback = on_update_callback

        self.window = tk.Toplevel(self.parent)
        self.window.withdraw()  # 一旦非表示で構築
        self.window.title(f"予定一覧 {self.date_key}")
        self.window.iconbitmap("event_icon.ico")
        self.window.configure(bg=COLORS["dialog_bg"])
        self.window.resizable(True, False)

        # サイズ調整 & 中央表示
        w, h = 380, 260
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        self.build_ui()

        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.deiconify()  # UI構築後に表示

    def build_ui(self):
        self.create_header()
        self.create_listbox_area()
        self.create_button_area()
        self.bind_shortcuts()

    def create_header(self):
        tk.Label(
            self.window,
            text=f"予定一覧（{self.date_key}）",
            font=(FONTS["base"][0], 13, "bold"),
            bg=COLORS["header_bg"],
            fg=COLORS["text"],
            pady=6
        ).pack(fill="x")

    def create_listbox_area(self):
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="both", expand=True, padx=14, pady=8)

        self.listbox = tk.Listbox(
            frame, font=FONTS["base"], bg=COLORS["bg"], fg=COLORS["text"],
            bd=0, relief="flat", selectbackground="#CCE8FF", activestyle="none",
            height=6, width=35
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: self.edit_event())

        scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_list()

    def create_button_area(self):
        frame = tk.Frame(self.window, bg=COLORS["dialog_bg"])
        frame.pack(fill="x", padx=14, pady=(0, 14))

        self.add_icon = tk.PhotoImage(file="plus_insert_icon.png").subsample(3, 3)
        add_btn = tk.Button(
            frame, text="予定追加", image=self.add_icon, compound="right",
            command=self.add_event,
            font=FONTS["base"], bg=COLORS["today"], fg=COLORS["text"],
            relief="flat", padx=8, pady=4
        )
        add_btn.pack(side="left")
        ToolTip(add_btn, "新しい予定を追加")

        right_frame = tk.Frame(frame, bg=COLORS["dialog_bg"])
        right_frame.pack(side="right")

        self.edit_icon = tk.PhotoImage(file="notes_edit_icon.png").subsample(3, 3)
        edit_btn = tk.Button(
            right_frame, text="編集", image=self.edit_icon, compound="right",
            command=self.edit_event,
            font=FONTS["base"], bg="#FFE7C1", fg=COLORS["text"],
            relief="flat", padx=8, pady=4
        )
        edit_btn.pack(side="left", padx=4)
        ToolTip(edit_btn, "選択中の予定を編集")

        self.delete_icon = tk.PhotoImage(file="delete-trash_icon3.png").subsample(3, 3)
        del_btn = tk.Button(
            right_frame, text="削除", image=self.delete_icon, compound="right",
            command=self.delete_event,
            font=FONTS["base"], bg="#F7C6C7", activebackground="#F4B6B7",
            fg=COLORS["text"], relief="flat", padx=8, pady=4
        )
        del_btn.pack(side="left", padx=4)
        ToolTip(del_btn, "選択中の予定を削除")

    def bind_shortcuts(self):
        self.listbox.bind("<Return>", lambda e: self.edit_event())
        self.listbox.bind("<Delete>", lambda e: self.delete_event())
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for ev in self.events.get(self.date_key, []):
            item = f"{ev['start_time']}-{ev['end_time']}  {ev['title']}"
            if ev.get("memo"):
                item += f"  - {ev['memo']}"
            self.listbox.insert(tk.END, item)

    def add_event(self):
        dialog = EditDialog(self.window, "予定の追加")
        dialog.window.wait_window()  # ここでブロック
        if dialog.result:
            title, st, et, memo = dialog.result
            self.events.setdefault(self.date_key, []).append({
                "title": title, "start_time": st, "end_time": et, "memo": memo
            })
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()

    def edit_event(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("警告", "編集する予定を選択してください")
            return
        idx = sel[0]
        ev = self.events[self.date_key][idx]
        dialog = EditDialog(
            self.window, "予定の編集",
            default_title=ev["title"],
            default_start_time=ev["start_time"],
            default_end_time=ev["end_time"],
            default_content=ev.get("memo", "")
        )
        dialog.window.wait_window()
        if dialog.result:
            self.events[self.date_key][idx] = {
                "title": dialog.result[0],
                "start_time": dialog.result[1],
                "end_time": dialog.result[2],
                "memo": dialog.result[3]
            }
            save_events(self.events)
            self.refresh_list()
            self.on_update_callback()

    def delete_event(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("警告", "削除する予定を選択してください")
            return
        idx = sel[0]
        del self.events[self.date_key][idx]
        if not self.events[self.date_key]:
            del self.events[self.date_key]
        save_events(self.events)
        self.refresh_list()
        self.on_update_callback()
