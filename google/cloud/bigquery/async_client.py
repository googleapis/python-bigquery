import sys
from google.cloud.bigquery.client import *
from google.cloud.bigquery.client import (
    _add_server_timeout_header,
    _extract_job_reference,
)
from google.cloud.bigquery.opentelemetry_tracing import async_create_span
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery.table import *
from google.cloud.bigquery.table import _table_arg_to_table_ref
from google.api_core.page_iterator import HTTPIterator
from google.cloud.bigquery.query import _QueryResults
from google.cloud.bigquery.retry import (
    DEFAULT_ASYNC_JOB_RETRY,
    DEFAULT_ASYNC_RETRY,
    DEFAULT_TIMEOUT,
)
from google.api_core import retry_async as retries

if sys.version_info >= (3, 9):
    import asyncio

    # import aiohttp
    # from google.auth.transport import _aiohttp_requests

# This code is experimental

_MIN_GET_QUERY_RESULTS_TIMEOUT = 120


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

    async def _get_query_results(  # make async
        self,
        job_id: str,
        retry: retries.AsyncRetry,
        project: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        location: Optional[str] = None,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> _QueryResults:
        extra_params: Dict[str, Any] = {"maxResults": 0}

        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                timeout = _MIN_GET_QUERY_RESULTS_TIMEOUT
            else:
                timeout = max(timeout, _MIN_GET_QUERY_RESULTS_TIMEOUT)

        if project is None:
            project = self._client.project

        if timeout_ms is not None:
            extra_params["timeoutMs"] = timeout_ms

        if location is None:
            location = self._client.location

        if location is not None:
            extra_params["location"] = location

        path = "/projects/{}/queries/{}".format(project, job_id)

        # This call is typically made in a polling loop that checks whether the
        # job is complete (from QueryJob.done(), called ultimately from
        # QueryJob.result()). So we don't need to poll here.
        span_attributes = {"path": path}
        resource = await self._call_api(
            retry,
            span_name="BigQuery.getQueryResults",
            span_attributes=span_attributes,
            method="GET",
            path=path,
            query_params=extra_params,
            timeout=timeout,
        )
        return _QueryResults.from_api_repr(resource)

    async def get_table(  # make async
        self,
        table: Union[Table, TableReference, TableListItem, str],
        retry: retries.AsyncRetry = DEFAULT_ASYNC_RETRY,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> Table:
        table_ref = _table_arg_to_table_ref(table, default_project=self._client.project)
        path = table_ref.path
        span_attributes = {"path": path}
        api_response = await self._call_api(
            retry,
            span_name="BigQuery.getTable",
            span_attributes=span_attributes,
            method="GET",
            path=path,
            timeout=timeout,
        )
        result = await asyncio.to_thread(Table.from_api_repr, api_response)
        return result

    async def list_partitions(  # make async
        self,
        table: Union[Table, TableReference, TableListItem, str],
        retry: retries.AsyncRetry = DEFAULT_ASYNC_RETRY,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> Sequence[str]:
        table = _table_arg_to_table_ref(table, default_project=self._client.project)
        meta_table = await self.get_table(
            TableReference(
                DatasetReference(table.project, table.dataset_id),
                "%s$__PARTITIONS_SUMMARY__" % table.table_id,
            ),
            retry=retry,
            timeout=timeout,
        )

        subset = [col for col in meta_table.schema if col.name == "partition_id"]
        return [
            row[0]
            for row in self._client.list_rows(
                meta_table, selected_fields=subset, retry=retry, timeout=timeout
            )
        ]

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

        # cloudcore,bigquery installed locally,
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
