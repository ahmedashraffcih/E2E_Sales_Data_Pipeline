import pandas as pd
import os
from datetime import datetime
import re
def load_users_dim():
    users_df = pd.read_csv('./datalake/silver/users.csv')
    users_df = users_df[['id','name','email','phone','city','start_date','end_date','is_current']]
    users_df.to_csv('./datalake/gold/users_dim.csv',index=False)

def load_sales_dim():
    sales_df = pd.read_csv('./datalake/silver/sales_data.csv')
    sales_df = sales_df[['order_id','customer_id','product_id','quantity','price','order_date','weather','temp','humidity']]
    sales_df.to_csv('./datalake/gold/sales_fact.csv',index=False)

def load_product_data():
    sales_df = pd.read_csv('./datalake/silver/sales_data.csv')
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    product_df = sales_df.groupby('product_id').apply(lambda x: x.loc[x['order_date'].idxmax()])
    product_df['price'] = round(product_df['price']/product_df['quantity'],2)
    product_df['product_name'] = 'product_' + product_df['product_id'].astype(str)
    product_df = product_df[['product_id','product_name','price']]
    # product_df['start_date'] = pd.to_datetime('today').date()
    # product_df['end_date'] = '9999-12-31'
    # product_df['is_current'] = True
    product_df.to_csv('./datalake/gold/product_master.csv',index=False)