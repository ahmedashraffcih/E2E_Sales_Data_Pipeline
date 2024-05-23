import pandas as pd
import os
from datetime import datetime
import re
import random
from scripts.utils.utils import *

def process_users_data():
    users_df = pd.read_csv('./datalake/bronze/users.csv')
    users_df['start_date'] = pd.to_datetime('today').date()
    users_df['end_date'] = '9999-12-31'
    users_df['is_current'] = True
    users_df['phone'] = users_df['phone'].apply(lambda x:re.sub(r'\D', '', x))
    # users_df.to_csv('./datalake/silver/users.csv',index=False)
    ##### Applying SCD Type 2 Logic
    try:
        # Load existing users data
        existing_users_df = pd.read_csv('./datalake/silver/users.csv')
        existing_users_df['start_date'] = pd.to_datetime(existing_users_df['start_date'])
        existing_users_df['end_date'] = existing_users_df['end_date']
    except FileNotFoundError:
        # If the Silver layer file does not exist, initialize it
        existing_users_df = pd.DataFrame(columns=users_df.columns)
    # list to hold the updated records
    updated_users = []

    for idx, new_row in users_df.iterrows():
        existing_row = existing_users_df[existing_users_df['user_id'] == new_row['user_id']]
        
        if not existing_row.empty:
            existing_row = existing_row.iloc[0]
            # Check for changes
            if (new_row['name'] != existing_row['name']) or \
               (new_row['email'] != existing_row['email']) or \
               (new_row['city'] != existing_row['city']):
                
                # Update existing record 
                existing_users_df.loc[existing_users_df['user_id'] == new_row['user_id'], 'end_date'] = datetime.now().date()
                existing_users_df.loc[existing_users_df['user_id'] == new_row['user_id'], 'is_current'] = False
                # Add the new record
                updated_users.append(new_row)
        else:
            # Add if it doesn't exist
            updated_users.append(new_row)
            
    updated_users_df = pd.DataFrame(updated_users)
    final_users_df = pd.concat([existing_users_df, updated_users_df], ignore_index=True)
    # Save the final DataFrame to the Silver layer
    os.makedirs('./datalake/silver/', exist_ok=True)
    final_users_df.to_csv('./datalake/silver/users.csv', index=False)

def process_sales_data(api_key):
    os.makedirs('./datalake/bronze/', exist_ok=True)
    sales_df = pd.read_csv('./datalake/bronze/sales_data.csv')
    sales_df.drop_duplicates(subset=['order_id'], inplace=True)
    store_ids = [random.randint(1, 20) for _ in range(len(sales_df))]
    sales_df['store_id'] = store_ids
    weather_data = []
    for store_id in range(1, 21):
        latitude = random.uniform(-90, 90)  
        longitude = random.uniform(-180, 180)
        weather_info = extract_weather_api2(latitude, longitude,api_key)
        if weather_info:
            weather_data.append({
                'store_id': store_id,
                'lat':weather_info['lat'],
                'lng':weather_info['lng'],
                'weather': weather_info['weather'],
                'description': weather_info['description'],
                'temp': weather_info['temp'],
                'pressure': weather_info['pressure'],
                'humidity': weather_info['humidity'],
                'country': weather_info['country'],
            })
    weather_df = pd.DataFrame(weather_data)
    merged_df = pd.merge(sales_df, weather_df, on='store_id', how='left')
    os.makedirs('./datalake/silver/', exist_ok=True)
    merged_df.to_csv('./datalake/silver/sales_data.csv', index=False)
    

# def process_sales_data():
#     sales_df = pd.read_csv('./datalake/bronze/sales_data.csv')
#     store_names = ['Store_A', 'Store_B', 'Store_C', 'Store_D', 'Store_E','Store_F','Store_G']
#     latitudes = [34.0522, 36.1699, 40.7128, 37.7749, 34.0522]
#     longitudes = [-118.2437, -115.1398, -74.0060, -122.4194, -118.2437]
#     # Add columns for store_name, lat, and lng with random values
#     sales_df['store_name'] = [random.choice(store_names) for _ in range(len(sales_df))]
#     sales_df['lat'] = [random.choice(latitudes) for _ in range(len(sales_df))]
#     sales_df['lng'] = [random.choice(longitudes) for _ in range(len(sales_df))]
#     # print(sales_df)
#     location_df = sales_df[['order_id', 'lat', 'lng']]
#     locationlist = list(location_df.values)
#     weather_df = pd.DataFrame(extract_weather_api(locationlist))
#     print(weather_df.head(5))
#     # weather_df = weather_df.astype({'order_id': str })
#     # sales_df = sales_df.astype({'order_id': str })
#     # SalesData_full =  pd.merge(sales_df, weather_df, left_on=['order_id'], right_on= ['id'], how='inner')
#     # SalesData_full.to_csv('./datalake/silver/sales_data.csv',index=False)