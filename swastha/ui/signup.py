# eita signup / registration screen er UI
# notun user account create korbe ekhane

import tkinter as tk
from theme import COLORS, FONTS
from ui.components import make_button, make_input
from services.auth_service import register_user


class SignupScreen:
    """
    Signup screen — notun user register korbe.
    Successful registration e login screen e navigate korbe.
    """

    def __init__(self, root, on_signup_success, on_go_login):
        """
        root: Tkinter parent window
        on_signup_success: callback — signup sesh hole call hobe
        on_go_login: callback — login page e jaoar jonno
        """
        self.root = root
        self.on_signup_success = on_signup_success
        self.on_go_login = on_go_login

        self.frame = tk.Frame(root, bg=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):
        """Signup UI build kora hocche."""

        center = tk.Frame(self.frame, bg=COLORS["bg_main"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        # ---- Header ----
        tk.Label(
            center,
            text="🏥",
            font=("Segoe UI", 48),
            bg=COLORS["bg_main"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 5))

        tk.Label(
            center,
            text="Join SWASTHA",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_main"],
            fg=COLORS["accent_dark"],
        ).pack()

        tk.Label(
            center,
            text="Create your free health account",
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_secondary"],
        ).pack(pady=(3, 20))

        # ---- Card ----
        card = tk.Frame(
            center,
            bg=COLORS["bg_card"],
            padx=40,
            pady=35,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        card.pack(ipadx=10)

        tk.Label(
            card,
            text="Create New Account",
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(pady=(0, 15))

        # ---- Username ----
        uf, self.uname_entry = make_input(card, "Username *", width=32)
        uf.pack(fill="x", pady=5)

        # ---- Email (optional) ----
        ef, self.email_entry = make_input(card, "Email (optional)", width=32)
        ef.pack(fill="x", pady=5)

        # ---- Password ----
        pf, self.pw_entry = make_input(card, "Password * (min 6 chars)", show="*", width=32)
        pf.pack(fill="x", pady=5)

        # ---- Confirm Password ----
        cf, self.confirm_entry = make_input(card, "Confirm Password *", show="*", width=32)
        cf.pack(fill="x", pady=5)

        # ---- Message label ----
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

        # ---- Signup button ----
        signup_btn = make_button(
            card,
            text="  ✅  Create Account  ",
            command=self._handle_signup,
            width=30,
        )
        signup_btn.pack(pady=(15, 8), ipady=4)

        # ---- Login link ----
        bottom = tk.Frame(card, bg=COLORS["bg_card"])
        bottom.pack(pady=(5, 0))

        tk.Label(
            bottom,
            text="Already account ache?",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        ).pack(side="left")

        login_link = tk.Label(
            bottom,
            text=" Login",
            font=(*FONTS["small"][:2], "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"],
            cursor="hand2",
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.on_go_login())

    def _handle_signup(self):
        """
        Signup button press e call hobe.
        Validation kore auth_service register kore.
        """
        username = self.uname_entry.get().strip()
        email    = self.email_entry.get().strip()
        password = self.pw_entry.get().strip()
        confirm  = self.confirm_entry.get().strip()

        # ---- Validation ----
        if not username or not password:
            self._show_msg("⚠  Username ar password dite hobe!", "warning")
            return

        if password != confirm:
            self._show_msg("✗  Password duto match korche na!", "error")
            return

        if len(password) < 6:
            self._show_msg("✗  Password obosshoi 6 character er beshi hobe!", "error")
            return

        # auth service call kora hocche
        result = register_user(username, password, email)

        if result["success"]:
            self._show_msg(f"✓  {result['message']}", "success")
            # 1.5 second por login page e jao
            self.root.after(1500, self.on_signup_success)
        else:
            self._show_msg(f"✗  {result['message']}", "error")

    def _show_msg(self, text, msg_type="error"):
        """Message show kore suitble color e."""
        color_map = {
            "success": COLORS["success"],
            "error":   COLORS["danger"],
            "warning": COLORS["warning"],
        }
        self.msg_var.set(text)
        self.msg_lbl.config(fg=color_map.get(msg_type, COLORS["danger"]))

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()