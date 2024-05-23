FROM apache/airflow:2.4.3-python3.9

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts