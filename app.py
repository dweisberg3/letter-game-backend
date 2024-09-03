from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)
@app.route('/click', methods=['GET'])
def handle_click():
    print("got here!")
    print(request.headers)
    data = {
        'message' : 'hello from the backend!'
    }
    return jsonify(data)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username  = request.form.get('username')
    password  = request.form.get('password')
    results = authenticate_user(username,password)
    conn      = sqlite3.connect('letter-game.db')
    if(username == "admin" and password == "admin"):
         return render_template('users.html')

@app.route('/create_user', methods=['POST'])
def create_account():
    print(request.form)
    firstname =  request.form.get('firstname')
    lastname =  request.form.get('lastname')
    grade = request.form.get('grade')
    username = request.form.get('username')
    password    = request.form.get('password')
    does_exist = check_for_existance_of_user(username)
    if(does_exist):
        data = {
        'message' : 'Username already exists!',
        'new_user' : None
        }
        return jsonify(data),400
        
    conn = sqlite3.connect('letter-game.db')
    # print(f'username is : {username}  and password :  {password}')
    # Create a cursor object
    cursor = conn.cursor()

    # Create  table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, grade TEXT, username TEXT, password TEXT)''')

    # Insert data into the table
    cursor.execute("INSERT INTO users (firstname, lastname, grade, username, password) VALUES (? , ?, ?, ?, ?)", (firstname,lastname, grade, username, password))
    conn.commit()
    last_id = cursor.lastrowid

# Retrieve the exact value you just inserted
    cursor.execute('''
        SELECT * FROM users WHERE id = ?
    ''', (last_id,))
    inserted_value = cursor.fetchone()
    print(inserted_value)
    data = {
        'message' : 'Account Created!',
        'new_user' : inserted_value
    }
    return jsonify(data),200

@app.route('/get_users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('letter-game.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from users')
  
    # cursor.execute('SELECT * FROM users')
    # print(cursor.fetchall())
    al = cursor.fetchall()
    # print(al)
    return jsonify(al)

@app.route('/gameover', methods=['POST'])
def recordNewScore():
    conn = sqlite3.connect('letter-game.db')
    print(request.get_json())
    data = request.get_json()
    username = data['username']
    points = data['points']
    letter_level = data['letter_level']
    accumulative = data['accumulative']
    letter_section = data['letter_section']
    lost_single_letter_game = data['lost_single_letter_game']
    # print(f'username is : {username}  and password :  {password}')
    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS played_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username INTEGER NOT NULL,
    points INTEGER NOT NULL,
    letter_level INTEGER NOT NULL,
    accumulative BOOLEAN NOT NULL,
    letters_section INTEGER NOT NULL,
    one_letter_game_with_miss BOOLEAN NOT NULL,
    timestamp TEXT
   
)
''')
     # FOREIGN KEY (username) REFERENCES user (username)
    cursor.execute("INSERT INTO attempts (username, points, letter_level, accumulative, letters_section,one_letter_game_with_miss,timestamp) VALUES (? , ?, ?,?,?,?,?)", (username,points,letter_level,accumulative,letter_section,lost_single_letter_game,datetime.now()))
    cursor.execute("SELECT * from attempts")
    
    # Fetch the stored password
    result = cursor.fetchone()
    print(result)

# Commit the changes and close the connection
    conn.commit()
    conn.close()
    # print(request.json)
    data = {
        'message' : 'hello from the backend we got the score!'
    }
    return jsonify(data)


def authenticate_user(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('letter-game.db')
    cursor = conn.cursor()
    
    # Prepare the SQL query
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    
    # Fetch the stored password
    result = cursor.fetchone()
    
    conn.close()
    
    # If the username exists, result will not be None
    if result:
        stored_password = result[0]
        
        # Check if the provided password matches the stored password
        if password == stored_password:
            return (True,"Authentication successful!")
        else:
            return (False,"Invalid password.")
    else:
        return (False,"User not found.")

@app.route('/get_records', methods=['GET'])
def get_game_records():
    data = request.get_json()
    username = data['user']
    conn = sqlite3.connect('letter-game.db')
    cursor = conn.cursor()
    
    # Prepare the SQL query
    cursor.execute("SELECT * FROM attempts WHERE username=?", (username,))
    result = cursor.fetchone()
    return jsonify(result),200


def check_for_existance_of_user(username):
    conn = sqlite3.connect('letter-game.db')
    cursor = conn.cursor()
    
    # Prepare the SQL query
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    return result
app.route('new_user')
if __name__ == '__main__':
    app.run(debug=True)
