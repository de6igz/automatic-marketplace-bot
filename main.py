import sqlite3

sqlite_connection = sqlite3.connect('database.db')
cursor = sqlite_connection.cursor()
sqlite_connection.commit()
