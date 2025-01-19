from flask import Flask, render_template, request, jsonify
import os
import sys

# Add the data directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

# from db_handler import validate_user, get_stores_from_db
import db_handler
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('index-main.html')



@app.route('/get_inventory', methods=['GET'])
def get_inventory():
    json_ary_of_objects = db_handler.get_inventory()
    print("get_inventory len = {}".format(len(json_ary_of_objects ) ) )
    return json_ary_of_objects


@app.route('/get_stores', methods=['GET'])
def get_stores():
    json_ary_of_objects = db_handler.get_stores()
    print("get_stores len = {}".format(len(json_ary_of_objects ) ) )
    return json_ary_of_objects

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print("login for {}".format(username) )
    result = {}
    if db_handler.validate_user(username, password):
        result["status"]="OK"
        result["message"] = "Login successful"
        result["statusType"] = "success"
    else:
        result["status"]="FAIL"
        result["message"] = "Invalid username or password!"
        result["statusType"] = "denied"
    return jsonify(result)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    print(f"Server is running at http://{host}:{port}")
    # Run the app using Waitress
    serve(app, host=host, port=port)
