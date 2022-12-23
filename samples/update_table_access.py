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


def update_dataset_access(table_id: str) -> None:

    # [START bigquery_update_table_access]
    from google.cloud import bigquery
    from google.api_core.iam import Policy
    import json

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to fetch.
    # table_id = 'your-project.your_dataset.your_table'

    table = client.get_table(table_id) # Make an API request.

    iam_entries = """
    {
        "bindings": [
            {
            "role": "roles/bigquery.admin",
            "members": [
                "user:cloud-developer-relations@google.com"
            ]
            }
        ]
    }
    """ # Role https://cloud.google.com/iam/docs/understanding-roles

    resource = json.loads(iam_entries)
    policy = Policy.from_api_repr(resource)

    policy = client.set_iam_policy(table, policy) # Make an API request.

    print(
        "Updated table '{}' with modified user permissions.".format(table_id)
    )
    # [END bigquery_update_table_access]
