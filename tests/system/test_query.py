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

import pytest


@pytest.fixture(
    params=[
        # None,
        # "insert",
        "query",
    ]
)
def query_api_method(request):
    return request.param


@pytest.fixture(scope="session")
def table_with_9999_columns_10_rows(bigquery_client, project_id, dataset_id):
    """Generate a table of maximum width via CREATE TABLE AS SELECT.

    The first column is named 'rowval', and has a value from 1..rowcount
    Subsequent columns are named col_<N> and contain the value N*rowval, where
    N is between 1 and 9999 inclusive.
    """
    table_id = "many_columns"
    row_count = 10
    col_projections = ",".join([f"r * {n} as col_{n}" for n in range(1, 10000)])
    sql = f"""
    CREATE TABLE `{project_id}.{dataset_id}.{table_id}`
    AS
    SELECT
        r as rowval,
        {col_projections}
    FROM
      UNNEST(GENERATE_ARRAY(1,{row_count},1)) as r
    """
    query_job = bigquery_client.query(sql)
    query_job.result()

    return f"{project_id}.{dataset_id}.{table_id}"


def test_query_many_columns(
    bigquery_client, table_with_9999_columns_10_rows, query_api_method
):
    # Test working with the widest schema BigQuery supports, 10k columns.
    if query_api_method is not None:
        query_job = bigquery_client.query(
            f"SELECT * FROM `{table_with_9999_columns_10_rows}`",
            api_method=query_api_method,
        )
    else:
        query_job = bigquery_client.query(
            f"SELECT * FROM `{table_with_9999_columns_10_rows}`"
        )
    rows = list(query_job)
    assert len(rows) == 10

    # check field representations adhere to expected values.
    for row in rows:
        rowval = row["rowval"]
        for column in range(1, 10000):
            assert row[f"col_{column}"] == rowval * column
