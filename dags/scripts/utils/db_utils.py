from dotenv import load_dotenv
import psycopg2
import os
from psycopg2 import Error

def load_db_credentials():
    load_dotenv()  # Load variables from .env file
    host = os.getenv("DATABASE_HOST")
    database = os.getenv("DATABASE_NAME")
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    return {
        "host": host,
        "database": database,
        "user": user,
        "password": password
    }
def create_connection():
    try:
        db_credentials = load_db_credentials()
        connection = psycopg2.connect(
            host='127.0.0.1',
            database='sales_db',
            user='postgres',
            password='postgres'
        )
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

def close_connection(connection):
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")

def execute_query(connection,query,table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print(f"Query executed successfully for table {table_name}!")
        return True
    except (Exception, Error) as error:
        print(f"Error while executing query for table {table_name}:", error)
        return False