# utils/notification.py
# eita background notification system
# threading use kore background e choltei thake ar time-based reminder check kore
# Tkinter messagebox use kore popup show kore

import threading    # background e run korar jonno
import time         # sleep ar time check er jonno
from datetime import datetime


class ReminderNotifier:
    """
    Background thread e medicine reminder check kore.
    Jodi current time kono reminder er sathe match kore,
    Tkinter messagebox popup show kore.

    Eita singleton pattern follow kore — ekbar start korle cholte thake.
    """

    def __init__(self):
        # thread reference rakha hocche — duplicate start theke bachao
        self._thread = None
        self._running = False
        self._user_id = None
        self._root = None       # Tkinter root window reference
        self._notified = set()  # ekdin e ek reminder bar bar show na korar jonno

    def start(self, user_id: int, root):
        """
        Background reminder checker thread start kore.
        user_id: logged-in user er ID
        root: Tkinter root window (after/messagebox er jonno)
        """
        if self._running:
            return  # already running thakle dobara start korbo na

        self._user_id = user_id
        self._root = root
        self._running = True

        # daemon=True mane main app close hole thread o automatically close hobe
        self._thread = threading.Thread(
            target=self._check_loop,
            daemon=True,
            name="ReminderThread"
        )
        self._thread.start()
        print(f"[Notification] Reminder checker started for user_id={user_id}")

    def stop(self):
        """
        Background thread band kore — logout er somoy call kora hobe.
        """
        self._running = False
        self._user_id = None
        self._notified.clear()
        print("[Notification] Reminder checker stopped.")

    def _check_loop(self):
        """
        Background e choltei thake — protiটা minute e reminder check kore.
        eita thread er main function.
        """
        last_minute = ""  # last checked minute rakha hocche

        while self._running:
            try:
                # current time "HH:MM" format e newa hocche
                now = datetime.now().strftime("%H:%M")

                # same minute e multiple check theke bachao
                if now != last_minute:
                    last_minute = now

                    # notified set clear kora hocche notun diner suru te
                    if now == "00:00":
                        self._notified.clear()

                    # due reminders check kora hocche
                    self._check_reminders(now)

            except Exception as e:
                print(f"[Notification ERROR] {e}")

            # 30 second por por check korbe
            time.sleep(30)

    def _check_reminders(self, current_time: str):
        """
        Current time diye database theke due reminders fetch kore.
        Jodi nowa thake, popup show kore.
        """
        if not self._user_id:
            return

        try:
            # import ekhane kora hocche circular import avoid er jonno
            from services.reminder_service import get_due_reminders

            due = get_due_reminders(self._user_id, current_time)

            for reminder in due:
                medicine = reminder["medicine_name"]
                key = f"{current_time}_{medicine}"

                # already notify kora hoyeche kina check — duplicate theke bachao
                if key not in self._notified:
                    self._notified.add(key)
                    # Tkinter root e after() use kore main thread e popup show kora hocche
                    # Tkinter thread-safe na, tai after() use korte hobe
                    if self._root:
                        self._root.after(
                            100,
                            lambda m=medicine: self._show_popup(m)
                        )

        except Exception as e:
            print(f"[Reminder Check ERROR] {e}")

    def _show_popup(self, medicine_name: str):
        """
        Tkinter messagebox diye medicine reminder popup show kore.
        Main thread e call kora hoy — thread safety maintain hocche.
        """
        try:
            from tkinter import messagebox
            messagebox.showinfo(
                "💊 Medicine Reminder",
                f"Ei medicine neyar somoy hoyeche:\n\n"
                f"🔔  {medicine_name}\n\n"
                f"Please take your medicine now!"
            )
        except Exception as e:
            print(f"[Popup ERROR] {e}")


# Global notifier instance — sob jaygay theke ekta instance use hobe
notifier = ReminderNotifier()