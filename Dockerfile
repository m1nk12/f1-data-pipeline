FROM apache/airflow:2.10.5-python3.11


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

