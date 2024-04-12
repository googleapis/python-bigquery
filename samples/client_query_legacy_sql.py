# Copyright 2019 Google LLC
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


def client_query_legacy_sql() -> None:
    # [START bigquery_query_legacy]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    query = (
        "SELECT name FROM [bigquery-public-data:usa_names.usa_1910_2013] "
        'WHERE state = "TX" '
        "LIMIT 100"
    )

    # Set use_legacy_sql to True to use legacy SQL syntax.
    job_config = bigquery.QueryJobConfig(use_legacy_sql=True)

    # Start the query and waits for query job to complete, passing in the extra configuration.
    results = client.query_and_wait(
        query, job_config=job_config
    )  # Make an API request.

    print("The query data:")
    for row in results:
        print(row)
    # [END bigquery_query_legacy]
