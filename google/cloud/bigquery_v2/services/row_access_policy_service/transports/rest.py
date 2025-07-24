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


from google.cloud.bigquery_v2.types import row_access_policy
from google.protobuf import empty_pb2  # type: ignore


from .rest_base import _BaseRowAccessPolicyServiceRestTransport
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


class RowAccessPolicyServiceRestInterceptor:
    """Interceptor for RowAccessPolicyService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RowAccessPolicyServiceRestTransport.

    .. code-block:: python
        class MyCustomRowAccessPolicyServiceInterceptor(RowAccessPolicyServiceRestInterceptor):
            def pre_batch_delete_row_access_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_create_row_access_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_row_access_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_row_access_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_row_access_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_row_access_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_row_access_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_row_access_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_row_access_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_row_access_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RowAccessPolicyServiceRestTransport(interceptor=MyCustomRowAccessPolicyServiceInterceptor())
        client = RowAccessPolicyServiceClient(transport=transport)


    """

    def pre_batch_delete_row_access_policies(
        self,
        request: row_access_policy.BatchDeleteRowAccessPoliciesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.BatchDeleteRowAccessPoliciesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for batch_delete_row_access_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RowAccessPolicyService server.
        """
        return request, metadata

    def pre_create_row_access_policy(
        self,
        request: row_access_policy.CreateRowAccessPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.CreateRowAccessPolicyRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_row_access_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RowAccessPolicyService server.
        """
        return request, metadata

    def post_create_row_access_policy(
        self, response: row_access_policy.RowAccessPolicy
    ) -> row_access_policy.RowAccessPolicy:
        """Post-rpc interceptor for create_row_access_policy

        DEPRECATED. Please use the `post_create_row_access_policy_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the RowAccessPolicyService server but before
        it is returned to user code. This `post_create_row_access_policy` interceptor runs
        before the `post_create_row_access_policy_with_metadata` interceptor.
        """
        return response

    def post_create_row_access_policy_with_metadata(
        self,
        response: row_access_policy.RowAccessPolicy,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.RowAccessPolicy, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for create_row_access_policy

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the RowAccessPolicyService server but before it is returned to user code.

        We recommend only using this `post_create_row_access_policy_with_metadata`
        interceptor in new development instead of the `post_create_row_access_policy` interceptor.
        When both interceptors are used, this `post_create_row_access_policy_with_metadata` interceptor runs after the
        `post_create_row_access_policy` interceptor. The (possibly modified) response returned by
        `post_create_row_access_policy` will be passed to
        `post_create_row_access_policy_with_metadata`.
        """
        return response, metadata

    def pre_delete_row_access_policy(
        self,
        request: row_access_policy.DeleteRowAccessPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.DeleteRowAccessPolicyRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_row_access_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RowAccessPolicyService server.
        """
        return request, metadata

    def pre_get_row_access_policy(
        self,
        request: row_access_policy.GetRowAccessPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.GetRowAccessPolicyRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_row_access_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RowAccessPolicyService server.
        """
        return request, metadata

    def post_get_row_access_policy(
        self, response: row_access_policy.RowAccessPolicy
    ) -> row_access_policy.RowAccessPolicy:
        """Post-rpc interceptor for get_row_access_policy

        DEPRECATED. Please use the `post_get_row_access_policy_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the RowAccessPolicyService server but before
        it is returned to user code. This `post_get_row_access_policy` interceptor runs
        before the `post_get_row_access_policy_with_metadata` interceptor.
        """
        return response

    def post_get_row_access_policy_with_metadata(
        self,
        response: row_access_policy.RowAccessPolicy,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.RowAccessPolicy, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get_row_access_policy

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the RowAccessPolicyService server but before it is returned to user code.

        We recommend only using this `post_get_row_access_policy_with_metadata`
        interceptor in new development instead of the `post_get_row_access_policy` interceptor.
        When both interceptors are used, this `post_get_row_access_policy_with_metadata` interceptor runs after the
        `post_get_row_access_policy` interceptor. The (possibly modified) response returned by
        `post_get_row_access_policy` will be passed to
        `post_get_row_access_policy_with_metadata`.
        """
        return response, metadata

    def pre_list_row_access_policies(
        self,
        request: row_access_policy.ListRowAccessPoliciesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.ListRowAccessPoliciesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_row_access_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RowAccessPolicyService server.
        """
        return request, metadata

    def post_list_row_access_policies(
        self, response: row_access_policy.ListRowAccessPoliciesResponse
    ) -> row_access_policy.ListRowAccessPoliciesResponse:
        """Post-rpc interceptor for list_row_access_policies

        DEPRECATED. Please use the `post_list_row_access_policies_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the RowAccessPolicyService server but before
        it is returned to user code. This `post_list_row_access_policies` interceptor runs
        before the `post_list_row_access_policies_with_metadata` interceptor.
        """
        return response

    def post_list_row_access_policies_with_metadata(
        self,
        response: row_access_policy.ListRowAccessPoliciesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.ListRowAccessPoliciesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_row_access_policies

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the RowAccessPolicyService server but before it is returned to user code.

        We recommend only using this `post_list_row_access_policies_with_metadata`
        interceptor in new development instead of the `post_list_row_access_policies` interceptor.
        When both interceptors are used, this `post_list_row_access_policies_with_metadata` interceptor runs after the
        `post_list_row_access_policies` interceptor. The (possibly modified) response returned by
        `post_list_row_access_policies` will be passed to
        `post_list_row_access_policies_with_metadata`.
        """
        return response, metadata

    def pre_update_row_access_policy(
        self,
        request: row_access_policy.UpdateRowAccessPolicyRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.UpdateRowAccessPolicyRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_row_access_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RowAccessPolicyService server.
        """
        return request, metadata

    def post_update_row_access_policy(
        self, response: row_access_policy.RowAccessPolicy
    ) -> row_access_policy.RowAccessPolicy:
        """Post-rpc interceptor for update_row_access_policy

        DEPRECATED. Please use the `post_update_row_access_policy_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the RowAccessPolicyService server but before
        it is returned to user code. This `post_update_row_access_policy` interceptor runs
        before the `post_update_row_access_policy_with_metadata` interceptor.
        """
        return response

    def post_update_row_access_policy_with_metadata(
        self,
        response: row_access_policy.RowAccessPolicy,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        row_access_policy.RowAccessPolicy, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for update_row_access_policy

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the RowAccessPolicyService server but before it is returned to user code.

        We recommend only using this `post_update_row_access_policy_with_metadata`
        interceptor in new development instead of the `post_update_row_access_policy` interceptor.
        When both interceptors are used, this `post_update_row_access_policy_with_metadata` interceptor runs after the
        `post_update_row_access_policy` interceptor. The (possibly modified) response returned by
        `post_update_row_access_policy` will be passed to
        `post_update_row_access_policy_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class RowAccessPolicyServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RowAccessPolicyServiceRestInterceptor


class RowAccessPolicyServiceRestTransport(_BaseRowAccessPolicyServiceRestTransport):
    """REST backend synchronous transport for RowAccessPolicyService.

    Service for interacting with row access policies.

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
        interceptor: Optional[RowAccessPolicyServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or RowAccessPolicyServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchDeleteRowAccessPolicies(
        _BaseRowAccessPolicyServiceRestTransport._BaseBatchDeleteRowAccessPolicies,
        RowAccessPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "RowAccessPolicyServiceRestTransport.BatchDeleteRowAccessPolicies"
            )

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
            request: row_access_policy.BatchDeleteRowAccessPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the batch delete row access
            policies method over HTTP.

                Args:
                    request (~.row_access_policy.BatchDeleteRowAccessPoliciesRequest):
                        The request object. Request message for the
                    BatchDeleteRowAccessPoliciesRequest
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.
            """

            http_options = (
                _BaseRowAccessPolicyServiceRestTransport._BaseBatchDeleteRowAccessPolicies._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_delete_row_access_policies(
                request, metadata
            )
            transcoded_request = _BaseRowAccessPolicyServiceRestTransport._BaseBatchDeleteRowAccessPolicies._get_transcoded_request(
                http_options, request
            )

            body = _BaseRowAccessPolicyServiceRestTransport._BaseBatchDeleteRowAccessPolicies._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRowAccessPolicyServiceRestTransport._BaseBatchDeleteRowAccessPolicies._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.BatchDeleteRowAccessPolicies",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "BatchDeleteRowAccessPolicies",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RowAccessPolicyServiceRestTransport._BatchDeleteRowAccessPolicies._get_response(
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

    class _CreateRowAccessPolicy(
        _BaseRowAccessPolicyServiceRestTransport._BaseCreateRowAccessPolicy,
        RowAccessPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("RowAccessPolicyServiceRestTransport.CreateRowAccessPolicy")

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
            request: row_access_policy.CreateRowAccessPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> row_access_policy.RowAccessPolicy:
            r"""Call the create row access policy method over HTTP.

            Args:
                request (~.row_access_policy.CreateRowAccessPolicyRequest):
                    The request object. Request message for the
                CreateRowAccessPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.row_access_policy.RowAccessPolicy:
                    Represents access on a subset of rows
                on the specified table, defined by its
                filter predicate. Access to the subset
                of rows is controlled by its IAM policy.

            """

            http_options = (
                _BaseRowAccessPolicyServiceRestTransport._BaseCreateRowAccessPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_row_access_policy(
                request, metadata
            )
            transcoded_request = _BaseRowAccessPolicyServiceRestTransport._BaseCreateRowAccessPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseRowAccessPolicyServiceRestTransport._BaseCreateRowAccessPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRowAccessPolicyServiceRestTransport._BaseCreateRowAccessPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.CreateRowAccessPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "CreateRowAccessPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RowAccessPolicyServiceRestTransport._CreateRowAccessPolicy._get_response(
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
            resp = row_access_policy.RowAccessPolicy()
            pb_resp = row_access_policy.RowAccessPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_row_access_policy(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_row_access_policy_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = row_access_policy.RowAccessPolicy.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.create_row_access_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "CreateRowAccessPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteRowAccessPolicy(
        _BaseRowAccessPolicyServiceRestTransport._BaseDeleteRowAccessPolicy,
        RowAccessPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("RowAccessPolicyServiceRestTransport.DeleteRowAccessPolicy")

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
            request: row_access_policy.DeleteRowAccessPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete row access policy method over HTTP.

            Args:
                request (~.row_access_policy.DeleteRowAccessPolicyRequest):
                    The request object. Request message for the
                DeleteRowAccessPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseRowAccessPolicyServiceRestTransport._BaseDeleteRowAccessPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_row_access_policy(
                request, metadata
            )
            transcoded_request = _BaseRowAccessPolicyServiceRestTransport._BaseDeleteRowAccessPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRowAccessPolicyServiceRestTransport._BaseDeleteRowAccessPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.DeleteRowAccessPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "DeleteRowAccessPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RowAccessPolicyServiceRestTransport._DeleteRowAccessPolicy._get_response(
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

    class _GetRowAccessPolicy(
        _BaseRowAccessPolicyServiceRestTransport._BaseGetRowAccessPolicy,
        RowAccessPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("RowAccessPolicyServiceRestTransport.GetRowAccessPolicy")

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
            request: row_access_policy.GetRowAccessPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> row_access_policy.RowAccessPolicy:
            r"""Call the get row access policy method over HTTP.

            Args:
                request (~.row_access_policy.GetRowAccessPolicyRequest):
                    The request object. Request message for the
                GetRowAccessPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.row_access_policy.RowAccessPolicy:
                    Represents access on a subset of rows
                on the specified table, defined by its
                filter predicate. Access to the subset
                of rows is controlled by its IAM policy.

            """

            http_options = (
                _BaseRowAccessPolicyServiceRestTransport._BaseGetRowAccessPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_row_access_policy(
                request, metadata
            )
            transcoded_request = _BaseRowAccessPolicyServiceRestTransport._BaseGetRowAccessPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRowAccessPolicyServiceRestTransport._BaseGetRowAccessPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.GetRowAccessPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "GetRowAccessPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                RowAccessPolicyServiceRestTransport._GetRowAccessPolicy._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = row_access_policy.RowAccessPolicy()
            pb_resp = row_access_policy.RowAccessPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_row_access_policy(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_row_access_policy_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = row_access_policy.RowAccessPolicy.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.get_row_access_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "GetRowAccessPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListRowAccessPolicies(
        _BaseRowAccessPolicyServiceRestTransport._BaseListRowAccessPolicies,
        RowAccessPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("RowAccessPolicyServiceRestTransport.ListRowAccessPolicies")

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
            request: row_access_policy.ListRowAccessPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> row_access_policy.ListRowAccessPoliciesResponse:
            r"""Call the list row access policies method over HTTP.

            Args:
                request (~.row_access_policy.ListRowAccessPoliciesRequest):
                    The request object. Request message for the
                ListRowAccessPolicies method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.row_access_policy.ListRowAccessPoliciesResponse:
                    Response message for the
                ListRowAccessPolicies method.

            """

            http_options = (
                _BaseRowAccessPolicyServiceRestTransport._BaseListRowAccessPolicies._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_row_access_policies(
                request, metadata
            )
            transcoded_request = _BaseRowAccessPolicyServiceRestTransport._BaseListRowAccessPolicies._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRowAccessPolicyServiceRestTransport._BaseListRowAccessPolicies._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.ListRowAccessPolicies",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "ListRowAccessPolicies",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RowAccessPolicyServiceRestTransport._ListRowAccessPolicies._get_response(
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
            resp = row_access_policy.ListRowAccessPoliciesResponse()
            pb_resp = row_access_policy.ListRowAccessPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_row_access_policies(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_row_access_policies_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        row_access_policy.ListRowAccessPoliciesResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.list_row_access_policies",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "ListRowAccessPolicies",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateRowAccessPolicy(
        _BaseRowAccessPolicyServiceRestTransport._BaseUpdateRowAccessPolicy,
        RowAccessPolicyServiceRestStub,
    ):
        def __hash__(self):
            return hash("RowAccessPolicyServiceRestTransport.UpdateRowAccessPolicy")

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
            request: row_access_policy.UpdateRowAccessPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> row_access_policy.RowAccessPolicy:
            r"""Call the update row access policy method over HTTP.

            Args:
                request (~.row_access_policy.UpdateRowAccessPolicyRequest):
                    The request object. Request message for the
                UpdateRowAccessPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.row_access_policy.RowAccessPolicy:
                    Represents access on a subset of rows
                on the specified table, defined by its
                filter predicate. Access to the subset
                of rows is controlled by its IAM policy.

            """

            http_options = (
                _BaseRowAccessPolicyServiceRestTransport._BaseUpdateRowAccessPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_row_access_policy(
                request, metadata
            )
            transcoded_request = _BaseRowAccessPolicyServiceRestTransport._BaseUpdateRowAccessPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseRowAccessPolicyServiceRestTransport._BaseUpdateRowAccessPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRowAccessPolicyServiceRestTransport._BaseUpdateRowAccessPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.UpdateRowAccessPolicy",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "UpdateRowAccessPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RowAccessPolicyServiceRestTransport._UpdateRowAccessPolicy._get_response(
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
            resp = row_access_policy.RowAccessPolicy()
            pb_resp = row_access_policy.RowAccessPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_row_access_policy(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_row_access_policy_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = row_access_policy.RowAccessPolicy.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.RowAccessPolicyServiceClient.update_row_access_policy",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.RowAccessPolicyService",
                        "rpcName": "UpdateRowAccessPolicy",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def batch_delete_row_access_policies(
        self,
    ) -> Callable[
        [row_access_policy.BatchDeleteRowAccessPoliciesRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteRowAccessPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_row_access_policy(
        self,
    ) -> Callable[
        [row_access_policy.CreateRowAccessPolicyRequest],
        row_access_policy.RowAccessPolicy,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRowAccessPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_row_access_policy(
        self,
    ) -> Callable[[row_access_policy.DeleteRowAccessPolicyRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRowAccessPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_row_access_policy(
        self,
    ) -> Callable[
        [row_access_policy.GetRowAccessPolicyRequest], row_access_policy.RowAccessPolicy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRowAccessPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_row_access_policies(
        self,
    ) -> Callable[
        [row_access_policy.ListRowAccessPoliciesRequest],
        row_access_policy.ListRowAccessPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRowAccessPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_row_access_policy(
        self,
    ) -> Callable[
        [row_access_policy.UpdateRowAccessPolicyRequest],
        row_access_policy.RowAccessPolicy,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRowAccessPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RowAccessPolicyServiceRestTransport",)
