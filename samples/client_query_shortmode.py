# Copyright 2024 Google LLC
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


def client_query_shortmode() -> None:
    # [START bigquery_query_shortquery]
    # This example demonstrates issuing a query that may be run in short query mode.
    #
    # To enable the short query mode preview feature, the QUERY_PREVIEW_ENABLED
    # environmental variable should be set to `TRUE`.
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    query = """
        SELECT
            name,
            gender,
            SUM(number) AS total
        FROM
            bigquery-public-data.usa_names.usa_1910_2013
        GROUP BY
            name, gender
        ORDER BY
            total DESC
        LIMIT 10
    """
    # Run the query.  The returned `rows` iterator can return information about
    # how the query was executed as well as the result data.
    rows = client.query_and_wait(query)

    if rows.job_id is not None:
        print("Query was run with job state.  Job ID: {}".format(rows.job_id))
    else:
        print("Query was run in short mode.  Query ID: {}".format(rows.query_id))

    print("The query data:")
    for row in rows:
        # Row values can be accessed by field name or index.
        print("name={}, gender={}, total={}".format(row[0], row[1], row["total"]))
    # [END bigquery_query_shortquery]
