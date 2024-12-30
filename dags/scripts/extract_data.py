import pandas as pd
import logging
from datetime import datetime
from scripts.utils.utils import format_users_data, extract_users_api, export_to_json


def extract_users_data_json():
    """
    Extract user data from an API and export it to JSON format.
    """
    logging.info("Extracting user data from API...")
    users_data = extract_users_api()
    if users_data:
        logging.info("Exporting user data to JSON...")
        export_to_json("./datalake/bronze/", users_data, "users.json")
        logging.info("User data exported to JSON successfully")
    else:
        logging.error("Failed to fetch user data from API")


def extract_users_data_csv():
    """
    Extract user data from an API and export it to CSV format.
    """
    logging.info("Extracting user data from API...")
    users_data = extract_users_api()
    if users_data:
        logging.info("Formatting user data...")
        formatted_data = [format_users_data(user) for user in users_data]
        users_df = pd.DataFrame(formatted_data)
        logging.info("Exporting user data to CSV...")
        users_df.to_csv("./datalake/bronze/users.csv", index=False)
        logging.info("User data exported to CSV successfully")
    else:
        logging.error("Failed to fetch user data from API")
