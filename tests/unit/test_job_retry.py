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
from unittest import mock

import pytest

import google.api_core.exceptions
import google.api_core.retry
import freezegun

from google.cloud.bigquery.client import Client
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery.retry import DEFAULT_JOB_RETRY

from .helpers import make_connection


# With job_retry_on_query, we're testing 4 scenarios:
# - No `job_retry` passed, retry on default rateLimitExceeded.
# - Pass NotFound retry to `query`.
# - Pass NotFound retry to `result`.
# - Pass BadRequest retry to query, with the value passed to `result` overriding.
@pytest.mark.parametrize("job_retry_on_query", [None, "Query", "Result", "Both"])
@mock.patch("time.sleep")
def test_retry_failed_jobs(sleep, client, job_retry_on_query):
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
        reason = "rateLimitExceeded"
    else:
        reason = "notFound"

    err = dict(reason=reason)
    responses = [
        dict(status=dict(state="DONE", errors=[err], errorResult=err)),
        dict(status=dict(state="DONE", errors=[err], errorResult=err)),
        dict(status=dict(state="DONE", errors=[err], errorResult=err)),
        dict(status=dict(state="DONE")),
        dict(rows=[{"f": [{"v": "1"}]}], totalRows="1"),
    ]

    def api_request(method, path, query_params=None, data=None, **kw):
        response = responses.pop(0)
        if data:
            response["jobReference"] = data["jobReference"]
        else:
            response["jobReference"] = dict(
                jobId=path.split("/")[-1], projectId="PROJECT"
            )
        return response

    conn = client._connection = make_connection()
    conn.api_request.side_effect = api_request

    if job_retry_on_query == "Query":
        job_retry = dict(job_retry=retry_notfound)
    elif job_retry_on_query == "Both":
        # This will be overridden in `result`
        job_retry = dict(job_retry=retry_badrequest)
    else:
        job_retry = {}
    job = client.query("select 1", **job_retry)

    orig_job_id = job.job_id
    job_retry = (
        dict(job_retry=retry_notfound)
        if job_retry_on_query in ("Result", "Both")
        else {}
    )
    result = job.result(**job_retry)
    assert result.total_rows == 1
    assert not responses  # We made all the calls we expected to.

    # The job adjusts it's job id based on the id of the last attempt.
    assert job.job_id != orig_job_id
    assert job.job_id == conn.mock_calls[3][2]["data"]["jobReference"]["jobId"]

    # We had to sleep three times
    assert len(sleep.mock_calls) == 3

    # Sleeps are random, however they're more than 0
    assert min(c[1][0] for c in sleep.mock_calls) > 0

    # They're at most 2 * (multiplier**(number of sleeps - 1)) * initial
    # The default multiplier is 2
    assert max(c[1][0] for c in sleep.mock_calls) <= 8

    # We can ask for the result again:
    responses = [
        dict(rows=[{"f": [{"v": "1"}]}], totalRows="1"),
    ]
    orig_job_id = job.job_id
    result = job.result()
    assert result.total_rows == 1
    assert not responses  # We made all the calls we expected to.

    # We wouldn't (and didn't) fail, because we're dealing with a successful job.
    # So the job id hasn't changed.
    assert job.job_id == orig_job_id


# With job_retry_on_query, we're testing 4 scenarios:
# - Pass None retry to `query`.
# - Pass None retry to `result`.
@pytest.mark.parametrize("job_retry_on_query", ["Query", "Result"])
@mock.patch("time.sleep")
def test_disable_retry_failed_jobs(sleep, client, job_retry_on_query):
    """
    Test retry of job failures, as opposed to API-invocation failures.
    """
    err = dict(reason="rateLimitExceeded")
    responses = [dict(status=dict(state="DONE", errors=[err], errorResult=err))] * 3

    def api_request(method, path, query_params=None, data=None, **kw):
        response = responses.pop(0)
        response["jobReference"] = data["jobReference"]
        return response

    conn = client._connection = make_connection()
    conn.api_request.side_effect = api_request

    if job_retry_on_query == "Query":
        job_retry = dict(job_retry=None)
    else:
        job_retry = {}
    job = client.query("select 1", **job_retry)

    orig_job_id = job.job_id
    job_retry = dict(job_retry=None) if job_retry_on_query == "Result" else {}
    with pytest.raises(google.api_core.exceptions.Forbidden):
        job.result(**job_retry)

    assert job.job_id == orig_job_id
    assert len(sleep.mock_calls) == 0


@mock.patch("time.sleep")
def test_retry_failed_jobs_after_retry_failed(sleep, client):
    """
    If at first you don't succeed, maybe you will later. :)
    """
    conn = client._connection = make_connection()

    with freezegun.freeze_time("2024-01-01 00:00:00") as frozen_datetime:
        err = dict(reason="rateLimitExceeded")

        def api_request(method, path, query_params=None, data=None, **kw):
            calls = sleep.mock_calls
            if calls:
                frozen_datetime.tick(delta=datetime.timedelta(seconds=calls[-1][1][0]))
            response = dict(status=dict(state="DONE", errors=[err], errorResult=err))
            response["jobReference"] = data["jobReference"]
            return response

        conn.api_request.side_effect = api_request

        job = client.query("select 1")
        orig_job_id = job.job_id

        with pytest.raises(google.api_core.exceptions.RetryError):
            job.result()

        # We never got a successful job, so the job id never changed:
        assert job.job_id == orig_job_id

        # We failed because we couldn't succeed after 120 seconds.
        # But we can try again:
        err2 = dict(reason="backendError")  # We also retry on this
        responses = [
            dict(status=dict(state="DONE", errors=[err2], errorResult=err2)),
            dict(status=dict(state="DONE", errors=[err], errorResult=err)),
            dict(status=dict(state="DONE", errors=[err2], errorResult=err2)),
            dict(status=dict(state="DONE")),
            dict(rows=[{"f": [{"v": "1"}]}], totalRows="1"),
        ]

        def api_request(method, path, query_params=None, data=None, **kw):
            calls = sleep.mock_calls
            frozen_datetime.tick(delta=datetime.timedelta(seconds=calls[-1][1][0]))
            response = responses.pop(0)
            if data:
                response["jobReference"] = data["jobReference"]
            else:
                response["jobReference"] = dict(
                    jobId=path.split("/")[-1], projectId="PROJECT"
                )
            return response

        conn.api_request.side_effect = api_request
        result = job.result()
        assert result.total_rows == 1
        assert not responses  # We made all the calls we expected to.
        assert job.job_id != orig_job_id


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
        retry=DEFAULT_JOB_RETRY,
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
