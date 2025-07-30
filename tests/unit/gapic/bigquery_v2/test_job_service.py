# -*- coding: utf-8 -*-
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
#
import os
import re

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable, AsyncIterable
from google.protobuf import json_format
import json
import math
import pytest
from google.api_core import api_core_version
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

try:
    from google.auth.aio import credentials as ga_credentials_async

    HAS_GOOGLE_AUTH_AIO = True
except ImportError:  # pragma: NO COVER
    HAS_GOOGLE_AUTH_AIO = False

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.bigquery_v2.services.job_service import JobServiceClient
from google.cloud.bigquery_v2.services.job_service import pagers
from google.cloud.bigquery_v2.services.job_service import transports
from google.cloud.bigquery_v2.types import clustering
from google.cloud.bigquery_v2.types import data_format_options
from google.cloud.bigquery_v2.types import dataset_reference
from google.cloud.bigquery_v2.types import decimal_target_types
from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import error
from google.cloud.bigquery_v2.types import external_data_config
from google.cloud.bigquery_v2.types import file_set_specification_type
from google.cloud.bigquery_v2.types import hive_partitioning
from google.cloud.bigquery_v2.types import job
from google.cloud.bigquery_v2.types import job_config
from google.cloud.bigquery_v2.types import job_creation_reason
from google.cloud.bigquery_v2.types import job_reference
from google.cloud.bigquery_v2.types import job_stats
from google.cloud.bigquery_v2.types import job_status
from google.cloud.bigquery_v2.types import json_extension
from google.cloud.bigquery_v2.types import map_target_type
from google.cloud.bigquery_v2.types import model
from google.cloud.bigquery_v2.types import model_reference
from google.cloud.bigquery_v2.types import query_parameter
from google.cloud.bigquery_v2.types import range_partitioning
from google.cloud.bigquery_v2.types import routine_reference
from google.cloud.bigquery_v2.types import row_access_policy_reference
from google.cloud.bigquery_v2.types import session_info
from google.cloud.bigquery_v2.types import standard_sql
from google.cloud.bigquery_v2.types import system_variable
from google.cloud.bigquery_v2.types import table_reference
from google.cloud.bigquery_v2.types import table_schema
from google.cloud.bigquery_v2.types import time_partitioning
from google.cloud.bigquery_v2.types import udf_resource
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
import google.auth


CRED_INFO_JSON = {
    "credential_source": "/path/to/file",
    "credential_type": "service account credentials",
    "principal": "service-account@example.com",
}
CRED_INFO_STRING = json.dumps(CRED_INFO_JSON)


async def mock_async_gen(data, chunk_size=1):
    for i in range(0, len(data)):  # pragma: NO COVER
        chunk = data[i : i + chunk_size]
        yield chunk.encode("utf-8")


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# TODO: use async auth anon credentials by default once the minimum version of google-auth is upgraded.
# See related issue: https://github.com/googleapis/gapic-generator-python/issues/2107.
def async_anonymous_credentials():
    if HAS_GOOGLE_AUTH_AIO:
        return ga_credentials_async.AnonymousCredentials()
    return ga_credentials.AnonymousCredentials()


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert JobServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        JobServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        JobServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        JobServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        JobServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert JobServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert JobServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert JobServiceClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert JobServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            JobServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert JobServiceClient._read_environment_variables() == (False, "never", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert JobServiceClient._read_environment_variables() == (False, "always", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert JobServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            JobServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert JobServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert JobServiceClient._get_client_cert_source(None, False) is None
    assert (
        JobServiceClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        JobServiceClient._get_client_cert_source(mock_provided_cert_source, True)
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                JobServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                JobServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    JobServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(JobServiceClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = JobServiceClient._DEFAULT_UNIVERSE
    default_endpoint = JobServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = JobServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        JobServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        JobServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == JobServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        JobServiceClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        JobServiceClient._get_api_endpoint(None, None, default_universe, "always")
        == JobServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        JobServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == JobServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        JobServiceClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        JobServiceClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        JobServiceClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        JobServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        JobServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        JobServiceClient._get_universe_domain(None, None)
        == JobServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        JobServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "error_code,cred_info_json,show_cred_info",
    [
        (401, CRED_INFO_JSON, True),
        (403, CRED_INFO_JSON, True),
        (404, CRED_INFO_JSON, True),
        (500, CRED_INFO_JSON, False),
        (401, None, False),
        (403, None, False),
        (404, None, False),
        (500, None, False),
    ],
)
def test__add_cred_info_for_auth_errors(error_code, cred_info_json, show_cred_info):
    cred = mock.Mock(["get_cred_info"])
    cred.get_cred_info = mock.Mock(return_value=cred_info_json)
    client = JobServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=["foo"])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    if show_cred_info:
        assert error.details == ["foo", CRED_INFO_STRING]
    else:
        assert error.details == ["foo"]


@pytest.mark.parametrize("error_code", [401, 403, 404, 500])
def test__add_cred_info_for_auth_errors_no_get_cred_info(error_code):
    cred = mock.Mock([])
    assert not hasattr(cred, "get_cred_info")
    client = JobServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=[])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    assert error.details == []


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (JobServiceClient, "rest"),
    ],
)
def test_job_service_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "bigquery.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://bigquery.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.JobServiceRestTransport, "rest"),
    ],
)
def test_job_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (JobServiceClient, "rest"),
    ],
)
def test_job_service_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "bigquery.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://bigquery.googleapis.com"
        )


def test_job_service_client_get_transport_class():
    transport = JobServiceClient.get_transport_class()
    available_transports = [
        transports.JobServiceRestTransport,
    ]
    assert transport in available_transports

    transport = JobServiceClient.get_transport_class("rest")
    assert transport == transports.JobServiceRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (JobServiceClient, transports.JobServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    JobServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(JobServiceClient),
)
def test_job_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(JobServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(JobServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (JobServiceClient, transports.JobServiceRestTransport, "rest", "true"),
        (JobServiceClient, transports.JobServiceRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    JobServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(JobServiceClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_job_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [JobServiceClient])
@mock.patch.object(
    JobServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(JobServiceClient)
)
def test_job_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize("client_class", [JobServiceClient])
@mock.patch.object(
    JobServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(JobServiceClient),
)
def test_job_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = JobServiceClient._DEFAULT_UNIVERSE
    default_endpoint = JobServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = JobServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (JobServiceClient, transports.JobServiceRestTransport, "rest"),
    ],
)
def test_job_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (JobServiceClient, transports.JobServiceRestTransport, "rest", None),
    ],
)
def test_job_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_cancel_job_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.cancel_job in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.cancel_job] = mock_rpc

        request = {}
        client.cancel_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.cancel_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_cancel_job_rest_required_fields(request_type=job.CancelJobRequest):
    transport_class = transports.JobServiceRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["job_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).cancel_job._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["jobId"] = "job_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).cancel_job._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("location",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "jobId" in jsonified_request
    assert jsonified_request["jobId"] == "job_id_value"

    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = job.JobCancelResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = job.JobCancelResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.cancel_job(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_cancel_job_rest_unset_required_fields():
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.cancel_job._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("location",))
        & set(
            (
                "projectId",
                "jobId",
            )
        )
    )


def test_get_job_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_job in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_job] = mock_rpc

        request = {}
        client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_job_rest_required_fields(request_type=job.GetJobRequest):
    transport_class = transports.JobServiceRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["job_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_job._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["jobId"] = "job_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_job._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("location",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "jobId" in jsonified_request
    assert jsonified_request["jobId"] == "job_id_value"

    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = job.Job()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = job.Job.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_job(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_job_rest_unset_required_fields():
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_job._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("location",))
        & set(
            (
                "projectId",
                "jobId",
            )
        )
    )


def test_insert_job_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.insert_job in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.insert_job] = mock_rpc

        request = {}
        client.insert_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.insert_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_job_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_job in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_job] = mock_rpc

        request = {}
        client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_job(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_job_rest_required_fields(request_type=job.DeleteJobRequest):
    transport_class = transports.JobServiceRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["job_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_job._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["jobId"] = "job_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_job._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("location",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "jobId" in jsonified_request
    assert jsonified_request["jobId"] == "job_id_value"

    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.delete_job(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_job_rest_unset_required_fields():
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_job._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("location",))
        & set(
            (
                "projectId",
                "jobId",
            )
        )
    )


def test_list_jobs_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_jobs in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_jobs] = mock_rpc

        request = {}
        client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_jobs(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_jobs_rest_required_fields(request_type=job.ListJobsRequest):
    transport_class = transports.JobServiceRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_jobs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_jobs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "all_users",
            "max_creation_time",
            "max_results",
            "min_creation_time",
            "page_token",
            "parent_job_id",
            "projection",
            "state_filter",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"

    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = job.JobList()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = job.JobList.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_jobs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_jobs_rest_unset_required_fields():
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_jobs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allUsers",
                "maxCreationTime",
                "maxResults",
                "minCreationTime",
                "pageToken",
                "parentJobId",
                "projection",
                "stateFilter",
            )
        )
        & set(("projectId",))
    )


def test_list_jobs_rest_pager(transport: str = "rest"):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            job.JobList(
                jobs=[
                    job.ListFormatJob(),
                    job.ListFormatJob(),
                    job.ListFormatJob(),
                ],
                next_page_token="abc",
            ),
            job.JobList(
                jobs=[],
                next_page_token="def",
            ),
            job.JobList(
                jobs=[
                    job.ListFormatJob(),
                ],
                next_page_token="ghi",
            ),
            job.JobList(
                jobs=[
                    job.ListFormatJob(),
                    job.ListFormatJob(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(job.JobList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project_id": "sample1"}

        pager = client.list_jobs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, job.ListFormatJob) for i in results)

        pages = list(client.list_jobs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_query_results_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_query_results in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_query_results
        ] = mock_rpc

        request = {}
        client.get_query_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_query_results(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_query_results_rest_required_fields(
    request_type=job.GetQueryResultsRequest,
):
    transport_class = transports.JobServiceRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["job_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_query_results._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["jobId"] = "job_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_query_results._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "format_options",
            "location",
            "max_results",
            "page_token",
            "start_index",
            "timeout_ms",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "jobId" in jsonified_request
    assert jsonified_request["jobId"] == "job_id_value"

    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = job.GetQueryResultsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = job.GetQueryResultsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_query_results(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_query_results_rest_unset_required_fields():
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_query_results._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "formatOptions",
                "location",
                "maxResults",
                "pageToken",
                "startIndex",
                "timeoutMs",
            )
        )
        & set(
            (
                "projectId",
                "jobId",
            )
        )
    )


def test_query_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.query in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.query] = mock_rpc

        request = {}
        client.query(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.query(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_query_rest_required_fields(request_type=job.PostQueryRequest):
    transport_class = transports.JobServiceRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).query._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).query._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"

    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = job.QueryResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = job.QueryResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.query(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_query_rest_unset_required_fields():
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.query._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "projectId",
                "queryRequest",
            )
        )
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = JobServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = JobServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = JobServiceClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.JobServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_rest():
    transport = JobServiceClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_cancel_job_rest_bad_request(request_type=job.CancelJobRequest):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "job_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.cancel_job(request)


@pytest.mark.parametrize(
    "request_type",
    [
        job.CancelJobRequest,
        dict,
    ],
)
def test_cancel_job_rest_call_success(request_type):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "job_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = job.JobCancelResponse(
            kind="kind_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = job.JobCancelResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.cancel_job(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.JobCancelResponse)
    assert response.kind == "kind_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_cancel_job_rest_interceptors(null_interceptor):
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.JobServiceRestInterceptor(),
    )
    client = JobServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_cancel_job"
    ) as post, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_cancel_job_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.JobServiceRestInterceptor, "pre_cancel_job"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = job.CancelJobRequest.pb(job.CancelJobRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = job.JobCancelResponse.to_json(job.JobCancelResponse())
        req.return_value.content = return_value

        request = job.CancelJobRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = job.JobCancelResponse()
        post_with_metadata.return_value = job.JobCancelResponse(), metadata

        client.cancel_job(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_job_rest_bad_request(request_type=job.GetJobRequest):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "job_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_job(request)


@pytest.mark.parametrize(
    "request_type",
    [
        job.GetJobRequest,
        dict,
    ],
)
def test_get_job_rest_call_success(request_type):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "job_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = job.Job(
            kind="kind_value",
            etag="etag_value",
            id="id_value",
            self_link="self_link_value",
            user_email="user_email_value",
            principal_subject="principal_subject_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = job.Job.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_job(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.Job)
    assert response.kind == "kind_value"
    assert response.etag == "etag_value"
    assert response.id == "id_value"
    assert response.self_link == "self_link_value"
    assert response.user_email == "user_email_value"
    assert response.principal_subject == "principal_subject_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_job_rest_interceptors(null_interceptor):
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.JobServiceRestInterceptor(),
    )
    client = JobServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_get_job"
    ) as post, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_get_job_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.JobServiceRestInterceptor, "pre_get_job"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = job.GetJobRequest.pb(job.GetJobRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = job.Job.to_json(job.Job())
        req.return_value.content = return_value

        request = job.GetJobRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = job.Job()
        post_with_metadata.return_value = job.Job(), metadata

        client.get_job(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_insert_job_rest_bad_request(request_type=job.InsertJobRequest):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.insert_job(request)


@pytest.mark.parametrize(
    "request_type",
    [
        job.InsertJobRequest,
        dict,
    ],
)
def test_insert_job_rest_call_success(request_type):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request_init["job"] = {
        "kind": "kind_value",
        "etag": "etag_value",
        "id": "id_value",
        "self_link": "self_link_value",
        "user_email": "user_email_value",
        "configuration": {
            "job_type": "job_type_value",
            "query": {
                "query": "query_value",
                "destination_table": {
                    "project_id": "project_id_value",
                    "dataset_id": "dataset_id_value",
                    "table_id": "table_id_value",
                },
                "external_table_definitions": {},
                "user_defined_function_resources": [
                    {"resource_uri": {"value": "value_value"}, "inline_code": {}}
                ],
                "create_disposition": "create_disposition_value",
                "write_disposition": "write_disposition_value",
                "default_dataset": {
                    "dataset_id": "dataset_id_value",
                    "project_id": "project_id_value",
                },
                "priority": "priority_value",
                "allow_large_results": {"value": True},
                "use_query_cache": {},
                "flatten_results": {},
                "maximum_bytes_billed": {"value": 541},
                "use_legacy_sql": {},
                "parameter_mode": "parameter_mode_value",
                "query_parameters": [
                    {
                        "name": "name_value",
                        "parameter_type": {
                            "type_": "type__value",
                            "array_type": {},
                            "struct_types": [
                                {
                                    "name": "name_value",
                                    "type_": {},
                                    "description": "description_value",
                                }
                            ],
                            "range_element_type": {},
                        },
                        "parameter_value": {
                            "value": {},
                            "array_values": {},
                            "struct_values": {},
                            "range_value": {"start": {}, "end": {}},
                            "alt_struct_values": [
                                {
                                    "null_value": 0,
                                    "number_value": 0.1285,
                                    "string_value": "string_value_value",
                                    "bool_value": True,
                                    "struct_value": {"fields": {}},
                                    "list_value": {"values": {}},
                                }
                            ],
                        },
                    }
                ],
                "system_variables": {"types": {}, "values": {}},
                "schema_update_options": [
                    "schema_update_options_value1",
                    "schema_update_options_value2",
                ],
                "time_partitioning": {
                    "type_": "type__value",
                    "expiration_ms": {},
                    "field": {},
                },
                "range_partitioning": {
                    "field": "field_value",
                    "range_": {
                        "start": "start_value",
                        "end": "end_value",
                        "interval": "interval_value",
                    },
                },
                "clustering": {"fields": ["fields_value1", "fields_value2"]},
                "destination_encryption_configuration": {"kms_key_name": {}},
                "script_options": {
                    "statement_timeout_ms": {},
                    "statement_byte_budget": {},
                    "key_result_statement": 1,
                },
                "connection_properties": [{"key": "key_value", "value": "value_value"}],
                "create_session": {},
                "continuous": {},
                "write_incremental_results": True,
            },
            "load": {
                "source_uris": ["source_uris_value1", "source_uris_value2"],
                "file_set_spec_type": 1,
                "schema": {
                    "fields": [
                        {
                            "name": "name_value",
                            "type_": "type__value",
                            "mode": "mode_value",
                            "fields": {},
                            "description": {},
                            "policy_tags": {"names": ["names_value1", "names_value2"]},
                            "data_policies": [{"name": "name_value"}],
                            "max_length": 1063,
                            "precision": 972,
                            "scale": 520,
                            "rounding_mode": 1,
                            "collation": {},
                            "default_value_expression": {},
                            "range_element_type": {"type_": "type__value"},
                            "foreign_type_definition": "foreign_type_definition_value",
                        }
                    ],
                    "foreign_type_info": {"type_system": 1},
                },
                "destination_table": {},
                "destination_table_properties": {
                    "friendly_name": {},
                    "description": {},
                    "labels": {},
                },
                "create_disposition": "create_disposition_value",
                "write_disposition": "write_disposition_value",
                "null_marker": {},
                "field_delimiter": "field_delimiter_value",
                "skip_leading_rows": {"value": 541},
                "encoding": "encoding_value",
                "quote": {},
                "max_bad_records": {},
                "allow_quoted_newlines": {},
                "source_format": "source_format_value",
                "allow_jagged_rows": {},
                "ignore_unknown_values": {},
                "projection_fields": [
                    "projection_fields_value1",
                    "projection_fields_value2",
                ],
                "autodetect": {},
                "schema_update_options": [
                    "schema_update_options_value1",
                    "schema_update_options_value2",
                ],
                "time_partitioning": {},
                "range_partitioning": {},
                "clustering": {},
                "destination_encryption_configuration": {},
                "use_avro_logical_types": {},
                "reference_file_schema_uri": {},
                "hive_partitioning_options": {
                    "mode": "mode_value",
                    "source_uri_prefix": "source_uri_prefix_value",
                    "require_partition_filter": {},
                    "fields": ["fields_value1", "fields_value2"],
                },
                "decimal_target_types": [1],
                "json_extension": 1,
                "parquet_options": {
                    "enum_as_string": {},
                    "enable_list_inference": {},
                    "map_target_type": 1,
                },
                "preserve_ascii_control_characters": {},
                "connection_properties": {},
                "create_session": {},
                "column_name_character_map": 1,
                "copy_files_only": {},
                "time_zone": {},
                "null_markers": ["null_markers_value1", "null_markers_value2"],
                "date_format": "date_format_value",
                "datetime_format": "datetime_format_value",
                "time_format": "time_format_value",
                "timestamp_format": "timestamp_format_value",
                "source_column_match": 1,
            },
            "copy": {
                "source_table": {},
                "source_tables": {},
                "destination_table": {},
                "create_disposition": "create_disposition_value",
                "write_disposition": "write_disposition_value",
                "destination_encryption_configuration": {},
                "operation_type": 1,
                "destination_expiration_time": {"seconds": 751, "nanos": 543},
            },
            "extract": {
                "source_table": {},
                "source_model": {
                    "project_id": "project_id_value",
                    "dataset_id": "dataset_id_value",
                    "model_id": "model_id_value",
                },
                "destination_uris": [
                    "destination_uris_value1",
                    "destination_uris_value2",
                ],
                "print_header": {},
                "field_delimiter": "field_delimiter_value",
                "destination_format": "destination_format_value",
                "compression": "compression_value",
                "use_avro_logical_types": {},
                "model_extract_options": {"trial_id": {}},
            },
            "dry_run": {},
            "job_timeout_ms": {},
            "labels": {},
            "reservation": "reservation_value",
        },
        "job_reference": {
            "project_id": "project_id_value",
            "job_id": "job_id_value",
            "location": {},
        },
        "statistics": {
            "creation_time": 1379,
            "start_time": 1084,
            "end_time": 837,
            "total_bytes_processed": {},
            "completion_ratio": {"value": 0.541},
            "quota_deferments": ["quota_deferments_value1", "quota_deferments_value2"],
            "query": {
                "query_plan": [
                    {
                        "name": "name_value",
                        "id": {},
                        "start_ms": 877,
                        "end_ms": 630,
                        "input_stages": [1303, 1304],
                        "wait_ratio_avg": {},
                        "wait_ms_avg": {},
                        "wait_ratio_max": {},
                        "wait_ms_max": {},
                        "read_ratio_avg": {},
                        "read_ms_avg": {},
                        "read_ratio_max": {},
                        "read_ms_max": {},
                        "compute_ratio_avg": {},
                        "compute_ms_avg": {},
                        "compute_ratio_max": {},
                        "compute_ms_max": {},
                        "write_ratio_avg": {},
                        "write_ms_avg": {},
                        "write_ratio_max": {},
                        "write_ms_max": {},
                        "shuffle_output_bytes": {},
                        "shuffle_output_bytes_spilled": {},
                        "records_read": {},
                        "records_written": {},
                        "parallel_inputs": {},
                        "completed_parallel_inputs": {},
                        "status": "status_value",
                        "steps": [
                            {
                                "kind": "kind_value",
                                "substeps": ["substeps_value1", "substeps_value2"],
                            }
                        ],
                        "slot_ms": {},
                        "compute_mode": 1,
                    }
                ],
                "estimated_bytes_processed": {},
                "timeline": [
                    {
                        "elapsed_ms": {},
                        "total_slot_ms": {},
                        "pending_units": {},
                        "completed_units": {},
                        "active_units": {},
                        "shuffle_ram_usage_ratio": {},
                        "estimated_runnable_units": {},
                    }
                ],
                "total_partitions_processed": {},
                "total_bytes_processed": {},
                "total_bytes_processed_accuracy": "total_bytes_processed_accuracy_value",
                "total_bytes_billed": {},
                "billing_tier": {},
                "total_slot_ms": {},
                "cache_hit": {},
                "referenced_tables": {},
                "referenced_routines": [
                    {
                        "project_id": "project_id_value",
                        "dataset_id": "dataset_id_value",
                        "routine_id": "routine_id_value",
                    }
                ],
                "schema": {},
                "num_dml_affected_rows": {},
                "dml_stats": {
                    "inserted_row_count": {},
                    "deleted_row_count": {},
                    "updated_row_count": {},
                },
                "undeclared_query_parameters": {},
                "statement_type": "statement_type_value",
                "ddl_operation_performed": "ddl_operation_performed_value",
                "ddl_target_table": {},
                "ddl_destination_table": {},
                "ddl_target_row_access_policy": {
                    "project_id": "project_id_value",
                    "dataset_id": "dataset_id_value",
                    "table_id": "table_id_value",
                    "policy_id": "policy_id_value",
                },
                "ddl_affected_row_access_policy_count": {},
                "ddl_target_routine": {},
                "ddl_target_dataset": {},
                "ml_statistics": {
                    "max_iterations": 1511,
                    "iteration_results": [
                        {
                            "index": {},
                            "duration_ms": {},
                            "training_loss": {},
                            "eval_loss": {},
                            "learn_rate": 0.1053,
                            "cluster_infos": [
                                {
                                    "centroid_id": 1156,
                                    "cluster_radius": {},
                                    "cluster_size": {},
                                }
                            ],
                            "arima_result": {
                                "arima_model_info": [
                                    {
                                        "non_seasonal_order": {
                                            "p": {},
                                            "d": {},
                                            "q": {},
                                        },
                                        "arima_coefficients": {
                                            "auto_regressive_coefficients": [
                                                0.2985,
                                                0.29860000000000003,
                                            ],
                                            "moving_average_coefficients": [
                                                0.2844,
                                                0.28450000000000003,
                                            ],
                                            "intercept_coefficient": {},
                                        },
                                        "arima_fitting_metrics": {
                                            "log_likelihood": {},
                                            "aic": {},
                                            "variance": {},
                                        },
                                        "has_drift": {},
                                        "time_series_id": "time_series_id_value",
                                        "time_series_ids": [
                                            "time_series_ids_value1",
                                            "time_series_ids_value2",
                                        ],
                                        "seasonal_periods": [1],
                                        "has_holiday_effect": {},
                                        "has_spikes_and_dips": {},
                                        "has_step_changes": {},
                                    }
                                ],
                                "seasonal_periods": [1],
                            },
                            "principal_component_infos": [
                                {
                                    "principal_component_id": {},
                                    "explained_variance": {},
                                    "explained_variance_ratio": {},
                                    "cumulative_explained_variance_ratio": {},
                                }
                            ],
                        }
                    ],
                    "model_type": 1,
                    "training_type": 1,
                    "hparam_trials": [
                        {
                            "trial_id": 840,
                            "start_time_ms": 1403,
                            "end_time_ms": 1156,
                            "hparams": {
                                "max_iterations": 1511,
                                "loss_type": 1,
                                "learn_rate": 0.1053,
                                "l1_regularization": {},
                                "l2_regularization": {},
                                "min_relative_progress": {},
                                "warm_start": {},
                                "early_stop": {},
                                "input_label_columns": [
                                    "input_label_columns_value1",
                                    "input_label_columns_value2",
                                ],
                                "data_split_method": 1,
                                "data_split_eval_fraction": 0.2529,
                                "data_split_column": "data_split_column_value",
                                "learn_rate_strategy": 1,
                                "initial_learn_rate": 0.1894,
                                "label_class_weights": {},
                                "user_column": "user_column_value",
                                "item_column": "item_column_value",
                                "distance_type": 1,
                                "num_clusters": 1316,
                                "model_uri": "model_uri_value",
                                "optimization_strategy": 1,
                                "hidden_units": [1279, 1280],
                                "batch_size": 1052,
                                "dropout": {},
                                "max_tree_depth": 1481,
                                "subsample": 0.972,
                                "min_split_loss": {},
                                "booster_type": 1,
                                "num_parallel_tree": {},
                                "dart_normalize_type": 1,
                                "tree_method": 1,
                                "min_tree_child_weight": {},
                                "colsample_bytree": {},
                                "colsample_bylevel": {},
                                "colsample_bynode": {},
                                "num_factors": 1185,
                                "feedback_type": 1,
                                "wals_alpha": {},
                                "kmeans_initialization_method": 1,
                                "kmeans_initialization_column": "kmeans_initialization_column_value",
                                "time_series_timestamp_column": "time_series_timestamp_column_value",
                                "time_series_data_column": "time_series_data_column_value",
                                "auto_arima": {},
                                "non_seasonal_order": {},
                                "data_frequency": 1,
                                "calculate_p_values": {},
                                "include_drift": {},
                                "holiday_region": 1,
                                "holiday_regions": [1],
                                "time_series_id_column": "time_series_id_column_value",
                                "time_series_id_columns": [
                                    "time_series_id_columns_value1",
                                    "time_series_id_columns_value2",
                                ],
                                "forecast_limit_lower_bound": 0.2772,
                                "forecast_limit_upper_bound": 0.2775,
                                "horizon": 777,
                                "auto_arima_max_order": 2114,
                                "auto_arima_min_order": 2112,
                                "num_trials": 1086,
                                "max_parallel_trials": 2016,
                                "hparam_tuning_objectives": [1],
                                "decompose_time_series": {},
                                "clean_spikes_and_dips": {},
                                "adjust_step_changes": {},
                                "enable_global_explain": {},
                                "sampled_shapley_num_paths": 2665,
                                "integrated_gradients_num_steps": 3204,
                                "category_encoding_method": 1,
                                "tf_version": "tf_version_value",
                                "color_space": 1,
                                "instance_weight_column": "instance_weight_column_value",
                                "trend_smoothing_window_size": 2917,
                                "time_series_length_fraction": 0.2863,
                                "min_time_series_length": 2333,
                                "max_time_series_length": 2335,
                                "xgboost_version": "xgboost_version_value",
                                "approx_global_feature_contrib": {},
                                "fit_intercept": {},
                                "num_principal_components": 2582,
                                "pca_explained_variance_ratio": 0.2931,
                                "scale_features": {},
                                "pca_solver": 1,
                                "auto_class_weights": {},
                                "activation_fn": "activation_fn_value",
                                "optimizer": "optimizer_value",
                                "budget_hours": 0.1291,
                                "standardize_features": {},
                                "l1_reg_activation": 0.1739,
                                "model_registry": 1,
                                "vertex_ai_model_version_aliases": [
                                    "vertex_ai_model_version_aliases_value1",
                                    "vertex_ai_model_version_aliases_value2",
                                ],
                                "dimension_id_columns": [
                                    "dimension_id_columns_value1",
                                    "dimension_id_columns_value2",
                                ],
                                "contribution_metric": "contribution_metric_value",
                                "is_test_column": "is_test_column_value",
                                "min_apriori_support": 0.2069,
                            },
                            "evaluation_metrics": {
                                "regression_metrics": {
                                    "mean_absolute_error": {},
                                    "mean_squared_error": {},
                                    "mean_squared_log_error": {},
                                    "median_absolute_error": {},
                                    "r_squared": {},
                                },
                                "binary_classification_metrics": {
                                    "aggregate_classification_metrics": {
                                        "precision": {},
                                        "recall": {},
                                        "accuracy": {},
                                        "threshold": {},
                                        "f1_score": {},
                                        "log_loss": {},
                                        "roc_auc": {},
                                    },
                                    "binary_confusion_matrix_list": [
                                        {
                                            "positive_class_threshold": {},
                                            "true_positives": {},
                                            "false_positives": {},
                                            "true_negatives": {},
                                            "false_negatives": {},
                                            "precision": {},
                                            "recall": {},
                                            "f1_score": {},
                                            "accuracy": {},
                                        }
                                    ],
                                    "positive_label": "positive_label_value",
                                    "negative_label": "negative_label_value",
                                },
                                "multi_class_classification_metrics": {
                                    "aggregate_classification_metrics": {},
                                    "confusion_matrix_list": [
                                        {
                                            "confidence_threshold": {},
                                            "rows": [
                                                {
                                                    "actual_label": "actual_label_value",
                                                    "entries": [
                                                        {
                                                            "predicted_label": "predicted_label_value",
                                                            "item_count": {},
                                                        }
                                                    ],
                                                }
                                            ],
                                        }
                                    ],
                                },
                                "clustering_metrics": {
                                    "davies_bouldin_index": {},
                                    "mean_squared_distance": {},
                                    "clusters": [
                                        {
                                            "centroid_id": 1156,
                                            "feature_values": [
                                                {
                                                    "feature_column": "feature_column_value",
                                                    "numerical_value": {},
                                                    "categorical_value": {
                                                        "category_counts": [
                                                            {
                                                                "category": "category_value",
                                                                "count": {},
                                                            }
                                                        ]
                                                    },
                                                }
                                            ],
                                            "count": {},
                                        }
                                    ],
                                },
                                "ranking_metrics": {
                                    "mean_average_precision": {},
                                    "mean_squared_error": {},
                                    "normalized_discounted_cumulative_gain": {},
                                    "average_rank": {},
                                },
                                "arima_forecasting_metrics": {
                                    "arima_single_model_forecasting_metrics": [
                                        {
                                            "non_seasonal_order": {},
                                            "arima_fitting_metrics": {},
                                            "has_drift": {},
                                            "time_series_id": "time_series_id_value",
                                            "time_series_ids": [
                                                "time_series_ids_value1",
                                                "time_series_ids_value2",
                                            ],
                                            "seasonal_periods": [1],
                                            "has_holiday_effect": {},
                                            "has_spikes_and_dips": {},
                                            "has_step_changes": {},
                                        }
                                    ]
                                },
                                "dimensionality_reduction_metrics": {
                                    "total_explained_variance_ratio": {}
                                },
                            },
                            "status": 1,
                            "error_message": "error_message_value",
                            "training_loss": {},
                            "eval_loss": {},
                            "hparam_tuning_evaluation_metrics": {},
                        }
                    ],
                },
                "export_data_statistics": {"file_count": {}, "row_count": {}},
                "external_service_costs": [
                    {
                        "external_service": "external_service_value",
                        "bytes_processed": {},
                        "bytes_billed": {},
                        "slot_ms": {},
                        "reserved_slot_count": 2057,
                    }
                ],
                "bi_engine_statistics": {
                    "bi_engine_mode": 1,
                    "acceleration_mode": 1,
                    "bi_engine_reasons": [{"code": 1, "message": "message_value"}],
                },
                "load_query_statistics": {
                    "input_files": {},
                    "input_file_bytes": {},
                    "output_rows": {},
                    "output_bytes": {},
                    "bad_records": {},
                },
                "dcl_target_table": {},
                "dcl_target_view": {},
                "dcl_target_dataset": {},
                "search_statistics": {
                    "index_usage_mode": 1,
                    "index_unused_reasons": [
                        {
                            "code": 1,
                            "message": "message_value",
                            "base_table": {},
                            "index_name": "index_name_value",
                        }
                    ],
                },
                "vector_search_statistics": {
                    "index_usage_mode": 1,
                    "index_unused_reasons": {},
                    "stored_columns_usages": [
                        {
                            "is_query_accelerated": True,
                            "base_table": {},
                            "stored_columns_unused_reasons": [
                                {
                                    "code": 1,
                                    "message": "message_value",
                                    "uncovered_columns": [
                                        "uncovered_columns_value1",
                                        "uncovered_columns_value2",
                                    ],
                                }
                            ],
                        }
                    ],
                },
                "performance_insights": {
                    "avg_previous_execution_ms": 2700,
                    "stage_performance_standalone_insights": [
                        {
                            "stage_id": 832,
                            "slot_contention": True,
                            "insufficient_shuffle_quota": True,
                            "bi_engine_reasons": {},
                            "high_cardinality_joins": [
                                {
                                    "left_rows": 981,
                                    "right_rows": 1096,
                                    "output_rows": 1243,
                                    "step_index": 1075,
                                }
                            ],
                            "partition_skew": {"skew_sources": [{"stage_id": 832}]},
                        }
                    ],
                    "stage_performance_change_insights": [
                        {
                            "stage_id": 832,
                            "input_data_change": {
                                "records_read_diff_percentage": 0.2914
                            },
                        }
                    ],
                },
                "query_info": {"optimization_details": {}},
                "spark_statistics": {
                    "spark_job_id": "spark_job_id_value",
                    "spark_job_location": "spark_job_location_value",
                    "endpoints": {},
                    "logging_info": {
                        "resource_type": "resource_type_value",
                        "project_id": "project_id_value",
                    },
                    "kms_key_name": "kms_key_name_value",
                    "gcs_staging_bucket": "gcs_staging_bucket_value",
                },
                "transferred_bytes": {},
                "materialized_view_statistics": {
                    "materialized_view": [
                        {
                            "table_reference": {},
                            "chosen": True,
                            "estimated_bytes_saved": 2232,
                            "rejected_reason": 1,
                        }
                    ]
                },
                "metadata_cache_statistics": {
                    "table_metadata_cache_usage": [
                        {
                            "table_reference": {},
                            "unused_reason": 1,
                            "explanation": "explanation_value",
                            "staleness": {"seconds": 751, "nanos": 543},
                            "table_type": "table_type_value",
                        }
                    ]
                },
            },
            "load": {
                "input_files": {},
                "input_file_bytes": {},
                "output_rows": {},
                "output_bytes": {},
                "bad_records": {},
                "timeline": {},
            },
            "extract": {
                "destination_uri_file_counts": [2892, 2893],
                "input_bytes": {},
                "timeline": {},
            },
            "copy": {"copied_rows": {}, "copied_logical_bytes": {}},
            "total_slot_ms": {},
            "reservation_id": "reservation_id_value",
            "num_child_jobs": 1472,
            "parent_job_id": "parent_job_id_value",
            "script_statistics": {
                "evaluation_kind": 1,
                "stack_frames": [
                    {
                        "start_line": 1077,
                        "start_column": 1307,
                        "end_line": 830,
                        "end_column": 1060,
                        "procedure_id": "procedure_id_value",
                        "text": "text_value",
                    }
                ],
            },
            "row_level_security_statistics": {"row_level_security_applied": True},
            "data_masking_statistics": {"data_masking_applied": True},
            "transaction_info": {"transaction_id": "transaction_id_value"},
            "session_info": {"session_id": "session_id_value"},
            "final_execution_duration_ms": 2881,
            "edition": 1,
        },
        "status": {
            "error_result": {
                "reason": "reason_value",
                "location": "location_value",
                "debug_info": "debug_info_value",
                "message": "message_value",
            },
            "errors": {},
            "state": "state_value",
        },
        "principal_subject": "principal_subject_value",
        "job_creation_reason": {"code": 1},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = job.InsertJobRequest.meta.fields["job"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["job"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["job"][field])):
                    del request_init["job"][field][i][subfield]
            else:
                del request_init["job"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = job.Job(
            kind="kind_value",
            etag="etag_value",
            id="id_value",
            self_link="self_link_value",
            user_email="user_email_value",
            principal_subject="principal_subject_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = job.Job.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.insert_job(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.Job)
    assert response.kind == "kind_value"
    assert response.etag == "etag_value"
    assert response.id == "id_value"
    assert response.self_link == "self_link_value"
    assert response.user_email == "user_email_value"
    assert response.principal_subject == "principal_subject_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_insert_job_rest_interceptors(null_interceptor):
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.JobServiceRestInterceptor(),
    )
    client = JobServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_insert_job"
    ) as post, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_insert_job_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.JobServiceRestInterceptor, "pre_insert_job"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = job.InsertJobRequest.pb(job.InsertJobRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = job.Job.to_json(job.Job())
        req.return_value.content = return_value

        request = job.InsertJobRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = job.Job()
        post_with_metadata.return_value = job.Job(), metadata

        client.insert_job(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_delete_job_rest_bad_request(request_type=job.DeleteJobRequest):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "job_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.delete_job(request)


@pytest.mark.parametrize(
    "request_type",
    [
        job.DeleteJobRequest,
        dict,
    ],
)
def test_delete_job_rest_call_success(request_type):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "job_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = ""
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.delete_job(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_job_rest_interceptors(null_interceptor):
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.JobServiceRestInterceptor(),
    )
    client = JobServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.JobServiceRestInterceptor, "pre_delete_job"
    ) as pre:
        pre.assert_not_called()
        pb_message = job.DeleteJobRequest.pb(job.DeleteJobRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        request = job.DeleteJobRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_job(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_list_jobs_rest_bad_request(request_type=job.ListJobsRequest):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_jobs(request)


@pytest.mark.parametrize(
    "request_type",
    [
        job.ListJobsRequest,
        dict,
    ],
)
def test_list_jobs_rest_call_success(request_type):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = job.JobList(
            etag="etag_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = job.JobList.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_jobs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobsPager)
    assert response.etag == "etag_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_jobs_rest_interceptors(null_interceptor):
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.JobServiceRestInterceptor(),
    )
    client = JobServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_list_jobs"
    ) as post, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_list_jobs_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.JobServiceRestInterceptor, "pre_list_jobs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = job.ListJobsRequest.pb(job.ListJobsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = job.JobList.to_json(job.JobList())
        req.return_value.content = return_value

        request = job.ListJobsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = job.JobList()
        post_with_metadata.return_value = job.JobList(), metadata

        client.list_jobs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_query_results_rest_bad_request(request_type=job.GetQueryResultsRequest):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "job_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_query_results(request)


@pytest.mark.parametrize(
    "request_type",
    [
        job.GetQueryResultsRequest,
        dict,
    ],
)
def test_get_query_results_rest_call_success(request_type):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "job_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = job.GetQueryResultsResponse(
            kind="kind_value",
            etag="etag_value",
            page_token="page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = job.GetQueryResultsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_query_results(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.GetQueryResultsResponse)
    assert response.kind == "kind_value"
    assert response.etag == "etag_value"
    assert response.page_token == "page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_query_results_rest_interceptors(null_interceptor):
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.JobServiceRestInterceptor(),
    )
    client = JobServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_get_query_results"
    ) as post, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_get_query_results_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.JobServiceRestInterceptor, "pre_get_query_results"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = job.GetQueryResultsRequest.pb(job.GetQueryResultsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = job.GetQueryResultsResponse.to_json(
            job.GetQueryResultsResponse()
        )
        req.return_value.content = return_value

        request = job.GetQueryResultsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = job.GetQueryResultsResponse()
        post_with_metadata.return_value = job.GetQueryResultsResponse(), metadata

        client.get_query_results(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_query_rest_bad_request(request_type=job.PostQueryRequest):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.query(request)


@pytest.mark.parametrize(
    "request_type",
    [
        job.PostQueryRequest,
        dict,
    ],
)
def test_query_rest_call_success(request_type):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request_init["query_request"] = {
        "kind": "kind_value",
        "query": "query_value",
        "max_results": {"value": 541},
        "default_dataset": {
            "dataset_id": "dataset_id_value",
            "project_id": "project_id_value",
        },
        "timeout_ms": {},
        "job_timeout_ms": 1504,
        "destination_encryption_configuration": {
            "kms_key_name": {"value": "value_value"}
        },
        "dry_run": True,
        "use_query_cache": {"value": True},
        "use_legacy_sql": {},
        "parameter_mode": "parameter_mode_value",
        "query_parameters": [
            {
                "name": "name_value",
                "parameter_type": {
                    "type_": "type__value",
                    "array_type": {},
                    "struct_types": [
                        {
                            "name": "name_value",
                            "type_": {},
                            "description": "description_value",
                        }
                    ],
                    "range_element_type": {},
                },
                "parameter_value": {
                    "value": {},
                    "array_values": {},
                    "struct_values": {},
                    "range_value": {"start": {}, "end": {}},
                    "alt_struct_values": [
                        {
                            "null_value": 0,
                            "number_value": 0.1285,
                            "string_value": "string_value_value",
                            "bool_value": True,
                            "struct_value": {"fields": {}},
                            "list_value": {"values": {}},
                        }
                    ],
                },
            }
        ],
        "location": "location_value",
        "format_options": {"use_int64_timestamp": True},
        "connection_properties": [{"key": "key_value", "value": "value_value"}],
        "labels": {},
        "maximum_bytes_billed": {"value": 541},
        "request_id": "request_id_value",
        "create_session": {},
        "job_creation_mode": 1,
        "reservation": "reservation_value",
        "write_incremental_results": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = job.PostQueryRequest.meta.fields["query_request"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["query_request"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["query_request"][field])):
                    del request_init["query_request"][field][i][subfield]
            else:
                del request_init["query_request"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = job.QueryResponse(
            kind="kind_value",
            query_id="query_id_value",
            location="location_value",
            page_token="page_token_value",
            total_bytes_billed=1909,
            total_slot_ms=1412,
            creation_time=1379,
            start_time=1084,
            end_time=837,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = job.QueryResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.query(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.QueryResponse)
    assert response.kind == "kind_value"
    assert response.query_id == "query_id_value"
    assert response.location == "location_value"
    assert response.page_token == "page_token_value"
    assert response.total_bytes_billed == 1909
    assert response.total_slot_ms == 1412
    assert response.creation_time == 1379
    assert response.start_time == 1084
    assert response.end_time == 837


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_query_rest_interceptors(null_interceptor):
    transport = transports.JobServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.JobServiceRestInterceptor(),
    )
    client = JobServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_query"
    ) as post, mock.patch.object(
        transports.JobServiceRestInterceptor, "post_query_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.JobServiceRestInterceptor, "pre_query"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = job.PostQueryRequest.pb(job.PostQueryRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = job.QueryResponse.to_json(job.QueryResponse())
        req.return_value.content = return_value

        request = job.PostQueryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = job.QueryResponse()
        post_with_metadata.return_value = job.QueryResponse(), metadata

        client.query(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_initialize_client_w_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_cancel_job_empty_call_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        client.cancel_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = job.CancelJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_job_empty_call_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        client.get_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = job.GetJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_insert_job_empty_call_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.insert_job), "__call__") as call:
        client.insert_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = job.InsertJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_job_empty_call_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        client.delete_job(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = job.DeleteJobRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_jobs_empty_call_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        client.list_jobs(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = job.ListJobsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_query_results_empty_call_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_query_results), "__call__"
    ) as call:
        client.get_query_results(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = job.GetQueryResultsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_query_empty_call_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.query), "__call__") as call:
        client.query(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = job.PostQueryRequest()

        assert args[0] == request_msg


def test_job_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.JobServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_job_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigquery_v2.services.job_service.transports.JobServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.JobServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "cancel_job",
        "get_job",
        "insert_job",
        "delete_job",
        "list_jobs",
        "get_query_results",
        "query",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_job_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.bigquery_v2.services.job_service.transports.JobServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.JobServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/devstorage.full_control",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/devstorage.read_write",
            ),
            quota_project_id="octopus",
        )


def test_job_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.bigquery_v2.services.job_service.transports.JobServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.JobServiceTransport()
        adc.assert_called_once()


def test_job_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        JobServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/devstorage.full_control",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/devstorage.read_write",
            ),
            quota_project_id=None,
        )


def test_job_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.JobServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_job_service_host_no_port(transport_name):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquery.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "bigquery.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://bigquery.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_job_service_host_with_port(transport_name):
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquery.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "bigquery.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://bigquery.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_job_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = JobServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = JobServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.cancel_job._session
    session2 = client2.transport.cancel_job._session
    assert session1 != session2
    session1 = client1.transport.get_job._session
    session2 = client2.transport.get_job._session
    assert session1 != session2
    session1 = client1.transport.insert_job._session
    session2 = client2.transport.insert_job._session
    assert session1 != session2
    session1 = client1.transport.delete_job._session
    session2 = client2.transport.delete_job._session
    assert session1 != session2
    session1 = client1.transport.list_jobs._session
    session2 = client2.transport.list_jobs._session
    assert session1 != session2
    session1 = client1.transport.get_query_results._session
    session2 = client2.transport.get_query_results._session
    assert session1 != session2
    session1 = client1.transport.query._session
    session2 = client2.transport.query._session
    assert session1 != session2


def test_bucket_path():
    expected = "*".format()
    actual = JobServiceClient.bucket_path()
    assert expected == actual


def test_parse_bucket_path():
    expected = {}
    path = JobServiceClient.bucket_path(**expected)

    # Check that the path construction is reversible.
    actual = JobServiceClient.parse_bucket_path(path)
    assert expected == actual


def test_crypto_key_path():
    project = "squid"
    location = "clam"
    key_ring = "whelk"
    crypto_key = "octopus"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
    )
    actual = JobServiceClient.crypto_key_path(project, location, key_ring, crypto_key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "key_ring": "cuttlefish",
        "crypto_key": "mussel",
    }
    path = JobServiceClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = JobServiceClient.parse_crypto_key_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = JobServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = JobServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = JobServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = JobServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = JobServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = JobServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = JobServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = JobServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = JobServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = JobServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = JobServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = JobServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = JobServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = JobServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = JobServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.JobServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.JobServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = JobServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_rest():
    client = JobServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_session")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
    ]
    for transport in transports:
        client = JobServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (JobServiceClient, transports.JobServiceRestTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
