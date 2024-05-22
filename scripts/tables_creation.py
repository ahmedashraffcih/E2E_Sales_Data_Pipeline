from utils.db_utils import *
from sql.sql_queries import *

host ="localhost"
database = "sales_db"
user ="postgres"
password = "postgres"

def create_tables():
    queries = [
        (CREATE_USERS_TABLE_SQL, "users"),
        (CREATE_PRODUCT_TABLE_SQL, "products"),
        (CREATE_FACT_TABLE_SQL, "facts")
    ]
    conn = create_connection()
    if conn:
        for query, table_name in queries:
            execute_query(conn, query, table_name)
        close_connection(conn)

create_tables()