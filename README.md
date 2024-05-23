# Comprehensive Sales Data Pipeline
The pipeline should combine generated sales data with data from external sources, perform data
transformations and aggregations, and store the final dataset in a database. 
The aim is to enable analysis and derive insights into customer behaviour and sales performance.


## Introduction

The goal of this project is to build an end-to-end data pipeline for sales data, integrating external weather data, transforming and storing it in a data warehouse.
through out the planning for the project I got different approaches to work with more and more investigating different challenges appears
I first though about the straight-forward solution to just perform normal ETL job in once but I wanted to make it more challangeble and more modern.
So the approach I followed is the Medallion-architecture to apply the with the goal of incrementally and progressively improving the structure and quality of data as it flows through each layer of the architecture (from Bronze ⇒ Silver ⇒ Gold layer tables)

### Step 1: Data Collection and Storage

We have 3 different Data Sources:

- Sales Data: Stored in CSV format.
- Users Data: Provided in a CSV file.
- Weather Data: Retrieved using the OpenWeatherMap API.

Data is initially stored in a data lake in the "bronze" layer (raw data).

### Step 2: Data Extraction and Transformation
After we loaded the data into our landing zone we can directly use it as our source.
Through out the developing of the data pipeline there's some data issues appeared
- sales_data.csv 
    - some products appeared multiple times with different prices and weird dates first I though about taking the average price of the product through the data, but the best case is to take the latest price by the latest order date of the purchase
- Since we need to know the weather for each sale it will make more since if we can fetch the data from the api with the sale date in addition to the lat and lan but that wasn't an option and also the only lat and lan values we have appears in the users side.
- I though about creating fake data for stores but the requirments

Loading New Users Data: The new users' data is loaded from the Bronze layer, and the necessary SCD columns (start_date, end_date, is_current) are added.

Loading Existing Users Data: The existing users' data is loaded from the Silver layer. If the file does not exist, an empty DataFrame is created.

Applying SCD Type 2 Logic: The new users' data is iterated over, and for each user, it checks if a corresponding record exists in the existing data:

If a change is detected, the end_date and is_current fields of the existing record are updated.
The new record is added to the list of updated users.
If no corresponding record exists, the new record is directly added.
Merging Data: The updated users' DataFrame is concatenated with the existing users' DataFrame to create the final users' DataFrame.

Saving to Silver Layer: The final DataFrame is saved back to the Silver layer.

This function ensures that historical changes are tracked for each user, maintaining a history of changes according to the SCD Type 2 methodology.

### Step 3: Data Delivery
- The choice between either Upsert the data or full load the data from silver layer I chose the full load approach since it have some advantages:
    - Simplifies the process, as it involves overwriting the entire dataset.
    - Ensures that the Gold layer is always in sync with the Silver layer without missing any updates.
    - Useful when data consistency and completeness are more critical than efficiency.

- Decision Factors
    - Dataset Size: For large datasets with minimal changes, use upsert. For small to moderate datasets, full load might be simpler and easier.
    - Frequency of Changes: If changes are frequent and impact a significant portion of the data, consider full load. For sparse and infrequent changes, upsert is more efficient.
    - Historical Accuracy: If maintaining historical accuracy and tracking incremental changes are critical, upsert is preferred.
    - Resource Constraints: Full load operations are resource-intensive. If resources are limited, upsert can be more efficient.

## Setting Up and Running the Data Pipeline
- We have 2 options either running the pipeline manually using main.py or using airflow through docker
- Prerequisites for Airflow
    - Docker
    - OpenWeatherMap API key for fetching weather data.
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

- Prerequisites for local
    - Python 3.x installed on your system.
    - Docker
    - OpenWeatherMap API key for fetching weather data.
    - Libraries in requirments.txt
    - .env file to store credentials
        - API Key
        - Database Credentials (host,db,user,password)

## Explanation of Data Transformation Steps and Assumptions
1. Data Extraction: The pipeline extracts sales data from a CSV file, users data from a CSV file, and weather data from the OpenWeatherMap API.

2. Data Cleaning and Transformation:

    - Sales Data: Removes duplicate entries, calculates the latest product price, and merges with weather data based on store ID.
    - Users Data: Applies slowly changing dimension (SCD) Type 2 logic to handle historical changes and updates in user data.
    - Product Data: Calculates the latest product price and applies SCD Type 2 logic to maintain product history.
    - Store Data: Cleans store data and handles missing values for country information.
    - Data Loading: The transformed data is loaded into a PostgreSQL database in the Gold layer, consisting of dimension and fact tables.
3. Data Loading: The transformed data is loaded into a PostgreSQL database in the Gold layer, consisting of dimension and fact tables.
4. Assumptions:
    - The sales data is assumed to be clean and does not require extensive cleaning or preprocessing.
    - Weather data from the OpenWeatherMap API is assumed to be accurate and reliable.
    - The database schema follows a star schema design for efficient querying and analysis.
    - SCD Type 2 logic is applied to track historical changes in user and product data for analytical purposes.

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

## Features

- Continuous Integration: Automatically runs unit tests whenever changes are pushed to the repository to ensure code quality.
- Continuous Deployment: Automates the deployment process, pushing updated DAGs and requirements files to AWS S3 for Airflow to consume.
- Integration with AWS MWAA: Seamlessly integrates with AWS Managed Workflows for Apache Airflow, allowing for efficient management and execution of DAGs.
- GitHub Actions: Utilizes GitHub Actions for orchestrating the CI/CD pipeline, providing a flexible and configurable automation framework.

## Setup

### Prerequisites

Before using this pipeline, ensure you have the following prerequisites installed:

- Python
- Docker

### Configuration

1. Clone this repository to your local machine.
2. Customize the DAGs in the `dags` directory according to your requirements.
3. Set up your AWS credentials and region in your GitHub repository secrets.

## Usage

### Running the CI/CD Pipeline

To deploy your DAGs using the CI/CD pipeline, follow these steps:

1. Make changes to your DAGs locally.
2. Commit and push your changes to the `main` branch of this repository.
3. The CI/CD pipeline will automatically trigger on each push to the `main` branch.
4. The pipeline will build a Docker image, run unit tests, deploy the DAGs to AWS S3, and trigger Airflow to reload the DAGs.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

