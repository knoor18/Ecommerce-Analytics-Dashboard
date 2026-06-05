import sqlite3

def get_connection():
    return sqlite3.connect("database.db")

# Verify Login
def authenticate(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM Users WHERE username=? AND password=?",
        (username, password)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return True, result[0]

    return False, None