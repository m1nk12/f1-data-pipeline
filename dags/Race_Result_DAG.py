from datetime import timedelta, datetime
from dags_tasks.tasks.extractors.race_result import fetch_race_result_data
from storage.write_parquet import write_parquet
from storage.minio_client import upload_file
from storage.postgres_client import load_parquet_to_postgres
from data_model.bronze import Race_result

from airflow.operators.bash import BashOperator
from airflow.decorators import dag, task
from airflow.models.param import Param

from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path
import pendulum

local_tz = pendulum.timezone("Asia/Ho_Chi_Minh")

engine = create_engine("postgresql+psycopg2://postgresadmin:postgresadmin@postgres_data_warehouse:5432/f1_dw")

default_args = {
    "owner": "f1-pipeline",
    "retries": 3,
    "retry_delay": timedelta(minutes = 5)
}

@dag(
    dag_id = "get_race_result",
    start_date = pendulum.datetime(2026,1,1, tz = local_tz),
    schedule_interval = '0 * * * *',
    catchup = False,
    default_args = default_args,
    tags = ['incremental'],
    is_paused_upon_creation=False,
)
def get_race_result():
    @task
    def check_race():
        sql = "SELECT season, round " \
                "FROM gold.dim_races " \
                "WHERE (date + time) " \
                "BETWEEN (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Ho_Chi_Minh') - INTERVAL '24 hours' " \
                "AND (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Ho_Chi_Minh') - INTERVAL '4 hours'"
        
        df = pd.read_sql(sql,con = engine)
        if(df.empty):
            return None

        return {"season": int(df.iloc[0]["season"]), "round": int(df.iloc[0]["round"])}
    @task.branch
    def decision(race):
        if(race is None):
            return "end"

        return "extract_result"
    @task
    def extract_result(race):
        season = race["season"]
        round = race["round"]

        df = fetch_race_result_data(season, round)

        records = df.to_dict(orient='records')
        validated = [Race_result.model_validate(record).model_dump() for record in records]

        df = pd.DataFrame(validated)

        path = write_parquet(
            df,
            f"/opt/airflow/tmp/results/{season}/round_{round}.parquet"
        )

        upload_file(
            "bronze",
            f"results/{season}/{Path(path).name}",
            path
        )

        load_parquet_to_postgres(df, 'race_result', 'bronze')
    @task
    def end():
        print("end")

    race_info = check_race()

    branch = decision(race_info)

    extract = extract_result(race_info)

    finish = end()

    dbt_build = BashOperator(
        task_id = "dbt_build",
        bash_command = """
            set -e
            cd /opt/airflow/project/dbt/f1_data_warehouse

            dbt debug --profiles-dir .

            dbt build --profiles-dir . --select stg_race_result
        """
    )
    gold_layer_build = BashOperator(
            task_id = "gold_layer_build",
            bash_command = """
                set -e
                cd /opt/airflow/project/dbt/f1_data_warehouse

                dbt debug --profiles-dir .

                dbt build --profiles-dir . --select fct_race_result
            """
        )

    race_info >> branch
    branch >> extract
    branch >> finish
    dbt_job = dbt_build >> gold_layer_build
    extract >> dbt_job


    


dag = get_race_result()