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

import datetime
import re

import mock
import pytest

import google.api_core.exceptions
import google.api_core.retry
import freezegun

from google.cloud.bigquery.client import Client
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery.retry import DEFAULT_RETRY, DEFAULT_JOB_RETRY

from .helpers import make_connection


# With job_retry_on_query, we're testing 4 scenarios:
# - No `job_retry` passed, retry on default rateLimitExceeded.
# - Pass NotFound retry to `query`.
# - Pass NotFound retry to `result`.
# - Pass BadRequest retry to query, with the value passed to `result` overriding.
@pytest.mark.parametrize("job_retry_on_query", [None, "Query", "Result", "Both"])
def test_retry_failed_jobs(job_retry_on_query):
    """
    Test retry of job failures, as opposed to API-invocation failures.
    """

    retry_notfound = google.api_core.retry.Retry(
        predicate=google.api_core.retry.if_exception_type(
            google.api_core.exceptions.NotFound
        )
    )
    retry_badrequest = google.api_core.retry.Retry(
        predicate=google.api_core.retry.if_exception_type(
            google.api_core.exceptions.BadRequest
        )
    )

    if job_retry_on_query is None:
        errs = [{"reason": "rateLimitExceeded"}]
    else:
        errs = [{"reason": "notFound"}]

    freezegun.freeze_time(auto_tick_seconds=1)
    client = mock.create_autospec(Client)
    client._call_api.__name__ = "_call_api"
    client._call_api.__qualname__ = "Client._call_api"
    client._call_api.__annotations__ = {}
    client._call_api.__type_params__ = ()
    client._call_api.side_effect = (
        {
            "jobReference": {
                "projectId": "response-project",
                "jobId": "abc",
                "location": "response-location",
            },
            "jobComplete": False,
        },
        google.api_core.exceptions.InternalServerError("job_retry me", errors=errs),
        {
            "jobReference": {
                "projectId": "response-project",
                "jobId": "abc",
                "location": "response-location",
            },
            "jobComplete": True,
            "schema": {
                "fields": [
                    {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "age", "type": "INT64", "mode": "NULLABLE"},
                ],
            },
            "rows": [
                {"f": [{"v": "Whillma Phlyntstone"}, {"v": "27"}]},
                {"f": [{"v": "Bhetty Rhubble"}, {"v": "28"}]},
                {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
                {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            ],
        },
    )

    if job_retry_on_query == "Query":
        job_retry = retry_notfound
    elif job_retry_on_query == "Both":
        # This will be overridden in `result`
        job_retry = retry_badrequest
    else:
        job_retry = None

    rows = _job_helpers.query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        page_size=None,
        max_results=None,
        retry=DEFAULT_RETRY,
        job_retry=job_retry,
    )

    assert len(list(rows)) == 4


# With job_retry_on_query, we're testing 4 scenarios:
# - Pass None retry to `query`.
# - Pass None retry to `result`.
@pytest.mark.parametrize("job_retry_on_query", ["Query", "Result"])
def test_disable_retry_failed_jobs(job_retry_on_query):
    """
    Test retry of job failures, as opposed to API-invocation failures.
    """

    freezegun.freeze_time(auto_tick_seconds=1)
    client = mock.create_autospec(Client)
    client._call_api.__name__ = "_call_api"
    client._call_api.__qualname__ = "Client._call_api"
    client._call_api.__annotations__ = {}
    client._call_api.__type_params__ = ()
    client._call_api.side_effect = (
        {
            "jobReference": {
                "projectId": "response-project",
                "jobId": "abc",
                "location": "response-location",
            },
            "jobComplete": False,
        },
        google.api_core.exceptions.InternalServerError(
            "job_retry me", errors=[{"reason": "rateLimitExceeded"}]
        ),
    )

    rows = _job_helpers.query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        page_size=None,
        max_results=None,
        retry=None,  # Explicitly disable retry
        job_retry=None,
    )

    with pytest.raises(google.api_core.exceptions.InternalServerError):
        list(rows)  # Raise the last error


def test_retry_failed_jobs_after_retry_failed(client):
    """
    If at first you don't succeed, maybe you will later. :)
    """

    freezegun.freeze_time(auto_tick_seconds=1)
    client = mock.create_autospec(Client)
    client._call_api.__name__ = "_call_api"
    client._call_api.__qualname__ = "Client._call_api"
    client._call_api.__annotations__ = {}
    client._call_api.__type_params__ = ()
    client._call_api.side_effect = (
        {
            "jobReference": {
                "projectId": "response-project",
                "jobId": "abc",
                "location": "response-location",
            },
            "jobComplete": False,
        },
        google.api_core.exceptions.InternalServerError(
            "job_retry me", errors=[{"reason": "rateLimitExceeded"}]
        ),
        # Responses for subsequent success
        {
            "jobReference": {
                "jobId": "job1",
                "projectId": "project",
                "location": "location",
            },
            "jobComplete": False,
        },
        google.api_core.exceptions.BadRequest(
            "job_retry me", errors=[{"reason": "backendError"}]
        ),
        google.api_core.exceptions.InternalServerError(
            "job_retry me", errors=[{"reason": "rateLimitExceeded"}]
        ),
        google.api_core.exceptions.BadRequest(
            "job_retry me", errors=[{"reason": "backendError"}]
        ),
        {
            "jobReference": {
                "projectId": "response-project",
                "jobId": "abc",
                "location": "response-location",
            },
            "jobComplete": True,
            "schema": {
                "fields": [
                    {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "age", "type": "INT64", "mode": "NULLABLE"},
                ],
            },
            "rows": [
                {"f": [{"v": "Whillma Phlyntstone"}, {"v": "27"}]},
                {"f": [{"v": "Bhetty Rhubble"}, {"v": "28"}]},
                {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
                {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            ],
        },
    )

    rows = _job_helpers.query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        page_size=None,
        max_results=None,
        retry=DEFAULT_RETRY,
        job_retry=DEFAULT_JOB_RETRY,
    )
    # TODO: different test to test if it retries until it times out
    with pytest.raises(google.api_core.exceptions.RetryError):
        list(rows)  # Trigger the initial retry failure

    # Second attempt with successful retries
    rows = _job_helpers.query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        page_size=None,
        max_results=None,
        retry=DEFAULT_RETRY,
        job_retry=DEFAULT_RETRY,
    )

    assert len(list(rows)) == 4


def test_raises_on_job_retry_on_query_with_non_retryable_jobs(client):
    with pytest.raises(
        TypeError,
        match=re.escape(
            "`job_retry` was provided, but the returned job is"
            " not retryable, because a custom `job_id` was"
            " provided."
        ),
    ):
        client.query("select 42", job_id=42, job_retry=google.api_core.retry.Retry())


def test_raises_on_job_retry_on_result_with_non_retryable_jobs(client):
    client._connection = make_connection({})
    job = client.query("select 42", job_id=42)
    with pytest.raises(
        TypeError,
        match=re.escape(
            "`job_retry` was provided, but this job is"
            " not retryable, because a custom `job_id` was"
            " provided to the query that created this job."
        ),
    ):
        job.result(job_retry=google.api_core.retry.Retry())


def test_query_and_wait_retries_job_for_DDL_queries():
    """
    Specific test for retrying DDL queries with "jobRateLimitExceeded" error:
    https://github.com/googleapis/python-bigquery/issues/1790
    """
    freezegun.freeze_time(auto_tick_seconds=1)
    client = mock.create_autospec(Client)
    client._call_api.__name__ = "_call_api"
    client._call_api.__qualname__ = "Client._call_api"
    client._call_api.__annotations__ = {}
    client._call_api.__type_params__ = ()
    client._call_api.side_effect = (
        {
            "jobReference": {
                "projectId": "response-project",
                "jobId": "abc",
                "location": "response-location",
            },
            "jobComplete": False,
        },
        google.api_core.exceptions.InternalServerError(
            "job_retry me", errors=[{"reason": "jobRateLimitExceeded"}]
        ),
        google.api_core.exceptions.BadRequest(
            "retry me", errors=[{"reason": "jobRateLimitExceeded"}]
        ),
        {
            "jobReference": {
                "projectId": "response-project",
                "jobId": "abc",
                "location": "response-location",
            },
            "jobComplete": True,
            "schema": {
                "fields": [
                    {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "age", "type": "INT64", "mode": "NULLABLE"},
                ],
            },
            "rows": [
                {"f": [{"v": "Whillma Phlyntstone"}, {"v": "27"}]},
                {"f": [{"v": "Bhetty Rhubble"}, {"v": "28"}]},
                {"f": [{"v": "Phred Phlyntstone"}, {"v": "32"}]},
                {"f": [{"v": "Bharney Rhubble"}, {"v": "33"}]},
            ],
        },
    )
    rows = _job_helpers.query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        page_size=None,
        max_results=None,
        retry=DEFAULT_RETRY,
        job_retry=DEFAULT_JOB_RETRY,
    )
    assert len(list(rows)) == 4

    # Relevant docs for the REST API path: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
    # and https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults
    query_request_path = "/projects/request-project/queries"

    calls = client._call_api.call_args_list
    _, kwargs = calls[0]
    assert kwargs["method"] == "POST"
    assert kwargs["path"] == query_request_path

    # TODO: Add assertion statements for response paths after PR#1797 is fixed

    _, kwargs = calls[3]
    assert kwargs["method"] == "POST"
    assert kwargs["path"] == query_request_path
