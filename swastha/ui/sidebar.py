"""
Sidebar Module
Manages sidebar navigation for the application
"""

import tkinter as tk
import config
from ui.theme import COLORS, FONTS, PADDING

class Sidebar:
    """Class to manage sidebar navigation"""
    
    def __init__(self, parent, on_feature_click=None, on_logout=None):
        """
        Initialize sidebar
        Args:
            parent: Parent widget
            on_feature_click: Callback when feature is clicked
            on_logout: Callback when logout is clicked
        """
        self.parent = parent
        self.on_feature_click = on_feature_click
        self.on_logout = on_logout
        self.current_feature = None
        self.feature_buttons = {}
        
        self.create_sidebar()
    
    def create_sidebar(self):
        """Create sidebar UI"""
        # Sidebar frame
        self.sidebar_frame = tk.Frame(
            self.parent,
            bg=COLORS["sidebar_bg"],
            width=250
        )
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)
        
        # Logo section
        logo_frame = tk.Frame(self.sidebar_frame, bg=COLORS["sidebar_bg"])
        logo_frame.pack(fill=tk.X, padx=PADDING["md"], pady=PADDING["lg"])
        
        logo_text = tk.Label(
            logo_frame,
            text="🏥 SWASTHA",
            font=("Arial", 14, "bold"),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["sidebar_text"]
        )
        logo_text.pack(anchor="w")
        
        version = tk.Label(
            logo_frame,
            text="v1.0.0",
            font=("Arial", 8),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["gray"]
        )
        version.pack(anchor="w")
        
        # Separator
        sep1 = tk.Canvas(
            self.sidebar_frame,
            height=1,
            bg="#445566",
            highlightthickness=0
        )
        sep1.pack(fill=tk.X, pady=PADDING["md"])
        
        # Features label
        features_label = tk.Label(
            self.sidebar_frame,
            text="FEATURES",
            font=("Arial", 9, "bold"),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["gray"],
            padx=PADDING["md"]
        )
        features_label.pack(anchor="w", pady=PADDING["sm"])
        
        # Create scrollable features list
        features_container = tk.Frame(self.sidebar_frame, bg=COLORS["sidebar_bg"])
        features_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Features
        features = [
            ("🔍 Disease Prediction", "Disease Prediction"),
            ("💬 AI Chatbot", "AI Chatbot"),
            ("💊 Medicine Reminder", "Medicine Reminder"),
            ("🧪 Lab Analyzer", "Lab Analyzer"),
            ("🥗 Diet Guide", "Diet Guide"),
            ("🧠 Mental Health", "Mental Health"),
            ("🖼️ Image Analyzer", "Image Analyzer"),
            ("🚑 First Aid", "First Aid"),
            ("📚 Disease Info", "Disease Info"),
        ]
        
        for icon_label, feature_name in features:
            self.create_feature_button(features_container, icon_label, feature_name)
        
        # Separator
        sep2 = tk.Canvas(
            self.sidebar_frame,
            height=1,
            bg="#445566",
            highlightthickness=0
        )
        sep2.pack(fill=tk.X, pady=PADDING["md"])
        
        # Bottom section (settings, logout)
        bottom_frame = tk.Frame(self.sidebar_frame, bg=COLORS["sidebar_bg"])
        bottom_frame.pack(fill=tk.X, padx=PADDING["md"], pady=PADDING["md"])
        
        # Settings button
        settings_btn = tk.Button(
            bottom_frame,
            text="⚙️  Settings",
            font=("Arial", 10),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["sidebar_text"],
            relief="flat",
            anchor="w",
            padx=PADDING["md"],
            pady=PADDING["sm"],
            cursor="hand2"
        )
        settings_btn.pack(fill=tk.X, pady=PADDING["sm"])
        settings_btn.bind("<Enter>", lambda e: settings_btn.config(bg=COLORS["sidebar_hover"]))
        settings_btn.bind("<Leave>", lambda e: settings_btn.config(bg=COLORS["sidebar_bg"]))
        
        # Logout button
        logout_btn = tk.Button(
            bottom_frame,
            text="🚪 Logout",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg=COLORS["white"],
            relief="flat",
            anchor="w",
            padx=PADDING["md"],
            pady=PADDING["sm"],
            cursor="hand2",
            command=self.on_logout if self.on_logout else lambda: None
        )
        logout_btn.pack(fill=tk.X, pady=PADDING["sm"])
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#c0392b"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#e74c3c"))
    
    def create_feature_button(self, parent, label, feature_name):
        """Create a feature button"""
        btn = tk.Button(
            parent,
            text=label,
            font=("Arial", 10),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["sidebar_text"],
            relief="flat",
            anchor="w",
            padx=PADDING["md"],
            pady=PADDING["sm"],
            cursor="hand2",
            command=lambda: self.select_feature(feature_name)
        )
        btn.pack(fill=tk.X, pady=2)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["sidebar_hover"]))
        btn.bind("<Leave>", lambda e: self.on_button_leave(btn, feature_name))
        
        self.feature_buttons[feature_name] = btn
    
    def on_button_leave(self, btn, feature_name):
        """Handle button leave event"""
        if feature_name == self.current_feature:
            btn.config(bg=COLORS["primary"])
        else:
            btn.config(bg=COLORS["sidebar_bg"])
    
    def select_feature(self, feature_name):
        """Select a feature"""
        # Reset previous selection
        if self.current_feature and self.current_feature in self.feature_buttons:
            prev_btn = self.feature_buttons[self.current_feature]
            prev_btn.config(bg=COLORS["sidebar_bg"])
        
        # Set new selection
        self.current_feature = feature_name
        btn = self.feature_buttons[feature_name]
        btn.config(bg=COLORS["primary"])
        
        # Call callback
        if self.on_feature_click:
            self.on_feature_click(feature_name)
    
    def get_sidebar_frame(self):
        """Get sidebar frame"""
        return self.sidebar_frame
