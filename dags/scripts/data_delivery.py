import pandas as pd
from datetime import datetime
from scripts.tables_creation import *
import logging

logging.basicConfig(
    filename="data_delivery.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load_users_dim(host, db_name, user, password):
    try:
        logging.info("Loading users dimension...")
        users_df = pd.read_csv("./datalake/silver/users.csv")
        users_df = users_df[
            [
                "user_id",
                "name",
                "email",
                "phone",
                "city",
                "start_date",
                "end_date",
                "is_current",
            ]
        ]
        users_df.to_csv("./datalake/gold/users_dim.csv", index=False)
        load_data_to_postgres("dim_users", users_df, host, db_name, user, password)
        logging.info("Users dimension loaded successfully")
    except Exception as e:
        logging.error(f"Error loading users dimension: {str(e)}")


def load_sales_dim(host, db_name, user, password):
    try:
        logging.info("Loading sales dimension...")
        sales_df = pd.read_csv("./datalake/silver/sales_data.csv")
        sales_df = sales_df[
            [
                "order_id",
                "customer_id",
                "product_id",
                "quantity",
                "price",
                "order_date",
                "store_id",
                "weather",
                "description",
                "temp",
                "pressure",
                "humidity",
            ]
        ]
        sales_df.to_csv("./datalake/gold/sales_fact.csv", index=False)
        load_data_to_postgres("fact_sales", sales_df, host, db_name, user, password)
        logging.info("Sales dimension loaded successfully")
    except Exception as e:
        logging.error(f"Error loading sales dimension: {str(e)}")


def load_stores_dim(host, db_name, user, password):
    try:
        logging.info("Loading stores dimension...")
        stores_df = pd.read_csv("./datalake/silver/sales_data.csv")
        stores_df.drop_duplicates(subset=["store_id"], inplace=True)
        stores_df = stores_df[["store_id", "lat", "lng", "country"]]
        stores_df["country"].fillna("N/A", inplace=True)
        stores_df = stores_df.sort_values(by="store_id").reset_index(drop=True)
        stores_df["store_name"] = "store_" + stores_df["store_id"].astype(str)
        stores_df.to_csv("./datalake/gold/dim_stores.csv", index=False)
        load_data_to_postgres("dim_stores", stores_df, host, db_name, user, password)
        logging.info("Stores dimension loaded successfully")
    except Exception as e:
        logging.error(f"Error loading stores dimension: {str(e)}")


def load_product_data(host, db_name, user, password):
    try:
        logging.info("Loading product data...")
        sales_df = pd.read_csv("./datalake/silver/sales_data.csv")
        sales_df["order_date"] = pd.to_datetime(sales_df["order_date"])
        product_df = sales_df.groupby("product_id").apply(
            lambda x: x.loc[x["order_date"].idxmax()]
        )
        product_df["price"] = round(product_df["price"] / product_df["quantity"], 2)
        product_df["product_name"] = "product_" + product_df["product_id"].astype(str)
        product_df = product_df[["product_id", "product_name", "price"]]
        product_df["start_date"] = pd.to_datetime("today").date()
        product_df["end_date"] = "9999-12-31"
        product_df["is_current"] = True
        ##### Applying SCD Type 2 Logic
        try:
            # Load existing product data
            existing_prod_df = pd.read_csv("./datalake/gold/product_master.csv")
            existing_prod_df["start_date"] = pd.to_datetime(
                existing_prod_df["start_date"]
            )
            existing_prod_df["end_date"] = existing_prod_df["end_date"]
        except FileNotFoundError:
            # If file does not exist, initialize it
            existing_prod_df = pd.DataFrame(columns=product_df.columns)
        # list to hold the updated records
        updated_prod = []
        for idx, new_row in product_df.iterrows():
            existing_row = existing_prod_df[
                existing_prod_df["product_id"] == new_row["product_id"]
            ]

            if not existing_row.empty:
                existing_row = existing_row.iloc[0]
                # Check for changes
                if (new_row["product_name"] != existing_row["product_name"]) or (
                    new_row["price"] != existing_row["price"]
                ):

                    # Update existing record
                    existing_prod_df.loc[
                        existing_prod_df["product_id"] == new_row["product_id"],
                        "end_date",
                    ] = datetime.now().date()
                    existing_prod_df.loc[
                        existing_prod_df["product_id"] == new_row["product_id"],
                        "is_current",
                    ] = False
                    # Add the new record
                    updated_prod.append(new_row)
            else:
                # Add if it doesn't exist
                updated_prod.append(new_row)
        updated_prod_df = pd.DataFrame(updated_prod)
        final_users_df = pd.concat(
            [existing_prod_df, updated_prod_df], ignore_index=True
        )
        final_users_df.to_csv("./datalake/gold/product_master.csv", index=False)
        load_data_to_postgres(
            "dim_product_master", product_df, host, db_name, user, password
        )
        logging.info("Product data loaded successfully")
    except Exception as e:
        logging.error(f"Error loading product data: {str(e)}")
