"""
Medical Chatbot Page - WhatsApp-style chat UI
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS
from models.chatbot_model import MedicalChatbot


class ChatbotPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.bot = MedicalChatbot()
        self._build()
        self._welcome()

    def _build(self):
        # Header
        hdr = tk.Frame(self.parent, bg=COLORS["green"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="🤖", font=("Segoe UI", 22),
                 bg=COLORS["green"]).place(relx=0.01, rely=0.5, anchor="w")
        tk.Label(hdr, text=" MediBot — AI Medical Chatbot",
                 font=FONTS["title"], bg=COLORS["green"], fg="white"
                 ).place(relx=0.06, rely=0.5, anchor="w")

        status = tk.Frame(hdr, bg=COLORS["green"])
        status.place(relx=0.98, rely=0.5, anchor="e")
        tk.Frame(status, bg="#2ECC71", width=8, height=8).pack(side="left")
        tk.Label(status, text=" Online", font=FONTS["small"],
                 bg=COLORS["green"], fg="#D5F5E3").pack(side="left")

        # Chat canvas
        canvas_frame = tk.Frame(self.parent, bg="#E8F5E9")
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="#E8F5E9", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.chat_frame = tk.Frame(self.canvas, bg="#E8F5E9")

        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Input bar
        input_bar = tk.Frame(self.parent, bg="white", height=60)
        input_bar.pack(fill="x", side="bottom")
        input_bar.pack_propagate(False)

        self.input_var = tk.StringVar()
        entry = tk.Entry(
            input_bar, textvariable=self.input_var,
            font=("Segoe UI", 11), relief="flat",
            bg="#F2F2F2", fg=COLORS["text"],
            insertbackground=COLORS["text"]
        )
        entry.pack(side="left", fill="both", expand=True, padx=12, pady=10, ipady=6)
        entry.bind("<Return>", lambda e: self._send())

        send_btn = tk.Button(
            input_bar, text="➤", font=("Segoe UI", 14, "bold"),
            bg=COLORS["green"], fg="white", relief="flat",
            cursor="hand2", width=3,
            command=self._send
        )
        send_btn.pack(side="right", padx=8, pady=8, fill="y")

        # Quick prompts
        quick_frame = tk.Frame(self.parent, bg="#F1F8E9")
        quick_frame.pack(fill="x", side="bottom")

        prompts = ["💊 About fever", "🤒 Cold symptoms", "❤️ Heart health",
                   "😴 Sleep tips", "🏃 Exercise", "🧠 Mental health"]
        for p in prompts:
            tk.Button(
                quick_frame, text=p,
                font=FONTS["small"], bg="white", fg=COLORS["green"],
                relief="flat", cursor="hand2", padx=6, pady=3,
                command=lambda t=p: self._quick_send(t)
            ).pack(side="left", padx=3, pady=4)

    def _welcome(self):
        welcome = ("👋 Hello! I'm **MediBot**, your AI medical assistant!\n\n"
                   "I can help you with:\n"
                   "• Symptom information\n"
                   "• Health advice & tips\n"
                   "• Disease information\n"
                   "• Medication guidance\n\n"
                   "What health question can I answer today? 😊")
        self._add_message("bot", welcome)

    def _send(self):
        msg = self.input_var.get().strip()
        if not msg:
            return
        self.input_var.set("")
        self._add_message("user", msg)
        self.db.save_message("user", msg)
        # Typing animation then respond
        threading.Thread(target=self._bot_reply, args=(msg,), daemon=True).start()

    def _quick_send(self, prompt):
        # Strip emoji prefix
        clean = prompt.split(" ", 1)[1] if " " in prompt else prompt
        self.input_var.set(clean)
        self._send()

    def _bot_reply(self, msg):
        """Show typing animation then render response."""
        typing_id = self._show_typing()
        time.sleep(0.8)
        response = self.bot.get_response(msg)
        self.parent.after(0, lambda: self._remove_typing(typing_id))
        self.parent.after(50, lambda: self._add_message("bot", response))
        self.db.save_message("bot", response)

    def _add_message(self, role, text):
        is_user = role == "user"
        row = tk.Frame(self.chat_frame, bg="#E8F5E9")
        row.pack(fill="x", pady=3, padx=10)

        if is_user:
            bubble_frame = tk.Frame(row, bg="#E8F5E9")
            bubble_frame.pack(anchor="e")

            bubble = tk.Frame(bubble_frame, bg=COLORS["green"])
            bubble.pack(side="right", padx=(60, 0))
        else:
            bubble_frame = tk.Frame(row, bg="#E8F5E9")
            bubble_frame.pack(anchor="w")

            # Avatar
            tk.Label(bubble_frame, text="🤖", font=("Segoe UI", 14),
                     bg="#E8F5E9").pack(side="left", anchor="n", pady=4)

            bubble = tk.Frame(bubble_frame, bg="white")
            bubble.pack(side="left", padx=(4, 60))

        lbl = tk.Label(
            bubble, text=text,
            font=FONTS["body"],
            bg=COLORS["green"] if is_user else "white",
            fg="white" if is_user else COLORS["text"],
            wraplength=480,
            justify="left",
            padx=12, pady=8
        )
        lbl.pack()

        self._scroll_bottom()

    def _show_typing(self):
        row = tk.Frame(self.chat_frame, bg="#E8F5E9")
        row.pack(fill="x", pady=3, padx=10)
        row_id = id(row)

        tk.Label(row, text="🤖", font=("Segoe UI", 14),
                 bg="#E8F5E9").pack(side="left", anchor="n", pady=4)

        bubble = tk.Frame(row, bg="white")
        bubble.pack(side="left")
        tk.Label(bubble, text="● ● ●  typing...",
                 font=("Segoe UI", 10, "italic"),
                 bg="white", fg=COLORS["text_lt"],
                 padx=12, pady=8).pack()

        self._typing_widget = row
        self._scroll_bottom()
        return row_id

    def _remove_typing(self, row_id):
        if hasattr(self, "_typing_widget"):
            try:
                self._typing_widget.destroy()
            except Exception:
                pass

    def _scroll_bottom(self):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
