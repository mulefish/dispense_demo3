import psycopg2
import json
import os
import sys

# Add the parent directory to the path to import connection_string.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import connection string information
from connection_string import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

# SQL to insert data into the Inventory table
INSERT_INVENTORY_QUERY = """
INSERT INTO inventory (json, instock, merchant_id, price, row, spool, store_id, uid, img)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def load_inventory_from_file(filename):
    """Load inventory data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in the file '{filename}': {e}")
        sys.exit(1)

def populate_inventory():
    try:
        # Load inventory data from the JSON file
        filename = "inventory.json"
        inventory_data = load_inventory_from_file(filename)

        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Insert each inventory item into the table
        for item in inventory_data:
            cursor.execute(
                INSERT_INVENTORY_QUERY,
                (
                    item["JSON"],
                    item["instock"],
                    item["merchant_id"],
                    item["price"],
                    item["row"],
                    item["spool"],
                    item["store_id"],
                    item["uid"],
                    item["img"],
                )
            )
        conn.commit()
        print(f"Inserted {len(inventory_data)} inventory items into the table.")

    except Exception as e:
        print("An error occurred while populating the Inventory table:", e)
    finally:
        # Clean up and close the connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_inventory()