import sqlite3

# Establish a connection and a cursor
connection = sqlite3.connect("./data.db")
cursor = connection.cursor() # this is an object that can execute SQL queries

# Query data
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)

# Inserting new rows
new_rows = [('Cats', 'Cat City', '2088.10.10')]
cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
# Write changes on the database
connection.commit()
