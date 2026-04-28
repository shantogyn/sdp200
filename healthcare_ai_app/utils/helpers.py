"""
Helpers - Shared utility functions for the Healthcare Assistant
"""

import tkinter as tk
from tkinter import ttk


# ── Color Palette ──────────────────────────────────────────────────────────────
COLORS = {
    "primary":    "#2E86C1",
    "primary_dk": "#1A5276",
    "primary_lt": "#5DADE2",
    "green":      "#28B463",
    "green_dk":   "#1E8449",
    "red":        "#E74C3C",
    "orange":     "#E67E22",
    "yellow":     "#F1C40F",
    "purple":     "#8E44AD",
    "teal":       "#17A589",
    "sidebar":    "#1B2631",
    "sidebar_lt": "#2C3E50",
    "bg":         "#F4F6F7",
    "card":       "#FFFFFF",
    "text":       "#2C3E50",
    "text_lt":    "#7F8C8D",
    "border":     "#D5D8DC",
    "hover":      "#EBF5FB",
}

FONTS = {
    "title":    ("Segoe UI", 22, "bold"),
    "heading":  ("Segoe UI", 14, "bold"),
    "subhead":  ("Segoe UI", 12, "bold"),
    "body":     ("Segoe UI", 10),
    "small":    ("Segoe UI", 9),
    "mono":     ("Consolas", 10),
    "btn":      ("Segoe UI", 10, "bold"),
    "big_icon": ("Segoe UI", 28),
}


def make_card(parent, padx=16, pady=16, **kwargs):
    """Create a white card frame with border styling."""
    frame = tk.Frame(
        parent,
        bg=COLORS["card"],
        relief="flat",
        bd=0,
        **kwargs
    )
    frame.pack(fill="x", padx=padx, pady=(0, 12))
    # Inner padding frame
    inner = tk.Frame(frame, bg=COLORS["card"])
    inner.pack(fill="both", expand=True, padx=padx, pady=pady)
    return inner


def styled_button(parent, text, command, color=None, width=16, **kwargs):
    """Create a styled button with hover effect."""
    if color is None:
        color = COLORS["primary"]

    def darken(c):
        # Simple darkening by reducing brightness
        r = int(c[1:3], 16)
        g = int(c[3:5], 16)
        b = int(c[5:7], 16)
        factor = 0.85
        return "#{:02x}{:02x}{:02x}".format(int(r*factor), int(g*factor), int(b*factor))

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg="white",
        font=FONTS["btn"],
        relief="flat",
        cursor="hand2",
        width=width,
        padx=10,
        pady=8,
        **kwargs
    )

    hover_color = darken(color)

    def on_enter(e):
        btn.config(bg=hover_color)

    def on_leave(e):
        btn.config(bg=color)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def section_title(parent, text, color=None):
    """Create a section title label."""
    if color is None:
        color = COLORS["primary"]
    lbl = tk.Label(
        parent,
        text=text,
        font=FONTS["heading"],
        bg=COLORS["card"],
        fg=color
    )
    lbl.pack(anchor="w", pady=(0, 8))
    return lbl


def info_row(parent, label, value, label_color=None, value_color=None):
    """Create a label-value row inside a card."""
    row = tk.Frame(parent, bg=COLORS["card"])
    row.pack(fill="x", pady=2)
    tk.Label(
        row,
        text=label,
        font=FONTS["body"],
        bg=COLORS["card"],
        fg=label_color or COLORS["text_lt"],
        width=18,
        anchor="w"
    ).pack(side="left")
    tk.Label(
        row,
        text=value,
        font=("Segoe UI", 10, "bold"),
        bg=COLORS["card"],
        fg=value_color or COLORS["text"],
        anchor="w"
    ).pack(side="left")
    return row


def scrollable_frame(parent, bg=None):
    """Return (outer_frame, inner_canvas_frame) for scrollable content."""
    bg = bg or COLORS["bg"]
    outer = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(outer, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)

    inner.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    return outer, inner


def status_badge(parent, text, color):
    """Small colored badge label."""
    lbl = tk.Label(
        parent,
        text=f"  {text}  ",
        font=FONTS["small"],
        bg=color,
        fg="white",
        relief="flat",
        padx=4,
        pady=2
    )
    return lbl


def separator(parent, color=None):
    """Horizontal separator line."""
    color = color or COLORS["border"]
    line = tk.Frame(parent, bg=color, height=1)
    line.pack(fill="x", pady=8)
    return line
