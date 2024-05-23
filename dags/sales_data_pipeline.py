from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from scripts.data_delivery import *
from scripts.data_enrichment import process_users_data, process_sales_data
from scripts.extract_data import extract_users_data_json, extract_users_data_csv
from airflow.models import Variable

# Define default arguments for the DAG
default_args = {
    'owner': 'Ahmed Ashraf',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

# Create the DAG
dag = DAG(
    'sales_pipeline',
    default_args=default_args,
    description='E-E sales data pipeline',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
)
def load_credentials():
    host = Variable.get("host")
    db_name = Variable.get("database")
    user = Variable.get("user")
    password = Variable.get("password")
    return {
        "host": host,
        "db_name": db_name,
        "user": user,
        "password": password
    }

# Define task functions
def database_preparation():
    db_credentials = load_credentials()
    print('database_preparation started')
    drop_tables(db_credentials['host'],db_credentials['db_name'],db_credentials['user'],db_credentials['password'])
    create_tables(db_credentials['host'],db_credentials['db_name'],db_credentials['user'],db_credentials['password'])
    print('database_preparation done')

def data_extraction():
    print('extraction started')
    extract_users_data_json()
    extract_users_data_csv()
    print('extraction done')

def data_enrichment():
    print('data_enrichment started')
    process_users_data()
    process_sales_data(Variable.get("OPENWEATHERMAP_API_KEY"))
    print('data_enrichment done')

def data_delivery():
    db_credentials = load_credentials()
    print('data_delivery started')
    load_users_dim(db_credentials['host'],db_credentials['db_name'],db_credentials['user'],db_credentials['password'])
    load_sales_dim(db_credentials['host'],db_credentials['db_name'],db_credentials['user'],db_credentials['password'])
    load_product_data(db_credentials['host'],db_credentials['db_name'],db_credentials['user'],db_credentials['password'])
    load_stores_dim(db_credentials['host'],db_credentials['db_name'],db_credentials['user'],db_credentials['password'])
    print('data_delivery done')

# Define the tasks
database_preparation_task = PythonOperator(
    task_id='database_preparation',
    python_callable=database_preparation,
    dag=dag,
)

data_extraction_task = PythonOperator(
    task_id='data_extraction',
    python_callable=data_extraction,
    dag=dag,
)

data_enrichment_task = PythonOperator(
    task_id='data_enrichment',
    python_callable=data_enrichment,
    dag=dag,
)

data_delivery_task = PythonOperator(
    task_id='data_delivery',
    python_callable=data_delivery,
    dag=dag,
)

# Set task dependencies
database_preparation_task >> data_extraction_task >> data_enrichment_task >> data_delivery_task