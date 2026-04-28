# ui/components.py
# eita reusable UI component library
# sob screen ei components use korbe — consistency ar DRY principle maintain korar jonno
# theme.py theke colors import kora hocche

import tkinter as tk
from tkinter import ttk
from theme import COLORS, FONTS, LAYOUT


# ============================
# PRIMARY BUTTON
# ============================

def make_button(parent, text, command, bg=None, fg=None, width=None, pady=8):
    """
    Styled primary button create kore.
    bg ar fg custom dite parbe, default primary green use hobe.
    """
    bg = bg or COLORS["primary"]
    fg = fg or COLORS["text_light"]

    btn_kwargs = dict(
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        font=FONTS["button"],
        relief="flat",
        cursor="hand2",           # hover e hand cursor — UX er jonno
        activebackground=COLORS["primary_light"],
        activeforeground=COLORS["text_light"],
        pady=pady,
        bd=0,
    )
    if width:
        btn_kwargs["width"] = width

    btn = tk.Button(parent, **btn_kwargs)

    # hover effect — mouse enter/leave e color change
    btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["primary_light"]))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

    return btn


# ============================
# SECONDARY / OUTLINE BUTTON
# ============================

def make_secondary_button(parent, text, command, width=None):
    """
    Secondary / ghost button — border style, transparent background.
    Cancel ba back button er jonno use hobe.
    """
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=COLORS["bg_card"],
        fg=COLORS["primary"],
        font=FONTS["button"],
        relief="flat",
        cursor="hand2",
        activebackground=COLORS["border"],
        activeforeground=COLORS["primary"],
        pady=8,
        bd=1,
        highlightbackground=COLORS["primary"],
        highlightthickness=1,
    )
    if width:
        btn.config(width=width)

    btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["border"]))
    btn.bind("<Leave>", lambda e: btn.config(bg=COLORS["bg_card"]))
    return btn


# ============================
# LABELED INPUT FIELD
# ============================

def make_input(parent, label_text, show=None, width=35):
    """
    Label + Entry field er combination ekসাথে return kore.
    show="*" dile password field hobe.
    Returns: (frame, entry_widget) — entry theke value nite hobe
    """
    frame = tk.Frame(parent, bg=COLORS["bg_card"])

    lbl = tk.Label(
        frame,
        text=label_text,
        font=FONTS["body_bold"],
        bg=COLORS["bg_card"],
        fg=COLORS["text_secondary"],
        anchor="w"
    )
    lbl.pack(fill="x", pady=(0, 3))

    entry_kwargs = dict(
        font=FONTS["body"],
        bg=COLORS["bg_main"],
        fg=COLORS["text_primary"],
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["primary"],
        width=width,
        insertbackground=COLORS["text_primary"],
    )
    if show:
        entry_kwargs["show"] = show

    entry = tk.Entry(frame, **entry_kwargs)
    entry.pack(fill="x", ipady=8, pady=(0, 2))

    return frame, entry


# ============================
# SECTION CARD
# ============================

def make_card(parent, title=None, padx=15, pady=15):
    """
    White rounded-look card container create kore.
    Section content wrap korar jonno use hobe dashboard e.
    Returns: (outer_frame, inner_frame)
    """
    # outer border frame — shadow effect er jonno
    outer = tk.Frame(
        parent,
        bg=COLORS["border"],
        bd=0,
    )

    # inner white frame
    inner = tk.Frame(
        outer,
        bg=COLORS["bg_card"],
        padx=padx,
        pady=pady,
    )
    inner.pack(fill="both", expand=True, padx=1, pady=1)

    if title:
        title_lbl = tk.Label(
            inner,
            text=title,
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        title_lbl.pack(fill="x", pady=(0, 10))

        # divider line
        sep = tk.Frame(inner, bg=COLORS["border"], height=1)
        sep.pack(fill="x", pady=(0, 10))

    return outer, inner


# ============================
# STATUS BADGE LABEL
# ============================

def make_badge(parent, text, status="NORMAL"):
    """
    Lab result status badge create kore (NORMAL/HIGH/LOW).
    Color auto set hobe status anujaye.
    """
    colors = {
        "NORMAL": (COLORS["success"], "#FFFFFF"),
        "HIGH":   (COLORS["danger"],  "#FFFFFF"),
        "LOW":    (COLORS["info"],    "#FFFFFF"),
    }
    bg_color, fg_color = colors.get(status, (COLORS["text_muted"], "#FFFFFF"))

    badge = tk.Label(
        parent,
        text=f"  {status}  ",
        font=FONTS["small"],
        bg=bg_color,
        fg=fg_color,
        relief="flat",
        padx=6,
        pady=3,
    )
    return badge


# ============================
# SCROLLABLE FRAME
# ============================

def make_scrollable_frame(parent):
    """
    Scroll korar joggo frame create kore.
    Beshi content thakle scroll bar dicche.
    Returns: (canvas, scrollable_frame)
    """
    container = tk.Frame(parent, bg=COLORS["bg_main"])

    canvas = tk.Canvas(
        container,
        bg=COLORS["bg_main"],
        highlightthickness=0,
        bd=0
    )

    scrollbar = ttk.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview
    )

    scrollable_frame = tk.Frame(canvas, bg=COLORS["bg_main"])

    # frame resize hole canvas scrollregion update hobe
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # mouse wheel scroll support
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    return container, scrollable_frame


# ============================
# TOPBAR
# ============================

def make_topbar(parent, app_title="Swastha"):
    """
    App er topbar create kore — title ar current time show kore.
    Returns: topbar frame
    """
    from datetime import datetime

    topbar = tk.Frame(
        parent,
        bg=COLORS["bg_topbar"],
        height=LAYOUT["topbar_height"],
        bd=0
    )
    topbar.pack_propagate(False)

    # left — app title with green dot
    left_frame = tk.Frame(topbar, bg=COLORS["bg_topbar"])
    left_frame.pack(side="left", padx=20, pady=10)

    # green accent dot
    dot = tk.Label(
        left_frame,
        text="●",
        font=("Segoe UI", 14),
        bg=COLORS["bg_topbar"],
        fg=COLORS["primary"],
    )
    dot.pack(side="left", padx=(0, 6))

    title_lbl = tk.Label(
        left_frame,
        text=app_title,
        font=FONTS["topbar"],
        bg=COLORS["bg_topbar"],
        fg=COLORS["text_primary"],
    )
    title_lbl.pack(side="left")

    # tagline
    tagline = tk.Label(
        left_frame,
        text=" — Your Health, Our Priority",
        font=FONTS["small"],
        bg=COLORS["bg_topbar"],
        fg=COLORS["text_muted"],
    )
    tagline.pack(side="left")

    # right — current date and time
    right_frame = tk.Frame(topbar, bg=COLORS["bg_topbar"])
    right_frame.pack(side="right", padx=20)

    time_lbl = tk.Label(
        right_frame,
        font=FONTS["body"],
        bg=COLORS["bg_topbar"],
        fg=COLORS["text_secondary"],
    )
    time_lbl.pack()

    # live clock update — protiটা second update hobe
    def _update_time():
        now = datetime.now().strftime("%A, %d %b %Y  |  %I:%M:%S %p")
        time_lbl.config(text=now)
        topbar.after(1000, _update_time)  # 1 second por por rekursive call

    _update_time()

    # bottom divider
    divider = tk.Frame(parent, bg=COLORS["border"], height=1)
    divider.pack(fill="x")

    return topbar


# ============================
# SIDEBAR
# ============================

def make_sidebar(parent, nav_items, on_nav_click, active_key="dashboard"):
    """
    Left navigation sidebar create kore.
    nav_items: [(label, key), ...] list
    on_nav_click: callback function — key diye call kora hobe
    active_key: currently active navigation item
    Returns: sidebar frame
    """
    sidebar = tk.Frame(
        parent,
        bg=COLORS["bg_sidebar"],
        width=LAYOUT["sidebar_width"]
    )
    sidebar.pack_propagate(False)

    # sidebar top — app logo area
    logo_frame = tk.Frame(sidebar, bg=COLORS["bg_sidebar"], pady=20)
    logo_frame.pack(fill="x")

    logo_icon = tk.Label(
        logo_frame,
        text="🏥",
        font=("Segoe UI", 28),
        bg=COLORS["bg_sidebar"],
        fg=COLORS["text_light"],
    )
    logo_icon.pack()

    logo_text = tk.Label(
        logo_frame,
        text="SWASTHA",
        font=("Segoe UI", 16, "bold"),
        bg=COLORS["bg_sidebar"],
        fg=COLORS["text_light"],
    )
    logo_text.pack()

    logo_sub = tk.Label(
        logo_frame,
        text="Healthcare Assistant",
        font=FONTS["small"],
        bg=COLORS["bg_sidebar"],
        fg=COLORS["text_muted"],
    )
    logo_sub.pack()

    # divider
    tk.Frame(sidebar, bg=COLORS["sidebar_hover"], height=1).pack(
        fill="x", padx=15, pady=10
    )

    # nav items loop
    btn_refs = {}  # button references rakha hocche active state update er jonno

    for label, key in nav_items:
        is_active = (key == active_key)
        is_logout = (key == "logout")

        btn_bg = COLORS["sidebar_active"] if is_active else COLORS["bg_sidebar"]
        btn_fg = COLORS["text_light"]

        btn = tk.Button(
            sidebar,
            text=f"  {label}",
            command=lambda k=key: on_nav_click(k),
            bg=btn_bg,
            fg=btn_fg,
            font=FONTS["sidebar_bold"] if is_active else FONTS["sidebar"],
            relief="flat",
            anchor="w",
            padx=15,
            pady=10,
            cursor="hand2",
            activebackground=COLORS["sidebar_active"],
            activeforeground=COLORS["text_light"],
            bd=0,
        )
        btn.pack(fill="x")

        if not is_logout:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["sidebar_hover"]))
            btn.bind("<Leave>", lambda e, b=btn, k=key: b.config(
                bg=COLORS["sidebar_active"] if k == active_key else COLORS["bg_sidebar"]
            ))

        btn_refs[key] = btn

    return sidebar, btn_refs


# ============================
# INFO ROW (label: value)
# ============================

def make_info_row(parent, label, value, label_color=None):
    """
    Label: Value format er info row create kore.
    Disease info, lab result display er jonno use hobe.
    """
    label_color = label_color or COLORS["text_secondary"]

    row = tk.Frame(parent, bg=COLORS["bg_card"])

    lbl = tk.Label(
        row,
        text=f"{label}:",
        font=FONTS["body_bold"],
        bg=COLORS["bg_card"],
        fg=label_color,
        anchor="nw",
        width=18,
    )
    lbl.pack(side="left", anchor="nw")

    val = tk.Label(
        row,
        text=value,
        font=FONTS["body"],
        bg=COLORS["bg_card"],
        fg=COLORS["text_primary"],
        anchor="nw",
        wraplength=420,
        justify="left",
    )
    val.pack(side="left", anchor="nw", padx=(5, 0))

    return row


# ============================
# DANGER / SUCCESS MESSAGE BOX
# ============================

def make_message(parent, text, msg_type="info"):
    """
    Inline message box create kore — form error ba success show korar jonno.
    msg_type: "success", "error", "warning", "info"
    """
    color_map = {
        "success": (COLORS["success"],  "#E8FFF4"),
        "error":   (COLORS["danger"],   "#FFF0F0"),
        "warning": (COLORS["warning"],  "#FFFAE6"),
        "info":    (COLORS["info"],     "#EBF5FF"),
    }
    fg, bg = color_map.get(msg_type, (COLORS["text_secondary"], COLORS["bg_card"]))

    msg = tk.Label(
        parent,
        text=text,
        font=FONTS["body"],
        bg=bg,
        fg=fg,
        relief="flat",
        padx=12,
        pady=8,
        wraplength=380,
        justify="left",
    )
    return msg