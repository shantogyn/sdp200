# sob UI file ekhane theke color import korbe 

# ============================
# COLOR 
# ============================

COLORS = {
    # Primary backgrounds
    "bg_main":        "#F0F4F8",   # halka grey-white — main background
    "bg_sidebar":     "#0B2D4E",   # dark navy blue — sidebar background
    "bg_card":        "#FFFFFF",   # white — card background
    "bg_topbar":      "#FFFFFF",   # white — topbar background

    # Accent / Brand Colors
    "primary":        "#1A6B3C",   # deep green — primary brand color (healthcare)
    "primary_light":  "#2E9E5B",   # lighter green — hover state
    "accent":         "#0B6EFD",   # blue — highlight / link color
    "accent_dark":    "#0B2D4E",   # dark navy — secondary accent

    # Text Colors
    "text_primary":   "#0D1B2A",   # almost black — headings
    "text_secondary": "#4A5568",   # grey — subtext
    "text_light":     "#FFFFFF",   # white — text on dark backgrounds
    "text_muted":     "#A0AEC0",   # light grey — placeholder / disabled

    # Status Colors — medical data te use hobe
    "success":        "#2ECC71",   # green — normal value
    "warning":        "#F39C12",   # orange — borderline value
    "danger":         "#E74C3C",   # red — abnormal / alert
    "info":           "#3498DB",   # blue — informational

    # Sidebar Active State
    "sidebar_active": "#1A6B3C",   # green — active nav item
    "sidebar_hover":  "#163D5C",   # slightly lighter dark blue

    # Border / Divider
    "border":         "#E2E8F0",   # light grey border
    "divider":        "#CBD5E0",   # slightly darker divider
}

# ============================
# FONTS
# ============================

FONTS = {
    "heading":    ("Segoe UI", 20, "bold"),     # bor heading er jonno
    "subheading": ("Segoe UI", 15, "bold"),     # section title er jonno
    "body":       ("Segoe UI", 11),             # normal text er jonno
    "body_bold":  ("Segoe UI", 11, "bold"),     # bold body text
    "small":      ("Segoe UI", 9),              # choto note / label
    "button":     ("Segoe UI", 11, "bold"),     # button text
    "topbar":     ("Segoe UI", 14, "bold"),     # topbar title
    "sidebar":    ("Segoe UI", 11),             # sidebar nav items
    "sidebar_bold": ("Segoe UI", 11, "bold"),   # active sidebar item
    "card_title": ("Segoe UI", 12, "bold"),     # feature card title
    "card_value": ("Segoe UI", 22, "bold"),     # dashboard stat number
    "monospace":  ("Courier New", 10),          # OCR / code output er jonno
}

# ============================
# DIMENSIONS / LAYOUT
# ============================

LAYOUT = {
    "sidebar_width":  220,    # sidebar er width (pixel)
    "topbar_height":  60,     # topbar er height
    "card_pad_x":     20,     # card er horizontal padding
    "card_pad_y":     15,     # card er vertical padding
    "btn_pad_x":      20,     # button horizontal padding
    "btn_pad_y":      10,     # button vertical padding
    "corner_radius":  10,     # rounded corner radius
    "icon_size":      32,     # icon size dashboard card e
}

# ============================
# SIDEBAR NAV ITEMS
# ============================

# eita sidebar e koi koi navigation item thakbe seta define kore
# (label, module_key) format e
NAV_ITEMS = [
    ("🏠  Dashboard",         "dashboard"),
    ("🔬  Disease Prediction", "disease_prediction"),
    ("🥗  Diet Plan",          "diet"),
    ("⏰  Medicine Reminder",  "reminder"),
    ("🧪  Lab Analyzer",       "lab_analyzer"),
    ("🚑  First Aid Guide",    "first_aid"),
    ("📋  Disease Info",       "disease_info"),
    ("🚪  Logout",             "logout"),
]