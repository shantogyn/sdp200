"""
Disease Prediction Module
Predicts diseases based on symptoms
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import COLORS, FONTS, PADDING
from ui.components import CustomButton, CustomEntry, CardFrame, InfoBox
from utils.helpers import SymptomAnalyzer

class DiseasePredictionUI:
    """Disease Prediction Feature UI"""
    
    def __init__(self, parent, user_id):
        """Initialize disease prediction UI"""
        self.parent = parent
        self.user_id = user_id
        self.symptoms_list = []
        self.create_ui()
    
    def create_ui(self):
        """Create UI for disease prediction"""
        # Title
        title = tk.Label(
            self.parent,
            text="🔍 Disease Prediction",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Main content frame
        content = tk.Frame(self.parent, bg=COLORS["light_gray"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Input
        left_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING["md"]), pady=0)
        
        # Input section
        input_label = tk.Label(
            left_panel,
            text="Enter Your Symptoms",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        input_label.pack(anchor="w")
        
        # Instructions
        instr = tk.Label(
            left_panel,
            text="Enter symptoms separated by commas (e.g., fever, headache, cough)",
            font=FONTS["body_small"],
            bg=COLORS["white"],
            fg=COLORS["gray"],
            wraplength=300,
            padx=PADDING["md"]
        )
        instr.pack(anchor="w", pady=(0, PADDING["md"]))
        
        # Text widget for symptoms
        self.symptoms_text = tk.Text(
            left_panel,
            font=FONTS["body_medium"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            height=5,
            width=35,
            relief="solid",
            bd=1
        )
        self.symptoms_text.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg=COLORS["white"])
        btn_frame.pack(fill=tk.X, padx=PADDING["md"], pady=PADDING["md"])
        
        predict_btn = CustomButton(
            btn_frame,
            text="Predict Disease",
            command=self.predict_disease
        )
        predict_btn.pack(side=tk.LEFT, padx=(0, PADDING["sm"]))
        
        clear_btn = CustomButton(
            btn_frame,
            text="Clear",
            bg=COLORS["gray"],
            command=lambda: self.symptoms_text.delete("1.0", tk.END)
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Right panel - Results
        right_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(PADDING["md"], 0), pady=0)
        
        result_label = tk.Label(
            right_panel,
            text="Prediction Results",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        result_label.pack(anchor="w")
        
        # Result display
        self.result_frame = tk.Frame(right_panel, bg=COLORS["white"])
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Welcome message
        welcome = tk.Label(
            self.result_frame,
            text="Enter symptoms and click 'Predict Disease' to see results",
            font=FONTS["body_medium"],
            bg=COLORS["white"],
            fg=COLORS["gray"],
            wraplength=250,
            justify="center"
        )
        welcome.pack(expand=True)
    
    def predict_disease(self):
        """Predict disease from symptoms"""
        symptoms_input = self.symptoms_text.get("1.0", tk.END).strip()
        
        if not symptoms_input:
            messagebox.showerror("Error", "Please enter symptoms")
            return
        
        # Parse symptoms
        symptoms = [s.strip().lower() for s in symptoms_input.split(",")]
        symptoms = [s for s in symptoms if s]  # Remove empty
        
        # Get prediction
        result = SymptomAnalyzer.predict_disease(symptoms)
        
        # Display results
        self.display_results(result)
    
    def display_results(self, result):
        """Display prediction results"""
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Disease name
        disease_label = tk.Label(
            self.result_frame,
            text=result["disease"],
            font=FONTS["title_medium"],
            bg=COLORS["white"],
            fg=COLORS["primary"],
            wraplength=300
        )
        disease_label.pack(anchor="w", pady=(0, PADDING["md"]))
        
        # Confidence
        conf_text = f"Confidence: {result['confidence']}%"
        conf_label = tk.Label(
            self.result_frame,
            text=conf_text,
            font=FONTS["body_large"],
            bg=COLORS["white"],
            fg=COLORS["success"],
            wraplength=300
        )
        conf_label.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Confidence bar
        bar_frame = tk.Frame(self.result_frame, bg=COLORS["light_gray"], height=10)
        bar_frame.pack(fill=tk.X, pady=(0, PADDING["md"]))
        
        bar_width = int((result["confidence"] / 100) * 200)
        bar = tk.Frame(bar_frame, bg=COLORS["success"], height=10, width=bar_width)
        bar.pack(fill=tk.X)
        
        # Advice
        advice_label = tk.Label(
            self.result_frame,
            text="⚠️ Disclaimer:",
            font=FONTS["heading_3"],
            bg=COLORS["white"],
            fg=COLORS["danger"],
            wraplength=300
        )
        advice_label.pack(anchor="w", pady=(PADDING["lg"], PADDING["sm"]))
        
        advice_text = tk.Label(
            self.result_frame,
            text=result["advice"],
            font=FONTS["body_medium"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            wraplength=300,
            justify="left"
        )
        advice_text.pack(anchor="w")
        
        # Consult button
        consult_btn = CustomButton(
            self.result_frame,
            text="📞 Consult a Doctor",
            bg=COLORS["danger"]
        )
        consult_btn.pack(pady=PADDING["lg"])
