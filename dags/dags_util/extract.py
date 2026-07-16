from dags_tasks.tasks.extractors.drivers import fetch_driver
from dags_tasks.tasks.extractors.constructor import fetch_constructor
from dags_tasks.tasks.extractors.races import fetch_race

from data_model.bronze import Driver, Constructor, Race

from storage.write_parquet import write_parquet

import pandas as pd

def extract(data_extract,season):
    if(data_extract == 'drivers'):
        df = fetch_driver(season)
        records = df.to_dict(orient='records')
        validated = [
            Driver.model_validate(record).model_dump()
            for record in records
        ]
        df = pd.DataFrame(validated)
    elif(data_extract == 'constructors'):
        df = fetch_constructor(season)
        records = df.to_dict(orient = "records")

        validated = [
            Constructor.model_validate(record).model_dump()
            for record in records
        ]
        df = pd.DataFrame(validated)
    else:
        df = fetch_race(season)
        records = df.to_dict(orient = "records")

        validated = [
            Race.model_validate(record).model_dump()
            for record in records
        ]
        df = pd.DataFrame(validated)
    path = write_parquet(
        df,
        f"/opt/airflow/tmp/{data_extract}/{data_extract}_{season}.parquet"
    )
    return path