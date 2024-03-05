from google.cloud.bigquery.client import *
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery import table
from google.cloud.bigquery.retry import (
    DEFAULT_ASYNC_JOB_RETRY,
    DEFAULT_ASYNC_RETRY,
    DEFAULT_TIMEOUT,
)
from google.api_core import retry_async as retries
import asyncio
import google.auth.transport._aiohttp_requests


class AsyncClient():  
    def __init__(self, *args, **kwargs):
        self._client = Client(*args, **kwargs)


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

        # if job_config is not None:
        #     self._client._verify_job_config_type(job_config, QueryJobConfig)

        # if job_config is not None:
        #     self._client._verify_job_config_type(job_config, QueryJobConfig)

        job_config = _job_helpers.job_config_with_defaults(
            job_config, self._client._default_query_job_config
        )

        return await async_query_and_wait(
            self._client,
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


async def async_query_and_wait(    
    client: "Client",
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
) -> table.RowIterator:
            
    # Some API parameters aren't supported by the jobs.query API. In these
    # cases, fallback to a jobs.insert call.
    if not _job_helpers._supported_by_jobs_query(job_config):
        return await async_wait_or_cancel(
            asyncio.to_thread(_job_helpers.query_jobs_insert( # throw in a background thread
                client=client,
                query=query,
                job_id=None,
                job_id_prefix=None,
                job_config=job_config,
                location=location,
                project=project,
                retry=retry,
                timeout=api_timeout,
                job_retry=job_retry,
            )),
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

    # For easier testing, handle the retries ourselves.
    if retry is not None:
        response = retry(client._call_api)( # ASYNCHRONOUS HTTP CALLS aiohttp (optional of google-auth)
            retry=None,  # We're calling the retry decorator ourselves, async_retries
            span_name="BigQuery.query",
            span_attributes=span_attributes,
            method="POST",
            path=path,
            data=request_body,
            timeout=api_timeout,
        )
    else:
        response = client._call_api(
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
    query_results = google.cloud.bigquery.query._QueryResults.from_api_repr(
        await response
    )
    page_token = query_results.page_token
    more_pages = page_token is not None

    if more_pages or not query_results.complete:
        # TODO(swast): Avoid a call to jobs.get in some cases (few
        # remaining pages) by waiting for the query to finish and calling
        # client._list_rows_from_query_results directly. Need to update
        # RowIterator to fetch destination table via the job ID if needed.
        result = await async_wait_or_cancel(
            _job_helpers._to_query_job(client, query, job_config, response),
            api_timeout=api_timeout,
            wait_timeout=wait_timeout,
            retry=retry,
            page_size=page_size,
            max_results=max_results,
        )

    result = table.RowIterator( # async of RowIterator? async version without all the pandas stuff
        client=client,
        api_request=functools.partial(client._call_api, retry, timeout=api_timeout),
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
        return job_retry(result) # AsyncRetries, new default objects, default_job_retry_async, default_retry_async
    else:
        return result

async def async_wait_or_cancel(
    job: job.QueryJob,
    api_timeout: Optional[float],
    wait_timeout: Optional[float],
    retry: Optional[retries.AsyncRetry],
    page_size: Optional[int],
    max_results: Optional[int],
) -> table.RowIterator:
    try:
        return asyncio.to_thread(job.result( # run in a background thread
            page_size=page_size,
            max_results=max_results,
            retry=retry,
            timeout=wait_timeout,
        ))
    except Exception:
        # Attempt to cancel the job since we can't return the results.
        try:
            job.cancel(retry=retry, timeout=api_timeout)
        except Exception:
            # Don't eat the original exception if cancel fails.
            pass
        raise