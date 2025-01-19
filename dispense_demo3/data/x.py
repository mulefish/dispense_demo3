import psycopg2
import os
import sys

# Add the directory containing connection_string.py to the path
sys.path.append(os.path.dirname(__file__))
from connection_string import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def validate_user(username, password):
    print("user {} and password {}".format(username, password))
    """
    Validates the username and password against the 'users' table in the database.
    Returns True if a match is found, otherwise False.
    """
    query = "SELECT 1 FROM users WHERE username = %s AND password = %s;"
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute(query, (username, password))
        result = cursor.fetchone()  # Fetch one row
        return result is not None  # Return True if a match is found
    except Exception as e:
        print(f"Error validating user: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
