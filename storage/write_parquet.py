import pyarrow as pa
import pyarrow.parquet as pq


def write_parquet(df, path):
    table = pa.Table.from_pandas(df)

    pq.write_table(
        table,
        path,
        compression='snappy'
    )