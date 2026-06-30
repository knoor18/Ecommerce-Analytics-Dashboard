import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM Users
WHERE rowid IN (51, 52)
""")

conn.commit()
conn.close()

print("Duplicates removed successfully")