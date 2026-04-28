"""
AI Smart Healthcare Assistant
Main entry point - launches the application
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import DatabaseManager
from ui.main_window import MainWindow


def main():
    """Initialize and run the application."""
    # Initialize database
    db = DatabaseManager()
    db.initialize()

    # Create root window
    root = tk.Tk()
    root.withdraw()  # Hide until fully loaded

    try:
        app = MainWindow(root)
        root.deiconify()
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Startup Error", f"Failed to start application:\n{e}")
        raise


if __name__ == "__main__":
    main()
