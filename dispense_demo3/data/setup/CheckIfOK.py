import psycopg2
from psycopg2 import sql
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connection_string import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

TABLES = [
    "merchants",
    "stores",
    "inventory",
    "featured_products"
]

COUNT_QUERY_TEMPLATE = "SELECT COUNT(*) FROM {}"

def check_table_population():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        all_populated = True

        for table in TABLES:
            # Prepare and execute the query for each table
            query = COUNT_QUERY_TEMPLATE.format(table)
            cursor.execute(query)
            count = cursor.fetchone()[0]
            print(f"Table '{table}' has {count} rows.")

            # Check if the table is empty
            if count == 0:
                all_populated = False

        # Final result
        if all_populated:
            print("OK! The tables are populated properly!")
        else:
            print("No! At least one table is missing data.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"An error occurred: {error}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    check_table_population()
