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

from google.cloud import bigquery


def test_dry_run(bigquery_client: bigquery.Client, scalars_table: str):
    query_config = bigquery.QueryJobConfig()
    query_config.dry_run = True

    query_string = f"SELECT * FROM {scalars_table}"
    query_job = bigquery_client.query(query_string, job_config=query_config,)

    # Note: `query_job.result()` is not necessary on a dry run query. All
    # necessary information is returned in the initial response.
    assert query_job.dry_run is True
    assert query_job.total_bytes_processed > 0
    assert len(query_job.schema) > 0


def test_query_session(bigquery_client: bigquery.Client):
    # CREATE TEMPORARY TABLE requires a script, a plain statement would not do.
    sql = """
        DECLARE my_number INT64;
        SET my_number = 123;
        CREATE TEMPORARY TABLE tbl_temp AS SELECT my_number AS foo;
    """
    job_config = bigquery.QueryJobConfig(create_session=True)
    query_job = bigquery_client.query(sql, job_config=job_config)
    query_job.result()

    session_id = query_job.session_id
    assert session_id is not None

    job_config = bigquery.QueryJobConfig(
        connection_properties=[
            bigquery.ConnectionProperty(key="session_id", value=session_id)
        ]
    )
    query_job_2 = bigquery_client.query("SELECT * FROM tbl_temp", job_config=job_config)
    result = query_job_2.result()  # No error if the session works.

    rows = list(result)
    assert len(rows) == 1
    assert list(rows[0].items()) == [("foo", 123)]
