"""
Chatbot Module
AI-powered healthcare chatbot
"""

import tkinter as tk
from tkinter import scrolledtext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import COLORS, FONTS, PADDING
from ui.components import CustomButton, CustomEntry

class ChatbotUI:
    """Chatbot Feature UI"""
    
    def __init__(self, parent, user_id):
        """Initialize chatbot UI"""
        self.parent = parent
        self.user_id = user_id
        self.conversation_history = []
        self.create_ui()
    
    def create_ui(self):
        """Create chatbot UI"""
        # Title
        title = tk.Label(
            self.parent,
            text="💬 AI Health Chatbot",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Main container
        container = tk.Frame(self.parent, bg=COLORS["white"], relief="raised", bd=1)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Chat display
        chat_label = tk.Label(
            container,
            text="Conversation",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        chat_label.pack(anchor="w", fill=tk.X)
        
        # Chat text widget
        self.chat_display = scrolledtext.ScrolledText(
            container,
            font=FONTS["body_medium"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            height=15,
            width=70,
            relief="solid",
            bd=1,
            state="disabled"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Welcome message
        self.add_bot_message("👋 Hello! I'm your AI Health Assistant. How can I help you today?")
        
        # Input section
        input_frame = tk.Frame(container, bg=COLORS["white"])
        input_frame.pack(fill=tk.X, padx=PADDING["md"], pady=PADDING["md"])
        
        # Input field
        self.message_entry = tk.Entry(
            input_frame,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"],
            relief="solid",
            bd=1
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING["sm"]))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        send_btn = CustomButton(
            input_frame,
            text="Send",
            command=self.send_message,
            padx=20
        )
        send_btn.pack(side=tk.LEFT)
    
    def send_message(self):
        """Send message to chatbot"""
        message = self.message_entry.get().strip()
        
        if not message:
            return
        
        # Add user message
        self.add_user_message(message)
        self.message_entry.delete(0, tk.END)
        
        # Get bot response
        response = self.get_bot_response(message)
        self.add_bot_message(response)
    
    def add_user_message(self, message):
        """Add user message to chat"""
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"You: {message}\n", "user")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)
    
    def add_bot_message(self, message):
        """Add bot message to chat"""
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"Bot: {message}\n\n", "bot")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)
    
    def get_bot_response(self, message):
        """Get response from chatbot"""
        message_lower = message.lower()
        
        # Knowledge base
        responses = {
            "symptoms": "Please describe your symptoms in detail. Are you experiencing fever, cough, body ache, or any other discomfort?",
            "fever": "A fever indicates your body is fighting an infection. Stay hydrated, rest well, and monitor your temperature. Consult a doctor if it persists.",
            "cough": "Coughs can be due to various reasons like cold, flu, or allergies. Drink warm liquids and see a doctor if it lasts more than 2 weeks.",
            "headache": "Headaches can result from stress, dehydration, or lack of sleep. Try to relax and stay hydrated. Persistent headaches need medical attention.",
            "medicine": "Always consult a healthcare professional before taking any medicine. Our Medicine Reminder feature can help you track your medicines.",
            "diet": "A balanced diet is essential for good health. Our Diet Guide feature can suggest personalized nutrition plans based on your health profile.",
            "exercise": "Regular exercise is important for maintaining good health. Aim for at least 30 minutes of physical activity daily.",
            "sleep": "Getting 7-9 hours of quality sleep daily is crucial for your health and immune system.",
            "stress": "Stress can negatively impact your health. Try meditation, yoga, or breathing exercises. Our Mental Health feature has more resources.",
            "help": "I can help you with health information, symptom analysis, medicine reminders, and general wellness advice. What would you like to know?",
        }
        
        # Match keywords
        for keyword, response in responses.items():
            if keyword in message_lower:
                return response
        
        # Default response
        return "I understand your concern. Could you provide more details? You can also check our Disease Prediction feature for symptom analysis."
