FROM apache/airflow:2.4.3-python3.9

USER root

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev

USER airflow

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs and scripts
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts