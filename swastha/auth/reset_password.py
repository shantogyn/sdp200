"""
Reset Password Module
Handles password reset functionality
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_connection import db
from utils.validation import Validator
from utils.helpers import PasswordHelper

class ResetPasswordWindow:
    """Class to handle password reset"""
    
    def __init__(self, parent, login_window, use_root=False):
        """
        Initialize reset password window
        Args:
            parent: Parent window
            login_window: Reference to login window
            use_root: Use parent as main window instead of Toplevel
        """
        self.parent = parent
        self.login_window = login_window
        self.use_root = use_root

        if self.use_root:
            for widget in self.parent.winfo_children():
                widget.destroy()
            self.parent.title("Swastha - Reset Password")
            self.container = self.parent
        else:
            self.reset_root = tk.Toplevel(parent)
            self.reset_root.title("Swastha - Reset Password")
            self.reset_root.geometry("500x500+400+150")
            self.reset_root.resizable(False, False)
            self.container = self.reset_root

        self.setup_ui()
    
    def setup_ui(self):
        """Setup reset password UI"""
        if not self.use_root:
            self.reset_root.title("Swastha - Reset Password")
            self.reset_root.geometry("500x500+400+150")
            self.reset_root.resizable(False, False)
        
        # Main frame
        main_frame = tk.Frame(self.container, bg="#f0f0f0", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            main_frame,
            text="Reset Password",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title.pack(pady=(0, 10))
        
        # Instructions
        info = tk.Label(
            main_frame,
            text="Enter your username and email to reset password",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        info.pack(pady=(0, 20))
        
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
        
        # New password field
        tk.Label(
            main_frame,
            text="New Password",
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
        
        hint = tk.Label(
            main_frame,
            text="(Min 6 chars: uppercase, lowercase, numbers)",
            font=("Arial", 8),
            bg="#f0f0f0",
            fg="#95a5a6"
        )
        hint.pack(anchor="w", pady=(0, 15))
        
        # Reset button
        reset_btn = tk.Button(
            main_frame,
            text="Reset Password",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.reset_password,
            padx=20,
            pady=10
        )
        reset_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Back button
        back_btn = tk.Button(
            main_frame,
            text="Back to Login",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#3498db",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.go_back,
            padx=0
        )
        back_btn.pack(anchor="w")

    def go_back(self):
        """Go back to login screen"""
        if self.use_root:
            self.login_window.setup_ui()
        else:
            self.reset_root.destroy()
    
    def reset_password(self):
        """Reset password for user"""
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        
        # Validate inputs
        if not username:
            messagebox.showerror("Error", "Please enter username")
            return
        
        if not email:
            messagebox.showerror("Error", "Please enter email")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter new password")
            return
        
        # Validate password
        is_valid, msg = Validator.validate_password(password)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return
        
        # Check database
        if not db.is_connected():
            db.connect()
        
        query = "SELECT id FROM users WHERE username = %s AND email = %s"
        results = db.execute_query(query, (username, email))
        
        if not results:
            messagebox.showerror("Error", "Username and email do not match any account")
            return
        
        # Update password
        hashed_password = PasswordHelper.hash_password(password)
        update_query = "UPDATE users SET password = %s WHERE username = %s"
        
        if db.execute_update(update_query, (hashed_password, username)):
            messagebox.showinfo("Success", "Password reset successfully! You can now login.")
            if self.use_root:
                self.login_window.setup_ui()
            else:
                self.reset_root.destroy()
