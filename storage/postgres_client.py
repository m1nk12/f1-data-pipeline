import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine("postgresql+psycopg2://postgresadmin:postgresadmin@postgres_data_warehouse:5432/f1_dw")

def load_parquet_to_postgres(
        df,
        table_name,
        schema
):
    df["time_stamp"] = datetime.now()
    
    df.to_sql(
        name = table_name,
        con = engine,
        schema = schema,
        if_exists = "append",
        index = False,
        method = "multi"
    )