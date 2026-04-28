"""
Lab Report Analyzer Page
"""

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, styled_button
from models.lab_model import LabAnalyzer


class LabPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.analyzer = LabAnalyzer()
        self._build()

    def _build(self):
        hdr = tk.Frame(self.parent, bg=COLORS["purple"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🧪 Lab Report Analyzer",
                 font=FONTS["title"], bg=COLORS["purple"], fg="white"
                 ).place(relx=0.02, rely=0.5, anchor="w")

        main = tk.Frame(self.parent, bg=COLORS["bg"])
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg=COLORS["bg"], width=360)
        left.pack(side="left", fill="y", padx=16, pady=16)
        left.pack_propagate(False)
        self._build_input(left)

        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="right", fill="both", expand=True, padx=16, pady=16)
        self._build_results(right)

    def _build_input(self, parent):
        card = tk.Frame(parent, bg="white")
        card.pack(fill="x")
        inner = tk.Frame(card, bg="white")
        inner.pack(padx=16, pady=16, fill="x")

        tk.Label(inner, text="📋 Enter Lab Values",
                 font=FONTS["heading"], bg="white", fg=COLORS["purple"]
                 ).pack(anchor="w", pady=(0, 12))

        self.entries = {}
        lab_fields = [
            ("blood_sugar",  "🩸 Blood Sugar (mg/dL)",         "70 – 100"),
            ("cholesterol",  "🫀 Total Cholesterol (mg/dL)",    "< 200"),
            ("systolic",     "💓 Systolic BP (mmHg)",           "90 – 120"),
            ("diastolic",    "💓 Diastolic BP (mmHg)",          "60 – 80"),
            ("hemoglobin",   "🔴 Hemoglobin (g/dL)",            "13 – 17.5"),
        ]

        for key, label, hint in lab_fields:
            tk.Label(inner, text=label, font=FONTS["small"],
                     bg="white", fg=COLORS["text_lt"]).pack(anchor="w", pady=(6, 1))
            row = tk.Frame(inner, bg="white")
            row.pack(fill="x")
            entry = tk.Entry(row, font=FONTS["body"], relief="solid",
                             bd=1, width=14, bg="white")
            entry.pack(side="left", ipady=5)
            tk.Label(row, text=f"  Normal: {hint}", font=("Segoe UI", 8),
                     bg="white", fg=COLORS["text_lt"]).pack(side="left")
            self.entries[key] = entry

        styled_button(inner, "🔬 Analyze Report", self._analyze,
                      color=COLORS["purple"], width=20).pack(fill="x", pady=(16, 0))
        styled_button(inner, "🗑 Clear All", self._clear_all,
                      color=COLORS["text_lt"], width=20).pack(fill="x", pady=(6, 0))

    def _build_results(self, parent):
        tk.Label(parent, text="📊 Analysis Results",
                 font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text"]
                 ).pack(anchor="w")

        self.results_frame = tk.Frame(parent, bg=COLORS["bg"])
        self.results_frame.pack(fill="both", expand=True, pady=8)

        tk.Label(
            self.results_frame,
            text="🔬 Enter your lab values\nand click Analyze to see results",
            font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text_lt"],
            justify="center"
        ).place(relx=0.5, rely=0.4, anchor="center")

    def _analyze(self):
        for w in self.results_frame.winfo_children():
            w.destroy()

        values = {}
        for key, entry in self.entries.items():
            val = entry.get().strip()
            if val:
                try:
                    values[key] = float(val)
                except ValueError:
                    pass

        if not values:
            tk.Label(self.results_frame, text="⚠️ Enter at least one lab value.",
                     font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["red"]
                     ).pack(pady=20)
            return

        results = self.analyzer.analyze(**values)

        for test_key, result in results.items():
            self._result_card(self.results_frame, result)

        # Disclaimer
        tk.Label(
            self.results_frame,
            text="⚠️ These results are for informational purposes only. Consult a doctor for medical advice.",
            font=("Segoe UI", 8, "italic"), bg=COLORS["bg"], fg=COLORS["red"],
            wraplength=550
        ).pack(anchor="w", pady=(8, 0))

    def _result_card(self, parent, result):
        color = result.get("color", COLORS["primary"])

        card = tk.Frame(parent, bg="white")
        card.pack(fill="x", pady=5)
        inner = tk.Frame(card, bg="white")
        inner.pack(padx=14, pady=12, fill="x")

        # Color stripe
        stripe = tk.Frame(card, bg=color, width=6)
        stripe.place(x=0, y=0, relheight=1)

        # Header
        head = tk.Frame(inner, bg="white")
        head.pack(fill="x")

        icon = result.get("icon", "📋")
        tk.Label(head, text=f"{icon} {result.get('label', 'Test')}",
                 font=FONTS["subhead"], bg="white", fg=COLORS["text"]).pack(side="left")

        # Value badge
        val = result.get("value", "")
        unit = result.get("unit", "")
        tk.Label(head, text=f"{val} {unit}",
                 font=("Segoe UI", 11, "bold"), bg="white", fg=color).pack(side="right")

        # Status badge
        status_row = tk.Frame(inner, bg="white")
        status_row.pack(fill="x", pady=(4, 0))

        status_lbl = tk.Label(status_row, text=f"  {result.get('status', '')}  ",
                               font=("Segoe UI", 9, "bold"), bg=color, fg="white",
                               padx=6, pady=2)
        status_lbl.pack(side="left")

        # Advice
        if result.get("advice"):
            tk.Label(inner, text=result["advice"],
                     font=FONTS["small"], bg="white", fg=COLORS["text"],
                     wraplength=500, justify="left").pack(anchor="w", pady=(6, 0))

    def _clear_all(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        for w in self.results_frame.winfo_children():
            w.destroy()
        tk.Label(
            self.results_frame,
            text="🔬 Enter your lab values\nand click Analyze to see results",
            font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text_lt"],
            justify="center"
        ).place(relx=0.5, rely=0.4, anchor="center")
