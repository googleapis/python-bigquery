import datetime

import mock
import pytest

import google.api_core.exceptions

from .helpers import make_connection


@mock.patch("time.sleep")
def test_retry_failed_jobs(sleep, client):
    """
    Test retry of job failures, as opposed to API-invocation failures.
    """
    err = dict(reason="rateLimitExceeded")
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

    job = client.query("select 1")

    orig_job_id = job.job_id
    result = job.result()
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


@mock.patch("google.api_core.retry.datetime_helpers")
@mock.patch("time.sleep")
def test_retry_failed_jobs_after_retry_failed(sleep, datetime_helpers, client):
    """
    If at first you don't succeed, maybe you will later. :)
    """
    conn = client._connection = make_connection()

    datetime_helpers.utcnow.return_value = datetime.datetime(2021, 7, 29, 10, 43, 2)

    err = dict(reason="rateLimitExceeded")

    def api_request(method, path, query_params=None, data=None, **kw):
        calls = sleep.mock_calls
        if calls:
            datetime_helpers.utcnow.return_value += datetime.timedelta(
                seconds=calls[-1][1][0]
            )
        response = dict(status=dict(state="DONE", errors=[err], errorResult=err))
        response["jobReference"] = data["jobReference"]
        return response

    conn.api_request.side_effect = api_request

    job = client.query("select 1")
    orig_job_id = job.job_id

    with pytest.raises(google.api_core.exceptions.RetryError):
        job.result()

    # We never fot a successful job, so the job id never changed:
    assert job.job_id == orig_job_id

    # We failed because we couldn't succeed after 120 seconds.
    # But we can try again:
    responses = [
        dict(status=dict(state="DONE", errors=[err], errorResult=err)),
        dict(status=dict(state="DONE", errors=[err], errorResult=err)),
        dict(status=dict(state="DONE", errors=[err], errorResult=err)),
        dict(status=dict(state="DONE")),
        dict(rows=[{"f": [{"v": "1"}]}], totalRows="1"),
    ]

    def api_request(method, path, query_params=None, data=None, **kw):
        calls = sleep.mock_calls
        if calls:
            datetime_helpers.utcnow.return_value += datetime.timedelta(
                seconds=calls[-1][1][0]
            )
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
