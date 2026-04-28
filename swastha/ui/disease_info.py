# ui/disease_info.py
# eita disease information center er UI
# database theke disease er symptoms, causes, prevention, treatment show kore

import tkinter as tk
from theme import COLORS, FONTS
from ui.components import make_scrollable_frame, make_info_row
from services.disease_service import get_all_diseases, get_disease_by_name


class DiseaseInfoScreen:
    """
    Disease information center screen.
    Sob diseases er list dekhabe, click korle details show hobe.
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
            text="📋  Disease Information Center",
            font=FONTS["heading"],
            bg=COLORS["accent_dark"],
            fg=COLORS["text_light"],
        ).pack(side="left")

        # main layout
        main = tk.Frame(self.frame, bg=COLORS["bg_main"], padx=20, pady=15)
        main.pack(fill="both", expand=True)

        # ---- LEFT: Disease list + search ----
        left = tk.Frame(
            main, bg=COLORS["bg_card"],
            highlightthickness=1, highlightbackground=COLORS["border"],
            width=230,
        )
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        # search box
        search_frame = tk.Frame(left, bg=COLORS["bg_card"], padx=10, pady=10)
        search_frame.pack(fill="x")

        tk.Label(
            search_frame,
            text="🔍  Disease khujun:",
            font=FONTS["body_bold"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)  # typing e auto search

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"],
            insertbackground=COLORS["text_primary"],
        )
        search_entry.pack(fill="x", ipady=6)

        tk.Frame(left, bg=COLORS["border"], height=1).pack(fill="x")

        # disease list scrollable area
        self.list_scroll, self.list_frame = make_scrollable_frame(left)
        self.list_scroll.pack(fill="both", expand=True)

        # diseases load kora hocche
        self.all_diseases = get_all_diseases()
        self._render_disease_list(self.all_diseases)

        # ---- RIGHT: Disease details ----
        right = tk.Frame(main, bg=COLORS["bg_main"])
        right.pack(side="left", fill="both", expand=True)

        self.details_scroll, self.details_frame = make_scrollable_frame(right)
        self.details_scroll.pack(fill="both", expand=True)

        # initial placeholder
        tk.Label(
            self.details_frame,
            text="👈  Bame ekটা disease select korun details dekhte",
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_muted"],
        ).pack(expand=True, pady=60)

    def _render_disease_list(self, diseases):
        """Disease list left panel e render kore."""
        for w in self.list_frame.winfo_children():
            w.destroy()

        if not diseases:
            tk.Label(
                self.list_frame,
                text="Kono disease pawa jacche na",
                font=FONTS["small"],
                bg=COLORS["bg_card"],
                fg=COLORS["text_muted"],
            ).pack(pady=20)
            return

        for disease in diseases:
            btn = tk.Button(
                self.list_frame,
                text=f"  🏥  {disease['name']}",
                command=lambda d=disease: self._show_disease(d),
                font=FONTS["sidebar"],
                bg=COLORS["bg_card"],
                fg=COLORS["text_primary"],
                relief="flat",
                anchor="w",
                padx=10,
                pady=9,
                cursor="hand2",
                activebackground=COLORS["bg_main"],
                bd=0,
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["bg_main"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["bg_card"]))

            tk.Frame(self.list_frame, bg=COLORS["border"], height=1).pack(fill="x", padx=8)

    def _on_search(self, *args):
        """Search box typing e disease list filter kore."""
        query = self.search_var.get().strip().lower()

        if not query:
            self._render_disease_list(self.all_diseases)
        else:
            filtered = [
                d for d in self.all_diseases
                if query in d["name"].lower()
            ]
            self._render_disease_list(filtered)

    def _show_disease(self, disease):
        """Disease select korle detail panel e info show kore."""
        # clear previous
        for w in self.details_frame.winfo_children():
            w.destroy()

        content = tk.Frame(self.details_frame, bg=COLORS["bg_main"], padx=5, pady=5)
        content.pack(fill="both", expand=True)

        # disease header card
        header_card = tk.Frame(
            content,
            bg=COLORS["accent_dark"],
            padx=22,
            pady=18,
        )
        header_card.pack(fill="x", pady=(0, 15))

        tk.Label(
            header_card,
            text=f"🏥  {disease['name']}",
            font=("Segoe UI", 18, "bold"),
            bg=COLORS["accent_dark"],
            fg=COLORS["text_light"],
        ).pack(anchor="w")

        desc = disease.get("description", "")
        if desc:
            tk.Label(
                header_card,
                text=desc,
                font=FONTS["body"],
                bg=COLORS["accent_dark"],
                fg=COLORS["text_muted"],
                anchor="w",
                wraplength=600,
                justify="left",
            ).pack(anchor="w", pady=(8, 0))

        # info sections
        sections = [
            ("🤒  Symptoms (Lakkhan)", disease.get("symptoms", ""),      COLORS["warning"]),
            ("⚡  Causes (Karon)",      disease.get("causes", ""),         COLORS["danger"]),
            ("🛡  Prevention (Protirodh)", disease.get("prevention", ""), COLORS["success"]),
            ("💊  Treatment (Chikitsa)", disease.get("treatment", ""),    COLORS["info"]),
        ]

        for section_title, section_content, accent_color in sections:
            if not section_content:
                continue

            section_card = tk.Frame(
                content,
                bg=COLORS["bg_card"],
                padx=20,
                pady=15,
                highlightthickness=1,
                highlightbackground=COLORS["border"],
            )
            section_card.pack(fill="x", pady=6)

            # section title with color accent
            title_row = tk.Frame(section_card, bg=COLORS["bg_card"])
            title_row.pack(fill="x", pady=(0, 8))

            tk.Frame(title_row, bg=accent_color, width=4).pack(side="left", fill="y")

            tk.Label(
                title_row,
                text=f"  {section_title}",
                font=FONTS["subheading"],
                bg=COLORS["bg_card"],
                fg=COLORS["text_primary"],
            ).pack(side="left")

            # content — comma-separated thakle bullet points e convert korbo
            items = [i.strip() for i in section_content.split(",") if i.strip()]

            if len(items) > 1:
                for item in items:
                    tk.Label(
                        section_card,
                        text=f"  •  {item}",
                        font=FONTS["body"],
                        bg=COLORS["bg_card"],
                        fg=COLORS["text_primary"],
                        anchor="w",
                        justify="left",
                        wraplength=580,
                    ).pack(fill="x", pady=2)
            else:
                tk.Label(
                    section_card,
                    text=section_content,
                    font=FONTS["body"],
                    bg=COLORS["bg_card"],
                    fg=COLORS["text_primary"],
                    anchor="w",
                    wraplength=580,
                    justify="left",
                ).pack(fill="x")

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()