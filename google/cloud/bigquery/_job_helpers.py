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

"""Helpers for interacting with the job REST APIs from the client.

For queries, there are three cases to consider:

1. jobs.insert: This always returns a job resource.
2. jobs.query, jobCreationMode=JOB_CREATION_REQUIRED:
   This sometimes can return the results inline, but always includes a job ID.
3. jobs.query, jobCreationMode=JOB_CREATION_OPTIONAL:
   This sometimes doesn't create a job at all, instead returning the results.
   For better debugging, a query ID is included in the response (not always a
   job ID).

Client.query() calls either (1) or (2), depending on what the user provides
for the api_method parameter. query() always returns a QueryJob object, which
can retry the query when the query job fails for a retriable reason.

Client.query_and_wait() calls (3). This returns a RowIterator that may wrap
local results from the response or may wrap a query job containing multiple
pages of results. Even though query_and_wait() waits for the job to complete,
we still need a separate job_retry object because there are different
predicates where it is safe to generate a new query ID.
"""

import copy
import functools
import os
import uuid
from typing import Any, Dict, TYPE_CHECKING, Optional

import google.api_core.exceptions as core_exceptions
from google.api_core import retry as retries

from google.cloud.bigquery import job
import google.cloud.bigquery.query
from google.cloud.bigquery import table

# Avoid circular imports
if TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud.bigquery.client import Client


# The purpose of _TIMEOUT_BUFFER_MILLIS is to allow the server-side timeout to
# happen before the client-side timeout. This is not strictly neccessary, as the
# client retries client-side timeouts, but the hope by making the server-side
# timeout slightly shorter is that it can save the server from some unncessary
# processing time.
#
# 250 milliseconds is chosen arbitrarily, though should be about the right
# order of magnitude for network latency and switching delays. It is about the
# amount of time for light to circumnavigate the world twice.
_TIMEOUT_BUFFER_MILLIS = 250


def make_job_id(job_id: Optional[str] = None, prefix: Optional[str] = None) -> str:
    """Construct an ID for a new job.

    Args:
        job_id: the user-provided job ID.
        prefix: the user-provided prefix for a job ID.

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
    job_config: Optional[job.QueryJobConfig],
    job_id: Optional[str],
    job_id_prefix: Optional[str],
    location: Optional[str],
    project: str,
    retry: retries.Retry,
    timeout: Optional[float],
    job_retry: retries.Retry,
) -> job.QueryJob:
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
                raise
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


def _to_query_request(
    job_config: Optional[job.QueryJobConfig] = None,
    *,
    query: str,
    location: Optional[str] = None,
    timeout: Optional[float] = None,
) -> Dict[str, Any]:
    """Transform from Job resource to QueryRequest resource.

    Most of the keys in job.configuration.query are in common with
    QueryRequest. If any configuration property is set that is not available in
    jobs.query, it will result in a server-side error.
    """
    request_body = {}
    job_config_resource = job_config.to_api_repr() if job_config else {}
    query_config_resource = job_config_resource.get("query", {})

    request_body.update(query_config_resource)

    # These keys are top level in job resource and query resource.
    if "labels" in job_config_resource:
        request_body["labels"] = job_config_resource["labels"]
    if "dryRun" in job_config_resource:
        request_body["dryRun"] = job_config_resource["dryRun"]

    # Default to standard SQL.
    request_body.setdefault("useLegacySql", False)

    # Since jobs.query can return results, ensure we use the lossless timestamp
    # format. See: https://github.com/googleapis/python-bigquery/issues/395
    request_body.setdefault("formatOptions", {})
    request_body["formatOptions"]["useInt64Timestamp"] = True  # type: ignore

    if timeout is not None:
        # Subtract a buffer for context switching, network latency, etc.
        request_body["timeoutMs"] = max(0, int(1000 * timeout) - _TIMEOUT_BUFFER_MILLIS)

    if location is not None:
        request_body["location"] = location

    request_body["query"] = query

    return request_body


def _to_query_job(
    client: "Client",
    query: str,
    request_config: Optional[job.QueryJobConfig],
    query_response: Dict[str, Any],
) -> job.QueryJob:
    job_ref_resource = query_response["jobReference"]
    job_ref = job._JobReference._from_api_repr(job_ref_resource)
    query_job = job.QueryJob(job_ref, query, client=client)
    query_job._properties.setdefault("configuration", {})

    # Not all relevant properties are in the jobs.query response. Populate some
    # expected properties based on the job configuration.
    if request_config is not None:
        query_job._properties["configuration"].update(request_config.to_api_repr())

    query_job._properties["configuration"].setdefault("query", {})
    query_job._properties["configuration"]["query"]["query"] = query
    query_job._properties["configuration"]["query"].setdefault("useLegacySql", False)

    query_job._properties.setdefault("statistics", {})
    query_job._properties["statistics"].setdefault("query", {})
    query_job._properties["statistics"]["query"]["cacheHit"] = query_response.get(
        "cacheHit"
    )
    query_job._properties["statistics"]["query"]["schema"] = query_response.get(
        "schema"
    )
    query_job._properties["statistics"]["query"][
        "totalBytesProcessed"
    ] = query_response.get("totalBytesProcessed")

    # Set errors if any were encountered.
    query_job._properties.setdefault("status", {})
    if "errors" in query_response:
        # Set errors but not errorResult. If there was an error that failed
        # the job, jobs.query behaves like jobs.getQueryResults and returns a
        # non-success HTTP status code.
        errors = query_response["errors"]
        query_job._properties["status"]["errors"] = errors

    # Transform job state so that QueryJob doesn't try to restart the query.
    job_complete = query_response.get("jobComplete")
    if job_complete:
        query_job._properties["status"]["state"] = "DONE"
        query_job._query_results = google.cloud.bigquery.query._QueryResults(
            query_response
        )
    else:
        query_job._properties["status"]["state"] = "PENDING"

    return query_job


def _to_query_path(project: str) -> str:
    return f"/projects/{project}/queries"


def query_jobs_query(
    client: "Client",
    query: str,
    job_config: Optional[job.QueryJobConfig],
    location: Optional[str],
    project: str,
    retry: retries.Retry,
    timeout: Optional[float],
    job_retry: retries.Retry,
) -> job.QueryJob:
    """Initiate a query using jobs.query with jobCreationMode=JOB_CREATION_REQUIRED.

    See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
    """
    path = _to_query_path(project)
    request_body = _to_query_request(
        query=query, job_config=job_config, location=location, timeout=timeout
    )

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
        return _to_query_job(client, query, job_config, api_response)

    future = do_query()

    # The future might be in a failed state now, but if it's
    # unrecoverable, we'll find out when we ask for it's result, at which
    # point, we may retry.
    future._retry_do_query = do_query  # in case we have to retry later
    future._job_retry = job_retry

    return future


def query_and_wait(
    client: "Client",
    query: str,
    job_config: Optional[job.QueryJobConfig],
    location: Optional[str],
    project: str,
    retry: Optional[retries.Retry],
    timeout: Optional[float],
    job_retry: Optional[retries.Retry],
    page_size: Optional[int] = None,
    max_results: Optional[int] = None,
) -> table.RowIterator:
    """Initiate a query using jobs.query and waits for results.

    While ``jobCreationMode=JOB_CREATION_OPTIONAL`` is in preview, use the
    default ``jobCreationMode`` unless the environment variable
    ``QUERY_PREVIEW_ENABLED=true``. After ``jobCreationMode`` is GA, this
    method will always use ``jobCreationMode=JOB_CREATION_OPTIONAL``.

    See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
    """
    path = _to_query_path(project)
    request_body = _to_query_request(
        query=query, job_config=job_config, location=location, timeout=timeout
    )

    if page_size is not None and max_results is not None:
        request_body["maxResults"] = min(page_size, max_results)
    elif page_size is not None or max_results is not None:
        request_body["maxResults"] = page_size or max_results

    if os.getenv("QUERY_PREVIEW_ENABLED", "").casefold() == "true":
        request_body["jobCreationMode"] = "JOB_CREATION_OPTIONAL"

    def do_query():
        request_body["requestId"] = make_job_id()
        span_attributes = {"path": path}

        # For easier testing, handle the retries ourselves.
        if retry is not None:
            response = retry(client._call_api)(
                retry=None,  # We're calling the retry decorator ourselves.
                span_name="BigQuery.query",
                span_attributes=span_attributes,
                method="POST",
                path=path,
                data=request_body,
                timeout=timeout,
            )
        else:
            response = client._call_api(
                retry=None,
                span_name="BigQuery.query",
                span_attributes=span_attributes,
                method="POST",
                path=path,
                data=request_body,
                timeout=timeout,
            )

        # Even if we run with JOB_CREATION_OPTIONAL, if there are more pages
        # to fetch, there will be a job ID for jobs.getQueryResults.
        query_results = google.cloud.bigquery.query._QueryResults.from_api_repr(
            response
        )
        page_token = query_results.page_token
        more_pages = page_token is not None

        if more_pages or not query_results.complete:
            # TODO(swast): Avoid a call to jobs.get in some cases (few
            # remaining pages) by waiting for the query to finish and calling
            # client._list_rows_from_query_results directly. Need to update
            # RowIterator to fetch destination table via the job ID if needed.
            return _to_query_job(client, query, job_config, response).result(
                retry=retry,
                timeout=timeout,
                page_size=page_size,
                max_results=max_results,
            )

        return table.RowIterator(
            client=client,
            api_request=functools.partial(client._call_api, retry, timeout=timeout),
            path=None,
            schema=query_results.schema,
            max_results=max_results,
            page_size=page_size,
            total_rows=query_results.total_rows,
            first_page_response=response,
            location=query_results.location,
            job_id=query_results.job_id,
            query_id=query_results.query_id,
            project=query_results.project,
        )

    if job_retry is not None:
        return job_retry(do_query)()
    else:
        return do_query()
