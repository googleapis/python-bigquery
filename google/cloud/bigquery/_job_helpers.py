# Copyright 2021 Google LLC
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

"""Helpers for interacting with the job REST APIs from the client."""

import copy
import uuid
from typing import Any, Dict, TYPE_CHECKING, Optional

import google.api_core.exceptions as core_exceptions
from google.api_core import retry as retries

from google.cloud.bigquery import job

# Avoid circular imports
if TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud.bigquery.client import Client


_TIMEOUT_BUFFER_SECS = 0.1


def make_job_id(job_id: Optional[str] = None, prefix: Optional[str] = None) -> str:
    """Construct an ID for a new job.

    Args:
        job_id (Optional[str]): the user-provided job ID.

        prefix (Optional[str]): the user-provided prefix for a job ID.

    Returns:
        str: A job ID
    """
    if job_id is not None:
        return job_id
    elif prefix is not None:
        return str(prefix) + str(uuid.uuid4())
    else:
        return str(uuid.uuid4())


def query_jobs_insert(
    client: "Client",
    query: str,
    job_config: job.QueryJobConfig,
    job_id: str,
    job_id_prefix: str,
    location: str,
    project: str,
    retry: retries.Retry,
    timeout: Optional[float],
    job_retry: retries.Retry,
):
    """Initiate a query using jobs.insert.

    See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    """
    job_id_given = job_id is not None
    job_id_save = job_id
    job_config_save = job_config

    def do_query():
        # Make a copy now, so that original doesn't get changed by the process
        # below and to facilitate retry
        job_config = copy.deepcopy(job_config_save)

        job_id = make_job_id(job_id_save, job_id_prefix)
        job_ref = job._JobReference(job_id, project=project, location=location)
        query_job = job.QueryJob(job_ref, query, client=client, job_config=job_config)

        try:
            query_job._begin(retry=retry, timeout=timeout)
        except core_exceptions.Conflict as create_exc:
            # The thought is if someone is providing their own job IDs and they get
            # their job ID generation wrong, this could end up returning results for
            # the wrong query. We thus only try to recover if job ID was not given.
            if job_id_given:
                raise create_exc

            try:
                query_job = client.get_job(
                    job_id,
                    project=project,
                    location=location,
                    retry=retry,
                    timeout=timeout,
                )
            except core_exceptions.GoogleAPIError:  # (includes RetryError)
                raise create_exc
            else:
                return query_job
        else:
            return query_job

    future = do_query()
    # The future might be in a failed state now, but if it's
    # unrecoverable, we'll find out when we ask for it's result, at which
    # point, we may retry.
    if not job_id_given:
        future._retry_do_query = do_query  # in case we have to retry later
        future._job_retry = job_retry

    return future


def _to_query_request(job_config: Optional[job.QueryJobConfig]) -> Dict[str, Any]:
    """Transform from Job resource to QueryRequest resource.

    Most of the keys in job.configuration.query are in common with
    QueryRequest. If any configuration property is set that is not available in
    jobs.query, it will result in a server-side error.
    """
    request_body = {}
    job_config_resource = job_config.to_api_repr() if job_config else {}
    query_config_resource = job_config_resource.get("configuration", {}).get(
        "query", {}
    )

    request_body.update(query_config_resource)

    # These keys are top level in job resource and query resource.
    if "labels" in job_config_resource:
        request_body["labels"] = job_config_resource["labels"]
    if "dryRun" in job_config_resource:
        request_body["dryRun"] = job_config_resource["dryRun"]

    # Default to standard SQL.
    request_body.setdefault("useLegacySql", False)

    return request_body


def _to_query_job(
    client: "Client", query: str, query_response: Dict[str, Any]
) -> job.QueryJob:
    # TODO: check for errors?
    job_ref_resource = query_response["jobReference"]
    job_ref = job._JobReference._from_api_repr(job_ref_resource)
    query_job = job.QueryJob(job_ref, query, client=client)

    # Set errors if any were encountered.
    query_job._properties.setdefault("status", {})
    if "errors" in query_response:
        query_job._properties["status"]["errors"] = query_response["errors"]
        query_job._properties["status"]["errorResult"] = query_response["errors"][0]

    # Transform job state so that QueryJob doesn't try to restart the query.
    job_complete = query_response.get("jobComplete")
    if job_complete:
        query_job._properties["status"]["state"] = "DONE"
        # TODO: set first page of results if job is "complete"
    else:
        query_job._properties["status"]["state"] = "PENDING"

    return query_job


def query_jobs_query(
    client: "Client",
    query: str,
    job_config: Optional[job.QueryJobConfig],
    location: str,
    project: str,
    retry: retries.Retry,
    timeout: Optional[float],
    job_retry: retries.Retry,
):
    """Initiate a query using jobs.query.

    See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
    """
    path = f"/projects/{project}/queries"
    request_body = _to_query_request(job_config)

    if timeout is not None:
        # Subtract a buffer for context switching, network latency, etc.
        request_body["timeoutMs"] = max(0, int(1000 * (timeout - _TIMEOUT_BUFFER_SECS)))
    request_body["location"] = location
    request_body["query"] = query

    def do_query():
        request_body["requestId"] = make_job_id()
        span_attributes = {"path": path}
        api_response = client._call_api(
            retry,
            span_name="BigQuery.query",
            span_attributes=span_attributes,
            method="POST",
            path=path,
            data=request_body,
            timeout=timeout,
        )
        return _to_query_job(client, query, api_response)

    future = do_query()

    # The future might be in a failed state now, but if it's
    # unrecoverable, we'll find out when we ask for it's result, at which
    # point, we may retry.
    future._retry_do_query = do_query  # in case we have to retry later
    future._job_retry = job_retry

    return future
