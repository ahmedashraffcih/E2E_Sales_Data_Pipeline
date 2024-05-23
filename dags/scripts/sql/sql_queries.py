CREATE_USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS dim_users (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    city VARCHAR(255),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);
"""
CREATE_PRODUCT_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS dim_product_master (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(255),
    price NUMERIC(10, 2),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);

"""
CREATE_STORES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS dim_stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(255),
    lat float,
    lng float
);
"""

CREATE_FACT_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS fact_sales (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT,
    price FLOAT,
    order_date DATE,
    store_id INT NOT NULL,
    lat float,
    lng float,
    description VARCHAR(255),
    weather VARCHAR(255),
    temp FLOAT,
    pressure INT,
    humidity INT
);
"""
DROP_USERS_TABLE_SQL = """
    DROP TABLE IF EXISTS dim_users CASCADE;
"""
DROP_PRODUCT_TABLE_SQL = """
    DROP TABLE IF EXISTS dim_product_master CASCADE;
"""
DROP_STORES_TABLE_SQL = """
    DROP TABLE IF EXISTS dim_stores CASCADE;
"""
DROP_FACT_TABLE_SQL = """
    DROP TABLE IF EXISTS fact_sales CASCADE;
"""