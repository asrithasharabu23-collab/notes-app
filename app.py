from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="smart_notes"
)

cursor = db.cursor()

# Register
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                   (data['username'], data['password']))
    db.commit()
    return jsonify({"message": "User registered"})

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                   (data['username'], data['password']))
    user = cursor.fetchone()

    if user:
        return jsonify({"status": "success", "user_id": user[0]})
    else:
        return jsonify({"status": "fail"})

# Add Note
@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.json
    cursor.execute("INSERT INTO notes (user_id, content) VALUES (%s, %s)",
                   (data['user_id'], data['content']))
    db.commit()
    return jsonify({"message": "Note added"})

# Get Notes
@app.route('/get_notes/<int:user_id>')
def get_notes(user_id):
    cursor.execute("SELECT id, content FROM notes WHERE user_id=%s", (user_id,))
    rows = cursor.fetchall()
    return jsonify(rows)

# Delete Note
@app.route('/delete/<int:id>')
def delete_note(id):
    cursor.execute("DELETE FROM notes WHERE id=%s", (id,))
    db.commit()
    return jsonify({"message": "Deleted"})

app.run(host="0.0.0.0", port=5000)