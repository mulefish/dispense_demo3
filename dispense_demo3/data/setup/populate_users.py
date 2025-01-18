import psycopg2
import os
import dotenv

dotenv.load_dotenv()

USERS_DATA = [
    {
        "username": "kermitt",
        "email": "paul.montgomery@gmail.com",
        "phone": "5037842584",
        "isIdentifyOk": True,
        "isAeropayOk": True,
        "password": "This is my password",
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
        "password": "This is my password",
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
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
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
