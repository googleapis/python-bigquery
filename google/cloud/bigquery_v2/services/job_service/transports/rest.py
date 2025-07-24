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


from google.cloud.bigquery_v2.types import job
from google.protobuf import empty_pb2  # type: ignore


from .rest_base import _BaseJobServiceRestTransport
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


class JobServiceRestInterceptor:
    """Interceptor for JobService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the JobServiceRestTransport.

    .. code-block:: python
        class MyCustomJobServiceInterceptor(JobServiceRestInterceptor):
            def pre_cancel_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_query_results(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_query_results(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_query(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = JobServiceRestTransport(interceptor=MyCustomJobServiceInterceptor())
        client = JobServiceClient(transport=transport)


    """

    def pre_cancel_job(
        self,
        request: job.CancelJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.CancelJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for cancel_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_cancel_job(self, response: job.JobCancelResponse) -> job.JobCancelResponse:
        """Post-rpc interceptor for cancel_job

        DEPRECATED. Please use the `post_cancel_job_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code. This `post_cancel_job` interceptor runs
        before the `post_cancel_job_with_metadata` interceptor.
        """
        return response

    def post_cancel_job_with_metadata(
        self,
        response: job.JobCancelResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.JobCancelResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for cancel_job

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the JobService server but before it is returned to user code.

        We recommend only using this `post_cancel_job_with_metadata`
        interceptor in new development instead of the `post_cancel_job` interceptor.
        When both interceptors are used, this `post_cancel_job_with_metadata` interceptor runs after the
        `post_cancel_job` interceptor. The (possibly modified) response returned by
        `post_cancel_job` will be passed to
        `post_cancel_job_with_metadata`.
        """
        return response, metadata

    def pre_delete_job(
        self,
        request: job.DeleteJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.DeleteJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def pre_get_job(
        self,
        request: job.GetJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.GetJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_get_job(self, response: job.Job) -> job.Job:
        """Post-rpc interceptor for get_job

        DEPRECATED. Please use the `post_get_job_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code. This `post_get_job` interceptor runs
        before the `post_get_job_with_metadata` interceptor.
        """
        return response

    def post_get_job_with_metadata(
        self, response: job.Job, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[job.Job, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_job

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the JobService server but before it is returned to user code.

        We recommend only using this `post_get_job_with_metadata`
        interceptor in new development instead of the `post_get_job` interceptor.
        When both interceptors are used, this `post_get_job_with_metadata` interceptor runs after the
        `post_get_job` interceptor. The (possibly modified) response returned by
        `post_get_job` will be passed to
        `post_get_job_with_metadata`.
        """
        return response, metadata

    def pre_get_query_results(
        self,
        request: job.GetQueryResultsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.GetQueryResultsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_query_results

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_get_query_results(
        self, response: job.GetQueryResultsResponse
    ) -> job.GetQueryResultsResponse:
        """Post-rpc interceptor for get_query_results

        DEPRECATED. Please use the `post_get_query_results_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code. This `post_get_query_results` interceptor runs
        before the `post_get_query_results_with_metadata` interceptor.
        """
        return response

    def post_get_query_results_with_metadata(
        self,
        response: job.GetQueryResultsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.GetQueryResultsResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_query_results

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the JobService server but before it is returned to user code.

        We recommend only using this `post_get_query_results_with_metadata`
        interceptor in new development instead of the `post_get_query_results` interceptor.
        When both interceptors are used, this `post_get_query_results_with_metadata` interceptor runs after the
        `post_get_query_results` interceptor. The (possibly modified) response returned by
        `post_get_query_results` will be passed to
        `post_get_query_results_with_metadata`.
        """
        return response, metadata

    def pre_insert_job(
        self,
        request: job.InsertJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.InsertJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for insert_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_insert_job(self, response: job.Job) -> job.Job:
        """Post-rpc interceptor for insert_job

        DEPRECATED. Please use the `post_insert_job_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code. This `post_insert_job` interceptor runs
        before the `post_insert_job_with_metadata` interceptor.
        """
        return response

    def post_insert_job_with_metadata(
        self, response: job.Job, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[job.Job, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for insert_job

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the JobService server but before it is returned to user code.

        We recommend only using this `post_insert_job_with_metadata`
        interceptor in new development instead of the `post_insert_job` interceptor.
        When both interceptors are used, this `post_insert_job_with_metadata` interceptor runs after the
        `post_insert_job` interceptor. The (possibly modified) response returned by
        `post_insert_job` will be passed to
        `post_insert_job_with_metadata`.
        """
        return response, metadata

    def pre_list_jobs(
        self,
        request: job.ListJobsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.ListJobsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_list_jobs(self, response: job.JobList) -> job.JobList:
        """Post-rpc interceptor for list_jobs

        DEPRECATED. Please use the `post_list_jobs_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code. This `post_list_jobs` interceptor runs
        before the `post_list_jobs_with_metadata` interceptor.
        """
        return response

    def post_list_jobs_with_metadata(
        self, response: job.JobList, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[job.JobList, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_jobs

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the JobService server but before it is returned to user code.

        We recommend only using this `post_list_jobs_with_metadata`
        interceptor in new development instead of the `post_list_jobs` interceptor.
        When both interceptors are used, this `post_list_jobs_with_metadata` interceptor runs after the
        `post_list_jobs` interceptor. The (possibly modified) response returned by
        `post_list_jobs` will be passed to
        `post_list_jobs_with_metadata`.
        """
        return response, metadata

    def pre_query(
        self,
        request: job.PostQueryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.PostQueryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for query

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_query(self, response: job.QueryResponse) -> job.QueryResponse:
        """Post-rpc interceptor for query

        DEPRECATED. Please use the `post_query_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code. This `post_query` interceptor runs
        before the `post_query_with_metadata` interceptor.
        """
        return response

    def post_query_with_metadata(
        self,
        response: job.QueryResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job.QueryResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for query

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the JobService server but before it is returned to user code.

        We recommend only using this `post_query_with_metadata`
        interceptor in new development instead of the `post_query` interceptor.
        When both interceptors are used, this `post_query_with_metadata` interceptor runs after the
        `post_query` interceptor. The (possibly modified) response returned by
        `post_query` will be passed to
        `post_query_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class JobServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: JobServiceRestInterceptor


class JobServiceRestTransport(_BaseJobServiceRestTransport):
    """REST backend synchronous transport for JobService.

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
        interceptor: Optional[JobServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or JobServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CancelJob(_BaseJobServiceRestTransport._BaseCancelJob, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.CancelJob")

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
            request: job.CancelJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job.JobCancelResponse:
            r"""Call the cancel job method over HTTP.

            Args:
                request (~.job.CancelJobRequest):
                    The request object. Describes format of a jobs
                cancellation request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job.JobCancelResponse:
                    Describes format of a jobs
                cancellation response.

            """

            http_options = (
                _BaseJobServiceRestTransport._BaseCancelJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_job(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseCancelJob._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseCancelJob._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.JobServiceClient.CancelJob",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "CancelJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._CancelJob._get_response(
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
            resp = job.JobCancelResponse()
            pb_resp = job.JobCancelResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_cancel_job(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_cancel_job_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job.JobCancelResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.JobServiceClient.cancel_job",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "CancelJob",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteJob(_BaseJobServiceRestTransport._BaseDeleteJob, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.DeleteJob")

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
            request: job.DeleteJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete job method over HTTP.

            Args:
                request (~.job.DeleteJobRequest):
                    The request object. Describes the format of a jobs
                deletion request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseJobServiceRestTransport._BaseDeleteJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_job(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseDeleteJob._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseDeleteJob._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.JobServiceClient.DeleteJob",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "DeleteJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._DeleteJob._get_response(
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

    class _GetJob(_BaseJobServiceRestTransport._BaseGetJob, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.GetJob")

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
            request: job.GetJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job.Job:
            r"""Call the get job method over HTTP.

            Args:
                request (~.job.GetJobRequest):
                    The request object. Describes format of a jobs get
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job.Job:

            """

            http_options = _BaseJobServiceRestTransport._BaseGetJob._get_http_options()

            request, metadata = self._interceptor.pre_get_job(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseGetJob._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseGetJob._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.JobServiceClient.GetJob",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "GetJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._GetJob._get_response(
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
            resp = job.Job()
            pb_resp = job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_job(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_job_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job.Job.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.JobServiceClient.get_job",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "GetJob",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetQueryResults(
        _BaseJobServiceRestTransport._BaseGetQueryResults, JobServiceRestStub
    ):
        def __hash__(self):
            return hash("JobServiceRestTransport.GetQueryResults")

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
            request: job.GetQueryResultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job.GetQueryResultsResponse:
            r"""Call the get query results method over HTTP.

            Args:
                request (~.job.GetQueryResultsRequest):
                    The request object. Request object of GetQueryResults.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job.GetQueryResultsResponse:
                    Response object of GetQueryResults.
            """

            http_options = (
                _BaseJobServiceRestTransport._BaseGetQueryResults._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_query_results(
                request, metadata
            )
            transcoded_request = _BaseJobServiceRestTransport._BaseGetQueryResults._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseJobServiceRestTransport._BaseGetQueryResults._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.JobServiceClient.GetQueryResults",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "GetQueryResults",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._GetQueryResults._get_response(
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
            resp = job.GetQueryResultsResponse()
            pb_resp = job.GetQueryResultsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_query_results(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_query_results_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job.GetQueryResultsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.JobServiceClient.get_query_results",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "GetQueryResults",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _InsertJob(_BaseJobServiceRestTransport._BaseInsertJob, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.InsertJob")

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
            request: job.InsertJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job.Job:
            r"""Call the insert job method over HTTP.

            Args:
                request (~.job.InsertJobRequest):
                    The request object. Describes format of a job insertion
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job.Job:

            """

            http_options = (
                _BaseJobServiceRestTransport._BaseInsertJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_insert_job(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseInsertJob._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseJobServiceRestTransport._BaseInsertJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseInsertJob._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.JobServiceClient.InsertJob",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "InsertJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._InsertJob._get_response(
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
            resp = job.Job()
            pb_resp = job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_insert_job(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_insert_job_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job.Job.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.JobServiceClient.insert_job",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "InsertJob",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListJobs(_BaseJobServiceRestTransport._BaseListJobs, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.ListJobs")

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
            request: job.ListJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job.JobList:
            r"""Call the list jobs method over HTTP.

            Args:
                request (~.job.ListJobsRequest):
                    The request object. Describes the format of the list jobs
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job.JobList:
                    JobList is the response format for a
                jobs.list call.

            """

            http_options = (
                _BaseJobServiceRestTransport._BaseListJobs._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_jobs(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseListJobs._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseListJobs._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.JobServiceClient.ListJobs",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "ListJobs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._ListJobs._get_response(
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
            resp = job.JobList()
            pb_resp = job.JobList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_jobs(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_jobs_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job.JobList.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.JobServiceClient.list_jobs",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "ListJobs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Query(_BaseJobServiceRestTransport._BaseQuery, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.Query")

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
            request: job.PostQueryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job.QueryResponse:
            r"""Call the query method over HTTP.

            Args:
                request (~.job.PostQueryRequest):
                    The request object. Request format for the query request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job.QueryResponse:

            """

            http_options = _BaseJobServiceRestTransport._BaseQuery._get_http_options()

            request, metadata = self._interceptor.pre_query(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseQuery._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseJobServiceRestTransport._BaseQuery._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseQuery._get_query_params_json(
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
                    f"Sending request for google.cloud.bigquery_v2.JobServiceClient.Query",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "Query",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._Query._get_response(
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
            resp = job.QueryResponse()
            pb_resp = job.QueryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_query(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_query_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job.QueryResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.bigquery_v2.JobServiceClient.query",
                    extra={
                        "serviceName": "google.cloud.bigquery.v2.JobService",
                        "rpcName": "Query",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def cancel_job(self) -> Callable[[job.CancelJobRequest], job.JobCancelResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_job(self) -> Callable[[job.DeleteJobRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_job(self) -> Callable[[job.GetJobRequest], job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_query_results(
        self,
    ) -> Callable[[job.GetQueryResultsRequest], job.GetQueryResultsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetQueryResults(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert_job(self) -> Callable[[job.InsertJobRequest], job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InsertJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_jobs(self) -> Callable[[job.ListJobsRequest], job.JobList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query(self) -> Callable[[job.PostQueryRequest], job.QueryResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Query(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("JobServiceRestTransport",)
