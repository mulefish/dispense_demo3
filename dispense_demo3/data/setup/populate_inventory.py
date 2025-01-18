import psycopg2
import json
import os
import sys
import dotenv

dotenv.load_dotenv()



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
        filename = "inventory.json"
        inventory_data = load_inventory_from_file(filename)

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

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
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_inventory()
