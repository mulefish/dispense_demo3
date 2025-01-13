import psycopg2
from psycopg2 import sql
import sys
import os

# Add the directory above the current one to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the constants from connection_string.py
from connection_string import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Name of the new database
new_db_name = 'jan21'

# Connection string to connect to the default PostgreSQL database
def get_connection_string_for_postgres():
    # Use the default 'postgres' database to manage other databases
    dbname = "postgres"  # Connect to the default database first
    user = DB_USER
    password = DB_PASSWORD
    host = DB_HOST
    port = DB_PORT

    return f"dbname={dbname} user={user} password={password} host={host} port={port}"

def drop_database_if_exists(cursor, db_name):
    """Drop the database if it already exists."""
    drop_db_query = sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name))
    cursor.execute(drop_db_query)
    print(f"Database '{db_name}' dropped if it existed.")

# Main script to create the database and then reconnect to it
try:
    # First, connect to the default "postgres" database to create a new one
    connection_string = get_connection_string_for_postgres()
    conn = psycopg2.connect(connection_string)
    conn.autocommit = True  # Enable autocommit mode for database creation
    cursor = conn.cursor()

    # Drop the database if it already exists
    drop_database_if_exists(cursor, new_db_name)

    # SQL to create the new database
    create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name))
    cursor.execute(create_db_query)
    print(f"Database '{new_db_name}' created successfully.")
    
    # Now, reconnect to the newly created database 'jan21'
    connection_string = f"dbname={new_db_name} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
    conn = psycopg2.connect(connection_string)
    print(f"Successfully connected to the database '{new_db_name}'.")

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error: {error}")
finally:
    if conn:
        cursor.close()
        conn.close()
