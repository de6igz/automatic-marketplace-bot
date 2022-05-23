import sqlite3

sqlite_connection = sqlite3.connect('database.db')
cursor = sqlite_connection.cursor()
sqlite_connection.commit()
sql_create_table = "CREATE TABLE sqlitedb_developers (id INTEGER PRIMARY KEY,name TEXT NOT NULL,email text NOT NULL UNIQUE,joining_date datetime,salary REAL NOT NULL)"