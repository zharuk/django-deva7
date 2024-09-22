import sqlite3

conn = sqlite3.connect(r'C:\Users\user\AppData\Roaming\ViberPC\380959291465\viber.db')  # Используйте 'r' для raw string, чтобы избежать проблем с экранированием
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)

conn.close()