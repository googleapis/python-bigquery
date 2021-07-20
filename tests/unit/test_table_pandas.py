# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

import pytest

from google.cloud import bigquery

pandas = pytest.importorskip("pandas")


TEST_PATH = "/v1/project/test-proj/dataset/test-dset/table/test-tbl/data"


@pytest.fixture
def class_under_test():
    from google.cloud.bigquery.table import RowIterator

    return RowIterator


def test_to_dataframe_defaults_to_nullable_dtypes(class_under_test):
    nullable_schema = [
        bigquery.SchemaField("date_col", "DATE"),
        bigquery.SchemaField("datetime_col", "DATETIME"),
        bigquery.SchemaField("float_col", "FLOAT"),
        bigquery.SchemaField("float64_col", "FLOAT64"),
        bigquery.SchemaField("integer_col", "INTEGER"),
        bigquery.SchemaField("int64_col", "INT64"),
        bigquery.SchemaField(
            "time_col", "TIME"
        ),  # TODO: use timedelta64 dtype for this?
        bigquery.SchemaField("timestamp_col", "TIMESTAMP"),
    ]
    mock_client = mock.create_autospec(bigquery.Client)
    mock_client.project = "test-proj"
    mock_api_request = mock.Mock()
    rows = class_under_test(mock_client, mock_api_request, TEST_PATH, nullable_schema,)
    rows.to_dataframe()  # TODO: if we are always using BQ Storage API for
    # to_dataframe, maybe wait to implement until after required?
    # TODO: behavior is based on schema (and data rows)
    assert False


def test_to_dataframe_bqstorage_defaults_to_nullable_dtypes(class_under_test):
    # TODO: behavior is based on schema (and data rows)
    assert False


def test_to_dataframe_overrides_nullable_dtypes(class_under_test):
    """Passing in explicit dtypes is merged with default behavior."""
    assert False


def test_to_dataframe_bqstorage_overrides_nullable_dtypes(class_under_test):
    """Passing in explicit dtypes is merged with default behavior."""
    assert False
