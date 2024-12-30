from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from scripts.data_delivery import *
from scripts.data_enrichment import process_users_data, process_sales_data
from scripts.extract_data import extract_users_data_json, extract_users_data_csv
from airflow.models import Variable

# Define default arguments for the DAG
default_args = {
    "owner": "Ahmed Ashraf",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

# Create the DAG
dag = DAG(
    "sales_pipeline",
    default_args=default_args,
    description="E-E sales data pipeline",
    schedule_interval="@daily",
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
        "password": password,
    }


# Define task functions
def database_preparation():
    try:
        db_credentials = load_credentials()
        logging.info("database_preparation started")
        drop_tables(**db_credentials)
        create_tables(**db_credentials)
        logging.info("database_preparation done")
    except Exception as e:
        logging.error(f"Error in database_preparation: {str(e)}")


def data_extraction():
    try:
        logging.info("data_extraction started")
        extract_users_data_json()
        extract_users_data_csv()
        logging.info("data_extraction done")
    except Exception as e:
        logging.error(f"Error in data_extraction: {str(e)}")


def data_enrichment():
    try:
        logging.info("data_enrichment started")
        process_users_data()
        process_sales_data(Variable.get("OPENWEATHERMAP_API_KEY"))
        logging.info("data_enrichment done")
    except Exception as e:
        logging.error(f"Error in data_enrichment: {str(e)}")


def data_delivery():
    try:
        db_credentials = load_credentials()
        logging.info("data_delivery started")
        load_users_dim(**db_credentials)
        load_sales_dim(**db_credentials)
        load_product_data(**db_credentials)
        load_stores_dim(**db_credentials)
        logging.info("data_delivery done")
    except Exception as e:
        logging.error(f"Error in data_delivery: {str(e)}")


database_preparation_task = PythonOperator(
    task_id="database_preparation",
    python_callable=database_preparation,
    dag=dag,
)

data_extraction_task = PythonOperator(
    task_id="data_extraction",
    python_callable=data_extraction,
    dag=dag,
)

data_enrichment_task = PythonOperator(
    task_id="data_enrichment",
    python_callable=data_enrichment,
    dag=dag,
)

data_delivery_task = PythonOperator(
    task_id="data_delivery",
    python_callable=data_delivery,
    dag=dag,
)

(
    database_preparation_task
    >> data_extraction_task
    >> data_enrichment_task
    >> data_delivery_task
)
