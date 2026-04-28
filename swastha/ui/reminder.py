# ui/reminder.py
# eita medicine reminder screen er UI
# user medicine ar time add korbe, list dekhe delete korte parbe

import tkinter as tk
from tkinter import messagebox
from theme import COLORS, FONTS
from ui.components import make_button, make_scrollable_frame
from services.reminder_service import add_reminder, get_reminders, delete_reminder


class ReminderScreen:
    """
    Medicine reminder management screen.
    Reminder add, list, delete kora jay ekhane.
    """

    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.frame = tk.Frame(parent, bg=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):
        # page header
        header = tk.Frame(self.frame, bg=COLORS["accent_dark"], padx=25, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="⏰  Medicine Reminder",
            font=FONTS["heading"],
            bg=COLORS["accent_dark"],
            fg=COLORS["text_light"],
        ).pack(side="left")

        # main content
        main = tk.Frame(self.frame, bg=COLORS["bg_main"], padx=30, pady=20)
        main.pack(fill="both", expand=True)

        # ---- LEFT: Add form ----
        left = tk.Frame(main, bg=COLORS["bg_card"], padx=20, pady=20,
                        highlightthickness=1, highlightbackground=COLORS["border"])
        left.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(
            left,
            text="➕  Notun Reminder Add Korun",
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 15))

        # Medicine name
        tk.Label(left, text="Medicine Name:", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")

        self.medicine_entry = tk.Entry(
            left, font=FONTS["body"],
            bg=COLORS["bg_main"], fg=COLORS["text_primary"],
            relief="flat",
            highlightthickness=1, highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"],
            width=24, insertbackground=COLORS["text_primary"],
        )
        self.medicine_entry.pack(fill="x", ipady=7, pady=(3, 15))

        # Time input
        tk.Label(left, text="Somoy (HH:MM, 24-hr):", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")

        time_frame = tk.Frame(left, bg=COLORS["bg_card"])
        time_frame.pack(fill="x", pady=(3, 5))

        # hour ar minute alag alag input — easier input er jonno
        self.hour_var = tk.StringVar(value="08")
        self.min_var  = tk.StringVar(value="00")

        hour_spin = tk.Spinbox(
            time_frame,
            from_=0, to=23,
            textvariable=self.hour_var,
            format="%02.0f",
            width=4,
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        hour_spin.pack(side="left")

        tk.Label(time_frame, text=":", font=("Segoe UI", 16, "bold"),
                 bg=COLORS["bg_card"], fg=COLORS["text_primary"]).pack(side="left", padx=3)

        min_spin = tk.Spinbox(
            time_frame,
            from_=0, to=59,
            textvariable=self.min_var,
            format="%02.0f",
            width=4,
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        min_spin.pack(side="left")

        # message label
        self.msg_var = tk.StringVar()
        tk.Label(
            left,
            textvariable=self.msg_var,
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["danger"],
            wraplength=220,
        ).pack(pady=(10, 5))

        # Add button
        make_button(
            left,
            text="  ➕  Add Reminder  ",
            command=self._add,
        ).pack(fill="x", ipady=4, pady=(5, 0))

        # info note
        tk.Label(
            left,
            text="ℹ  Background e run kore,\napp open thakte hobe.",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
            justify="left",
        ).pack(anchor="w", pady=(12, 0))

        # ---- RIGHT: Reminder list ----
        right = tk.Frame(main, bg=COLORS["bg_main"])
        right.pack(side="left", fill="both", expand=True)

        header_row = tk.Frame(right, bg=COLORS["bg_main"])
        header_row.pack(fill="x", pady=(0, 10))

        tk.Label(
            header_row,
            text="📋  Apnar Sob Reminder",
            font=FONTS["subheading"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
        ).pack(side="left")

        # Refresh button
        tk.Button(
            header_row,
            text="🔄 Refresh",
            command=self._load_reminders,
            font=FONTS["small"],
            bg=COLORS["bg_main"],
            fg=COLORS["primary"],
            relief="flat",
            cursor="hand2",
        ).pack(side="right")

        self.list_scroll, self.list_frame = make_scrollable_frame(right)
        self.list_scroll.pack(fill="both", expand=True)

        # reminder list load kora hocche
        self._load_reminders()

    def _add(self):
        """Add button press e reminder database e add kore."""
        medicine = self.medicine_entry.get().strip()
        hour     = self.hour_var.get().zfill(2)
        minute   = self.min_var.get().zfill(2)
        time_str = f"{hour}:{minute}"

        if not medicine:
            self.msg_var.set("⚠  Medicine naam dite hobe!")
            return

        result = add_reminder(self.user["id"], medicine, time_str)

        if result["success"]:
            self.msg_var.set(f"✓  {result['message']}")
            self.medicine_entry.delete(0, tk.END)
            self._load_reminders()  # list refresh kora hocche
        else:
            self.msg_var.set(f"✗  {result['message']}")

    def _load_reminders(self):
        """Database theke reminders fetch kore list render kore."""
        # puranotো widgets clear koro
        for w in self.list_frame.winfo_children():
            w.destroy()

        reminders = get_reminders(self.user["id"])

        if not reminders:
            tk.Label(
                self.list_frame,
                text="📭  Kono reminder add kora nai ekhono.",
                font=FONTS["body"],
                bg=COLORS["bg_main"],
                fg=COLORS["text_muted"],
            ).pack(pady=30)
            return

        # protiটা reminder ekटা card hisebe show korbo
        for rem in reminders:
            self._render_reminder_card(rem)

    def _render_reminder_card(self, reminder):
        """Ekটা reminder card render kore."""
        card = tk.Frame(
            self.list_frame,
            bg=COLORS["bg_card"],
            padx=18,
            pady=12,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        card.pack(fill="x", pady=5)

        left = tk.Frame(card, bg=COLORS["bg_card"])
        left.pack(side="left", fill="both", expand=True)

        # medicine icon + name
        tk.Label(
            left,
            text=f"💊  {reminder['medicine_name']}",
            font=FONTS["body_bold"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w")

        # time — formatted e show hobe
        tk.Label(
            left,
            text=f"🕐  {reminder.get('reminder_time_fmt', reminder.get('raw_time', ''))}",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(3, 0))

        # Delete button
        del_btn = tk.Button(
            card,
            text="🗑 Delete",
            command=lambda r=reminder: self._delete(r),
            font=FONTS["small"],
            bg=COLORS["bg_main"],
            fg=COLORS["danger"],
            relief="flat",
            cursor="hand2",
            pady=5,
            padx=10,
        )
        del_btn.pack(side="right")

    def _delete(self, reminder):
        """Reminder delete confirmation er pore delete kore."""
        confirm = messagebox.askyesno(
            "Delete Reminder",
            f"'{reminder['medicine_name']}' reminder delete korben?",
        )
        if confirm:
            result = delete_reminder(reminder["id"])
            if result["success"]:
                self._load_reminders()
            else:
                messagebox.showerror("Error", result["message"])

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()