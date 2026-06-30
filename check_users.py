import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT rowid, username, role FROM Users")

for row in cursor.fetchall():
    print(row)

conn.close()