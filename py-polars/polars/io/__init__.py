"""Functions for reading data."""

from polars.io.avro import read_avro
from polars.io.csv import read_csv
from polars.io.csv import read_csv_batched
from polars.io.csv import scan_csv
from polars.io.database import read_database
from polars.io.database import read_sql
from polars.io.delta import read_delta
from polars.io.delta import scan_delta
from polars.io.excel import read_excel
from polars.io.ipc import read_ipc
from polars.io.ipc import scan_ipc
from polars.io.json import read_json
from polars.io.ndjson import read_ndjson
from polars.io.ndjson import scan_ndjson
from polars.io.parquet import read_parquet
from polars.io.parquet import scan_parquet
from polars.io.pyarrow_dataset import scan_ds
from polars.io.pyarrow_dataset import scan_pyarrow_dataset

__all__ = [
    "read_avro",
    "read_csv",
    "read_csv_batched",
    "read_database",
    "read_delta",
    "read_excel",
    "read_ipc",
    "read_json",
    "read_ndjson",
    "read_parquet",
    "read_sql",
    "scan_csv",
    "scan_delta",
    "scan_ds",
    "scan_ipc",
    "scan_ndjson",
    "scan_parquet",
    "scan_pyarrow_dataset",
]
