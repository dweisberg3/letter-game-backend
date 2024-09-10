from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    username  = request.form.get('username')
    password  = request.form.get('password')
    if(username == "binyan" and password == "yisroel"):
         response = {}
         response['authenticated'] = True
         response['admin'] = True
         return jsonify(response)
    results = authenticate_user(username,password)
    return jsonify(results)

@app.route('/create_user', methods=['POST'])
def create_account():
    print(request.form)
    firstname =  request.form.get('firstname')
    lastname =  request.form.get('lastname')
    grade = request.form.get('grade')
    username = request.form.get('username')
    password    = request.form.get('password')
    conn = sqlite3.connect('letter-game.db')
    cursor = conn.cursor()
    # Create  table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, grade TEXT, username TEXT, password TEXT)''')

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    does_exist = cursor.fetchone()
    # does_exist = check_for_existance_of_user(username)
    if(does_exist):
        data = {
        'message' : 'Username already exists!',
        'new_user' : None
        }
        return jsonify(data),409
        
    conn = sqlite3.connect('letter-game.db')
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, grade TEXT, username TEXT, password TEXT)''')
    cursor.execute('SELECT * from users')
  
    # cursor.execute('SELECT * FROM users')
    # print(cursor.fetchall())
    users = []
    result = cursor.fetchall()
    for el in result:
        user = {
            "id": el[0],
            "firstname": el[1],
            "lastname":el[2],
            "grade":el[3],
            "username":el[4],
            "password":el[5]

        }
        users.append(user)
    # print(al)
    return jsonify(users)

@app.route('/gameover', methods=['POST'])
def recordNewScore():
    conn = sqlite3.connect('letter-game.db')
    print(request.get_json())
    data = request.get_json()
    username = data['username']
    points = data['points']
    letter_level = data['letter_level']
    is_cumulative = data['is_cumulative']
    selected_sections_index = data['selected_sections_index']
    lost_single_letter_game = data['lost_single_letter_game']

    cursor = conn.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS played_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    points INTEGER NOT NULL,
    letter_level INTEGER NOT NULL,
    selected_sections_index INTEGER NOT NULL,
    is_cumulative BOOLEAN NOT NULL,
    one_letter_game_with_miss BOOLEAN NOT NULL,
    timestamp TEXT
   
)
''')
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %I:%M:%S %p").lower()
     # FOREIGN KEY (username) REFERENCES user (username)
    cursor.execute("INSERT INTO played_games (username, points, letter_level, selected_sections_index,is_cumulative,one_letter_game_with_miss,timestamp) VALUES (? , ?, ?,?,?,?,?)", (username,points,letter_level,selected_sections_index ,is_cumulative,lost_single_letter_game,formatted_time))
    # cursor.execute("SELECT * from attempts")
    
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

@app.route('/scoreboard', methods=['GET'])
def get_scoreboard():
     conn = sqlite3.connect('letter-game.db')
     cursor = conn.cursor()
     cursor.execute('''
        CREATE TABLE IF NOT EXISTS played_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        points INTEGER NOT NULL,
        letter_level INTEGER NOT NULL,
        is_cumulative BOOLEAN NOT NULL,
        one_letter_game_with_miss BOOLEAN NOT NULL,
        timestamp TEXT
        )
                    ''')
     query = '''
SELECT users.username, users.firstname, users.lastname, SUM(played_games.points) AS total_points
FROM played_games
JOIN users ON played_games.username = users.username
GROUP BY users.username, users.firstname, users.lastname;
'''

     cursor.execute(query)
     results = cursor.fetchall()
     print(results)
     users_points = []
     for row in results:
        users_points.append({
            'username': row[0],
            'firstname': row[1],
            'lastname': row[2],
            'total_points': row[3]
        })

     conn.close()
     return jsonify(users_points)
       
def authenticate_user(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('letter-game.db')
    cursor = conn.cursor()
    
    # Prepare the SQL query
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    
    # Fetch the stored password
    result = cursor.fetchone()
    
    conn.close()
    response = {}
    # If the username exists, result will not be None
    if result:
        stored_password = result[0]
        
        # Check if the provided password matches the stored password
        if password == stored_password:
            response['authenticated'] = True
            response['admin'] = False
            return response
            # return (True,"Authentication successful!")
        else:
            response['authenticated'] = False
            response['admin'] = False
            return response
    else:
        response['authenticated'] = False
        response['admin']  = False
        return response

@app.route('/get_records', methods=['GET'])
def get_game_records():
    username = request.args['username']
    conn = sqlite3.connect('letter-game.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS played_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        points INTEGER NOT NULL,
        letter_level INTEGER NOT NULL,
        is_cumulative BOOLEAN NOT NULL,
        one_letter_game_with_miss BOOLEAN NOT NULL,
        timestamp TEXT
        )
                    ''')
    # Prepare the SQL query
    cursor.execute("SELECT * FROM  played_games WHERE username=?", (username,))
    records = []
    result = cursor.fetchall()
    print(result)
    for el in result:
        record = {
            "id": el[0],
            "username": el[1],
            "points":el[2],
            "letter_level":el[3],
            "selected_sections_index":el[4],
            "is_cumulative":bool(el[5]),
            "one_letter_game_with_miss":bool(el[6]),
            "timestamp":el[7]

        }
        records.append(record)

    return jsonify(records),200


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
