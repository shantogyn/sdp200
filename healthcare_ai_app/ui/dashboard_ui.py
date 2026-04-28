"""
Dashboard Page - Home screen with overview cards
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, scrollable_frame


FEATURE_CARDS = [
    ("🦠", "Disease\nPredictor",    COLORS["primary"],  "#EBF5FB"),
    ("🤖", "AI Medical\nChatbot",   COLORS["green"],    "#EAFAF1"),
    ("⏰", "Medicine\nReminder",    COLORS["orange"],   "#FEF9E7"),
    ("🧪", "Lab Report\nAnalyzer",  COLORS["purple"],   "#F4ECF7"),
    ("🥗", "Diet\nPlanner",         COLORS["teal"],     "#E8F8F5"),
    ("🧘", "Mental\nHealth",        "#E91E63",          "#FCE4EC"),
    ("🚑", "First Aid\nGuide",      COLORS["red"],      "#FDEDEC"),
    ("🏥", "Hospital\nFinder",      COLORS["primary_dk"], "#EBF5FB"),
    ("📚", "Disease\nInfo",         "#795548",          "#EFEBE9"),
]

HEALTH_TIPS = [
    "💧 Drink at least 8 glasses of water daily.",
    "🏃 Exercise for 30 minutes, 5 days a week.",
    "🛌 Adults need 7-9 hours of quality sleep per night.",
    "🥦 Fill half your plate with fruits and vegetables.",
    "🚭 Avoid tobacco and limit alcohol consumption.",
    "🧴 Wash hands for 20 seconds to prevent infections.",
    "🩺 Schedule regular health check-ups and screenings.",
    "🧘 Practice mindfulness to reduce stress levels.",
    "☀️ Get 10-15 minutes of sunlight for Vitamin D.",
    "😊 Maintain social connections for mental wellbeing.",
]


class DashboardPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self._build()

    def _build(self):
        # Header
        header = tk.Frame(self.parent, bg=COLORS["primary"], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        now = datetime.now()
        greeting = "Good Morning" if now.hour < 12 else ("Good Afternoon" if now.hour < 17 else "Good Evening")

        tk.Label(
            header,
            text=f"{greeting}! Welcome to AI Smart Healthcare Assistant 🏥",
            font=("Segoe UI", 15, "bold"),
            bg=COLORS["primary"], fg="white"
        ).place(relx=0.02, rely=0.3)

        tk.Label(
            header,
            text=f"📅 {now.strftime('%A, %B %d, %Y')}   🕐 {now.strftime('%I:%M %p')}",
            font=FONTS["body"],
            bg=COLORS["primary"], fg="#AED6F1"
        ).place(relx=0.02, rely=0.65)

        # Scrollable content
        outer, content = scrollable_frame(self.parent)
        outer.pack(fill="both", expand=True)

        # Stats bar
        self._stats_bar(content)

        # Feature cards section
        tk.Label(
            content, text="🚀 Quick Access",
            font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text"]
        ).pack(anchor="w", padx=20, pady=(16, 8))

        grid_frame = tk.Frame(content, bg=COLORS["bg"])
        grid_frame.pack(fill="x", padx=16)
        self._feature_grid(grid_frame)

        # Health tip
        self._health_tip(content)

        # Reminder preview
        self._reminder_preview(content)

    def _stats_bar(self, parent):
        stats = [
            ("🦠", "9", "Diseases\nMonitored", COLORS["primary"]),
            ("💊", str(len(self.db.get_reminders())), "Active\nReminders", COLORS["orange"]),
            ("🤖", "AI", "Chatbot\nActive", COLORS["green"]),
            ("🏥", "24/7", "Support\nAvailable", COLORS["purple"]),
        ]
        bar = tk.Frame(parent, bg=COLORS["bg"])
        bar.pack(fill="x", padx=16, pady=(16, 8))

        for icon, val, label, color in stats:
            card = tk.Frame(bar, bg="white", relief="flat", bd=0)
            card.pack(side="left", fill="x", expand=True, padx=4)

            inner = tk.Frame(card, bg="white")
            inner.pack(padx=16, pady=12)

            top = tk.Frame(inner, bg="white")
            top.pack()
            tk.Label(top, text=icon, font=("Segoe UI", 18), bg="white").pack(side="left")
            tk.Label(top, text=val, font=("Segoe UI", 20, "bold"),
                     bg="white", fg=color).pack(side="left", padx=6)

            tk.Label(inner, text=label, font=FONTS["small"],
                     bg="white", fg=COLORS["text_lt"]).pack()

    def _feature_grid(self, parent):
        cols = 3
        for i, (icon, label, color, bg) in enumerate(FEATURE_CARDS):
            row = i // cols
            col = i % cols

            card = tk.Frame(parent, bg=bg, relief="flat", bd=0, cursor="hand2")
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
            parent.columnconfigure(col, weight=1)

            inner = tk.Frame(card, bg=bg)
            inner.pack(padx=20, pady=16)

            icon_lbl = tk.Label(inner, text=icon, font=("Segoe UI", 26),
                                bg=bg, fg=color)
            icon_lbl.pack()

            tk.Label(inner, text=label, font=("Segoe UI", 10, "bold"),
                     bg=bg, fg=COLORS["text"], justify="center").pack(pady=(4, 0))

    def _health_tip(self, parent):
        import random
        tip = random.choice(HEALTH_TIPS)

        frame = tk.Frame(parent, bg="#EBF5FB", relief="flat")
        frame.pack(fill="x", padx=16, pady=(8, 4))

        inner = tk.Frame(frame, bg="#EBF5FB")
        inner.pack(padx=16, pady=12, fill="x")

        tk.Label(
            inner, text="💡 Health Tip of the Day",
            font=FONTS["subhead"], bg="#EBF5FB", fg=COLORS["primary"]
        ).pack(anchor="w")

        tk.Label(
            inner, text=tip, font=FONTS["body"],
            bg="#EBF5FB", fg=COLORS["text"], wraplength=700, justify="left"
        ).pack(anchor="w", pady=(4, 0))

    def _reminder_preview(self, parent):
        reminders = self.db.get_reminders()

        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=16, pady=(8, 16))
        inner = tk.Frame(frame, bg="white")
        inner.pack(padx=16, pady=12, fill="x")

        tk.Label(
            inner, text="⏰ Upcoming Reminders",
            font=FONTS["subhead"], bg="white", fg=COLORS["orange"]
        ).pack(anchor="w", pady=(0, 6))

        if not reminders:
            tk.Label(
                inner, text="No medicine reminders set. Go to Medicine Reminders to add one.",
                font=FONTS["body"], bg="white", fg=COLORS["text_lt"]
            ).pack(anchor="w")
        else:
            for r in reminders[:3]:
                rid, med, rtime, dosage, notes, active, created = r
                row = tk.Frame(inner, bg="#F8F9FA")
                row.pack(fill="x", pady=2)
                tk.Label(row, text=f"💊 {med}",
                         font=("Segoe UI", 10, "bold"), bg="#F8F9FA",
                         fg=COLORS["text"], width=20, anchor="w").pack(side="left", padx=8, pady=4)
                tk.Label(row, text=f"🕐 {rtime}",
                         font=FONTS["body"], bg="#F8F9FA",
                         fg=COLORS["primary"]).pack(side="left", padx=8)
                if dosage:
                    tk.Label(row, text=dosage, font=FONTS["small"],
                             bg="#F8F9FA", fg=COLORS["text_lt"]).pack(side="left")
