# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Accesses the google.cloud.bigquery.v2 ModelService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import grpc

from google.cloud.bigquery_v2.gapic import enums
from google.cloud.bigquery_v2.gapic import model_service_client_config
from google.cloud.bigquery_v2.gapic.transports import model_service_grpc_transport
from google.cloud.bigquery_v2.proto import model_pb2
from google.cloud.bigquery_v2.proto import model_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import wrappers_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-bigquery",
).version


class ModelServiceClient(object):
    SERVICE_ADDRESS = "bigquery.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.bigquery.v2.ModelService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ModelServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.ModelServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.ModelServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = model_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=model_service_grpc_transport.ModelServiceGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = model_service_grpc_transport.ModelServiceGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION,
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME],
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def get_model(
        self,
        project_id,
        dataset_id,
        model_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the specified model resource by model ID.

        Example:
            >>> from google.cloud import bigquery_v2
            >>>
            >>> client = bigquery_v2.ModelServiceClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `dataset_id`:
            >>> dataset_id = ''
            >>>
            >>> # TODO: Initialize `model_id`:
            >>> model_id = ''
            >>>
            >>> response = client.get_model(project_id, dataset_id, model_id)

        Args:
            project_id (str): Required. Project ID of the requested model.
            dataset_id (str): Required. Dataset ID of the requested model.
            model_id (str): Required. Model ID of the requested model.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_v2.types.Model` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_model,
                default_retry=self._method_configs["GetModel"].retry,
                default_timeout=self._method_configs["GetModel"].timeout,
                client_info=self._client_info,
            )

        request = model_pb2.GetModelRequest(
            project_id=project_id, dataset_id=dataset_id, model_id=model_id,
        )
        return self._inner_api_calls["get_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_models(
        self,
        project_id,
        dataset_id,
        max_results=None,
        page_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all models in the specified dataset. Requires the READER dataset
        role.

        Example:
            >>> from google.cloud import bigquery_v2
            >>>
            >>> client = bigquery_v2.ModelServiceClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `dataset_id`:
            >>> dataset_id = ''
            >>>
            >>> response = client.list_models(project_id, dataset_id)

        Args:
            project_id (str): Required. Project ID of the models to list.
            dataset_id (str): Required. Dataset ID of the models to list.
            max_results (Union[dict, ~google.cloud.bigquery_v2.types.UInt32Value]): The maximum number of results to return in a single response page.
                Leverage the page tokens to iterate through the entire collection.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_v2.types.UInt32Value`
            page_token (str): Page token, returned by a previous call to request the next page of
                results
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_v2.types.ListModelsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_models" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_models"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_models,
                default_retry=self._method_configs["ListModels"].retry,
                default_timeout=self._method_configs["ListModels"].timeout,
                client_info=self._client_info,
            )

        request = model_pb2.ListModelsRequest(
            project_id=project_id,
            dataset_id=dataset_id,
            max_results=max_results,
            page_token=page_token,
        )
        return self._inner_api_calls["list_models"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def patch_model(
        self,
        project_id,
        dataset_id,
        model_id,
        model,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Patch specific fields in the specified model.

        Example:
            >>> from google.cloud import bigquery_v2
            >>>
            >>> client = bigquery_v2.ModelServiceClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `dataset_id`:
            >>> dataset_id = ''
            >>>
            >>> # TODO: Initialize `model_id`:
            >>> model_id = ''
            >>>
            >>> # TODO: Initialize `model`:
            >>> model = {}
            >>>
            >>> response = client.patch_model(project_id, dataset_id, model_id, model)

        Args:
            project_id (str): Required. Project ID of the model to patch.
            dataset_id (str): Required. Dataset ID of the model to patch.
            model_id (str): Required. Model ID of the model to patch.
            model (Union[dict, ~google.cloud.bigquery_v2.types.Model]): Required. Patched model.
                Follows RFC5789 patch semantics. Missing fields are not updated.
                To clear a field, explicitly set to default value.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_v2.types.Model`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_v2.types.Model` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "patch_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "patch_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.patch_model,
                default_retry=self._method_configs["PatchModel"].retry,
                default_timeout=self._method_configs["PatchModel"].timeout,
                client_info=self._client_info,
            )

        request = model_pb2.PatchModelRequest(
            project_id=project_id,
            dataset_id=dataset_id,
            model_id=model_id,
            model=model,
        )
        return self._inner_api_calls["patch_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_model(
        self,
        project_id,
        dataset_id,
        model_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the model specified by modelId from the dataset.

        Example:
            >>> from google.cloud import bigquery_v2
            >>>
            >>> client = bigquery_v2.ModelServiceClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `dataset_id`:
            >>> dataset_id = ''
            >>>
            >>> # TODO: Initialize `model_id`:
            >>> model_id = ''
            >>>
            >>> client.delete_model(project_id, dataset_id, model_id)

        Args:
            project_id (str): Required. Project ID of the model to delete.
            dataset_id (str): Required. Dataset ID of the model to delete.
            model_id (str): Required. Model ID of the model to delete.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_model,
                default_retry=self._method_configs["DeleteModel"].retry,
                default_timeout=self._method_configs["DeleteModel"].timeout,
                client_info=self._client_info,
            )

        request = model_pb2.DeleteModelRequest(
            project_id=project_id, dataset_id=dataset_id, model_id=model_id,
        )
        self._inner_api_calls["delete_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
