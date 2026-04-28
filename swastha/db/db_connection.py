"""
Database Connection Module
Handles MySQL database connections for Swastha application
"""

import mysql.connector
from mysql.connector import Error
import config

class DatabaseConnection:
    """Class to manage MySQL database connections"""
    
    def __init__(self):
        """Initialize database connection parameters"""
        self.connection = None
        self.host = config.DB_HOST
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD
        self.database = config.DB_NAME
        self.port = config.DB_PORT
    
    def connect(self):
        """
        Establish connection to MySQL database
        Returns: Connection object or None if failed
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print(f"✓ Connected to {self.database} database")
                return self.connection
        except Error as e:
            print(f"✗ Database Connection Error: {e}")
            return None
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query, params=None):
        """
        Execute SELECT query and return results
        Args:
            query: SQL query string
            params: Query parameters (optional)
        Returns: List of results or None if failed
        """
        if not self.connection or not self.connection.is_connected():
            print("✗ No database connection")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"✗ Query Execution Error: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """
        Execute INSERT, UPDATE, DELETE queries
        Args:
            query: SQL query string
            params: Query parameters (optional)
        Returns: Boolean indicating success
        """
        if not self.connection or not self.connection.is_connected():
            print("✗ No database connection")
            return False

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            self.connection.rollback()
            print(f"✗ Update Error: {e}")
            return False
    
    def get_connection(self):
        """Get current database connection"""
        return self.connection
    
    def is_connected(self):
        """Check if database is connected"""
        if self.connection:
            return self.connection.is_connected()
        return False

# Create global database instance
db = DatabaseConnection()
