from minio import Minio
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