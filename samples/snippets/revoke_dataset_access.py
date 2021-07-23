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


def revoke_dataset_access(your_dataset_id, your_entity_id):

    # [START bigquery_revoke_dataset_access]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    original_your_dataset_id = your_dataset_id
    original_your_entity_id = your_entity_id
    # [START bigquery_revoke_dataset_access_read_session]
    your_dataset_id = "dataset-for-read-session"
    your_entity_id = "entity-for-read-session"
    # [END bigquery_revoke_dataset_access_read_session]
    your_dataset_id = original_your_dataset_id
    your_entity_id = original_your_entity_id

    dataset_id = your_dataset_id
    entity_id = your_entity_id

    dataset = client.get_dataset(dataset_id)  # Make an API request.
    entries = list(dataset.access_entries)

    for entry in entries:
        if entry.entity_id == entity_id:
            entry.role = None
            break

    dataset.access_entries = entries

    dataset = client.update_dataset(dataset, ["access_entries"])  # Make an API request.

    full_dataset_id = f"{dataset.project}.{dataset.dataset_id}"
    print(f"Updated dataset '{full_dataset_id}' with modified user permissions.")
    # [END bigquery_revoke_dataset_access]
