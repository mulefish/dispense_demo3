import psycopg2
import os
import sys


sys.path.append(os.path.dirname(__file__))
from connection_string import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def get_inventory():
    query = "SELECT * FROM inventory;"
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        items = []
        for row in result:
            item = {
                "machineId": row[0],
                "instock": row[1],
                "price": str(row[2]),
                "merchantId_fk": row[7],
                "rowId": row[3],
                "spoolId": row[4],
                "storeId_fk": row[8],
                "uid": row[5],
                "img": row[6],
                "JSON": row[9]
            }
            items.append(item)

        return items

    except Exception as e:
        error_response = {"error": f"Error retrieving inventory: {str(e)}", "status": "error"}
        
        if "FLASK_APP" in os.environ:
            from flask import jsonify
            return jsonify(error_response), 500
        else:
            return json.dumps(error_response, indent=4)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_stores():
    query = "SELECT * FROM stores;"
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        stores_list = []
        for row in result:
            store = {
                "address": row[1],
                "lat": float(row[2]),
                "lon": float(row[3]),
                "merchantId_fk": row[8],
                "name": row[4],
                "phone": row[5],
                "storeId": row[0],
                "image": row[6]
            }
            stores_list.append(store)

        return stores_list

    except Exception as e:
        print(f"Error retrieving stores: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def validate_user(username, password):
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
        result = cursor.fetchone()
        return result is not None  # Return True if a match is found
    except Exception as e:
        print(f"Error validating user: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
