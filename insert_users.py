import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

users = [
    ("admin", "1234", "admin"),
    ("noor", "1234", "user")
]

for user in users:
    cursor.execute(
        "SELECT * FROM Users WHERE username=?",
        (user[0],)
    )

    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO Users (username,password,role) VALUES (?,?,?)",
            user
        )

conn.commit()
conn.close()

print("Users Added")