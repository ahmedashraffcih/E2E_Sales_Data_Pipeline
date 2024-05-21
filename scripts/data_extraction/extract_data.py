import pandas as pd
from datetime import datetime
from utils.utils import format_users_data, extract_users_api, export_to_json, extract_weather_api

def extract_users_data_json():
    # Export data to bronze layer
    users_data = extract_users_api()
    export_to_json('./datalake/bronze/',users_data,'users.json')

def extract_users_data_csv():
    users_data = extract_users_api()
    formatted_data = [format_users_data(user) for user in users_data]
    users_df = pd.DataFrame(formatted_data)
    users_df.to_csv('./datalake/bronze/users.csv',index=False)
    print('users.csv file has been exported to ./datalake/bronze/users.csv')

# def extract_users_df():
#     users_data = extract_users_api()
#     formatted_data = [format_users_data(user) for user in users_data]
#     return pd.DataFrame(formatted_data)

def extract_weather_data_csv():
    # Export data to bronze layer
    users_data = extract_users_api()
    formatted_data = [format_users_data(user) for user in users_data]
    users_df = pd.DataFrame(formatted_data)
    location_df = users_df[['id', 'lat', 'lng']]
    locationlist = list(location_df.values)
    weather_df = pd.DataFrame(extract_weather_api(locationlist))
    weather_df.to_csv('./datalake/bronze/weather.csv',index=False)