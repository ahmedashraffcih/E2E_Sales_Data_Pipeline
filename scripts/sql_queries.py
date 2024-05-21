CREATE_USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS dim_users (
    id SERIAL PRIMARY KEY,
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
    product_name VARCHAR(255),
    price NUMERIC(10, 2),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);

"""
CREATE_FACT_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS fact_sales (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    price FLOAT,
    order_date DATE,
    weather VARCHAR(255),
    temp FLOAT,
    humidity INT
);
"""
