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

from unittest import mock
import requests
import packaging
import pytest
import sys
import inspect
from tests.unit.test_client import _make_list_partitons_meta_info

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
from google.cloud.bigquery import async_client
from google.cloud.bigquery.async_client import AsyncClient
from google.cloud.bigquery.job import query as job_query


def asyncio_run(async_func):
    def wrapper(*args, **kwargs):
        return asyncio.run(async_func(*args, **kwargs))

    wrapper.__signature__ = inspect.signature(
        async_func
    )  # without this, fixtures are not injected

    return wrapper


def _make_credentials():
    from google.auth import _credentials_async as credentials

    return mock.Mock(spec=credentials.Credentials)


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
    async def test_get_job_miss_w_explict_project(self):
        from google.cloud.exceptions import NotFound

        OTHER_PROJECT = "OTHER_PROJECT"
        JOB_ID = "NONESUCH"
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._client._connection = make_connection()

        with self.assertRaises(NotFound):
            await client.get_job(JOB_ID, project=OTHER_PROJECT)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/OTHER_PROJECT/jobs/NONESUCH",
            query_params={"projection": "full"},
            timeout=DEFAULT_TIMEOUT,
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_get_job_miss_w_client_location(self):
        from google.cloud.exceptions import NotFound

        JOB_ID = "NONESUCH"
        creds = _make_credentials()
        client = self._make_one("client-proj", creds, location="client-loc")
        conn = client._client._connection = make_connection()

        with self.assertRaises(NotFound):
            await client.get_job(JOB_ID)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/client-proj/jobs/NONESUCH",
            query_params={"projection": "full", "location": "client-loc"},
            timeout=DEFAULT_TIMEOUT,
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_get_job_hit_w_timeout(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery.job import WriteDisposition

        JOB_ID = "query_job"
        QUERY_DESTINATION_TABLE = "query_destination_table"
        QUERY = "SELECT * from test_dataset:test_table"
        ASYNC_QUERY_DATA = {
            "id": "{}:{}".format(self.PROJECT, JOB_ID),
            "jobReference": {
                "projectId": "resource-proj",
                "jobId": "query_job",
                "location": "us-east1",
            },
            "state": "DONE",
            "configuration": {
                "query": {
                    "query": QUERY,
                    "destinationTable": {
                        "projectId": self.PROJECT,
                        "datasetId": self.DS_ID,
                        "tableId": QUERY_DESTINATION_TABLE,
                    },
                    "createDisposition": CreateDisposition.CREATE_IF_NEEDED,
                    "writeDisposition": WriteDisposition.WRITE_TRUNCATE,
                }
            },
        }
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._client._connection = make_connection(ASYNC_QUERY_DATA)
        job_from_resource = QueryJob.from_api_repr(ASYNC_QUERY_DATA, client._client)

        job = await client.get_job(job_from_resource, timeout=7.5)

        self.assertIsInstance(job, QueryJob)
        self.assertEqual(job.job_id, JOB_ID)
        self.assertEqual(job.project, "resource-proj")
        self.assertEqual(job.location, "us-east1")
        self.assertEqual(job.create_disposition, CreateDisposition.CREATE_IF_NEEDED)
        self.assertEqual(job.write_disposition, WriteDisposition.WRITE_TRUNCATE)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/resource-proj/jobs/query_job",
            query_params={"projection": "full", "location": "us-east1"},
            timeout=7.5,
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test__get_query_results_miss_w_explicit_project_and_timeout(self):
        from google.cloud.exceptions import NotFound

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._client._connection = make_connection()
        path = "/projects/other-project/queries/nothere"
        with self.assertRaises(NotFound):
            with mock.patch(
                "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
            ) as final_attributes:
                await client._get_query_results(
                    "nothere",
                    None,
                    project="other-project",
                    location=self.LOCATION,
                    timeout_ms=500,
                    timeout=420,
                )

        final_attributes.assert_called_once_with({"path": path}, client._client, None)

        conn.api_request.assert_called_once_with(
            method="GET",
            path=path,
            query_params={"maxResults": 0, "timeoutMs": 500, "location": self.LOCATION},
            timeout=420,
            headers={"X-Server-Timeout": "420"},
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test__get_query_results_miss_w_short_timeout(self):
        import google.cloud.bigquery.client
        from google.cloud.exceptions import NotFound

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._client._connection = make_connection()
        path = "/projects/other-project/queries/nothere"
        with self.assertRaises(NotFound):
            await client._get_query_results(
                "nothere",
                None,
                project="other-project",
                location=self.LOCATION,
                timeout_ms=500,
                timeout=1,
            )

        conn.api_request.assert_called_once_with(
            method="GET",
            path=path,
            query_params={"maxResults": 0, "timeoutMs": 500, "location": self.LOCATION},
            timeout=google.cloud.bigquery.client._MIN_GET_QUERY_RESULTS_TIMEOUT,
            headers={"X-Server-Timeout": "120"},
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test__get_query_results_miss_w_default_timeout(self):
        import google.cloud.bigquery.client
        from google.cloud.exceptions import NotFound

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._client._connection = make_connection()
        path = "/projects/other-project/queries/nothere"
        with self.assertRaises(NotFound):
            await client._get_query_results(
                "nothere",
                None,
                project="other-project",
                location=self.LOCATION,
                timeout_ms=500,
                timeout=object(),  # the api core default timeout
            )

        conn.api_request.assert_called_once_with(
            method="GET",
            path=path,
            query_params={"maxResults": 0, "timeoutMs": 500, "location": self.LOCATION},
            timeout=google.cloud.bigquery.client._MIN_GET_QUERY_RESULTS_TIMEOUT,
            headers={"X-Server-Timeout": "120"},  # why is this here?
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test__get_query_results_miss_w_client_location(self):
        from google.cloud.exceptions import NotFound

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds, location=self.LOCATION)
        conn = client._client._connection = make_connection()

        with self.assertRaises(NotFound):
            await client._get_query_results("nothere", None)

        conn.api_request.assert_called_once_with(
            method="GET",
            path="/projects/PROJECT/queries/nothere",
            query_params={"maxResults": 0, "location": self.LOCATION},
            timeout=DEFAULT_TIMEOUT,
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test__get_query_results_hit(self):
        job_id = "query_job"
        data = {
            "kind": "bigquery#getQueryResultsResponse",
            "etag": "some-tag",
            "schema": {
                "fields": [
                    {"name": "title", "type": "STRING", "mode": "NULLABLE"},
                    {"name": "unique_words", "type": "INTEGER", "mode": "NULLABLE"},
                ]
            },
            "jobReference": {"projectId": self.PROJECT, "jobId": job_id},
            "totalRows": "10",
            "totalBytesProcessed": "2464625",
            "jobComplete": True,
            "cacheHit": False,
        }

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        client._client._connection = make_connection(data)
        query_results = await client._get_query_results(job_id, None)

        self.assertEqual(query_results.total_rows, 10)
        self.assertTrue(query_results.complete)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_get_table(self):
        path = "projects/%s/datasets/%s/tables/%s" % (
            self.PROJECT,
            self.DS_ID,
            self.TABLE_ID,
        )
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        resource = self._make_table_resource()
        conn = client._client._connection = make_connection(resource)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            table = await client.get_table(self.TABLE_REF, timeout=7.5)

        final_attributes.assert_called_once_with({"path": "/%s" % path}, client, None)

        conn.api_request.assert_called_once_with(
            method="GET", path="/%s" % path, timeout=7.5
        )
        self.assertEqual(table.table_id, self.TABLE_ID)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_get_table_sets_user_agent(self):
        creds = _make_credentials()
        http = mock.create_autospec(requests.Session)
        mock_response = http.request(
            url=mock.ANY, method=mock.ANY, headers=mock.ANY, data=mock.ANY
        )
        http.reset_mock()
        http.is_mtls = False
        mock_response.status_code = 200
        mock_response.json.return_value = self._make_table_resource()
        user_agent_override = client_info.ClientInfo(user_agent="my-application/1.2.3")
        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            client_info=user_agent_override,
            _http=http,
        )

        await client.get_table(self.TABLE_REF)

        expected_user_agent = user_agent_override.to_user_agent()
        http.request.assert_called_once_with(
            url=mock.ANY,
            method="GET",
            headers={
                "X-Goog-API-Client": expected_user_agent,
                "Accept-Encoding": "gzip",
                "User-Agent": expected_user_agent,
            },
            data=mock.ANY,
            timeout=DEFAULT_TIMEOUT,
        )
        self.assertIn("my-application/1.2.3", expected_user_agent)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_list_partitions(self):
        from google.cloud.bigquery.table import Table

        rows = 3
        meta_info = _make_list_partitons_meta_info(
            self.PROJECT, self.DS_ID, self.TABLE_ID, rows
        )

        data = {
            "totalRows": str(rows),
            "rows": [
                {"f": [{"v": "20180101"}]},
                {"f": [{"v": "20180102"}]},
                {"f": [{"v": "20180103"}]},
            ],
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        client._client._connection = make_connection(meta_info, data)
        table = Table(self.TABLE_REF)

        partition_list = await client.list_partitions(table)
        self.assertEqual(len(partition_list), rows)
        self.assertIn("20180102", partition_list)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test_list_partitions_with_string_id(self):
        meta_info = _make_list_partitons_meta_info(
            self.PROJECT, self.DS_ID, self.TABLE_ID, 0
        )

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds, _http=http)
        client._client._connection = make_connection(meta_info, {})

        partition_list = await client.list_partitions(
            "{}.{}".format(self.DS_ID, self.TABLE_ID)
        )

        self.assertEqual(len(partition_list), 0)

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test__call_api_applying_custom_retry_on_timeout(self):
        from concurrent.futures import TimeoutError
        from google.cloud.bigquery.retry import DEFAULT_ASYNC_RETRY

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)

        api_request_patcher = mock.patch.object(
            client._client._connection,
            "api_request",
            side_effect=[TimeoutError, "result"],
        )
        retry = DEFAULT_ASYNC_RETRY.with_deadline(1).with_predicate(
            lambda exc: isinstance(exc, TimeoutError)
        )

        with api_request_patcher as fake_api_request:
            result = await client._call_api(retry, foo="bar")

        self.assertEqual(result, "result")
        self.assertEqual(
            fake_api_request.call_args_list,
            [mock.call(foo="bar"), mock.call(foo="bar")],  # was retried once
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test__call_api_span_creator_not_called(self):
        from concurrent.futures import TimeoutError
        from google.cloud.bigquery.retry import DEFAULT_ASYNC_RETRY

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)

        api_request_patcher = mock.patch.object(
            client._client._connection,
            "api_request",
            side_effect=[TimeoutError, "result"],
        )
        retry = DEFAULT_ASYNC_RETRY.with_deadline(1).with_predicate(
            lambda exc: isinstance(exc, TimeoutError)
        )

        with api_request_patcher:
            with mock.patch(
                "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
            ) as final_attributes:
                await client._call_api(retry)

            final_attributes.assert_not_called()

    @pytest.mark.skipif(
        sys.version_info < (3, 9), reason="requires python3.9 or higher"
    )
    @asyncio_run
    async def test__call_api_span_creator_called(self):
        from concurrent.futures import TimeoutError
        from google.cloud.bigquery.retry import DEFAULT_ASYNC_RETRY

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)

        api_request_patcher = mock.patch.object(
            client._client._connection,
            "api_request",
            side_effect=[TimeoutError, "result"],
        )
        retry = DEFAULT_ASYNC_RETRY.with_deadline(1).with_predicate(
            lambda exc: isinstance(exc, TimeoutError)
        )

        with api_request_patcher:
            with mock.patch(
                "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
            ) as final_attributes:
                await client._call_api(
                    retry,
                    span_name="test_name",
                    span_attributes={"test_attribute": "test_attribute-value"},
                )

            final_attributes.assert_called_once()

# make tests to show its cancelleable
# row iterator, paginated access, we need to make