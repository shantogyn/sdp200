"""
Configuration file for Swastha 
Contains all configuration settings for the application
"""

# Database Configuration
DB_HOST = "localhost"
DB_USER = "swastha"
DB_PASSWORD = "1234"  
DB_NAME = "swastha"
DB_PORT = 3306

# Application Settings
APP_TITLE = "Swastha "
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+100+100"

# Feature Settings
FEATURES = [
    "Disease Prediction",
    "AI Chatbot",
    "Medicine Reminder",
    "Lab Analyzer",
    "Diet Guide",
    "Mental Health",
    "Image Analyzer",
    "First Aid",
    "Disease Info"
]

# Reminder Settings
REMINDER_CHECK_INTERVAL = 60000  # Check every 60 seconds in milliseconds
