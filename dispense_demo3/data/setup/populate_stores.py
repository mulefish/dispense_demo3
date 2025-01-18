import psycopg2
import os
import sys
import dotenv

dotenv.load_dotenv()


STORES_DATA = [
    {
        "address": "232 Alameda, Oregon City, OR",
        "lat": 45.3573,
        "lon": -122.6068,
        "merchant_id": 1,
        "name": "Kitty Buds",
        "phone": "5032492584",
        "image": "big_kittybuds.jpg",
        "distance": "unknown",
    },
    {
        "address": "3000 NE Alberta, LA, CA",
        "lat": 34.0522,
        "lon": -118.2437,
        "merchant_id": 1,
        "name": "Bright Flower",
        "phone": "5032492999",
        "image": "big_brightflower.jpg",
        "distance": None,  # Default to NULL if unspecified
    },
    {
        "address": "223 SW 18th ave, NYC, NY",
        "lat": 40.7128,
        "lon": -74.0060,
        "merchant_id": 2,
        "name": "House of Johnson",
        "phone": "9714342669",
        "image": "big_house_of_johnson.jpg",
        "distance": None,  # Default to NULL if unspecified
    },
]

INSERT_STORE_QUERY = """
INSERT INTO Stores (address, lat, lon, merchant_id, name, phone, image, distance)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def populate_stores():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        for store in STORES_DATA:
            cursor.execute(
                INSERT_STORE_QUERY,
                (
                    store["address"],
                    store["lat"],
                    store["lon"],
                    store["merchant_id"],
                    store["name"],
                    store["phone"],
                    store["image"],
                    store["distance"],
                )
            )
        conn.commit()
        print(f"Inserted {len(STORES_DATA)} stores into the table.")

    except Exception as e:
        print("An error occurred while populating the Stores table:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_stores()
