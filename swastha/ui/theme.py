"""
Theme Module
Defines colors, fonts, and styling for the application
"""

# Color Palette
COLORS = {
    # Primary colors
    "primary": "#3498db",      # Blue
    "success": "#27ae60",      # Green
    "danger": "#e74c3c",       # Red
    "warning": "#f39c12",      # Orange
    "info": "#2980b9",         # Dark Blue
    
    # Neutral colors
    "white": "#ffffff",
    "light_gray": "#f0f0f0",
    "gray": "#95a5a6",
    "dark_gray": "#7f8c8d",
    "darker_gray": "#34495e",
    "black": "#2c3e50",
    
    # Backgrounds
    "bg_primary": "#ecf0f1",
    "bg_secondary": "#ffffff",
    "bg_dark": "#34495e",
    
    # Sidebar
    "sidebar_bg": "#2c3e50",
    "sidebar_hover": "#34495e",
    "sidebar_text": "#ecf0f1",
    
    # Cards
    "card_bg": "#ffffff",
    "card_border": "#bdc3c7",
    "card_shadow": "#95a5a6",
    
    # Accent colors
    "accent_1": "#e74c3c",  # Red
    "accent_2": "#f39c12",  # Orange
    "accent_3": "#27ae60",  # Green
    "accent_4": "#3498db",  # Blue
    "accent_5": "#9b59b6",  # Purple
}

# Font Configuration
FONTS = {
    # Titles
    "title_large": ("Arial", 28, "bold"),
    "title_medium": ("Arial", 18, "bold"),
    "title_small": ("Arial", 14, "bold"),
    
    # Headings
    "heading_1": ("Arial", 16, "bold"),
    "heading_2": ("Arial", 13, "bold"),
    "heading_3": ("Arial", 11, "bold"),
    
    # Regular text
    "body_large": ("Arial", 12),
    "body_medium": ("Arial", 11),
    "body_small": ("Arial", 10),
    
    # UI elements
    "button": ("Arial", 11, "bold"),
    "label": ("Arial", 10),
    "input": ("Arial", 11),
    
    # Special
    "mono": ("Courier New", 10),
    "emphasis": ("Arial", 11, "italic"),
}

# Component Styling
STYLES = {
    "button": {
        "font": FONTS["button"],
        "relief": "flat",
        "cursor": "hand2",
        "padx": 15,
        "pady": 8,
        "bg": COLORS["primary"],
        "fg": COLORS["white"],
        "activebackground": COLORS["info"],
        "activeforeground": COLORS["white"],
        "border": 0,
    },
    
    "button_success": {
        "bg": COLORS["success"],
        "activebackground": "#229954",
    },
    
    "button_danger": {
        "bg": COLORS["danger"],
        "activebackground": "#c0392b",
    },
    
    "button_secondary": {
        "bg": COLORS["light_gray"],
        "fg": COLORS["black"],
        "activebackground": COLORS["gray"],
    },
    
    "entry": {
        "font": FONTS["input"],
        "relief": "flat",
        "bg": COLORS["white"],
        "fg": COLORS["black"],
        "insertbackground": COLORS["primary"],
        "border": 1,
    },
    
    "label": {
        "font": FONTS["label"],
        "bg": COLORS["light_gray"],
        "fg": COLORS["black"],
    },
    
    "frame": {
        "bg": COLORS["light_gray"],
    },
}

# Padding values
PADDING = {
    "xs": 2,
    "sm": 5,
    "md": 10,
    "lg": 15,
    "xl": 20,
    "xxl": 30,
}

# Border radius (simulated with relief)
BORDER_OPTIONS = {
    "flat": "flat",
    "raised": "raised",
    "sunken": "sunken",
}

def get_color(name):
    """Get color by name"""
    return COLORS.get(name, "#000000")

def get_font(name):
    """Get font by name"""
    return FONTS.get(name, ("Arial", 10))

def get_style(name):
    """Get style by name"""
    return STYLES.get(name, {})

# Quick style functions
def button_primary():
    """Get primary button style"""
    return STYLES["button"].copy()

def button_success():
    """Get success button style"""
    style = STYLES["button"].copy()
    style.update(STYLES["button_success"])
    return style

def button_danger():
    """Get danger button style"""
    style = STYLES["button"].copy()
    style.update(STYLES["button_danger"])
    return style

def button_secondary():
    """Get secondary button style"""
    style = STYLES["button"].copy()
    style.update(STYLES["button_secondary"])
    return style
