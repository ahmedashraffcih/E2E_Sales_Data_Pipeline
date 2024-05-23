from scripts_local.utils.db_utils import *
from scripts_local.sql.sql_queries import *

logging.basicConfig(filename='table_creations.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_tables():
    """
    Create tables in the database based on SQL queries defined in sql_queries.py.
    """
    logging.info('Creating tables...')
    queries = [
        (CREATE_USERS_TABLE_SQL, "users"),
        (CREATE_PRODUCT_TABLE_SQL, "products"),
        (CREATE_FACT_TABLE_SQL, "facts"),
        (CREATE_STORES_TABLE_SQL, "stores")
    ]
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        for query, table_name in queries:
            if execute_query(conn, query, table_name):
                logging.info(f'Table {table_name} created successfully')
            else:
                logging.error(f'Failed to create table {table_name}')
        close_connection(conn)
    else:
        logging.error('Failed to establish a connection to the database')


def drop_tables():
    """
    Drop tables from the database based on SQL queries defined in sql_queries.py.
    """
    logging.info('Dropping tables...')
    queries = [
        (DROP_USERS_TABLE_SQL, "users"),
        (DROP_PRODUCT_TABLE_SQL, "products"),
        (DROP_FACT_TABLE_SQL, "facts"),
        (DROP_STORES_TABLE_SQL, "stores")
    ]
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        for query, table_name in queries:
            if execute_query(conn, query, table_name):
                logging.info(f'Table {table_name} dropped successfully')
            else:
                logging.error(f'Failed to drop table {table_name}')
        close_connection(conn)
    else:
        logging.error('Failed to establish a connection to the database')

def load_data_to_postgres(table_name, data_frame):
    """
    Load data from a pandas DataFrame into a PostgreSQL table.
    """
    logging.info(f'Loading data into table {table_name}...')
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY;")
        # Insert new data
        for i, row in data_frame.iterrows():
            cols = ', '.join(list(row.index))
            vals = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({vals})"
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        logging.info(f"Data loaded successfully into table {table_name}")
        close_connection(conn)
    else:
        logging.error(f"Failed to connect to the database and load data into table {table_name}")