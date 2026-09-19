# End-to-End Formula 1 Data Engineering Pipeline

An end-to-end batch data pipeline that ingests Formula 1 telemetry and race data from the [Fastf1](https://theoehrly-fast-f1.mintlify.app/introduction) API, stores raw data in a Bronze layer on [MinIO](https://www.min.io/), transforms it into curated Silver and Gold layers in [PostgreSQL](https://www.postgresql.org/docs/).

## Architecture
![Architecture](image/architecture.png)

Project containerized through [Docker](https://www.docker.com/) and orchestrated through [Airflow](https://airflow.apache.org/).

pipeline workflow:
1. extract data from [Fastf1](https://theoehrly-fast-f1.mintlify.app/introduction) api to generate bronze layer data.
2. Load bronze data to [MinIO](https://www.min.io/).
3. Validate incoming records using [Pydantic](https://pypi.org/project/pydantic/) models before loading them into the Silver layer.
4. generate star-schema analytical tables including race results, lap statistics, and telemetry metrics for dashboarding.

## Airflow architecture 
Pipeline is divided into multiple DAGs following the Medallion Architecture (Bronze -> silver -> gold)
### Bronze layer
consists of 3 independent ingestion DAGs.
#### 1. Season Initialization DAG
This DAG is executed at the beginning of each Formula 1 season or triggered manual when there is changed in season data
It contains 3 independent tasks that can run in parallel:
- **Fetch drivers**
    - Retrieve driver information from Jolpica API.
    - Convert the data to parquet format.
    - Upload the Parquet file to Bronze bucket.
- **Fetch constructors**
    - Retrieve constructors information from Jolpica API.
    - Convert the data to parquet format.
    - Upload the Parquet file to Bronze bucket.
- **Fetch races**
    - Retrieve races metadata for the season.
    - Convert the data to parquet format.
    - Upload the Parquet file to Bronze bucket.
#### 2. Race result DAG
This DAG will check race result and fetch result data about position, points gain or fastest lap time

## How to run project
- **Prerequisites**
    - install [docker desktop](https://docs.docker.com/desktop/setup/install/windows-install/) and python
- **how to run**
    - open cmd and change directory to project folder
    - run
        ```
        docker compose up --build
        ```
    - open web browser and access airflow webserver by searching
        ```
        http://localhost:8080/
        ```
    - manually run the season init DAG and input the current season