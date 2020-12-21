# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""System tests for pandas connector."""

import collections
import datetime
import decimal
import operator

import pkg_resources
import pytest
import pytz
import six

from google.cloud import bigquery
from . import helpers


bigquery_storage = pytest.importorskip(
    "google.cloud.bigquery_storage", minversion="2.0.0"
)
pandas = pytest.importorskip("pandas", minversion="0.23.0")
pyarrow = pytest.importorskip("pyarrow", minversion="1.0.0")


PANDAS_INSTALLED_VERSION = pkg_resources.get_distribution("pandas").parsed_version
PANDAS_INT64_VERSION = pkg_resources.parse_version("1.0.0")


def test_list_rows_max_results_w_bqstorage(bigquery_client, bqstorage_client):
    table_ref = bigquery.TableReference.from_string(
        "bigquery-public-data.utility_us.country_code_iso"
    )

    row_iterator = bigquery_client.list_rows(
        table_ref,
        selected_fields=[bigquery.SchemaField("country_name", "STRING")],
        max_results=100,
    )
    with pytest.warns(
        UserWarning, match="Cannot use bqstorage_client if max_results is set"
    ):
        dataframe = row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

    assert len(dataframe.index) == 100


def test_nested_table_to_dataframe(bigquery_client, dataset_id):
    from google.cloud.bigquery.job import SourceFormat
    from google.cloud.bigquery.job import WriteDisposition

    SF = bigquery.SchemaField
    schema = [
        SF("string_col", "STRING", mode="NULLABLE"),
        SF(
            "record_col",
            "RECORD",
            mode="NULLABLE",
            fields=[
                SF("nested_string", "STRING", mode="NULLABLE"),
                SF("nested_repeated", "INTEGER", mode="REPEATED"),
                SF(
                    "nested_record",
                    "RECORD",
                    mode="NULLABLE",
                    fields=[SF("nested_nested_string", "STRING", mode="NULLABLE")],
                ),
            ],
        ),
        SF("bigfloat_col", "FLOAT", mode="NULLABLE"),
        SF("smallfloat_col", "FLOAT", mode="NULLABLE"),
    ]
    record = {
        "nested_string": "another string value",
        "nested_repeated": [0, 1, 2],
        "nested_record": {"nested_nested_string": "some deep insight"},
    }
    # Load data into a temporary table, which we can then read from.
    to_insert = [
        {
            "string_col": "Some value",
            "record_col": record,
            "bigfloat_col": 3.14,
            "smallfloat_col": 2.72,
        }
    ]
    table_id = "pandas_test_nested_table_to_dataframe" + helpers.temp_suffix()
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
    job_config.source_format = SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.schema = schema
    bigquery_client.load_table_from_json(
        to_insert, f"{dataset_id}.{table_id}", job_config=job_config
    ).result()

    df = bigquery_client.list_rows(
        f"{dataset_id}.{table_id}", selected_fields=schema,
    ).to_dataframe(dtypes={"smallfloat_col": "float16"})

    assert isinstance(df, pandas.DataFrame)
    assert len(df.index) == 1  # verify the number of rows
    exp_columns = ["string_col", "record_col", "bigfloat_col", "smallfloat_col"]
    assert list(df) == exp_columns  # verify the column names
    row = df.iloc[0]
    # verify the row content
    assert row["string_col"] == "Some value"
    expected_keys = tuple(sorted(record.keys()))
    row_keys = tuple(sorted(row["record_col"].keys()))
    assert row_keys == expected_keys
    # Can't compare numpy arrays, which pyarrow encodes the embedded
    # repeated column to, so convert to list.
    assert list(row["record_col"]["nested_repeated"]) == [0, 1, 2]
    # verify that nested data can be accessed with indices/keys
    assert row["record_col"]["nested_repeated"][0] == 0
    assert (
        row["record_col"]["nested_record"]["nested_nested_string"]
        == "some deep insight"
    )
    # verify dtypes
    assert df.dtypes["bigfloat_col"].name == "float64"
    assert df.dtypes["smallfloat_col"].name == "float16"


@pytest.mark.parametrize(("create_bqstorage_client",), [(True,), (False,)])
def test_query_results_to_dataframe(bigquery_client, create_bqstorage_client):
    query = """
    SELECT id, author, time_ts, dead
    FROM `bigquery-public-data.hacker_news.comments`
    LIMIT 10
    """
    df = (
        bigquery_client.query(query)
        .result()
        .to_dataframe(create_bqstorage_client=create_bqstorage_client)
    )

    assert isinstance(df, pandas.DataFrame)
    assert len(df.index) == 10  # verify the number of rows
    column_names = ["id", "author", "time_ts", "dead"]
    assert list(df) == column_names  # verify the column names
    exp_datatypes = {
        "id": int,
        "author": six.text_type,
        "time_ts": pandas.Timestamp,
        "dead": bool,
    }
    for _, row in df.iterrows():
        for col in column_names:
            # all the schema fields are nullable, so None is acceptable
            assert row[col] is None or isinstance(row[col], exp_datatypes[col])


def test_insert_rows_from_dataframe(bigquery_client, dataset_id):
    SF = bigquery.SchemaField
    schema = [
        SF("float_col", "FLOAT", mode="REQUIRED"),
        SF("int_col", "INTEGER", mode="REQUIRED"),
        SF("bool_col", "BOOLEAN", mode="REQUIRED"),
        SF("string_col", "STRING", mode="NULLABLE"),
    ]

    dataframe = pandas.DataFrame(
        [
            {
                "float_col": 1.11,
                "bool_col": True,
                "string_col": "my string",
                "int_col": 10,
            },
            {
                "float_col": 2.22,
                "bool_col": False,
                "string_col": "another string",
                "int_col": 20,
            },
            {
                "float_col": 3.33,
                "bool_col": False,
                "string_col": "another string",
                "int_col": 30,
            },
            {
                "float_col": 4.44,
                "bool_col": True,
                "string_col": "another string",
                "int_col": 40,
            },
            {
                "float_col": 5.55,
                "bool_col": False,
                "string_col": "another string",
                "int_col": 50,
            },
            {
                "float_col": 6.66,
                "bool_col": True,
                # Include a NaN value, because pandas often uses NaN as a
                # NULL value indicator.
                "string_col": float("NaN"),
                "int_col": 60,
            },
        ]
    )

    table_id = "pandas_test_insert_rows_from_dataframe" + helpers.temp_suffix()
    table_arg = bigquery.Table(
        f"{bigquery_client.project}.{dataset_id}.{table_id}", schema=schema
    )
    table = helpers.retry_403(bigquery_client.create_table)(table_arg)

    chunk_errors = bigquery_client.insert_rows_from_dataframe(
        table, dataframe, chunk_size=3
    )
    for errors in chunk_errors:
        assert not errors

    # Use query to fetch rows instead of listing directly from the table so
    # that we get values from the streaming buffer.
    rows = list(
        bigquery_client.query(
            "SELECT * FROM `{}.{}.{}`".format(
                table.project, table.dataset_id, table.table_id
            )
        )
    )

    sorted_rows = sorted(rows, key=operator.attrgetter("int_col"))
    row_tuples = [r.values() for r in sorted_rows]
    expected = [
        tuple(None if col != col else col for col in data_row)
        for data_row in dataframe.itertuples(index=False)
    ]

    assert len(row_tuples) == len(expected)

    for row, expected_row in zip(row_tuples, expected):
        # column order does not matter
        assert len(row) == len(expected_row)


def test_load_table_from_dataframe_w_automatic_schema(bigquery_client, dataset_id):
    """Test that a DataFrame with dtypes that map well to BigQuery types
    can be uploaded without specifying a schema.

    https://github.com/googleapis/google-cloud-python/issues/9044
    """
    df_data = collections.OrderedDict(
        [
            ("bool_col", pandas.Series([True, False, True], dtype="bool")),
            (
                "ts_col",
                pandas.Series(
                    [
                        datetime.datetime(2010, 1, 2, 3, 44, 50),
                        datetime.datetime(2011, 2, 3, 14, 50, 59),
                        datetime.datetime(2012, 3, 14, 15, 16),
                    ],
                    dtype="datetime64[ns]",
                ).dt.tz_localize(pytz.utc),
            ),
            (
                "dt_col",
                pandas.Series(
                    [
                        datetime.datetime(2010, 1, 2, 3, 44, 50),
                        datetime.datetime(2011, 2, 3, 14, 50, 59),
                        datetime.datetime(2012, 3, 14, 15, 16),
                    ],
                    dtype="datetime64[ns]",
                ),
            ),
            ("float32_col", pandas.Series([1.0, 2.0, 3.0], dtype="float32")),
            ("float64_col", pandas.Series([4.0, 5.0, 6.0], dtype="float64")),
            ("int8_col", pandas.Series([-12, -11, -10], dtype="int8")),
            ("int16_col", pandas.Series([-9, -8, -7], dtype="int16")),
            ("int32_col", pandas.Series([-6, -5, -4], dtype="int32")),
            ("int64_col", pandas.Series([-3, -2, -1], dtype="int64")),
            ("uint8_col", pandas.Series([0, 1, 2], dtype="uint8")),
            ("uint16_col", pandas.Series([3, 4, 5], dtype="uint16")),
            ("uint32_col", pandas.Series([6, 7, 8], dtype="uint32")),
        ]
    )
    dataframe = pandas.DataFrame(df_data, columns=df_data.keys())
    table_id = (
        f"{bigquery_client.project}.{dataset_id}"
        ".pandas_test_load_table_from_dataframe_w_automatic_schema"
        f"{helpers.temp_suffix()}"
    )

    load_job = bigquery_client.load_table_from_dataframe(dataframe, table_id)
    load_job.result()

    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == (
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("ts_col", "TIMESTAMP"),
        # BigQuery does not support uploading DATETIME values from
        # Parquet files. See:
        # https://github.com/googleapis/google-cloud-python/issues/9996
        bigquery.SchemaField("dt_col", "TIMESTAMP"),
        bigquery.SchemaField("float32_col", "FLOAT"),
        bigquery.SchemaField("float64_col", "FLOAT"),
        bigquery.SchemaField("int8_col", "INTEGER"),
        bigquery.SchemaField("int16_col", "INTEGER"),
        bigquery.SchemaField("int32_col", "INTEGER"),
        bigquery.SchemaField("int64_col", "INTEGER"),
        bigquery.SchemaField("uint8_col", "INTEGER"),
        bigquery.SchemaField("uint16_col", "INTEGER"),
        bigquery.SchemaField("uint32_col", "INTEGER"),
    )
    assert table.num_rows == 3


@pytest.mark.skipif(
    pandas is None or PANDAS_INSTALLED_VERSION < PANDAS_INT64_VERSION,
    reason="only `pandas version >=1.0.0` supports Int64 extension dtype",
)
def test_load_table_from_dataframe_w_nullable_int64_datatype(
    bigquery_client, dataset_id
):
    """Test that a DataFrame containing column with None-type values and int64 datatype
    can be uploaded if a BigQuery schema is specified.

    https://github.com/googleapis/python-bigquery/issues/22
    """

    table_id = (
        f"{bigquery_client.project}.{dataset_id}"
        ".pandas_test_load_table_from_dataframe_w_nullable_int64_datatype"
        f"{helpers.temp_suffix()}"
    )
    table_schema = (bigquery.SchemaField("x", "INTEGER", mode="NULLABLE"),)
    table = helpers.retry_403(bigquery_client.create_table)(
        bigquery.Table(table_id, schema=table_schema)
    )
    df_data = collections.OrderedDict(
        [("x", pandas.Series([1, 2, None, 4], dtype="Int64"))]
    )
    dataframe = pandas.DataFrame(df_data, columns=df_data.keys())
    load_job = bigquery_client.load_table_from_dataframe(dataframe, table_id)
    load_job.result()
    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == (bigquery.SchemaField("x", "INTEGER"),)
    assert table.num_rows == 4


@pytest.mark.skipif(
    pandas is None or PANDAS_INSTALLED_VERSION < PANDAS_INT64_VERSION,
    reason="only `pandas version >=1.0.0` supports Int64 extension dtype",
)
def test_load_table_from_dataframe_w_nullable_int64_datatype_automatic_schema(
    bigquery_client, dataset_id
):
    """Test that a DataFrame containing column with None-type values and int64 datatype
    can be uploaded without specifying a schema.

    https://github.com/googleapis/python-bigquery/issues/22
    """

    table_id = (
        f"{bigquery_client.project}.{dataset_id}"
        ".pandas_test_load_table_from_dataframe_w_nullable_int64_datatype_automatic_schema"
        f"{helpers.temp_suffix()}"
    )
    df_data = collections.OrderedDict(
        [("x", pandas.Series([1, 2, None, 4], dtype="Int64"))]
    )
    dataframe = pandas.DataFrame(df_data, columns=df_data.keys())
    load_job = bigquery_client.load_table_from_dataframe(dataframe, table_id)
    load_job.result()
    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == (bigquery.SchemaField("x", "INTEGER"),)
    assert table.num_rows == 4


def test_load_table_from_dataframe_w_nulls(bigquery_client, dataset_id):
    """Test that a DataFrame with null columns can be uploaded if a
    BigQuery schema is specified.

    See: https://github.com/googleapis/google-cloud-python/issues/7370
    """
    # Schema with all scalar types.
    scalars_schema = (
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("bytes_col", "BYTES"),
        bigquery.SchemaField("date_col", "DATE"),
        bigquery.SchemaField("dt_col", "DATETIME"),
        bigquery.SchemaField("float_col", "FLOAT"),
        bigquery.SchemaField("geo_col", "GEOGRAPHY"),
        bigquery.SchemaField("int_col", "INTEGER"),
        bigquery.SchemaField("num_col", "NUMERIC"),
        bigquery.SchemaField("str_col", "STRING"),
        bigquery.SchemaField("time_col", "TIME"),
        bigquery.SchemaField("ts_col", "TIMESTAMP"),
    )
    table_schema = scalars_schema + (
        bigquery.SchemaField(
            "record_col",
            "RECORD",
            fields=[
                bigquery.SchemaField("id", "INTEGER"),
                bigquery.SchemaField("age", "INTEGER"),
            ],
        ),
        # TODO: Array columns aren't supported.
        #       https://github.com/googleapis/python-bigquery/issues/19
        # bigquery.SchemaField("array_col", "INTEGER", mode="REPEATED"),
        # bigquery.SchemaField("struct_col", "RECORD", fields=scalars_schema),
    )
    num_rows = 100
    nulls = [None] * num_rows
    df_data = collections.OrderedDict(
        [
            ("bool_col", nulls),
            ("bytes_col", nulls),
            ("date_col", nulls),
            ("dt_col", nulls),
            ("float_col", nulls),
            ("geo_col", nulls),
            ("int_col", nulls),
            ("num_col", nulls),
            ("str_col", nulls),
            ("time_col", nulls),
            ("ts_col", nulls),
            ("record_col", nulls),
        ]
    )
    dataframe = pandas.DataFrame(df_data, columns=df_data.keys())
    table_id = (
        f"{bigquery_client.project}.{dataset_id}"
        ".pandas_test_load_table_from_dataframe_w_nulls"
        f"{helpers.temp_suffix()}"
    )

    # Create the table before loading so that schema mismatch errors are
    # identified.
    table = helpers.retry_403(bigquery_client.create_table)(
        bigquery.Table(table_id, schema=table_schema)
    )

    job_config = bigquery.LoadJobConfig(schema=table_schema)
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table)
    assert tuple(table.schema) == table_schema
    assert table.num_rows == num_rows


def test_load_table_from_dataframe_w_required(bigquery_client, dataset_id):
    """Test that a DataFrame with required columns can be uploaded if a
    BigQuery schema is specified.

    See: https://github.com/googleapis/google-cloud-python/issues/8093
    """
    table_schema = (
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    )

    records = [{"name": "Chip", "age": 2}, {"name": "Dale", "age": 3}]
    dataframe = pandas.DataFrame(records, columns=["name", "age"])
    job_config = bigquery.LoadJobConfig(schema=table_schema)
    table_id = (
        f"{bigquery_client.project}.{dataset_id}"
        ".pandas_test_load_table_from_dataframe_w_required"
        f"{helpers.temp_suffix()}"
    )

    # Create the table before loading so that schema mismatch errors are
    # identified.
    table = helpers.retry_403(bigquery_client.create_table)(
        bigquery.Table(table_id, schema=table_schema)
    )

    job_config = bigquery.LoadJobConfig(schema=table_schema)
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table)
    assert tuple(table.schema) == table_schema
    assert table.num_rows == 2


def test_load_table_from_dataframe_w_explicit_schema(bigquery_client, dataset_id):
    # Schema with all scalar types.
    # TODO: Uploading DATETIME columns currently fails, thus that field type
    #       is temporarily  removed from the test.
    # See:
    #       https://github.com/googleapis/python-bigquery/issues/61
    #       https://issuetracker.google.com/issues/151765076
    scalars_schema = (
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("bytes_col", "BYTES"),
        bigquery.SchemaField("date_col", "DATE"),
        # bigquery.SchemaField("dt_col", "DATETIME"),
        bigquery.SchemaField("float_col", "FLOAT"),
        bigquery.SchemaField("geo_col", "GEOGRAPHY"),
        bigquery.SchemaField("int_col", "INTEGER"),
        bigquery.SchemaField("num_col", "NUMERIC"),
        bigquery.SchemaField("str_col", "STRING"),
        bigquery.SchemaField("time_col", "TIME"),
        bigquery.SchemaField("ts_col", "TIMESTAMP"),
    )
    table_schema = scalars_schema + (
        # Struct / Record columns are supported when serializing to Parquet.
        # https://github.com/googleapis/python-bigquery/issues/21
        bigquery.SchemaField(
            "record_col",
            "RECORD",
            fields=[
                bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
            ],
            mode="REQUIRED",
        ),
        # TODO: Array columns can't be read due to NULLABLE versus REPEATED
        #       mode mismatch. See:
        #       https://issuetracker.google.com/133415569#comment3
        # bigquery.SchemaField("array_col", "INTEGER", mode="REPEATED"),
        # TODO: Support writing StructArrays to Parquet. See:
        #       https://jira.apache.org/jira/browse/ARROW-2587
        # bigquery.SchemaField("struct_col", "RECORD", fields=scalars_schema),
    )
    df_data = collections.OrderedDict(
        [
            ("bool_col", [True, None, False]),
            ("bytes_col", [b"abc", None, b"def"]),
            ("date_col", [datetime.date(1, 1, 1), None, datetime.date(9999, 12, 31)],),
            # (
            #     "dt_col",
            #     [
            #         datetime.datetime(1, 1, 1, 0, 0, 0),
            #         None,
            #         datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
            #     ],
            # ),
            ("float_col", [float("-inf"), float("nan"), float("inf")]),
            (
                "geo_col",
                [
                    "POINT(30 10)",
                    None,
                    "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
                ],
            ),
            ("int_col", [-9223372036854775808, None, 9223372036854775807]),
            (
                "num_col",
                [
                    decimal.Decimal("-99999999999999999999999999999.999999999"),
                    None,
                    decimal.Decimal("99999999999999999999999999999.999999999"),
                ],
            ),
            ("str_col", ["abc", None, "def"]),
            (
                "time_col",
                [datetime.time(0, 0, 0), None, datetime.time(23, 59, 59, 999999)],
            ),
            (
                "ts_col",
                [
                    datetime.datetime(1, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    None,
                    datetime.datetime(
                        9999, 12, 31, 23, 59, 59, 999999, tzinfo=pytz.utc
                    ),
                ],
            ),
            ("record_col", [None, {"id": 2, "age": 22}, {"id": 3, "age": 23}],),
        ]
    )
    dataframe = pandas.DataFrame(df_data, dtype="object", columns=df_data.keys())

    table_id = (
        f"{bigquery_client.project}.{dataset_id}"
        ".pandas_test_load_table_from_dataframe_w_explicit_schema"
        f"{helpers.temp_suffix()}"
    )

    job_config = bigquery.LoadJobConfig(schema=table_schema)
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == table_schema
    assert table.num_rows == 3


def test_load_table_from_dataframe_w_explicit_schema_source_format_csv(
    bigquery_client, dataset_id
):
    from google.cloud.bigquery.job import SourceFormat

    table_schema = (
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("bytes_col", "BYTES"),
        bigquery.SchemaField("date_col", "DATE"),
        bigquery.SchemaField("dt_col", "DATETIME"),
        bigquery.SchemaField("float_col", "FLOAT"),
        bigquery.SchemaField("geo_col", "GEOGRAPHY"),
        bigquery.SchemaField("int_col", "INTEGER"),
        bigquery.SchemaField("num_col", "NUMERIC"),
        bigquery.SchemaField("str_col", "STRING"),
        bigquery.SchemaField("time_col", "TIME"),
        bigquery.SchemaField("ts_col", "TIMESTAMP"),
    )
    df_data = collections.OrderedDict(
        [
            ("bool_col", [True, None, False]),
            ("bytes_col", ["abc", None, "def"]),
            ("date_col", [datetime.date(1, 1, 1), None, datetime.date(9999, 12, 31)],),
            (
                "dt_col",
                [
                    datetime.datetime(1, 1, 1, 0, 0, 0),
                    None,
                    datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
                ],
            ),
            ("float_col", [float("-inf"), float("nan"), float("inf")]),
            (
                "geo_col",
                [
                    "POINT(30 10)",
                    None,
                    "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
                ],
            ),
            ("int_col", [-9223372036854775808, None, 9223372036854775807]),
            (
                "num_col",
                [
                    decimal.Decimal("-99999999999999999999999999999.999999999"),
                    None,
                    decimal.Decimal("99999999999999999999999999999.999999999"),
                ],
            ),
            ("str_col", ["abc", None, "def"]),
            (
                "time_col",
                [datetime.time(0, 0, 0), None, datetime.time(23, 59, 59, 999999)],
            ),
            (
                "ts_col",
                [
                    datetime.datetime(1, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    None,
                    datetime.datetime(
                        9999, 12, 31, 23, 59, 59, 999999, tzinfo=pytz.utc
                    ),
                ],
            ),
        ]
    )
    dataframe = pandas.DataFrame(df_data, dtype="object", columns=df_data.keys())

    table_id = (
        f"{bigquery_client.project}.{dataset_id}"
        ".pandas_test_load_table_from_dataframe_w_explicit_schema_source_format_csv"
        f"{helpers.temp_suffix()}"
    )

    job_config = bigquery.LoadJobConfig(
        schema=table_schema, source_format=SourceFormat.CSV
    )
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == table_schema
    assert table.num_rows == 3


def test_load_table_from_dataframe_w_explicit_schema_source_format_csv_floats(
    bigquery_client, dataset_id
):
    from google.cloud.bigquery.job import SourceFormat

    table_schema = (bigquery.SchemaField("float_col", "FLOAT"),)
    df_data = collections.OrderedDict(
        [
            (
                "float_col",
                [
                    0.14285714285714285,
                    0.51428571485748,
                    0.87128748,
                    1.807960649,
                    2.0679610649,
                    2.4406779661016949,
                    3.7148514257,
                    3.8571428571428572,
                    1.51251252e40,
                ],
            ),
        ]
    )
    dataframe = pandas.DataFrame(df_data, dtype="object", columns=df_data.keys())
    table_id = (
        f"{bigquery_client.project}.{dataset_id}"
        ".pandas_test_load_table_from_dataframe_w_explicit_schema_source_format_csv_floats"
        f"{helpers.temp_suffix()}"
    )

    job_config = bigquery.LoadJobConfig(
        schema=table_schema, source_format=SourceFormat.CSV
    )
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table_id)
    rows = list(bigquery_client.list_rows(table))
    floats = [r.values()[0] for r in rows]
    assert tuple(table.schema) == table_schema
    assert table.num_rows == 9
    assert floats == df_data["float_col"]
