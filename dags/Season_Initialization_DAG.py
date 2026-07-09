from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.models.param import Param
from airflow.decorators import get_current_context

from dags_tasks.tasks.extractors.drivers import fetch_driver
from dags_tasks.tasks.extractors.constructor import fetch_constructor
from dags_tasks.tasks.extractors.races import fetch_race

from storage.write_parquet import write_parquet
from storage.minio_client import upload_file

from pathlib import Path
import os

default_args = {
    "owner": "f1-pipeline",
    "retries": 3,
    "retry_delay": timedelta(minutes = 5)
}

@dag(
    dag_id = "init_season_data",
    start_date = datetime(2026,1,1),
    schedule = None,
    catchup = False,
    default_args = default_args,
    tags = ['bronze', 'season_init'],
    params = {
        "season": Param(2027,type = "integer")
    }
)
def init_season_data():
    @task
    def extract_drivers():
        
        context = get_current_context()
        season = context["params"]["season"]

        df = fetch_driver(season)

        path = write_parquet(
            df,
            f"/opt/airflow/tmp/drivers/drivers_{season}.parquet"
        )
        return path
    @task
    def upload_drivers(local_path):

        upload_file(
            "bronze",
            f"drivers/{Path(local_path).name}",
            local_path
        )
    @task
    def extract_constructors():
        context = get_current_context()
        season = context["params"]["season"]
        df = fetch_constructor(season)
        path = write_parquet(
            df,
            f"/opt/airflow/tmp/constructors/constructors_{season}.parquet"
        )
        return path
    @task
    def upload_constructors(local_path):

        upload_file(
            "bronze",
            f"constructors/{Path(local_path).name}",
            local_path
        )
    @task
    def extract_races():
        context = get_current_context()
        season = context["params"]["season"]
        df = fetch_race(season)
        path = write_parquet(
            df,
            f"/opt/airflow/tmp/races/races_{season}.parquet"
        )
        return path
    @task
    def upload_races(local_path):

        upload_file(
            "bronze",
            f"races/{Path(local_path).name}",
            local_path
        )
    @task
    def cleanup(local_path): #clean up temporary file after upload to minIO
        os.remove(local_path)

        
    drivers_path = extract_drivers()
    upload_drivers(drivers_path)
    cleanup(drivers_path)
    constructors_path = extract_constructors()
    upload_constructors(constructors_path)
    cleanup(constructors_path)
    races_path = extract_races()
    upload_races(races_path)
    cleanup(races_path)



dag = init_season_data()