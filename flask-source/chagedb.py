import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('test.db')
cursor = connection.cursor()

# Export data to SQL file
with open('grocery.sql', 'w') as sql_file:
    for line in connection.iterdump():
        sql_file.write('%s\n' % line)

# Close the connection
connection.close()
