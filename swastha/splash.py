# splash.py
# eita app start howar age loading screen show korar jonno use kora hocche
# user experience better korar jonno splash screen add kora hoy

import tkinter as tk
from theme import COLORS, FONTS

class SplashScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback

        # splash frame (NOT new window)
        self.frame = tk.Frame(root, bg=COLORS["bg_sidebar"])
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text="Swastha AI Healthcare",
            font=FONTS["heading"],
            bg=COLORS["bg_sidebar"],
            fg=COLORS["primary"]
        ).pack(pady=200)

        # after 2 sec move to app
        self.root.after(2000, self.load_app)

    def load_app(self):
        self.frame.destroy()   # splash remove kora hocche
        self.callback()        # main app call