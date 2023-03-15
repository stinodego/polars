from __future__ import annotations

from typing import TYPE_CHECKING

from polars.datatypes import Date
from polars.datatypes import Datetime
from polars.datatypes import Decimal
from polars.datatypes import Duration
from polars.datatypes import Float32
from polars.datatypes import Float64
from polars.datatypes import Int8
from polars.datatypes import Int16
from polars.datatypes import Int32
from polars.datatypes import Int64
from polars.datatypes import Time
from polars.datatypes import UInt8
from polars.datatypes import UInt16
from polars.datatypes import UInt32
from polars.datatypes import UInt64

if TYPE_CHECKING:
    from polars.datatypes.type_aliases import PolarsDataType
    from polars.internals.type_aliases import TimeUnit

DTYPE_TEMPORAL_UNITS: frozenset[TimeUnit] = frozenset(["ns", "us", "ms"])
DATETIME_DTYPES: frozenset[PolarsDataType] = frozenset(
    [
        # TODO: ideally need a mechanism to wildcard timezones here too
        Datetime("ms"),
        Datetime("us"),
        Datetime("ns"),
    ]
)
DURATION_DTYPES: frozenset[PolarsDataType] = frozenset(
    [
        Duration("ms"),
        Duration("us"),
        Duration("ns"),
    ]
)
TEMPORAL_DTYPES: frozenset[PolarsDataType] = (
    frozenset([Date, Time]) | DATETIME_DTYPES | DURATION_DTYPES
)
INTEGER_DTYPES: frozenset[PolarsDataType] = frozenset(
    [
        UInt8,
        UInt16,
        UInt32,
        UInt64,
        Int8,
        Int16,
        Int32,
        Int64,
    ]
)
FLOAT_DTYPES: frozenset[PolarsDataType] = frozenset([Float32, Float64])
NUMERIC_DTYPES: frozenset[PolarsDataType] = (
    FLOAT_DTYPES | INTEGER_DTYPES | frozenset([Decimal])
)

# number of rows to scan by default when inferring datatypes
N_INFER_DEFAULT = 100
