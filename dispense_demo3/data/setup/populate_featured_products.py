import psycopg2
import json
import os
import sys

# Add the parent directory to the path to import connection_string.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# SQL to insert data into the featured_products table
INSERT_FEATURED_PRODUCTS_QUERY = """
INSERT INTO featured_products (json, instock, merchant_id, price, row, spool, store_id, uid, img, description)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

# Import connection string information
from connection_string import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
def load_featured_products_from_file(filename):
    """
    Load featured products data from a JSON file.

    Args:
        filename (str): The name of the JSON file to read data from.

    Returns:
        list: A list of dictionaries containing featured products data.

    Raises:
        SystemExit: If the file is not found or the JSON data is invalid.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in the file '{filename}': {e}")
        sys.exit(1)

def populate_featured_products():
    try:
        # Load featured products data from the JSON file
        filename = "featured_products.json"
        featured_products_data = load_featured_products_from_file(filename)

        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Insert each featured product into the table
        for item in featured_products_data:
            cursor.execute(
                INSERT_FEATURED_PRODUCTS_QUERY,
                (
                    item["JSON"],  # Matches column `json` in the table
                    item["instock"],
                    item["merchant_id"],
                    item["price"],
                    item.get("row"),
                    item.get("spool"),
                    item.get("store_id"),
                    item.get("uid"),
                    item.get("img"),
                    item["description"]
                )
            )
        conn.commit()
        print(f"Inserted {len(featured_products_data)} featured products into the table.")

    except Exception as e:
        print("An error occurred while populating the featured_products table:", e)
    finally:
        # Clean up and close the connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_featured_products()
