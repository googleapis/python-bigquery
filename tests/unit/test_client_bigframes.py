# Copyright 2025 Google LLC
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

"""Tests for Client features enabling the bigframes integration."""

from __future__ import annotations

from unittest import mock

import pytest

import google.auth.credentials
from google.api_core import exceptions
from google.cloud import bigquery
import google.cloud.bigquery.client
from google.cloud.bigquery import _job_helpers


PROJECT = "test-project"
LOCATION = "test-location"


def make_response(body, *, status_code: int = 200):
    response = mock.Mock()
    type(response).status_code = mock.PropertyMock(return_value=status_code)
    response.json.return_value = body
    return response


@pytest.fixture
def client():
    """A real client object with mocked API requests."""
    credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    http_session = mock.Mock()
    return google.cloud.bigquery.client.Client(
        project=PROJECT,
        credentials=credentials,
        _http=http_session,
        location=LOCATION,
    )


def test_query_and_wait_bigframes_callback(client):
    client._http.request.side_effect = [
        make_response(
            {
                # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
                "location": LOCATION,
                "queryId": "abcdefg",
                "totalRows": "100",
                "totalBytesProcessed": "123",
                "totalSlotMs": "987",
                "jobComplete": True,
            }
        ),
    ]
    callback = mock.Mock()
    client._query_and_wait_bigframes(query="SELECT 1", callback=callback)
    callback.assert_has_calls(
        [
            mock.call(
                _job_helpers.QuerySentEvent(
                    query="SELECT 1",
                    billing_project=PROJECT,
                    location=LOCATION,
                    # No job ID, because a basic query is elegible for jobs.query.
                    job_id=None,
                    request_id=mock.ANY,
                )
            ),
            mock.call(
                _job_helpers.QueryFinishedEvent(
                    billing_project=PROJECT,
                    location=LOCATION,
                    query_id="abcdefg",
                    total_rows=100,
                    total_bytes_processed=123,
                    slot_millis=987,
                    # No job ID or destination, because a basic query is elegible for jobs.query.
                    job_id=None,
                    destination=None,
                ),
            ),
        ]
    )


def test_query_and_wait_bigframes_with_job_callback(client):
    client._http.request.side_effect = [
        make_response(
            {
                # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
                # https://cloud.google.com/bigquery/docs/reference/rest/v2/Job
                "jobReference": {},
            }
        ),
        make_response(
            {
                # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
                # https://cloud.google.com/bigquery/docs/reference/rest/v2/Job
                "jobReference": {},
                "status": {"state": "DONE"},
            }
        ),
    ]
    callback = mock.Mock()
    config = bigquery.QueryJobConfig()
    config.destination = "proj.dset.table"
    client._query_and_wait_bigframes(
        query="SELECT 1", job_config=config, callback=callback
    )
    callback.assert_has_calls(
        [
            mock.call(
                _job_helpers.QuerySentEvent(
                    query="SELECT 1",
                    billing_project=PROJECT,
                    location=LOCATION,
                    # No job ID, because a basic query is elegible for jobs.query.
                    job_id=None,
                    request_id=mock.ANY,
                )
            ),
            mock.call(
                _job_helpers.QueryFinishedEvent(
                    billing_project=PROJECT,
                    location=LOCATION,
                    query_id="abcdefg",
                    total_rows=100,
                    total_bytes_processed=123,
                    slot_millis=987,
                    # No job ID or destination, because a basic query is elegible for jobs.query.
                    job_id=None,
                    destination=None,
                ),
            ),
        ]
    )


def test_query_and_wait_bigframes_with_query_retry_callbacks(client):
    client._http.request.side_effect = [
        exceptions.InternalServerError(
            "first try", errors=({"reason": "jobInternalError"},)
        ),
        make_response(
            {
                # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
                "location": LOCATION,
                "queryId": "abcdefg",
                "totalRows": "100",
                "totalBytesProcessed": "123",
                "totalSlotMs": "987",
                "jobComplete": True,
            }
        ),
    ]
    callback = mock.Mock()
    client._query_and_wait_bigframes(query="SELECT 1", callback=callback)
    callback.assert_has_calls(
        [
            mock.call(
                _job_helpers.QuerySentEvent(
                    query="SELECT 1",
                    billing_project=PROJECT,
                    location=LOCATION,
                    # No job ID, because a basic query is elegible for jobs.query.
                    job_id=None,
                    request_id=mock.ANY,
                )
            ),
            mock.call(
                _job_helpers.QueryRetryEvent(
                    query="SELECT 1",
                    billing_project=PROJECT,
                    location=LOCATION,
                    # No job ID, because a basic query is elegible for jobs.query.
                    job_id=None,
                    request_id=mock.ANY,
                )
            ),
            mock.call(
                _job_helpers.QueryFinishedEvent(
                    billing_project=PROJECT,
                    location=LOCATION,
                    query_id=mock.ANY,
                    total_rows=100,
                    total_bytes_processed=123,
                    slot_millis=987,
                    # No job ID or destination, because a basic query is elegible for jobs.query.
                    job_id=None,
                    destination=None,
                ),
            ),
        ]
    )
