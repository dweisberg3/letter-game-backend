import sqlite3
from datetime import datetime
conn = sqlite3.connect('letter-game.db')  # This will create a new database file named 'letter-game.db'
cursor = conn.cursor()


    # Create  table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, grade TEXT, username TEXT, password TEXT)''')

# Insert data into the table
cursor.execute("INSERT INTO users (firstname, lastname, grade, username, password) VALUES (? , ?, ?, ?, ?)", ('Asher','Cohen', '4', 'acohen', 'super_secret'))
conn.commit()
# Get today's date
# today = datetime.today()

# # Format the date as YYYY MM DD


# # Print the formatted date
# # print(formatted_date)
# # cursor.execute('SELECT * FROM users')
# # print(cursor.fetchall())

# username = "admin"
# password = "admin"
# score = 0
# formatted_date = today.strftime("%Y %m %d")
# # cursor = conn.cursor()

# #     # Create  table
# # cursor.execute('''CREATE TABLE IF NOT EXISTS users
# #                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

# # # Insert data into the table
# # cursor.execute("INSERT INTO users (username, password) VALUES (? , ?)", (username, password))
# # conn.commit()

# # Create  table
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, score INTEGER, last_login TEXT)''')

# # Insert data into the table
# cursor.execute("INSERT INTO users (name, username, password, score, last_login) VALUES (? , ?, ?, ?)", (username, password, score, formatted_date))
# conn.commit()

# cursor.execute('SELECT * FROM users')
print(cursor.fetchall())