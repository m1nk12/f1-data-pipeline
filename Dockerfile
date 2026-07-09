FROM apache/airflow:3.0.3-python3.1


USER root

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt