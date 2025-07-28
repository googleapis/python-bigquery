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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.bigquery_v2.types import data_format_options
from google.cloud.bigquery_v2.types import dataset_reference
from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import error
from google.cloud.bigquery_v2.types import job_config
from google.cloud.bigquery_v2.types import (
    job_creation_reason as gcb_job_creation_reason,
)
from google.cloud.bigquery_v2.types import job_reference as gcb_job_reference
from google.cloud.bigquery_v2.types import job_stats
from google.cloud.bigquery_v2.types import job_status
from google.cloud.bigquery_v2.types import query_parameter
from google.cloud.bigquery_v2.types import session_info as gcb_session_info
from google.cloud.bigquery_v2.types import table_schema
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "Job",
        "CancelJobRequest",
        "JobCancelResponse",
        "GetJobRequest",
        "InsertJobRequest",
        "DeleteJobRequest",
        "ListJobsRequest",
        "ListFormatJob",
        "JobList",
        "GetQueryResultsRequest",
        "GetQueryResultsResponse",
        "PostQueryRequest",
        "QueryRequest",
        "QueryResponse",
    },
)


class Job(proto.Message):
    r"""

    Attributes:
        kind (str):
            Output only. The type of the resource.
        etag (str):
            Output only. A hash of this resource.
        id (str):
            Output only. Opaque ID field of the job.
        self_link (str):
            Output only. A URL that can be used to access
            the resource again.
        user_email (str):
            Output only. Email address of the user who
            ran the job.
        configuration (google.cloud.bigquery_v2.types.JobConfiguration):
            Required. Describes the job configuration.
        job_reference (google.cloud.bigquery_v2.types.JobReference):
            Optional. Reference describing the
            unique-per-user name of the job.
        statistics (google.cloud.bigquery_v2.types.JobStatistics):
            Output only. Information about the job,
            including starting time and ending time of the
            job.
        status (google.cloud.bigquery_v2.types.JobStatus):
            Output only. The status of this job. Examine
            this value when polling an asynchronous job to
            see if the job is complete.
        principal_subject (str):
            Output only. [Full-projection-only] String representation of
            identity of requesting party. Populated for both first- and
            third-party identities. Only present for APIs that support
            third-party identities.
        job_creation_reason (google.cloud.bigquery_v2.types.JobCreationReason):
            Output only. The reason why a Job was
            created.
    """

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )
    id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    self_link: str = proto.Field(
        proto.STRING,
        number=4,
    )
    user_email: str = proto.Field(
        proto.STRING,
        number=5,
    )
    configuration: job_config.JobConfiguration = proto.Field(
        proto.MESSAGE,
        number=6,
        message=job_config.JobConfiguration,
    )
    job_reference: gcb_job_reference.JobReference = proto.Field(
        proto.MESSAGE,
        number=7,
        message=gcb_job_reference.JobReference,
    )
    statistics: job_stats.JobStatistics = proto.Field(
        proto.MESSAGE,
        number=8,
        message=job_stats.JobStatistics,
    )
    status: job_status.JobStatus = proto.Field(
        proto.MESSAGE,
        number=9,
        message=job_status.JobStatus,
    )
    principal_subject: str = proto.Field(
        proto.STRING,
        number=13,
    )
    job_creation_reason: gcb_job_creation_reason.JobCreationReason = proto.Field(
        proto.MESSAGE,
        number=14,
        message=gcb_job_creation_reason.JobCreationReason,
    )


class CancelJobRequest(proto.Message):
    r"""Describes format of a jobs cancellation request.

    Attributes:
        project_id (str):
            Required. Project ID of the job to cancel
        job_id (str):
            Required. Job ID of the job to cancel
        location (str):
            The geographic location of the job. You must `specify the
            location <https://cloud.google.com/bigquery/docs/locations#specify_locations>`__
            to run the job for the following scenarios:

            -  If the location to run a job is not in the ``us`` or the
               ``eu`` multi-regional location
            -  If the job's location is in a single region (for example,
               ``us-central1``)
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    location: str = proto.Field(
        proto.STRING,
        number=3,
    )


class JobCancelResponse(proto.Message):
    r"""Describes format of a jobs cancellation response.

    Attributes:
        kind (str):
            The resource type of the response.
        job (google.cloud.bigquery_v2.types.Job):
            The final state of the job.
    """

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job: "Job" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Job",
    )


class GetJobRequest(proto.Message):
    r"""Describes format of a jobs get request.

    Attributes:
        project_id (str):
            Required. Project ID of the requested job.
        job_id (str):
            Required. Job ID of the requested job.
        location (str):
            The geographic location of the job. You must specify the
            location to run the job for the following scenarios:

            -  If the location to run a job is not in the ``us`` or the
               ``eu`` multi-regional location
            -  If the job's location is in a single region (for example,
               ``us-central1``)

            For more information, see how to `specify
            locations <https://cloud.google.com/bigquery/docs/locations#specify_locations>`__.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    location: str = proto.Field(
        proto.STRING,
        number=3,
    )


class InsertJobRequest(proto.Message):
    r"""Describes format of a job insertion request.

    Attributes:
        project_id (str):
            Project ID of project that will be billed for
            the job.
        job (google.cloud.bigquery_v2.types.Job):
            Jobs resource to insert.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job: "Job" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Job",
    )


class DeleteJobRequest(proto.Message):
    r"""Describes the format of a jobs deletion request.

    Attributes:
        project_id (str):
            Required. Project ID of the job for which
            metadata is to be deleted.
        job_id (str):
            Required. Job ID of the job for which
            metadata is to be deleted. If this is a parent
            job which has child jobs, the metadata from all
            child jobs will be deleted as well. Direct
            deletion of the metadata of child jobs is not
            allowed.
        location (str):
            The geographic location of the job. Required.

            For more information, see how to `specify
            locations <https://cloud.google.com/bigquery/docs/locations#specify_locations>`__.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    location: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListJobsRequest(proto.Message):
    r"""Describes the format of the list jobs request.

    Attributes:
        project_id (str):
            Project ID of the jobs to list.
        all_users (bool):
            Whether to display jobs owned by all users in
            the project. Default False.
        max_results (google.protobuf.wrappers_pb2.Int32Value):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        min_creation_time (int):
            Min value for job creation time, in
            milliseconds since the POSIX epoch. If set, only
            jobs created after or at this timestamp are
            returned.
        max_creation_time (google.protobuf.wrappers_pb2.UInt64Value):
            Max value for job creation time, in
            milliseconds since the POSIX epoch. If set, only
            jobs created before or at this timestamp are
            returned.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results.
        projection (google.cloud.bigquery_v2.types.ListJobsRequest.Projection):
            Restrict information returned to a set of
            selected fields
        state_filter (MutableSequence[google.cloud.bigquery_v2.types.ListJobsRequest.StateFilter]):
            Filter for job state
        parent_job_id (str):
            If set, show only child jobs of the specified
            parent.  Otherwise, show all top-level jobs.
    """

    class Projection(proto.Enum):
        r"""Projection is used to control what job information is
        returned.

        Values:
            minimal (0):
                Does not include the job configuration
            MINIMAL (0):
                Does not include the job configuration
            full (1):
                Includes all job data
            FULL (1):
                Includes all job data
        """
        _pb_options = {"allow_alias": True}
        minimal = 0
        MINIMAL = 0
        full = 1
        FULL = 1

    class StateFilter(proto.Enum):
        r"""StateFilter allows filtration by job execution state.

        Values:
            done (0):
                Finished jobs
            DONE (0):
                Finished jobs
            pending (1):
                Pending jobs
            PENDING (1):
                Pending jobs
            running (2):
                Running jobs
            RUNNING (2):
                Running jobs.
        """
        _pb_options = {"allow_alias": True}
        done = 0
        DONE = 0
        pending = 1
        PENDING = 1
        running = 2
        RUNNING = 2

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    all_users: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    max_results: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.Int32Value,
    )
    min_creation_time: int = proto.Field(
        proto.UINT64,
        number=4,
    )
    max_creation_time: wrappers_pb2.UInt64Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.UInt64Value,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )
    projection: Projection = proto.Field(
        proto.ENUM,
        number=7,
        enum=Projection,
    )
    state_filter: MutableSequence[StateFilter] = proto.RepeatedField(
        proto.ENUM,
        number=8,
        enum=StateFilter,
    )
    parent_job_id: str = proto.Field(
        proto.STRING,
        number=9,
    )


class ListFormatJob(proto.Message):
    r"""ListFormatJob is a partial projection of job information
    returned as part of a jobs.list response.

    Attributes:
        id (str):
            Unique opaque ID of the job.
        kind (str):
            The resource type.
        job_reference (google.cloud.bigquery_v2.types.JobReference):
            Unique opaque ID of the job.
        state (str):
            Running state of the job. When the state is
            DONE, errorResult can be checked to determine
            whether the job succeeded or failed.
        error_result (google.cloud.bigquery_v2.types.ErrorProto):
            A result object that will be present only if
            the job has failed.
        statistics (google.cloud.bigquery_v2.types.JobStatistics):
            Output only. Information about the job,
            including starting time and ending time of the
            job.
        configuration (google.cloud.bigquery_v2.types.JobConfiguration):
            Required. Describes the job configuration.
        status (google.cloud.bigquery_v2.types.JobStatus):
            [Full-projection-only] Describes the status of this job.
        user_email (str):
            [Full-projection-only] Email address of the user who ran the
            job.
        principal_subject (str):
            [Full-projection-only] String representation of identity of
            requesting party. Populated for both first- and third-party
            identities. Only present for APIs that support third-party
            identities.
    """

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    kind: str = proto.Field(
        proto.STRING,
        number=2,
    )
    job_reference: gcb_job_reference.JobReference = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcb_job_reference.JobReference,
    )
    state: str = proto.Field(
        proto.STRING,
        number=4,
    )
    error_result: error.ErrorProto = proto.Field(
        proto.MESSAGE,
        number=5,
        message=error.ErrorProto,
    )
    statistics: job_stats.JobStatistics = proto.Field(
        proto.MESSAGE,
        number=6,
        message=job_stats.JobStatistics,
    )
    configuration: job_config.JobConfiguration = proto.Field(
        proto.MESSAGE,
        number=7,
        message=job_config.JobConfiguration,
    )
    status: job_status.JobStatus = proto.Field(
        proto.MESSAGE,
        number=8,
        message=job_status.JobStatus,
    )
    user_email: str = proto.Field(
        proto.STRING,
        number=9,
    )
    principal_subject: str = proto.Field(
        proto.STRING,
        number=10,
    )


class JobList(proto.Message):
    r"""JobList is the response format for a jobs.list call.

    Attributes:
        etag (str):
            A hash of this page of results.
        kind (str):
            The resource type of the response.
        next_page_token (str):
            A token to request the next page of results.
        jobs (MutableSequence[google.cloud.bigquery_v2.types.ListFormatJob]):
            List of jobs that were requested.
        unreachable (MutableSequence[str]):
            A list of skipped locations that were
            unreachable. For more information about BigQuery
            locations, see:

            https://cloud.google.com/bigquery/docs/locations.
            Example: "europe-west5".
    """

    @property
    def raw_page(self):
        return self

    etag: str = proto.Field(
        proto.STRING,
        number=1,
    )
    kind: str = proto.Field(
        proto.STRING,
        number=2,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    jobs: MutableSequence["ListFormatJob"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="ListFormatJob",
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class GetQueryResultsRequest(proto.Message):
    r"""Request object of GetQueryResults.

    Attributes:
        project_id (str):
            Required. Project ID of the query job.
        job_id (str):
            Required. Job ID of the query job.
        start_index (google.protobuf.wrappers_pb2.UInt64Value):
            Zero-based index of the starting row.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results.
        max_results (google.protobuf.wrappers_pb2.UInt32Value):
            Maximum number of results to read.
        timeout_ms (google.protobuf.wrappers_pb2.UInt32Value):
            Optional: Specifies the maximum amount of
            time, in milliseconds, that the client is
            willing to wait for the query to complete. By
            default, this limit is 10 seconds (10,000
            milliseconds). If the query is complete, the
            jobComplete field in the response is true. If
            the query has not yet completed, jobComplete is
            false.

            You can request a longer timeout period in the
            timeoutMs field.  However, the call is not
            guaranteed to wait for the specified timeout; it
            typically returns after around 200 seconds
            (200,000 milliseconds), even if the query is not
            complete.

            If jobComplete is false, you can continue to
            wait for the query to complete by calling the
            getQueryResults method until the jobComplete
            field in the getQueryResults response is true.
        location (str):
            The geographic location of the job. You must specify the
            location to run the job for the following scenarios:

            -  If the location to run a job is not in the ``us`` or the
               ``eu`` multi-regional location
            -  If the job's location is in a single region (for example,
               ``us-central1``)

            For more information, see how to `specify
            locations <https://cloud.google.com/bigquery/docs/locations#specify_locations>`__.
        format_options (google.cloud.bigquery_v2.types.DataFormatOptions):
            Optional. Output format adjustments.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    start_index: wrappers_pb2.UInt64Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.UInt64Value,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )
    max_results: wrappers_pb2.UInt32Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.UInt32Value,
    )
    timeout_ms: wrappers_pb2.UInt32Value = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.UInt32Value,
    )
    location: str = proto.Field(
        proto.STRING,
        number=7,
    )
    format_options: data_format_options.DataFormatOptions = proto.Field(
        proto.MESSAGE,
        number=8,
        message=data_format_options.DataFormatOptions,
    )


class GetQueryResultsResponse(proto.Message):
    r"""Response object of GetQueryResults.

    Attributes:
        kind (str):
            The resource type of the response.
        etag (str):
            A hash of this response.
        schema (google.cloud.bigquery_v2.types.TableSchema):
            The schema of the results. Present only when
            the query completes successfully.
        job_reference (google.cloud.bigquery_v2.types.JobReference):
            Reference to the BigQuery Job that was
            created to run the query. This field will be
            present even if the original request timed out,
            in which case GetQueryResults can be used to
            read the results once the query has completed.
            Since this API only returns the first page of
            results, subsequent pages can be fetched via the
            same mechanism (GetQueryResults).
        total_rows (google.protobuf.wrappers_pb2.UInt64Value):
            The total number of rows in the complete
            query result set, which can be more than the
            number of rows in this single page of results.
            Present only when the query completes
            successfully.
        page_token (str):
            A token used for paging results.  When this
            token is non-empty, it indicates additional
            results are available.
        rows (MutableSequence[google.protobuf.struct_pb2.Struct]):
            An object with as many results as can be
            contained within the maximum permitted reply
            size. To get any additional rows, you can call
            GetQueryResults and specify the jobReference
            returned above. Present only when the query
            completes successfully.

            The REST-based representation of this data
            leverages a series of JSON f,v objects for
            indicating fields and values.
        total_bytes_processed (google.protobuf.wrappers_pb2.Int64Value):
            The total number of bytes processed for this
            query.
        job_complete (google.protobuf.wrappers_pb2.BoolValue):
            Whether the query has completed or not. If
            rows or totalRows are present, this will always
            be true. If this is false, totalRows will not be
            available.
        errors (MutableSequence[google.cloud.bigquery_v2.types.ErrorProto]):
            Output only. The first errors or warnings encountered during
            the running of the job. The final message includes the
            number of errors that caused the process to stop. Errors
            here do not necessarily mean that the job has completed or
            was unsuccessful. For more information about error messages,
            see `Error
            messages <https://cloud.google.com/bigquery/docs/error-messages>`__.
        cache_hit (google.protobuf.wrappers_pb2.BoolValue):
            Whether the query result was fetched from the
            query cache.
        num_dml_affected_rows (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of rows affected by a
            DML statement. Present only for DML statements
            INSERT, UPDATE or DELETE.
    """

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )
    schema: table_schema.TableSchema = proto.Field(
        proto.MESSAGE,
        number=3,
        message=table_schema.TableSchema,
    )
    job_reference: gcb_job_reference.JobReference = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gcb_job_reference.JobReference,
    )
    total_rows: wrappers_pb2.UInt64Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.UInt64Value,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )
    rows: MutableSequence[struct_pb2.Struct] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=struct_pb2.Struct,
    )
    total_bytes_processed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=8,
        message=wrappers_pb2.Int64Value,
    )
    job_complete: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=9,
        message=wrappers_pb2.BoolValue,
    )
    errors: MutableSequence[error.ErrorProto] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=error.ErrorProto,
    )
    cache_hit: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=11,
        message=wrappers_pb2.BoolValue,
    )
    num_dml_affected_rows: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=12,
        message=wrappers_pb2.Int64Value,
    )


class PostQueryRequest(proto.Message):
    r"""Request format for the query request.

    Attributes:
        project_id (str):
            Required. Project ID of the query request.
        query_request (google.cloud.bigquery_v2.types.QueryRequest):
            The query request body.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query_request: "QueryRequest" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="QueryRequest",
    )


class QueryRequest(proto.Message):
    r"""Describes the format of the jobs.query request.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        kind (str):
            The resource type of the request.
        query (str):
            Required. A query string to execute, using
            Google Standard SQL or legacy SQL syntax.
            Example: "SELECT COUNT(f1) FROM
            myProjectId.myDatasetId.myTableId".
        max_results (google.protobuf.wrappers_pb2.UInt32Value):
            Optional. The maximum number of rows of data
            to return per page of results. Setting this flag
            to a small value such as 1000 and then paging
            through results might improve reliability when
            the query result set is large. In addition to
            this limit, responses are also limited to 10 MB.
            By default, there is no maximum row count, and
            only the byte limit applies.
        default_dataset (google.cloud.bigquery_v2.types.DatasetReference):
            Optional. Specifies the default datasetId and
            projectId to assume for any unqualified table
            names in the query. If not set, all table names
            in the query string must be qualified in the
            format 'datasetId.tableId'.
        timeout_ms (google.protobuf.wrappers_pb2.UInt32Value):
            Optional. Optional: Specifies the maximum
            amount of time, in milliseconds, that the client
            is willing to wait for the query to complete. By
            default, this limit is 10 seconds (10,000
            milliseconds). If the query is complete, the
            jobComplete field in the response is true. If
            the query has not yet completed, jobComplete is
            false.

            You can request a longer timeout period in the
            timeoutMs field.  However, the call is not
            guaranteed to wait for the specified timeout; it
            typically returns after around 200 seconds
            (200,000 milliseconds), even if the query is not
            complete.

            If jobComplete is false, you can continue to
            wait for the query to complete by calling the
            getQueryResults method until the jobComplete
            field in the getQueryResults response is true.
        job_timeout_ms (int):
            Optional. Job timeout in milliseconds. If
            this time limit is exceeded, BigQuery will
            attempt to stop a longer job, but may not always
            succeed in canceling it before the job
            completes. For example, a job that takes more
            than 60 seconds to complete has a better chance
            of being stopped than a job that takes 10
            seconds to complete. This timeout applies to the
            query even if a job does not need to be created.

            This field is a member of `oneof`_ ``_job_timeout_ms``.
        destination_encryption_configuration (google.cloud.bigquery_v2.types.EncryptionConfiguration):
            Optional. Custom encryption configuration
            (e.g., Cloud KMS keys)
        dry_run (bool):
            Optional. If set to true, BigQuery doesn't
            run the job. Instead, if the query is valid,
            BigQuery returns statistics about the job such
            as how many bytes would be processed. If the
            query is invalid, an error returns. The default
            value is false.
        use_query_cache (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Whether to look for the result in
            the query cache. The query cache is a
            best-effort cache that will be flushed whenever
            tables in the query are modified. The default
            value is true.
        use_legacy_sql (google.protobuf.wrappers_pb2.BoolValue):
            Specifies whether to use BigQuery's legacy
            SQL dialect for this query. The default value is
            true. If set to false, the query will use
            BigQuery's GoogleSQL:
            https://cloud.google.com/bigquery/sql-reference/
            When useLegacySql is set to false, the value of
            flattenResults is ignored; query will be run as
            if flattenResults is false.
        parameter_mode (str):
            GoogleSQL only. Set to POSITIONAL to use
            positional (?) query parameters or to NAMED to
            use named (@myparam) query parameters in this
            query.
        query_parameters (MutableSequence[google.cloud.bigquery_v2.types.QueryParameter]):
            Query parameters for GoogleSQL queries.
        location (str):
            The geographic location where the job should run. For more
            information, see how to `specify
            locations <https://cloud.google.com/bigquery/docs/locations#specify_locations>`__.
        format_options (google.cloud.bigquery_v2.types.DataFormatOptions):
            Optional. Output format adjustments.
        connection_properties (MutableSequence[google.cloud.bigquery_v2.types.ConnectionProperty]):
            Optional. Connection properties which can
            modify the query behavior.
        labels (MutableMapping[str, str]):
            Optional. The labels associated with this
            query. Labels can be used to organize and group
            query jobs. Label keys and values can be no
            longer than 63 characters, can only contain
            lowercase letters, numeric characters,
            underscores and dashes. International characters
            are allowed. Label keys must start with a letter
            and each label in the list must have a different
            key.
        maximum_bytes_billed (google.protobuf.wrappers_pb2.Int64Value):
            Optional. Limits the bytes billed for this
            query. Queries with bytes billed above this
            limit will fail (without incurring a charge). If
            unspecified, the project default is used.
        request_id (str):
            Optional. A unique user provided identifier to ensure
            idempotent behavior for queries. Note that this is different
            from the job_id. It has the following properties:

            1. It is case-sensitive, limited to up to 36 ASCII
               characters. A UUID is recommended.

            2. Read only queries can ignore this token since they are
               nullipotent by definition.

            3. For the purposes of idempotency ensured by the
               request_id, a request is considered duplicate of another
               only if they have the same request_id and are actually
               duplicates. When determining whether a request is a
               duplicate of another request, all parameters in the
               request that may affect the result are considered. For
               example, query, connection_properties, query_parameters,
               use_legacy_sql are parameters that affect the result and
               are considered when determining whether a request is a
               duplicate, but properties like timeout_ms don't affect
               the result and are thus not considered. Dry run query
               requests are never considered duplicate of another
               request.

            4. When a duplicate mutating query request is detected, it
               returns: a. the results of the mutation if it completes
               successfully within the timeout. b. the running operation
               if it is still in progress at the end of the timeout.

            5. Its lifetime is limited to 15 minutes. In other words, if
               two requests are sent with the same request_id, but more
               than 15 minutes apart, idempotency is not guaranteed.
        create_session (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If true, creates a new session using a randomly
            generated session_id. If false, runs query with an existing
            session_id passed in ConnectionProperty, otherwise runs
            query in non-session mode.

            The session location will be set to QueryRequest.location if
            it is present, otherwise it's set to the default location
            based on existing routing logic.
        job_creation_mode (google.cloud.bigquery_v2.types.QueryRequest.JobCreationMode):
            Optional. If not set, jobs are always
            required.
            If set, the query request will follow the
            behavior described JobCreationMode.
        reservation (str):
            Optional. The reservation that jobs.query request would use.
            User can specify a reservation to execute the job.query. The
            expected format is
            ``projects/{project}/locations/{location}/reservations/{reservation}``.

            This field is a member of `oneof`_ ``_reservation``.
        write_incremental_results (bool):
            Optional. This is only supported for SELECT
            query. If set, the query is allowed to write
            results incrementally to the temporary result
            table. This may incur a performance penalty.
            This option cannot be used with Legacy SQL. This
            feature is not yet available.
    """

    class JobCreationMode(proto.Enum):
        r"""Job Creation Mode provides different options on job creation.

        Values:
            JOB_CREATION_MODE_UNSPECIFIED (0):
                If unspecified JOB_CREATION_REQUIRED is the default.
            JOB_CREATION_REQUIRED (1):
                Default. Job creation is always required.
            JOB_CREATION_OPTIONAL (2):
                Job creation is optional. Returning immediate results is
                prioritized. BigQuery will automatically determine if a Job
                needs to be created. The conditions under which BigQuery can
                decide to not create a Job are subject to change. If Job
                creation is required, JOB_CREATION_REQUIRED mode should be
                used, which is the default.
        """
        JOB_CREATION_MODE_UNSPECIFIED = 0
        JOB_CREATION_REQUIRED = 1
        JOB_CREATION_OPTIONAL = 2

    kind: str = proto.Field(
        proto.STRING,
        number=2,
    )
    query: str = proto.Field(
        proto.STRING,
        number=3,
    )
    max_results: wrappers_pb2.UInt32Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.UInt32Value,
    )
    default_dataset: dataset_reference.DatasetReference = proto.Field(
        proto.MESSAGE,
        number=5,
        message=dataset_reference.DatasetReference,
    )
    timeout_ms: wrappers_pb2.UInt32Value = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.UInt32Value,
    )
    job_timeout_ms: int = proto.Field(
        proto.INT64,
        number=26,
        optional=True,
    )
    destination_encryption_configuration: encryption_config.EncryptionConfiguration = (
        proto.Field(
            proto.MESSAGE,
            number=27,
            message=encryption_config.EncryptionConfiguration,
        )
    )
    dry_run: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    use_query_cache: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=9,
        message=wrappers_pb2.BoolValue,
    )
    use_legacy_sql: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=10,
        message=wrappers_pb2.BoolValue,
    )
    parameter_mode: str = proto.Field(
        proto.STRING,
        number=11,
    )
    query_parameters: MutableSequence[
        query_parameter.QueryParameter
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message=query_parameter.QueryParameter,
    )
    location: str = proto.Field(
        proto.STRING,
        number=13,
    )
    format_options: data_format_options.DataFormatOptions = proto.Field(
        proto.MESSAGE,
        number=15,
        message=data_format_options.DataFormatOptions,
    )
    connection_properties: MutableSequence[
        job_config.ConnectionProperty
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message=job_config.ConnectionProperty,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=17,
    )
    maximum_bytes_billed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=18,
        message=wrappers_pb2.Int64Value,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=19,
    )
    create_session: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=20,
        message=wrappers_pb2.BoolValue,
    )
    job_creation_mode: JobCreationMode = proto.Field(
        proto.ENUM,
        number=22,
        enum=JobCreationMode,
    )
    reservation: str = proto.Field(
        proto.STRING,
        number=24,
        optional=True,
    )
    write_incremental_results: bool = proto.Field(
        proto.BOOL,
        number=25,
    )


class QueryResponse(proto.Message):
    r"""

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        kind (str):
            The resource type.
        schema (google.cloud.bigquery_v2.types.TableSchema):
            The schema of the results. Present only when
            the query completes successfully.
        job_reference (google.cloud.bigquery_v2.types.JobReference):
            Reference to the Job that was created to run the query. This
            field will be present even if the original request timed
            out, in which case GetQueryResults can be used to read the
            results once the query has completed. Since this API only
            returns the first page of results, subsequent pages can be
            fetched via the same mechanism (GetQueryResults).

            If job_creation_mode was set to ``JOB_CREATION_OPTIONAL``
            and the query completes without creating a job, this field
            will be empty.
        job_creation_reason (google.cloud.bigquery_v2.types.JobCreationReason):
            Optional. The reason why a Job was created.

            Only relevant when a job_reference is present in the
            response. If job_reference is not present it will always be
            unset.
        query_id (str):
            Auto-generated ID for the query.
        location (str):
            Output only. The geographic location of the
            query.
            For more information about BigQuery locations,
            see:

            https://cloud.google.com/bigquery/docs/locations
        total_rows (google.protobuf.wrappers_pb2.UInt64Value):
            The total number of rows in the complete
            query result set, which can be more than the
            number of rows in this single page of results.
        page_token (str):
            A token used for paging results. A non-empty token indicates
            that additional results are available. To see additional
            results, query the
            ```jobs.getQueryResults`` <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults>`__
            method. For more information, see `Paging through table
            data <https://cloud.google.com/bigquery/docs/paging-results>`__.
        rows (MutableSequence[google.protobuf.struct_pb2.Struct]):
            An object with as many results as can be
            contained within the maximum permitted reply
            size. To get any additional rows, you can call
            GetQueryResults and specify the jobReference
            returned above.
        total_bytes_processed (google.protobuf.wrappers_pb2.Int64Value):
            The total number of bytes processed for this
            query. If this query was a dry run, this is the
            number of bytes that would be processed if the
            query were run.
        total_bytes_billed (int):
            Output only. If the project is configured to
            use on-demand pricing, then this field contains
            the total bytes billed for the job. If the
            project is configured to use flat-rate pricing,
            then you are not billed for bytes and this field
            is informational only.

            This field is a member of `oneof`_ ``_total_bytes_billed``.
        total_slot_ms (int):
            Output only. Number of slot ms the user is
            actually billed for.

            This field is a member of `oneof`_ ``_total_slot_ms``.
        job_complete (google.protobuf.wrappers_pb2.BoolValue):
            Whether the query has completed or not. If
            rows or totalRows are present, this will always
            be true. If this is false, totalRows will not be
            available.
        errors (MutableSequence[google.cloud.bigquery_v2.types.ErrorProto]):
            Output only. The first errors or warnings encountered during
            the running of the job. The final message includes the
            number of errors that caused the process to stop. Errors
            here do not necessarily mean that the job has completed or
            was unsuccessful. For more information about error messages,
            see `Error
            messages <https://cloud.google.com/bigquery/docs/error-messages>`__.
        cache_hit (google.protobuf.wrappers_pb2.BoolValue):
            Whether the query result was fetched from the
            query cache.
        num_dml_affected_rows (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of rows affected by a
            DML statement. Present only for DML statements
            INSERT, UPDATE or DELETE.
        session_info (google.cloud.bigquery_v2.types.SessionInfo):
            Output only. Information of the session if
            this job is part of one.
        dml_stats (google.cloud.bigquery_v2.types.DmlStats):
            Output only. Detailed statistics for DML
            statements INSERT, UPDATE, DELETE, MERGE or
            TRUNCATE.
        creation_time (int):
            Output only. Creation time of this query, in
            milliseconds since the epoch. This field will be
            present on all queries.

            This field is a member of `oneof`_ ``_creation_time``.
        start_time (int):
            Output only. Start time of this query, in
            milliseconds since the epoch. This field will be
            present when the query job transitions from the
            PENDING state to either RUNNING or DONE.

            This field is a member of `oneof`_ ``_start_time``.
        end_time (int):
            Output only. End time of this query, in
            milliseconds since the epoch. This field will be
            present whenever a query job is in the DONE
            state.

            This field is a member of `oneof`_ ``_end_time``.
    """

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    schema: table_schema.TableSchema = proto.Field(
        proto.MESSAGE,
        number=2,
        message=table_schema.TableSchema,
    )
    job_reference: gcb_job_reference.JobReference = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcb_job_reference.JobReference,
    )
    job_creation_reason: gcb_job_creation_reason.JobCreationReason = proto.Field(
        proto.MESSAGE,
        number=15,
        message=gcb_job_creation_reason.JobCreationReason,
    )
    query_id: str = proto.Field(
        proto.STRING,
        number=14,
    )
    location: str = proto.Field(
        proto.STRING,
        number=18,
    )
    total_rows: wrappers_pb2.UInt64Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.UInt64Value,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=5,
    )
    rows: MutableSequence[struct_pb2.Struct] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )
    total_bytes_processed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.Int64Value,
    )
    total_bytes_billed: int = proto.Field(
        proto.INT64,
        number=16,
        optional=True,
    )
    total_slot_ms: int = proto.Field(
        proto.INT64,
        number=17,
        optional=True,
    )
    job_complete: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=8,
        message=wrappers_pb2.BoolValue,
    )
    errors: MutableSequence[error.ErrorProto] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=error.ErrorProto,
    )
    cache_hit: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=10,
        message=wrappers_pb2.BoolValue,
    )
    num_dml_affected_rows: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=11,
        message=wrappers_pb2.Int64Value,
    )
    session_info: gcb_session_info.SessionInfo = proto.Field(
        proto.MESSAGE,
        number=12,
        message=gcb_session_info.SessionInfo,
    )
    dml_stats: job_stats.DmlStats = proto.Field(
        proto.MESSAGE,
        number=13,
        message=job_stats.DmlStats,
    )
    creation_time: int = proto.Field(
        proto.INT64,
        number=19,
        optional=True,
    )
    start_time: int = proto.Field(
        proto.INT64,
        number=20,
        optional=True,
    )
    end_time: int = proto.Field(
        proto.INT64,
        number=21,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
