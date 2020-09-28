# -*- coding: utf-8 -*-

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
#

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.bigquery_v2.services.model_service import ModelServiceAsyncClient
from google.cloud.bigquery_v2.services.model_service import ModelServiceClient
from google.cloud.bigquery_v2.services.model_service import transports
from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import model
from google.cloud.bigquery_v2.types import model as gcb_model
from google.cloud.bigquery_v2.types import model_reference
from google.cloud.bigquery_v2.types import standard_sql
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert ModelServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ModelServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        ModelServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ModelServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ModelServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert ModelServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [ModelServiceClient, ModelServiceAsyncClient])
def test_model_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "bigquery.googleapis.com:443"


def test_model_service_client_get_transport_class():
    transport = ModelServiceClient.get_transport_class()
    assert transport == transports.ModelServiceGrpcTransport

    transport = ModelServiceClient.get_transport_class("grpc")
    assert transport == transports.ModelServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ModelServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ModelServiceClient)
)
@mock.patch.object(
    ModelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ModelServiceAsyncClient),
)
def test_model_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ModelServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ModelServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc", "true"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc", "false"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ModelServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ModelServiceClient)
)
@mock.patch.object(
    ModelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ModelServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_model_service_client_mtls_env_auto(
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
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_model_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_model_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_model_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigquery_v2.services.model_service.transports.ModelServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ModelServiceClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_get_model(transport: str = "grpc", request_type=model.GetModelRequest):
    client = ModelServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model(
            etag="etag_value",
            creation_time=1379,
            last_modified_time=1890,
            description="description_value",
            friendly_name="friendly_name_value",
            expiration_time=1617,
            location="location_value",
            model_type=model.Model.ModelType.LINEAR_REGRESSION,
        )

        response = client.get_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == model.GetModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.Model)

    assert response.etag == "etag_value"

    assert response.creation_time == 1379

    assert response.last_modified_time == 1890

    assert response.description == "description_value"

    assert response.friendly_name == "friendly_name_value"

    assert response.expiration_time == 1617

    assert response.location == "location_value"

    assert response.model_type == model.Model.ModelType.LINEAR_REGRESSION


def test_get_model_from_dict():
    test_get_model(request_type=dict)


@pytest.mark.asyncio
async def test_get_model_async(transport: str = "grpc_asyncio"):
    client = ModelServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = model.GetModelRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model.Model(
                etag="etag_value",
                creation_time=1379,
                last_modified_time=1890,
                description="description_value",
                friendly_name="friendly_name_value",
                expiration_time=1617,
                location="location_value",
                model_type=model.Model.ModelType.LINEAR_REGRESSION,
            )
        )

        response = await client.get_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.Model)

    assert response.etag == "etag_value"

    assert response.creation_time == 1379

    assert response.last_modified_time == 1890

    assert response.description == "description_value"

    assert response.friendly_name == "friendly_name_value"

    assert response.expiration_time == 1617

    assert response.location == "location_value"

    assert response.model_type == model.Model.ModelType.LINEAR_REGRESSION


def test_get_model_flattened():
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_model(
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].dataset_id == "dataset_id_value"

        assert args[0].model_id == "model_id_value"


def test_get_model_flattened_error():
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_model(
            model.GetModelRequest(),
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
        )


@pytest.mark.asyncio
async def test_get_model_flattened_async():
    client = ModelServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(model.Model())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_model(
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].dataset_id == "dataset_id_value"

        assert args[0].model_id == "model_id_value"


@pytest.mark.asyncio
async def test_get_model_flattened_error_async():
    client = ModelServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_model(
            model.GetModelRequest(),
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
        )


def test_list_models(transport: str = "grpc", request_type=model.ListModelsRequest):
    client = ModelServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.ListModelsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == model.ListModelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.ListModelsResponse)

    assert response.next_page_token == "next_page_token_value"


def test_list_models_from_dict():
    test_list_models(request_type=dict)


@pytest.mark.asyncio
async def test_list_models_async(transport: str = "grpc_asyncio"):
    client = ModelServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = model.ListModelsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_models), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model.ListModelsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.ListModelsResponse)

    assert response.next_page_token == "next_page_token_value"


def test_list_models_flattened():
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.ListModelsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_models(
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            max_results=wrappers.UInt32Value(value=541),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].dataset_id == "dataset_id_value"

        assert args[0].max_results == wrappers.UInt32Value(value=541)


def test_list_models_flattened_error():
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_models(
            model.ListModelsRequest(),
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            max_results=wrappers.UInt32Value(value=541),
        )


@pytest.mark.asyncio
async def test_list_models_flattened_async():
    client = ModelServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_models), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.ListModelsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model.ListModelsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_models(
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            max_results=wrappers.UInt32Value(value=541),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].dataset_id == "dataset_id_value"

        assert args[0].max_results == wrappers.UInt32Value(value=541)


@pytest.mark.asyncio
async def test_list_models_flattened_error_async():
    client = ModelServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_models(
            model.ListModelsRequest(),
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            max_results=wrappers.UInt32Value(value=541),
        )


def test_patch_model(transport: str = "grpc", request_type=gcb_model.PatchModelRequest):
    client = ModelServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.patch_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcb_model.Model(
            etag="etag_value",
            creation_time=1379,
            last_modified_time=1890,
            description="description_value",
            friendly_name="friendly_name_value",
            expiration_time=1617,
            location="location_value",
            model_type=gcb_model.Model.ModelType.LINEAR_REGRESSION,
        )

        response = client.patch_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == gcb_model.PatchModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcb_model.Model)

    assert response.etag == "etag_value"

    assert response.creation_time == 1379

    assert response.last_modified_time == 1890

    assert response.description == "description_value"

    assert response.friendly_name == "friendly_name_value"

    assert response.expiration_time == 1617

    assert response.location == "location_value"

    assert response.model_type == gcb_model.Model.ModelType.LINEAR_REGRESSION


def test_patch_model_from_dict():
    test_patch_model(request_type=dict)


@pytest.mark.asyncio
async def test_patch_model_async(transport: str = "grpc_asyncio"):
    client = ModelServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gcb_model.PatchModelRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.patch_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcb_model.Model(
                etag="etag_value",
                creation_time=1379,
                last_modified_time=1890,
                description="description_value",
                friendly_name="friendly_name_value",
                expiration_time=1617,
                location="location_value",
                model_type=gcb_model.Model.ModelType.LINEAR_REGRESSION,
            )
        )

        response = await client.patch_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcb_model.Model)

    assert response.etag == "etag_value"

    assert response.creation_time == 1379

    assert response.last_modified_time == 1890

    assert response.description == "description_value"

    assert response.friendly_name == "friendly_name_value"

    assert response.expiration_time == 1617

    assert response.location == "location_value"

    assert response.model_type == gcb_model.Model.ModelType.LINEAR_REGRESSION


def test_patch_model_flattened():
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.patch_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcb_model.Model()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.patch_model(
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
            model=gcb_model.Model(etag="etag_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].dataset_id == "dataset_id_value"

        assert args[0].model_id == "model_id_value"

        assert args[0].model == gcb_model.Model(etag="etag_value")


def test_patch_model_flattened_error():
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_model(
            gcb_model.PatchModelRequest(),
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
            model=gcb_model.Model(etag="etag_value"),
        )


@pytest.mark.asyncio
async def test_patch_model_flattened_async():
    client = ModelServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.patch_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcb_model.Model()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcb_model.Model())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.patch_model(
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
            model=gcb_model.Model(etag="etag_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].dataset_id == "dataset_id_value"

        assert args[0].model_id == "model_id_value"

        assert args[0].model == gcb_model.Model(etag="etag_value")


@pytest.mark.asyncio
async def test_patch_model_flattened_error_async():
    client = ModelServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.patch_model(
            gcb_model.PatchModelRequest(),
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
            model=gcb_model.Model(etag="etag_value"),
        )


def test_delete_model(transport: str = "grpc", request_type=model.DeleteModelRequest):
    client = ModelServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == model.DeleteModelRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_model_from_dict():
    test_delete_model(request_type=dict)


@pytest.mark.asyncio
async def test_delete_model_async(transport: str = "grpc_asyncio"):
    client = ModelServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = model.DeleteModelRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_model_flattened():
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_model(
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].dataset_id == "dataset_id_value"

        assert args[0].model_id == "model_id_value"


def test_delete_model_flattened_error():
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_model(
            model.DeleteModelRequest(),
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
        )


@pytest.mark.asyncio
async def test_delete_model_flattened_async():
    client = ModelServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_model(
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].dataset_id == "dataset_id_value"

        assert args[0].model_id == "model_id_value"


@pytest.mark.asyncio
async def test_delete_model_flattened_error_async():
    client = ModelServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_model(
            model.DeleteModelRequest(),
            project_id="project_id_value",
            dataset_id="dataset_id_value",
            model_id="model_id_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ModelServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ModelServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ModelServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = ModelServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ModelServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.ModelServiceGrpcTransport, transports.ModelServiceGrpcAsyncIOTransport],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ModelServiceClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.ModelServiceGrpcTransport,)


def test_model_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.ModelServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_model_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigquery_v2.services.model_service.transports.ModelServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ModelServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_model",
        "list_models",
        "patch_model",
        "delete_model",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_model_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.bigquery_v2.services.model_service.transports.ModelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ModelServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


def test_model_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.bigquery_v2.services.model_service.transports.ModelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ModelServiceTransport()
        adc.assert_called_once()


def test_model_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        ModelServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id=None,
        )


def test_model_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.ModelServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


def test_model_service_host_no_port():
    client = ModelServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquery.googleapis.com"
        ),
    )
    assert client._transport._host == "bigquery.googleapis.com:443"


def test_model_service_host_with_port():
    client = ModelServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquery.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "bigquery.googleapis.com:8000"


def test_model_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.ModelServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


def test_model_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.ModelServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


@pytest.mark.parametrize(
    "transport_class",
    [transports.ModelServiceGrpcTransport, transports.ModelServiceGrpcAsyncIOTransport],
)
def test_model_service_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/bigquery",
                    "https://www.googleapis.com/auth/bigquery.readonly",
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.ModelServiceGrpcTransport, transports.ModelServiceGrpcAsyncIOTransport],
)
def test_model_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/bigquery",
                    "https://www.googleapis.com/auth/bigquery.readonly",
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ModelServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ModelServiceClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ModelServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ModelServiceClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
