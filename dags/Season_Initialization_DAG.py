from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.models.param import Param
from airflow.operators.python import get_current_context
from airflow.operators.bash import BashOperator

from dags_util.extract import extract
from storage.minio_client import upload_file, read_parquet_from_minio
from storage.postgres_client import load_parquet_to_postgres

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

        path = extract("drivers",season)
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

        path = extract("constructors",season)
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

        path = extract("races",season)
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
    @task
    def push_from_minio_to_postgresql():
        context = get_current_context()
        season = context["params"]["season"]

        race_df = read_parquet_from_minio("bronze", f"races/races_{season}.parquet")
        constructor_df = read_parquet_from_minio("bronze", f"constructors/constructors_{season}.parquet")
        driver_df = read_parquet_from_minio("bronze", f"drivers/drivers_{season}.parquet")


        load_parquet_to_postgres(driver_df, "drivers", "bronze")
        load_parquet_to_postgres(constructor_df, "constructors", "bronze")
        load_parquet_to_postgres(race_df, "races", "bronze")

        
    drivers_path = extract_drivers()
    drivers_upload = upload_drivers(drivers_path)
    drivers_cleanup = cleanup(drivers_path)

    constructors_path = extract_constructors()
    constructors_upload = upload_constructors(constructors_path)
    constructors_cleanup = cleanup(constructors_path)

    races_path = extract_races()
    races_upload = upload_races(races_path)
    races_cleanup = cleanup(races_path)

    
    drivers_upload >> drivers_cleanup
    constructors_upload >> constructors_cleanup
    races_upload >> races_cleanup

    
    push_task = push_from_minio_to_postgresql()

    dbt_build = BashOperator(
        task_id = "dbt_build",
        bash_command="""
            set -e

            cd /opt/airflow/project/dbt/f1_data_warehouse

            dbt debug --profiles-dir .

            dbt build --profiles-dir . --select stg_drivers stg_races stg_constructors
        """
    )

    mart_build = BashOperator(
        task_id = "mart_build",
        bash_command="""
            set -e

            cd /opt/airflow/project/dbt/f1_data_warehouse

            dbt debug --profiles-dir .

            dbt build --profiles-dir . --select dim_drivers dim_constructors dim_races
        """
    )



    [drivers_cleanup, constructors_cleanup, races_cleanup] >> push_task >> dbt_build >> mart_build
    
    



dag = init_season_data()