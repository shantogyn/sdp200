"""
Signup Module
Handles user registration
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_connection import db
from utils.validation import Validator
from utils.helpers import PasswordHelper

class SignupWindow:
    """Class to handle signup window"""
    
    def __init__(self, parent, login_window):
        """
        Initialize signup window
        Args:
            parent: Parent window
            login_window: Reference to login window
        """
        self.parent = parent
        self.login_window = login_window
        self.signup_root = tk.Toplevel(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup signup UI"""
        self.signup_root.title("Swastha - Sign Up")
        self.signup_root.geometry("500x700+400+100")
        self.signup_root.resizable(False, False)
        
        # Main frame
        main_frame = tk.Frame(self.signup_root, bg="#f0f0f0", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            main_frame,
            text="Create Account",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title.pack(pady=(0, 20))
        
        # Username field
        tk.Label(
            main_frame,
            text="Username",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(5, 0))
        
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(
            main_frame,
            textvariable=self.username_var,
            font=("Arial", 11),
            relief=tk.FLAT,
            bg="white",
            fg="#2c3e50"
        )
        username_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Email field
        tk.Label(
            main_frame,
            text="Email Address",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(5, 0))
        
        self.email_var = tk.StringVar()
        email_entry = tk.Entry(
            main_frame,
            textvariable=self.email_var,
            font=("Arial", 11),
            relief=tk.FLAT,
            bg="white",
            fg="#2c3e50"
        )
        email_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Password field
        tk.Label(
            main_frame,
            text="Password",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(5, 0))
        
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            main_frame,
            textvariable=self.password_var,
            font=("Arial", 11),
            relief=tk.FLAT,
            bg="white",
            fg="#2c3e50",
            show="●"
        )
        password_entry.pack(fill=tk.X, pady=(0, 5), ipady=8)
        
        # Password hint
        hint = tk.Label(
            main_frame,
            text="(Min 6 chars: uppercase, lowercase, numbers)",
            font=("Arial", 8),
            bg="#f0f0f0",
            fg="#95a5a6"
        )
        hint.pack(anchor="w", pady=(0, 15))
        
        # Confirm Password field
        tk.Label(
            main_frame,
            text="Confirm Password",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(5, 0))
        
        self.confirm_password_var = tk.StringVar()
        confirm_entry = tk.Entry(
            main_frame,
            textvariable=self.confirm_password_var,
            font=("Arial", 11),
            relief=tk.FLAT,
            bg="white",
            fg="#2c3e50",
            show="●"
        )
        confirm_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # Sign up button
        signup_btn = tk.Button(
            main_frame,
            text="Sign Up",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.register,
            padx=20,
            pady=10
        )
        signup_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Back button
        back_btn = tk.Button(
            main_frame,
            text="Back to Login",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#3498db",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.signup_root.destroy,
            padx=0
        )
        back_btn.pack(anchor="w")
    
    def register(self):
        """Register new user"""
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Validate username
        is_valid, msg = Validator.validate_username(username)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return
        
        # Validate email
        is_valid, msg = Validator.validate_email(email)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return
        
        # Validate password
        is_valid, msg = Validator.validate_password(password)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return
        
        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Check if user already exists
        if not db.is_connected():
            db.connect()
        
        query = "SELECT id FROM users WHERE username = %s OR email = %s"
        results = db.execute_query(query, (username, email))
        
        if results:
            messagebox.showerror("Error", "Username or email already exists")
            return
        
        # Hash password and insert into database
        hashed_password = PasswordHelper.hash_password(password)
        insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        
        if db.execute_update(insert_query, (username, email, hashed_password)):
            messagebox.showinfo("Success", "Account created successfully! You can now login.")
            self.signup_root.destroy()
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again.")
