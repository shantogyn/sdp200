# SWASTHA SETUP GUIDE - Step by Step

## ✅ Prerequisites Checklist

- [ ] Python 3.6+ installed
- [ ] MySQL Server installed and running
- [ ] Administrator access (for installing packages)
- [ ] 500MB free disk space

---

## 🔷 Step 1: Verify Python Installation

### Windows & Mac:
```bash
python --version
python -m pip --version
```

### Linux:
```bash
python3 --version
python3 -m pip --version
```

**Expected Output**: Python 3.6 or higher and pip version

---

## 🔷 Step 2: Install MySQL Server

### Windows:
1. Download from: https://dev.mysql.com/downloads/mysql/
2. Run installer
3. Choose "Developer Default"
4. Configure MySQL Server:
   - Port: 3306
   - Config Type: Server
   - Root password: `root` (or remember your password)
5. Click "Execute" and finish

### macOS (Homebrew):
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install mysql-server -y
sudo mysql_secure_installation
sudo systemctl start mysql
```

### Verify MySQL:
```bash
mysql -u root -p
```
Enter password when prompted. If successful, you'll see `mysql>` prompt.

---

## 🔷 Step 3: Download & Prepare Project

### Option A: If you have the project folder:
```bash
cd path/to/swastha
```

### Option B: Create fresh copy:
```bash
mkdir swastha_app
cd swastha_app
# Copy all project files here
```

---

## 🔷 Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- mysql-connector-python (MySQL database driver)

---

## 🔷 Step 5: Configure Database Connection

Open `config.py` and update:

```python
DB_HOST = "localhost"      # Usually: localhost
DB_USER = "root"           # MySQL username
DB_PASSWORD = "root"       # MySQL password (use your password)
DB_NAME = "swastha"        # Database name (keep this)
DB_PORT = 3306             # Usually: 3306
```

### Example (if you set different password):
```python
DB_PASSWORD = "MySecurePassword123"
```

---

## 🔷 Step 6: Verify Database Connection (CRITICAL)

Create a test file `test_db.py`:

```python
from db.db_connection import db

if db.connect():
    print("✓ Database connection successful!")
    db.disconnect()
else:
    print("✗ Database connection failed!")
    print("Check config.py - username/password may be wrong")
```

Run test:
```bash
python test_db.py
```

**Expected Output**: 
```
✓ Connected to swastha database
✓ Database connection successful!
✓ Database connection closed
```

**If it fails**:
- Check MySQL is running: `mysql -u root -p`
- Verify password in config.py
- Check firewall (port 3306)

---

## 🔷 Step 7: Start the Application

### Windows:
```bash
python main.py
```

### macOS/Linux:
```bash
python3 main.py
```

**First Run will**:
- ✅ Create `swastha` database
- ✅ Create all required tables
- ✅ Show Login Screen

---

## 🔷 Step 8: Create Your Account

1. Click **"Sign Up"**
2. Enter details:
   - **Username**: (3+ chars, alphanumeric, no spaces)
     - ✅ john_doe
     - ✅ user123
     - ✅ HealthGuy
   - **Email**: Valid email
     - ✅ user@example.com
     - ✅ name@gmail.com
   - **Password**: Min 6 chars, must have UPPERCASE, lowercase, NUMBERS
     - ✅ MyPassword123
     - ✅ Health@2024
     - ✗ password123 (no uppercase)
     - ✗ PASSWORD123 (no lowercase)

3. Click **"Sign Up"**
4. If successful: "Account created successfully!"
5. Login with your credentials

---

## 🔷 Step 9: Explore Features

Once logged in:

1. **Sidebar Left**: Shows all 9 features
2. **Main Area**: Click a feature to load it
3. **Top Bar**: Shows logged-in username
4. **Logout**: Bottom of sidebar

### Try each feature:
- 🔍 **Disease Prediction**: Type symptoms (comma-separated)
- 💬 **Chatbot**: Type health questions
- 💊 **Medicine Reminder**: Add medicines you take
- 🧪 **Lab Analyzer**: Mock upload lab results
- 🥗 **Diet Guide**: Enter age, weight, height
- 🧠 **Mental Health**: Log your mood
- 🖼️ **Image Analyzer**: Simulated medical image analysis
- 🚑 **First Aid**: Browse emergency guides
- 📚 **Disease Info**: Search disease information

---

## 🔶 Troubleshooting

### Problem: "Can't connect to database"

**Cause 1**: MySQL not running

**Solution**:
- **Windows**: 
  - Open Services (services.msc)
  - Find MySQL80 (or similar)
  - Click "Start service"
  
- **Mac**: 
  ```bash
  brew services start mysql
  ```

- **Linux**: 
  ```bash
  sudo systemctl start mysql
  ```

**Cause 2**: Wrong password in config.py

**Solution**:
```bash
mysql -u root -p
# Enter your MySQL password
# Type: exit
# Update config.py with correct password
```

**Cause 3**: MySQL not installed

**Solution**: Install MySQL (see Step 2 above)

---

### Problem: "ModuleNotFoundError: mysql.connector"

**Solution**:
```bash
pip install mysql-connector-python
```

If still not working:
```bash
pip install --upgrade mysql-connector-python
```

---

### Problem: "Port 3306 already in use"

**Windows/Mac**:
```bash
# Kill service using port
lsof -ti:3306 | xargs kill -9
```

**Then restart MySQL**

---

### Problem: Application crashes on startup

**Check**:
1. Is MySQL running?
2. Are credentials correct in config.py?
3. Can you connect manually?
   ```bash
   mysql -u root -p -h localhost
   ```

---

### Problem: "Permission Denied" (Linux/Mac)

**Solution**:
```bash
chmod +x main.py
python3 main.py
```

---

## 🟢 Application Ready!

Once you see the login screen, everything is working! 

### Next Steps:
1. Create an account
2. Login
3. Explore features
4. Add your health data
5. Share feedback!

---

## 🔴 Emergency: Reset Everything

If something goes very wrong:

### Option 1: Reset Database

```bash
# Connect to MySQL
mysql -u root -p

# In MySQL prompt:
DROP DATABASE IF EXISTS swastha;
EXIT;

# Run app again - it will recreate database
python3 main.py
```

### Option 2: Reset MySQL Password (Windows)

```bash
# Stop MySQL Service in Services.msc
# Then:
mysqld --skip-grant-tables

# In another terminal:
mysql -u root
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
EXIT;

# Restart MySQL Service
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] MySQL service running
- [ ] Can login to MySQL: `mysql -u root -p`
- [ ] Python dependencies installed: `pip list`
- [ ] config.py has correct password
- [ ] Application starts: `python3 main.py`
- [ ] Can create account
- [ ] Can login with account
- [ ] Can access all 9 features

---

## 📞 Still Having Issues?

1. **Check Logs**: Run `python3 main.py` and read error messages carefully
2. **Verify MySQL**: `mysql -u root -p -e "SELECT DATABASE();"`
3. **Check Database exists**: `mysql -u root -p -e "SHOW DATABASES;"`
4. **Check Tables**: `mysql -u root -p swastha -e "SHOW TABLES;"`

---

## 🎯 Success! 

You now have a fully functional healthcare system. Enjoy exploring all the features!

For more features or customization, see the main README.md file.
