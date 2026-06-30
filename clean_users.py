import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM Users
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM Users
    GROUP BY username
)
""")

conn.commit()

cursor.execute("SELECT username, role FROM Users")
print(cursor.fetchall())

conn.close()

print("Duplicate users removed successfully")