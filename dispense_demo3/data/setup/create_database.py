import psycopg2
from psycopg2 import sql
import sys
import os
import dotenv
dotenv.load_dotenv()

new_db_name = os.getenv("DB_NAME") # Currently it is 'jan21'

def get_connection_string_for_postgres():
    dbname = "postgres"  # Connect to the default database first! I forgot about this! And that took time. 
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    return f"dbname={dbname} user={user} password={password} host={host} port={port}"

def drop_database_if_exists(cursor, db_name):
    """Drop the database if it already exists."""
    drop_db_query = sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name))
    cursor.execute(drop_db_query)
    print(f"Database '{db_name}' dropped if it existed.")

try:
    # First, connect to the default "postgres" database to create a new one!  I forgot about this! And it took time. 
    connection_string = get_connection_string_for_postgres()
    conn = psycopg2.connect(connection_string)
    conn.autocommit = True # Actually I do not know what this means. 
    cursor = conn.cursor()

    drop_database_if_exists(cursor, new_db_name)

    create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name))
    cursor.execute(create_db_query)
    print(f"Database '{new_db_name}' created successfully.")
    
    connection_string = f"dbname={new_db_name} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
    conn = psycopg2.connect(connection_string)
    print(f"Successfully connected to the database '{new_db_name}'.")

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error: {error}")
finally:
    if conn:
        cursor.close()
        conn.close()
