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

from typing import Dict, Any
from unittest import mock

import pytest

from google.cloud.bigquery.client import Client
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery.job.query import QueryJob, QueryJobConfig


def make_query_response(
    completed: bool = False,
    job_id: str = "abcd-efg-hijk-lmnop",
    location="US",
    project_id="test-project",
) -> Dict[str, Any]:
    response = {
        "jobReference": {
            "projectId": project_id,
            "jobId": job_id,
            "location": location,
        },
        "jobComplete": completed,
    }
    return response


@pytest.mark.parametrize(
    ("job_config", "expected"),
    (
        (None, {"useLegacySql": False}),
        (QueryJobConfig(), {"useLegacySql": False}),
        (QueryJobConfig(dry_run=True), {"useLegacySql": False, "dryRun": True}),
        (
            QueryJobConfig(labels={"abc": "def"}),
            {"useLegacySql": False, "labels": {"abc": "def"}},
        ),
        (
            QueryJobConfig(use_query_cache=False),
            {"useLegacySql": False, "useQueryCache": False},
        ),
    ),
)
def test__to_query_request(job_config, expected):
    result = _job_helpers._to_query_request(job_config)
    assert result == expected


def test__to_query_job_defaults():
    mock_client = mock.create_autospec(Client)
    response = make_query_response(
        job_id="test-job", project_id="some-project", location="asia-northeast1"
    )
    job: QueryJob = _job_helpers._to_query_job(mock_client, "query-str", None, response)
    assert job.query == "query-str"
    assert job._client is mock_client
    assert job.job_id == "test-job"
    assert job.project == "some-project"
    assert job.location == "asia-northeast1"
    assert job.error_result is None
    assert job.errors is None


def test__to_query_job_dry_run():
    mock_client = mock.create_autospec(Client)
    response = make_query_response(
        job_id="test-job", project_id="some-project", location="asia-northeast1"
    )
    job_config: QueryJobConfig = QueryJobConfig()
    job_config.dry_run = True
    job: QueryJob = _job_helpers._to_query_job(
        mock_client, "query-str", job_config, response
    )
    assert job.dry_run is True


@pytest.mark.parametrize(
    ("completed", "expected_state"), ((True, "DONE"), (False, "PENDING"),),
)
def test__to_query_job_sets_state(completed, expected_state):
    mock_client = mock.create_autospec(Client)
    response = make_query_response(completed=completed)
    job: QueryJob = _job_helpers._to_query_job(mock_client, "query-str", None, response)
    assert job.state == expected_state


def test__to_query_job_sets_errors():
    assert False
