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


from google.cloud.bigquery_v2.types import table
from google.protobuf import empty_pb2  # type: ignore


from .rest_base import _BaseTableServiceRestTransport
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


class TableServiceRestInterceptor:
    """Interceptor for TableService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the TableServiceRestTransport.

    .. code-block:: python
        class MyCustomTableServiceInterceptor(TableServiceRestInterceptor):
            def pre_delete_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_tables(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_tables(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_patch_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_table(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = TableServiceRestTransport(interceptor=MyCustomTableServiceInterceptor())
        client = TableServiceClient(transport=transport)


    """

    def pre_delete_table(
        self,
        request: table.DeleteTableRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[table.DeleteTableRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TableService server.
        """
        return request, metadata

    def pre_get_table(
        self,
        request: table.GetTableRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[table.GetTableRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TableService server.
        """
        return request, metadata

    def post_get_table(self, response: table.Table) -> table.Table:
        """Post-rpc interceptor for get_table

        DEPRECATED. Please use the `post_get_table_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TableService server but before
        it is returned to user code. This `post_get_table` interceptor runs
        before the `post_get_table_with_metadata` interceptor.
        """
        return response

    def post_get_table_with_metadata(
        self, response: table.Table, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[table.Table, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_table

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TableService server but before it is returned to user code.

        We recommend only using this `post_get_table_with_metadata`
        interceptor in new development instead of the `post_get_table` interceptor.
        When both interceptors are used, this `post_get_table_with_metadata` interceptor runs after the
        `post_get_table` interceptor. The (possibly modified) response returned by
        `post_get_table` will be passed to
        `post_get_table_with_metadata`.
        """
        return response, metadata

    def pre_insert_table(
        self,
        request: table.InsertTableRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[table.InsertTableRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for insert_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TableService server.
        """
        return request, metadata

    def post_insert_table(self, response: table.Table) -> table.Table:
        """Post-rpc interceptor for insert_table

        DEPRECATED. Please use the `post_insert_table_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TableService server but before
        it is returned to user code. This `post_insert_table` interceptor runs
        before the `post_insert_table_with_metadata` interceptor.
        """
        return response

    def post_insert_table_with_metadata(
        self, response: table.Table, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[table.Table, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for insert_table

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TableService server but before it is returned to user code.

        We recommend only using this `post_insert_table_with_metadata`
        interceptor in new development instead of the `post_insert_table` interceptor.
        When both interceptors are used, this `post_insert_table_with_metadata` interceptor runs after the
        `post_insert_table` interceptor. The (possibly modified) response returned by
        `post_insert_table` will be passed to
        `post_insert_table_with_metadata`.
        """
        return response, metadata

    def pre_list_tables(
        self,
        request: table.ListTablesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[table.ListTablesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_tables

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TableService server.
        """
        return request, metadata

    def post_list_tables(self, response: table.TableList) -> table.TableList:
        """Post-rpc interceptor for list_tables

        DEPRECATED. Please use the `post_list_tables_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TableService server but before
        it is returned to user code. This `post_list_tables` interceptor runs
        before the `post_list_tables_with_metadata` interceptor.
        """
        return response

    def post_list_tables_with_metadata(
        self,
        response: table.TableList,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[table.TableList, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_tables

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TableService server but before it is returned to user code.

        We recommend only using this `post_list_tables_with_metadata`
        interceptor in new development instead of the `post_list_tables` interceptor.
        When both interceptors are used, this `post_list_tables_with_metadata` interceptor runs after the
        `post_list_tables` interceptor. The (possibly modified) response returned by
        `post_list_tables` will be passed to
        `post_list_tables_with_metadata`.
        """
        return response, metadata

    def pre_patch_table(
        self,
        request: table.UpdateOrPatchTableRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        table.UpdateOrPatchTableRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for patch_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TableService server.
        """
        return request, metadata

    def post_patch_table(self, response: table.Table) -> table.Table:
        """Post-rpc interceptor for patch_table

        DEPRECATED. Please use the `post_patch_table_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TableService server but before
        it is returned to user code. This `post_patch_table` interceptor runs
        before the `post_patch_table_with_metadata` interceptor.
        """
        return response

    def post_patch_table_with_metadata(
        self, response: table.Table, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[table.Table, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for patch_table

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TableService server but before it is returned to user code.

        We recommend only using this `post_patch_table_with_metadata`
        interceptor in new development instead of the `post_patch_table` interceptor.
        When both interceptors are used, this `post_patch_table_with_metadata` interceptor runs after the
        `post_patch_table` interceptor. The (possibly modified) response returned by
        `post_patch_table` will be passed to
        `post_patch_table_with_metadata`.
        """
        return response, metadata

    def pre_update_table(
        self,
        request: table.UpdateOrPatchTableRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        table.UpdateOrPatchTableRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TableService server.
        """
        return request, metadata

    def post_update_table(self, response: table.Table) -> table.Table:
        """Post-rpc interceptor for update_table

        DEPRECATED. Please use the `post_update_table_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the TableService server but before
        it is returned to user code. This `post_update_table` interceptor runs
        before the `post_update_table_with_metadata` interceptor.
        """
        return response

    def post_update_table_with_metadata(
        self, response: table.Table, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[table.Table, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_table

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the TableService server but before it is returned to user code.

        We recommend only using this `post_update_table_with_metadata`
        interceptor in new development instead of the `post_update_table` interceptor.
        When both interceptors are used, this `post_update_table_with_metadata` interceptor runs after the
        `post_update_table` interceptor. The (possibly modified) response returned by
        `post_update_table` will be passed to
        `post_update_table_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class TableServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: TableServiceRestInterceptor


class TableServiceRestTransport(_BaseTableServiceRestTransport):
    """REST backend synchronous transport for TableService.

    TableService provides methods for managing BigQuery tables
    and table-like entities such as views and snapshots.

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
        interceptor: Optional[TableServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or TableServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _DeleteTable(
        _BaseTableServiceRestTransport._BaseDeleteTable, TableServiceRestStub
    ):
        def __hash__(self):
            return hash("TableServiceRestTransport.DeleteTable")

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
            request: table.DeleteTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete table method over HTTP.

            Args:
                request (~.table.DeleteTableRequest):
                    The request object. Request format for deleting a table.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseTableServiceRestTransport._BaseDeleteTable._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_table(request, metadata)
            transcoded_request = (
                _BaseTableServiceRestTransport._BaseDeleteTable._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTableServiceRestTransport._BaseDeleteTable._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.TableServiceClient.DeleteTable",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "DeleteTable",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TableServiceRestTransport._DeleteTable._get_response(
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

    class _GetTable(_BaseTableServiceRestTransport._BaseGetTable, TableServiceRestStub):
        def __hash__(self):
            return hash("TableServiceRestTransport.GetTable")

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
            request: table.GetTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> table.Table:
            r"""Call the get table method over HTTP.

            Args:
                request (~.table.GetTableRequest):
                    The request object. Request format for getting table
                metadata.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.table.Table:

            """

            http_options = (
                _BaseTableServiceRestTransport._BaseGetTable._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_table(request, metadata)
            transcoded_request = (
                _BaseTableServiceRestTransport._BaseGetTable._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTableServiceRestTransport._BaseGetTable._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.TableServiceClient.GetTable",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "GetTable",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TableServiceRestTransport._GetTable._get_response(
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
            resp = table.Table()
            pb_resp = table.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_table(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_table_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = table.Table.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.TableServiceClient.get_table",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "GetTable",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _InsertTable(
        _BaseTableServiceRestTransport._BaseInsertTable, TableServiceRestStub
    ):
        def __hash__(self):
            return hash("TableServiceRestTransport.InsertTable")

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
            request: table.InsertTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> table.Table:
            r"""Call the insert table method over HTTP.

            Args:
                request (~.table.InsertTableRequest):
                    The request object. Request format for inserting table
                metadata.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.table.Table:

            """

            http_options = (
                _BaseTableServiceRestTransport._BaseInsertTable._get_http_options()
            )

            request, metadata = self._interceptor.pre_insert_table(request, metadata)
            transcoded_request = (
                _BaseTableServiceRestTransport._BaseInsertTable._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseTableServiceRestTransport._BaseInsertTable._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTableServiceRestTransport._BaseInsertTable._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.TableServiceClient.InsertTable",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "InsertTable",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TableServiceRestTransport._InsertTable._get_response(
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
            resp = table.Table()
            pb_resp = table.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_insert_table(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_insert_table_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = table.Table.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.TableServiceClient.insert_table",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "InsertTable",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListTables(
        _BaseTableServiceRestTransport._BaseListTables, TableServiceRestStub
    ):
        def __hash__(self):
            return hash("TableServiceRestTransport.ListTables")

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
            request: table.ListTablesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> table.TableList:
            r"""Call the list tables method over HTTP.

            Args:
                request (~.table.ListTablesRequest):
                    The request object. Request format for enumerating
                tables.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.table.TableList:
                    Partial projection of the metadata
                for a given table in a list response.

            """

            http_options = (
                _BaseTableServiceRestTransport._BaseListTables._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_tables(request, metadata)
            transcoded_request = (
                _BaseTableServiceRestTransport._BaseListTables._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTableServiceRestTransport._BaseListTables._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.TableServiceClient.ListTables",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "ListTables",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TableServiceRestTransport._ListTables._get_response(
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
            resp = table.TableList()
            pb_resp = table.TableList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_tables(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_tables_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = table.TableList.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.TableServiceClient.list_tables",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "ListTables",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _PatchTable(
        _BaseTableServiceRestTransport._BasePatchTable, TableServiceRestStub
    ):
        def __hash__(self):
            return hash("TableServiceRestTransport.PatchTable")

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
            request: table.UpdateOrPatchTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> table.Table:
            r"""Call the patch table method over HTTP.

            Args:
                request (~.table.UpdateOrPatchTableRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.table.Table:

            """

            http_options = (
                _BaseTableServiceRestTransport._BasePatchTable._get_http_options()
            )

            request, metadata = self._interceptor.pre_patch_table(request, metadata)
            transcoded_request = (
                _BaseTableServiceRestTransport._BasePatchTable._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseTableServiceRestTransport._BasePatchTable._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTableServiceRestTransport._BasePatchTable._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.TableServiceClient.PatchTable",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "PatchTable",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TableServiceRestTransport._PatchTable._get_response(
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
            resp = table.Table()
            pb_resp = table.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_patch_table(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_patch_table_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = table.Table.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.TableServiceClient.patch_table",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "PatchTable",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateTable(
        _BaseTableServiceRestTransport._BaseUpdateTable, TableServiceRestStub
    ):
        def __hash__(self):
            return hash("TableServiceRestTransport.UpdateTable")

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
            request: table.UpdateOrPatchTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> table.Table:
            r"""Call the update table method over HTTP.

            Args:
                request (~.table.UpdateOrPatchTableRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.table.Table:

            """

            http_options = (
                _BaseTableServiceRestTransport._BaseUpdateTable._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_table(request, metadata)
            transcoded_request = (
                _BaseTableServiceRestTransport._BaseUpdateTable._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseTableServiceRestTransport._BaseUpdateTable._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTableServiceRestTransport._BaseUpdateTable._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.TableServiceClient.UpdateTable",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "UpdateTable",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = TableServiceRestTransport._UpdateTable._get_response(
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
            resp = table.Table()
            pb_resp = table.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_table(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_table_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = table.Table.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.TableServiceClient.update_table",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.TableService",
                        "rpcName": "UpdateTable",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def delete_table(self) -> Callable[[table.DeleteTableRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_table(self) -> Callable[[table.GetTableRequest], table.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert_table(self) -> Callable[[table.InsertTableRequest], table.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InsertTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_tables(self) -> Callable[[table.ListTablesRequest], table.TableList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTables(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch_table(self) -> Callable[[table.UpdateOrPatchTableRequest], table.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PatchTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_table(self) -> Callable[[table.UpdateOrPatchTableRequest], table.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("TableServiceRestTransport",)
