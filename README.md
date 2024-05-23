# Comprehensive Sales Data Pipeline
The pipeline should combine generated sales data with data from external sources, perform data
transformations and aggregations, and store the final dataset in a database. 
The aim is to enable analysis and derive insights into customer behaviour and sales performance.

---

## Introduction

The goal of this project is to build an end-to-end data pipeline for sales data, integrating external weather data, transforming and storing it in a data warehouse.
through out the planning for the project I got different approaches to work with more and more investigating different challenges appears
I first though about the straight-forward solution to just perform normal ETL job in once but I wanted to make it more challangeble and more modern.
So the approach I followed is the Medallion-architecture to apply the with the goal of incrementally and progressively improving the structure and quality of data as it flows through each layer of the architecture (from Bronze ⇒ Silver ⇒ Gold layer tables)

### Assumptions 
- The sales data is assumed to be clean and does not require extensive cleaning or preprocessing.
- Weather data from the OpenWeatherMap API is assumed to be accurate and reliable.
- The database schema follows a star schema design for efficient querying and analysis.
- SCD Type 2 logic is applied to track historical changes in user and product data for analytical purposes.
- sales_data.csv 
    - I wanted to create a product dim from the source but some products appeared multiple times with different prices and weird dates first I though about taking the average price of the product through the data, but the best case is to take the latest price by the latest order date of the purchase
    - Since we need to know the weather for each sale it will make more since if we can fetch the data from the api with the sale date in addition to the lat and lan but that wasn't an option and also the only lat and lan values we have appears in the users side.
    - I created a dummy data for stores and applied that logic to the store lat and lng+

---

### Step 1: Data Collection and Storage

We have 3 different Data Sources:

- Sales Data: Stored in CSV format.
- Users Data: Provided in a nested JSON format which can be found at the given URL https://jsonplaceholder.typicode.com/users
- Weather Data: Retrieved using the OpenWeatherMap API https://openweathermap.org/.
    - Register and get an API key, which is free for limited requests for per day

- extract_data.py
    Data is initially stored in a data lake in the "bronze" layer (raw data) in csv format to have unified landing zone.
    - extract_users_data_json()
        - Extract users data from the API and dumb it as is in the bronze layer
    - extract_users_data_csv()
        - Extract users data from the API and foramt it in csv format and save it in the bronze layer 
---

### Step 2: Data Enrichment

- data_enrichment.py: 
    - process_users_data()
        - Loading New Users Data: The new users' data is loaded from the Bronze layer, and applied SCD type 2 logic
        - The final DataFrame is saved back to the Silver layer.
        - This function ensures that historical changes are tracked for each user, maintaining a history of changes according to the SCD Type 2 methodology.
    
    - process_sales_data()
        - Removes duplicate entries, calculates the latest product price, and merges with weather data based on store ID.

---

### Step 3: Data Delivery

- tables_creation.py:
    - Prepared Create, Drop, Load functions which read the statemnts from sql_queries.py which are used to prepare the datawarehouse.

- data_delivery.py
    - load_users_dim()
        - Load transformed user data from silver layer, selecting required columns and loaded into a PostgreSQL database in the Gold layer

    - load_sales_dim()
        - Load transformed sales data from silver layer, selecting required columns and loaded into a PostgreSQL database in the Gold layer

    - load_stores_dim()
        - Load transformed sales data from silver layer, extract and clean store data, generate dummy store name along with the country from the api with handles missing values for country and loaded into a PostgreSQL database in the Gold layer

    - load_product_data()
        - Load transformed sales data from silver layer, extract and clean products data, calculates the latest product price and applies SCD Type 2 logic to maintain product history.

- Loading Approach
    - The choice between either Upsert the data or full load the data from silver layer I chose the full load approach since it have some advantages:
        - Simplifies the process, as it involves overwriting the entire dataset.
        - Ensures that the Gold layer is always in sync with the Silver layer without missing any updates.
        - Useful when data consistency and completeness are more critical than efficiency.

    - Decision Factors
        - Dataset Size: For large datasets with minimal changes, use upsert. For small to moderate datasets, full load might be simpler and easier.
        - Frequency of Changes: If changes are frequent and impact a significant portion of the data, consider full load. For sparse and infrequent changes, upsert is more efficient.
        - Historical Accuracy: If maintaining historical accuracy and tracking incremental changes are critical, upsert is preferred.
        - Resource Constraints: Full load operations are resource-intensive. If resources are limited, upsert can be more efficient.
---

## Database Schema
The transformed data is stored in a relational database with a star schema design, consisting of the following tables:

1. dim_users: Contains information about users, including their name, email, phone number, city, start date, end date, and whether they are current users.
    - Columns: user_id, name, email, phone, city, start_date, end_date, is_current

2. fact_sales: Stores sales data along with relevant information such as product details, order quantity, price, order date, store ID, and weather conditions.
    - Columns: order_id, customer_id, product_id, quantity, price, order_date, store_id, weather, description, temp, pressure, humidity

3. dim_stores: Holds details about stores, including store ID, geographical coordinates (latitude and longitude), and country.
    - Columns: store_id, lat, lng, country

4. dim_product_master: Contains information about products, such as product ID, name, price, start date, end date, and whether it is a current product.
    - Columns: product_id, product_name, price, start_date, end_date, is_current

---

## Setup
- We have 2 options either running the pipeline manually using local enviroment(postgres on docker) or using airflow through docker

### Prerequisites for Airflow

Before using this pipeline, ensure you have the following prerequisites:

- Python
- Docker
- OpenWeatherMap API key for fetching weather data.

---

### Configuration

1. Clone the Repository: Clone the sales data pipeline repository from the GitHub repository.

```
git clone https://github.com/your_username/sales-data-pipeline.git
```
2. Navigate to Project Directory: Move into the project directory.

```
cd sales-data-pipeline
```

3. Run Docker Container: Start a Docker container using the built image.

```
docker-compose up -d
```
4. Access Airflow UI: Access the Airflow web interface by navigating to http://localhost:8080 in your web browser.
5. Add credentials in Airflow Variables
    - API Key
    - Database Credentials (host,db,user,password)
6. Trigger DAG: Trigger the DAG manually from the Airflow UI or wait for the scheduled interval to execute the pipeline automatically.

---

### Prerequisites for Local Enviroment

Before using this pipeline, ensure you have the following prerequisites:

- Python
- Docker
    - You can use postgres locally but remember to change the configurations in .env file 
    - For my case I used postgres on docker
- OpenWeatherMap API key for fetching weather data.
- .env file to store credentials
        - API Key
        - Database Credentials (host,db,user,password)

---

### Configuration
1. Clone the Repository: Clone the sales data pipeline repository from the GitHub repository.

```
git clone https://github.com/your_username/sales-data-pipeline.git
```
2. Navigate to Project Directory: Move into the project directory.

```
cd sales-data-pipeline
```

3. Install the required packages
```
pip install requirements.txt
```

4. Create .env file the project directory and add the credentials

5. Run main.py
```
python main.py
```

---

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.