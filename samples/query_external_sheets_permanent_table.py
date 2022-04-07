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


def query_external_sheets_permanent_table(dataset_id: str) -> None:

    # [START bigquery_query_external_sheets_perm]
    from google.cloud import bigquery
    import google.auth

    # Create credentials with Drive & BigQuery API scopes.
    # Both APIs must be enabled for your project before running this code.
    #
    # If you are using credentials from gcloud, you must authorize the
    # application first with the following command:
    #
    # gcloud auth application-default login \
    #   --scopes=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/cloud-platform
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery",
        ]
    )

    # Construct a BigQuery client object.
    client = bigquery.Client(credentials=credentials, project=project)

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    # dataset_id = "your-project.your_dataset"

    # Configure the external data source.
    dataset = client.get_dataset(dataset_id)
    table_id = "us_states"
    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    table = bigquery.Table(dataset.table(table_id), schema=schema)
    external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
    # Use a shareable link or grant viewing access to the email address you
    # used to authenticate with BigQuery (this example Sheet is public).
    sheet_url = (
        "https://docs.google.com/spreadsheets"
        "/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing"
    )
    external_config.source_uris = [sheet_url]
    options = external_config.google_sheets_options
    assert options is not None
    options.skip_leading_rows = 1  # Optionally skip header row.
    options.range = (
        "us-states!A20:B49"  # Optionally set range of the sheet to query from.
    )
    table.external_data_configuration = external_config

    # Create a permanent table linked to the Sheets file.
    table = client.create_table(table)  # Make an API request.

    # Example query to find states starting with "W".
    sql = 'SELECT * FROM `{}.{}` WHERE name LIKE "W%"'.format(dataset_id, table_id)

    query_job = client.query(sql)  # Make an API request.

    # Wait for the query to complete.
    w_states = list(query_job)
    print(
        "There are {} states with names starting with W in the selected range.".format(
            len(w_states)
        )
    )
    # [END bigquery_query_external_sheets_perm]
