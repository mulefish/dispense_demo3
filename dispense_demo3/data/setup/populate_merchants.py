import psycopg2
from psycopg2 import sql
import os
import sys

# Add the parent directory to the path to import connection_string.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import connection string information
from connection_string import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

# Data to insert into the Merchants table
MERCHANTS_DATA = [
    {
        "bank_account_info": "TBD",
        "billing_address": "308 E. Florida, Urbana Il, 61801",
        "logo_location": "TBD",
        "name": "kermitt",
        "password": "Happy$100",
        "phone": "217.367.3196",
    },
    {
        "bank_account_info": "TBD",
        "billing_address": "1017 Lynn St., Urbana Il, 61801",
        "logo_location": "TBD",
        "name": "admin",
        "password": "topsecret",
        "phone": "217.367.4449",
    },
]

# SQL to insert data into the Merchants table
INSERT_MERCHANT_QUERY = """
INSERT INTO Merchants (bank_account_info, billing_address, logo_location, name, password, phone)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def populate_merchants():
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Insert each merchant into the table
        for merchant in MERCHANTS_DATA:
            cursor.execute(
                INSERT_MERCHANT_QUERY,
                (
                    merchant["bank_account_info"],
                    merchant["billing_address"],
                    merchant["logo_location"],
                    merchant["name"],
                    merchant["password"],
                    merchant["phone"],
                )
            )
        conn.commit()
        print(f"Inserted {len(MERCHANTS_DATA)} merchants into the table.")

    except Exception as e:
        print("An error occurred while populating the Merchants table:", e)
    finally:
        # Clean up and close the connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_merchants()
