# F1 Telemetry End-To_End Pipeline

Data pipeline that extracts telemetry data from [fastf1](https://theoehrly-fast-f1.mintlify.app/introduction) api 

## architecture
![Architecture](image/architecture.png)

Project containerized through [Docker](https://www.docker.com/) and orchestrated through [Airflow](https://airflow.apache.org/)

pipeline workflow:
1. extract data from [Fastf1](https://theoehrly-fast-f1.mintlify.app/introduction) api to generate bronze layer data
2. Load bronze data to [MinIO](https://www.min.io/)
3. Load bronze data to [PostgreSQL](https://www.postgresql.org/docs/)
4. Initial data parsing and validation through Pydantic to generate silver data
5. aggregated data for analytics

