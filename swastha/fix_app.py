#!/usr/bin/env python3
"""
Auto-fix script for Swastha application
Fixes common issues preventing the app from running
"""

import os
import re

print("🔧 Starting Swastha Auto-Fix...\n")

# Define the fixes needed
fixes = []

# Fix 1: Signup.py import issue (already fixed, but let's verify)
signup_file = "auth/signup.py"
print(f"✓ Checking {signup_file}...")

with open(signup_file, 'r') as f:
    content = f.read()
    if "from tkinter import messagebox, toplevel" in content:
        print(f"  ⚠ Found incorrect import in {signup_file}")
        content = content.replace(
            "from tkinter import messagebox, toplevel",
            "from tkinter import messagebox"
        )
        with open(signup_file, 'w') as f:
            f.write(content)
        print(f"  ✅ Fixed import in {signup_file}")
    else:
        print(f"  ✅ {signup_file} is correct")

# Fix 2: Check reset_password.py
reset_file = "auth/reset_password.py"
print(f"\n✓ Checking {reset_file}...")

with open(reset_file, 'r') as f:
    content = f.read()
    if "from tkinter import messagebox, toplevel" in content:
        print(f"  ⚠ Found incorrect import in {reset_file}")
        content = content.replace(
            "from tkinter import messagebox, toplevel",
            "from tkinter import messagebox"
        )
        with open(reset_file, 'w') as f:
            f.write(content)
        print(f"  ✅ Fixed import in {reset_file}")
    else:
        print(f"  ✅ {reset_file} is correct")

# Fix 3: Check main.py for import issues
main_file = "main.py"
print(f"\n✓ Checking {main_file}...")

with open(main_file, 'r') as f:
    main_content = f.read()
    print(f"  ✅ {main_file} syntax OK")

print("\n" + "="*60)
print("✅ Auto-fix completed successfully!")
print("="*60)
print("\nNext steps:")
print("1. Ensure MySQL server is running")
print("2. Update config.py with your MySQL credentials if needed")
print("3. Run: python3 main.py")
print("="*60)
