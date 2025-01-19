import psycopg2
import json
import os
import sys

# Add the parent directory to the path to import connection_string.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connection_string import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT



INSERT_INVENTORY_QUERY = """
INSERT INTO inventory (machine_id, instock, merchant_id, price, row, spool, store_id, uid, img, json)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        filename = "inventory.json"
        inventory_data = load_inventory_from_file(filename)

        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

        for item in inventory_data:
            cursor.execute(
                INSERT_INVENTORY_QUERY,
                (
                    item["machine_id"],
                    item["instock"],
                    item["merchant_id"],
                    item["price"],
                    item["row"],
                    item["spool"],
                    item["store_id"],
                    item["uid"],
                    item["img"],                    
                    item["JSON"],

                )
            )
        conn.commit()
        print(f"Inserted {len(inventory_data)} inventory items into the table.")

    except Exception as e:
        print("An error occurred while populating the Inventory table:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_inventory()
