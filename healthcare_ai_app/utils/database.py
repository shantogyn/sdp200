"""
Database Manager - SQLite operations for the Healthcare Assistant
"""

import sqlite3
import os
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "healthcare.db")


class DatabaseManager:
    """Handles all SQLite database operations."""

    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.db_path = DB_PATH

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def initialize(self):
        """Create all required tables if they don't exist."""
        conn = self.get_connection()
        cur = conn.cursor()

        # Reminders table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_name TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                dosage TEXT,
                notes TEXT,
                active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Chat history table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # User profile table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                weight REAL,
                blood_group TEXT,
                allergies TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    # ── Reminders ──────────────────────────────────────────────────────────────

    def add_reminder(self, medicine_name, reminder_time, dosage="", notes=""):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reminders (medicine_name, reminder_time, dosage, notes) VALUES (?, ?, ?, ?)",
            (medicine_name, reminder_time, dosage, notes)
        )
        conn.commit()
        conn.close()

    def get_reminders(self, active_only=True):
        conn = self.get_connection()
        cur = conn.cursor()
        if active_only:
            cur.execute("SELECT * FROM reminders WHERE active=1 ORDER BY reminder_time")
        else:
            cur.execute("SELECT * FROM reminders ORDER BY reminder_time")
        rows = cur.fetchall()
        conn.close()
        return rows

    def delete_reminder(self, reminder_id):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
        conn.commit()
        conn.close()

    # ── Chat History ───────────────────────────────────────────────────────────

    def save_message(self, role, message):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history (role, message) VALUES (?, ?)",
            (role, message)
        )
        conn.commit()
        conn.close()

    def get_chat_history(self, limit=50):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT role, message, timestamp FROM chat_history ORDER BY id DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return list(reversed(rows))

    def clear_chat_history(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM chat_history")
        conn.commit()
        conn.close()
