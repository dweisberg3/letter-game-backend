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
    conn = sqlite3.connect('letter-game.db')
    print(f'username is : {username}  and password :  {password}')
    # Create a cursor object
    cursor = conn.cursor()

    # Create  table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, grade TEXT, username TEXT, password TEXT)''')

    # Insert data into the table
    cursor.execute("INSERT INTO users (firstname, lastname, grade, username, password) VALUES (? , ?, ?, ?, ?)", (firstname,lastname, grade, username, password))
    conn.commit()
    data = {
        'message' : 'Account Created!'
    }
    return jsonify(data)

@app.route('/get_users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('letter-game.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from users')
  
    # cursor.execute('SELECT * FROM users')
    # print(cursor.fetchall())
    al = cursor.fetchall()
    print(al)
    return jsonify(al)

@app.route('/gameover', methods=['POST'])
def recordNewScore():
    print(request.json)
    data = {
        'message' : 'hello from the backend we got the score!'
    }
    return jsonify(data)


app.route('new_user')
if __name__ == '__main__':
    app.run(debug=True)
