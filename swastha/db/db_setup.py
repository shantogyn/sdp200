"""
Database Setup Module
Creates database and tables for Swastha application
"""

import mysql.connector
from mysql.connector import Error
import config

class DatabaseSetup:
    """Class to setup and initialize database"""
    
    def __init__(self):
        """Initialize setup parameters"""
        self.host = config.DB_HOST
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD
        self.database = config.DB_NAME
    
    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f"✓ Database '{self.database}' ready")
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"✗ Database Creation Error: {e}")
            return False
    
    def create_tables(self):
        """Create all required tables"""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conn.cursor()
            
            # Users Table
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(150) UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(users_table)
            print("✓ Users table created")
            
            # Medicines Table
            medicines_table = """
            CREATE TABLE IF NOT EXISTS medicines (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                medicine_name VARCHAR(100) NOT NULL,
                dosage VARCHAR(50),
                time_hours VARCHAR(200),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            cursor.execute(medicines_table)
            print("✓ Medicines table created")
            
            # User Health Records Table
            health_records_table = """
            CREATE TABLE IF NOT EXISTS health_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                height FLOAT,
                weight FLOAT,
                blood_type VARCHAR(10),
                allergies TEXT,
                medical_conditions TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            cursor.execute(health_records_table)
            print("✓ Health Records table created")
            
            # Lab Results Table
            lab_results_table = """
            CREATE TABLE IF NOT EXISTS lab_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                test_name VARCHAR(100) NOT NULL,
                test_result TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            cursor.execute(lab_results_table)
            print("✓ Lab Results table created")
            
            # Mood Records Table
            mood_records_table = """
            CREATE TABLE IF NOT EXISTS mood_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                mood VARCHAR(50),
                mood_level INT,
                notes TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            cursor.execute(mood_records_table)
            print("✓ Mood Records table created")
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✓ All tables created successfully")
            return True
        except Error as e:
            print(f"✗ Table Creation Error: {e}")
            return False
    
    def setup_all(self):
        """Run complete database setup"""
        print("\n=== Starting Database Setup ===")
        if self.create_database():
            if self.create_tables():
                print("=== Database Setup Complete ===\n")
                return True
        return False

# Initialize database on startup
if __name__ == "__main__":
    setup = DatabaseSetup()
    setup.setup_all()
