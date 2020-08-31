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


def table_insert_rows(table_id):

    # [START bigquery_table_insert_rows]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the model to fetch.
    table_id = "your-project.your_dataset.your_table"

    # The client converts Python objects to JSON-serialization, but this requires a schema.
    # A schema can be fetched by calling `client.get_table` as shown below.
    # schema = client.get_table(table_id).schema
    
    # If inserting many rows, it is suggested that you cache the schema.
    # The backend API for `client.insert_rows` supports a much higher QPS
    # than the backend API for `client.get_table`.

    schema = [
        bigquery.SchemaField("col_1", "STRING"),
        bigquery.SchemaField("col_2", "INTEGER"),
        ]

    # Populate data for entry
    rows_to_insert = [(u"Phred Phlyntstone", 32), (u"Wylma Phlyntstone", 29)]

    try:
        # Stream data to BQ
        client.insert_rows(table_id, selected_fields=schema, rows_to_insert)
        print("New rows have been added.")
    # [END bigquery_table_insert_rows]
    
    
