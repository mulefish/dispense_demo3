import psycopg2
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connection_string import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

USERS_DATA = [
    {
        "username": "kermitt",
        "email": "paul.montgomery@gmail.com",
        "phone": "5037842584",
        "isIdentifyOk": True,
        "isAeropayOk": True,
        "password": "a",
        "isLocationOk": True,
        "lat": 45.5152,
        "lon": -122.6784
    },
    {
        "username": "bluegreensomething",
        "email": "paul.montgomery@dispensego.com",
        "phone": "5037842584",
        "isIdentifyOk": True,
        "isAeropayOk": True,
        "password": "a",
        "isLocationOk": True,
        "lat": 45.3573,
        "lon": -122.6068
    }
]

INSERT_USER_QUERY = """
INSERT INTO users (username, email, phone, isIdentifyOk, isAeropayOk, password, isLocationOk, lat, lon)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def populate_users():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

        for user in USERS_DATA:
            cursor.execute(
                INSERT_USER_QUERY,
                (
                    user["username"],
                    user["email"],
                    user["phone"],
                    user["isIdentifyOk"],
                    user["isAeropayOk"],
                    user["password"],
                    user["isLocationOk"],
                    user["lat"],
                    user["lon"]
                )
            )
        conn.commit()
        print(f"Inserted {len(USERS_DATA)} users into the table.")

    except Exception as e:
        print("An error occurred while populating the Users table:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_users()
