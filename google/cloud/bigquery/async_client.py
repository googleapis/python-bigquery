from google.cloud.bigquery.client import *
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery import table
import asyncio

class AsyncClient(Client):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def query_and_wait(
        self,
        query,
        *,
        job_config: Optional[QueryJobConfig] = None,
        location: Optional[str] = None,
        project: Optional[str] = None,
        api_timeout: TimeoutType = DEFAULT_TIMEOUT,
        wait_timeout: TimeoutType = None,
        retry: retries.Retry = DEFAULT_RETRY,
        job_retry: retries.Retry = DEFAULT_JOB_RETRY,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
        ) -> RowIterator:

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        # if job_config is not None:
        #     self._verify_job_config_type(job_config, QueryJobConfig)

        # if job_config is not None:
        #     self._verify_job_config_type(job_config, QueryJobConfig)

        job_config = _job_helpers.job_config_with_defaults(
            job_config, self._default_query_job_config
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


async def async_query_and_wait(    
    client: "Client",
    query: str,
    *,
    job_config: Optional[job.QueryJobConfig],
    location: Optional[str],
    project: str,
    api_timeout: Optional[float] = None,
    wait_timeout: Optional[float] = None,
    retry: Optional[retries.Retry],
    job_retry: Optional[retries.Retry],
    page_size: Optional[int] = None,
    max_results: Optional[int] = None,
) -> table.RowIterator:
            
    # Some API parameters aren't supported by the jobs.query API. In these
    # cases, fallback to a jobs.insert call.
    if not _job_helpers._supported_by_jobs_query(job_config):
        return await async_wait_or_cancel(
            _job_helpers.query_jobs_insert(
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

    async def do_query():
        request_body["requestId"] = _job_helpers.make_job_id()
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
            response
        )
        page_token = query_results.page_token
        more_pages = page_token is not None

        if more_pages or not query_results.complete:
            # TODO(swast): Avoid a call to jobs.get in some cases (few
            # remaining pages) by waiting for the query to finish and calling
            # client._list_rows_from_query_results directly. Need to update
            # RowIterator to fetch destination table via the job ID if needed.
            return await async_wait_or_cancel(
                _job_helpers._to_query_job(client, query, job_config, response),
                api_timeout=api_timeout,
                wait_timeout=wait_timeout,
                retry=retry,
                page_size=page_size,
                max_results=max_results,
            )

        return table.RowIterator(
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
        return job_retry(do_query)()
    else:
        return await do_query()

async def async_wait_or_cancel(
    job: job.QueryJob,
    api_timeout: Optional[float],
    wait_timeout: Optional[float],
    retry: Optional[retries.Retry],
    page_size: Optional[int],
    max_results: Optional[int],
) -> table.RowIterator:
    try:
        return await job.result(
            page_size=page_size,
            max_results=max_results,
            retry=retry,
            timeout=wait_timeout,
        )
    except Exception:
        # Attempt to cancel the job since we can't return the results.
        try:
            job.cancel(retry=retry, timeout=api_timeout)
        except Exception:
            # Don't eat the original exception if cancel fails.
            pass
        raise