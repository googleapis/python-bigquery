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

import typing

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def delete_dataset_labels(dataset_id: str) -> bigquery.Dataset:

    # [START bigquery_delete_label_dataset]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    # dataset_id = "your-project.your_dataset"

    dataset = client.get_dataset(dataset_id)  # Make an API request.

    # To delete a label from a dataset, set its value to None.
    dataset.labels["color"] = None

    dataset = client.update_dataset(dataset, ["labels"])  # Make an API request.
    print("Labels deleted from {}".format(dataset_id))
    # [END bigquery_delete_label_dataset]
    return dataset
