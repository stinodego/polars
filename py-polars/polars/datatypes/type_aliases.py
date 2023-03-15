from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal
from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import Union

if TYPE_CHECKING:
    import sys

    import polars.datatypes

    if sys.version_info >= (3, 10):
        from typing import TypeAlias
    else:
        from typing_extensions import TypeAlias

# note: defined this way as some types can have instances that
# act as specialisations (eg: "List" and "List[Int32]")
PolarsDataType: TypeAlias = Union[
    "polars.datatypes.DataTypeClass",
    "polars.datatypes.DataType",
]
PolarsTemporalType: TypeAlias = Union[
    Type["polars.datatypes.TemporalType"],
    "polars.datatypes.TemporalType",
]
OneOrMoreDataTypes: TypeAlias = Union[PolarsDataType, Iterable[PolarsDataType]]
PythonDataType: TypeAlias = Union[
    Type[int],
    Type[float],
    Type[bool],
    Type[str],
    Type[date],
    Type[time],
    Type[datetime],
    Type[timedelta],
    Type[List[Any]],
    Type[Tuple[Any, ...]],
    Type[bytes],
    Type[Decimal],
    Type[None],
]

SchemaDefinition: TypeAlias = Union[
    Sequence[str],
    Mapping[str, Union[PolarsDataType, PythonDataType]],
    Sequence[Union[str, Tuple[str, Union[PolarsDataType, PythonDataType, None]]]],
]
SchemaDict: TypeAlias = Mapping[str, PolarsDataType]
