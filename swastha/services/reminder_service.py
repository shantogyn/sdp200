# services/reminder_service.py
# eita medicine reminder er backend logic
# reminder add, delete, fetch kora hoy ekhane
# background thread time check kore notification trigger kore

from config.db_config import get_connection, close_connection


def add_reminder(user_id: int, medicine_name: str, reminder_time: str) -> dict:
    """
    Notun medicine reminder database e add kore.
    reminder_time format: "HH:MM" (24-hour)
    """
    if not medicine_name.strip() or not reminder_time.strip():
        return {"success": False, "message": "Medicine naam ar time dite hobe!"}

    conn = get_connection()
    if not conn:
        return {"success": False, "message": "Database connection fail!"}

    try:
        cursor = conn.cursor()

        # reminder insert kora hocche
        cursor.execute(
            "INSERT INTO reminders (user_id, medicine_name, reminder_time) VALUES (%s, %s, %s)",
            (user_id, medicine_name.strip(), reminder_time.strip())
        )
        conn.commit()

        return {"success": True, "message": f"'{medicine_name}' reminder add hoyeche!"}

    except Exception as e:
        return {"success": False, "message": f"Reminder add korte error: {e}"}

    finally:
        close_connection(conn)


def get_reminders(user_id: int) -> list:
    """
    Ekটা user er sob active reminders fetch kore.
    Reminder list screen e show kora hobe.
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)

        # sudhu active reminders (is_active=1) fetch kora hocche
        cursor.execute(
            """SELECT id, medicine_name,
                      TIME_FORMAT(reminder_time, '%h:%i %p') AS reminder_time_fmt,
                      reminder_time AS raw_time
               FROM reminders
               WHERE user_id = %s AND is_active = 1
               ORDER BY reminder_time ASC""",
            (user_id,)
        )
        return cursor.fetchall()

    except Exception as e:
        print(f"[Reminder Service ERROR] {e}")
        return []

    finally:
        close_connection(conn)


def delete_reminder(reminder_id: int) -> dict:
    """
    Ekটা reminder delete kore (soft delete — is_active = 0 set kore).
    Hard delete na kore soft delete use kora hocche audit trail er jonno.
    """
    conn = get_connection()
    if not conn:
        return {"success": False, "message": "Database connection fail!"}

    try:
        cursor = conn.cursor()

        # soft delete — actual row remove na kore flag change kora hocche
        cursor.execute(
            "UPDATE reminders SET is_active = 0 WHERE id = %s",
            (reminder_id,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            return {"success": True, "message": "Reminder delete hoyeche."}
        else:
            return {"success": False, "message": "Reminder khuja pachhi na!"}

    except Exception as e:
        return {"success": False, "message": f"Delete error: {e}"}

    finally:
        close_connection(conn)


def get_due_reminders(user_id: int, current_time_str: str) -> list:
    """
    Background thread theke call kora hobe — current time er sathe
    sob reminder compare kore je gulo match kore segulo return kore.
    current_time_str format: "HH:MM"
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)

        # current time er sathe exact match check kora hocche
        cursor.execute(
            """SELECT medicine_name FROM reminders
               WHERE user_id = %s
               AND is_active = 1
               AND TIME_FORMAT(reminder_time, '%H:%i') = %s""",
            (user_id, current_time_str)
        )
        return cursor.fetchall()

    except Exception as e:
        print(f"[Reminder Check ERROR] {e}")
        return []

    finally:
        close_connection(conn)