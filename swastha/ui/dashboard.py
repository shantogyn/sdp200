"""
Dashboard Module
Main dashboard UI and feature management
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import COLORS, FONTS, PADDING
from ui.sidebar import Sidebar
from ui.components import FeatureCard, ScrollableFrame, CustomButton
from features.disease_prediction import DiseasePredictionUI
from features.chatbot import ChatbotUI
from features.medicine_reminder import MedicineReminderUI
from features.lab_analyzer import LabAnalyzerUI
from features.diet_guide import DietGuideUI
from features.mental_health import MentalHealthUI
from features.image_analyzer import ImageAnalyzerUI
from features.first_aid import FirstAidUI
from features.disease_info import DiseaseInfoUI

class Dashboard:
    """Main dashboard class"""
    
    def __init__(self, root, user_id, username):
        """
        Initialize dashboard
        Args:
            root: Tkinter root window
            user_id: Current user ID
            username: Current username
        """
        self.root = root
        self.user_id = user_id
        self.username = username
        self.current_view = None
        self.current_feature = None
        
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Setup dashboard UI"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Swastha - Dashboard")
        
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS["light_gray"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        sidebar = Sidebar(
            main_container,
            on_feature_click=self.load_feature,
            on_logout=self.logout
        )
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg=COLORS["light_gray"])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header()
        
        # Welcome screen
        self.show_welcome_screen()
    
    def create_header(self):
        """Create header with user info"""
        header = tk.Frame(self.content_frame, bg=COLORS["white"], height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        # User info
        user_label = tk.Label(
            header,
            text=f"👤 Welcome, {self.username}",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["xl"]
        )
        user_label.pack(side=tk.LEFT, pady=PADDING["md"])
        
        # Separator
        sep = tk.Canvas(header, height=1, bg=COLORS["card_border"], highlightthickness=0)
        sep.pack(fill=tk.X, pady=(0, 0))
    
    def show_welcome_screen(self):
        """Show welcome/home screen with feature cards"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            if widget != self.content_frame.winfo_children()[0]:  # Keep header
                widget.destroy()
        
        # About label
        about_label = tk.Label(
            self.content_frame,
            text="Select a Feature from the Sidebar",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"],
            padx=PADDING["xl"],
            pady=PADDING["lg"]
        )
        about_label.pack(anchor="w")
        
        # Features grid
        grid_frame = tk.Frame(self.content_frame, bg=COLORS["light_gray"])
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["xl"], pady=PADDING["xl"])
        
        features_info = [
            ("🔍", "Disease Prediction", "Predict diseases based on symptoms"),
            ("💬", "AI Chatbot", "Chat with our AI health assistant"),
            ("💊", "Medicine Reminder", "Keep track of medicines"),
            ("🧪", "Lab Analyzer", "Analyze lab test results"),
            ("🥗", "Diet Guide", "Get personalized diet suggestions"),
            ("🧠", "Mental Health", "Monitor your mental wellness"),
            ("🖼️", "Image Analyzer", "Analyze medical images"),
            ("🚑", "First Aid", "Learn emergency first aid"),
            ("📚", "Disease Info", "Explore disease information"),
        ]
        
        col = 0
        row = 0
        for icon, title, desc in features_info:
            card = FeatureCard(
                grid_frame,
                title=title,
                icon=icon,
                description=desc,
                command=lambda t=title: self.load_feature(t),
                width=150,
                height=180
            )
            card.grid(row=row, column=col, padx=PADDING["md"], pady=PADDING["md"], sticky="nsew")
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
    
    def load_feature(self, feature_name):
        """Load feature view"""
        self.current_feature = feature_name
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            if widget != self.content_frame.winfo_children()[0]:  # Keep header
                widget.destroy()
        
        # Create feature container
        feature_frame = tk.Frame(self.content_frame, bg=COLORS["light_gray"])
        feature_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["lg"], pady=PADDING["lg"])
        
        # Load appropriate feature
        feature_map = {
            "Disease Prediction": DiseasePredictionUI,
            "AI Chatbot": ChatbotUI,
            "Medicine Reminder": MedicineReminderUI,
            "Lab Analyzer": LabAnalyzerUI,
            "Diet Guide": DietGuideUI,
            "Mental Health": MentalHealthUI,
            "Image Analyzer": ImageAnalyzerUI,
            "First Aid": FirstAidUI,
            "Disease Info": DiseaseInfoUI,
        }
        
        if feature_name in feature_map:
            FeatureClass = feature_map[feature_name]
            feature_ui = FeatureClass(feature_frame, self.user_id)
            self.current_view = feature_ui
        else:
            error_label = tk.Label(
                feature_frame,
                text=f"Feature '{feature_name}' not found",
                font=FONTS["heading_2"],
                bg=COLORS["light_gray"],
                fg=COLORS["danger"]
            )
            error_label.pack(pady=PADDING["xl"])
    
    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            from auth.login import LoginWindow
            login = LoginWindow(self.root, on_login_success=self.on_login_success)
    
    def on_login_success(self, user_id, username):
        """Handle successful login"""
        self.user_id = user_id
        self.username = username
        self.setup_dashboard()
