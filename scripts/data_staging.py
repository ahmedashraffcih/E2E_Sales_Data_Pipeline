import pandas as pd
import os
from datetime import datetime
import re


def process_users_data():
    users_df = pd.read_csv('./datalake/bronze/users.csv')
    users_df['start_date'] = pd.to_datetime('today').date()
    users_df['end_date'] = '9999-12-31'
    users_df['is_current'] = True
    users_df['phone'] = users_df['phone'].apply(lambda x:re.sub(r'\D', '', x))
    users_df.to_csv('./datalake/silver/users.csv',index=False)

def process_product_data():
    sales_df = pd.read_csv('./datalake/bronze/sales_data.csv')
    avg_price_df = sales_df.groupby('product_id')['price'].mean().round(2).reset_index()
    product_df = sales_df.drop_duplicates(subset=['product_id'])
    product_df = product_df[['product_id']].merge(avg_price_df, on='product_id', suffixes=('_original', '_average'))
    product_df['product_name'] = 'product_' + product_df['product_id'].astype(str)
    product_df['start_date'] = pd.to_datetime('today').date()
    product_df['end_date'] = '9999-12-31'
    product_df['is_current'] = True
    product_df.to_csv('./datalake/silver/product_master.csv',index=False)