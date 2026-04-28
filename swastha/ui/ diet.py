# ui/diet.py
# eita diet recommendation screen er UI
# user er age, weight, disease input niye personalized diet plan show kore

import tkinter as tk
from theme import COLORS, FONTS
from ui.components import make_button, make_scrollable_frame
from services.diet_service import get_personalized_diet


class DietScreen:
    """
    Diet recommendation screen.
    User er health info niye customized diet plan generate kore.
    """

    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.frame = tk.Frame(parent, bg=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):
        # page header
        header = tk.Frame(self.frame, bg=COLORS["primary"], padx=25, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🥗  Diet Plan Recommendation",
            font=FONTS["heading"],
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
        ).pack(side="left")

        # main area
        main = tk.Frame(self.frame, bg=COLORS["bg_main"], padx=30, pady=20)
        main.pack(fill="both", expand=True)

        # ---- LEFT: Form ----
        left = tk.Frame(main, bg=COLORS["bg_card"], padx=20, pady=20,
                        highlightthickness=1, highlightbackground=COLORS["border"])
        left.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(
            left,
            text="👤  Apnar Tottho Din",
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 15))

        # Age input
        tk.Label(left, text="Boyosh (Age):", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")
        self.age_entry = tk.Entry(
            left, font=FONTS["body"], bg=COLORS["bg_main"],
            fg=COLORS["text_primary"], relief="flat",
            highlightthickness=1, highlightbackground=COLORS["border"],
            width=22,
        )
        self.age_entry.pack(fill="x", ipady=6, pady=(3, 12))

        # Weight input
        tk.Label(left, text="Ojon (Weight in kg):", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")
        self.weight_entry = tk.Entry(
            left, font=FONTS["body"], bg=COLORS["bg_main"],
            fg=COLORS["text_primary"], relief="flat",
            highlightthickness=1, highlightbackground=COLORS["border"],
            width=22,
        )
        self.weight_entry.pack(fill="x", ipady=6, pady=(3, 12))

        # Disease dropdown
        tk.Label(left, text="Rog / Condition:", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")

        self.disease_var = tk.StringVar(value="General / No Disease")
        disease_options = [
            "General / No Disease",
            "Diabetes", "Hypertension", "Dengue",
            "Common Cold", "Typhoid", "Malaria",
            "Anemia", "Gastritis", "Arthritis",
        ]

        disease_menu = tk.OptionMenu(left, self.disease_var, *disease_options)
        disease_menu.config(
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            width=20,
        )
        disease_menu["menu"].config(font=FONTS["body"], bg=COLORS["bg_card"])
        disease_menu.pack(fill="x", pady=(3, 20))

        # Generate button
        make_button(
            left,
            text="  🥗  Generate Diet Plan  ",
            command=self._generate,
        ).pack(fill="x", ipady=4)

        # ---- RIGHT: Result ----
        right = tk.Frame(main, bg=COLORS["bg_main"])
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="📋  Your Personalized Diet Plan",
            font=FONTS["subheading"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 10))

        self.result_scroll, self.result_frame = make_scrollable_frame(right)
        self.result_scroll.pack(fill="both", expand=True)

        self._show_placeholder()

    def _generate(self):
        """Form submit e personalized diet plan generate kore show kore."""
        age_str    = self.age_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        disease    = self.disease_var.get()

        # validation
        try:
            age = int(age_str) if age_str else 30
            if age < 1 or age > 120:
                raise ValueError
        except ValueError:
            self._clear_results()
            self._show_msg("⚠  Valid boyosh dite hobe (1-120)!", "warning")
            return

        try:
            weight = float(weight_str) if weight_str else 65.0
            if weight < 10 or weight > 300:
                raise ValueError
        except ValueError:
            self._clear_results()
            self._show_msg("⚠  Valid weight dite hobe (10-300 kg)!", "warning")
            return

        # diet service call
        plan_text = get_personalized_diet(age, weight, disease)

        self._clear_results()
        self._render_plan(plan_text, age, weight, disease)

    def _render_plan(self, plan_text, age, weight, disease):
        """Diet plan text parse kore formatted UI render kore."""

        # summary card
        summary = tk.Frame(
            self.result_frame,
            bg=COLORS["primary"],
            padx=18,
            pady=12,
        )
        summary.pack(fill="x", pady=(0, 15))

        tk.Label(
            summary,
            text=f"👤  Age: {age}  |  ⚖️  Weight: {weight} kg  |  🏥  Condition: {disease}",
            font=FONTS["body_bold"],
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
        ).pack(anchor="w")

        # plan text blocks — section by section parse kora hocche
        card_outer = tk.Frame(
            self.result_frame,
            bg=COLORS["bg_card"],
            padx=20,
            pady=18,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        card_outer.pack(fill="x")

        for line in plan_text.split("\n"):
            line = line.strip()
            if not line:
                tk.Frame(card_outer, bg=COLORS["bg_card"], height=6).pack(fill="x")
                continue

            if line.startswith("---"):
                # section divider
                tk.Frame(card_outer, bg=COLORS["border"], height=1).pack(fill="x", pady=4)
            elif line[0] in "📋👤⚖️💧":
                # section header
                tk.Label(
                    card_outer,
                    text=line,
                    font=FONTS["body_bold"],
                    bg=COLORS["bg_card"],
                    fg=COLORS["primary"],
                    anchor="w",
                ).pack(fill="x", pady=(8, 2))
            elif line.startswith("•"):
                # bullet point
                tk.Label(
                    card_outer,
                    text=f"   {line}",
                    font=FONTS["body"],
                    bg=COLORS["bg_card"],
                    fg=COLORS["text_primary"],
                    anchor="w",
                    justify="left",
                    wraplength=480,
                ).pack(fill="x")
            else:
                # regular text
                tk.Label(
                    card_outer,
                    text=line,
                    font=FONTS["body"],
                    bg=COLORS["bg_card"],
                    fg=COLORS["text_secondary"],
                    anchor="w",
                    wraplength=480,
                ).pack(fill="x")

    def _show_placeholder(self):
        tk.Label(
            self.result_frame,
            text="👈  Tottho diye 'Generate' button press korun",
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_muted"],
        ).pack(expand=True, pady=60)

    def _show_msg(self, text, msg_type="info"):
        fg = {"warning": COLORS["warning"], "info": COLORS["info"]}.get(msg_type, COLORS["text_secondary"])
        tk.Label(
            self.result_frame,
            text=text,
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=fg,
        ).pack(anchor="w", pady=20)

    def _clear_results(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()