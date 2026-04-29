"""
Login Module
Handles user authentication and login
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_connection import db
from utils.validation import Validator
from utils.helpers import PasswordHelper
from auth.signup import SignupWindow
from auth.reset_password import ResetPasswordWindow

class LoginWindow:
    """Class to handle login window and authentication"""
    
    def __init__(self, root, on_login_success=None):
        """
        Initialize login window
        Args:
            root: Tkinter root window
            on_login_success: Callback function when login is successful
        """
        self.root = root
        self.on_login_success = on_login_success
        self.current_user_id = None
        self.current_username = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup login UI"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Swastha - Login")
        self.root.geometry("500x600+400+150")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            main_frame,
            text="🏥 Swastha",
            font=("Arial", 28, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title.pack(pady=(0, 5))
        
        subtitle = tk.Label(
            main_frame,
            text="AI Smart Healthcare System",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        subtitle.pack(pady=(0, 30))
        
        # Login heading
        heading = tk.Label(
            main_frame,
            text="Login to Your Account",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        heading.pack(pady=(0, 20))
        
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
        password_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # Login button
        login_btn = tk.Button(
            main_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2","Enter",
            command=self.login,
            padx=20,
            pady=10
        )
        login_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Forgot password button
        forgot_btn = tk.Button(
            main_frame,
            text="Forgot Password?",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#3498db",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_reset_password,
            padx=0
        )
        forgot_btn.pack(anchor="w", pady=(0, 15))
        
        # Separator
        sep = tk.Canvas(main_frame, height=1, bg="#bdc3c7", highlightthickness=0)
        sep.pack(fill=tk.X, pady=10)
        
        # Signup prompt
        signup_frame = tk.Frame(main_frame, bg="#f0f0f0")
        signup_frame.pack(fill=tk.X)
        
        signup_text = tk.Label(
            signup_frame,
            text="Don't have an account?",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        signup_text.pack(side=tk.LEFT)
        
        signup_btn = tk.Button(
            signup_frame,
            text="Sign Up",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            fg="#27ae60",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_signup,
            padx=0
        )
        signup_btn.pack(side=tk.LEFT, padx=(5, 0))
    
    def login(self):
        """Authenticate user"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        # Validation
        if not username:
            messagebox.showerror("Error", "Please enter username")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter password")
            return
        
        # Check database
        if not db.is_connected():
            db.connect()
        
        query = "SELECT id, username, password FROM users WHERE username = %s"
        results = db.execute_query(query, (username,))
        
        if results and len(results) > 0:
            user = results[0]
            # Verify password
            if PasswordHelper.verify_password(user['password'], password):
                self.current_user_id = user['id']
                self.current_username = user['username']
                messagebox.showinfo("Success", f"Welcome, {username}!")
                if self.on_login_success:
                    self.on_login_success(self.current_user_id, self.current_username)
            else:
                messagebox.showerror("Error", "Invalid password")
        else:
            messagebox.showerror("Error", "Username not found")
    
    def show_signup(self):
        """Show signup screen in the same window"""
        SignupWindow(self.root, self, use_root=True)
    
    def show_reset_password(self):
        """Show reset password screen in the same window"""
        ResetPasswordWindow(self.root, self, use_root=True)
    
    def get_current_user(self):
        """Get current logged-in user"""
        return {
            "id": self.current_user_id,
            "username": self.current_username
        }
