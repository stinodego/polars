"""
Core Polars functionality.

The modules within `polars.internals` are interdependent. To prevent cyclical imports,
they all import from each other via this __init__ file using
`import polars.internals as pli`. The imports below are being shared across this module.
"""
from polars.internals.anonymous_scan import _deser_and_exec
from polars.internals.anonymous_scan import _scan_ipc_fsspec
from polars.internals.anonymous_scan import _scan_parquet_fsspec
from polars.internals.anonymous_scan import _scan_pyarrow_dataset
from polars.internals.batched import BatchedCsvReader
from polars.internals.dataframe import DataFrame
from polars.internals.dataframe import wrap_df
from polars.internals.expr import Expr
from polars.internals.expr import expr_to_lit_or_expr
from polars.internals.expr import selection_to_pyexpr_list
from polars.internals.expr import wrap_expr
from polars.internals.functions import concat
from polars.internals.functions import date_range
from polars.internals.io import _is_local_file
from polars.internals.io import _prepare_file_arg
from polars.internals.io import _update_columns
from polars.internals.io import read_ipc_schema
from polars.internals.io import read_parquet_schema
from polars.internals.lazy_functions import all
from polars.internals.lazy_functions import arange
from polars.internals.lazy_functions import arg_sort_by
from polars.internals.lazy_functions import arg_where
from polars.internals.lazy_functions import argsort_by
from polars.internals.lazy_functions import coalesce
from polars.internals.lazy_functions import col
from polars.internals.lazy_functions import collect_all
from polars.internals.lazy_functions import concat_list
from polars.internals.lazy_functions import count
from polars.internals.lazy_functions import element
from polars.internals.lazy_functions import format
from polars.internals.lazy_functions import from_epoch
from polars.internals.lazy_functions import lit
from polars.internals.lazy_functions import select
from polars.internals.lazy_functions import struct
from polars.internals.lazyframe import LazyFrame
from polars.internals.lazyframe import wrap_ldf
from polars.internals.series import Series
from polars.internals.series import wrap_s
from polars.internals.whenthen import WhenThen
from polars.internals.whenthen import WhenThenThen
from polars.internals.whenthen import when

__all__ = [
    "DataFrame",
    "Expr",
    "LazyFrame",
    "Series",
    "all",
    "arange",
    "arg_where",
    "arg_sort_by",
    "argsort_by",
    "BatchedCsvReader",
    "coalesce",
    "col",
    "collect_all",
    "concat",
    "concat_list",
    "count",
    "date_range",
    "element",
    "expr_to_lit_or_expr",
    "format",
    "from_epoch",
    "lit",
    "read_ipc_schema",
    "read_parquet_schema",
    "select",
    "selection_to_pyexpr_list",
    "struct",
    "when",
    "wrap_df",
    "wrap_expr",
    "wrap_ldf",
    "wrap_s",
    "WhenThen",
    "WhenThenThen",
    "_deser_and_exec",
    "_is_local_file",
    "_prepare_file_arg",
    "_scan_pyarrow_dataset",
    "_scan_ipc_fsspec",
    "_scan_parquet_fsspec",
    "_update_columns",
]
