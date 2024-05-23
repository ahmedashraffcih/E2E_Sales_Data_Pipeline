import pandas as pd
from datetime import datetime
import logging
from scripts_local.utils.utils import format_users_data, extract_users_api, export_to_json, extract_weather_api

def extract_users_data_json():
    """
    Extract user data from an API and export it to JSON format.
    """
    logging.info('Extracting user data from API...')
    users_data = extract_users_api()
    if users_data:
        logging.info('Exporting user data to JSON...')
        export_to_json('./datalake/bronze/', users_data, 'users.json')
        logging.info('User data exported to JSON successfully')
    else:
        logging.error('Failed to fetch user data from API')

def extract_users_data_csv():
    """
    Extract user data from an API and export it to CSV format.
    """
    logging.info('Extracting user data from API...')
    users_data = extract_users_api()
    if users_data:
        logging.info('Formatting user data...')
        formatted_data = [format_users_data(user) for user in users_data]
        users_df = pd.DataFrame(formatted_data)
        logging.info('Exporting user data to CSV...')
        users_df.to_csv('./datalake/bronze/users.csv', index=False)
        logging.info('User data exported to CSV successfully')
    else:
        logging.error('Failed to fetch user data from API')

# def extract_users_df():
#     users_data = extract_users_api()
#     formatted_data = [format_users_data(user) for user in users_data]
#     return pd.DataFrame(formatted_data)

def extract_weather_data_csv():
    """
    Extract weather data based on user locations and export it to CSV format.
    """
    logging.info('Extracting user data from API...')
    users_data = extract_users_api()
    if users_data:
        logging.info('Formatting user data...')
        formatted_data = [format_users_data(user) for user in users_data]
        users_df = pd.DataFrame(formatted_data)
        location_df = users_df[['id', 'lat', 'lng']]
        locationlist = list(location_df.values)
        logging.info('Extracting weather data...')
        weather_data = extract_weather_api(locationlist)
        if weather_data:
            logging.info('Exporting weather data to CSV...')
            weather_df = pd.DataFrame(weather_data)
            weather_df.to_csv('./datalake/bronze/weather.csv', index=False)
            logging.info('Weather data exported to CSV successfully')
        else:
            logging.error('Failed to fetch weather data')
    else:
        logging.error('Failed to fetch user data from API')