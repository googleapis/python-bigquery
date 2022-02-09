# Copyright 2021 Google LLC
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

"""System tests for Arrow connector."""

from typing import Optional

import pyarrow
import pyarrow.types
import pytest

from google.cloud import bigquery
from google.cloud.bigquery import enums
from . import helpers


@pytest.mark.parametrize(
    ("max_results", "scalars_table_name"),
    (
        (None, "scalars_table"),  # Use BQ Storage API.
        (10, "scalars_table"),  # Use REST API.
        (None, "scalars_extreme_table"),  # Use BQ Storage API.
        (10, "scalars_extreme_table"),  # Use REST API.
    ),
)
def test_list_rows_nullable_scalars_dtypes(
    bigquery_client: bigquery.Client,
    scalars_table: str,
    scalars_extreme_table: str,
    max_results: Optional[int],
    scalars_table_name: str,
):
    table_id = scalars_table
    if scalars_table_name == "scalars_extreme_table":
        table_id = scalars_extreme_table

    # TODO(GH#836): Avoid INTERVAL columns until they are supported by the
    # BigQuery Storage API and pyarrow.
    schema = [
        bigquery.SchemaField("bool_col", enums.SqlTypeNames.BOOLEAN),
        bigquery.SchemaField("bignumeric_col", enums.SqlTypeNames.BIGNUMERIC),
        bigquery.SchemaField("bytes_col", enums.SqlTypeNames.BYTES),
        bigquery.SchemaField("date_col", enums.SqlTypeNames.DATE),
        bigquery.SchemaField("datetime_col", enums.SqlTypeNames.DATETIME),
        bigquery.SchemaField("float64_col", enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("geography_col", enums.SqlTypeNames.GEOGRAPHY),
        bigquery.SchemaField("int64_col", enums.SqlTypeNames.INT64),
        bigquery.SchemaField("numeric_col", enums.SqlTypeNames.NUMERIC),
        bigquery.SchemaField("string_col", enums.SqlTypeNames.STRING),
        bigquery.SchemaField("time_col", enums.SqlTypeNames.TIME),
        bigquery.SchemaField("timestamp_col", enums.SqlTypeNames.TIMESTAMP),
    ]

    arrow_table = bigquery_client.list_rows(
        table_id, max_results=max_results, selected_fields=schema,
    ).to_arrow()

    schema = arrow_table.schema
    bignumeric_type = schema.field("bignumeric_col").type
    # 77th digit is partial.
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types
    assert bignumeric_type.precision in {76, 77}
    assert bignumeric_type.scale == 38

    bool_type = schema.field("bool_col").type
    assert bool_type.equals(pyarrow.bool_())

    bytes_type = schema.field("bytes_col").type
    assert bytes_type.equals(pyarrow.binary())

    date_type = schema.field("date_col").type
    assert date_type.equals(pyarrow.date32())

    datetime_type = schema.field("datetime_col").type
    assert datetime_type.unit == "us"
    assert datetime_type.tz is None

    float64_type = schema.field("float64_col").type
    assert float64_type.equals(pyarrow.float64())

    geography_type = schema.field("geography_col").type
    assert geography_type.equals(pyarrow.string())

    int64_type = schema.field("int64_col").type
    assert int64_type.equals(pyarrow.int64())

    numeric_type = schema.field("numeric_col").type
    assert numeric_type.precision == 38
    assert numeric_type.scale == 9

    string_type = schema.field("string_col").type
    assert string_type.equals(pyarrow.string())

    time_type = schema.field("time_col").type
    assert time_type.equals(pyarrow.time64("us"))

    timestamp_type = schema.field("timestamp_col").type
    assert timestamp_type.unit == "us"
    assert timestamp_type.tz is not None


@pytest.mark.parametrize("do_insert", [True, False])
def test_arrow_extension_types_same_for_storage_and_REST_APIs_894(
    dataset_client, test_table_name, do_insert
):
    types = dict(
        astring=("STRING", "'x'"),
        astring9=("STRING(9)", "'x'"),
        abytes=("BYTES", "b'x'"),
        abytes9=("BYTES(9)", "b'x'"),
        anumeric=("NUMERIC", "42"),
        anumeric9=("NUMERIC(9)", "42"),
        anumeric92=("NUMERIC(9,2)", "42"),
        abignumeric=("BIGNUMERIC", "42e30"),
        abignumeric49=("BIGNUMERIC(37)", "42e30"),
        abignumeric492=("BIGNUMERIC(37,2)", "42e30"),
        abool=("BOOL", "true"),
        adate=("DATE", "'2021-09-06'"),
        adatetime=("DATETIME", "'2021-09-06T09:57:26'"),
        ageography=("GEOGRAPHY", "ST_GEOGFROMTEXT('point(0 0)')"),
        # Can't get arrow data for interval :(
        # ainterval=('INTERVAL', "make_interval(1, 2, 3, 4, 5, 6)"),
        aint64=("INT64", "42"),
        afloat64=("FLOAT64", "42.0"),
        astruct=("STRUCT<v int64>", "struct(42)"),
        atime=("TIME", "'1:2:3'"),
        atimestamp=("TIMESTAMP", "'2021-09-06T09:57:26'"),
    )
    columns = ", ".join(f"{k} {t[0]}" for k, t in types.items())
    dataset_client.query(f"create table {test_table_name} ({columns})").result()
    if do_insert:
        names = list(types)
        values = ", ".join(types[name][1] for name in names)
        names = ", ".join(names)
        dataset_client.query(
            f"insert into {test_table_name} ({names}) values ({values})"
        ).result()
    at = dataset_client.query(f"select * from {test_table_name}").result().to_arrow()
    storage_api_metadata = {
        at.field(i).name: at.field(i).metadata for i in range(at.num_columns)
    }
    at = (
        dataset_client.query(f"select * from {test_table_name}")
        .result()
        .to_arrow(create_bqstorage_client=False)
    )
    rest_api_metadata = {
        at.field(i).name: at.field(i).metadata for i in range(at.num_columns)
    }

    assert rest_api_metadata == storage_api_metadata
    assert rest_api_metadata["adatetime"] == {
        b"ARROW:extension:name": b"google:sqlType:datetime"
    }
    assert rest_api_metadata["ageography"] == {
        b"ARROW:extension:name": b"google:sqlType:geography",
        b"ARROW:extension:metadata": b'{"encoding": "WKT"}',
    }


@pytest.mark.parametrize(("use_bqstorage_api",), [(True,), (False,)])
def test_query_extreme_bignumeric(bigquery_client, use_bqstorage_api):
    """
    Check that values outside of the pyarrow representable bounds can still be
    passed in.

    https://github.com/googleapis/python-bigquery/issues/812
    """
    query_text = f"""
    DECLARE MIN_BIGNUMERIC STRING;
    DECLARE MAX_BIGNUMERIC STRING;
    SET MIN_BIGNUMERIC = '{helpers.MIN_BIGNUMERIC}';
    SET MAX_BIGNUMERIC = '{helpers.MAX_BIGNUMERIC}';

    SELECT
    CAST(MIN_BIGNUMERIC AS BIGNUMERIC) AS min_bignumeric,
    CAST(MAX_BIGNUMERIC AS BIGNUMERIC) AS max_bignumeric,
    CAST('1.2345' AS BIGNUMERIC) AS small_bignumeric,
    STRUCT<x BIGNUMERIC, y BIGNUMERIC>(
        CAST(MIN_BIGNUMERIC AS BIGNUMERIC),
        CAST(MAX_BIGNUMERIC AS BIGNUMERIC)
    ) AS struct_bignumeric,
    [
        CAST(MIN_BIGNUMERIC AS BIGNUMERIC),
        CAST(MAX_BIGNUMERIC AS BIGNUMERIC)
    ] AS array_bignumeric,
    [
        STRUCT<x BIGNUMERIC, y BIGNUMERIC>(
            CAST(MIN_BIGNUMERIC AS BIGNUMERIC),
            CAST(MAX_BIGNUMERIC AS BIGNUMERIC)
        ),
            STRUCT<x BIGNUMERIC, y BIGNUMERIC>(
            CAST(MIN_BIGNUMERIC AS BIGNUMERIC),
            CAST(MAX_BIGNUMERIC AS BIGNUMERIC)
        )
    ] AS array_struct_bignumeric;
    """
    arrow_table = bigquery_client.query(query_text).to_arrow(
        create_bqstorage_client=use_bqstorage_api
    )
    arrow_schema = arrow_table.schema
    assert pyarrow.types.is_decimal256(arrow_schema.field("small_bignumeric").type)

    if use_bqstorage_api:
        assert pyarrow.types.is_decimal256(arrow_schema.field("min_bignumeric").type)
        assert pyarrow.types.is_decimal256(arrow_schema.field("max_bignumeric").type)
        assert pyarrow.types.is_decimal256(
            arrow_schema.field("array_bignumeric").type.value_type
        )
        assert pyarrow.types.is_decimal256(
            arrow_schema.field("struct_bignumeric").type["x"].type
        )
        assert pyarrow.types.is_decimal256(
            arrow_schema.field("struct_bignumeric").type["y"].type
        )
        assert pyarrow.types.is_decimal256(
            arrow_schema.field("array_struct_bignumeric").type.value_type["x"].type
        )
        assert pyarrow.types.is_decimal256(
            arrow_schema.field("array_struct_bignumeric").type.value_type["y"].type
        )
    else:
        assert pyarrow.types.is_string(arrow_schema.field("min_bignumeric").type)
        assert pyarrow.types.is_string(arrow_schema.field("max_bignumeric").type)
        assert pyarrow.types.is_string(
            arrow_schema.field("array_bignumeric").type.value_type
        )
        assert pyarrow.types.is_string(
            arrow_schema.field("struct_bignumeric").type["x"].type
        )
        assert pyarrow.types.is_string(
            arrow_schema.field("struct_bignumeric").type["y"].type
        )
        assert pyarrow.types.is_string(
            arrow_schema.field("array_struct_bignumeric").type.value_type["x"].type
        )
        assert pyarrow.types.is_string(
            arrow_schema.field("array_struct_bignumeric").type.value_type["y"].type
        )
