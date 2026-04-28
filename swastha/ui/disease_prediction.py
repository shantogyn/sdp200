# ui/disease_prediction.py
# eita disease prediction screen er UI
# user symptoms input kore disease prediction pabe

import tkinter as tk
from theme import COLORS, FONTS
from ui.components import make_button, make_scrollable_frame
from services.disease_service import predict_disease


class DiseasePredictionScreen:
    """
    Symptom-based disease prediction screen.
    User symptoms type korbe, system possible diseases suggest korbe.
    """

    def __init__(self, parent, user):
        self.parent = parent
        self.user = user

        self.frame = tk.Frame(parent, bg=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):
        """UI layout build kora hocche."""

        # page header
        header = tk.Frame(self.frame, bg=COLORS["accent_dark"], padx=25, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🔬  Disease Prediction",
            font=FONTS["heading"],
            bg=COLORS["accent_dark"],
            fg=COLORS["text_light"],
        ).pack(side="left")

        tk.Label(
            header,
            text="Symptoms diye possible diseases janun",
            font=FONTS["body"],
            bg=COLORS["accent_dark"],
            fg=COLORS["text_muted"],
        ).pack(side="left", padx=15)

        # main content
        content = tk.Frame(self.frame, bg=COLORS["bg_main"], padx=30, pady=20)
        content.pack(fill="both", expand=True)

        # ---- LEFT: Input Panel ----
        left = tk.Frame(content, bg=COLORS["bg_card"], padx=20, pady=20,
                        highlightthickness=1, highlightbackground=COLORS["border"])
        left.pack(side="left", fill="y", padx=(0, 15), ipadx=5)

        tk.Label(
            left,
            text="📝  Apnar Symptoms Likhun",
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            left,
            text="Comma diye alag alag symptoms likhun\n(e.g. fever, headache, fatigue)",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        # symptom text area
        self.symptom_text = tk.Text(
            left,
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"],
            width=32,
            height=8,
            wrap="word",
            insertbackground=COLORS["text_primary"],
        )
        self.symptom_text.pack(pady=(0, 10))

        # sample symptoms chips for easy input
        tk.Label(
            left,
            text="Quick Add (click to add):",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(5, 5))

        # common symptoms quick buttons
        quick_symptoms = [
            "fever", "headache", "cough", "fatigue",
            "dizziness", "nausea", "rash", "chest pain",
            "joint pain", "vomiting", "diarrhea", "thirst",
        ]

        chips_frame = tk.Frame(left, bg=COLORS["bg_card"])
        chips_frame.pack(fill="x", pady=(0, 15))

        # 3 chips per row
        for i, sym in enumerate(quick_symptoms):
            row = i // 3
            col = i % 3
            if col == 0:
                row_frame = tk.Frame(chips_frame, bg=COLORS["bg_card"])
                row_frame.pack(fill="x", pady=2)

            chip = tk.Button(
                row_frame,
                text=sym,
                font=FONTS["small"],
                bg=COLORS["bg_main"],
                fg=COLORS["primary"],
                relief="flat",
                cursor="hand2",
                padx=8,
                pady=4,
                bd=1,
                highlightbackground=COLORS["primary"],
                highlightthickness=1,
                command=lambda s=sym: self._add_symptom(s),
            )
            chip.pack(side="left", padx=2)

        # predict button
        make_button(
            left,
            text="  🔍  Predict Disease  ",
            command=self._predict,
        ).pack(fill="x", ipady=4)

        # clear button
        tk.Button(
            left,
            text="🗑  Clear",
            command=self._clear,
            font=FONTS["small"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_secondary"],
            relief="flat",
            cursor="hand2",
            pady=5,
        ).pack(fill="x", pady=(5, 0))

        # ---- RIGHT: Results Panel ----
        right = tk.Frame(content, bg=COLORS["bg_main"])
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="📊  Prediction Results",
            font=FONTS["subheading"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 10))

        # results container — scroll kora jabe
        self.results_scroll, self.results_frame = make_scrollable_frame(right)
        self.results_scroll.pack(fill="both", expand=True)

        # initial placeholder
        self._show_placeholder()

    def _add_symptom(self, symptom: str):
        """Quick chip click e symptom text box e add kore."""
        current = self.symptom_text.get("1.0", tk.END).strip()

        if current and not current.endswith(","):
            self.symptom_text.insert(tk.END, f", {symptom}")
        elif current:
            self.symptom_text.insert(tk.END, f"{symptom}")
        else:
            self.symptom_text.insert(tk.END, symptom)

    def _clear(self):
        """Input ar results clear kore."""
        self.symptom_text.delete("1.0", tk.END)
        self._clear_results()
        self._show_placeholder()

    def _predict(self):
        """
        Predict button press e call hobe.
        Symptoms niye disease_service call kore results show kore.
        """
        symptoms = self.symptom_text.get("1.0", tk.END).strip()

        if not symptoms:
            self._clear_results()
            self._show_message("⚠  Kono symptom likha nai! Amake janao ki lagche.", "warning")
            return

        # disease service call kora hocche
        results = predict_disease(symptoms)

        self._clear_results()

        if not results:
            self._show_message(
                "❓  Ei symptoms diye kono disease match pawa jacche na.\n"
                "Beshi specific symptoms try korun ba doctor er sathe kotha bolun.",
                "info"
            )
            return

        # results render kora hocche
        tk.Label(
            self.results_frame,
            text=f"✅  {len(results)} possible condition(s) found:",
            font=FONTS["body_bold"],
            bg=COLORS["bg_main"],
            fg=COLORS["primary"],
        ).pack(anchor="w", pady=(0, 10))

        for i, result in enumerate(results):
            self._render_result_card(result, rank=i + 1)

        # disclaimer
        tk.Label(
            self.results_frame,
            text="⚠  Ei result shudhumatra tottho provider hisebe — actual diagnosis er jonno doctor er sathe kotha bolun.",
            font=FONTS["small"],
            bg=COLORS["bg_main"],
            fg=COLORS["warning"],
            wraplength=520,
            justify="left",
        ).pack(anchor="w", pady=(15, 0))

    def _render_result_card(self, result, rank):
        """Ekটা disease prediction result card render kore."""

        score = result["score"]

        # score anujaye color — high match = green, low = orange
        if score >= 60:
            score_color = COLORS["success"]
            border_color = COLORS["success"]
        elif score >= 30:
            score_color = COLORS["warning"]
            border_color = COLORS["warning"]
        else:
            score_color = COLORS["text_secondary"]
            border_color = COLORS["border"]

        card = tk.Frame(
            self.results_frame,
            bg=COLORS["bg_card"],
            padx=18,
            pady=14,
            highlightthickness=2,
            highlightbackground=border_color,
        )
        card.pack(fill="x", pady=6)

        # header row — rank, disease name, score
        header_row = tk.Frame(card, bg=COLORS["bg_card"])
        header_row.pack(fill="x")

        tk.Label(
            header_row,
            text=f"#{rank}",
            font=FONTS["body_bold"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
            width=3,
        ).pack(side="left")

        tk.Label(
            header_row,
            text=f"  {result['disease']}",
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(side="left")

        # score bar + percentage
        score_frame = tk.Frame(header_row, bg=COLORS["bg_card"])
        score_frame.pack(side="right")

        tk.Label(
            score_frame,
            text=f"{score}% match",
            font=FONTS["body_bold"],
            bg=COLORS["bg_card"],
            fg=score_color,
        ).pack()

        # visual progress bar
        bar_bg = tk.Frame(card, bg=COLORS["border"], height=6)
        bar_bg.pack(fill="x", pady=(6, 8))

        bar_width_ratio = score / 100
        bar_fill = tk.Frame(bar_bg, bg=score_color, height=6)
        bar_fill.place(relwidth=bar_width_ratio, relheight=1.0)

        # matched symptoms
        matched = result.get("matched_symptoms", [])
        if matched:
            tk.Label(
                card,
                text="✓  Matched symptoms:  " + ",  ".join(matched),
                font=FONTS["small"],
                bg=COLORS["bg_card"],
                fg=COLORS["text_secondary"],
                wraplength=490,
                justify="left",
            ).pack(anchor="w")

    def _show_placeholder(self):
        """Initial state placeholder show kore."""
        tk.Label(
            self.results_frame,
            text="👈  Bame symptoms likhe 'Predict' button press korun",
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_muted"],
        ).pack(expand=True, pady=60)

    def _show_message(self, text, msg_type="info"):
        """Ekটা message results area te show kore."""
        color_map = {
            "info":    COLORS["info"],
            "warning": COLORS["warning"],
            "success": COLORS["success"],
        }
        tk.Label(
            self.results_frame,
            text=text,
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=color_map.get(msg_type, COLORS["text_secondary"]),
            wraplength=500,
            justify="left",
        ).pack(anchor="w", pady=20)

    def _clear_results(self):
        """Results frame er sob widgets destroy kore."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()