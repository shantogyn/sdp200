"""
Main Window - Dashboard with sidebar navigation
"""

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS
from utils.database import DatabaseManager
from utils.notifier import ReminderNotifier


class MainWindow:
    """Main application window with sidebar navigation."""

    MENU_ITEMS = [
        ("🏠", "Dashboard",   "dashboard"),
        ("🦠", "Disease Predict", "disease"),
        ("🤖", "Medical Chatbot", "chatbot"),
        ("⏰", "Med Reminders",   "reminder"),
        ("🧪", "Lab Analyzer",    "lab"),
        ("🥗", "Diet Planner",    "diet"),
        ("🧘", "Mental Health",   "mental"),
        ("🚑", "First Aid",       "firstaid"),
        ("🏥", "Hospital Finder", "hospital"),
        ("📚", "Disease Info",    "info"),
    ]

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AI Smart Healthcare Assistant")
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        self.root.configure(bg=COLORS["sidebar"])

        # Try to set icon
        try:
            self.root.iconbitmap("")
        except Exception:
            pass

        self.db = DatabaseManager()
        self.notifier = ReminderNotifier(self.db)
        self.notifier.start()

        self.active_page = None
        self.sidebar_btns = {}
        self.frames = {}

        self._build_layout()
        self._load_all_pages()
        self._show_page("dashboard")

    # ── Layout ─────────────────────────────────────────────────────────────────

    def _build_layout(self):
        """Build sidebar + content area."""
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=COLORS["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo area
        logo_frame = tk.Frame(self.sidebar, bg=COLORS["primary_dk"], height=80)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        tk.Label(
            logo_frame,
            text="🏥 MediAssist",
            font=("Segoe UI", 14, "bold"),
            bg=COLORS["primary_dk"],
            fg="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Separator
        tk.Frame(self.sidebar, bg=COLORS["sidebar_lt"], height=1).pack(fill="x")

        # Nav scroll area
        nav_canvas = tk.Canvas(self.sidebar, bg=COLORS["sidebar"], highlightthickness=0)
        nav_canvas.pack(fill="both", expand=True, pady=(8, 0))

        nav_inner = tk.Frame(nav_canvas, bg=COLORS["sidebar"])
        nav_canvas.create_window((0, 0), window=nav_inner, anchor="nw")

        # Menu buttons
        for icon, label, key in self.MENU_ITEMS:
            self._make_nav_btn(nav_inner, icon, label, key)

        # Bottom info
        bottom = tk.Frame(self.sidebar, bg=COLORS["sidebar_lt"], height=50)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)
        tk.Label(
            bottom,
            text="v1.0 • AI Healthcare",
            font=FONTS["small"],
            bg=COLORS["sidebar_lt"],
            fg="#7F8C8D"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Content area
        self.content = tk.Frame(self.root, bg=COLORS["bg"])
        self.content.pack(side="right", fill="both", expand=True)

    def _make_nav_btn(self, parent, icon, label, key):
        """Create a sidebar navigation button."""
        frame = tk.Frame(parent, bg=COLORS["sidebar"], cursor="hand2")
        frame.pack(fill="x", pady=1)

        icon_lbl = tk.Label(frame, text=icon, font=("Segoe UI", 13),
                            bg=COLORS["sidebar"], fg="white", width=3)
        icon_lbl.pack(side="left", padx=(12, 4), pady=10)

        text_lbl = tk.Label(frame, text=label, font=("Segoe UI", 10),
                            bg=COLORS["sidebar"], fg="#BDC3C7", anchor="w")
        text_lbl.pack(side="left", fill="x", expand=True, pady=10)

        # Hover effect
        def on_enter(e, f=frame, il=icon_lbl, tl=text_lbl):
            if self.active_page != key:
                f.config(bg=COLORS["sidebar_lt"])
                il.config(bg=COLORS["sidebar_lt"])
                tl.config(bg=COLORS["sidebar_lt"])

        def on_leave(e, f=frame, il=icon_lbl, tl=text_lbl):
            if self.active_page != key:
                f.config(bg=COLORS["sidebar"])
                il.config(bg=COLORS["sidebar"])
                tl.config(bg=COLORS["sidebar"])

        def on_click(e=None, k=key):
            self._show_page(k)

        for widget in (frame, icon_lbl, text_lbl):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

        self.sidebar_btns[key] = (frame, icon_lbl, text_lbl)

    def _highlight_nav(self, key):
        """Highlight the active nav item."""
        for k, (f, il, tl) in self.sidebar_btns.items():
            if k == key:
                f.config(bg=COLORS["primary"])
                il.config(bg=COLORS["primary"], fg="white")
                tl.config(bg=COLORS["primary"], fg="white", font=("Segoe UI", 10, "bold"))
            else:
                f.config(bg=COLORS["sidebar"])
                il.config(bg=COLORS["sidebar"], fg="white")
                tl.config(bg=COLORS["sidebar"], fg="#BDC3C7", font=("Segoe UI", 10))

    # ── Pages ──────────────────────────────────────────────────────────────────

    def _load_all_pages(self):
        """Import and instantiate all page modules."""
        from ui.dashboard_ui import DashboardPage
        from ui.disease_ui import DiseasePage
        from ui.chatbot_ui import ChatbotPage
        from ui.reminder_ui import ReminderPage
        from ui.lab_ui import LabPage
        from ui.diet_ui import DietPage
        from ui.mental_ui import MentalPage
        from ui.emergency_ui import EmergencyPage
        from ui.hospital_ui import HospitalPage
        from ui.info_ui import InfoPage

        page_classes = {
            "dashboard": DashboardPage,
            "disease":   DiseasePage,
            "chatbot":   ChatbotPage,
            "reminder":  ReminderPage,
            "lab":       LabPage,
            "diet":      DietPage,
            "mental":    MentalPage,
            "firstaid":  EmergencyPage,
            "hospital":  HospitalPage,
            "info":      InfoPage,
        }

        for key, cls in page_classes.items():
            frame = tk.Frame(self.content, bg=COLORS["bg"])
            frame.place(relwidth=1, relheight=1)
            try:
                page = cls(frame, self.db)
                self.frames[key] = frame
            except Exception as e:
                # Show error page if a module fails to load
                tk.Label(
                    frame, text=f"⚠️ Error loading {key}:\n{e}",
                    bg=COLORS["bg"], fg=COLORS["red"],
                    font=FONTS["body"], wraplength=400
                ).pack(expand=True)
                self.frames[key] = frame

    def _show_page(self, key):
        """Bring a page frame to front."""
        self.active_page = key
        self._highlight_nav(key)
        if key in self.frames:
            self.frames[key].lift()
