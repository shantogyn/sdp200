"""
Medicine Reminder Page
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, styled_button


class ReminderPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self.parent, bg=COLORS["orange"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="⏰ Medicine Reminder System",
                 font=FONTS["title"], bg=COLORS["orange"], fg="white"
                 ).place(relx=0.02, rely=0.5, anchor="w")

        main = tk.Frame(self.parent, bg=COLORS["bg"])
        main.pack(fill="both", expand=True)

        # Left: add form
        left = tk.Frame(main, bg=COLORS["bg"], width=350)
        left.pack(side="left", fill="y", padx=16, pady=16)
        left.pack_propagate(False)
        self._build_form(left)

        # Right: reminders list
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="right", fill="both", expand=True, padx=16, pady=16)
        self._build_list(right)

    def _build_form(self, parent):
        card = tk.Frame(parent, bg="white")
        card.pack(fill="x")
        inner = tk.Frame(card, bg="white")
        inner.pack(padx=16, pady=16, fill="x")

        tk.Label(inner, text="➕ Add New Reminder",
                 font=FONTS["heading"], bg="white", fg=COLORS["orange"]
                 ).pack(anchor="w", pady=(0, 12))

        fields = [
            ("💊 Medicine Name *", "med_entry"),
            ("🕐 Time (HH:MM) *", "time_entry"),
            ("📏 Dosage", "dose_entry"),
            ("📝 Notes", "notes_entry"),
        ]

        for label, attr in fields:
            tk.Label(inner, text=label, font=FONTS["small"],
                     bg="white", fg=COLORS["text_lt"]).pack(anchor="w", pady=(6, 2))
            entry = tk.Entry(inner, font=FONTS["body"], relief="solid",
                             bd=1, bg="white", fg=COLORS["text"], insertbackground=COLORS["text"])
            entry.pack(fill="x", ipady=6)
            setattr(self, attr, entry)

        # Placeholder hints
        self.time_entry.insert(0, "e.g. 08:30")
        self.time_entry.config(fg="#AAAAAA")
        self.time_entry.bind("<FocusIn>", lambda e: self._clear_placeholder(self.time_entry, "e.g. 08:30"))
        self.time_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(self.time_entry, "e.g. 08:30"))

        styled_button(inner, "💾 Save Reminder", self._save,
                      color=COLORS["orange"], width=20).pack(fill="x", pady=(16, 0))

        # Info
        tk.Label(
            inner,
            text="ℹ️ The app checks reminders every 30 seconds\nand shows a popup notification.",
            font=("Segoe UI", 8), bg="white", fg=COLORS["text_lt"],
            justify="left"
        ).pack(anchor="w", pady=(8, 0))

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg=COLORS["text"])

    def _restore_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="#AAAAAA")

    def _build_list(self, parent):
        tk.Label(parent, text="📋 Active Reminders",
                 font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text"]
                 ).pack(anchor="w")

        self.list_frame = tk.Frame(parent, bg=COLORS["bg"])
        self.list_frame.pack(fill="both", expand=True, pady=8)
        self._refresh_list()

    def _refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        reminders = self.db.get_reminders()
        if not reminders:
            tk.Label(
                self.list_frame,
                text="💊 No reminders yet.\nAdd your first medicine reminder!",
                font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text_lt"],
                justify="center"
            ).place(relx=0.5, rely=0.4, anchor="center")
            return

        for r in reminders:
            rid, med, rtime, dosage, notes, active, created = r
            card = tk.Frame(self.list_frame, bg="white")
            card.pack(fill="x", pady=4)
            inner = tk.Frame(card, bg="white")
            inner.pack(padx=12, pady=10, fill="x")

            left = tk.Frame(inner, bg="white")
            left.pack(side="left", fill="x", expand=True)

            tk.Label(left, text=f"💊 {med}",
                     font=FONTS["subhead"], bg="white", fg=COLORS["text"]).pack(anchor="w")

            row2 = tk.Frame(left, bg="white")
            row2.pack(anchor="w")
            tk.Label(row2, text=f"🕐 {rtime}",
                     font=FONTS["body"], bg="white", fg=COLORS["primary"]).pack(side="left", padx=(0, 12))
            if dosage:
                tk.Label(row2, text=f"📏 {dosage}",
                         font=FONTS["body"], bg="white", fg=COLORS["text_lt"]).pack(side="left")

            if notes:
                tk.Label(left, text=f"📝 {notes}",
                         font=FONTS["small"], bg="white", fg=COLORS["text_lt"]).pack(anchor="w")

            # Delete button
            tk.Button(
                inner, text="🗑 Delete",
                font=FONTS["small"], bg="#FDEDEC", fg=COLORS["red"],
                relief="flat", cursor="hand2", padx=8, pady=4,
                command=lambda rid=rid: self._delete(rid)
            ).pack(side="right")

    def _save(self):
        med = self.med_entry.get().strip()
        rtime = self.time_entry.get().strip()

        if not med:
            messagebox.showerror("Error", "Medicine name is required!", parent=self.parent)
            return

        if not rtime or rtime == "e.g. 08:30":
            messagebox.showerror("Error", "Please enter a valid time!", parent=self.parent)
            return

        # Validate HH:MM format
        try:
            h, m = rtime.split(":")
            assert 0 <= int(h) <= 23 and 0 <= int(m) <= 59
        except Exception:
            messagebox.showerror("Error", "Time must be in HH:MM format (e.g., 08:30)", parent=self.parent)
            return

        dosage = self.dose_entry.get().strip()
        notes = self.notes_entry.get().strip()

        self.db.add_reminder(med, rtime, dosage, notes)

        # Clear form
        for e in [self.med_entry, self.dose_entry, self.notes_entry]:
            e.delete(0, "end")
        self.time_entry.delete(0, "end")
        self.time_entry.insert(0, "e.g. 08:30")
        self.time_entry.config(fg="#AAAAAA")

        messagebox.showinfo("Success", f"✅ Reminder set for {med} at {rtime}", parent=self.parent)
        self._refresh_list()

    def _delete(self, rid):
        if messagebox.askyesno("Delete", "Delete this reminder?", parent=self.parent):
            self.db.delete_reminder(rid)
            self._refresh_list()
