"""
Dashboard Module
Main dashboard UI and feature management
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_connection import db
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
            on_logout=self.logout,
            on_user_info=self.show_user_info
        )
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg=COLORS["light_gray"])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.header_frame = tk.Frame(self.content_frame, bg=COLORS["white"], height=60)
        self.header_frame.pack(fill=tk.X)
        
        self.body_frame = tk.Frame(self.content_frame, bg=COLORS["light_gray"])
        self.body_frame.pack(fill=tk.BOTH, expand=True)
        
        self.feature_frames = {}
        self.welcome_frame = None
        self.current_feature = None
        
        self.create_header()
        
        # Welcome screen
        self.show_welcome_screen()
    
    def create_header(self):
        """Create header with user info"""
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        
        header_title = tk.Label(
            self.header_frame,
            text="Dashboard",
            font=FONTS["title_small"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["xl"]
        )
        header_title.pack(side=tk.LEFT, pady=PADDING["md"])
        
        user_icon = tk.Label(
            self.header_frame,
            text="👤",
            font=("Arial", 18),
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"]
        )
        user_icon.pack(side=tk.RIGHT, pady=PADDING["md"], padx=PADDING["xl"])
        
        # Separator
        sep = tk.Canvas(self.header_frame, height=1, bg=COLORS["card_border"], highlightthickness=0)
        sep.pack(fill=tk.X, pady=(0, 0))

    def clear_body(self):
        """Hide current body content"""
        for widget in self.body_frame.winfo_children():
            widget.pack_forget()
    
    def show_welcome_screen(self):
        """Show welcome/home screen with feature cards"""
        self.clear_body()
        self.current_feature = None
        
        if self.welcome_frame is None:
            self.welcome_frame = tk.Frame(self.body_frame, bg=COLORS["light_gray"])
            
            about_label = tk.Label(
                self.welcome_frame,
                text="Select a Feature from the Sidebar",
                font=FONTS["title_medium"],
                bg=COLORS["light_gray"],
                fg=COLORS["black"],
                padx=PADDING["xl"],
                pady=PADDING["lg"]
            )
            about_label.pack(anchor="w")
            
            grid_frame = tk.Frame(self.welcome_frame, bg=COLORS["light_gray"])
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
            
            for i in range(3):
                grid_frame.columnconfigure(i, weight=1)
        
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
    
    def load_feature(self, feature_name):
        """Load feature view"""
        self.current_feature = feature_name
        self.clear_body()
        
        if feature_name in self.feature_frames:
            self.feature_frames[feature_name].pack(fill=tk.BOTH, expand=True)
            return
        
        feature_frame = tk.Frame(self.body_frame, bg=COLORS["light_gray"])
        feature_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["lg"], pady=PADDING["lg"])
        self.feature_frames[feature_name] = feature_frame
        
        back_btn = CustomButton(
            feature_frame,
            text="← Back to Home",
            bg=COLORS["primary"],
            fg=COLORS["white"],
            command=self.show_welcome_screen
        )
        back_btn.pack(anchor="w", padx=PADDING["md"], pady=(0, PADDING["md"]))
        
        feature_container = tk.Frame(feature_frame, bg=COLORS["light_gray"])
        feature_container.pack(fill=tk.BOTH, expand=True)
        
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
            feature_ui = FeatureClass(feature_container, self.user_id)
            self.current_view = feature_ui
        else:
            error_label = tk.Label(
                feature_container,
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

    def show_user_info(self):
        """Show a popup with current user info"""
        if not db.is_connected():
            db.connect()
        
        user_info = None
        try:
            query = "SELECT username, email FROM users WHERE id = %s"
            results = db.execute_query(query, (self.user_id,))
            if results:
                user_info = results[0]
        except Exception:
            user_info = None
        
        if user_info:
            messagebox.showinfo(
                "User Info",
                f"Username: {user_info.get('username', self.username)}\nEmail: {user_info.get('email', 'Not available')}"
            )
        else:
            messagebox.showinfo(
                "User Info",
                f"Username: {self.username}\nUser ID: {self.user_id}"
            )
    
    def on_login_success(self, user_id, username):
        """Handle successful login"""
        self.user_id = user_id
        self.username = username
        self.setup_dashboard()
