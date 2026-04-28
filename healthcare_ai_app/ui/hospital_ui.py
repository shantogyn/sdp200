"""
Hospital Finder Page
"""

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, styled_button, scrollable_frame

# Dummy hospital database by city (Bangladesh-focused + global cities)
HOSPITAL_DB = {
    "dhaka": [
        {"name": "Dhaka Medical College Hospital", "type": "Government", "phone": "+880-2-55165087", "address": "Bakshibazar, Dhaka 1000", "specialty": "General / Emergency", "emergency": True},
        {"name": "Bangabandhu Sheikh Mujib Medical University", "type": "Government", "phone": "+880-2-9661063", "address": "Shahbag, Dhaka 1000", "specialty": "Multi-specialty", "emergency": True},
        {"name": "Square Hospitals Ltd.", "type": "Private", "phone": "+880-10616-7890", "address": "18/F, Bir Uttam Qazi Nuruzzaman Sarak, Dhaka", "specialty": "Cardiac, Oncology, Ortho", "emergency": True},
        {"name": "United Hospital Ltd.", "type": "Private", "phone": "+880-10666-5555", "address": "Plot 15, Road 71, Gulshan, Dhaka", "specialty": "Multi-specialty", "emergency": True},
        {"name": "Apollo Hospitals Dhaka", "type": "Private", "phone": "+880-10678-0066", "address": "Plot 81, Block E, Bashundhara, Dhaka", "specialty": "Multi-specialty", "emergency": True},
        {"name": "National Heart Foundation Hospital", "type": "Semi-Govt", "phone": "+880-2-9101595", "address": "Mirpur 2, Dhaka 1216", "specialty": "Cardiology", "emergency": True},
    ],
    "chittagong": [
        {"name": "Chittagong Medical College Hospital", "type": "Government", "phone": "+880-31-616006", "address": "K. B. Fazlul Kader Road, Chittagong", "specialty": "General / Emergency", "emergency": True},
        {"name": "Chevron Clinical Laboratory", "type": "Private", "phone": "+880-31-2850066", "address": "Probortak, Chittagong", "specialty": "Diagnostics & Multi-specialty", "emergency": False},
        {"name": "Park View Hospital", "type": "Private", "phone": "+880-31-2550100", "address": "Khulshi, Chittagong", "specialty": "General & Surgery", "emergency": True},
    ],
    "sylhet": [
        {"name": "Sylhet MAG Osmani Medical College", "type": "Government", "phone": "+880-821-712937", "address": "Mianfool Road, Sylhet 3100", "specialty": "General / Emergency", "emergency": True},
        {"name": "Mount Adora Hospital", "type": "Private", "phone": "+880-821-726700", "address": "Sunnyside East, Sylhet", "specialty": "Multi-specialty", "emergency": True},
    ],
    "rajshahi": [
        {"name": "Rajshahi Medical College Hospital", "type": "Government", "phone": "+880-721-772150", "address": "Rajshahi 6000", "specialty": "General / Emergency", "emergency": True},
        {"name": "Popular Medical Centre", "type": "Private", "phone": "+880-721-810444", "address": "Rajshahi City", "specialty": "General & Diagnostics", "emergency": False},
    ],
    "london": [
        {"name": "St Thomas' Hospital", "type": "NHS", "phone": "+44 20 7188 7188", "address": "Westminster Bridge Rd, London SE1 7EH", "specialty": "General / Emergency", "emergency": True},
        {"name": "King's College Hospital", "type": "NHS", "phone": "+44 20 3299 9000", "address": "Denmark Hill, London SE5 9RS", "specialty": "Multi-specialty", "emergency": True},
        {"name": "The London Clinic", "type": "Private", "phone": "+44 20 7935 4444", "address": "20 Devonshire Pl, London W1G 6BW", "specialty": "Multi-specialty", "emergency": False},
    ],
    "new york": [
        {"name": "NewYork-Presbyterian Hospital", "type": "Private Non-profit", "phone": "+1 212-746-5454", "address": "525 E 68th St, New York, NY 10065", "specialty": "Multi-specialty", "emergency": True},
        {"name": "Mount Sinai Hospital", "type": "Private", "phone": "+1 212-241-6500", "address": "1 Gustave L. Levy Pl, New York, NY 10029", "specialty": "Multi-specialty", "emergency": True},
        {"name": "Bellevue Hospital Center", "type": "Public", "phone": "+1 212-562-4141", "address": "462 1st Ave, New York, NY 10016", "specialty": "General / Trauma", "emergency": True},
    ],
    "mumbai": [
        {"name": "KEM Hospital", "type": "Government", "phone": "+91 22 2410 7000", "address": "Acharya Donde Marg, Parel, Mumbai 400012", "specialty": "General / Emergency", "emergency": True},
        {"name": "Lilavati Hospital", "type": "Private", "phone": "+91 22 2675 1000", "address": "A-791, Bandra Reclamation, Bandra (W), Mumbai", "specialty": "Multi-specialty", "emergency": True},
        {"name": "Tata Memorial Hospital", "type": "Government", "phone": "+91 22 2417 7000", "address": "Dr. E Borges Road, Parel, Mumbai 400012", "specialty": "Oncology", "emergency": True},
    ],
}

TYPE_COLORS = {
    "Government":       COLORS["primary"],
    "Private":          COLORS["green"],
    "NHS":              "#0077BB",
    "Public":           COLORS["primary"],
    "Semi-Govt":        COLORS["teal"],
    "Private Non-profit": COLORS["purple"],
}


class HospitalPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self._build()

    def _build(self):
        hdr = tk.Frame(self.parent, bg=COLORS["primary_dk"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🏥 Hospital Finder",
                 font=FONTS["title"], bg=COLORS["primary_dk"], fg="white"
                 ).place(relx=0.02, rely=0.5, anchor="w")

        main = tk.Frame(self.parent, bg=COLORS["bg"])
        main.pack(fill="both", expand=True)

        # Search panel
        search_card = tk.Frame(main, bg="white")
        search_card.pack(fill="x", padx=16, pady=16)
        si = tk.Frame(search_card, bg="white")
        si.pack(padx=16, pady=14, fill="x")

        tk.Label(si, text="🔍 Search Hospitals by City",
                 font=FONTS["heading"], bg="white", fg=COLORS["primary_dk"]
                 ).pack(anchor="w", pady=(0, 8))

        row = tk.Frame(si, bg="white")
        row.pack(fill="x")

        self.city_var = tk.StringVar()
        entry = tk.Entry(row, textvariable=self.city_var, font=("Segoe UI", 12),
                         relief="solid", bd=1, bg="white", width=30,
                         insertbackground=COLORS["text"])
        entry.pack(side="left", ipady=8, padx=(0, 8))
        entry.bind("<Return>", lambda e: self._search())

        styled_button(row, "🔍 Search", self._search,
                      color=COLORS["primary_dk"], width=12).pack(side="left")

        # Quick city buttons
        quick_frame = tk.Frame(si, bg="white")
        quick_frame.pack(fill="x", pady=(8, 0))
        tk.Label(quick_frame, text="Quick:",
                 font=FONTS["small"], bg="white", fg=COLORS["text_lt"]).pack(side="left")

        cities = ["Dhaka", "Chittagong", "Sylhet", "London", "New York", "Mumbai"]
        for city in cities:
            tk.Button(
                quick_frame, text=city,
                font=FONTS["small"], bg="#EBF5FB", fg=COLORS["primary"],
                relief="flat", cursor="hand2", padx=8, pady=3,
                command=lambda c=city: self._quick_search(c)
            ).pack(side="left", padx=2)

        # Results area
        self.results_frame = tk.Frame(main, bg=COLORS["bg"])
        self.results_frame.pack(fill="both", expand=True, padx=16)
        self._show_placeholder()

    def _quick_search(self, city):
        self.city_var.set(city)
        self._search()

    def _search(self):
        city = self.city_var.get().strip().lower()
        for w in self.results_frame.winfo_children():
            w.destroy()

        if not city:
            tk.Label(self.results_frame, text="Please enter a city name.",
                     font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["red"]).pack(pady=20)
            return

        # Find matches
        matches = {}
        for key, hospitals in HOSPITAL_DB.items():
            if city in key or key in city:
                matches[key] = hospitals

        if not matches:
            tk.Label(
                self.results_frame,
                text=f"🏙️ No results for '{city.title()}'.\nAvailable cities: {', '.join(k.title() for k in HOSPITAL_DB.keys())}",
                font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text_lt"],
                justify="center"
            ).place(relx=0.5, rely=0.4, anchor="center")
            return

        outer, scroll = scrollable_frame(self.results_frame)
        outer.pack(fill="both", expand=True)

        for city_key, hospitals in matches.items():
            tk.Label(scroll, text=f"🏙️ {city_key.title()} — {len(hospitals)} hospitals found",
                     font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text"]
                     ).pack(anchor="w", pady=(8, 4))

            for h in hospitals:
                self._hospital_card(scroll, h)

        tk.Label(scroll,
                 text="📍 Data shown is for reference only. Please verify directly with the hospital.",
                 font=("Segoe UI", 8, "italic"), bg=COLORS["bg"], fg=COLORS["text_lt"]
                 ).pack(anchor="w", pady=(8, 16))

    def _hospital_card(self, parent, h):
        card = tk.Frame(parent, bg="white")
        card.pack(fill="x", pady=4)
        inner = tk.Frame(card, bg="white")
        inner.pack(padx=14, pady=12, fill="x")

        # Name + type badge
        head = tk.Frame(inner, bg="white")
        head.pack(fill="x")

        type_color = TYPE_COLORS.get(h["type"], COLORS["primary"])
        tk.Label(head, text=f"🏥 {h['name']}",
                 font=FONTS["subhead"], bg="white", fg=COLORS["text"]).pack(side="left")

        tk.Label(head, text=f"  {h['type']}  ",
                 font=("Segoe UI", 8, "bold"), bg=type_color, fg="white",
                 padx=4, pady=2).pack(side="left", padx=8)

        if h.get("emergency"):
            tk.Label(head, text=" 🚨 24/7 Emergency ",
                     font=("Segoe UI", 8, "bold"), bg=COLORS["red"], fg="white",
                     padx=4, pady=2).pack(side="left")

        # Details
        details = tk.Frame(inner, bg="white")
        details.pack(fill="x", pady=(6, 0))

        rows = [
            ("📍 Address", h["address"]),
            ("📞 Phone", h["phone"]),
            ("🩺 Specialty", h["specialty"]),
        ]
        for label, val in rows:
            row = tk.Frame(details, bg="white")
            row.pack(anchor="w", pady=1)
            tk.Label(row, text=label, font=FONTS["small"], bg="white",
                     fg=COLORS["text_lt"], width=14, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=FONTS["body"], bg="white",
                     fg=COLORS["text"]).pack(side="left")

        # Google Maps button
        maps_url = f"https://www.google.com/maps/search/{h['name'].replace(' ', '+')}"
        tk.Button(
            inner, text="📍 Open in Maps",
            font=FONTS["small"], bg="#EBF5FB", fg=COLORS["primary"],
            relief="flat", cursor="hand2", padx=8, pady=4,
            command=lambda url=maps_url: self._open_maps(url)
        ).pack(anchor="w", pady=(8, 0))

    def _open_maps(self, url):
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception:
            pass

    def _show_placeholder(self):
        tk.Label(
            self.results_frame,
            text="🏥 Enter a city name above\nto find nearby hospitals",
            font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text_lt"],
            justify="center"
        ).place(relx=0.5, rely=0.4, anchor="center")
