"""
Mental Health Support Page
"""

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, scrollable_frame

MOOD_DATA = {
    "Happy 😊": {
        "color": "#F1C40F",
        "messages": [
            "Wonderful! Keep spreading that positivity! 🌟",
            "Your happiness is contagious — share it with someone today! 💛",
            "Amazing energy! Channel it into something creative or productive!",
        ],
        "tips": [
            "📓 Journal your happy moments to revisit later",
            "🤝 Reach out to a friend and brighten their day",
            "🏃 Use this energy for a workout or walk",
            "🎯 Set a new goal while motivation is high",
        ],
        "exercise": "Try a gratitude meditation: list 5 things you're grateful for right now."
    },
    "Sad 😢": {
        "color": "#3498DB",
        "messages": [
            "It's okay to feel sad. Your feelings are valid. 💙",
            "This too shall pass. You are stronger than you know. 🌊",
            "Be gentle with yourself today. Small steps forward are enough. 🌸",
        ],
        "tips": [
            "🚶 Take a gentle walk in nature",
            "📞 Talk to someone you trust",
            "🎵 Listen to music that comforts you",
            "🛁 Take care of your basic needs: eat, hydrate, rest",
            "📝 Write down your feelings in a journal",
        ],
        "exercise": "Box Breathing: Inhale 4 counts → Hold 4 → Exhale 4 → Hold 4. Repeat 5 times."
    },
    "Stressed 😖": {
        "color": "#E67E22",
        "messages": [
            "Stress is temporary. Take it one step at a time. 🌿",
            "You've handled tough situations before — you can handle this too. 💪",
            "Pause, breathe, and remember: not everything needs to be solved right now.",
        ],
        "tips": [
            "🧘 Try 5 minutes of deep breathing",
            "📋 Write down your stressors and tackle them one by one",
            "🚫 Say no to non-essential tasks today",
            "☕ Take a break — step away from screens",
            "🏃 Physical activity reduces cortisol levels significantly",
        ],
        "exercise": "4-7-8 Breathing: Inhale 4 counts → Hold 7 → Exhale slowly 8 counts. Repeat 4×."
    },
    "Angry 😡": {
        "color": "#E74C3C",
        "messages": [
            "Anger is natural. What you do with it makes the difference. 🌬️",
            "Take a moment before reacting. Your response is your power. 🔥",
            "It's okay to feel angry. Channel it constructively. 💪",
        ],
        "tips": [
            "🚶 Remove yourself from the situation temporarily",
            "💨 Take 10 slow deep breaths before responding",
            "🏋️ Physical exercise is a powerful anger release",
            "✍️ Write out your frustrations in a private journal",
            "🎵 Music can shift your emotional state quickly",
        ],
        "exercise": "Progressive Muscle Relaxation: Tense each muscle group for 5s, then release. Start from feet to head."
    },
    "Anxious 😰": {
        "color": "#9B59B6",
        "messages": [
            "Anxiety is your body preparing — you can redirect that energy. 🦋",
            "You are safe right now, in this moment. 💜",
            "Ground yourself: 5 things you see, 4 you hear, 3 you can touch.",
        ],
        "tips": [
            "🌍 Try the 5-4-3-2-1 grounding technique",
            "📵 Limit news and social media today",
            "🛌 Maintain a regular sleep schedule",
            "☕ Reduce caffeine intake",
            "🧘 Guided meditation apps (Headspace, Calm) can help",
        ],
        "exercise": "5-4-3-2-1 Grounding: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste."
    },
    "Tired 😴": {
        "color": "#1ABC9C",
        "messages": [
            "Rest is productive. Your body is asking for what it needs. 😴",
            "Fatigue is a signal — honor it with rest and care. 🌙",
            "Even a short rest can restore your energy. Be kind to yourself.",
        ],
        "tips": [
            "💤 Aim for 7-9 hours of sleep tonight",
            "🚶 A short walk can boost energy levels",
            "💧 Dehydration causes fatigue — drink water now",
            "🍎 Eat a nutritious snack (not sugar)",
            "🧘 A 10-minute power nap can restore alertness",
        ],
        "exercise": "Body Scan Relaxation: Lie down and mentally scan from head to toe, releasing tension in each area."
    },
}

CRISIS_RESOURCES = [
    ("🆘", "Emergency", "Call 999 / 911", "#E74C3C"),
    ("📞", "Crisis Line",  "KAAN Pete Roi (BD): 01779-554391", "#E67E22"),
    ("💬", "Talk to Someone", "Befrienders Worldwide: befrienders.org", "#3498DB"),
    ("🏥", "Mental Health Help", "Consult a psychiatrist or therapist", "#9B59B6"),
]


class MentalPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self._build()

    def _build(self):
        hdr = tk.Frame(self.parent, bg="#8E44AD", height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🧘 Mental Health Support Center",
                 font=FONTS["title"], bg="#8E44AD", fg="white"
                 ).place(relx=0.02, rely=0.5, anchor="w")

        outer, content = scrollable_frame(self.parent)
        outer.pack(fill="both", expand=True)

        # Mood selector
        mood_card = tk.Frame(content, bg="white")
        mood_card.pack(fill="x", padx=16, pady=(16, 8))
        mi = tk.Frame(mood_card, bg="white")
        mi.pack(padx=16, pady=14, fill="x")

        tk.Label(mi, text="💭 How are you feeling today?",
                 font=FONTS["heading"], bg="white", fg="#8E44AD").pack(anchor="w", pady=(0, 10))

        mood_grid = tk.Frame(mi, bg="white")
        mood_grid.pack(fill="x")

        self.mood_var = tk.StringVar(value="")
        self.mood_result_frame = tk.Frame(content, bg=COLORS["bg"])
        self.mood_result_frame.pack(fill="x", padx=16)

        moods = list(MOOD_DATA.keys())
        cols = 3
        for i, mood in enumerate(moods):
            row_i = i // cols
            col_i = i % cols
            color = MOOD_DATA[mood]["color"]

            btn = tk.Button(
                mood_grid, text=mood,
                font=("Segoe UI", 11, "bold"),
                bg=color, fg="white",
                relief="flat", cursor="hand2",
                padx=12, pady=10,
                command=lambda m=mood: self._show_mood(m)
            )
            btn.grid(row=row_i, column=col_i, padx=4, pady=4, sticky="ew")
            mood_grid.columnconfigure(col_i, weight=1)

        # Crisis resources
        self._crisis_section(content)

    def _show_mood(self, mood):
        for w in self.mood_result_frame.winfo_children():
            w.destroy()

        data = MOOD_DATA[mood]
        color = data["color"]
        import random

        # Main response card
        card = tk.Frame(self.mood_result_frame, bg="white")
        card.pack(fill="x", pady=(8, 4))
        inner = tk.Frame(card, bg="white")
        inner.pack(padx=16, pady=14, fill="x")

        # Color bar
        tk.Frame(card, bg=color, height=4).pack(fill="x", side="top")

        tk.Label(inner, text=f"You selected: {mood}",
                 font=FONTS["subhead"], bg="white", fg=color).pack(anchor="w")
        tk.Label(inner, text=random.choice(data["messages"]),
                 font=("Segoe UI", 11, "italic"), bg="white", fg=COLORS["text"],
                 wraplength=680, justify="left").pack(anchor="w", pady=(6, 0))

        # Tips card
        tips_card = tk.Frame(self.mood_result_frame, bg="white")
        tips_card.pack(fill="x", pady=4)
        ti = tk.Frame(tips_card, bg="white")
        ti.pack(padx=16, pady=14, fill="x")

        tk.Label(ti, text="💡 Helpful Tips for You",
                 font=FONTS["subhead"], bg="white", fg=COLORS["primary"]).pack(anchor="w", pady=(0, 6))
        for tip in data["tips"]:
            tk.Label(ti, text=tip, font=FONTS["body"],
                     bg="white", fg=COLORS["text"],
                     wraplength=660, justify="left").pack(anchor="w", pady=2)

        # Breathing exercise card
        ex_card = tk.Frame(self.mood_result_frame, bg="#F4ECF7")
        ex_card.pack(fill="x", pady=4)
        ei = tk.Frame(ex_card, bg="#F4ECF7")
        ei.pack(padx=16, pady=14, fill="x")

        tk.Label(ei, text="🧘 Recommended Exercise",
                 font=FONTS["subhead"], bg="#F4ECF7", fg="#8E44AD").pack(anchor="w", pady=(0, 4))
        tk.Label(ei, text=data["exercise"],
                 font=FONTS["body"], bg="#F4ECF7", fg=COLORS["text"],
                 wraplength=660, justify="left").pack(anchor="w")

    def _crisis_section(self, parent):
        card = tk.Frame(parent, bg="#FDEDEC")
        card.pack(fill="x", padx=16, pady=(12, 16))
        inner = tk.Frame(card, bg="#FDEDEC")
        inner.pack(padx=16, pady=12, fill="x")

        tk.Label(inner, text="🆘 Crisis Support Resources",
                 font=FONTS["subhead"], bg="#FDEDEC", fg=COLORS["red"]).pack(anchor="w", pady=(0, 8))

        grid = tk.Frame(inner, bg="#FDEDEC")
        grid.pack(fill="x")

        for i, (icon, label, detail, color) in enumerate(CRISIS_RESOURCES):
            cell = tk.Frame(grid, bg="white")
            cell.grid(row=0, column=i, padx=4, pady=2, sticky="nsew")
            grid.columnconfigure(i, weight=1)

            ci = tk.Frame(cell, bg="white")
            ci.pack(padx=10, pady=10)
            tk.Label(ci, text=icon, font=("Segoe UI", 20), bg="white").pack()
            tk.Label(ci, text=label, font=FONTS["subhead"], bg="white", fg=color).pack()
            tk.Label(ci, text=detail, font=FONTS["small"], bg="white",
                     fg=COLORS["text_lt"], wraplength=140, justify="center").pack()
