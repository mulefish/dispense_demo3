import psycopg2
import json
import os
import sys
import dotenv

dotenv.load_dotenv()


INSERT_FEATURED_PRODUCTS_QUERY = """
INSERT INTO featured_products (json, instock, merchant_id, price, row, spool, store_id, uid, img, description)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def load_featured_products_from_file(filename):
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
        filename = "featured_products.json"
        featured_products_data = load_featured_products_from_file(filename)

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )
        cursor = conn.cursor()

        for item in featured_products_data:
            cursor.execute(
                INSERT_FEATURED_PRODUCTS_QUERY,
                (
                    item["JSON"],
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
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_featured_products()
