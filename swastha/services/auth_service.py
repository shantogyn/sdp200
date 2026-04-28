
# eita user authentication er jonno — signup ar login logic ekhane ache
# UI file theke ei service call kora hobe, directly DB touch korbe na UI

import hashlib  # password hashing er jonno SHA256 use korbo
from config.db_config import get_connection, close_connection


def hash_password(password: str) -> str:
    """
    Password ke SHA256 hash e convert kore.
    Plain text password database e kabhi save korbo na — security er jonno.
    """
    # encode kore sha256 hash generate kora hocche
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(username: str, password: str, email: str = "") -> dict:
    """
    Notun user register kore database e.
    Success hole {'success': True, 'message': '...'} return kore.
    Failure hole {'success': False, 'message': '...'} return kore.
    """
    # input validation — username ar password khali thakle reject
    if not username.strip() or not password.strip():
        return {"success": False, "message": "Username ar password dite hobe!"}

    if len(password) < 6:
        return {"success": False, "message": "Password obosshoi 6 character er beshi hote hobe!"}

    conn = get_connection()
    if not conn:
        return {"success": False, "message": "Database connection fail hoyeche!"}

    try:
        cursor = conn.cursor()

        # username already ache kina check kora hocche
        cursor.execute("SELECT id FROM users WHERE username = %s", (username.strip(),))
        existing = cursor.fetchone()

        if existing:
            return {"success": False, "message": "Ei username already newa ache! Onno naam try korun."}

        # password hash kore save kora hocche
        hashed_pw = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username.strip(), hashed_pw, email.strip())
        )
        conn.commit()

        return {"success": True, "message": "Account successfully create hoyeche! Login korun."}

    except Exception as e:
        return {"success": False, "message": f"Registration error: {e}"}

    finally:
        # sob sesh hole connection close kora hocche — memory leak theke bachao
        close_connection(conn)


def login_user(username: str, password: str) -> dict:
    """
    User login verify kore.
    Correct credentials dile user info return kore.
    Wrong hole error message return kore.
    """
    if not username.strip() or not password.strip():
        return {"success": False, "message": "Username ar password dite hobe!"}

    conn = get_connection()
    if not conn:
        return {"success": False, "message": "Database connection fail hoyeche!"}

    try:
        cursor = conn.cursor(dictionary=True)  # dict format e result pabo

        # hashed password diye match kora hocche
        hashed_pw = hash_password(password)

        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = %s AND password = %s",
            (username.strip(), hashed_pw)
        )
        user = cursor.fetchone()

        if user:
            # login successful — user info return koro
            return {
                "success": True,
                "message": "Login successful!",
                "user": user  # {'id': ..., 'username': ..., 'email': ...}
            }
        else:
            return {"success": False, "message": "Username ba password ভুল আছে!"}

    except Exception as e:
        return {"success": False, "message": f"Login error: {e}"}

    finally:
        close_connection(conn)