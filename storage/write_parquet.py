import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

def write_parquet(df, path):
    table = pa.Table.from_pandas(df, preserve_index = False)

    output_path = Path(path)
    
    output_path.parent.mkdir(parents = True, exist_ok = True)

    pq.write_table(
        table,
        output_path,
        compression='snappy'
    )
    return str(output_path)