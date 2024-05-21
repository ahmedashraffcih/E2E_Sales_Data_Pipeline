import pandas as pd
import os
from datetime import datetime
import re

from scripts.extract_data import extract_weather_data_csv

def process_users_data():
    users_df = pd.read_csv('./datalake/bronze/users.csv')
    users_df['start_date'] = pd.to_datetime('today').date()
    users_df['end_date'] = '9999-12-31'
    users_df['is_current'] = True
    users_df['phone'] = users_df['phone'].apply(lambda x:re.sub(r'\D', '', x))
    users_df.to_csv('./datalake/silver/users.csv',index=False)

def process_sales_data():
    sales_df = pd.read_csv('./datalake/bronze/sales_data.csv')
    weather_df = extract_weather_data_csv()
    weather_df = weather_df.astype({'id': str })
    sales_df = sales_df.astype({'customer_id': str })
    SalesData_full =  pd.merge(sales_df, weather_df, left_on=['customer_id'], right_on= ['id'], how='inner')
    SalesData_full.to_csv('./datalake/silver/sales_data.csv',index=False)