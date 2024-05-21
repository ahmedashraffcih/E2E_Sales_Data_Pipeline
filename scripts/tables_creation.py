import psycopg2
from psycopg2 import Error
from sql_queries import *

host ="localhost"
database = "sales_db"
user ="postgres"
password = "postgres"

def create_tables():
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute(CREATE_USERS_TABLE_SQL)
        cursor.execute(CREATE_PRODUCT_TABLE_SQL)
        cursor.execute(CREATE_FACT_TABLE_SQL)
        connection.commit()
        print("Tables created successfully!")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

create_tables()