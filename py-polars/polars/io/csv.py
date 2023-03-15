from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import BinaryIO
from typing import Callable
from typing import Mapping
from typing import Sequence
from typing import TextIO
from typing import cast

import polars.internals as pli
from polars.convert import from_arrow
from polars.datatypes import N_INFER_DEFAULT
from polars.datatypes import Utf8
from polars.internals import DataFrame
from polars.internals import LazyFrame
from polars.internals.batched import BatchedCsvReader
from polars.internals.io import _prepare_file_arg
from polars.utils.decorators import deprecate_nonkeyword_arguments
from polars.utils.decorators import deprecated_alias
from polars.utils.various import handle_projection_columns
from polars.utils.various import normalise_filepath

if TYPE_CHECKING:
    from io import BytesIO

    from polars.datatypes import PolarsDataType
    from polars.datatypes import SchemaDict
    from polars.internals.type_aliases import CsvEncoding


@deprecate_nonkeyword_arguments()
@deprecated_alias(file="source", sep="separator", parse_dates="try_parse_dates")
def read_csv(
    source: str | TextIO | BytesIO | Path | BinaryIO | bytes,
    has_header: bool = True,
    columns: Sequence[int] | Sequence[str] | None = None,
    new_columns: list[str] | None = None,
    separator: str = ",",
    comment_char: str | None = None,
    quote_char: str | None = r'"',
    skip_rows: int = 0,
    dtypes: Mapping[str, PolarsDataType] | list[PolarsDataType] | None = None,
    null_values: str | list[str] | dict[str, str] | None = None,
    missing_utf8_is_empty_string: bool = False,
    ignore_errors: bool = False,
    try_parse_dates: bool = False,
    n_threads: int | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
    batch_size: int = 8192,
    n_rows: int | None = None,
    encoding: CsvEncoding | str = "utf8",
    low_memory: bool = False,
    rechunk: bool = True,
    use_pyarrow: bool = False,
    storage_options: dict[str, Any] | None = None,
    skip_rows_after_header: int = 0,
    row_count_name: str | None = None,
    row_count_offset: int = 0,
    sample_size: int = 1024,
    eol_char: str = "\n",
) -> DataFrame:
    """
    Read a CSV file into a DataFrame.

    Notes
    -----
    This operation defaults to a `rechunk` operation at the end, meaning that
    all data will be stored continuously in memory.
    Set `rechunk=False` if you are benchmarking the csv-reader. A `rechunk` is
    an expensive operation.

    Parameters
    ----------
    source
        Path to a file or a file-like object.
        By file-like object, we refer to objects with a ``read()``
        method, such as a file handler (e.g. via builtin ``open``
        function) or ``StringIO`` or ``BytesIO``.
        If ``fsspec`` is installed, it will be used to open remote
        files.
    has_header
        Indicate if the first row of dataset is a header or not.
        If set to False, column names will be autogenerated in the
        following format: ``column_x``, with ``x`` being an
        enumeration over every column in the dataset starting at 1.
    columns
        Columns to select. Accepts a list of column indices (starting
        at zero) or a list of column names.
    new_columns
        Rename columns right after parsing the CSV file. If the given
        list is shorter than the width of the DataFrame the remaining
        columns will have their original name.
    separator
        Single byte character to use as delimiter in the file.
    comment_char
        Single byte character that indicates the start of a comment line,
        for instance ``#``.
    quote_char
        Single byte character used for csv quoting, default = ``"``.
        Set to None to turn off special handling and escaping of quotes.
    skip_rows
        Start reading after ``skip_rows`` lines.
    dtypes
        Overwrite dtypes for specific or all columns during schema inference.
    null_values
        Values to interpret as null values. You can provide a:

        - ``str``: All values equal to this string will be null.
        - ``List[str]``: All values equal to any string in this list will be null.
        - ``Dict[str, str]``: A dictionary that maps column name to a
          null value string.
    missing_utf8_is_empty_string
        By default a missing value is considered to be null; if you would prefer missing
        utf8 values to be treated as the empty string you can set this param True.
    ignore_errors
        Try to keep reading lines if some lines yield errors.
        Before using this option, try to increase the number of lines used for schema
        inference with e.g ```infer_schema_length=10000`` or override automatic dtype
        inference for specific columns with the ``dtypes`` option or use
        ``infer_schema_length=0`` to read all columns as ``pl.Utf8`` to check which
        values might cause an issue.
    try_parse_dates
        Try to automatically parse dates. Most ISO8601-like time zone naive formats can
        be inferred, as well as a handful of others. If this does not succeed,
        the column remains of data type ``pl.Utf8``.
        If ``use_pyarrow=True``, dates will always be parsed.
    n_threads
        Number of threads to use in csv parsing.
        Defaults to the number of physical cpu's of your system.
    infer_schema_length
        Maximum number of lines to read to infer schema.
        If schema is inferred wrongly (e.g. as ``pl.Int64`` instead of ``pl.Float64``),
        try to increase the number of lines used to infer the schema or override
        inferred dtype for those columns with ``dtypes``.
        If set to 0, all columns will be read as ``pl.Utf8``.
        If set to ``None``, a full table scan will be done (slow).
    batch_size
        Number of lines to read into the buffer at once.
        Modify this to change performance.
    n_rows
        Stop reading from CSV file after reading ``n_rows``.
        During multi-threaded parsing, an upper bound of ``n_rows``
        rows cannot be guaranteed.
    encoding : {'utf8', 'utf8-lossy', ...}
        Lossy means that invalid utf8 values are replaced with ``�``
        characters. When using other encodings than ``utf8`` or
        ``utf8-lossy``, the input is first decoded im memory with
        python. Defaults to ``utf8``.
    low_memory
        Reduce memory usage at expense of performance.
    rechunk
        Make sure that all columns are contiguous in memory by
        aggregating the chunks into a single array.
    use_pyarrow
        Try to use pyarrow's native CSV parser. This will always
        parse dates, even if ``try_parse_dates=False``.
        This is not always possible. The set of arguments given to
        this function determines if it is possible to use pyarrow's
        native parser. Note that pyarrow and polars may have a
        different strategy regarding type inference.
    storage_options
        Extra options that make sense for ``fsspec.open()`` or a
        particular storage connection.
        e.g. host, port, username, password, etc.
    skip_rows_after_header
        Skip this number of rows when the header is parsed.
    row_count_name
        If not None, this will insert a row count column with the given name into
        the DataFrame.
    row_count_offset
        Offset to start the row_count column (only used if the name is set).
    sample_size
        Set the sample size. This is used to sample statistics to estimate the
        allocation needed.
    eol_char
        Single byte end of line character.

    Returns
    -------
    DataFrame

    See Also
    --------
    scan_csv : Lazily read from a CSV file or multiple files via glob patterns.

    """
    _check_arg_is_1byte("separator", separator, False)
    _check_arg_is_1byte("comment_char", comment_char, False)
    _check_arg_is_1byte("quote_char", quote_char, True)
    _check_arg_is_1byte("eol_char", eol_char, False)

    projection, columns = handle_projection_columns(columns)

    if isinstance(source, bytes) and len(source) == 0:
        raise ValueError("Empty bytes data provided.")

    storage_options = storage_options or {}

    if columns and not has_header:
        for column in columns:
            if not column.startswith("column_"):
                raise ValueError(
                    'Specified column names do not start with "column_", '
                    "but autogenerated header names were requested."
                )

    if (
        use_pyarrow
        and dtypes is None
        and n_rows is None
        and n_threads is None
        and not low_memory
        and null_values is None
    ):
        include_columns: Sequence[str] | None = None

        if columns:
            if not has_header:
                # Convert 'column_1', 'column_2', ... column names to 'f0', 'f1', ...
                # column names for pyarrow, if CSV file does not contain a header.
                include_columns = [f"f{int(column[7:]) - 1}" for column in columns]
            else:
                include_columns = columns

        if not columns and projection:
            # Convert column indices from projection to 'f0', 'f1', ... column names
            # for pyarrow.
            include_columns = [f"f{column_idx}" for column_idx in projection]

        with _prepare_file_arg(
            source, encoding=None, use_pyarrow=True, **storage_options
        ) as data:
            import pyarrow as pa
            import pyarrow.csv

            tbl = pa.csv.read_csv(
                data,
                pa.csv.ReadOptions(
                    skip_rows=skip_rows,
                    autogenerate_column_names=not has_header,
                    encoding=encoding,
                ),
                pa.csv.ParseOptions(
                    delimiter=separator,
                    quote_char=quote_char if quote_char else False,
                    double_quote=quote_char is not None and quote_char == '"',
                ),
                pa.csv.ConvertOptions(
                    column_types=None,
                    include_columns=include_columns,
                    include_missing_columns=ignore_errors,
                ),
            )

        if not has_header:
            # Rename 'f0', 'f1', ... columns names autogenerated by pyarrow
            # to 'column_1', 'column_2', ...
            tbl = tbl.rename_columns(
                [f"column_{int(column[1:]) + 1}" for column in tbl.column_names]
            )

        df = cast(DataFrame, from_arrow(tbl, rechunk=rechunk))
        if new_columns:
            return pli._update_columns(df, new_columns)
        return df

    if projection and dtypes and isinstance(dtypes, list):
        if len(projection) < len(dtypes):
            raise ValueError(
                "More dtypes overrides are specified than there are selected columns."
            )

        # Fix list of dtypes when used together with projection as polars CSV reader
        # wants a list of dtypes for the x first columns before it does the projection.
        dtypes_list: list[PolarsDataType] = [Utf8] * (max(projection) + 1)

        for idx, column_idx in enumerate(projection):
            if idx < len(dtypes):
                dtypes_list[column_idx] = dtypes[idx]

        dtypes = dtypes_list

    if columns and dtypes and isinstance(dtypes, list):
        if len(columns) < len(dtypes):
            raise ValueError(
                "More dtypes overrides are specified than there are selected columns."
            )

        # Map list of dtypes when used together with selected columns as a dtypes dict
        # so the dtypes are applied to the correct column instead of the first x
        # columns.
        dtypes = {column: dtype for column, dtype in zip(columns, dtypes)}

    if new_columns and dtypes and isinstance(dtypes, dict):
        current_columns = None

        # As new column names are not available yet while parsing the CSV file, rename
        # column names in dtypes to old names (if possible) so they can be used during
        # CSV parsing.
        if columns:
            if len(columns) < len(new_columns):
                raise ValueError(
                    "More new column names are specified than there are selected"
                    " columns."
                )

            # Get column names of requested columns.
            current_columns = columns[0 : len(new_columns)]
        elif not has_header:
            # When there are no header, column names are autogenerated (and known).

            if projection:
                if columns and len(columns) < len(new_columns):
                    raise ValueError(
                        "More new column names are specified than there are selected"
                        " columns."
                    )
                # Convert column indices from projection to 'column_1', 'column_2', ...
                # column names.
                current_columns = [
                    f"column_{column_idx + 1}" for column_idx in projection
                ]
            else:
                # Generate autogenerated 'column_1', 'column_2', ... column names for
                # new column names.
                current_columns = [
                    f"column_{column_idx}"
                    for column_idx in range(1, len(new_columns) + 1)
                ]
        else:
            # When a header is present, column names are not known yet.

            if len(dtypes) <= len(new_columns):
                # If dtypes dictionary contains less or same amount of values than new
                # column names a list of dtypes can be created if all listed column
                # names in dtypes dictionary appear in the first consecutive new column
                # names.
                dtype_list = [
                    dtypes[new_column_name]
                    for new_column_name in new_columns[0 : len(dtypes)]
                    if new_column_name in dtypes
                ]

                if len(dtype_list) == len(dtypes):
                    dtypes = dtype_list

        if current_columns and isinstance(dtypes, dict):
            new_to_current = {
                new_column: current_column
                for new_column, current_column in zip(new_columns, current_columns)
            }
            # Change new column names to current column names in dtype.
            dtypes = {
                new_to_current.get(column_name, column_name): column_dtype
                for column_name, column_dtype in dtypes.items()
            }

    with _prepare_file_arg(
        source, encoding=encoding, use_pyarrow=False, **storage_options
    ) as data:
        df = DataFrame._read_csv(
            data,
            has_header=has_header,
            columns=columns if columns else projection,
            separator=separator,
            comment_char=comment_char,
            quote_char=quote_char,
            skip_rows=skip_rows,
            dtypes=dtypes,
            null_values=null_values,
            missing_utf8_is_empty_string=missing_utf8_is_empty_string,
            ignore_errors=ignore_errors,
            try_parse_dates=try_parse_dates,
            n_threads=n_threads,
            infer_schema_length=infer_schema_length,
            batch_size=batch_size,
            n_rows=n_rows,
            encoding=encoding if encoding == "utf8-lossy" else "utf8",
            low_memory=low_memory,
            rechunk=rechunk,
            skip_rows_after_header=skip_rows_after_header,
            row_count_name=row_count_name,
            row_count_offset=row_count_offset,
            sample_size=sample_size,
            eol_char=eol_char,
        )

    if new_columns:
        return pli._update_columns(df, new_columns)
    return df


@deprecate_nonkeyword_arguments()
@deprecated_alias(file="source", sep="separator")
def read_csv_batched(
    source: str | Path,
    has_header: bool = True,
    columns: Sequence[int] | Sequence[str] | None = None,
    new_columns: list[str] | None = None,
    separator: str = ",",
    comment_char: str | None = None,
    quote_char: str | None = r'"',
    skip_rows: int = 0,
    dtypes: Mapping[str, PolarsDataType] | list[PolarsDataType] | None = None,
    null_values: str | list[str] | dict[str, str] | None = None,
    missing_utf8_is_empty_string: bool = False,
    ignore_errors: bool = False,
    try_parse_dates: bool = False,
    n_threads: int | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
    batch_size: int = 50_000,
    n_rows: int | None = None,
    encoding: CsvEncoding | str = "utf8",
    low_memory: bool = False,
    rechunk: bool = True,
    skip_rows_after_header: int = 0,
    row_count_name: str | None = None,
    row_count_offset: int = 0,
    sample_size: int = 1024,
    eol_char: str = "\n",
) -> BatchedCsvReader:
    """
    Read a CSV file in batches.

    Upon creation of the ``BatchedCsvReader``, Polars will gather statistics and
    determine the file chunks. After that, work will only be done if ``next_batches``
    is called.

    Parameters
    ----------
    source
        Path to a file or a file-like object.
        By file-like object, we refer to objects with a ``read()``
        method, such as a file handler (e.g. via builtin ``open``
        function) or ``StringIO`` or ``BytesIO``.
        If ``fsspec`` is installed, it will be used to open remote
        files.
    has_header
        Indicate if the first row of dataset is a header or not.
        If set to False, column names will be autogenerated in the
        following format: ``column_x``, with ``x`` being an
        enumeration over every column in the dataset starting at 1.
    columns
        Columns to select. Accepts a list of column indices (starting
        at zero) or a list of column names.
    new_columns
        Rename columns right after parsing the CSV file. If the given
        list is shorter than the width of the DataFrame the remaining
        columns will have their original name.
    separator
        Single byte character to use as delimiter in the file.
    comment_char
        Single byte character that indicates the start of a comment line,
        for instance ``#``.
    quote_char
        Single byte character used for csv quoting, default = ``"``.
        Set to None to turn off special handling and escaping of quotes.
    skip_rows
        Start reading after ``skip_rows`` lines.
    dtypes
        Overwrite dtypes during inference.
    null_values
        Values to interpret as null values. You can provide a:

        - ``str``: All values equal to this string will be null.
        - ``List[str]``: All values equal to any string in this list will be null.
        - ``Dict[str, str]``: A dictionary that maps column name to a
          null value string.
    missing_utf8_is_empty_string
        By default a missing value is considered to be null; if you would prefer missing
        utf8 values to be treated as the empty string you can set this param True.
    ignore_errors
        Try to keep reading lines if some lines yield errors.
        First try ``infer_schema_length=0`` to read all columns as
        ``pl.Utf8`` to check which values might cause an issue.
    try_parse_dates
        Try to automatically parse dates. Most ISO8601-like time zone naive formats can
        be inferred, as well as a handful of others. If this does not succeed,
        the column remains of data type ``pl.Utf8``.
    n_threads
        Number of threads to use in csv parsing.
        Defaults to the number of physical cpu's of your system.
    infer_schema_length
        Maximum number of lines to read to infer schema.
        If set to 0, all columns will be read as ``pl.Utf8``.
        If set to ``None``, a full table scan will be done (slow).
    batch_size
        Number of lines to read into the buffer at once.

        Modify this to change performance.
    n_rows
        Stop reading from CSV file after reading ``n_rows``.
        During multi-threaded parsing, an upper bound of ``n_rows``
        rows cannot be guaranteed.
    encoding : {'utf8', 'utf8-lossy', ...}
        Lossy means that invalid utf8 values are replaced with ``�``
        characters. When using other encodings than ``utf8`` or
        ``utf8-lossy``, the input is first decoded im memory with
        python. Defaults to ``utf8``.
    low_memory
        Reduce memory usage at expense of performance.
    rechunk
        Make sure that all columns are contiguous in memory by
        aggregating the chunks into a single array.
    skip_rows_after_header
        Skip this number of rows when the header is parsed.
    row_count_name
        If not None, this will insert a row count column with the given name into
        the DataFrame.
    row_count_offset
        Offset to start the row_count column (only used if the name is set).
    sample_size
        Set the sample size. This is used to sample statistics to estimate the
        allocation needed.
    eol_char
        Single byte end of line character.

    Returns
    -------
    BatchedCsvReader

    See Also
    --------
    scan_csv : Lazily read from a CSV file or multiple files via glob patterns.

    Examples
    --------
    >>> reader = pl.read_csv_batched(
    ...     "./tpch/tables_scale_100/lineitem.tbl", separator="|", try_parse_dates=True
    ... )  # doctest: +SKIP
    >>> batches = reader.next_batches(5)  # doctest: +SKIP
    >>> for df in batches:  # doctest: +SKIP
    ...     print(df)
    ...

    Read big CSV file in batches and write a CSV file for each "group" of interest.

    >>> seen_groups = set()
    >>> reader = pl.read_csv_batched("big_file.csv")  # doctest: +SKIP
    >>> batches = reader.next_batches(100)  # doctest: +SKIP

    >>> while batches:  # doctest: +SKIP
    ...     df_current_batches = pl.concat(batches)
    ...     partition_dfs = df_current_batches.partition_by("group", as_dict=True)
    ...
    ...     for group, df in partition_dfs.items():
    ...         if group in seen_groups:
    ...             with open(f"./data/{group}.csv", "a") as fh:
    ...                 fh.write(df.write_csv(file=None, has_header=False))
    ...         else:
    ...             df.write_csv(file=f"./data/{group}.csv", has_header=True)
    ...         seen_groups.add(group)
    ...
    ...     batches = reader.next_batches(100)
    ...

    """
    projection, columns = handle_projection_columns(columns)

    if isinstance(source, bytes) and len(source) == 0:
        raise ValueError("Empty bytes data provided.")

    if columns and not has_header:
        for column in columns:
            if not column.startswith("column_"):
                raise ValueError(
                    'Specified column names do not start with "column_", '
                    "but autogenerated header names were requested."
                )

    if projection and dtypes and isinstance(dtypes, list):
        if len(projection) < len(dtypes):
            raise ValueError(
                "More dtypes overrides are specified than there are selected columns."
            )

        # Fix list of dtypes when used together with projection as polars CSV reader
        # wants a list of dtypes for the x first columns before it does the projection.
        dtypes_list: list[PolarsDataType] = [Utf8] * (max(projection) + 1)

        for idx, column_idx in enumerate(projection):
            if idx < len(dtypes):
                dtypes_list[column_idx] = dtypes[idx]

        dtypes = dtypes_list

    if columns and dtypes and isinstance(dtypes, list):
        if len(columns) < len(dtypes):
            raise ValueError(
                "More dtypes overrides are specified than there are selected columns."
            )

        # Map list of dtypes when used together with selected columns as a dtypes dict
        # so the dtypes are applied to the correct column instead of the first x
        # columns.
        dtypes = {column: dtype for column, dtype in zip(columns, dtypes)}

    if new_columns and dtypes and isinstance(dtypes, dict):
        current_columns = None

        # As new column names are not available yet while parsing the CSV file, rename
        # column names in dtypes to old names (if possible) so they can be used during
        # CSV parsing.
        if columns:
            if len(columns) < len(new_columns):
                raise ValueError(
                    "More new column names are specified than there are selected"
                    " columns."
                )

            # Get column names of requested columns.
            current_columns = columns[0 : len(new_columns)]
        elif not has_header:
            # When there are no header, column names are autogenerated (and known).

            if projection:
                if columns and len(columns) < len(new_columns):
                    raise ValueError(
                        "More new column names are specified than there are selected"
                        " columns."
                    )
                # Convert column indices from projection to 'column_1', 'column_2', ...
                # column names.
                current_columns = [
                    f"column_{column_idx + 1}" for column_idx in projection
                ]
            else:
                # Generate autogenerated 'column_1', 'column_2', ... column names for
                # new column names.
                current_columns = [
                    f"column_{column_idx}"
                    for column_idx in range(1, len(new_columns) + 1)
                ]
        else:
            # When a header is present, column names are not known yet.

            if len(dtypes) <= len(new_columns):
                # If dtypes dictionary contains less or same amount of values than new
                # column names a list of dtypes can be created if all listed column
                # names in dtypes dictionary appear in the first consecutive new column
                # names.
                dtype_list = [
                    dtypes[new_column_name]
                    for new_column_name in new_columns[0 : len(dtypes)]
                    if new_column_name in dtypes
                ]

                if len(dtype_list) == len(dtypes):
                    dtypes = dtype_list

        if current_columns and isinstance(dtypes, dict):
            new_to_current = {
                new_column: current_column
                for new_column, current_column in zip(new_columns, current_columns)
            }
            # Change new column names to current column names in dtype.
            dtypes = {
                new_to_current.get(column_name, column_name): column_dtype
                for column_name, column_dtype in dtypes.items()
            }

    return BatchedCsvReader(
        source,
        has_header=has_header,
        columns=columns if columns else projection,
        separator=separator,
        comment_char=comment_char,
        quote_char=quote_char,
        skip_rows=skip_rows,
        dtypes=dtypes,
        null_values=null_values,
        missing_utf8_is_empty_string=missing_utf8_is_empty_string,
        ignore_errors=ignore_errors,
        try_parse_dates=try_parse_dates,
        n_threads=n_threads,
        infer_schema_length=infer_schema_length,
        batch_size=batch_size,
        n_rows=n_rows,
        encoding=encoding if encoding == "utf8-lossy" else "utf8",
        low_memory=low_memory,
        rechunk=rechunk,
        skip_rows_after_header=skip_rows_after_header,
        row_count_name=row_count_name,
        row_count_offset=row_count_offset,
        sample_size=sample_size,
        eol_char=eol_char,
        new_columns=new_columns,
    )


@deprecate_nonkeyword_arguments()
@deprecated_alias(file="source", sep="separator", parse_dates="try_parse_dates")
def scan_csv(
    source: str | Path,
    has_header: bool = True,
    separator: str = ",",
    comment_char: str | None = None,
    quote_char: str | None = r'"',
    skip_rows: int = 0,
    dtypes: SchemaDict | None = None,
    null_values: str | list[str] | dict[str, str] | None = None,
    missing_utf8_is_empty_string: bool = False,
    ignore_errors: bool = False,
    cache: bool = True,
    with_column_names: Callable[[list[str]], list[str]] | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
    n_rows: int | None = None,
    encoding: CsvEncoding = "utf8",
    low_memory: bool = False,
    rechunk: bool = True,
    skip_rows_after_header: int = 0,
    row_count_name: str | None = None,
    row_count_offset: int = 0,
    try_parse_dates: bool = False,
    eol_char: str = "\n",
) -> LazyFrame:
    """
    Lazily read from a CSV file or multiple files via glob patterns.

    This allows the query optimizer to push down predicates and
    projections to the scan level, thereby potentially reducing
    memory overhead.

    Parameters
    ----------
    source
        Path to a file.
    has_header
        Indicate if the first row of dataset is a header or not.
        If set to False, column names will be autogenerated in the
        following format: ``column_x``, with ``x`` being an
        enumeration over every column in the dataset starting at 1.
    separator
        Single byte character to use as delimiter in the file.
    comment_char
        Single byte character that indicates the start of a comment line,
        for instance ``#``.
    quote_char
        Single byte character used for csv quoting, default = ``"``.
        Set to None to turn off special handling and escaping of quotes.
    skip_rows
        Start reading after ``skip_rows`` lines. The header will be parsed at this
        offset.
    dtypes
        Overwrite dtypes during inference.
    null_values
        Values to interpret as null values. You can provide a:

        - ``str``: All values equal to this string will be null.
        - ``List[str]``: All values equal to any string in this list will be null.
        - ``Dict[str, str]``: A dictionary that maps column name to a
          null value string.
    missing_utf8_is_empty_string
        By default a missing value is considered to be null; if you would prefer missing
        utf8 values to be treated as the empty string you can set this param True.
    ignore_errors
        Try to keep reading lines if some lines yield errors.
        First try ``infer_schema_length=0`` to read all columns as
        ``pl.Utf8`` to check which values might cause an issue.
    cache
        Cache the result after reading.
    with_column_names
        Apply a function over the column names.
        This can be used to update a schema just in time, thus before
        scanning.
    infer_schema_length
        Maximum number of lines to read to infer schema.
        If set to 0, all columns will be read as ``pl.Utf8``.
        If set to ``None``, a full table scan will be done (slow).
    n_rows
        Stop reading from CSV file after reading ``n_rows``.
    encoding : {'utf8', 'utf8-lossy'}
        Lossy means that invalid utf8 values are replaced with ``�``
        characters. Defaults to "utf8".
    low_memory
        Reduce memory usage in expense of performance.
    rechunk
        Reallocate to contiguous memory when all chunks/ files are parsed.
    skip_rows_after_header
        Skip this number of rows when the header is parsed.
    row_count_name
        If not None, this will insert a row count column with the given name into
        the DataFrame.
    row_count_offset
        Offset to start the row_count column (only used if the name is set).
    try_parse_dates
        Try to automatically parse dates. Most ISO8601-like time zone naive formats can
        be inferred, as well as a handful of others. If this does not succeed,
        the column remains of data type ``pl.Utf8``.
    eol_char
        Single byte end of line character

    Returns
    -------
    LazyFrame

    See Also
    --------
    read_csv : Read a CSV file into a DataFrame.

    Examples
    --------
    >>> import pathlib
    >>>
    >>> (
    ...     pl.scan_csv("my_long_file.csv")  # lazy, doesn't do a thing
    ...     .select(
    ...         ["a", "c"]
    ...     )  # select only 2 columns (other columns will not be read)
    ...     .filter(
    ...         pl.col("a") > 10
    ...     )  # the filter is pushed down the scan, so less data is read into memory
    ...     .fetch(100)  # pushed a limit of 100 rows to the scan level
    ... )  # doctest: +SKIP

    We can use ``with_column_names`` to modify the header before scanning:

    >>> df = pl.DataFrame(
    ...     {"BrEeZaH": [1, 2, 3, 4], "LaNgUaGe": ["is", "terrible", "to", "read"]}
    ... )
    >>> path: pathlib.Path = dirpath / "mydf.csv"
    >>> df.write_csv(path)
    >>> pl.scan_csv(
    ...     path, with_column_names=lambda cols: [col.lower() for col in cols]
    ... ).fetch()
    shape: (4, 2)
    ┌─────────┬──────────┐
    │ breezah ┆ language │
    │ ---     ┆ ---      │
    │ i64     ┆ str      │
    ╞═════════╪══════════╡
    │ 1       ┆ is       │
    │ 2       ┆ terrible │
    │ 3       ┆ to       │
    │ 4       ┆ read     │
    └─────────┴──────────┘

    """
    _check_arg_is_1byte("separator", separator, False)
    _check_arg_is_1byte("comment_char", comment_char, False)
    _check_arg_is_1byte("quote_char", quote_char, True)

    if isinstance(source, (str, Path)):
        source = normalise_filepath(source)

    return LazyFrame._scan_csv(
        source,
        has_header=has_header,
        separator=separator,
        comment_char=comment_char,
        quote_char=quote_char,
        skip_rows=skip_rows,
        dtypes=dtypes,
        null_values=null_values,
        missing_utf8_is_empty_string=missing_utf8_is_empty_string,
        ignore_errors=ignore_errors,
        cache=cache,
        with_column_names=with_column_names,
        infer_schema_length=infer_schema_length,
        n_rows=n_rows,
        low_memory=low_memory,
        rechunk=rechunk,
        skip_rows_after_header=skip_rows_after_header,
        encoding=encoding,
        row_count_name=row_count_name,
        row_count_offset=row_count_offset,
        try_parse_dates=try_parse_dates,
        eol_char=eol_char,
    )


def _check_arg_is_1byte(
    arg_name: str, arg: str | None, can_be_empty: bool = False
) -> None:
    if isinstance(arg, str):
        arg_byte_length = len(arg.encode("utf-8"))
        if can_be_empty:
            if arg_byte_length > 1:
                raise ValueError(
                    f'{arg_name}="{arg}" should be a single byte character or empty,'
                    f" but is {arg_byte_length} bytes long."
                )
        elif arg_byte_length != 1:
            raise ValueError(
                f'{arg_name}="{arg}" should be a single byte character, but is'
                f" {arg_byte_length} bytes long."
            )
