"""
Notifier - Background thread for medicine reminders
"""

import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class ReminderNotifier:
    """Background scheduler that checks medicine reminders every minute."""

    def __init__(self, db_manager):
        self.db = db_manager
        self.running = False
        self.thread = None
        self.notified_today = set()  # Track already-notified reminders

    def start(self):
        """Start the background checking thread."""
        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the background thread."""
        self.running = False

    def _check_loop(self):
        """Continuously check for due reminders."""
        while self.running:
            self._check_reminders()
            time.sleep(30)  # Check every 30 seconds

    def _check_reminders(self):
        """Check if any reminder time matches current time."""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")

        try:
            reminders = self.db.get_reminders(active_only=True)
            for reminder in reminders:
                rid, medicine, rtime, dosage, notes, active, created = reminder
                key = f"{rid}_{current_date}_{current_time}"

                if rtime == current_time and key not in self.notified_today:
                    self.notified_today.add(key)
                    self._show_notification(medicine, rtime, dosage)
        except Exception:
            pass  # Silently ignore DB errors during background check

    def _show_notification(self, medicine, rtime, dosage):
        """Show a popup notification for a medicine reminder."""
        # Schedule on main thread to avoid Tkinter threading issues
        def popup():
            try:
                root = tk.Tk()
                root.withdraw()
                msg = f"💊 Medicine Reminder!\n\nTime to take: {medicine}"
                if dosage:
                    msg += f"\nDosage: {dosage}"
                msg += f"\n\nScheduled time: {rtime}"
                messagebox.showinfo("Medicine Reminder 💊", msg, parent=root)
                root.destroy()
            except Exception:
                pass

        t = threading.Thread(target=popup, daemon=True)
        t.start()
