# Comprehensive Sales Data Pipeline

The pipeline should combine generated sales data with data from external sources, perform data
transformations and aggregations, and store the final dataset in a database. 
The aim is to enable analysis and derive insights into customer behaviour and sales performance.

## Table of Contents
- [Introduction](#introduction)
- [Database Schema](#database-schema)
- [Reporting](#reporting-layer)
- [Setup](#setup)
---

## Introduction

The goal of this project is to build an end-to-end data pipeline for sales data, integrating external weather data, transforming it, and storing it in a data warehouse. Throughout the planning process, various approaches were considered to tackle emerging challenges. 
Initially, a straightforward ETL job was considered, but the project was made more challenging and modern by adopting the Medallion architecture. 
This architecture incrementally and progressively improves the structure and quality of data as it flows through each layer (from Bronze ⇒ Silver ⇒ Gold).

- The sales data pipeline is designed with modularity and scalability in mind. 
- The codebase is organized into separate modules and packages to encapsulate related functionality and promote code reusability. 
- incorporates robust error handling mechanisms to gracefully handle exceptions and ensure smooth execution.

![Solution Architecture](https://github.com/ahmedashraffcih/E2E_Sales_Data_Pipeline/blob/main/assets/arch.png)

---

### Assumptions 
- The sales data is assumed to be clean and does not require extensive cleaning or preprocessing.
- Weather data from the OpenWeatherMap API is assumed to be accurate and reliable.
- The database schema follows a star schema design for efficient querying and analysis.
- SCD Type 2 logic is applied to track historical changes in user and product data for analytical purposes.
- Specific considerations for sales_data.csv:
    - When creating a product dimension table from the source data, I encountered products that appeared multiple times with varying prices and unusual dates. Initially, I considered calculating the average price for each product. However, I determined that the best approach was to take the latest price based on the most recent order date for each product.
    - To accurately associate weather data with each sale, it would have been ideal to fetch weather data from the API using the sale date along with the latitude and longitude. Unfortunately, this option was not available. Additionally, the only available latitude and longitude values were those associated with users.
    - Therefore, I generated dummy data for stores and applied the logic to use the store's latitude and longitude for associating weather data with sales.

---

### Step 1: Data Collection and Storage

We have 3 different Data Sources:

- Sales Data: Stored in CSV format.
- Users Data: Provided in a nested JSON format API, available at https://jsonplaceholder.typicode.com/users
- Weather Data: Retrieved using the OpenWeatherMap API. Register to get an API key, which is free for limited daily requests.

- extract_data.py
    Data is initially stored in a data lake in the "bronze" layer (raw data) in csv format to have unified landing zone.
    - extract_users_data_json()
        - Extracts users data from the API and stores it as-is in the bronze layer.
    - extract_users_data_csv()
        - Extracts users data from the API, formats it in CSV, and saves it in the bronze layer.
---

### Step 2: Data Enrichment

- data_enrichment.py: 
    - process_users_data()
        - Loads new users' data from the Bronze layer and applies SCD Type 2 logic
        - Saves the final DataFrame back to the Silver layer, ensuring historical changes are tracked according to SCD Type 2 methodology.
    
    - process_sales_data()
        - Removes duplicate entries, calculates the latest product price, and merges with weather data based on store ID.

---

### Step 3: Data Delivery

- tables_creation.py:
    - Contains functions to create, drop, and load tables, reading the statements from sql_queries.py for preparing the data warehouse.

- data_delivery.py
    - load_users_dim()
        - Load transformed user data from silver layer, selecting required columns and loaded into a PostgreSQL database in the Gold layer

    - load_sales_dim()
        - Load transformed sales data from silver layer, selecting required columns and loaded into a PostgreSQL database in the Gold layer

    - load_stores_dim()
        - Extracts and cleans store data from the Silver layer, generates dummy store names along with country information, handles missing values, and loads it into a PostgreSQL database in the Gold layer.

    - load_product_data()
        - Extracts and cleans product data from the Silver layer, calculates the latest product price, and applies SCD Type 2 logic to maintain product history

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
### Extra Functionallity

- utils.py
    - The `utils.py` module contains utility functions used across the pipeline for common tasks such as data parsing, file handling, and API interactions. 
    - These functions abstract away repetitive tasks and promote cleaner, more maintainable code.

- db_utils.py
    - The `db_utils.py` module provides a set of database utility functions for interacting with the PostgreSQL database. 
    - These functions handle database connections, data loading, and query execution, ensuring efficient and reliable data management within the pipeline.



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

![Data Model](https://github.com/ahmedashraffcih/E2E_Sales_Data_Pipeline/blob/main/assets/data_model.png)

---

## Reporting Layer

![Dashboard 1](https://github.com/ahmedashraffcih/E2E_Sales_Data_Pipeline/blob/main/reporting/assets/report_1.png)
![Dashboard 2](https://github.com/ahmedashraffcih/E2E_Sales_Data_Pipeline/blob/main/reporting/assets/report_2.png)

- Sales Analysis: Aggregate sales data to analyze performance metrics such as total sales, quantity sold, average price, and sales margins over different time periods (e.g., daily, weekly, monthly).

- Product Analysis: Identify top-selling products.

- Store Performance: Identify high-performing stores.

- Weather Impact: Assess the impact of weather conditions on sales by correlating sales data with weather data.

- Metrics
    - Average Order Amount
    - Average Order Quantity
    - Average Sales
    - Order Count
    - Quarterly Sales
    - Total Sales
    - Total Sales monthly difference 
    - Total Sales per weather

By performing these aggregations and data manipulations, businesses can gain valuable insights into their sales operations, customer behavior, product performance, and market trends, enabling informed decision-making and strategic planning.

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
git clone https://github.com/ahmedashraffcih/E2E_Sales_Data_Pipeline
```
2. Navigate to Project Directory: Move into the project directory.

```
cd E2E_Sales_Data_Pipeline
```

3. Install the required packages
```
pip install requirements.txt
```

4. Create .env file the project directory and add the credentials

5. Run main.pyproduct performance by calculating metrics such as sales volume, revenue, profitability, and customer satisfaction ratings. Identify top-selling products, slow-moving items, and product
```
python main.py
```

---


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.