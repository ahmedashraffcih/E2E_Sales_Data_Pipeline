from dotenv import load_dotenv
import psycopg2
import os
import logging
from psycopg2 import Error

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_connection(host, db_name, user, password):
    try:
        connection = psycopg2.connect(
            host=host, database=db_name, user=user, password=password
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
