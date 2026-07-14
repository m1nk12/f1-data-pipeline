from minio import Minio
from io import BytesIO
import pandas as pd

client = Minio(
    "minio:9000",
    access_key = "minioadmin",
    secret_key = "minioadmin",
    secure = False
)

def upload_file(
    bucket,
    obj_name,
    file_path
):
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    
    client.fput_object(
        bucket,
        obj_name,
        file_path
    )

def read_parquet_from_minio(
    bucket_name,
    object_name
):
    response = client.get_object(
        bucket_name,
        object_name
    )

    try:
        df = pd.read_parquet(
            BytesIO(response.read())
        )
        return df

    finally:
        response.close()
        response.release_conn()