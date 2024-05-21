import pandas as pd
from datetime import datetime
from utils.utils import format_data, extract_users_api, export_to_json

def extract_users_data_json():
    # Export data to bronze layer
    users_data = extract_users_api()
    export_to_json('./datalake/bronze/',users_data,'users.json')

def extract_users_data_csv():
    users_data = extract_users_api()
    formatted_data = [format_data(user) for user in users_data]
    users_df = pd.DataFrame(formatted_data)
    users_df.to_csv('./datalake/bronze/users.csv',index=False)
    print('users.csv file has been exported to ./datalake/bronze/users.csv')

extract_users_data_csv()