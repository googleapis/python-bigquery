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


def test_bqstorage(bigquery_client, scalars_table):
    arrow_table = bigquery_client.list_rows(scalars_table).to_arrow()
    assert arrow_table.schema is None

    # timestamp_col: timestamp[us, tz=UTC]
    # time_col: time64[us]
    # float64_col: double
    # datetime_col: timestamp[us]
    #   -- field metadata --
    #   ARROW:extension:name: 'google:sqlType:datetime'
    # bignumeric_col: decimal256(76, 38)
    # numeric_col: decimal128(38, 9)
    # geography_col: string
    #   -- field metadata --
    #   ARROW:extension:name: 'google:sqlType:geography'
    #   ARROW:extension:metadata: '{"encoding": "WKT"}'
    # date_col: date32[day]
    # string_col: string
    # bool_col: bool
    # bytes_col: binary
    # int64_col: int64


def test_rest(bigquery_client, scalars_table):
    arrow_table = bigquery_client.list_rows(scalars_table, max_results=10).to_arrow()
    assert arrow_table.schema is None

    # timestamp_col: timestamp[us, tz=UTC]
    # time_col: time64[us]
    # float64_col: double
    # datetime_col: timestamp[us]
    # bignumeric_col: decimal256(76, 38)
    # numeric_col: decimal128(38, 9)
    # geography_col: string
    # date_col: date32[day]
    # string_col: string
    # bool_col: bool
    # bytes_col: binary
    # int64_col: int64
