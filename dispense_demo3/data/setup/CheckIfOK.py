import psycopg2
from psycopg2 import sql
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connection_string import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def print_fail(message):
    red_color = "\033[31m"
    reset_color = "\033[0m"    
    sys.stdout.write(f"{red_color}{message}{reset_color}\n")

TABLES = [
    "merchants",
    "stores",
    "inventory",
    "featured_products",
    "users"
]

COUNT_QUERY_TEMPLATE = "SELECT COUNT(*) FROM {}"

def check_table_population():
    try:
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
            query = COUNT_QUERY_TEMPLATE.format(table)
            cursor.execute(query)
            count = cursor.fetchone()[0]
            print(f"Table '{table}' has {count} rows.")

            # FAILBOT! Everything ought to have at least 2!
            if count < 2:
                all_populated = False

        if all_populated:
            print("OK! The tables are populated properly!")
        else:
            print_fail("No! At least one table is missing data.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"An error occurred: {error}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    check_table_population()
