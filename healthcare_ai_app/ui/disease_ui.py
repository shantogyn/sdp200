"""
Disease Prediction Page
"""

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, styled_button, scrollable_frame
from models.disease_model import DiseasePredictor, ALL_SYMPTOMS


class DiseasePage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.predictor = DiseasePredictor()
        self.selected_symptoms = []
        self.symptom_vars = {}
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self.parent, bg=COLORS["primary"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🦠 Disease Prediction System",
                 font=FONTS["title"], bg=COLORS["primary"], fg="white"
                 ).place(relx=0.02, rely=0.5, anchor="w")

        # Main 2-column layout
        main = tk.Frame(self.parent, bg=COLORS["bg"])
        main.pack(fill="both", expand=True)

        # Left: symptom selector
        left = tk.Frame(main, bg=COLORS["bg"], width=400)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        self._build_symptom_panel(left)

        # Right: results
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="right", fill="both", expand=True)
        self._build_results_panel(right)

    def _build_symptom_panel(self, parent):
        tk.Label(parent, text="Select Your Symptoms",
                 font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text"]
                 ).pack(anchor="w", padx=16, pady=(12, 4))

        # Search bar
        search_frame = tk.Frame(parent, bg="white")
        search_frame.pack(fill="x", padx=16, pady=(0, 8))
        tk.Label(search_frame, text="🔍", font=("Segoe UI", 11),
                 bg="white").pack(side="left", padx=6)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_symptoms)
        tk.Entry(search_frame, textvariable=self.search_var,
                 font=FONTS["body"], relief="flat", bg="white",
                 fg=COLORS["text"]).pack(side="left", fill="x", expand=True, pady=6)

        # Symptom checkboxes
        outer, inner = scrollable_frame(parent)
        outer.pack(fill="both", expand=True, padx=16)
        self.symptom_container = inner
        self._render_symptoms(ALL_SYMPTOMS)

        # Buttons
        btn_frame = tk.Frame(parent, bg=COLORS["bg"])
        btn_frame.pack(fill="x", padx=16, pady=8)
        styled_button(btn_frame, "🔍 Analyze", self._predict,
                      color=COLORS["primary"], width=14).pack(side="left", padx=4)
        styled_button(btn_frame, "🗑 Clear", self._clear,
                      color=COLORS["text_lt"], width=10).pack(side="left", padx=4)

        # Selected count
        self.count_lbl = tk.Label(parent, text="0 symptoms selected",
                                   font=FONTS["small"], bg=COLORS["bg"],
                                   fg=COLORS["text_lt"])
        self.count_lbl.pack(anchor="w", padx=16)

    def _render_symptoms(self, symptoms):
        for widget in self.symptom_container.winfo_children():
            widget.destroy()
        self.symptom_vars = {}

        for s in symptoms:
            var = tk.BooleanVar()
            if s in self.selected_symptoms:
                var.set(True)
            self.symptom_vars[s] = var

            cb = tk.Checkbutton(
                self.symptom_container,
                text=s.title(),
                variable=var,
                font=FONTS["body"],
                bg=COLORS["bg"],
                fg=COLORS["text"],
                activebackground=COLORS["hover"],
                selectcolor="white",
                command=lambda s=s, v=var: self._toggle_symptom(s, v)
            )
            cb.pack(anchor="w", padx=4, pady=1)

    def _filter_symptoms(self, *args):
        query = self.search_var.get().lower()
        filtered = [s for s in ALL_SYMPTOMS if query in s.lower()] if query else ALL_SYMPTOMS
        self._render_symptoms(filtered)

    def _toggle_symptom(self, symptom, var):
        if var.get():
            if symptom not in self.selected_symptoms:
                self.selected_symptoms.append(symptom)
        else:
            if symptom in self.selected_symptoms:
                self.selected_symptoms.remove(symptom)
        self.count_lbl.config(text=f"{len(self.selected_symptoms)} symptoms selected")

    def _build_results_panel(self, parent):
        tk.Label(parent, text="Prediction Results",
                 font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text"]
                 ).pack(anchor="w", padx=16, pady=(12, 4))

        self.results_frame = tk.Frame(parent, bg=COLORS["bg"])
        self.results_frame.pack(fill="both", expand=True, padx=16)

        # Placeholder
        tk.Label(
            self.results_frame,
            text="👆 Select symptoms on the left\nand click Analyze to see results",
            font=FONTS["heading"],
            bg=COLORS["bg"], fg=COLORS["text_lt"],
            justify="center"
        ).place(relx=0.5, rely=0.4, anchor="center")

    def _predict(self):
        for w in self.results_frame.winfo_children():
            w.destroy()

        if not self.selected_symptoms:
            tk.Label(self.results_frame, text="⚠️ Please select at least one symptom.",
                     font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["red"]
                     ).pack(pady=20)
            return

        results = self.predictor.predict(self.selected_symptoms)
        if not results:
            tk.Label(self.results_frame,
                     text="No matching diseases found for the selected symptoms.",
                     font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text_lt"]
                     ).pack(pady=20)
            return

        # Selected symptoms display
        symp_frame = tk.Frame(self.results_frame, bg="#EBF5FB")
        symp_frame.pack(fill="x", pady=(0, 12))
        inner = tk.Frame(symp_frame, bg="#EBF5FB")
        inner.pack(padx=12, pady=8)
        tk.Label(inner, text="Analyzed Symptoms:",
                 font=FONTS["subhead"], bg="#EBF5FB", fg=COLORS["primary"]).pack(anchor="w")
        symp_text = " • ".join(s.title() for s in self.selected_symptoms)
        tk.Label(inner, text=symp_text, font=FONTS["small"],
                 bg="#EBF5FB", fg=COLORS["text"],
                 wraplength=500, justify="left").pack(anchor="w")

        # Results
        outer, scroll_inner = scrollable_frame(self.results_frame)
        outer.pack(fill="both", expand=True)

        rank_colors = [COLORS["red"], COLORS["orange"], COLORS["primary"],
                       COLORS["teal"], COLORS["green"]]

        for i, (disease, prob, data) in enumerate(results):
            color = rank_colors[i % len(rank_colors)]
            self._disease_card(scroll_inner, i+1, disease, prob, data, color)

    def _disease_card(self, parent, rank, disease, prob, data, color):
        card = tk.Frame(parent, bg="white")
        card.pack(fill="x", pady=6)
        inner = tk.Frame(card, bg="white")
        inner.pack(padx=14, pady=12, fill="x")

        # Header row
        head = tk.Frame(inner, bg="white")
        head.pack(fill="x")

        badge = tk.Label(head, text=f" #{rank} ", font=("Segoe UI", 9, "bold"),
                         bg=color, fg="white", padx=4, pady=2)
        badge.pack(side="left")

        tk.Label(head, text=disease, font=FONTS["subhead"],
                 bg="white", fg=COLORS["text"]).pack(side="left", padx=8)

        tk.Label(head, text=f"{prob}%", font=("Segoe UI", 12, "bold"),
                 bg="white", fg=color).pack(side="right")

        # Progress bar
        bar_bg = tk.Frame(inner, bg="#ECF0F1", height=8)
        bar_bg.pack(fill="x", pady=(6, 8))
        bar_bg.pack_propagate(False)
        bar_fill_width = max(int(prob / 100 * 1), 1)
        bar_fill = tk.Frame(bar_bg, bg=color, height=8)
        bar_fill.place(relwidth=prob/100, relheight=1)

        # Details
        if data.get("description"):
            tk.Label(inner, text=f"📋 {data['description']}",
                     font=FONTS["small"], bg="white", fg=COLORS["text"],
                     wraplength=460, justify="left").pack(anchor="w")
        if data.get("treatment"):
            tk.Label(inner, text=f"💊 Treatment: {data['treatment']}",
                     font=FONTS["small"], bg="white", fg=COLORS["text_lt"],
                     wraplength=460, justify="left").pack(anchor="w", pady=(2, 0))

        tk.Label(inner,
                 text="⚠️ This is an AI estimate only. Please consult a qualified doctor.",
                 font=("Segoe UI", 8, "italic"), bg="white", fg=COLORS["red"]
                 ).pack(anchor="w", pady=(4, 0))

    def _clear(self):
        self.selected_symptoms.clear()
        self._render_symptoms(ALL_SYMPTOMS)
        self.count_lbl.config(text="0 symptoms selected")
        for w in self.results_frame.winfo_children():
            w.destroy()
        tk.Label(
            self.results_frame,
            text="👆 Select symptoms on the left\nand click Analyze to see results",
            font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text_lt"],
            justify="center"
        ).place(relx=0.5, rely=0.4, anchor="center")
