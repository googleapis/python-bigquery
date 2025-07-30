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
import logging
import json  # type: ignore

from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import gapic_v1

from google.protobuf import json_format

from requests import __version__ as requests_version
import dataclasses
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings


from google.cloud.bigquery_v2.types import dataset
from google.protobuf import empty_pb2  # type: ignore


from .rest_base import _BaseDatasetServiceRestTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class DatasetServiceRestInterceptor:
    """Interceptor for DatasetService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DatasetServiceRestTransport.

    .. code-block:: python
        class MyCustomDatasetServiceInterceptor(DatasetServiceRestInterceptor):
            def pre_delete_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_datasets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_datasets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_patch_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DatasetServiceRestTransport(interceptor=MyCustomDatasetServiceInterceptor())
        client = DatasetServiceClient(transport=transport)


    """

    def pre_delete_dataset(
        self,
        request: dataset.DeleteDatasetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.DeleteDatasetRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DatasetService server.
        """
        return request, metadata

    def pre_get_dataset(
        self,
        request: dataset.GetDatasetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.GetDatasetRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DatasetService server.
        """
        return request, metadata

    def post_get_dataset(self, response: dataset.Dataset) -> dataset.Dataset:
        """Post-rpc interceptor for get_dataset

        DEPRECATED. Please use the `post_get_dataset_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DatasetService server but before
        it is returned to user code. This `post_get_dataset` interceptor runs
        before the `post_get_dataset_with_metadata` interceptor.
        """
        return response

    def post_get_dataset_with_metadata(
        self,
        response: dataset.Dataset,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.Dataset, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_dataset

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DatasetService server but before it is returned to user code.

        We recommend only using this `post_get_dataset_with_metadata`
        interceptor in new development instead of the `post_get_dataset` interceptor.
        When both interceptors are used, this `post_get_dataset_with_metadata` interceptor runs after the
        `post_get_dataset` interceptor. The (possibly modified) response returned by
        `post_get_dataset` will be passed to
        `post_get_dataset_with_metadata`.
        """
        return response, metadata

    def pre_insert_dataset(
        self,
        request: dataset.InsertDatasetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.InsertDatasetRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for insert_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DatasetService server.
        """
        return request, metadata

    def post_insert_dataset(self, response: dataset.Dataset) -> dataset.Dataset:
        """Post-rpc interceptor for insert_dataset

        DEPRECATED. Please use the `post_insert_dataset_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DatasetService server but before
        it is returned to user code. This `post_insert_dataset` interceptor runs
        before the `post_insert_dataset_with_metadata` interceptor.
        """
        return response

    def post_insert_dataset_with_metadata(
        self,
        response: dataset.Dataset,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.Dataset, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for insert_dataset

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DatasetService server but before it is returned to user code.

        We recommend only using this `post_insert_dataset_with_metadata`
        interceptor in new development instead of the `post_insert_dataset` interceptor.
        When both interceptors are used, this `post_insert_dataset_with_metadata` interceptor runs after the
        `post_insert_dataset` interceptor. The (possibly modified) response returned by
        `post_insert_dataset` will be passed to
        `post_insert_dataset_with_metadata`.
        """
        return response, metadata

    def pre_list_datasets(
        self,
        request: dataset.ListDatasetsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.ListDatasetsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_datasets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DatasetService server.
        """
        return request, metadata

    def post_list_datasets(self, response: dataset.DatasetList) -> dataset.DatasetList:
        """Post-rpc interceptor for list_datasets

        DEPRECATED. Please use the `post_list_datasets_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DatasetService server but before
        it is returned to user code. This `post_list_datasets` interceptor runs
        before the `post_list_datasets_with_metadata` interceptor.
        """
        return response

    def post_list_datasets_with_metadata(
        self,
        response: dataset.DatasetList,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.DatasetList, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_datasets

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DatasetService server but before it is returned to user code.

        We recommend only using this `post_list_datasets_with_metadata`
        interceptor in new development instead of the `post_list_datasets` interceptor.
        When both interceptors are used, this `post_list_datasets_with_metadata` interceptor runs after the
        `post_list_datasets` interceptor. The (possibly modified) response returned by
        `post_list_datasets` will be passed to
        `post_list_datasets_with_metadata`.
        """
        return response, metadata

    def pre_patch_dataset(
        self,
        request: dataset.UpdateOrPatchDatasetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataset.UpdateOrPatchDatasetRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for patch_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DatasetService server.
        """
        return request, metadata

    def post_patch_dataset(self, response: dataset.Dataset) -> dataset.Dataset:
        """Post-rpc interceptor for patch_dataset

        DEPRECATED. Please use the `post_patch_dataset_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DatasetService server but before
        it is returned to user code. This `post_patch_dataset` interceptor runs
        before the `post_patch_dataset_with_metadata` interceptor.
        """
        return response

    def post_patch_dataset_with_metadata(
        self,
        response: dataset.Dataset,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.Dataset, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for patch_dataset

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DatasetService server but before it is returned to user code.

        We recommend only using this `post_patch_dataset_with_metadata`
        interceptor in new development instead of the `post_patch_dataset` interceptor.
        When both interceptors are used, this `post_patch_dataset_with_metadata` interceptor runs after the
        `post_patch_dataset` interceptor. The (possibly modified) response returned by
        `post_patch_dataset` will be passed to
        `post_patch_dataset_with_metadata`.
        """
        return response, metadata

    def pre_undelete_dataset(
        self,
        request: dataset.UndeleteDatasetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.UndeleteDatasetRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for undelete_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DatasetService server.
        """
        return request, metadata

    def post_undelete_dataset(self, response: dataset.Dataset) -> dataset.Dataset:
        """Post-rpc interceptor for undelete_dataset

        DEPRECATED. Please use the `post_undelete_dataset_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DatasetService server but before
        it is returned to user code. This `post_undelete_dataset` interceptor runs
        before the `post_undelete_dataset_with_metadata` interceptor.
        """
        return response

    def post_undelete_dataset_with_metadata(
        self,
        response: dataset.Dataset,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.Dataset, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for undelete_dataset

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DatasetService server but before it is returned to user code.

        We recommend only using this `post_undelete_dataset_with_metadata`
        interceptor in new development instead of the `post_undelete_dataset` interceptor.
        When both interceptors are used, this `post_undelete_dataset_with_metadata` interceptor runs after the
        `post_undelete_dataset` interceptor. The (possibly modified) response returned by
        `post_undelete_dataset` will be passed to
        `post_undelete_dataset_with_metadata`.
        """
        return response, metadata

    def pre_update_dataset(
        self,
        request: dataset.UpdateOrPatchDatasetRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataset.UpdateOrPatchDatasetRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DatasetService server.
        """
        return request, metadata

    def post_update_dataset(self, response: dataset.Dataset) -> dataset.Dataset:
        """Post-rpc interceptor for update_dataset

        DEPRECATED. Please use the `post_update_dataset_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the DatasetService server but before
        it is returned to user code. This `post_update_dataset` interceptor runs
        before the `post_update_dataset_with_metadata` interceptor.
        """
        return response

    def post_update_dataset_with_metadata(
        self,
        response: dataset.Dataset,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataset.Dataset, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_dataset

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the DatasetService server but before it is returned to user code.

        We recommend only using this `post_update_dataset_with_metadata`
        interceptor in new development instead of the `post_update_dataset` interceptor.
        When both interceptors are used, this `post_update_dataset_with_metadata` interceptor runs after the
        `post_update_dataset` interceptor. The (possibly modified) response returned by
        `post_update_dataset` will be passed to
        `post_update_dataset_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class DatasetServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DatasetServiceRestInterceptor


class DatasetServiceRestTransport(_BaseDatasetServiceRestTransport):
    """REST backend synchronous transport for DatasetService.

    DatasetService provides methods for managing BigQuery
    datasets.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "bigquery.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DatasetServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'bigquery.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or DatasetServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _DeleteDataset(
        _BaseDatasetServiceRestTransport._BaseDeleteDataset, DatasetServiceRestStub
    ):
        def __hash__(self):
            return hash("DatasetServiceRestTransport.DeleteDataset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: dataset.DeleteDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete dataset method over HTTP.

            Args:
                request (~.dataset.DeleteDatasetRequest):
                    The request object. Request format for deleting a
                dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDatasetServiceRestTransport._BaseDeleteDataset._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_dataset(request, metadata)
            transcoded_request = _BaseDatasetServiceRestTransport._BaseDeleteDataset._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDatasetServiceRestTransport._BaseDeleteDataset._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery_v2.DatasetServiceClient.DeleteDataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "DeleteDataset",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DatasetServiceRestTransport._DeleteDataset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetDataset(
        _BaseDatasetServiceRestTransport._BaseGetDataset, DatasetServiceRestStub
    ):
        def __hash__(self):
            return hash("DatasetServiceRestTransport.GetDataset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: dataset.GetDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataset.Dataset:
            r"""Call the get dataset method over HTTP.

            Args:
                request (~.dataset.GetDatasetRequest):
                    The request object. Request format for getting
                information about a dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataset.Dataset:
                    Represents a BigQuery dataset.
            """

            http_options = (
                _BaseDatasetServiceRestTransport._BaseGetDataset._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_dataset(request, metadata)
            transcoded_request = _BaseDatasetServiceRestTransport._BaseGetDataset._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseDatasetServiceRestTransport._BaseGetDataset._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery_v2.DatasetServiceClient.GetDataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "GetDataset",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DatasetServiceRestTransport._GetDataset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataset.Dataset()
            pb_resp = dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_dataset(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_dataset_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataset.Dataset.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.DatasetServiceClient.get_dataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "GetDataset",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _InsertDataset(
        _BaseDatasetServiceRestTransport._BaseInsertDataset, DatasetServiceRestStub
    ):
        def __hash__(self):
            return hash("DatasetServiceRestTransport.InsertDataset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: dataset.InsertDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataset.Dataset:
            r"""Call the insert dataset method over HTTP.

            Args:
                request (~.dataset.InsertDatasetRequest):
                    The request object. Request format for inserting a
                dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataset.Dataset:
                    Represents a BigQuery dataset.
            """

            http_options = (
                _BaseDatasetServiceRestTransport._BaseInsertDataset._get_http_options()
            )

            request, metadata = self._interceptor.pre_insert_dataset(request, metadata)
            transcoded_request = _BaseDatasetServiceRestTransport._BaseInsertDataset._get_transcoded_request(
                http_options, request
            )

            body = _BaseDatasetServiceRestTransport._BaseInsertDataset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDatasetServiceRestTransport._BaseInsertDataset._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery_v2.DatasetServiceClient.InsertDataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "InsertDataset",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DatasetServiceRestTransport._InsertDataset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataset.Dataset()
            pb_resp = dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_insert_dataset(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_insert_dataset_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataset.Dataset.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.DatasetServiceClient.insert_dataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "InsertDataset",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListDatasets(
        _BaseDatasetServiceRestTransport._BaseListDatasets, DatasetServiceRestStub
    ):
        def __hash__(self):
            return hash("DatasetServiceRestTransport.ListDatasets")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: dataset.ListDatasetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataset.DatasetList:
            r"""Call the list datasets method over HTTP.

            Args:
                request (~.dataset.ListDatasetsRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataset.DatasetList:
                    Response format for a page of results
                when listing datasets.

            """

            http_options = (
                _BaseDatasetServiceRestTransport._BaseListDatasets._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_datasets(request, metadata)
            transcoded_request = _BaseDatasetServiceRestTransport._BaseListDatasets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDatasetServiceRestTransport._BaseListDatasets._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery_v2.DatasetServiceClient.ListDatasets",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "ListDatasets",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DatasetServiceRestTransport._ListDatasets._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataset.DatasetList()
            pb_resp = dataset.DatasetList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_datasets(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_datasets_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataset.DatasetList.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.DatasetServiceClient.list_datasets",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "ListDatasets",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _PatchDataset(
        _BaseDatasetServiceRestTransport._BasePatchDataset, DatasetServiceRestStub
    ):
        def __hash__(self):
            return hash("DatasetServiceRestTransport.PatchDataset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: dataset.UpdateOrPatchDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataset.Dataset:
            r"""Call the patch dataset method over HTTP.

            Args:
                request (~.dataset.UpdateOrPatchDatasetRequest):
                    The request object. Message for updating or patching a
                dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataset.Dataset:
                    Represents a BigQuery dataset.
            """

            http_options = (
                _BaseDatasetServiceRestTransport._BasePatchDataset._get_http_options()
            )

            request, metadata = self._interceptor.pre_patch_dataset(request, metadata)
            transcoded_request = _BaseDatasetServiceRestTransport._BasePatchDataset._get_transcoded_request(
                http_options, request
            )

            body = _BaseDatasetServiceRestTransport._BasePatchDataset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDatasetServiceRestTransport._BasePatchDataset._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery_v2.DatasetServiceClient.PatchDataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "PatchDataset",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DatasetServiceRestTransport._PatchDataset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataset.Dataset()
            pb_resp = dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_patch_dataset(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_patch_dataset_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataset.Dataset.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.DatasetServiceClient.patch_dataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "PatchDataset",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UndeleteDataset(
        _BaseDatasetServiceRestTransport._BaseUndeleteDataset, DatasetServiceRestStub
    ):
        def __hash__(self):
            return hash("DatasetServiceRestTransport.UndeleteDataset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: dataset.UndeleteDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataset.Dataset:
            r"""Call the undelete dataset method over HTTP.

            Args:
                request (~.dataset.UndeleteDatasetRequest):
                    The request object. Request format for undeleting a
                dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataset.Dataset:
                    Represents a BigQuery dataset.
            """

            http_options = (
                _BaseDatasetServiceRestTransport._BaseUndeleteDataset._get_http_options()
            )

            request, metadata = self._interceptor.pre_undelete_dataset(
                request, metadata
            )
            transcoded_request = _BaseDatasetServiceRestTransport._BaseUndeleteDataset._get_transcoded_request(
                http_options, request
            )

            body = _BaseDatasetServiceRestTransport._BaseUndeleteDataset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDatasetServiceRestTransport._BaseUndeleteDataset._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery_v2.DatasetServiceClient.UndeleteDataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "UndeleteDataset",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DatasetServiceRestTransport._UndeleteDataset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataset.Dataset()
            pb_resp = dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_undelete_dataset(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_undelete_dataset_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataset.Dataset.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.DatasetServiceClient.undelete_dataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "UndeleteDataset",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateDataset(
        _BaseDatasetServiceRestTransport._BaseUpdateDataset, DatasetServiceRestStub
    ):
        def __hash__(self):
            return hash("DatasetServiceRestTransport.UpdateDataset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: dataset.UpdateOrPatchDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataset.Dataset:
            r"""Call the update dataset method over HTTP.

            Args:
                request (~.dataset.UpdateOrPatchDatasetRequest):
                    The request object. Message for updating or patching a
                dataset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataset.Dataset:
                    Represents a BigQuery dataset.
            """

            http_options = (
                _BaseDatasetServiceRestTransport._BaseUpdateDataset._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_dataset(request, metadata)
            transcoded_request = _BaseDatasetServiceRestTransport._BaseUpdateDataset._get_transcoded_request(
                http_options, request
            )

            body = _BaseDatasetServiceRestTransport._BaseUpdateDataset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDatasetServiceRestTransport._BaseUpdateDataset._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.bigquery_v2.DatasetServiceClient.UpdateDataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "UpdateDataset",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DatasetServiceRestTransport._UpdateDataset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataset.Dataset()
            pb_resp = dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_dataset(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_dataset_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataset.Dataset.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.DatasetServiceClient.update_dataset",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.DatasetService",
                        "rpcName": "UpdateDataset",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def delete_dataset(
        self,
    ) -> Callable[[dataset.DeleteDatasetRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_dataset(self) -> Callable[[dataset.GetDatasetRequest], dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert_dataset(
        self,
    ) -> Callable[[dataset.InsertDatasetRequest], dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InsertDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_datasets(
        self,
    ) -> Callable[[dataset.ListDatasetsRequest], dataset.DatasetList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatasets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch_dataset(
        self,
    ) -> Callable[[dataset.UpdateOrPatchDatasetRequest], dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PatchDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_dataset(
        self,
    ) -> Callable[[dataset.UndeleteDatasetRequest], dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_dataset(
        self,
    ) -> Callable[[dataset.UpdateOrPatchDatasetRequest], dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DatasetServiceRestTransport",)
