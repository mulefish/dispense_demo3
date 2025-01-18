from flask import Flask, render_template, request, jsonify
import os
import sys

# Add the data directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from db_handler import validate_user
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Parse JSON data from the request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(f"username: {username}, password: {password}")

    if validate_user(username, password):
        return jsonify({
            "status": "OK",
            "message": "Login successful!",
            "statusType": "success"
        })
    else:
        return jsonify({
            "status": "FAIL",
            "message": "Invalid username or password!",
            "statusType": "error"
        })

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    print(f"Server is running at http://{host}:{port}")
    # Run the app using Waitress
    serve(app, host=host, port=port)
