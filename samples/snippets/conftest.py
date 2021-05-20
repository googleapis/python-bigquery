# Copyright 2020 Google LLC
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

import datetime
import random

from google.cloud import bigquery
import pytest


RESOURCE_PREFIX = "python_bigquery_samples_snippets"
RESOURCE_DATE_FORMAT = "%Y%m%d_%H%M%S"
RESOURCE_DATE_LENGTH = 4 + 2 + 2 + 1 + 2 + 2 + 2


def resource_prefix() -> str:
    timestamp = datetime.datetime.utcnow().strftime(RESOURCE_DATE_FORMAT)
    random_string = hex(random.randrange(1000000))[2:]
    return f"{RESOURCE_PREFIX}_{timestamp}_{random_string}"


def resource_name_to_date(resource_name: str):
    start_date = len(RESOURCE_PREFIX) + 1
    date_string = resource_name[start_date : start_date + RESOURCE_DATE_LENGTH]
    return datetime.datetime.strptime(date_string, RESOURCE_DATE_FORMAT)


@pytest.fixture(scope="session", autouse=True)
def cleanup_datasets(bigquery_client: bigquery.Client):
    yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    for dataset in bigquery_client.list_datasets():
        if (
            dataset.dataset_id.startswith(RESOURCE_PREFIX)
            and resource_name_to_date(dataset.dataset_id) < yesterday
        ):
            bigquery_client.delete_dataset(
                dataset, delete_contents=True, not_found_ok=True
            )


@pytest.fixture(scope="session")
def bigquery_client():
    bigquery_client = bigquery.Client()
    return bigquery_client


@pytest.fixture(scope="session")
def project_id(bigquery_client):
    return bigquery_client.project


@pytest.fixture(scope="session")
def dataset_id(bigquery_client: bigquery.Client, project_id: str):
    dataset_id = resource_prefix()
    full_dataset_id = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(full_dataset_id)
    bigquery_client.create_dataset(dataset)
    yield dataset_id
    bigquery_client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)


@pytest.fixture
def bigquery_client_patch(monkeypatch, bigquery_client):
    monkeypatch.setattr(bigquery, "Client", lambda: bigquery_client)
