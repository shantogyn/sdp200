# ui/login.py
# eita login screen er UI
# username ar password niye auth_service call kore login kore

import tkinter as tk
from theme import COLORS, FONTS, LAYOUT
from ui.components import make_button, make_input, make_message
from services.auth_service import login_user


class LoginScreen:
    """
    Login screen — user email/password diye login korbe.
    Successful login e dashboard e navigate korbe.
    """

    def __init__(self, root, on_login_success, on_go_signup):
        """
        root: Tkinter root/parent frame
        on_login_success: callback(user_dict) — login er pore call hobe
        on_go_signup: callback — signup page e jaoar jonno
        """
        self.root = root
        self.on_login_success = on_login_success
        self.on_go_signup = on_go_signup

        # main frame — puro screen cover korbe
        self.frame = tk.Frame(root, bg=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):
        """Login UI build kora hocche."""

        # ---- Center container ----
        center = tk.Frame(self.frame, bg=COLORS["bg_main"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        # ---- Logo / header ----
        logo_lbl = tk.Label(
            center,
            text="🏥",
            font=("Segoe UI", 56),
            bg=COLORS["bg_main"],
            fg=COLORS["primary"],
        )
        logo_lbl.pack(pady=(0, 5))

        app_name = tk.Label(
            center,
            text="SWASTHA",
            font=("Segoe UI", 28, "bold"),
            bg=COLORS["bg_main"],
            fg=COLORS["accent_dark"],
        )
        app_name.pack()

        tagline = tk.Label(
            center,
            text="Your AI-Powered Healthcare Companion",
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_secondary"],
        )
        tagline.pack(pady=(3, 20))

        # ---- Card ----
        card = tk.Frame(
            center,
            bg=COLORS["bg_card"],
            bd=0,
            padx=40,
            pady=35,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        card.pack(ipadx=10)

        card_title = tk.Label(
            card,
            text="Sign in to your account",
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        )
        card_title.pack(pady=(0, 20))

        # ---- Username input ----
        uname_frame, self.uname_entry = make_input(card, "Username", width=32)
        uname_frame.pack(fill="x", pady=5)

        # ---- Password input ----
        pw_frame, self.pw_entry = make_input(card, "Password", show="*", width=32)
        pw_frame.pack(fill="x", pady=5)

        # ---- Message label (error/success show hobar jonno) ----
        self.msg_var = tk.StringVar()
        self.msg_lbl = tk.Label(
            card,
            textvariable=self.msg_var,
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["danger"],
            wraplength=300,
        )
        self.msg_lbl.pack(pady=(5, 0))

        # ---- Login button ----
        login_btn = make_button(
            card,
            text="  🔓  Login  ",
            command=self._handle_login,
            width=30,
        )
        login_btn.pack(pady=(15, 8), ipady=4)

        # Enter key diye o login kora jabe
        self.root.bind("<Return>", lambda e: self._handle_login())

        # ---- Signup link ----
        bottom_frame = tk.Frame(card, bg=COLORS["bg_card"])
        bottom_frame.pack(pady=(5, 0))

        tk.Label(
            bottom_frame,
            text="Account nei?",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        ).pack(side="left")

        signup_link = tk.Label(
            bottom_frame,
            text=" Sign up",
            font=(*FONTS["small"][:2], "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"],
            cursor="hand2",
        )
        signup_link.pack(side="left")
        signup_link.bind("<Button-1>", lambda e: self.on_go_signup())

    def _handle_login(self):
        """
        Login button press e call hobe.
        Input validate kore auth_service theke login kore.
        """
        username = self.uname_entry.get().strip()
        password = self.pw_entry.get().strip()

        # empty check
        if not username or not password:
            self.msg_var.set("⚠  Username ar password dite hobe!")
            self.msg_lbl.config(fg=COLORS["warning"])
            return

        # auth service call kora hocche
        result = login_user(username, password)

        if result["success"]:
            # success — password field clear kore dashboard e jao
            self.pw_entry.delete(0, tk.END)
            self.msg_var.set("")
            self.on_login_success(result["user"])  # user dict pass kora hocche
        else:
            # failure — error message show koro
            self.msg_var.set(f"✗  {result['message']}")
            self.msg_lbl.config(fg=COLORS["danger"])

    def show(self):
        """Screen show kore."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Screen hide kore."""
        self.frame.pack_forget()
        # Enter binding remove koro — onno screen e conflict na hok
        try:
            self.root.unbind("<Return>")
        except Exception:
            pass