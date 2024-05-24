import copy
import collections
import datetime
import decimal
import email
import gzip
import http.client
import io
import itertools
import json
import operator
import unittest
import warnings
import freezegun
import mock
import requests
import packaging
import pytest
import sys
import inspect

if sys.version_info >= (3, 9):
    import asyncio

try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata

try:
    import pandas
except (ImportError, AttributeError):  # pragma: NO COVER
    pandas = None

try:
    import opentelemetry
except ImportError:
    opentelemetry = None

if opentelemetry is not None:
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
            InMemorySpanExporter,
        )
    except (ImportError, AttributeError) as exc:  # pragma: NO COVER
        msg = "Error importing from opentelemetry, is the installed version compatible?"
        raise ImportError(msg) from exc

try:
    import pyarrow
except (ImportError, AttributeError):  # pragma: NO COVER
    pyarrow = None

import google.api_core.exceptions
from google.api_core import client_info
import google.cloud._helpers
from google.cloud import bigquery

from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery import exceptions
from google.cloud.bigquery import ParquetOptions
from google.cloud.bigquery.retry import DEFAULT_TIMEOUT
import google.cloud.bigquery.table

try:
    from google.cloud import bigquery_storage
except (ImportError, AttributeError):  # pragma: NO COVER
    bigquery_storage = None
from test_utils.imports import maybe_fail_import
from tests.unit.helpers import make_connection

if pandas is not None:
    PANDAS_INSTALLED_VERSION = metadata.version("pandas")
else:
    PANDAS_INSTALLED_VERSION = "0.0.0"

from google.cloud.bigquery.retry import (
    DEFAULT_ASYNC_JOB_RETRY,
    DEFAULT_ASYNC_RETRY,
    DEFAULT_TIMEOUT,
)
from google.api_core import retry_async as retries
from google.cloud.bigquery.async_client import AsyncClient, async_query_and_wait
from google.cloud.bigquery.client import Client
from google.cloud.bigquery.job import query as job_query


def asyncio_run(async_func):
    def wrapper(*args, **kwargs):
        return asyncio.run(async_func(*args, **kwargs))

    wrapper.__signature__ = inspect.signature(
        async_func
    )  # without this, fixtures are not injected

    return wrapper


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):
    PROJECT = "PROJECT"
    DS_ID = "DATASET_ID"
    TABLE_ID = "TABLE_ID"
    MODEL_ID = "MODEL_ID"
    TABLE_REF = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)
    KMS_KEY_NAME = "projects/1/locations/us/keyRings/1/cryptoKeys/1"
    LOCATION = "us-central"

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.async_client import AsyncClient

        return AsyncClient

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_table_resource(self):
        return {
            "id": "%s:%s:%s" % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            "tableReference": {
                "projectId": self.PROJECT,
                "datasetId": self.DS_ID,
                "tableId": self.TABLE_ID,
            },
        }

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    def test_ctor_defaults(self):
        from google.cloud.bigquery._http import Connection

        creds = _make_credentials()
        http = object()
        client = self._make_one(
            project=self.PROJECT, credentials=creds, _http=http
        )._client
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)
        self.assertIsNone(client.location)
        self.assertEqual(
            client._connection.API_BASE_URL, Connection.DEFAULT_API_ENDPOINT
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    def test_ctor_w_empty_client_options(self):
        from google.api_core.client_options import ClientOptions

        creds = _make_credentials()
        http = object()
        client_options = ClientOptions()
        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            client_options=client_options,
        )._client
        self.assertEqual(
            client._connection.API_BASE_URL, client._connection.DEFAULT_API_ENDPOINT
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    def test_ctor_w_client_options_dict(self):
        creds = _make_credentials()
        http = object()
        client_options = {"api_endpoint": "https://www.foo-googleapis.com"}
        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            client_options=client_options,
        )._client
        self.assertEqual(
            client._connection.API_BASE_URL, "https://www.foo-googleapis.com"
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    def test_ctor_w_client_options_object(self):
        from google.api_core.client_options import ClientOptions

        creds = _make_credentials()
        http = object()
        client_options = ClientOptions(api_endpoint="https://www.foo-googleapis.com")
        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            client_options=client_options,
        )._client
        self.assertEqual(
            client._connection.API_BASE_URL, "https://www.foo-googleapis.com"
        )

    @pytest.mark.skipif(
        packaging.version.parse(getattr(google.api_core, "__version__", "0.0.0"))
        < packaging.version.Version("2.15.0"),
        reason="universe_domain not supported with google-api-core < 2.15.0",
    )
    def test_ctor_w_client_options_universe(self):
        creds = _make_credentials()
        http = object()
        client_options = {"universe_domain": "foo.com"}
        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            client_options=client_options,
        )._client
        self.assertEqual(client._connection.API_BASE_URL, "https://bigquery.foo.com")

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    def test_ctor_w_location(self):
        from google.cloud.bigquery._http import Connection

        creds = _make_credentials()
        http = object()
        location = "us-central"
        client = self._make_one(
            project=self.PROJECT, credentials=creds, _http=http, location=location
        )._client
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)
        self.assertEqual(client.location, location)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    def test_ctor_w_query_job_config(self):
        from google.cloud.bigquery._http import Connection
        from google.cloud.bigquery import QueryJobConfig

        creds = _make_credentials()
        http = object()
        location = "us-central"
        job_config = QueryJobConfig()
        job_config.dry_run = True

        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            location=location,
            default_query_job_config=job_config,
        )._client
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)
        self.assertEqual(client.location, location)

        self.assertIsInstance(client._default_query_job_config, QueryJobConfig)
        self.assertTrue(client._default_query_job_config.dry_run)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    def test_ctor_w_load_job_config(self):
        from google.cloud.bigquery._http import Connection
        from google.cloud.bigquery import LoadJobConfig

        creds = _make_credentials()
        http = object()
        location = "us-central"
        job_config = LoadJobConfig()
        job_config.create_session = True

        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            location=location,
            default_load_job_config=job_config,
        )._client
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)
        self.assertEqual(client.location, location)

        self.assertIsInstance(client._default_load_job_config, LoadJobConfig)
        self.assertTrue(client._default_load_job_config.create_session)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_query_and_wait_defaults(self):
        query = "select count(*) from `bigquery-public-data.usa_names.usa_1910_2013`"
        jobs_query_response = {
            "jobComplete": True,
            "schema": {
                "fields": [
                    {
                        "name": "f0_",
                        "type": "INTEGER",
                        "mode": "NULLABLE",
                    },
                ],
            },
            "totalRows": "1",
            "rows": [{"f": [{"v": "5552452"}]}],
            "queryId": "job_abcDEF_",
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._client._connection = make_connection(jobs_query_response)

        rows = await client.query_and_wait(query)

        self.assertIsInstance(rows, google.cloud.bigquery.table.RowIterator)
        self.assertEqual(rows.query_id, "job_abcDEF_")
        self.assertEqual(rows.total_rows, 1)
        # No job reference in the response should be OK for completed query.
        self.assertIsNone(rows.job_id)
        self.assertIsNone(rows.project)
        self.assertIsNone(rows.location)

        # Verify the request we send is to jobs.query.
        conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], "/projects/PROJECT/queries")
        self.assertEqual(req["timeout"], DEFAULT_TIMEOUT)
        sent = req["data"]
        self.assertEqual(sent["query"], query)
        self.assertFalse(sent["useLegacySql"])

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_query_and_wait_w_default_query_job_config(self):
        from google.cloud.bigquery import job

        query = "select count(*) from `bigquery-public-data.usa_names.usa_1910_2013`"
        jobs_query_response = {
            "jobComplete": True,
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
            default_query_job_config=job.QueryJobConfig(
                labels={
                    "default-label": "default-value",
                },
            ),
        )
        conn = client._client._connection = make_connection(jobs_query_response)

        future_result = client.query_and_wait(query)
        _ = await future_result

        # Verify the request we send is to jobs.query.
        # Instantiate my query path, dumping call stacks to see where I am. Get the address of my mocked call and actual call thats invoked, see if thats the same. See if my mocked thing is the thing getting invoked or not.
        # conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], f"/projects/{self.PROJECT}/queries")
        sent = req["data"]
        self.assertEqual(sent["labels"], {"default-label": "default-value"})

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_query_and_wait_w_job_config(self):
        from google.cloud.bigquery import job

        query = "select count(*) from `bigquery-public-data.usa_names.usa_1910_2013`"
        jobs_query_response = {
            "jobComplete": True,
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            _http=http,
        )
        conn = client._client._connection = make_connection(jobs_query_response)

        future_result = client.query_and_wait(
            query,
            job_config=job.QueryJobConfig(
                labels={
                    "job_config-label": "job_config-value",
                },
            ),
        )
        rows = await future_result

        # Verify the request we send is to jobs.query.
        # conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], f"/projects/{self.PROJECT}/queries")
        sent = req["data"]
        self.assertEqual(sent["labels"], {"job_config-label": "job_config-value"})

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_query_and_wait_w_location(self):
        query = "select count(*) from `bigquery-public-data.usa_names.usa_1910_2013`"
        jobs_query_response = {
            "jobComplete": True,
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._client._connection = make_connection(jobs_query_response)

        future_result = client.query_and_wait(query, location="not-the-client-location")
        _ = await future_result

        # Verify the request we send is to jobs.query.
        # conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], f"/projects/{self.PROJECT}/queries")
        sent = req["data"]
        self.assertEqual(sent["location"], "not-the-client-location")

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_query_and_wait_w_project(self):
        query = "select count(*) from `bigquery-public-data.usa_names.usa_1910_2013`"
        jobs_query_response = {
            "jobComplete": True,
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        conn = client._client._connection = make_connection(jobs_query_response)

        future_result = client.query_and_wait(query, project="not-the-client-project")
        _ = await future_result

        # Verify the request we send is to jobs.query.
        # conn.api_request.assert_called_once()
        _, req = conn.api_request.call_args
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["path"], "/projects/not-the-client-project/queries")

@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 or higher"
)
@asyncio_run
async def test_query_and_wait_retries_job():
    freezegun.freeze_time(auto_tick_seconds=100)
    client = mock.create_autospec(AsyncClient)
    client._client = mock.create_autospec(Client)
    client._call_api.__name__ = "_call_api"
    client._call_api.__qualname__ = "Client._call_api"
    client._call_api.__annotations__ = {}
    client._call_api.__type_params__ = ()
    client._call_api.side_effect = (
        google.api_core.exceptions.BadGateway("retry me"),
        google.api_core.exceptions.InternalServerError("job_retry me"),
        google.api_core.exceptions.BadGateway("retry me"),
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
    rows = await async_query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        page_size=None,
        max_results=None,
        retry=retries.AsyncRetry(
            lambda exc: isinstance(exc, google.api_core.exceptions.BadGateway),
            multiplier=1.0,
        ).with_deadline(
            200.0
        ),  # Since auto_tick_seconds is 100, we should get at least 1 retry.
        job_retry=retries.AsyncRetry(
            lambda exc: isinstance(exc, google.api_core.exceptions.InternalServerError),
            multiplier=1.0,
        ).with_deadline(600.0),
    )
    assert len(list(rows)) == 4

    # For this code path, where the query has finished immediately, we should
    # only be calling the jobs.query API and no other request path.
    request_path = "/projects/request-project/queries"
    for call in client._call_api.call_args_list:
        _, kwargs = call
        assert kwargs["method"] == "POST"
        assert kwargs["path"] == request_path


@freezegun.freeze_time(auto_tick_seconds=100)
@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 or higher"
)
@asyncio_run
async def test_query_and_wait_retries_job_times_out():
    client = mock.create_autospec(AsyncClient)
    client._client = mock.create_autospec(Client)
    client._call_api.__name__ = "_call_api"
    client._call_api.__qualname__ = "Client._call_api"
    client._call_api.__annotations__ = {}
    client._call_api.__type_params__ = ()
    client._call_api.side_effect = (
        google.api_core.exceptions.BadGateway("retry me"),
        google.api_core.exceptions.InternalServerError("job_retry me"),
        google.api_core.exceptions.BadGateway("retry me"),
        google.api_core.exceptions.InternalServerError("job_retry me"),
    )

    with pytest.raises(google.api_core.exceptions.RetryError) as exc_info:
        await async_query_and_wait(
            client,
            query="SELECT 1",
            location="request-location",
            project="request-project",
            job_config=None,
            page_size=None,
            max_results=None,
            retry=retries.AsyncRetry(
                lambda exc: isinstance(exc, google.api_core.exceptions.BadGateway),
                multiplier=1.0,
            ).with_deadline(
                200.0
            ),  # Since auto_tick_seconds is 100, we should get at least 1 retry.
            job_retry=retries.AsyncRetry(
                lambda exc: isinstance(
                    exc, google.api_core.exceptions.InternalServerError
                ),
                multiplier=1.0,
            ).with_deadline(400.0),
        )

    assert isinstance(
        exc_info.value.cause, google.api_core.exceptions.InternalServerError
    )

@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 or higher"
)
@asyncio_run
async def test_query_and_wait_sets_job_creation_mode(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(
        "QUERY_PREVIEW_ENABLED",
        # The comparison should be case insensitive.
        "TrUe",
    )
    client = mock.create_autospec(AsyncClient)
    client._client = mock.create_autospec(Client)
    client._call_api.return_value = {
        "jobReference": {
            "projectId": "response-project",
            "jobId": "abc",
            "location": "response-location",
        },
        "jobComplete": True,
    }
    async_query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        retry=None,
        job_retry=None,
        page_size=None,
        max_results=None,
    )

    # We should only call jobs.query once, no additional row requests needed.
    request_path = "/projects/request-project/queries"
    client._call_api.assert_called_once_with(
        None,  # retry
        span_name="BigQuery.query",
        span_attributes={"path": request_path},
        method="POST",
        path=request_path,
        data={
            "query": "SELECT 1",
            "location": "request-location",
            "useLegacySql": False,
            "formatOptions": {
                "useInt64Timestamp": True,
            },
            "requestId": mock.ANY,
            "jobCreationMode": "JOB_CREATION_OPTIONAL",
        },
        timeout=None,
    )

@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 or higher"
)
@asyncio_run
async def test_query_and_wait_sets_location():
    client = mock.create_autospec(AsyncClient)
    client._client = mock.create_autospec(Client)
    client._call_api.return_value = {
        "jobReference": {
            "projectId": "response-project",
            "jobId": "abc",
            "location": "response-location",
        },
        "jobComplete": True,
    }
    rows = await async_query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        retry=None,
        job_retry=None,
        page_size=None,
        max_results=None,
    )
    assert rows.location == "response-location"

    # We should only call jobs.query once, no additional row requests needed.
    request_path = "/projects/request-project/queries"
    client._call_api.assert_called_once_with(
        None,  # retry
        span_name="BigQuery.query",
        span_attributes={"path": request_path},
        method="POST",
        path=request_path,
        data={
            "query": "SELECT 1",
            "location": "request-location",
            "useLegacySql": False,
            "formatOptions": {
                "useInt64Timestamp": True,
            },
            "requestId": mock.ANY,
        },
        timeout=None,
    )


@pytest.mark.parametrize(
    ("max_results", "page_size", "expected"),
    [
        (10, None, 10),
        (None, 11, 11),
        (12, 100, 12),
        (100, 13, 13),
    ],
)
@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 or higher"
)
@asyncio_run
async def test_query_and_wait_sets_max_results(max_results, page_size, expected):
    client = mock.create_autospec(AsyncClient)
    client._client = mock.create_autospec(Client)
    client._call_api.return_value = {
        "jobReference": {
            "projectId": "response-project",
            "jobId": "abc",
            "location": "response-location",
        },
        "jobComplete": True,
    }
    rows = await async_query_and_wait(
        client,
        query="SELECT 1",
        location="request-location",
        project="request-project",
        job_config=None,
        retry=None,
        job_retry=None,
        page_size=page_size,
        max_results=max_results,
    )
    assert rows.location == "response-location"

    # We should only call jobs.query once, no additional row requests needed.
    request_path = "/projects/request-project/queries"
    client._call_api.assert_called_once_with(
        None,  # retry
        span_name="BigQuery.query",
        span_attributes={"path": request_path},
        method="POST",
        path=request_path,
        data={
            "query": "SELECT 1",
            "location": "request-location",
            "useLegacySql": False,
            "formatOptions": {
                "useInt64Timestamp": True,
            },
            "requestId": mock.ANY,
            "maxResults": expected,
        },
        timeout=None,
    )

@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 or higher"
)
@asyncio_run
async def test_query_and_wait_caches_completed_query_results_one_page():
    client = mock.create_autospec(AsyncClient)
    client._client = mock.create_autospec(Client)
    client._call_api.return_value = {
        "jobReference": {
            "projectId": "response-project",
            "jobId": "abc",
            "location": "US",
        },
        "jobComplete": True,
        "queryId": "xyz",
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
        # Even though totalRows > len(rows), we should use the presence of a
        # next page token to decide if there are any more pages.
        "totalRows": 8,
    }
    rows = await async_query_and_wait(
        client,
        query="SELECT full_name, age FROM people;",
        job_config=None,
        location=None,
        project="request-project",
        retry=None,
        job_retry=None,
        page_size=None,
        max_results=None,
    )
    rows_list = list(rows)
    assert rows.project == "response-project"
    assert rows.job_id == "abc"
    assert rows.location == "US"
    assert rows.query_id == "xyz"
    assert rows.total_rows == 8
    assert len(rows_list) == 4

    # We should only call jobs.query once, no additional row requests needed.
    request_path = "/projects/request-project/queries"
    client._call_api.assert_called_once_with(
        None,  # retry
        span_name="BigQuery.query",
        span_attributes={"path": request_path},
        method="POST",
        path=request_path,
        data={
            "query": "SELECT full_name, age FROM people;",
            "useLegacySql": False,
            "formatOptions": {
                "useInt64Timestamp": True,
            },
            "requestId": mock.ANY,
        },
        timeout=None,
    )

@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 or higher"
)
@asyncio_run
async def test_query_and_wait_caches_completed_query_results_one_page_no_rows():
    client = mock.create_autospec(AsyncClient)
    client._client = mock.create_autospec(Client)
    client._call_api.return_value = {
        "jobReference": {
            "projectId": "response-project",
            "jobId": "abc",
            "location": "US",
        },
        "jobComplete": True,
        "queryId": "xyz",
    }
    rows = await async_query_and_wait(
        client,
        query="CREATE TABLE abc;",
        project="request-project",
        job_config=None,
        location=None,
        retry=None,
        job_retry=None,
        page_size=None,
        max_results=None,
    )
    assert rows.project == "response-project"
    assert rows.job_id == "abc"
    assert rows.location == "US"
    assert rows.query_id == "xyz"
    assert list(rows) == []

    # We should only call jobs.query once, no additional row requests needed.
    request_path = "/projects/request-project/queries"
    client._call_api.assert_called_once_with(
        None,  # retry
        span_name="BigQuery.query",
        span_attributes={"path": request_path},
        method="POST",
        path=request_path,
        data={
            "query": "CREATE TABLE abc;",
            "useLegacySql": False,
            "formatOptions": {
                "useInt64Timestamp": True,
            },
            "requestId": mock.ANY,
        },
        timeout=None,
    )
