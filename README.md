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

