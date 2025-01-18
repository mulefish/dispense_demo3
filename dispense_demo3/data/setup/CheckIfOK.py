import os
import sys

import dotenv
import psycopg2

dotenv.load_dotenv()


def print_fail(message):
    red_color = "\033[31m"
    reset_color = "\033[0m"    
    sys.stdout.write(f"{red_color}{message}{reset_color}\n")

def print_success(message):
    light_green_color = "\033[92m"
    reset_color = "\033[0m"
    sys.stdout.write(f"{light_green_color}{message}{reset_color}\n")

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
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        all_populated = True

        for table in TABLES:
            query = COUNT_QUERY_TEMPLATE.format(table)
            cursor.execute(query)
            count = cursor.fetchone()[0]
            print(f"Table '{table}' has {count} rows.")

            # FAILBOT! Everything ought to have at least 2!
            # NOTE TO SELF! IF this is a fail, mostly likely the " email VARCHAR(255) NOT NULL UNIQUE," is the issue!
            if count < 2:
                all_populated = False

        if all_populated:
            print_success("OK! The tables are populated properly!")
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
