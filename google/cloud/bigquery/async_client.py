from google.cloud.bigquery.client import *
from google.cloud.bigquery.client import (
    _add_server_timeout_header,
    _extract_job_reference,
)
from google.cloud.bigquery.opentelemetry_tracing import async_create_span
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery.table import *
from google.api_core.page_iterator import HTTPIterator
from google.cloud.bigquery.retry import (
    DEFAULT_ASYNC_JOB_RETRY,
    DEFAULT_ASYNC_RETRY,
    DEFAULT_TIMEOUT,
)
from google.api_core import retry_async as retries
import asyncio
from google.auth.transport import _aiohttp_requests

# This code is experimental


class AsyncClient:
    def __init__(self, *args, **kwargs):
        self._client = Client(*args, **kwargs)

    async def get_job(
        self,
        job_id: Union[str, job.LoadJob, job.CopyJob, job.ExtractJob, job.QueryJob],
        project: Optional[str] = None,
        location: Optional[str] = None,
        retry: retries.AsyncRetry = DEFAULT_ASYNC_RETRY,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> Union[job.LoadJob, job.CopyJob, job.ExtractJob, job.QueryJob, job.UnknownJob]:
        extra_params = {"projection": "full"}

        project, location, job_id = _extract_job_reference(
            job_id, project=project, location=location
        )

        if project is None:
            project = self._client.project

        if location is None:
            location = self._client.location

        if location is not None:
            extra_params["location"] = location

        path = "/projects/{}/jobs/{}".format(project, job_id)

        span_attributes = {"path": path, "job_id": job_id, "location": location}

        resource = await self._call_api(
            retry,
            span_name="BigQuery.getJob",
            span_attributes=span_attributes,
            method="GET",
            path=path,
            query_params=extra_params,
            timeout=timeout,
        )

        return await asyncio.to_thread(self._client.job_from_resource(await resource))

    async def query_and_wait(
        self,
        query,
        *,
        job_config: Optional[QueryJobConfig] = None,
        location: Optional[str] = None,
        project: Optional[str] = None,
        api_timeout: TimeoutType = DEFAULT_TIMEOUT,
        wait_timeout: TimeoutType = None,
        retry: retries.AsyncRetry = DEFAULT_ASYNC_RETRY,
        job_retry: retries.AsyncRetry = DEFAULT_ASYNC_JOB_RETRY,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
    ) -> RowIterator:
        if project is None:
            project = self._client.project

        if location is None:
            location = self._client.location

        # for some reason these cannot find the function call
        # if job_config is not None:
        #     self._client._verify_job_config_type(job_config, QueryJobConfig)

        # if job_config is not None:
        #     self._client._verify_job_config_type(job_config, QueryJobConfig)

        job_config = _job_helpers.job_config_with_defaults(
            job_config, self._client._default_query_job_config
        )

        return await async_query_and_wait(
            self,
            query,
            job_config=job_config,
            location=location,
            project=project,
            api_timeout=api_timeout,
            wait_timeout=wait_timeout,
            retry=retry,
            job_retry=job_retry,
            page_size=page_size,
            max_results=max_results,
        )

    async def _call_api(
        self,
        retry: Optional[retries.AsyncRetry] = None,
        span_name: Optional[str] = None,
        span_attributes: Optional[Dict] = None,
        job_ref=None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        kwargs = _add_server_timeout_header(headers, kwargs)

        # Prepare the asynchronous request function
        # async with _aiohttp_requests.Request(**kwargs) as response:
        #     response.raise_for_status()
        #     response = await response.json()  # or response.text()

        async_call = functools.partial(self._client._connection.api_request, **kwargs)

        if retry:
            async_call = retry(async_call)

        if span_name is not None:
            async with async_create_span(
                name=span_name,
                attributes=span_attributes,
                client=self._client,
                job_ref=job_ref,
            ):
                return async_call()  # Await the asynchronous call

        return async_call()  # Await the asynchronous call


async def async_query_and_wait(
    client: "AsyncClient",
    query: str,
    *,
    job_config: Optional[job.QueryJobConfig],
    location: Optional[str],
    project: str,
    api_timeout: Optional[float] = None,
    wait_timeout: Optional[float] = None,
    retry: Optional[retries.AsyncRetry],
    job_retry: Optional[retries.AsyncRetry],
    page_size: Optional[int] = None,
    max_results: Optional[int] = None,
) -> RowIterator:
    if not _job_helpers._supported_by_jobs_query(job_config):
        return await async_wait_or_cancel(
            asyncio.to_thread(
                _job_helpers.query_jobs_insert(
                    client=client._client,
                    query=query,
                    job_id=None,
                    job_id_prefix=None,
                    job_config=job_config,
                    location=location,
                    project=project,
                    retry=retry,
                    timeout=api_timeout,
                    job_retry=job_retry,
                )
            ),
            api_timeout=api_timeout,
            wait_timeout=wait_timeout,
            retry=retry,
            page_size=page_size,
            max_results=max_results,
        )

    path = _job_helpers._to_query_path(project)
    request_body = _job_helpers._to_query_request(
        query=query, job_config=job_config, location=location, timeout=api_timeout
    )

    if page_size is not None and max_results is not None:
        request_body["maxResults"] = min(page_size, max_results)
    elif page_size is not None or max_results is not None:
        request_body["maxResults"] = page_size or max_results

    if os.getenv("QUERY_PREVIEW_ENABLED", "").casefold() == "true":
        request_body["jobCreationMode"] = "JOB_CREATION_OPTIONAL"

    request_body["requestId"] = _job_helpers.make_job_id()
    span_attributes = {"path": path}

    if retry is not None:
        response = await client._call_api(  # ASYNCHRONOUS HTTP CALLS aiohttp (optional of google-auth), add back retry()
            retry=None,  # We're calling the retry decorator ourselves, async_retries, need to implement after making HTTP calls async
            span_name="BigQuery.query",
            span_attributes=span_attributes,
            method="POST",
            path=path,
            data=request_body,
            timeout=api_timeout,
        )

    else:
        response = await client._call_api(
            retry=None,
            span_name="BigQuery.query",
            span_attributes=span_attributes,
            method="POST",
            path=path,
            data=request_body,
            timeout=api_timeout,
        )

    # Even if we run with JOB_CREATION_OPTIONAL, if there are more pages
    # to fetch, there will be a job ID for jobs.getQueryResults.
    query_results = google.cloud.bigquery.query._QueryResults.from_api_repr(response)
    page_token = query_results.page_token
    more_pages = page_token is not None

    if more_pages or not query_results.complete:
        # TODO(swast): Avoid a call to jobs.get in some cases (few
        # remaining pages) by waiting for the query to finish and calling
        # client._list_rows_from_query_results directly. Need to update
        # RowIterator to fetch destination table via the job ID if needed.
        result = await async_wait_or_cancel(
            asyncio.to_thread(
                _job_helpers._to_query_job(client._client, query, job_config, response),
                api_timeout=api_timeout,
                wait_timeout=wait_timeout,
                retry=retry,
                page_size=page_size,
                max_results=max_results,
            )
        )

    def api_request(*args, **kwargs):
        return client._call_api(
            span_name="BigQuery.query",
            span_attributes=span_attributes,
            *args,
            timeout=api_timeout,
            **kwargs,
        )

    result = AsyncRowIterator(  # async of RowIterator? async version without all the pandas stuff
        client=client._client,
        api_request=api_request,
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
        num_dml_affected_rows=query_results.num_dml_affected_rows,
    )

    if job_retry is not None:
        return job_retry(result)
    else:
        return result


async def async_wait_or_cancel(
    job: job.QueryJob,
    api_timeout: Optional[float],
    wait_timeout: Optional[float],
    retry: Optional[retries.AsyncRetry],
    page_size: Optional[int],
    max_results: Optional[int],
) -> RowIterator:
    try:
        return asyncio.to_thread(
            job.result(
                page_size=page_size,
                max_results=max_results,
                retry=retry,
                timeout=wait_timeout,
            )
        )
    except Exception:
        # Attempt to cancel the job since we can't return the results.
        try:
            job.cancel(retry=retry, timeout=api_timeout)
        except Exception:
            # Don't eat the original exception if cancel fails.
            pass
        raise


class AsyncRowIterator(RowIterator):
    async def _get_next_page_response(self):
        """Asynchronous version of fetching the next response page."""
        if self._first_page_response:
            rows = self._first_page_response.get(self._items_key, [])[
                : self.max_results
            ]
            response = {
                self._items_key: rows,
            }
            if self._next_token in self._first_page_response:
                response[self._next_token] = self._first_page_response[self._next_token]

            self._first_page_response = None
            return response

        params = self._get_query_params()
        if self._page_size is not None:
            if self.page_number and "startIndex" in params:
                del params["startIndex"]
            params["maxResults"] = self._page_size
        return await self.api_request(
            method=self._HTTP_METHOD, path=self.path, query_params=params
        )
