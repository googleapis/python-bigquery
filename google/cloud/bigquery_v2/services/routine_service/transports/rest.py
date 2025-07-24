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


from google.cloud.bigquery_v2.types import routine
from google.protobuf import empty_pb2  # type: ignore


from .rest_base import _BaseRoutineServiceRestTransport
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


class RoutineServiceRestInterceptor:
    """Interceptor for RoutineService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RoutineServiceRestTransport.

    .. code-block:: python
        class MyCustomRoutineServiceInterceptor(RoutineServiceRestInterceptor):
            def pre_delete_routine(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_routine(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_routine(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert_routine(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert_routine(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_routines(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_routines(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_patch_routine(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch_routine(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_routine(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_routine(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RoutineServiceRestTransport(interceptor=MyCustomRoutineServiceInterceptor())
        client = RoutineServiceClient(transport=transport)


    """

    def pre_delete_routine(
        self,
        request: routine.DeleteRoutineRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.DeleteRoutineRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_routine

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RoutineService server.
        """
        return request, metadata

    def pre_get_routine(
        self,
        request: routine.GetRoutineRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.GetRoutineRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_routine

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RoutineService server.
        """
        return request, metadata

    def post_get_routine(self, response: routine.Routine) -> routine.Routine:
        """Post-rpc interceptor for get_routine

        DEPRECATED. Please use the `post_get_routine_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the RoutineService server but before
        it is returned to user code. This `post_get_routine` interceptor runs
        before the `post_get_routine_with_metadata` interceptor.
        """
        return response

    def post_get_routine_with_metadata(
        self,
        response: routine.Routine,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.Routine, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_routine

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the RoutineService server but before it is returned to user code.

        We recommend only using this `post_get_routine_with_metadata`
        interceptor in new development instead of the `post_get_routine` interceptor.
        When both interceptors are used, this `post_get_routine_with_metadata` interceptor runs after the
        `post_get_routine` interceptor. The (possibly modified) response returned by
        `post_get_routine` will be passed to
        `post_get_routine_with_metadata`.
        """
        return response, metadata

    def pre_insert_routine(
        self,
        request: routine.InsertRoutineRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.InsertRoutineRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for insert_routine

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RoutineService server.
        """
        return request, metadata

    def post_insert_routine(self, response: routine.Routine) -> routine.Routine:
        """Post-rpc interceptor for insert_routine

        DEPRECATED. Please use the `post_insert_routine_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the RoutineService server but before
        it is returned to user code. This `post_insert_routine` interceptor runs
        before the `post_insert_routine_with_metadata` interceptor.
        """
        return response

    def post_insert_routine_with_metadata(
        self,
        response: routine.Routine,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.Routine, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for insert_routine

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the RoutineService server but before it is returned to user code.

        We recommend only using this `post_insert_routine_with_metadata`
        interceptor in new development instead of the `post_insert_routine` interceptor.
        When both interceptors are used, this `post_insert_routine_with_metadata` interceptor runs after the
        `post_insert_routine` interceptor. The (possibly modified) response returned by
        `post_insert_routine` will be passed to
        `post_insert_routine_with_metadata`.
        """
        return response, metadata

    def pre_list_routines(
        self,
        request: routine.ListRoutinesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.ListRoutinesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_routines

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RoutineService server.
        """
        return request, metadata

    def post_list_routines(
        self, response: routine.ListRoutinesResponse
    ) -> routine.ListRoutinesResponse:
        """Post-rpc interceptor for list_routines

        DEPRECATED. Please use the `post_list_routines_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the RoutineService server but before
        it is returned to user code. This `post_list_routines` interceptor runs
        before the `post_list_routines_with_metadata` interceptor.
        """
        return response

    def post_list_routines_with_metadata(
        self,
        response: routine.ListRoutinesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.ListRoutinesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_routines

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the RoutineService server but before it is returned to user code.

        We recommend only using this `post_list_routines_with_metadata`
        interceptor in new development instead of the `post_list_routines` interceptor.
        When both interceptors are used, this `post_list_routines_with_metadata` interceptor runs after the
        `post_list_routines` interceptor. The (possibly modified) response returned by
        `post_list_routines` will be passed to
        `post_list_routines_with_metadata`.
        """
        return response, metadata

    def pre_update_routine(
        self,
        request: routine.UpdateRoutineRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.UpdateRoutineRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_routine

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RoutineService server.
        """
        return request, metadata

    def post_update_routine(self, response: routine.Routine) -> routine.Routine:
        """Post-rpc interceptor for update_routine

        DEPRECATED. Please use the `post_update_routine_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the RoutineService server but before
        it is returned to user code. This `post_update_routine` interceptor runs
        before the `post_update_routine_with_metadata` interceptor.
        """
        return response

    def post_update_routine_with_metadata(
        self,
        response: routine.Routine,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[routine.Routine, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_routine

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the RoutineService server but before it is returned to user code.

        We recommend only using this `post_update_routine_with_metadata`
        interceptor in new development instead of the `post_update_routine` interceptor.
        When both interceptors are used, this `post_update_routine_with_metadata` interceptor runs after the
        `post_update_routine` interceptor. The (possibly modified) response returned by
        `post_update_routine` will be passed to
        `post_update_routine_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class RoutineServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RoutineServiceRestInterceptor


class RoutineServiceRestTransport(_BaseRoutineServiceRestTransport):
    """REST backend synchronous transport for RoutineService.

    RoutineService provides management access to BigQuery
    routines.

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
        interceptor: Optional[RoutineServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or RoutineServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _DeleteRoutine(
        _BaseRoutineServiceRestTransport._BaseDeleteRoutine, RoutineServiceRestStub
    ):
        def __hash__(self):
            return hash("RoutineServiceRestTransport.DeleteRoutine")

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
            request: routine.DeleteRoutineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete routine method over HTTP.

            Args:
                request (~.routine.DeleteRoutineRequest):
                    The request object. Describes the format for deleting a
                routine.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseRoutineServiceRestTransport._BaseDeleteRoutine._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_routine(request, metadata)
            transcoded_request = _BaseRoutineServiceRestTransport._BaseDeleteRoutine._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRoutineServiceRestTransport._BaseDeleteRoutine._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RoutineServiceClient.DeleteRoutine",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "DeleteRoutine",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RoutineServiceRestTransport._DeleteRoutine._get_response(
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

    class _GetRoutine(
        _BaseRoutineServiceRestTransport._BaseGetRoutine, RoutineServiceRestStub
    ):
        def __hash__(self):
            return hash("RoutineServiceRestTransport.GetRoutine")

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
            request: routine.GetRoutineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> routine.Routine:
            r"""Call the get routine method over HTTP.

            Args:
                request (~.routine.GetRoutineRequest):
                    The request object. Describes the format for getting
                information about a routine.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.routine.Routine:
                    A user-defined function or a stored
                procedure.

            """

            http_options = (
                _BaseRoutineServiceRestTransport._BaseGetRoutine._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_routine(request, metadata)
            transcoded_request = _BaseRoutineServiceRestTransport._BaseGetRoutine._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseRoutineServiceRestTransport._BaseGetRoutine._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RoutineServiceClient.GetRoutine",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "GetRoutine",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RoutineServiceRestTransport._GetRoutine._get_response(
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
            resp = routine.Routine()
            pb_resp = routine.Routine.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_routine(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_routine_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = routine.Routine.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.RoutineServiceClient.get_routine",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "GetRoutine",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _InsertRoutine(
        _BaseRoutineServiceRestTransport._BaseInsertRoutine, RoutineServiceRestStub
    ):
        def __hash__(self):
            return hash("RoutineServiceRestTransport.InsertRoutine")

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
            request: routine.InsertRoutineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> routine.Routine:
            r"""Call the insert routine method over HTTP.

            Args:
                request (~.routine.InsertRoutineRequest):
                    The request object. Describes the format for inserting a
                routine.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.routine.Routine:
                    A user-defined function or a stored
                procedure.

            """

            http_options = (
                _BaseRoutineServiceRestTransport._BaseInsertRoutine._get_http_options()
            )

            request, metadata = self._interceptor.pre_insert_routine(request, metadata)
            transcoded_request = _BaseRoutineServiceRestTransport._BaseInsertRoutine._get_transcoded_request(
                http_options, request
            )

            body = _BaseRoutineServiceRestTransport._BaseInsertRoutine._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRoutineServiceRestTransport._BaseInsertRoutine._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RoutineServiceClient.InsertRoutine",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "InsertRoutine",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RoutineServiceRestTransport._InsertRoutine._get_response(
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
            resp = routine.Routine()
            pb_resp = routine.Routine.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_insert_routine(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_insert_routine_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = routine.Routine.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.RoutineServiceClient.insert_routine",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "InsertRoutine",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListRoutines(
        _BaseRoutineServiceRestTransport._BaseListRoutines, RoutineServiceRestStub
    ):
        def __hash__(self):
            return hash("RoutineServiceRestTransport.ListRoutines")

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
            request: routine.ListRoutinesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> routine.ListRoutinesResponse:
            r"""Call the list routines method over HTTP.

            Args:
                request (~.routine.ListRoutinesRequest):
                    The request object. Describes the format for listing
                routines.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.routine.ListRoutinesResponse:
                    Describes the format of a single
                result page when listing routines.

            """

            http_options = (
                _BaseRoutineServiceRestTransport._BaseListRoutines._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_routines(request, metadata)
            transcoded_request = _BaseRoutineServiceRestTransport._BaseListRoutines._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRoutineServiceRestTransport._BaseListRoutines._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RoutineServiceClient.ListRoutines",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "ListRoutines",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RoutineServiceRestTransport._ListRoutines._get_response(
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
            resp = routine.ListRoutinesResponse()
            pb_resp = routine.ListRoutinesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_routines(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_routines_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = routine.ListRoutinesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.RoutineServiceClient.list_routines",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "ListRoutines",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _PatchRoutine(
        _BaseRoutineServiceRestTransport._BasePatchRoutine, RoutineServiceRestStub
    ):
        def __hash__(self):
            return hash("RoutineServiceRestTransport.PatchRoutine")

        def __call__(
            self,
            request: routine.PatchRoutineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> routine.Routine:
            raise NotImplementedError(
                "Method PatchRoutine is not available over REST transport"
            )

    class _UpdateRoutine(
        _BaseRoutineServiceRestTransport._BaseUpdateRoutine, RoutineServiceRestStub
    ):
        def __hash__(self):
            return hash("RoutineServiceRestTransport.UpdateRoutine")

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
            request: routine.UpdateRoutineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> routine.Routine:
            r"""Call the update routine method over HTTP.

            Args:
                request (~.routine.UpdateRoutineRequest):
                    The request object. Describes the format for updating a
                routine.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.routine.Routine:
                    A user-defined function or a stored
                procedure.

            """

            http_options = (
                _BaseRoutineServiceRestTransport._BaseUpdateRoutine._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_routine(request, metadata)
            transcoded_request = _BaseRoutineServiceRestTransport._BaseUpdateRoutine._get_transcoded_request(
                http_options, request
            )

            body = _BaseRoutineServiceRestTransport._BaseUpdateRoutine._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRoutineServiceRestTransport._BaseUpdateRoutine._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RoutineServiceClient.UpdateRoutine",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "UpdateRoutine",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RoutineServiceRestTransport._UpdateRoutine._get_response(
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
            resp = routine.Routine()
            pb_resp = routine.Routine.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_routine(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_routine_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = routine.Routine.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.RoutineServiceClient.update_routine",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RoutineService",
                        "rpcName": "UpdateRoutine",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def delete_routine(
        self,
    ) -> Callable[[routine.DeleteRoutineRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRoutine(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_routine(self) -> Callable[[routine.GetRoutineRequest], routine.Routine]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRoutine(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert_routine(
        self,
    ) -> Callable[[routine.InsertRoutineRequest], routine.Routine]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InsertRoutine(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_routines(
        self,
    ) -> Callable[[routine.ListRoutinesRequest], routine.ListRoutinesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRoutines(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch_routine(self) -> Callable[[routine.PatchRoutineRequest], routine.Routine]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PatchRoutine(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_routine(
        self,
    ) -> Callable[[routine.UpdateRoutineRequest], routine.Routine]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRoutine(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RoutineServiceRestTransport",)
