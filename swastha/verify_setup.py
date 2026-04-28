#!/usr/bin/env python3
"""
Comprehensive Swastha Setup & Test Script
Verifies all components are working correctly
"""

import sys
import os
import subprocess

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_check(status, message):
    symbol = "✅" if status else "❌"
    print(f"  {symbol} {message}")

def print_warning(message):
    print(f"  ⚠️  {message}")

# Start
print_header("SWASTHA APPLICATION - SETUP & VERIFICATION")

# Change to app directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Check 1: Python version
print_header("1. CHECKING PYTHON VERSION")
py_version = sys.version_info
print(f"  Python: {py_version.major}.{py_version.minor}.{py_version.micro}")
py_ok = py_version.major >= 3 and py_version.minor >= 6
print_check(py_ok, "Python version compatible")
if not py_ok:
    print("  ❌ FATAL: Python 3.6+ required")
    sys.exit(1)

# Check 2: Required modules
print_header("2. CHECKING PYTHON MODULES")

modules_ok = True
try:
    import tkinter
    print_check(True, "tkinter (built-in)")
except ImportError:
    print_check(False, "tkinter (INSTALL REQUIRED)")
    modules_ok = False

try:
    import mysql.connector
    print_check(True, "mysql-connector-python")
except ImportError:
    print_warning("mysql-connector-python not installed")
    print("  Install with: pip install mysql-connector-python")
    modules_ok = False

# Check 3: Project files
print_header("3. CHECKING PROJECT FILES")

required_files = [
    "main.py",
    "config.py",
    "requirements.txt",
    "db/db_connection.py",
    "db/db_setup.py",
    "auth/login.py",
    "auth/signup.py",
    "auth/reset_password.py",
    "ui/theme.py",
    "ui/components.py",
    "ui/sidebar.py",
    "ui/dashboard.py",
    "utils/validation.py",
    "utils/helpers.py",
    "features/disease_prediction.py",
    "features/chatbot.py",
    "features/medicine_reminder.py",
    "features/lab_analyzer.py",
    "features/diet_guide.py",
    "features/mental_health.py",
    "features/image_analyzer.py",
    "features/first_aid.py",
    "features/disease_info.py",
]

files_ok = True
for file_path in required_files:
    exists = os.path.isfile(file_path)
    if not exists:
        print_check(False, f"{file_path}")
        files_ok = False
    
print_check(files_ok, f"All {len(required_files)} project files present")

# Check 4: File syntax
print_header("4. CHECKING PYTHON SYNTAX")

syntax_ok = True
critical_files = [
    "main.py",
    "config.py",
    "auth/login.py",
    "auth/signup.py",
    "db/db_connection.py",
]

for file_path in critical_files:
    try:
        with open(file_path, 'r') as f:
            compile(f.read(), file_path, 'exec')
        print_check(True, f"{file_path}")
    except SyntaxError as e:
        print_check(False, f"{file_path}: {e}")
        syntax_ok = False

# Check 5: Config file
print_header("5. CHECKING CONFIGURATION")

try:
    with open("config.py", 'r') as f:
        content = f.read()
        
    # Extract config values
    import re
    db_host = re.search(r'DB_HOST\s*=\s*["\']([^"\']+)["\']', content)
    db_user = re.search(r'DB_USER\s*=\s*["\']([^"\']+)["\']', content)
    db_pass = re.search(r'DB_PASSWORD\s*=\s*["\']([^"\']+)["\']', content)
    db_name = re.search(r'DB_NAME\s*=\s*["\']([^"\']+)["\']', content)
    
    if db_host and db_user and db_pass and db_name:
        print(f"  Database Host: {db_host.group(1)}")
        print(f"  Database User: {db_user.group(1)}")
        print(f"  Database Name: {db_name.group(1)}")
        print_check(True, "Configuration file valid")
    else:
        print_check(False, "Configuration file incomplete")
        
except Exception as e:
    print_check(False, f"Error reading config: {e}")

# Check 6: Import test
print_header("6. TESTING IMPORTS")

imports_ok = True
test_imports = [
    ("config", None),
    ("utils.validation", "Validator"),
    ("utils.helpers", "PasswordHelper"),
    ("db.db_connection", "db"),
    ("ui.theme", "COLORS"),
    ("auth.login", "LoginWindow"),
]

for module_name, class_name in test_imports:
    try:
        module = __import__(module_name, fromlist=[class_name] if class_name else [])
        if class_name:
            getattr(module, class_name)
        print_check(True, module_name)
    except Exception as e:
        print_check(False, f"{module_name}: {str(e)[:50]}")
        imports_ok = False

# Summary
print_header("VERIFICATION SUMMARY")

all_ok = py_ok and files_ok and syntax_ok and imports_ok

if all_ok:
    print_check(True, "All checks passed!")
    print("\n✅ APPLICATION IS READY TO RUN\n")
    print("Next steps:")
    print("  1. Make sure MySQL Server is running")
    print("  2. Run: python3 main.py")
    print("\nIf MySQL is not installed:")
    print("  - Linux: sudo apt-get install mysql-server")
    print("  - macOS: brew install mysql")
    print("  - Windows: Download from mysql.com")
else:
    print("\n❌ SOME CHECKS FAILED\n")
    print("Please fix the issues above and try again.")
    if not modules_ok:
        print("\nTo install missing modules:")
        print("  pip install -r requirements.txt")
    sys.exit(1)

print("="*70 + "\n")
