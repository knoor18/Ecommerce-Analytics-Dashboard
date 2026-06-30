import sqlite3

def authenticate(username, password):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM Users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return True, user[0]   # success, role
    else:
        return False, None

def create_user(username, password, role):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Users WHERE username=?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False

    cursor.execute(
        "INSERT INTO Users(username,password,role) VALUES (?,?,?)",
        (username, password, role)
    )

    conn.commit()
    conn.close()

    return True