import os

from polars import api
from polars.config import Config
from polars.convert import from_arrow
from polars.convert import from_dataframe
from polars.convert import from_dict
from polars.convert import from_dicts
from polars.convert import from_numpy
from polars.convert import from_pandas
from polars.convert import from_records
from polars.datatypes import DATETIME_DTYPES
from polars.datatypes import DURATION_DTYPES
from polars.datatypes import FLOAT_DTYPES
from polars.datatypes import INTEGER_DTYPES
from polars.datatypes import NUMERIC_DTYPES
from polars.datatypes import TEMPORAL_DTYPES
from polars.datatypes import Binary
from polars.datatypes import Boolean
from polars.datatypes import Categorical
from polars.datatypes import DataType
from polars.datatypes import Date
from polars.datatypes import Datetime
from polars.datatypes import Decimal
from polars.datatypes import Duration
from polars.datatypes import Field
from polars.datatypes import Float32
from polars.datatypes import Float64
from polars.datatypes import Int8
from polars.datatypes import Int16
from polars.datatypes import Int32
from polars.datatypes import Int64
from polars.datatypes import List
from polars.datatypes import Null
from polars.datatypes import Object
from polars.datatypes import PolarsDataType
from polars.datatypes import Struct
from polars.datatypes import Time
from polars.datatypes import UInt8
from polars.datatypes import UInt16
from polars.datatypes import UInt32
from polars.datatypes import UInt64
from polars.datatypes import Unknown
from polars.datatypes import Utf8
from polars.exceptions import ArrowError
from polars.exceptions import ColumnNotFoundError
from polars.exceptions import ComputeError
from polars.exceptions import DuplicateError
from polars.exceptions import InvalidOperationError
from polars.exceptions import NoDataError
from polars.exceptions import PanicException
from polars.exceptions import SchemaError
from polars.exceptions import SchemaFieldNotFoundError
from polars.exceptions import ShapeError
from polars.exceptions import StructFieldNotFoundError

# TODO remove need for wrap_df
from polars.internals.dataframe import DataFrame
from polars.internals.dataframe import wrap_df  # noqa: F401
from polars.internals.expr.expr import Expr
from polars.internals.functions import align_frames
from polars.internals.functions import concat
from polars.internals.functions import cut
from polars.internals.functions import date_range
from polars.internals.functions import get_dummies
from polars.internals.functions import ones
from polars.internals.functions import zeros
from polars.internals.io import read_ipc_schema
from polars.internals.io import read_parquet_schema
from polars.internals.lazy_functions import all
from polars.internals.lazy_functions import any
from polars.internals.lazy_functions import apply
from polars.internals.lazy_functions import arange
from polars.internals.lazy_functions import arg_sort_by
from polars.internals.lazy_functions import arg_where
from polars.internals.lazy_functions import argsort_by
from polars.internals.lazy_functions import avg
from polars.internals.lazy_functions import coalesce
from polars.internals.lazy_functions import col
from polars.internals.lazy_functions import collect_all
from polars.internals.lazy_functions import concat_list
from polars.internals.lazy_functions import concat_str
from polars.internals.lazy_functions import corr
from polars.internals.lazy_functions import count
from polars.internals.lazy_functions import cov
from polars.internals.lazy_functions import cumfold
from polars.internals.lazy_functions import cumreduce
from polars.internals.lazy_functions import cumsum
from polars.internals.lazy_functions import date_ as date
from polars.internals.lazy_functions import datetime_ as datetime
from polars.internals.lazy_functions import duration
from polars.internals.lazy_functions import element
from polars.internals.lazy_functions import exclude
from polars.internals.lazy_functions import first
from polars.internals.lazy_functions import fold
from polars.internals.lazy_functions import format
from polars.internals.lazy_functions import from_epoch
from polars.internals.lazy_functions import groups
from polars.internals.lazy_functions import head
from polars.internals.lazy_functions import last
from polars.internals.lazy_functions import list_ as list
from polars.internals.lazy_functions import lit
from polars.internals.lazy_functions import map
from polars.internals.lazy_functions import max
from polars.internals.lazy_functions import mean
from polars.internals.lazy_functions import median
from polars.internals.lazy_functions import min
from polars.internals.lazy_functions import n_unique
from polars.internals.lazy_functions import pearson_corr
from polars.internals.lazy_functions import quantile
from polars.internals.lazy_functions import reduce
from polars.internals.lazy_functions import repeat
from polars.internals.lazy_functions import select
from polars.internals.lazy_functions import spearman_rank_corr
from polars.internals.lazy_functions import std
from polars.internals.lazy_functions import struct
from polars.internals.lazy_functions import sum
from polars.internals.lazy_functions import tail
from polars.internals.lazy_functions import var
from polars.internals.lazyframe import LazyFrame

# TODO: remove need for wrap_s
from polars.internals.series import wrap_s  # noqa: F401
from polars.internals.series.series import Series
from polars.internals.sql import SQLContext
from polars.internals.whenthen import when
from polars.io import read_avro
from polars.io import read_csv
from polars.io import read_csv_batched
from polars.io import read_database
from polars.io import read_delta
from polars.io import read_excel
from polars.io import read_ipc
from polars.io import read_json
from polars.io import read_ndjson
from polars.io import read_parquet
from polars.io import read_sql
from polars.io import scan_csv
from polars.io import scan_delta
from polars.io import scan_ds
from polars.io import scan_ipc
from polars.io import scan_ndjson
from polars.io import scan_parquet
from polars.io import scan_pyarrow_dataset
from polars.string_cache import StringCache
from polars.string_cache import toggle_string_cache
from polars.string_cache import using_string_cache
from polars.utils import build_info
from polars.utils import get_idx_type
from polars.utils import get_index_type
from polars.utils import show_versions
from polars.utils import threadpool_size
from polars.utils.polars_version import get_polars_version as _get_polars_version

__version__: str = _get_polars_version()
del _get_polars_version

__all__ = [
    "api",
    "exceptions",
    # exceptions/errors
    "ArrowError",
    "ColumnNotFoundError",
    "ComputeError",
    "DuplicateError",
    "InvalidOperationError",
    "NoDataError",
    "PanicException",
    "SchemaError",
    "SchemaFieldNotFoundError",
    "ShapeError",
    "StructFieldNotFoundError",
    # core classes
    "DataFrame",
    "Expr",
    "LazyFrame",
    "Series",
    # polars.datatypes
    "Binary",
    "Boolean",
    "Categorical",
    "DataType",
    "Date",
    "Datetime",
    "Decimal",
    "Duration",
    "Field",
    "Float32",
    "Float64",
    "Int16",
    "Int32",
    "Int64",
    "Int8",
    "List",
    "Null",
    "Object",
    "PolarsDataType",
    "Struct",
    "Time",
    "UInt16",
    "UInt32",
    "UInt64",
    "UInt8",
    "Unknown",
    "Utf8",
    # polars.datatypes: dtype groups
    "DATETIME_DTYPES",
    "DURATION_DTYPES",
    "FLOAT_DTYPES",
    "INTEGER_DTYPES",
    "NUMERIC_DTYPES",
    "TEMPORAL_DTYPES",
    # polars.io
    "read_avro",
    "read_csv",
    "read_csv_batched",
    "read_database",
    "read_delta",
    "read_excel",
    "read_ipc",
    "read_ipc_schema",
    "read_json",
    "read_ndjson",
    "read_parquet",
    "read_parquet_schema",
    "read_sql",
    "scan_csv",
    "scan_delta",
    "scan_ds",
    "scan_ipc",
    "scan_ndjson",
    "scan_parquet",
    "scan_pyarrow_dataset",
    # polars.stringcache
    "StringCache",
    "toggle_string_cache",
    "using_string_cache",
    # polars.config
    "Config",
    # polars.internals.whenthen
    "when",
    # polars.internals.functions
    "align_frames",
    "arg_where",
    "concat",
    "cut",
    "date_range",
    "element",
    "get_dummies",
    "ones",
    "repeat",
    "zeros",
    # polars.internals.lazy_functions
    "all",
    "any",
    "apply",
    "arange",
    "arg_sort_by",
    "argsort_by",
    "avg",
    "coalesce",
    "col",
    "collect_all",
    "concat_list",
    "concat_str",
    "corr",
    "count",
    "cov",
    "cumfold",
    "cumreduce",
    "cumsum",
    "date",  # named date_, see import above
    "datetime",  # named datetime_, see import above
    "duration",
    "exclude",
    "first",
    "fold",
    "format",
    "from_epoch",
    "groups",
    "head",
    "last",
    "list",  # named list_, see import above
    "lit",
    "map",
    "max",
    "mean",
    "median",
    "min",
    "n_unique",
    "pearson_corr",
    "quantile",
    "reduce",
    "select",
    "spearman_rank_corr",
    "std",
    "struct",
    "sum",
    "tail",
    "var",
    "var",
    # polars.convert
    "from_arrow",
    "from_dataframe",
    "from_dict",
    "from_dicts",
    "from_numpy",
    "from_pandas",
    "from_records",
    # sql
    "SQLContext",
    # utils
    "build_info",
    "get_idx_type",
    "get_index_type",
    "show_versions",
    "threadpool_size",
]

os.environ["POLARS_ALLOW_EXTENSION"] = "true"
