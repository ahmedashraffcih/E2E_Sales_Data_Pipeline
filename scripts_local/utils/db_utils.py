import logging
from dotenv import load_dotenv
import psycopg2
import os
from psycopg2 import Error

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_db_credentials():
    load_dotenv()  # Load variables from .env file
    host = os.getenv("DATABASE_HOST")
    database = os.getenv("DATABASE_NAME")
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    return {"host": host, "database": database, "user": user, "password": password}


def create_connection():
    try:
        db_credentials = load_db_credentials()
        connection = psycopg2.connect(
            host=db_credentials["host"],
            database=db_credentials["database"],
            user=db_credentials["user"],
            password=db_credentials["password"],
        )
        logging.info("Connected to PostgreSQL database successfully")
        return connection
    except (Exception, Error) as error:
        logging.error("Error while connecting to PostgreSQL: %s", error)
        return None


def close_connection(connection):
    if connection:
        connection.close()
        logging.info("PostgreSQL connection is closed")


def execute_query(connection, query, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        logging.info("Query executed successfully for table %s", table_name)
        return True
    except (Exception, Error) as error:
        logging.error("Error while executing query for table %s: %s", table_name, error)
        return False
