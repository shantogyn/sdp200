"""
Diet Guide Module
Provides personalized diet suggestions
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import COLORS, FONTS, PADDING
from ui.components import CustomButton, CustomEntry, CardFrame, InfoBox
from utils.helpers import BMICalculator

class DietGuideUI:
    """Diet Guide Feature UI"""
    
    def __init__(self, parent, user_id):
        """Initialize diet guide UI"""
        self.parent = parent
        self.user_id = user_id
        self.create_ui()
    
    def create_ui(self):
        """Create diet guide UI"""
        # Title
        title = tk.Label(
            self.parent,
            text="🥗 Diet Guide",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Main container
        content = tk.Frame(self.parent, bg=COLORS["light_gray"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Input
        left_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING["md"]), pady=0)
        
        input_label = tk.Label(
            left_panel,
            text="Your Health Profile",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        input_label.pack(anchor="w", fill=tk.X)
        
        form_frame = tk.Frame(left_panel, bg=COLORS["white"])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Age
        tk.Label(form_frame, text="Age (years)", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.age_input = tk.Entry(form_frame, font=FONTS["body_medium"], relief="solid", bd=1)
        self.age_input.pack(fill=tk.X, pady=(0, PADDING["md"]))
        
        # Weight
        tk.Label(form_frame, text="Weight (kg)", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.weight_input = tk.Entry(form_frame, font=FONTS["body_medium"], relief="solid", bd=1)
        self.weight_input.pack(fill=tk.X, pady=(0, PADDING["md"]))
        
        # Height
        tk.Label(form_frame, text="Height (cm)", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.height_input = tk.Entry(form_frame, font=FONTS["body_medium"], relief="solid", bd=1)
        self.height_input.pack(fill=tk.X, pady=(0, PADDING["md"]))
        
        # Activity level
        tk.Label(form_frame, text="Activity Level", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.activity_var = tk.StringVar(value="moderate")
        activity_menu = tk.OptionMenu(
            form_frame,
            self.activity_var,
            "sedentary",
            "light",
            "moderate",
            "active",
            "very active"
        )
        activity_menu.pack(fill=tk.X, pady=(0, PADDING["lg"]))
        
        # Generate button
        gen_btn = CustomButton(
            form_frame,
            text="Generate Diet Plan",
            bg=COLORS["success"],
            command=self.generate_diet
        )
        gen_btn.pack(fill=tk.X)
        
        # Right panel - Results
        right_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(PADDING["md"], 0), pady=0)
        
        result_label = tk.Label(
            right_panel,
            text="Your Diet Plan",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        result_label.pack(anchor="w", fill=tk.X)
        
        # Results display
        scrollbar_frame = tk.Frame(right_panel)
        scrollbar_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        scrollbar = tk.Scrollbar(scrollbar_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(
            scrollbar_frame,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            yscrollcommand=scrollbar.set,
            height=15,
            relief="solid",
            bd=1
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)
        self.result_text.insert("1.0", "Enter your details and generate a personalized diet plan.\n\nNote: This is a general guide. Consult a nutritionist for personalized advice.")
        self.result_text.config(state="disabled")
    
    def generate_diet(self):
        """Generate personalized diet plan"""
        try:
            age = int(self.age_input.get())
            weight = float(self.weight_input.get())
            height = float(self.height_input.get())
            activity = self.activity_var.get()
            
            # Calculate BMI
            bmi = BMICalculator.calculate_bmi(weight, height)
            bmi_category = BMICalculator.get_bmi_category(bmi)
            
            # Calculate caloric needs (simplified)
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
            activity_factors = {
                "sedentary": 1.2,
                "light": 1.375,
                "moderate": 1.55,
                "active": 1.725,
                "very active": 1.9
            }
            tdee = bmr * activity_factors.get(activity, 1.55)
            
            # Generate plan
            diet_plan = self.create_diet_plan(age, weight, height, bmi, bmi_category, tdee)
            
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", diet_plan)
            self.result_text.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for age, weight, and height")
    
    def create_diet_plan(self, age, weight, height, bmi, bmi_category, tdee):
        """Create personalized diet plan"""
        plan = f"🥗 PERSONALIZED DIET PLAN\n"
        plan += f"{'='*40}\n\n"
        
        plan += f"YOUR HEALTH METRICS\n"
        plan += f"{'-'*40}\n"
        plan += f"Age: {age} years\n"
        plan += f"Weight: {weight} kg\n"
        plan += f"Height: {height} cm\n"
        plan += f"BMI: {bmi} ({bmi_category})\n"
        plan += f"Daily Caloric Needs: ~{int(tdee)} calories\n\n"
        
        plan += f"DAILY NUTRITIONAL GOALS\n"
        plan += f"{'-'*40}\n"
        plan += f"Proteins: {int(weight * 1.6)}g (30%)\n"
        plan += f"Carbs: {int(tdee * 0.45 / 4)}g (45%)\n"
        plan += f"Fats: {int(tdee * 0.25 / 9)}g (25%)\n\n"
        
        plan += f"RECOMMENDED FOODS\n"
        plan += f"{'-'*40}\n"
        plan += f"✓ Proteins: Chicken, Fish, Eggs, Beans, Tofu\n"
        plan += f"✓ Carbs: Brown Rice, Oats, Whole Wheat, Quinoa\n"
        plan += f"✓ Fats: Olive Oil, Nuts, Avocado, Fish Oil\n"
        plan += f"✓ Vegetables: Leafy Greens, Broccoli, Carrots\n"
        plan += f"✓ Fruits: Berries, Apples, Bananas, Oranges\n\n"
        
        plan += f"SAMPLE MEAL PLAN\n"
        plan += f"{'-'*40}\n"
        plan += f"Breakfast: Oatmeal with fruits and nuts\n"
        plan += f"Snack: Greek yogurt or nuts\n"
        plan += f"Lunch: Grilled chicken with brown rice\n"
        plan += f"Snack: Fresh fruit or salad\n"
        plan += f"Dinner: Fish with vegetables and quinoa\n\n"
        
        plan += f"TIPS\n"
        plan += f"{'-'*40}\n"
        plan += f"• Drink 8-10 glasses of water daily\n"
        plan += f"• Eat smaller, frequent meals\n"
        plan += f"• Avoid processed and fried foods\n"
        plan += f"• Exercise regularly with proper nutrition\n"
        plan += f"• Consult a nutritionist for customization\n"
        
        return plan
