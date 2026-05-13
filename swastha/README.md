# 🏥 Swastha - AI Smart Healthcare System

A comprehensive production-quality desktop application built with Python 3, Tkinter, and MySQL for intelligent healthcare management.

## 🎯 Features

### Authentication System
- ✅ User Registration (Sign Up)
- ✅ Secure Login with Password Hashing
- ✅ Password Reset Functionality
- ✅ Session Management

### Healthcare Features (9 Modules)

1. **🔍 Disease Prediction** - Analyzes symptoms and predicts potential diseases with confidence scores
2. **💬 AI Chatbot** - Intelligent conversational healthcare assistant
3. **💊 Medicine Reminder** - Track and manage medication schedules
4. **🧪 Lab Analyzer** - Store and analyze lab test results
5. **🥗 Diet Guide** - Personalized nutrition plans based on health metrics
6. **🧠 Mental Health** - Mood tracking and wellness resources
7. **🖼️ Image Analyzer** - Medical image analysis with simulated OCR
8. **🚑 First Aid** - Emergency first aid instructions and CPR guide
9. **📚 Disease Info** - Comprehensive disease information database

### Additional Features
- Modern dashboard UI with sidebar navigation
- Responsive card-based layout
- Database persistence for all user data
- Professional color theme
- Comprehensive error handling
- Input validation

## 📋 System Requirements

- **Python**: 3.6 or higher
- **Operating System**: Windows, macOS, or Linux
- **MySQL Server**: 5.7 or higher
- **RAM**: Minimum 2GB
- **Storage**: 500MB

## 🔧 Installation & Setup

### Step 1: Install Python Dependencies

```bash
pip install mysql-connector-python
```

### Step 2: Install & Configure MySQL Database

**Windows/Mac:**
1. Download MySQL from: https://dev.mysql.com/downloads/mysql/
2. Install with default settings
3. During installation, set:
   - Root user: `root`
   - Password: `root` (or your preference)
   - Port: `3306`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

**Linux (Fedora/CentOS):**
```bash
sudo dnf install mysql-server
sudo systemctl start mysqld
sudo mysql_secure_installation
```

### Step 3: Configure Application

Edit `config.py` in the project root:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"  # Change if your MySQL password is different
DB_NAME = "swastha"
DB_PORT = 3306
```

### Step 4: Run the Application

#### Windows:
```bash
cd path\to\swastha
python main.py
```

#### macOS/Linux:
```bash
cd path/to/swastha
python3 main.py
```

## 🚀 Quick Start

1. **First Run**: The application will automatically:
   - Create the `swastha` database
   - Create all required tables
   - Connect to MySQL

2. **Create Account**: Click "Sign Up" and create new account
   - Username: Must be 3+ characters, alphanumeric
   - Email: Valid email format
   - Password: Min 6 chars, must contain uppercase, lowercase, numbers

3. **Login**: Use your credentials to login

4. **Explore Features**: Click on features in the sidebar to explore

## 📁 Project Structure

```
swastha/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
│
├── db/
│   ├── db_connection.py   # Database connection management
│   └── db_setup.py        # Database initialization
│
├── auth/
│   ├── login.py           # Login UI and authentication
│   ├── signup.py          # User registration
│   └── reset_password.py  # Password recovery
│
├── ui/
│   ├── theme.py           # Color scheme and styling
│   ├── components.py      # Reusable UI components
│   ├── sidebar.py         # Navigation sidebar
│   └── dashboard.py       # Main dashboard
│
├── features/
│   ├── disease_prediction.py
│   ├── chatbot.py
│   ├── medicine_reminder.py
│   ├── lab_analyzer.py
│   ├── diet_guide.py
│   ├── mental_health.py
│   ├── image_analyzer.py
│   ├── first_aid.py
│   └── disease_info.py
│
└── utils/
    ├── validation.py      # Input validation
    └── helpers.py         # Utility functions
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Medicines Table
```sql
CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    medicine_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    time_hours VARCHAR(200),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

Similar tables exist for: `health_records`, `lab_results`, `mood_records`

## 🎨 UI Features

- **Modern Design**: Clean, professional interface with consistent styling
- **Responsive Layout**: Adapts to different screen sizes (minimum 800x600)
- **Color Theme**: Professional healthcare color palette
- **Navigation**: Easy sidebar navigation between features
- **Cards & Sections**: Organized content with clear visual hierarchy

## 🔒 Security Features

- ✅ Password Hashing (SHA256 with PBKDF2)
- ✅ Input Validation
- ✅ SQL Injection Prevention (Parameterized Queries)
- ✅ User Session Management
- ✅ Email Format Validation

## 🐛 Troubleshooting

### "Connection Refused" or "Database Error"
**Solution**: 
- Check MySQL is running: `mysql -u root -p`
- Verify config.py has correct credentials
- Check firewall isn't blocking port 3306

### "ModuleNotFoundError: mysql.connector"
**Solution**: 
```bash
pip install mysql-connector-python
```

### Application won't start
**Solution**:
- Ensure Python 3.6+: `python --version`
- Check all dependencies: `pip list`
- Run from swastha directory with full path

### MySQL password issues
**Solution**:
- Reset MySQL password (Windows):
```bash
mysqld --skip-grant-tables
```
- Then reset in MySQL with proper credentials

## 📝 Default Test Account

After first run, you can create test accounts. There's no default account for security.

## 🔄 How Features Work

### Disease Prediction
1. Enter symptoms separated by commas
2. System analyzes against symptom database
3. Returns predicted disease with confidence score

### Medicine Reminder
1. Add medicine name, dosage, and times
2. View all medicines in list
3. Delete outdated reminders

### Diet Guide
1. Enter age, weight, height, activity level
2. System calculates BMI and daily caloric needs
3. Generates personalized nutrition plan

### Mental Health
1. Log your mood and optional notes
2. View mood history
3. Access wellness resources and tips

### First Aid
1. Select emergency type
2. View step-by-step instructions
3. Emergency contact info available

## 📊 Data Storage

All user data is securely stored in MySQL:
- Medicines and dosages
- Lab results
- Mood records
- Health metrics
- Personal information

## 🎓 Code Quality

- ✅ Object-Oriented Programming
- ✅ Modular Architecture
- ✅ Clean Code Principles
- ✅ Comprehensive Comments
- ✅ Consistent Naming Conventions
- ✅ Error Handling
- ✅ Input Validation

## ⚖️ Legal Disclaimer

**IMPORTANT**: This application is for educational purposes only. The health information and predictions provided are NOT medical advice and should NOT be used for diagnosis or treatment. Always consult with qualified healthcare professionals for medical concerns.

## 📄 License

This project is provided for educational purposes.

## 🤝 Support

For issues or questions:
1. Check troubleshooting section above
2. Verify MySQL is running
3. Ensure config.py is correctly configured
4. Check that all dependencies are installed

## 🎯 Future Enhancements

Possible additions:
- Integration with real medical APIs
- AI-powered diagnosis (ML models)
- Appointment scheduling
- Doctor consultation booking
- Health report generation
- Export data to PDF
- Multi-language support
- Cloud backup


---

**Built with ❤️ using Python & Tkinter **
