from scripts_local.utils.db_utils import *
from scripts_local.sql.sql_queries import *

host ="localhost"
database = "sales_db"
user ="postgres"
password = "postgres"

def create_tables():
    queries = [
        (CREATE_USERS_TABLE_SQL, "users"),
        (CREATE_PRODUCT_TABLE_SQL, "products"),
        (CREATE_FACT_TABLE_SQL, "facts"),
        (CREATE_STORES_TABLE_SQL, "stores")
    ]
    conn = create_connection()
    if conn:
        for query, table_name in queries:
            execute_query(conn, query, table_name)
        close_connection(conn)


def drop_tables():
    queries = [
        (DROP_USERS_TABLE_SQL, "users"),
        (DROP_PRODUCT_TABLE_SQL, "products"),
        (DROP_FACT_TABLE_SQL, "facts"),
        (DROP_STORES_TABLE_SQL, "stores")
    ]
    conn = create_connection()
    if conn:
        for query, table_name in queries:
            execute_query(conn, query, table_name)
        close_connection(conn)

def load_data_to_postgres(table_name, data_frame):
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
        print(f"Data loaded successfully into table {table_name}!")
        close_connection(conn)
    else:
        print(f"Failed to connect to the database and load data into table {table_name}")