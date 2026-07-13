from dags_tasks.tasks.extractors.drivers import fetch_driver
from dags_tasks.tasks.extractors.constructor import fetch_constructor
from dags_tasks.tasks.extractors.races import fetch_race

from storage.write_parquet import write_parquet

def extract(data_extract,season):
    if(data_extract == 'drivers'):
        df = fetch_driver(season)
    elif(data_extract == 'constructors'):
        df = fetch_constructor(season)
    else:
        df = fetch_race(season)
    path = write_parquet(
        df,
        f"/opt/airflow/tmp/{data_extract}/{data_extract}_{season}.parquet"
    )
    return path