"""
Quick Start Script for Swastha
Verifies all dependencies and starts the application
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is 3.6+"""
    print("📦 Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✅ Python {version.major}.{version.minor}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (requires 3.6+)")
        return False

def check_mysql_connector():
    """Check if mysql-connector-python is installed"""
    print("📦 Checking mysql-connector-python...", end=" ")
    try:
        import mysql.connector
        print("✅ Installed")
        return True
    except ImportError:
        print("❌ Not installed")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n" + "="*50)
    print("Installing dependencies...")
    print("="*50 + "\n")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✅ Dependencies installed successfully!\n")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Failed to install dependencies\n")
        return False

def check_mysql_running():
    """Check if MySQL is running"""
    print("📦 Checking MySQL connection...", end=" ")
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
        conn.close()
        print("✅ MySQL is running")
        return True
    except Exception as e:
        print(f"❌ Cannot connect to MySQL")
        print(f"   Error: {str(e)}")
        print("\n⚠️  SETUP REQUIRED:")
        print("   1. Make sure MySQL Server is installed and running")
        print("   2. Update config.py with correct credentials")
        print("   3. Check that you can run: mysql -u root -p")
        return False

def verify_project_structure():
    """Verify project structure"""
    print("📦 Checking project structure...", end=" ")
    
    required_dirs = ["db", "auth", "ui", "features", "utils"]
    required_files = ["main.py", "config.py", "requirements.txt"]
    
    for dir_name in required_dirs:
        if not os.path.isdir(dir_name):
            print(f"❌ Missing directory: {dir_name}")
            return False
    
    for file_name in required_files:
        if not os.path.isfile(file_name):
            print(f"❌ Missing file: {file_name}")
            return False
    
    print("✅ Complete")
    return True

def start_application():
    """Start the Swastha application"""
    print("\n" + "="*50)
    print("🚀 Starting Swastha Application...")
    print("="*50 + "\n")
    
    try:
        subprocess.call([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Application closed.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("\n" + "="*50)
    print("🏥 SWASTHA - Quick Start Verification")
    print("="*50 + "\n")
    
    all_good = True
    
    # Check Python
    if not check_python_version():
        all_good = False
    
    # Check MySQL Connector
    if not check_mysql_connector():
        all_good = False
        print("\n💡 Installing mysql-connector-python...")
        if not install_dependencies():
            sys.exit(1)
    
    # Check project structure
    if not verify_project_structure():
        all_good = False
    
    # Check MySQL
    if not check_mysql_running():
        print("\n❌ Cannot start application without MySQL")
        sys.exit(1)
    
    # Summary
    print("\n" + "="*50)
    if all_good:
        print("✅ All checks passed! Ready to start.")
        print("="*50)
        start_application()
    else:
        print("❌ Some checks failed. Please fix issues above.")
        print("="*50)
        sys.exit(1)

if __name__ == "__main__":
    main()
