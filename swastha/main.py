"""
Swastha 
Main Application 
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from db.db_setup import DatabaseSetup
from db.db_connection import db
from auth.login import LoginWindow
from ui.dashboard import Dashboard

class SwasthaApp:
    """Main Application Class"""
    
    def __init__(self, root):
        """Initialize Swastha Application"""
        self.root = root
        self.root.title(config.APP_TITLE)
        self.root.geometry(config.WINDOW_GEOMETRY)
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(800, 600)
        #set maximum window size
       # self.root.maxsize(1920, 1080)
        # Center window on screen
        self.center_window()
        
        # Initialize database
        self.initialize_database()
        
        # Show login screen
        self.show_login()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (config.WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (config.WINDOW_HEIGHT // 2)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{x}+{y}")
    
    def initialize_database(self):
        """Initialize database"""
        try:
            # Setup database and tables
            setup = DatabaseSetup()
            setup.setup_all()
            
            # Connect to database
            db.connect()
            
            if not db.is_connected():
                messagebox.showerror(
                    "Database Error",
                    "Failed to connect to database.\n\nPlease ensure MySQL is installed and running.\n\nUpdate DB_PASSWORD in config.py if needed."
                )
                sys.exit(1)
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Error initializing database: {e}\n\nPlease check MySQL configuration."
            )
            sys.exit(1)
    
    def show_login(self):
        """Show login screen"""
        login = LoginWindow(self.root, on_login_success=self.on_login_success)
    
    def on_login_success(self, user_id, username):
        """Handle successful login"""
        dashboard = Dashboard(self.root, user_id, username)

def main():
    """Main entry point"""
    # Create root window
    root = tk.Tk()
    
    # Initialize application
    app = SwasthaApp(root)
    
    # Start event loop
    root.mainloop()

if __name__ == "__main__":
    main()
