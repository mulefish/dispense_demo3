import psycopg2
import os
import sys

# Add the parent directory to the path to import connection_string.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connection_string import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

DROP_FEATURED_PRODUCTS_TABLE_QUERY = "DROP TABLE IF EXISTS featured_products;"
DROP_INVENTORY_TABLE_QUERY = "DROP TABLE IF EXISTS inventory;"
DROP_STORES_TABLE_QUERY = "DROP TABLE IF EXISTS stores;"
DROP_MERCHANTS_TABLE_QUERY = "DROP TABLE IF EXISTS merchants;"

CREATE_MERCHANTS_TABLE_QUERY = """
CREATE TABLE merchants (
    merchant_id SERIAL PRIMARY KEY,
    bank_account_info TEXT,
    billing_address TEXT NOT NULL,
    logo_location TEXT,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(50)
);
"""

CREATE_STORES_TABLE_QUERY = """
CREATE TABLE stores (
    store_id SERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    image TEXT,
    distance TEXT DEFAULT 'unknown',
    merchant_id INTEGER NOT NULL,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE
);
"""

CREATE_INVENTORY_TABLE_QUERY = """
CREATE TABLE inventory (
    machine_id SERIAL PRIMARY KEY,
    json JSON NOT NULL,
    instock INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    row INTEGER,
    spool TEXT,
    uid TEXT,
    img TEXT,
    merchant_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE CASCADE
);
"""

CREATE_FEATURED_PRODUCTS_TABLE_QUERY = """
CREATE TABLE featured_products (
    product_id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    json JSON NOT NULL,
    instock INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    row INTEGER,
    spool TEXT,
    uid TEXT,
    img TEXT,
    merchant_id INTEGER NOT NULL,
    store_id INTEGER,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE CASCADE
);
"""

def create_tables():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

        cursor.execute(DROP_FEATURED_PRODUCTS_TABLE_QUERY)
        print("Table 'featured_products' dropped successfully (if it existed).")
        cursor.execute(DROP_INVENTORY_TABLE_QUERY)
        print("Table 'inventory' dropped successfully (if it existed).")
        cursor.execute(DROP_STORES_TABLE_QUERY)
        print("Table 'stores' dropped successfully (if it existed).")
        cursor.execute(DROP_MERCHANTS_TABLE_QUERY)
        print("Table 'merchants' dropped successfully (if it existed).")

        cursor.execute(CREATE_MERCHANTS_TABLE_QUERY)
        print("Table 'merchants' created successfully.")

        cursor.execute(CREATE_STORES_TABLE_QUERY)
        print("Table 'stores' created successfully.")

        cursor.execute(CREATE_INVENTORY_TABLE_QUERY)
        print("Table 'inventory' created successfully.")

        cursor.execute(CREATE_FEATURED_PRODUCTS_TABLE_QUERY)
        print("Table 'featured_products' created successfully.")

        conn.commit() # Doesn't autocommit do this?

    except Exception as e:
        print("An error occurred while creating the tables:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_tables()
