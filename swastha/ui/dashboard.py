# ui/dashboard.py
# eita main dashboard screen er UI
# login er pore user prothome ei screen dekhe
# feature cards, welcome message, health alerts show hobe ekhane

import tkinter as tk
from theme import COLORS, FONTS
from ui.components import make_scrollable_frame
from services.disease_service import get_health_alerts


# Feature cards er data — icon, title, description, navigation key
FEATURE_CARDS = [
    ("🔬", "Disease Prediction",  "Symptoms diye disease\npredict korun",    "disease_prediction"),
    ("🥗", "Diet Plan",           "Personalized diet\nplan paan",             "diet"),
    ("⏰", "Medicine Reminder",   "Medicine er somoy\nmissed korben na",      "reminder"),
    ("🧪", "Lab Analyzer",        "Lab report upload\nkore analyze korun",    "lab_analyzer"),
    ("🚑", "First Aid Guide",     "Emergency e ki\nkorben janun",             "first_aid"),
    ("📋", "Disease Info",        "Diseases er detail\ninfo dekhuun",         "disease_info"),
]


class DashboardScreen:
    """
    Main dashboard — sob features er entry point.
    Health alerts ar quick stats show kore.
    """

    def __init__(self, parent, user, on_nav):
        """
        parent: right panel frame jekhanে dashboard render hobe
        user: logged-in user dict {'id', 'username', 'email'}
        on_nav: callback(key) — nav item click e call hobe
        """
        self.parent = parent
        self.user = user
        self.on_nav = on_nav

        self.frame = tk.Frame(parent, bg=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):
        """Dashboard UI build kora hocche."""

        # ---- Scrollable wrapper ----
        scroll_container, scroll_frame = make_scrollable_frame(self.frame)
        scroll_container.pack(fill="both", expand=True)

        content = tk.Frame(scroll_frame, bg=COLORS["bg_main"], padx=30, pady=20)
        content.pack(fill="both", expand=True)

        # ---- Welcome Banner ----
        self._build_welcome(content)

        # ---- Feature Cards Grid ----
        tk.Label(
            content,
            text="Quick Access",
            font=FONTS["subheading"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(20, 10))

        self._build_feature_grid(content)

        # ---- Health Alerts Section ----
        tk.Label(
            content,
            text="🚨  Active Health Alerts",
            font=FONTS["subheading"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(25, 10))

        self._build_alerts(content)

    def _build_welcome(self, parent):
        """Welcome banner — user greeting ar summary."""

        banner = tk.Frame(
            parent,
            bg=COLORS["primary"],
            padx=25,
            pady=20,
        )
        banner.pack(fill="x")

        left = tk.Frame(banner, bg=COLORS["primary"])
        left.pack(side="left", fill="both", expand=True)

        tk.Label(
            left,
            text=f"👋  Welcome back, {self.user.get('username', 'User')}!",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            left,
            text="Your AI health assistant is ready. Kothay jete chai?",
            font=FONTS["body"],
            bg=COLORS["primary"],
            fg="#C8F0DA",
            anchor="w",
        ).pack(fill="x", pady=(5, 0))

        # right — large icon
        tk.Label(
            banner,
            text="🏥",
            font=("Segoe UI", 48),
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
        ).pack(side="right", padx=10)

    def _build_feature_grid(self, parent):
        """
        Feature cards 3-column grid e render kora hocche.
        Card click e corresponding screen e navigate korbe.
        """
        grid_frame = tk.Frame(parent, bg=COLORS["bg_main"])
        grid_frame.pack(fill="x")

        # 3 column grid
        for col in range(3):
            grid_frame.columnconfigure(col, weight=1)

        for idx, (icon, title, desc, key) in enumerate(FEATURE_CARDS):
            row_num = idx // 3
            col_num = idx % 3

            card = self._make_feature_card(grid_frame, icon, title, desc, key)
            card.grid(
                row=row_num,
                column=col_num,
                padx=8,
                pady=8,
                sticky="nsew"
            )

    def _make_feature_card(self, parent, icon, title, desc, nav_key):
        """
        Ekটা feature card widget create kore.
        Click e on_nav callback call korbe.
        """
        card = tk.Frame(
            parent,
            bg=COLORS["bg_card"],
            bd=0,
            cursor="hand2",
            padx=20,
            pady=18,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )

        # icon
        tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 32),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"],
        ).pack()

        # title
        tk.Label(
            card,
            text=title,
            font=FONTS["card_title"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(pady=(8, 3))

        # description
        tk.Label(
            card,
            text=desc,
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
            justify="center",
        ).pack()

        # green bottom accent bar
        accent = tk.Frame(card, bg=COLORS["primary"], height=3)
        accent.pack(fill="x", side="bottom", pady=(12, 0))

        # click handler — card ar sob children e click bind kora hocche
        def _click(e, k=nav_key):
            self.on_nav(k)

        for widget in [card] + card.winfo_children():
            widget.bind("<Button-1>", _click)

        # hover effect
        def _enter(e):
            card.config(highlightbackground=COLORS["primary"])
            accent.config(bg=COLORS["primary_light"])

        def _leave(e):
            card.config(highlightbackground=COLORS["border"])
            accent.config(bg=COLORS["primary"])

        card.bind("<Enter>", _enter)
        card.bind("<Leave>", _leave)

        return card

    def _build_alerts(self, parent):
        """
        Database theke health alerts fetch kore list e show kore.
        Severity anujaye color diye highlight kora hobe.
        """
        alerts = get_health_alerts()

        alerts_frame = tk.Frame(parent, bg=COLORS["bg_main"])
        alerts_frame.pack(fill="x")

        if not alerts:
            # kono alert nai hole message show koro
            tk.Label(
                alerts_frame,
                text="✅  Ei muhurte kono active health alert nei.",
                font=FONTS["body"],
                bg=COLORS["bg_main"],
                fg=COLORS["success"],
            ).pack(anchor="w", pady=10)
            return

        # severity anujaye colors
        severity_colors = {
            "High":   (COLORS["danger"],  "#FFF0F0"),
            "Medium": (COLORS["warning"], "#FFFAE6"),
            "Low":    (COLORS["info"],    "#EBF5FF"),
        }

        for alert in alerts:
            severity = alert.get("severity", "Medium")
            fg_color, bg_color = severity_colors.get(severity, (COLORS["info"], "#EBF5FF"))

            alert_card = tk.Frame(
                alerts_frame,
                bg=bg_color,
                padx=15,
                pady=12,
                bd=0,
                highlightthickness=1,
                highlightbackground=fg_color,
            )
            alert_card.pack(fill="x", pady=5)

            top_row = tk.Frame(alert_card, bg=bg_color)
            top_row.pack(fill="x")

            # severity badge
            badge = tk.Label(
                top_row,
                text=f"  {severity.upper()}  ",
                font=FONTS["small"],
                bg=fg_color,
                fg="#FFFFFF",
                padx=6,
                pady=2,
            )
            badge.pack(side="left")

            # disease name
            tk.Label(
                top_row,
                text=f"  {alert.get('disease_name', '')}",
                font=FONTS["body_bold"],
                bg=bg_color,
                fg=COLORS["text_primary"],
            ).pack(side="left")

            # location
            tk.Label(
                top_row,
                text=f"  📍 {alert.get('location', '')}",
                font=FONTS["small"],
                bg=bg_color,
                fg=COLORS["text_secondary"],
            ).pack(side="right")

            # description
            desc = alert.get("description", "")
            if desc:
                tk.Label(
                    alert_card,
                    text=desc,
                    font=FONTS["small"],
                    bg=bg_color,
                    fg=COLORS["text_secondary"],
                    anchor="w",
                    wraplength=700,
                ).pack(fill="x", pady=(6, 0))

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()