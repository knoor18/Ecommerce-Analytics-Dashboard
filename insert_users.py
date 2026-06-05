import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

users = [
    ("admin", "1234", "admin"),
    ("noor", "1234", "user")
]

cursor.executemany(
    "INSERT INTO Users (username,password,role) VALUES (?,?,?)",
    users
)

conn.commit()
conn.close()

print("Users Added")