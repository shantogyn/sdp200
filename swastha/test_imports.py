
"""
Test script to verify all imports work correctly
"""

import sys
import os

print("=" * 60)
print("Testing Swastha Application Imports")
print("=" * 60)

# Test 1: Check Python version
print(f"\n1. Python Version: {sys.version}")
if sys.version_info.major >= 3 and sys.version_info.minor >= 6:
    print("   ✅ Python version is compatible")
else:
    print("   ❌ Python version too old (requires 3.6+)")
    sys.exit(1)

# Test 2: Test basic imports
print("\n2. Testing module imports...")
try:
    import tkinter as tk
    print("   ✅ Tkinter imported")
except ImportError as e:
    print(f"   ❌ Tkinter import failed: {e}")
    sys.exit(1)

try:
    import mysql.connector
    print("   ✅ MySQL Connector imported")
except ImportError as e:
    print(f"   ⚠️  MySQL Connector not installed: {e}")
    print("      Install with: pip install mysql-connector-python")

# Test 3: Test project module imports
print("\n3. Testing project modules...")
try:
    from config import *
    print("   ✅ config imported")
except Exception as e:
    print(f"   ❌ config import failed: {e}")
    sys.exit(1)

try:
    from utils.validation import Validator
    print("   ✅ utils.validation imported")
except Exception as e:
    print(f"   ❌ utils.validation import failed: {e}")
    sys.exit(1)

try:
    from utils.helpers import PasswordHelper
    print("   ✅ utils.helpers imported")
except Exception as e:
    print(f"   ❌ utils.helpers import failed: {e}")
    sys.exit(1)

try:
    from db.db_connection import db
    print("   ✅ db.db_connection imported")
except Exception as e:
    print(f"   ❌ db.db_connection import failed: {e}")
    sys.exit(1)

try:
    from db.db_setup import DatabaseSetup
    print("   ✅ db.db_setup imported")
except Exception as e:
    print(f"   ❌ db.db_setup import failed: {e}")
    sys.exit(1)

try:
    from ui.theme import COLORS, FONTS
    print("   ✅ ui.theme imported")
except Exception as e:
    print(f"   ❌ ui.theme import failed: {e}")
    sys.exit(1)

try:
    from ui.components import CustomButton
    print("   ✅ ui.components imported")
except Exception as e:
    print(f"   ❌ ui.components import failed: {e}")
    sys.exit(1)

try:
    from ui.sidebar import Sidebar
    print("   ✅ ui.sidebar imported")
except Exception as e:
    print(f"   ❌ ui.sidebar import failed: {e}")
    sys.exit(1)

try:
    from auth.login import LoginWindow
    print("   ✅ auth.login imported")
except Exception as e:
    print(f"   ❌ auth.login import failed: {e}")
    sys.exit(1)

try:
    from auth.signup import SignupWindow
    print("   ✅ auth.signup imported")
except Exception as e:
    print(f"   ❌ auth.signup import failed: {e}")
    sys.exit(1)

try:
    from auth.reset_password import ResetPasswordWindow
    print("   ✅ auth.reset_password imported")
except Exception as e:
    print(f"   ❌ auth.reset_password import failed: {e}")
    sys.exit(1)

try:
    from ui.dashboard import Dashboard
    print("   ✅ ui.dashboard imported")
except Exception as e:
    print(f"   ❌ ui.dashboard import failed: {e}")
    sys.exit(1)

# Test features
feature_modules = [
    "disease_prediction",
    "chatbot",
    "medicine_reminder",
    "lab_analyzer",
    "diet_guide",
    "mental_health",
    "image_analyzer",
    "first_aid",
    "disease_info"
]

print("\n4. Testing feature modules...")
for module_name in feature_modules:
    try:
        module = __import__(f"features.{module_name}", fromlist=[module_name])
        print(f"   ✅ features.{module_name} imported")
    except Exception as e:
        print(f"   ❌ features.{module_name} import failed: {e}")
        sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL IMPORTS SUCCESSFUL!")
print("=" * 60)
print("\nYou can now run: python3 main.py")
print("\nNote: Make sure MySQL server is running before starting the app")
print("=" * 60)
