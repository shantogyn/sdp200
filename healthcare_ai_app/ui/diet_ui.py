"""
Diet Planner Page
"""

import tkinter as tk
from tkinter import ttk
import random
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, styled_button, scrollable_frame
from models.diet_model import DietRecommender


class DietPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.recommender = DietRecommender()
        self._build()

    def _build(self):
        hdr = tk.Frame(self.parent, bg=COLORS["teal"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🥗 Personalized Diet Planner",
                 font=FONTS["title"], bg=COLORS["teal"], fg="white"
                 ).place(relx=0.02, rely=0.5, anchor="w")

        main = tk.Frame(self.parent, bg=COLORS["bg"])
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg=COLORS["bg"], width=330)
        left.pack(side="left", fill="y", padx=16, pady=16)
        left.pack_propagate(False)
        self._build_form(left)

        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="right", fill="both", expand=True, padx=16, pady=16)
        self._build_plan_area(right)

    def _build_form(self, parent):
        card = tk.Frame(parent, bg="white")
        card.pack(fill="x")
        inner = tk.Frame(card, bg="white")
        inner.pack(padx=16, pady=16, fill="x")

        tk.Label(inner, text="📝 Your Profile",
                 font=FONTS["heading"], bg="white", fg=COLORS["teal"]
                 ).pack(anchor="w", pady=(0, 12))

        # Age
        tk.Label(inner, text="🎂 Age (years)", font=FONTS["small"],
                 bg="white", fg=COLORS["text_lt"]).pack(anchor="w", pady=(6, 2))
        self.age_var = tk.StringVar(value="30")
        tk.Spinbox(inner, from_=1, to=120, textvariable=self.age_var,
                   font=FONTS["body"], width=10).pack(anchor="w", ipady=4)

        # Weight
        tk.Label(inner, text="⚖️ Weight (kg)", font=FONTS["small"],
                 bg="white", fg=COLORS["text_lt"]).pack(anchor="w", pady=(6, 2))
        self.weight_var = tk.StringVar(value="70")
        tk.Entry(inner, textvariable=self.weight_var, font=FONTS["body"],
                 relief="solid", bd=1, width=14).pack(anchor="w", ipady=5)

        # Gender
        tk.Label(inner, text="👤 Gender", font=FONTS["small"],
                 bg="white", fg=COLORS["text_lt"]).pack(anchor="w", pady=(6, 2))
        self.gender_var = tk.StringVar(value="Male")
        for g in ["Male", "Female"]:
            tk.Radiobutton(inner, text=g, variable=self.gender_var, value=g,
                           font=FONTS["body"], bg="white").pack(anchor="w")

        # Condition
        tk.Label(inner, text="🩺 Health Condition", font=FONTS["small"],
                 bg="white", fg=COLORS["text_lt"]).pack(anchor="w", pady=(6, 2))
        conditions = ["General Health", "Diabetes", "Hypertension",
                      "Obesity / Weight Loss", "Anemia"]
        self.cond_var = tk.StringVar(value=conditions[0])
        cond_menu = ttk.Combobox(inner, textvariable=self.cond_var,
                                  values=conditions, state="readonly",
                                  font=FONTS["body"], width=22)
        cond_menu.pack(anchor="w", ipady=2)

        styled_button(inner, "🥗 Generate Diet Plan", self._generate,
                      color=COLORS["teal"], width=20).pack(fill="x", pady=(16, 0))

    def _build_plan_area(self, parent):
        tk.Label(parent, text="🍽️ Your Diet Plan",
                 font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text"]
                 ).pack(anchor="w")

        self.plan_frame = tk.Frame(parent, bg=COLORS["bg"])
        self.plan_frame.pack(fill="both", expand=True, pady=8)

        tk.Label(
            self.plan_frame,
            text="🥗 Fill in your profile\nand click Generate Diet Plan",
            font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text_lt"],
            justify="center"
        ).place(relx=0.5, rely=0.4, anchor="center")

    def _generate(self):
        for w in self.plan_frame.winfo_children():
            w.destroy()

        try:
            age = int(self.age_var.get())
            weight = float(self.weight_var.get())
        except ValueError:
            tk.Label(self.plan_frame, text="⚠️ Please enter valid age and weight.",
                     font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["red"]).pack(pady=20)
            return

        condition = self.cond_var.get()
        plan = self.recommender.get_plan(age, weight, condition)

        outer, scroll = scrollable_frame(self.plan_frame)
        outer.pack(fill="both", expand=True)

        # Plan header
        head = tk.Frame(scroll, bg=COLORS["teal"])
        head.pack(fill="x", pady=(0, 12))
        hinner = tk.Frame(head, bg=COLORS["teal"])
        hinner.pack(padx=16, pady=10)

        tk.Label(hinner, text=f"🥗 {plan['label']}",
                 font=FONTS["heading"], bg=COLORS["teal"], fg="white").pack(anchor="w")
        tk.Label(hinner, text=f"🔥 Estimated Daily Calories: ~{plan['calories']} kcal",
                 font=FONTS["body"], bg=COLORS["teal"], fg="#A3E4D7").pack(anchor="w")
        tk.Label(hinner, text=f"ℹ️ {plan['notes']}",
                 font=("Segoe UI", 9, "italic"), bg=COLORS["teal"], fg="#A3E4D7",
                 wraplength=500).pack(anchor="w")

        # Meal sections
        meals = [
            ("🌅 Breakfast", "morning",  "#FFF9C4"),
            ("☀️ Lunch",     "lunch",    "#C8E6C9"),
            ("🌙 Dinner",    "dinner",   "#BBDEFB"),
            ("🍎 Snacks",    "snacks",   "#F8BBD9"),
        ]

        for emoji_label, key, bg in meals:
            if key not in plan:
                continue
            meal_card = tk.Frame(scroll, bg=bg)
            meal_card.pack(fill="x", pady=4)
            mi = tk.Frame(meal_card, bg=bg)
            mi.pack(padx=14, pady=10, fill="x")

            tk.Label(mi, text=emoji_label, font=FONTS["subhead"],
                     bg=bg, fg=COLORS["text"]).pack(anchor="w", pady=(0, 6))

            options = plan[key]
            chosen = random.choice(options)
            tk.Label(mi, text=f"✅  {chosen}",
                     font=FONTS["body"], bg=bg, fg=COLORS["text"],
                     wraplength=520, justify="left").pack(anchor="w")

            if len(options) > 1:
                alts = [o for o in options if o != chosen]
                tk.Label(mi, text="Alternative options:",
                         font=FONTS["small"], bg=bg, fg=COLORS["text_lt"]).pack(anchor="w", pady=(4, 0))
                for alt in alts:
                    tk.Label(mi, text=f"  • {alt}",
                             font=FONTS["small"], bg=bg, fg=COLORS["text_lt"]).pack(anchor="w")

        # Water reminder
        water = tk.Frame(scroll, bg="#E3F2FD")
        water.pack(fill="x", pady=4)
        wi = tk.Frame(water, bg="#E3F2FD")
        wi.pack(padx=14, pady=10, fill="x")
        tk.Label(wi, text="💧 Hydration Goal",
                 font=FONTS["subhead"], bg="#E3F2FD", fg=COLORS["primary"]).pack(anchor="w")
        tk.Label(wi, text=f"Drink approximately {int(weight * 0.033):.1f} litres of water per day.",
                 font=FONTS["body"], bg="#E3F2FD", fg=COLORS["text"]).pack(anchor="w")
