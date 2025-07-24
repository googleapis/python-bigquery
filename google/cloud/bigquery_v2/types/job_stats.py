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

from google.cloud.bigquery_v2.types import dataset_reference
from google.cloud.bigquery_v2.types import model
from google.cloud.bigquery_v2.types import query_parameter
from google.cloud.bigquery_v2.types import routine_reference
from google.cloud.bigquery_v2.types import row_access_policy_reference
from google.cloud.bigquery_v2.types import session_info as gcb_session_info
from google.cloud.bigquery_v2.types import table_reference as gcb_table_reference
from google.cloud.bigquery_v2.types import table_schema
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "ReservationEdition",
        "ExplainQueryStep",
        "ExplainQueryStage",
        "QueryTimelineSample",
        "ExternalServiceCost",
        "ExportDataStatistics",
        "BiEngineReason",
        "BiEngineStatistics",
        "IndexUnusedReason",
        "StoredColumnsUsage",
        "SearchStatistics",
        "VectorSearchStatistics",
        "QueryInfo",
        "LoadQueryStatistics",
        "JobStatistics2",
        "JobStatistics3",
        "JobStatistics4",
        "CopyJobStatistics",
        "MlStatistics",
        "ScriptStatistics",
        "RowLevelSecurityStatistics",
        "DataMaskingStatistics",
        "JobStatistics",
        "DmlStats",
        "PerformanceInsights",
        "StagePerformanceChangeInsight",
        "InputDataChange",
        "StagePerformanceStandaloneInsight",
        "HighCardinalityJoin",
        "PartitionSkew",
        "SparkStatistics",
        "MaterializedViewStatistics",
        "MaterializedView",
        "TableMetadataCacheUsage",
        "MetadataCacheStatistics",
    },
)


class ReservationEdition(proto.Enum):
    r"""The type of editions.
    Different features and behaviors are provided to different
    editions Capacity commitments and reservations are linked to
    editions.

    Values:
        RESERVATION_EDITION_UNSPECIFIED (0):
            Default value, which will be treated as
            ENTERPRISE.
        STANDARD (1):
            Standard edition.
        ENTERPRISE (2):
            Enterprise edition.
        ENTERPRISE_PLUS (3):
            Enterprise Plus edition.
    """
    RESERVATION_EDITION_UNSPECIFIED = 0
    STANDARD = 1
    ENTERPRISE = 2
    ENTERPRISE_PLUS = 3


class ExplainQueryStep(proto.Message):
    r"""An operation within a stage.

    Attributes:
        kind (str):
            Machine-readable operation type.
        substeps (MutableSequence[str]):
            Human-readable description of the step(s).
    """

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    substeps: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class ExplainQueryStage(proto.Message):
    r"""A single stage of query execution.

    Attributes:
        name (str):
            Human-readable name for the stage.
        id (google.protobuf.wrappers_pb2.Int64Value):
            Unique ID for the stage within the plan.
        start_ms (int):
            Stage start time represented as milliseconds
            since the epoch.
        end_ms (int):
            Stage end time represented as milliseconds
            since the epoch.
        input_stages (MutableSequence[int]):
            IDs for stages that are inputs to this stage.
        wait_ratio_avg (google.protobuf.wrappers_pb2.DoubleValue):
            Relative amount of time the average shard
            spent waiting to be scheduled.
        wait_ms_avg (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds the average shard spent waiting
            to be scheduled.
        wait_ratio_max (google.protobuf.wrappers_pb2.DoubleValue):
            Relative amount of time the slowest shard
            spent waiting to be scheduled.
        wait_ms_max (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds the slowest shard spent waiting
            to be scheduled.
        read_ratio_avg (google.protobuf.wrappers_pb2.DoubleValue):
            Relative amount of time the average shard
            spent reading input.
        read_ms_avg (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds the average shard spent reading
            input.
        read_ratio_max (google.protobuf.wrappers_pb2.DoubleValue):
            Relative amount of time the slowest shard
            spent reading input.
        read_ms_max (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds the slowest shard spent reading
            input.
        compute_ratio_avg (google.protobuf.wrappers_pb2.DoubleValue):
            Relative amount of time the average shard
            spent on CPU-bound tasks.
        compute_ms_avg (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds the average shard spent on
            CPU-bound tasks.
        compute_ratio_max (google.protobuf.wrappers_pb2.DoubleValue):
            Relative amount of time the slowest shard
            spent on CPU-bound tasks.
        compute_ms_max (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds the slowest shard spent on
            CPU-bound tasks.
        write_ratio_avg (google.protobuf.wrappers_pb2.DoubleValue):
            Relative amount of time the average shard
            spent on writing output.
        write_ms_avg (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds the average shard spent on
            writing output.
        write_ratio_max (google.protobuf.wrappers_pb2.DoubleValue):
            Relative amount of time the slowest shard
            spent on writing output.
        write_ms_max (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds the slowest shard spent on
            writing output.
        shuffle_output_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Total number of bytes written to shuffle.
        shuffle_output_bytes_spilled (google.protobuf.wrappers_pb2.Int64Value):
            Total number of bytes written to shuffle and
            spilled to disk.
        records_read (google.protobuf.wrappers_pb2.Int64Value):
            Number of records read into the stage.
        records_written (google.protobuf.wrappers_pb2.Int64Value):
            Number of records written by the stage.
        parallel_inputs (google.protobuf.wrappers_pb2.Int64Value):
            Number of parallel input segments to be
            processed
        completed_parallel_inputs (google.protobuf.wrappers_pb2.Int64Value):
            Number of parallel input segments completed.
        status (str):
            Current status for this stage.
        steps (MutableSequence[google.cloud.bigquery_v2.types.ExplainQueryStep]):
            List of operations within the stage in
            dependency order (approximately chronological).
        slot_ms (google.protobuf.wrappers_pb2.Int64Value):
            Slot-milliseconds used by the stage.
        compute_mode (google.cloud.bigquery_v2.types.ExplainQueryStage.ComputeMode):
            Output only. Compute mode for this stage.
    """

    class ComputeMode(proto.Enum):
        r"""Indicates the type of compute mode.

        Values:
            COMPUTE_MODE_UNSPECIFIED (0):
                ComputeMode type not specified.
            BIGQUERY (1):
                This stage was processed using BigQuery
                slots.
            BI_ENGINE (2):
                This stage was processed using BI Engine
                compute.
        """
        COMPUTE_MODE_UNSPECIFIED = 0
        BIGQUERY = 1
        BI_ENGINE = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    start_ms: int = proto.Field(
        proto.INT64,
        number=3,
    )
    end_ms: int = proto.Field(
        proto.INT64,
        number=4,
    )
    input_stages: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=5,
    )
    wait_ratio_avg: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.DoubleValue,
    )
    wait_ms_avg: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.Int64Value,
    )
    wait_ratio_max: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=8,
        message=wrappers_pb2.DoubleValue,
    )
    wait_ms_max: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=9,
        message=wrappers_pb2.Int64Value,
    )
    read_ratio_avg: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=10,
        message=wrappers_pb2.DoubleValue,
    )
    read_ms_avg: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=11,
        message=wrappers_pb2.Int64Value,
    )
    read_ratio_max: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=12,
        message=wrappers_pb2.DoubleValue,
    )
    read_ms_max: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=13,
        message=wrappers_pb2.Int64Value,
    )
    compute_ratio_avg: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=14,
        message=wrappers_pb2.DoubleValue,
    )
    compute_ms_avg: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=15,
        message=wrappers_pb2.Int64Value,
    )
    compute_ratio_max: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=16,
        message=wrappers_pb2.DoubleValue,
    )
    compute_ms_max: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=17,
        message=wrappers_pb2.Int64Value,
    )
    write_ratio_avg: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=18,
        message=wrappers_pb2.DoubleValue,
    )
    write_ms_avg: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=19,
        message=wrappers_pb2.Int64Value,
    )
    write_ratio_max: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=20,
        message=wrappers_pb2.DoubleValue,
    )
    write_ms_max: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=21,
        message=wrappers_pb2.Int64Value,
    )
    shuffle_output_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=22,
        message=wrappers_pb2.Int64Value,
    )
    shuffle_output_bytes_spilled: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=23,
        message=wrappers_pb2.Int64Value,
    )
    records_read: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=24,
        message=wrappers_pb2.Int64Value,
    )
    records_written: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=25,
        message=wrappers_pb2.Int64Value,
    )
    parallel_inputs: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=26,
        message=wrappers_pb2.Int64Value,
    )
    completed_parallel_inputs: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=27,
        message=wrappers_pb2.Int64Value,
    )
    status: str = proto.Field(
        proto.STRING,
        number=28,
    )
    steps: MutableSequence["ExplainQueryStep"] = proto.RepeatedField(
        proto.MESSAGE,
        number=29,
        message="ExplainQueryStep",
    )
    slot_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=30,
        message=wrappers_pb2.Int64Value,
    )
    compute_mode: ComputeMode = proto.Field(
        proto.ENUM,
        number=31,
        enum=ComputeMode,
    )


class QueryTimelineSample(proto.Message):
    r"""Summary of the state of query execution at a given time.

    Attributes:
        elapsed_ms (google.protobuf.wrappers_pb2.Int64Value):
            Milliseconds elapsed since the start of query
            execution.
        total_slot_ms (google.protobuf.wrappers_pb2.Int64Value):
            Cumulative slot-ms consumed by the query.
        pending_units (google.protobuf.wrappers_pb2.Int64Value):
            Total units of work remaining for the query.
            This number can be revised (increased or
            decreased) while the query is running.
        completed_units (google.protobuf.wrappers_pb2.Int64Value):
            Total parallel units of work completed by
            this query.
        active_units (google.protobuf.wrappers_pb2.Int64Value):
            Total number of active workers. This does not
            correspond directly to slot usage. This is the
            largest value observed since the last sample.
        shuffle_ram_usage_ratio (google.protobuf.wrappers_pb2.DoubleValue):
            Total shuffle usage ratio in shuffle RAM per
            reservation of this query. This will be provided
            for reservation customers only.
        estimated_runnable_units (google.protobuf.wrappers_pb2.Int64Value):
            Units of work that can be scheduled
            immediately. Providing additional slots for
            these units of work will accelerate the query,
            if no other query in the reservation needs
            additional slots.
    """

    elapsed_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.Int64Value,
    )
    total_slot_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    pending_units: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.Int64Value,
    )
    completed_units: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.Int64Value,
    )
    active_units: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.Int64Value,
    )
    shuffle_ram_usage_ratio: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.DoubleValue,
    )
    estimated_runnable_units: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.Int64Value,
    )


class ExternalServiceCost(proto.Message):
    r"""The external service cost is a portion of the total cost, these
    costs are not additive with total_bytes_billed. Moreover, this field
    only track external service costs that will show up as BigQuery
    costs (e.g. training BigQuery ML job with google cloud CAIP or
    Automl Tables services), not other costs which may be accrued by
    running the query (e.g. reading from Bigtable or Cloud Storage). The
    external service costs with different billing sku (e.g. CAIP job is
    charged based on VM usage) are converted to BigQuery billed_bytes
    and slot_ms with equivalent amount of US dollars. Services may not
    directly correlate to these metrics, but these are the equivalents
    for billing purposes. Output only.

    Attributes:
        external_service (str):
            External service name.
        bytes_processed (google.protobuf.wrappers_pb2.Int64Value):
            External service cost in terms of bigquery
            bytes processed.
        bytes_billed (google.protobuf.wrappers_pb2.Int64Value):
            External service cost in terms of bigquery
            bytes billed.
        slot_ms (google.protobuf.wrappers_pb2.Int64Value):
            External service cost in terms of bigquery
            slot milliseconds.
        reserved_slot_count (int):
            Non-preemptable reserved slots used for
            external job. For example, reserved slots for
            Cloua AI Platform job are the VM usages
            converted to BigQuery slot with equivalent mount
            of price.
    """

    external_service: str = proto.Field(
        proto.STRING,
        number=1,
    )
    bytes_processed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    bytes_billed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.Int64Value,
    )
    slot_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.Int64Value,
    )
    reserved_slot_count: int = proto.Field(
        proto.INT64,
        number=5,
    )


class ExportDataStatistics(proto.Message):
    r"""Statistics for the EXPORT DATA statement as part of Query
    Job. EXTRACT JOB statistics are populated in JobStatistics4.

    Attributes:
        file_count (google.protobuf.wrappers_pb2.Int64Value):
            Number of destination files generated in case
            of EXPORT DATA statement only.
        row_count (google.protobuf.wrappers_pb2.Int64Value):
            [Alpha] Number of destination rows generated in case of
            EXPORT DATA statement only.
    """

    file_count: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.Int64Value,
    )
    row_count: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )


class BiEngineReason(proto.Message):
    r"""Reason why BI Engine didn't accelerate the query (or
    sub-query).

    Attributes:
        code (google.cloud.bigquery_v2.types.BiEngineReason.Code):
            Output only. High-level BI Engine reason for
            partial or disabled acceleration
        message (str):
            Output only. Free form human-readable reason
            for partial or disabled acceleration.
    """

    class Code(proto.Enum):
        r"""Indicates the high-level reason for no/partial acceleration

        Values:
            CODE_UNSPECIFIED (0):
                BiEngineReason not specified.
            NO_RESERVATION (1):
                No reservation available for BI Engine
                acceleration.
            INSUFFICIENT_RESERVATION (2):
                Not enough memory available for BI Engine
                acceleration.
            UNSUPPORTED_SQL_TEXT (4):
                This particular SQL text is not supported for
                acceleration by BI Engine.
            INPUT_TOO_LARGE (5):
                Input too large for acceleration by BI
                Engine.
            OTHER_REASON (6):
                Catch-all code for all other cases for
                partial or disabled acceleration.
            TABLE_EXCLUDED (7):
                One or more tables were not eligible for BI
                Engine acceleration.
        """
        CODE_UNSPECIFIED = 0
        NO_RESERVATION = 1
        INSUFFICIENT_RESERVATION = 2
        UNSUPPORTED_SQL_TEXT = 4
        INPUT_TOO_LARGE = 5
        OTHER_REASON = 6
        TABLE_EXCLUDED = 7

    code: Code = proto.Field(
        proto.ENUM,
        number=1,
        enum=Code,
    )
    message: str = proto.Field(
        proto.STRING,
        number=2,
    )


class BiEngineStatistics(proto.Message):
    r"""Statistics for a BI Engine specific query.
    Populated as part of JobStatistics2

    Attributes:
        bi_engine_mode (google.cloud.bigquery_v2.types.BiEngineStatistics.BiEngineMode):
            Output only. Specifies which mode of BI
            Engine acceleration was performed (if any).
        acceleration_mode (google.cloud.bigquery_v2.types.BiEngineStatistics.BiEngineAccelerationMode):
            Output only. Specifies which mode of BI
            Engine acceleration was performed (if any).
        bi_engine_reasons (MutableSequence[google.cloud.bigquery_v2.types.BiEngineReason]):
            In case of DISABLED or PARTIAL bi_engine_mode, these contain
            the explanatory reasons as to why BI Engine could not
            accelerate. In case the full query was accelerated, this
            field is not populated.
    """

    class BiEngineMode(proto.Enum):
        r"""Indicates the type of BI Engine acceleration.

        Values:
            ACCELERATION_MODE_UNSPECIFIED (0):
                BiEngineMode type not specified.
            DISABLED (1):
                BI Engine disabled the acceleration. bi_engine_reasons
                specifies a more detailed reason.
            PARTIAL (2):
                Part of the query was accelerated using BI Engine. See
                bi_engine_reasons for why parts of the query were not
                accelerated.
            FULL (3):
                All of the query was accelerated using BI
                Engine.
        """
        ACCELERATION_MODE_UNSPECIFIED = 0
        DISABLED = 1
        PARTIAL = 2
        FULL = 3

    class BiEngineAccelerationMode(proto.Enum):
        r"""Indicates the type of BI Engine acceleration.

        Values:
            BI_ENGINE_ACCELERATION_MODE_UNSPECIFIED (0):
                BiEngineMode type not specified.
            BI_ENGINE_DISABLED (1):
                BI Engine acceleration was attempted but disabled.
                bi_engine_reasons specifies a more detailed reason.
            PARTIAL_INPUT (2):
                Some inputs were accelerated using BI Engine. See
                bi_engine_reasons for why parts of the query were not
                accelerated.
            FULL_INPUT (3):
                All of the query inputs were accelerated
                using BI Engine.
            FULL_QUERY (4):
                All of the query was accelerated using BI
                Engine.
        """
        BI_ENGINE_ACCELERATION_MODE_UNSPECIFIED = 0
        BI_ENGINE_DISABLED = 1
        PARTIAL_INPUT = 2
        FULL_INPUT = 3
        FULL_QUERY = 4

    bi_engine_mode: BiEngineMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=BiEngineMode,
    )
    acceleration_mode: BiEngineAccelerationMode = proto.Field(
        proto.ENUM,
        number=3,
        enum=BiEngineAccelerationMode,
    )
    bi_engine_reasons: MutableSequence["BiEngineReason"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="BiEngineReason",
    )


class IndexUnusedReason(proto.Message):
    r"""Reason about why no search index was used in the search query
    (or sub-query).


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        code (google.cloud.bigquery_v2.types.IndexUnusedReason.Code):
            Specifies the high-level reason for the
            scenario when no search index was used.

            This field is a member of `oneof`_ ``_code``.
        message (str):
            Free form human-readable reason for the
            scenario when no search index was used.

            This field is a member of `oneof`_ ``_message``.
        base_table (google.cloud.bigquery_v2.types.TableReference):
            Specifies the base table involved in the
            reason that no search index was used.

            This field is a member of `oneof`_ ``_base_table``.
        index_name (str):
            Specifies the name of the unused search
            index, if available.

            This field is a member of `oneof`_ ``_index_name``.
    """

    class Code(proto.Enum):
        r"""Indicates the high-level reason for the scenario when no
        search index was used.

        Values:
            CODE_UNSPECIFIED (0):
                Code not specified.
            INDEX_CONFIG_NOT_AVAILABLE (1):
                Indicates the search index configuration has
                not been created.
            PENDING_INDEX_CREATION (2):
                Indicates the search index creation has not
                been completed.
            BASE_TABLE_TRUNCATED (3):
                Indicates the base table has been truncated
                (rows have been removed from table with TRUNCATE
                TABLE statement) since the last time the search
                index was refreshed.
            INDEX_CONFIG_MODIFIED (4):
                Indicates the search index configuration has
                been changed since the last time the search
                index was refreshed.
            TIME_TRAVEL_QUERY (5):
                Indicates the search query accesses data at a
                timestamp before the last time the search index
                was refreshed.
            NO_PRUNING_POWER (6):
                Indicates the usage of search index will not
                contribute to any pruning improvement for the
                search function, e.g. when the search predicate
                is in a disjunction with other non-search
                predicates.
            UNINDEXED_SEARCH_FIELDS (7):
                Indicates the search index does not cover all
                fields in the search function.
            UNSUPPORTED_SEARCH_PATTERN (8):
                Indicates the search index does not support
                the given search query pattern.
            OPTIMIZED_WITH_MATERIALIZED_VIEW (9):
                Indicates the query has been optimized by
                using a materialized view.
            SECURED_BY_DATA_MASKING (11):
                Indicates the query has been secured by data
                masking, and thus search indexes are not
                applicable.
            MISMATCHED_TEXT_ANALYZER (12):
                Indicates that the search index and the
                search function call do not have the same text
                analyzer.
            BASE_TABLE_TOO_SMALL (13):
                Indicates the base table is too small (below
                a certain threshold). The index does not provide
                noticeable search performance gains when the
                base table is too small.
            BASE_TABLE_TOO_LARGE (14):
                Indicates that the total size of indexed base tables in your
                organization exceeds your region's limit and the index is
                not used in the query. To index larger base tables, you can
                use your own reservation for index-management jobs.
            ESTIMATED_PERFORMANCE_GAIN_TOO_LOW (15):
                Indicates that the estimated performance gain
                from using the search index is too low for the
                given search query.
            COLUMN_METADATA_INDEX_NOT_USED (21):
                Indicates that the column metadata index (which the search
                index depends on) is not used. User can refer to the `column
                metadata index
                usage <https://cloud.google.com/bigquery/docs/metadata-indexing-managed-tables#view_column_metadata_index_usage>`__
                for more details on why it was not used.
            NOT_SUPPORTED_IN_STANDARD_EDITION (17):
                Indicates that search indexes can not be used
                for search query with STANDARD edition.
            INDEX_SUPPRESSED_BY_FUNCTION_OPTION (18):
                Indicates that an option in the search
                function that cannot make use of the index has
                been selected.
            QUERY_CACHE_HIT (19):
                Indicates that the query was cached, and thus
                the search index was not used.
            STALE_INDEX (20):
                The index cannot be used in the search query
                because it is stale.
            INTERNAL_ERROR (10):
                Indicates an internal error that causes the
                search index to be unused.
            OTHER_REASON (16):
                Indicates that the reason search indexes
                cannot be used in the query is not covered by
                any of the other IndexUnusedReason options.
        """
        CODE_UNSPECIFIED = 0
        INDEX_CONFIG_NOT_AVAILABLE = 1
        PENDING_INDEX_CREATION = 2
        BASE_TABLE_TRUNCATED = 3
        INDEX_CONFIG_MODIFIED = 4
        TIME_TRAVEL_QUERY = 5
        NO_PRUNING_POWER = 6
        UNINDEXED_SEARCH_FIELDS = 7
        UNSUPPORTED_SEARCH_PATTERN = 8
        OPTIMIZED_WITH_MATERIALIZED_VIEW = 9
        SECURED_BY_DATA_MASKING = 11
        MISMATCHED_TEXT_ANALYZER = 12
        BASE_TABLE_TOO_SMALL = 13
        BASE_TABLE_TOO_LARGE = 14
        ESTIMATED_PERFORMANCE_GAIN_TOO_LOW = 15
        COLUMN_METADATA_INDEX_NOT_USED = 21
        NOT_SUPPORTED_IN_STANDARD_EDITION = 17
        INDEX_SUPPRESSED_BY_FUNCTION_OPTION = 18
        QUERY_CACHE_HIT = 19
        STALE_INDEX = 20
        INTERNAL_ERROR = 10
        OTHER_REASON = 16

    code: Code = proto.Field(
        proto.ENUM,
        number=1,
        optional=True,
        enum=Code,
    )
    message: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    base_table: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=3,
        optional=True,
        message=gcb_table_reference.TableReference,
    )
    index_name: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )


class StoredColumnsUsage(proto.Message):
    r"""Indicates the stored columns usage in the query.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        is_query_accelerated (bool):
            Specifies whether the query was accelerated
            with stored columns.

            This field is a member of `oneof`_ ``_is_query_accelerated``.
        base_table (google.cloud.bigquery_v2.types.TableReference):
            Specifies the base table.

            This field is a member of `oneof`_ ``_base_table``.
        stored_columns_unused_reasons (MutableSequence[google.cloud.bigquery_v2.types.StoredColumnsUsage.StoredColumnsUnusedReason]):
            If stored columns were not used, explain why.
    """

    class StoredColumnsUnusedReason(proto.Message):
        r"""If the stored column was not used, explain why.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            code (google.cloud.bigquery_v2.types.StoredColumnsUsage.StoredColumnsUnusedReason.Code):
                Specifies the high-level reason for the
                unused scenario, each reason must have a code
                associated.

                This field is a member of `oneof`_ ``_code``.
            message (str):
                Specifies the detailed description for the
                scenario.

                This field is a member of `oneof`_ ``_message``.
            uncovered_columns (MutableSequence[str]):
                Specifies which columns were not covered by the stored
                columns for the specified code up to 20 columns. This is
                populated when the code is STORED_COLUMNS_COVER_INSUFFICIENT
                and BASE_TABLE_HAS_CLS.
        """

        class Code(proto.Enum):
            r"""Indicates the high-level reason for the scenario when stored
            columns cannot be used in the query.

            Values:
                CODE_UNSPECIFIED (0):
                    Default value.
                STORED_COLUMNS_COVER_INSUFFICIENT (1):
                    If stored columns do not fully cover the
                    columns.
                BASE_TABLE_HAS_RLS (2):
                    If the base table has RLS (Row Level
                    Security).
                BASE_TABLE_HAS_CLS (3):
                    If the base table has CLS (Column Level
                    Security).
                UNSUPPORTED_PREFILTER (4):
                    If the provided prefilter is not supported.
                INTERNAL_ERROR (5):
                    If an internal error is preventing stored
                    columns from being used.
                OTHER_REASON (6):
                    Indicates that the reason stored columns
                    cannot be used in the query is not covered by
                    any of the other StoredColumnsUnusedReason
                    options.
            """
            CODE_UNSPECIFIED = 0
            STORED_COLUMNS_COVER_INSUFFICIENT = 1
            BASE_TABLE_HAS_RLS = 2
            BASE_TABLE_HAS_CLS = 3
            UNSUPPORTED_PREFILTER = 4
            INTERNAL_ERROR = 5
            OTHER_REASON = 6

        code: "StoredColumnsUsage.StoredColumnsUnusedReason.Code" = proto.Field(
            proto.ENUM,
            number=1,
            optional=True,
            enum="StoredColumnsUsage.StoredColumnsUnusedReason.Code",
        )
        message: str = proto.Field(
            proto.STRING,
            number=2,
            optional=True,
        )
        uncovered_columns: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )

    is_query_accelerated: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    base_table: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=2,
        optional=True,
        message=gcb_table_reference.TableReference,
    )
    stored_columns_unused_reasons: MutableSequence[
        StoredColumnsUnusedReason
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=StoredColumnsUnusedReason,
    )


class SearchStatistics(proto.Message):
    r"""Statistics for a search query.
    Populated as part of JobStatistics2.

    Attributes:
        index_usage_mode (google.cloud.bigquery_v2.types.SearchStatistics.IndexUsageMode):
            Specifies the index usage mode for the query.
        index_unused_reasons (MutableSequence[google.cloud.bigquery_v2.types.IndexUnusedReason]):
            When ``indexUsageMode`` is ``UNUSED`` or ``PARTIALLY_USED``,
            this field explains why indexes were not used in all or part
            of the search query. If ``indexUsageMode`` is
            ``FULLY_USED``, this field is not populated.
    """

    class IndexUsageMode(proto.Enum):
        r"""Indicates the type of search index usage in the entire search
        query.

        Values:
            INDEX_USAGE_MODE_UNSPECIFIED (0):
                Index usage mode not specified.
            UNUSED (1):
                No search indexes were used in the search query. See
                [``indexUnusedReasons``]
                (/bigquery/docs/reference/rest/v2/Job#IndexUnusedReason) for
                detailed reasons.
            PARTIALLY_USED (2):
                Part of the search query used search indexes. See
                [``indexUnusedReasons``]
                (/bigquery/docs/reference/rest/v2/Job#IndexUnusedReason) for
                why other parts of the query did not use search indexes.
            FULLY_USED (4):
                The entire search query used search indexes.
        """
        INDEX_USAGE_MODE_UNSPECIFIED = 0
        UNUSED = 1
        PARTIALLY_USED = 2
        FULLY_USED = 4

    index_usage_mode: IndexUsageMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=IndexUsageMode,
    )
    index_unused_reasons: MutableSequence["IndexUnusedReason"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="IndexUnusedReason",
    )


class VectorSearchStatistics(proto.Message):
    r"""Statistics for a vector search query.
    Populated as part of JobStatistics2.

    Attributes:
        index_usage_mode (google.cloud.bigquery_v2.types.VectorSearchStatistics.IndexUsageMode):
            Specifies the index usage mode for the query.
        index_unused_reasons (MutableSequence[google.cloud.bigquery_v2.types.IndexUnusedReason]):
            When ``indexUsageMode`` is ``UNUSED`` or ``PARTIALLY_USED``,
            this field explains why indexes were not used in all or part
            of the vector search query. If ``indexUsageMode`` is
            ``FULLY_USED``, this field is not populated.
        stored_columns_usages (MutableSequence[google.cloud.bigquery_v2.types.StoredColumnsUsage]):
            Specifies the usage of stored columns in the
            query when stored columns are used in the query.
    """

    class IndexUsageMode(proto.Enum):
        r"""Indicates the type of vector index usage in the entire vector
        search query.

        Values:
            INDEX_USAGE_MODE_UNSPECIFIED (0):
                Index usage mode not specified.
            UNUSED (1):
                No vector indexes were used in the vector search query. See
                [``indexUnusedReasons``]
                (/bigquery/docs/reference/rest/v2/Job#IndexUnusedReason) for
                detailed reasons.
            PARTIALLY_USED (2):
                Part of the vector search query used vector indexes. See
                [``indexUnusedReasons``]
                (/bigquery/docs/reference/rest/v2/Job#IndexUnusedReason) for
                why other parts of the query did not use vector indexes.
            FULLY_USED (4):
                The entire vector search query used vector
                indexes.
        """
        INDEX_USAGE_MODE_UNSPECIFIED = 0
        UNUSED = 1
        PARTIALLY_USED = 2
        FULLY_USED = 4

    index_usage_mode: IndexUsageMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=IndexUsageMode,
    )
    index_unused_reasons: MutableSequence["IndexUnusedReason"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="IndexUnusedReason",
    )
    stored_columns_usages: MutableSequence["StoredColumnsUsage"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="StoredColumnsUsage",
    )


class QueryInfo(proto.Message):
    r"""Query optimization information for a QUERY job.

    Attributes:
        optimization_details (google.protobuf.struct_pb2.Struct):
            Output only. Information about query
            optimizations.
    """

    optimization_details: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )


class LoadQueryStatistics(proto.Message):
    r"""Statistics for a LOAD query.

    Attributes:
        input_files (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of source files in a LOAD
            query.
        input_file_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of bytes of source data
            in a LOAD query.
        output_rows (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of rows imported in a
            LOAD query. Note that while a LOAD query is in
            the running state, this value may change.
        output_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Size of the loaded data in
            bytes. Note that while a LOAD query is in the
            running state, this value may change.
        bad_records (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of bad records
            encountered while processing a LOAD query. Note
            that if the job has failed because of more bad
            records encountered than the maximum allowed in
            the load job configuration, then this number can
            be less than the total number of bad records
            present in the input data.
    """

    input_files: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.Int64Value,
    )
    input_file_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    output_rows: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.Int64Value,
    )
    output_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.Int64Value,
    )
    bad_records: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.Int64Value,
    )


class JobStatistics2(proto.Message):
    r"""Statistics for a query job.

    Attributes:
        query_plan (MutableSequence[google.cloud.bigquery_v2.types.ExplainQueryStage]):
            Output only. Describes execution plan for the
            query.
        estimated_bytes_processed (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The original estimate of bytes
            processed for the job.
        timeline (MutableSequence[google.cloud.bigquery_v2.types.QueryTimelineSample]):
            Output only. Describes a timeline of job
            execution.
        total_partitions_processed (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Total number of partitions
            processed from all partitioned tables referenced
            in the job.
        total_bytes_processed (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Total bytes processed for the
            job.
        total_bytes_processed_accuracy (str):
            Output only. For dry-run jobs, totalBytesProcessed is an
            estimate and this field specifies the accuracy of the
            estimate. Possible values can be: UNKNOWN: accuracy of the
            estimate is unknown. PRECISE: estimate is precise.
            LOWER_BOUND: estimate is lower bound of what the query would
            cost. UPPER_BOUND: estimate is upper bound of what the query
            would cost.
        total_bytes_billed (google.protobuf.wrappers_pb2.Int64Value):
            Output only. If the project is configured to
            use on-demand pricing, then this field contains
            the total bytes billed for the job. If the
            project is configured to use flat-rate pricing,
            then you are not billed for bytes and this field
            is informational only.
        billing_tier (google.protobuf.wrappers_pb2.Int32Value):
            Output only. Billing tier for the job. This
            is a BigQuery-specific concept which is not
            related to the Google Cloud notion of "free
            tier". The value here is a measure of the
            query's resource consumption relative to the
            amount of data scanned. For on-demand queries,
            the limit is 100, and all queries within this
            limit are billed at the standard on-demand
            rates. On-demand queries that exceed this limit
            will fail with a billingTierLimitExceeded error.
        total_slot_ms (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Slot-milliseconds for the job.
        cache_hit (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the query result was
            fetched from the query cache.
        referenced_tables (MutableSequence[google.cloud.bigquery_v2.types.TableReference]):
            Output only. Referenced tables for the job.
        referenced_routines (MutableSequence[google.cloud.bigquery_v2.types.RoutineReference]):
            Output only. Referenced routines for the job.
        schema (google.cloud.bigquery_v2.types.TableSchema):
            Output only. The schema of the results.
            Present only for successful dry run of
            non-legacy SQL queries.
        num_dml_affected_rows (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of rows affected by a
            DML statement. Present only for DML statements
            INSERT, UPDATE or DELETE.
        dml_stats (google.cloud.bigquery_v2.types.DmlStats):
            Output only. Detailed statistics for DML
            statements INSERT, UPDATE, DELETE, MERGE or
            TRUNCATE.
        undeclared_query_parameters (MutableSequence[google.cloud.bigquery_v2.types.QueryParameter]):
            Output only. GoogleSQL only: list of
            undeclared query parameters detected during a
            dry run validation.
        statement_type (str):
            Output only. The type of query statement, if valid. Possible
            values:

            -  ``SELECT``:
               ```SELECT`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#select_list>`__
               statement.
            -  ``ASSERT``:
               ```ASSERT`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/debugging-statements#assert>`__
               statement.
            -  ``INSERT``:
               ```INSERT`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#insert_statement>`__
               statement.
            -  ``UPDATE``:
               ```UPDATE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#update_statement>`__
               statement.
            -  ``DELETE``:
               ```DELETE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language>`__
               statement.
            -  ``MERGE``:
               ```MERGE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language>`__
               statement.
            -  ``CREATE_TABLE``:
               ```CREATE TABLE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_table_statement>`__
               statement, without ``AS SELECT``.
            -  ``CREATE_TABLE_AS_SELECT``:
               ```CREATE TABLE AS SELECT`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_table_statement>`__
               statement.
            -  ``CREATE_VIEW``:
               ```CREATE VIEW`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_view_statement>`__
               statement.
            -  ``CREATE_MODEL``:
               ```CREATE MODEL`` <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create#create_model_statement>`__
               statement.
            -  ``CREATE_MATERIALIZED_VIEW``:
               ```CREATE MATERIALIZED VIEW`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_materialized_view_statement>`__
               statement.
            -  ``CREATE_FUNCTION``:
               ```CREATE FUNCTION`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_function_statement>`__
               statement.
            -  ``CREATE_TABLE_FUNCTION``:
               ```CREATE TABLE FUNCTION`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_table_function_statement>`__
               statement.
            -  ``CREATE_PROCEDURE``:
               ```CREATE PROCEDURE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_procedure>`__
               statement.
            -  ``CREATE_ROW_ACCESS_POLICY``:
               ```CREATE ROW ACCESS POLICY`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_row_access_policy_statement>`__
               statement.
            -  ``CREATE_SCHEMA``:
               ```CREATE SCHEMA`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_schema_statement>`__
               statement.
            -  ``CREATE_SNAPSHOT_TABLE``:
               ```CREATE SNAPSHOT TABLE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_snapshot_table_statement>`__
               statement.
            -  ``CREATE_SEARCH_INDEX``:
               ```CREATE SEARCH INDEX`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_search_index_statement>`__
               statement.
            -  ``DROP_TABLE``:
               ```DROP TABLE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_table_statement>`__
               statement.
            -  ``DROP_EXTERNAL_TABLE``:
               ```DROP EXTERNAL TABLE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_external_table_statement>`__
               statement.
            -  ``DROP_VIEW``:
               ```DROP VIEW`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_view_statement>`__
               statement.
            -  ``DROP_MODEL``:
               ```DROP MODEL`` <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-drop-model>`__
               statement.
            -  ``DROP_MATERIALIZED_VIEW``:
               ```DROP MATERIALIZED VIEW`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_materialized_view_statement>`__
               statement.
            -  ``DROP_FUNCTION`` :
               ```DROP FUNCTION`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_function_statement>`__
               statement.
            -  ``DROP_TABLE_FUNCTION`` :
               ```DROP TABLE FUNCTION`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_table_function>`__
               statement.
            -  ``DROP_PROCEDURE``:
               ```DROP PROCEDURE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_procedure_statement>`__
               statement.
            -  ``DROP_SEARCH_INDEX``:
               ```DROP SEARCH INDEX`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_search_index>`__
               statement.
            -  ``DROP_SCHEMA``:
               ```DROP SCHEMA`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_schema_statement>`__
               statement.
            -  ``DROP_SNAPSHOT_TABLE``:
               ```DROP SNAPSHOT TABLE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_snapshot_table_statement>`__
               statement.
            -  ``DROP_ROW_ACCESS_POLICY``:
               ```DROP [ALL] ROW ACCESS POLICY|POLICIES`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_row_access_policy_statement>`__
               statement.
            -  ``ALTER_TABLE``:
               ```ALTER TABLE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_table_set_options_statement>`__
               statement.
            -  ``ALTER_VIEW``:
               ```ALTER VIEW`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_view_set_options_statement>`__
               statement.
            -  ``ALTER_MATERIALIZED_VIEW``:
               ```ALTER MATERIALIZED VIEW`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_materialized_view_set_options_statement>`__
               statement.
            -  ``ALTER_SCHEMA``:
               ```ALTER SCHEMA`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_schema_set_options_statement>`__
               statement.
            -  ``SCRIPT``:
               ```SCRIPT`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language>`__.
            -  ``TRUNCATE_TABLE``:
               ```TRUNCATE TABLE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#truncate_table_statement>`__
               statement.
            -  ``CREATE_EXTERNAL_TABLE``:
               ```CREATE EXTERNAL TABLE`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_external_table_statement>`__
               statement.
            -  ``EXPORT_DATA``:
               ```EXPORT DATA`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#export_data_statement>`__
               statement.
            -  ``EXPORT_MODEL``:
               ```EXPORT MODEL`` <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-export-model>`__
               statement.
            -  ``LOAD_DATA``:
               ```LOAD DATA`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#load_data_statement>`__
               statement.
            -  ``CALL``:
               ```CALL`` <https://cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language#call>`__
               statement.
        ddl_operation_performed (str):
            Output only. The DDL operation performed,
            possibly dependent on the pre-existence of the
            DDL target.
        ddl_target_table (google.cloud.bigquery_v2.types.TableReference):
            Output only. The DDL target table. Present
            only for CREATE/DROP TABLE/VIEW and DROP ALL ROW
            ACCESS POLICIES queries.
        ddl_destination_table (google.cloud.bigquery_v2.types.TableReference):
            Output only. The table after rename. Present
            only for ALTER TABLE RENAME TO query.
        ddl_target_row_access_policy (google.cloud.bigquery_v2.types.RowAccessPolicyReference):
            Output only. The DDL target row access
            policy. Present only for CREATE/DROP ROW ACCESS
            POLICY queries.
        ddl_affected_row_access_policy_count (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of row access
            policies affected by a DDL statement. Present
            only for DROP ALL ROW ACCESS POLICIES queries.
        ddl_target_routine (google.cloud.bigquery_v2.types.RoutineReference):
            Output only. [Beta] The DDL target routine. Present only for
            CREATE/DROP FUNCTION/PROCEDURE queries.
        ddl_target_dataset (google.cloud.bigquery_v2.types.DatasetReference):
            Output only. The DDL target dataset. Present
            only for CREATE/ALTER/DROP SCHEMA(dataset)
            queries.
        ml_statistics (google.cloud.bigquery_v2.types.MlStatistics):
            Output only. Statistics of a BigQuery ML
            training job.
        export_data_statistics (google.cloud.bigquery_v2.types.ExportDataStatistics):
            Output only. Stats for EXPORT DATA statement.
        external_service_costs (MutableSequence[google.cloud.bigquery_v2.types.ExternalServiceCost]):
            Output only. Job cost breakdown as bigquery
            internal cost and external service costs.
        bi_engine_statistics (google.cloud.bigquery_v2.types.BiEngineStatistics):
            Output only. BI Engine specific Statistics.
        load_query_statistics (google.cloud.bigquery_v2.types.LoadQueryStatistics):
            Output only. Statistics for a LOAD query.
        dcl_target_table (google.cloud.bigquery_v2.types.TableReference):
            Output only. Referenced table for DCL
            statement.
        dcl_target_view (google.cloud.bigquery_v2.types.TableReference):
            Output only. Referenced view for DCL
            statement.
        dcl_target_dataset (google.cloud.bigquery_v2.types.DatasetReference):
            Output only. Referenced dataset for DCL
            statement.
        search_statistics (google.cloud.bigquery_v2.types.SearchStatistics):
            Output only. Search query specific
            statistics.
        vector_search_statistics (google.cloud.bigquery_v2.types.VectorSearchStatistics):
            Output only. Vector Search query specific
            statistics.
        performance_insights (google.cloud.bigquery_v2.types.PerformanceInsights):
            Output only. Performance insights.
        query_info (google.cloud.bigquery_v2.types.QueryInfo):
            Output only. Query optimization information
            for a QUERY job.
        spark_statistics (google.cloud.bigquery_v2.types.SparkStatistics):
            Output only. Statistics of a Spark procedure
            job.
        transferred_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Total bytes transferred for
            cross-cloud queries such as Cross Cloud Transfer
            and CREATE TABLE AS SELECT (CTAS).
        materialized_view_statistics (google.cloud.bigquery_v2.types.MaterializedViewStatistics):
            Output only. Statistics of materialized views
            of a query job.
        metadata_cache_statistics (google.cloud.bigquery_v2.types.MetadataCacheStatistics):
            Output only. Statistics of metadata cache
            usage in a query for BigLake tables.
    """

    query_plan: MutableSequence["ExplainQueryStage"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ExplainQueryStage",
    )
    estimated_bytes_processed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    timeline: MutableSequence["QueryTimelineSample"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="QueryTimelineSample",
    )
    total_partitions_processed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.Int64Value,
    )
    total_bytes_processed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.Int64Value,
    )
    total_bytes_processed_accuracy: str = proto.Field(
        proto.STRING,
        number=21,
    )
    total_bytes_billed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.Int64Value,
    )
    billing_tier: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.Int32Value,
    )
    total_slot_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=8,
        message=wrappers_pb2.Int64Value,
    )
    cache_hit: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=9,
        message=wrappers_pb2.BoolValue,
    )
    referenced_tables: MutableSequence[
        gcb_table_reference.TableReference
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=gcb_table_reference.TableReference,
    )
    referenced_routines: MutableSequence[
        routine_reference.RoutineReference
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=24,
        message=routine_reference.RoutineReference,
    )
    schema: table_schema.TableSchema = proto.Field(
        proto.MESSAGE,
        number=11,
        message=table_schema.TableSchema,
    )
    num_dml_affected_rows: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=12,
        message=wrappers_pb2.Int64Value,
    )
    dml_stats: "DmlStats" = proto.Field(
        proto.MESSAGE,
        number=32,
        message="DmlStats",
    )
    undeclared_query_parameters: MutableSequence[
        query_parameter.QueryParameter
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message=query_parameter.QueryParameter,
    )
    statement_type: str = proto.Field(
        proto.STRING,
        number=14,
    )
    ddl_operation_performed: str = proto.Field(
        proto.STRING,
        number=15,
    )
    ddl_target_table: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=16,
        message=gcb_table_reference.TableReference,
    )
    ddl_destination_table: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=31,
        message=gcb_table_reference.TableReference,
    )
    ddl_target_row_access_policy: row_access_policy_reference.RowAccessPolicyReference = proto.Field(
        proto.MESSAGE,
        number=26,
        message=row_access_policy_reference.RowAccessPolicyReference,
    )
    ddl_affected_row_access_policy_count: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=27,
        message=wrappers_pb2.Int64Value,
    )
    ddl_target_routine: routine_reference.RoutineReference = proto.Field(
        proto.MESSAGE,
        number=22,
        message=routine_reference.RoutineReference,
    )
    ddl_target_dataset: dataset_reference.DatasetReference = proto.Field(
        proto.MESSAGE,
        number=30,
        message=dataset_reference.DatasetReference,
    )
    ml_statistics: "MlStatistics" = proto.Field(
        proto.MESSAGE,
        number=23,
        message="MlStatistics",
    )
    export_data_statistics: "ExportDataStatistics" = proto.Field(
        proto.MESSAGE,
        number=25,
        message="ExportDataStatistics",
    )
    external_service_costs: MutableSequence[
        "ExternalServiceCost"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=28,
        message="ExternalServiceCost",
    )
    bi_engine_statistics: "BiEngineStatistics" = proto.Field(
        proto.MESSAGE,
        number=29,
        message="BiEngineStatistics",
    )
    load_query_statistics: "LoadQueryStatistics" = proto.Field(
        proto.MESSAGE,
        number=33,
        message="LoadQueryStatistics",
    )
    dcl_target_table: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=34,
        message=gcb_table_reference.TableReference,
    )
    dcl_target_view: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=35,
        message=gcb_table_reference.TableReference,
    )
    dcl_target_dataset: dataset_reference.DatasetReference = proto.Field(
        proto.MESSAGE,
        number=36,
        message=dataset_reference.DatasetReference,
    )
    search_statistics: "SearchStatistics" = proto.Field(
        proto.MESSAGE,
        number=37,
        message="SearchStatistics",
    )
    vector_search_statistics: "VectorSearchStatistics" = proto.Field(
        proto.MESSAGE,
        number=44,
        message="VectorSearchStatistics",
    )
    performance_insights: "PerformanceInsights" = proto.Field(
        proto.MESSAGE,
        number=38,
        message="PerformanceInsights",
    )
    query_info: "QueryInfo" = proto.Field(
        proto.MESSAGE,
        number=39,
        message="QueryInfo",
    )
    spark_statistics: "SparkStatistics" = proto.Field(
        proto.MESSAGE,
        number=40,
        message="SparkStatistics",
    )
    transferred_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=41,
        message=wrappers_pb2.Int64Value,
    )
    materialized_view_statistics: "MaterializedViewStatistics" = proto.Field(
        proto.MESSAGE,
        number=42,
        message="MaterializedViewStatistics",
    )
    metadata_cache_statistics: "MetadataCacheStatistics" = proto.Field(
        proto.MESSAGE,
        number=43,
        message="MetadataCacheStatistics",
    )


class JobStatistics3(proto.Message):
    r"""Statistics for a load job.

    Attributes:
        input_files (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of source files in a load
            job.
        input_file_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of bytes of source data
            in a load job.
        output_rows (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of rows imported in a
            load job. Note that while an import job is in
            the running state, this value may change.
        output_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Size of the loaded data in
            bytes. Note that while a load job is in the
            running state, this value may change.
        bad_records (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of bad records
            encountered. Note that if the job has failed
            because of more bad records encountered than the
            maximum allowed in the load job configuration,
            then this number can be less than the total
            number of bad records present in the input data.
        timeline (MutableSequence[google.cloud.bigquery_v2.types.QueryTimelineSample]):
            Output only. Describes a timeline of job
            execution.
    """

    input_files: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.Int64Value,
    )
    input_file_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    output_rows: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.Int64Value,
    )
    output_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.Int64Value,
    )
    bad_records: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.Int64Value,
    )
    timeline: MutableSequence["QueryTimelineSample"] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="QueryTimelineSample",
    )


class JobStatistics4(proto.Message):
    r"""Statistics for an extract job.

    Attributes:
        destination_uri_file_counts (MutableSequence[int]):
            Output only. Number of files per destination
            URI or URI pattern specified in the extract
            configuration. These values will be in the same
            order as the URIs specified in the
            'destinationUris' field.
        input_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of user bytes extracted
            into the result. This is the byte count as
            computed by BigQuery for billing purposes and
            doesn't have any relationship with the number of
            actual result bytes extracted in the desired
            format.
        timeline (MutableSequence[google.cloud.bigquery_v2.types.QueryTimelineSample]):
            Output only. Describes a timeline of job
            execution.
    """

    destination_uri_file_counts: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=1,
    )
    input_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    timeline: MutableSequence["QueryTimelineSample"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="QueryTimelineSample",
    )


class CopyJobStatistics(proto.Message):
    r"""Statistics for a copy job.

    Attributes:
        copied_rows (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of rows copied to the
            destination table.
        copied_logical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of logical bytes copied
            to the destination table.
    """

    copied_rows: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.Int64Value,
    )
    copied_logical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )


class MlStatistics(proto.Message):
    r"""Job statistics specific to a BigQuery ML training job.

    Attributes:
        max_iterations (int):
            Output only. Maximum number of iterations specified as
            max_iterations in the 'CREATE MODEL' query. The actual
            number of iterations may be less than this number due to
            early stop.
        iteration_results (MutableSequence[google.cloud.bigquery_v2.types.Model.TrainingRun.IterationResult]):
            Results for all completed iterations. Empty for
            `hyperparameter tuning
            jobs <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__.
        model_type (google.cloud.bigquery_v2.types.Model.ModelType):
            Output only. The type of the model that is
            being trained.
        training_type (google.cloud.bigquery_v2.types.MlStatistics.TrainingType):
            Output only. Training type of the job.
        hparam_trials (MutableSequence[google.cloud.bigquery_v2.types.Model.HparamTuningTrial]):
            Output only. Trials of a `hyperparameter tuning
            job <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__
            sorted by trial_id.
    """

    class TrainingType(proto.Enum):
        r"""Training type.

        Values:
            TRAINING_TYPE_UNSPECIFIED (0):
                Unspecified training type.
            SINGLE_TRAINING (1):
                Single training with fixed parameter space.
            HPARAM_TUNING (2):
                `Hyperparameter tuning
                training <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__.
        """
        TRAINING_TYPE_UNSPECIFIED = 0
        SINGLE_TRAINING = 1
        HPARAM_TUNING = 2

    max_iterations: int = proto.Field(
        proto.INT64,
        number=1,
    )
    iteration_results: MutableSequence[
        model.Model.TrainingRun.IterationResult
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=model.Model.TrainingRun.IterationResult,
    )
    model_type: model.Model.ModelType = proto.Field(
        proto.ENUM,
        number=3,
        enum=model.Model.ModelType,
    )
    training_type: TrainingType = proto.Field(
        proto.ENUM,
        number=4,
        enum=TrainingType,
    )
    hparam_trials: MutableSequence[model.Model.HparamTuningTrial] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=model.Model.HparamTuningTrial,
    )


class ScriptStatistics(proto.Message):
    r"""Job statistics specific to the child job of a script.

    Attributes:
        evaluation_kind (google.cloud.bigquery_v2.types.ScriptStatistics.EvaluationKind):
            Whether this child job was a statement or
            expression.
        stack_frames (MutableSequence[google.cloud.bigquery_v2.types.ScriptStatistics.ScriptStackFrame]):
            Stack trace showing the line/column/procedure
            name of each frame on the stack at the point
            where the current evaluation happened. The leaf
            frame is first, the primary script is last.
            Never empty.
    """

    class EvaluationKind(proto.Enum):
        r"""Describes how the job is evaluated.

        Values:
            EVALUATION_KIND_UNSPECIFIED (0):
                Default value.
            STATEMENT (1):
                The statement appears directly in the script.
            EXPRESSION (2):
                The statement evaluates an expression that
                appears in the script.
        """
        EVALUATION_KIND_UNSPECIFIED = 0
        STATEMENT = 1
        EXPRESSION = 2

    class ScriptStackFrame(proto.Message):
        r"""Represents the location of the statement/expression being
        evaluated. Line and column numbers are defined as follows:

        - Line and column numbers start with one.  That is, line 1
          column 1 denotes   the start of the script.
        - When inside a stored procedure, all line/column numbers are
          relative   to the procedure body, not the script in which the
          procedure was defined.
        - Start/end positions exclude leading/trailing comments and
          whitespace.   The end position always ends with a ";", when
          present.
        - Multi-byte Unicode characters are treated as just one column.
        - If the original script (or procedure definition) contains TAB
          characters,   a tab "snaps" the indentation forward to the
          nearest multiple of 8   characters, plus 1. For example, a TAB
          on column 1, 2, 3, 4, 5, 6 , or 8   will advance the next
          character to column 9.  A TAB on column 9, 10, 11,   12, 13,
          14, 15, or 16 will advance the next character to column 17.

        Attributes:
            start_line (int):
                Output only. One-based start line.
            start_column (int):
                Output only. One-based start column.
            end_line (int):
                Output only. One-based end line.
            end_column (int):
                Output only. One-based end column.
            procedure_id (str):
                Output only. Name of the active procedure,
                empty if in a top-level script.
            text (str):
                Output only. Text of the current
                statement/expression.
        """

        start_line: int = proto.Field(
            proto.INT32,
            number=1,
        )
        start_column: int = proto.Field(
            proto.INT32,
            number=2,
        )
        end_line: int = proto.Field(
            proto.INT32,
            number=3,
        )
        end_column: int = proto.Field(
            proto.INT32,
            number=4,
        )
        procedure_id: str = proto.Field(
            proto.STRING,
            number=5,
        )
        text: str = proto.Field(
            proto.STRING,
            number=6,
        )

    evaluation_kind: EvaluationKind = proto.Field(
        proto.ENUM,
        number=1,
        enum=EvaluationKind,
    )
    stack_frames: MutableSequence[ScriptStackFrame] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=ScriptStackFrame,
    )


class RowLevelSecurityStatistics(proto.Message):
    r"""Statistics for row-level security.

    Attributes:
        row_level_security_applied (bool):
            Whether any accessed data was protected by
            row access policies.
    """

    row_level_security_applied: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class DataMaskingStatistics(proto.Message):
    r"""Statistics for data-masking.

    Attributes:
        data_masking_applied (bool):
            Whether any accessed data was protected by
            the data masking.
    """

    data_masking_applied: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class JobStatistics(proto.Message):
    r"""Statistics for a single job execution.

    Attributes:
        creation_time (int):
            Output only. Creation time of this job, in
            milliseconds since the epoch. This field will be
            present on all jobs.
        start_time (int):
            Output only. Start time of this job, in
            milliseconds since the epoch. This field will be
            present when the job transitions from the
            PENDING state to either RUNNING or DONE.
        end_time (int):
            Output only. End time of this job, in
            milliseconds since the epoch. This field will be
            present whenever a job is in the DONE state.
        total_bytes_processed (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Total bytes processed for the
            job.
        completion_ratio (google.protobuf.wrappers_pb2.DoubleValue):
            Output only. [TrustedTester] Job progress (0.0 -> 1.0) for
            LOAD and EXTRACT jobs.
        quota_deferments (MutableSequence[str]):
            Output only. Quotas which delayed this job's
            start time.
        query (google.cloud.bigquery_v2.types.JobStatistics2):
            Output only. Statistics for a query job.
        load (google.cloud.bigquery_v2.types.JobStatistics3):
            Output only. Statistics for a load job.
        extract (google.cloud.bigquery_v2.types.JobStatistics4):
            Output only. Statistics for an extract job.
        copy (google.cloud.bigquery_v2.types.CopyJobStatistics):
            Output only. Statistics for a copy job.
        total_slot_ms (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Slot-milliseconds for the job.
        reservation_id (str):
            Output only. Name of the primary reservation
            assigned to this job. Note that this could be
            different than reservations reported in the
            reservation usage field if parent reservations
            were used to execute this job.
        num_child_jobs (int):
            Output only. Number of child jobs executed.
        parent_job_id (str):
            Output only. If this is a child job,
            specifies the job ID of the parent.
        script_statistics (google.cloud.bigquery_v2.types.ScriptStatistics):
            Output only. If this a child job of a script,
            specifies information about the context of this
            job within the script.
        row_level_security_statistics (google.cloud.bigquery_v2.types.RowLevelSecurityStatistics):
            Output only. Statistics for row-level
            security. Present only for query and extract
            jobs.
        data_masking_statistics (google.cloud.bigquery_v2.types.DataMaskingStatistics):
            Output only. Statistics for data-masking.
            Present only for query and extract jobs.
        transaction_info (google.cloud.bigquery_v2.types.JobStatistics.TransactionInfo):
            Output only. [Alpha] Information of the multi-statement
            transaction if this job is part of one.

            This property is only expected on a child job or a job that
            is in a session. A script parent job is not part of the
            transaction started in the script.
        session_info (google.cloud.bigquery_v2.types.SessionInfo):
            Output only. Information of the session if
            this job is part of one.
        final_execution_duration_ms (int):
            Output only. The duration in milliseconds of
            the execution of the final attempt of this job,
            as BigQuery may internally re-attempt to execute
            the job.
        edition (google.cloud.bigquery_v2.types.ReservationEdition):
            Output only. Name of edition corresponding to
            the reservation for this job at the time of this
            update.
    """

    class TransactionInfo(proto.Message):
        r"""[Alpha] Information of a multi-statement transaction.

        Attributes:
            transaction_id (str):
                Output only. [Alpha] Id of the transaction.
        """

        transaction_id: str = proto.Field(
            proto.STRING,
            number=1,
        )

    creation_time: int = proto.Field(
        proto.INT64,
        number=1,
    )
    start_time: int = proto.Field(
        proto.INT64,
        number=2,
    )
    end_time: int = proto.Field(
        proto.INT64,
        number=3,
    )
    total_bytes_processed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.Int64Value,
    )
    completion_ratio: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.DoubleValue,
    )
    quota_deferments: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    query: "JobStatistics2" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="JobStatistics2",
    )
    load: "JobStatistics3" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="JobStatistics3",
    )
    extract: "JobStatistics4" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="JobStatistics4",
    )
    copy: "CopyJobStatistics" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="CopyJobStatistics",
    )
    total_slot_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=10,
        message=wrappers_pb2.Int64Value,
    )
    reservation_id: str = proto.Field(
        proto.STRING,
        number=15,
    )
    num_child_jobs: int = proto.Field(
        proto.INT64,
        number=12,
    )
    parent_job_id: str = proto.Field(
        proto.STRING,
        number=13,
    )
    script_statistics: "ScriptStatistics" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="ScriptStatistics",
    )
    row_level_security_statistics: "RowLevelSecurityStatistics" = proto.Field(
        proto.MESSAGE,
        number=16,
        message="RowLevelSecurityStatistics",
    )
    data_masking_statistics: "DataMaskingStatistics" = proto.Field(
        proto.MESSAGE,
        number=20,
        message="DataMaskingStatistics",
    )
    transaction_info: TransactionInfo = proto.Field(
        proto.MESSAGE,
        number=17,
        message=TransactionInfo,
    )
    session_info: gcb_session_info.SessionInfo = proto.Field(
        proto.MESSAGE,
        number=18,
        message=gcb_session_info.SessionInfo,
    )
    final_execution_duration_ms: int = proto.Field(
        proto.INT64,
        number=22,
    )
    edition: "ReservationEdition" = proto.Field(
        proto.ENUM,
        number=24,
        enum="ReservationEdition",
    )


class DmlStats(proto.Message):
    r"""Detailed statistics for DML statements

    Attributes:
        inserted_row_count (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of inserted Rows.
            Populated by DML INSERT and MERGE statements
        deleted_row_count (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of deleted Rows.
            populated by DML DELETE, MERGE and TRUNCATE
            statements.
        updated_row_count (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of updated Rows.
            Populated by DML UPDATE and MERGE statements.
    """

    inserted_row_count: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.Int64Value,
    )
    deleted_row_count: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    updated_row_count: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.Int64Value,
    )


class PerformanceInsights(proto.Message):
    r"""Performance insights for the job.

    Attributes:
        avg_previous_execution_ms (int):
            Output only. Average execution ms of previous runs.
            Indicates the job ran slow compared to previous executions.
            To find previous executions, use INFORMATION_SCHEMA tables
            and filter jobs with same query hash.
        stage_performance_standalone_insights (MutableSequence[google.cloud.bigquery_v2.types.StagePerformanceStandaloneInsight]):
            Output only. Standalone query stage
            performance insights, for exploring potential
            improvements.
        stage_performance_change_insights (MutableSequence[google.cloud.bigquery_v2.types.StagePerformanceChangeInsight]):
            Output only. Query stage performance insights
            compared to previous runs, for diagnosing
            performance regression.
    """

    avg_previous_execution_ms: int = proto.Field(
        proto.INT64,
        number=1,
    )
    stage_performance_standalone_insights: MutableSequence[
        "StagePerformanceStandaloneInsight"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="StagePerformanceStandaloneInsight",
    )
    stage_performance_change_insights: MutableSequence[
        "StagePerformanceChangeInsight"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="StagePerformanceChangeInsight",
    )


class StagePerformanceChangeInsight(proto.Message):
    r"""Performance insights compared to the previous executions for
    a specific stage.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        stage_id (int):
            Output only. The stage id that the insight
            mapped to.
        input_data_change (google.cloud.bigquery_v2.types.InputDataChange):
            Output only. Input data change insight of the
            query stage.

            This field is a member of `oneof`_ ``_input_data_change``.
    """

    stage_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    input_data_change: "InputDataChange" = proto.Field(
        proto.MESSAGE,
        number=2,
        optional=True,
        message="InputDataChange",
    )


class InputDataChange(proto.Message):
    r"""Details about the input data change insight.

    Attributes:
        records_read_diff_percentage (float):
            Output only. Records read difference
            percentage compared to a previous run.
    """

    records_read_diff_percentage: float = proto.Field(
        proto.FLOAT,
        number=1,
    )


class StagePerformanceStandaloneInsight(proto.Message):
    r"""Standalone performance insights for a specific stage.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        stage_id (int):
            Output only. The stage id that the insight
            mapped to.
        slot_contention (bool):
            Output only. True if the stage has a slot
            contention issue.

            This field is a member of `oneof`_ ``_slot_contention``.
        insufficient_shuffle_quota (bool):
            Output only. True if the stage has
            insufficient shuffle quota.

            This field is a member of `oneof`_ ``_insufficient_shuffle_quota``.
        bi_engine_reasons (MutableSequence[google.cloud.bigquery_v2.types.BiEngineReason]):
            Output only. If present, the stage had the
            following reasons for being disqualified from BI
            Engine execution.
        high_cardinality_joins (MutableSequence[google.cloud.bigquery_v2.types.HighCardinalityJoin]):
            Output only. High cardinality joins in the
            stage.
        partition_skew (google.cloud.bigquery_v2.types.PartitionSkew):
            Output only. Partition skew in the stage.

            This field is a member of `oneof`_ ``_partition_skew``.
    """

    stage_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    slot_contention: bool = proto.Field(
        proto.BOOL,
        number=2,
        optional=True,
    )
    insufficient_shuffle_quota: bool = proto.Field(
        proto.BOOL,
        number=3,
        optional=True,
    )
    bi_engine_reasons: MutableSequence["BiEngineReason"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="BiEngineReason",
    )
    high_cardinality_joins: MutableSequence[
        "HighCardinalityJoin"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="HighCardinalityJoin",
    )
    partition_skew: "PartitionSkew" = proto.Field(
        proto.MESSAGE,
        number=7,
        optional=True,
        message="PartitionSkew",
    )


class HighCardinalityJoin(proto.Message):
    r"""High cardinality join detailed information.

    Attributes:
        left_rows (int):
            Output only. Count of left input rows.
        right_rows (int):
            Output only. Count of right input rows.
        output_rows (int):
            Output only. Count of the output rows.
        step_index (int):
            Output only. The index of the join operator
            in the ExplainQueryStep lists.
    """

    left_rows: int = proto.Field(
        proto.INT64,
        number=1,
    )
    right_rows: int = proto.Field(
        proto.INT64,
        number=2,
    )
    output_rows: int = proto.Field(
        proto.INT64,
        number=3,
    )
    step_index: int = proto.Field(
        proto.INT32,
        number=4,
    )


class PartitionSkew(proto.Message):
    r"""Partition skew detailed information.

    Attributes:
        skew_sources (MutableSequence[google.cloud.bigquery_v2.types.PartitionSkew.SkewSource]):
            Output only. Source stages which produce
            skewed data.
    """

    class SkewSource(proto.Message):
        r"""Details about source stages which produce skewed data.

        Attributes:
            stage_id (int):
                Output only. Stage id of the skew source
                stage.
        """

        stage_id: int = proto.Field(
            proto.INT64,
            number=1,
        )

    skew_sources: MutableSequence[SkewSource] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=SkewSource,
    )


class SparkStatistics(proto.Message):
    r"""Statistics for a BigSpark query.
    Populated as part of JobStatistics2


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        spark_job_id (str):
            Output only. Spark job ID if a Spark job is
            created successfully.

            This field is a member of `oneof`_ ``_spark_job_id``.
        spark_job_location (str):
            Output only. Location where the Spark job is
            executed. A location is selected by BigQueury
            for jobs configured to run in a multi-region.

            This field is a member of `oneof`_ ``_spark_job_location``.
        endpoints (MutableMapping[str, str]):
            Output only. Endpoints returned from Dataproc. Key list:

            -  history_server_endpoint: A link to Spark job UI.
        logging_info (google.cloud.bigquery_v2.types.SparkStatistics.LoggingInfo):
            Output only. Logging info is used to generate
            a link to Cloud Logging.

            This field is a member of `oneof`_ ``_logging_info``.
        kms_key_name (str):
            Output only. The Cloud KMS encryption key that is used to
            protect the resources created by the Spark job. If the Spark
            procedure uses the invoker security mode, the Cloud KMS
            encryption key is either inferred from the provided system
            variable, ``@@spark_proc_properties.kms_key_name``, or the
            default key of the BigQuery job's project (if the CMEK
            organization policy is enforced). Otherwise, the Cloud KMS
            key is either inferred from the Spark connection associated
            with the procedure (if it is provided), or from the default
            key of the Spark connection's project if the CMEK
            organization policy is enforced.

            Example:

            -  ``projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key]``

            This field is a member of `oneof`_ ``_kms_key_name``.
        gcs_staging_bucket (str):
            Output only. The Google Cloud Storage bucket that is used as
            the default file system by the Spark application. This field
            is only filled when the Spark procedure uses the invoker
            security mode. The ``gcsStagingBucket`` bucket is inferred
            from the ``@@spark_proc_properties.staging_bucket`` system
            variable (if it is provided). Otherwise, BigQuery creates a
            default staging bucket for the job and returns the bucket
            name in this field.

            Example:

            -  ``gs://[bucket_name]``

            This field is a member of `oneof`_ ``_gcs_staging_bucket``.
    """

    class LoggingInfo(proto.Message):
        r"""Spark job logs can be filtered by these fields in Cloud
        Logging.

        Attributes:
            resource_type (str):
                Output only. Resource type used for logging.
            project_id (str):
                Output only. Project ID where the Spark logs
                were written.
        """

        resource_type: str = proto.Field(
            proto.STRING,
            number=1,
        )
        project_id: str = proto.Field(
            proto.STRING,
            number=2,
        )

    spark_job_id: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    spark_job_location: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    endpoints: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )
    logging_info: LoggingInfo = proto.Field(
        proto.MESSAGE,
        number=4,
        optional=True,
        message=LoggingInfo,
    )
    kms_key_name: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )
    gcs_staging_bucket: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )


class MaterializedViewStatistics(proto.Message):
    r"""Statistics of materialized views considered in a query job.

    Attributes:
        materialized_view (MutableSequence[google.cloud.bigquery_v2.types.MaterializedView]):
            Materialized views considered for the query
            job. Only certain materialized views are used.
            For a detailed list, see the child message.

            If many materialized views are considered, then
            the list might be incomplete.
    """

    materialized_view: MutableSequence["MaterializedView"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="MaterializedView",
    )


class MaterializedView(proto.Message):
    r"""A materialized view considered for a query job.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        table_reference (google.cloud.bigquery_v2.types.TableReference):
            The candidate materialized view.

            This field is a member of `oneof`_ ``_table_reference``.
        chosen (bool):
            Whether the materialized view is chosen for
            the query.
            A materialized view can be chosen to rewrite
            multiple parts of the same query. If a
            materialized view is chosen to rewrite any part
            of the query, then this field is true, even if
            the materialized view was not chosen to rewrite
            others parts.

            This field is a member of `oneof`_ ``_chosen``.
        estimated_bytes_saved (int):
            If present, specifies a best-effort
            estimation of the bytes saved by using the
            materialized view rather than its base tables.

            This field is a member of `oneof`_ ``_estimated_bytes_saved``.
        rejected_reason (google.cloud.bigquery_v2.types.MaterializedView.RejectedReason):
            If present, specifies the reason why the
            materialized view was not chosen for the query.

            This field is a member of `oneof`_ ``_rejected_reason``.
    """

    class RejectedReason(proto.Enum):
        r"""Reason why a materialized view was not chosen for a query. For more
        information, see `Understand why materialized views were
        rejected <https://cloud.google.com/bigquery/docs/materialized-views-use#understand-rejected>`__.

        Values:
            REJECTED_REASON_UNSPECIFIED (0):
                Default unspecified value.
            NO_DATA (1):
                View has no cached data because it has not
                refreshed yet.
            COST (2):
                The estimated cost of the view is more
                expensive than another view or the base table.

                Note: The estimate cost might not match the
                billed cost.
            BASE_TABLE_TRUNCATED (3):
                View has no cached data because a base table
                is truncated.
            BASE_TABLE_DATA_CHANGE (4):
                View is invalidated because of a data change in one or more
                base tables. It could be any recent change if the
                ```maxStaleness`` <https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#Table.FIELDS.max_staleness>`__
                option is not set for the view, or otherwise any change
                outside of the staleness window.
            BASE_TABLE_PARTITION_EXPIRATION_CHANGE (5):
                View is invalidated because a base table's
                partition expiration has changed.
            BASE_TABLE_EXPIRED_PARTITION (6):
                View is invalidated because a base table's
                partition has expired.
            BASE_TABLE_INCOMPATIBLE_METADATA_CHANGE (7):
                View is invalidated because a base table has
                an incompatible metadata change.
            TIME_ZONE (8):
                View is invalidated because it was refreshed
                with a time zone other than that of the current
                job.
            OUT_OF_TIME_TRAVEL_WINDOW (9):
                View is outside the time travel window.
            BASE_TABLE_FINE_GRAINED_SECURITY_POLICY (10):
                View is inaccessible to the user because of a
                fine-grained security policy on one of its base
                tables.
            BASE_TABLE_TOO_STALE (11):
                One of the view's base tables is too stale.
                For example, the cached metadata of a BigLake
                external table needs to be updated.
        """
        REJECTED_REASON_UNSPECIFIED = 0
        NO_DATA = 1
        COST = 2
        BASE_TABLE_TRUNCATED = 3
        BASE_TABLE_DATA_CHANGE = 4
        BASE_TABLE_PARTITION_EXPIRATION_CHANGE = 5
        BASE_TABLE_EXPIRED_PARTITION = 6
        BASE_TABLE_INCOMPATIBLE_METADATA_CHANGE = 7
        TIME_ZONE = 8
        OUT_OF_TIME_TRAVEL_WINDOW = 9
        BASE_TABLE_FINE_GRAINED_SECURITY_POLICY = 10
        BASE_TABLE_TOO_STALE = 11

    table_reference: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=1,
        optional=True,
        message=gcb_table_reference.TableReference,
    )
    chosen: bool = proto.Field(
        proto.BOOL,
        number=2,
        optional=True,
    )
    estimated_bytes_saved: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    rejected_reason: RejectedReason = proto.Field(
        proto.ENUM,
        number=4,
        optional=True,
        enum=RejectedReason,
    )


class TableMetadataCacheUsage(proto.Message):
    r"""Table level detail on the usage of metadata caching. Only set
    for Metadata caching eligible tables referenced in the query.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        table_reference (google.cloud.bigquery_v2.types.TableReference):
            Metadata caching eligible table referenced in
            the query.

            This field is a member of `oneof`_ ``_table_reference``.
        unused_reason (google.cloud.bigquery_v2.types.TableMetadataCacheUsage.UnusedReason):
            Reason for not using metadata caching for the
            table.

            This field is a member of `oneof`_ ``_unused_reason``.
        explanation (str):
            Free form human-readable reason metadata
            caching was unused for the job.

            This field is a member of `oneof`_ ``_explanation``.
        staleness (google.protobuf.duration_pb2.Duration):
            Duration since last refresh as of this job
            for managed tables (indicates metadata cache
            staleness as seen by this job).
        table_type (str):
            `Table
            type <https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#Table.FIELDS.type>`__.
    """

    class UnusedReason(proto.Enum):
        r"""Reasons for not using metadata caching.

        Values:
            UNUSED_REASON_UNSPECIFIED (0):
                Unused reasons not specified.
            EXCEEDED_MAX_STALENESS (1):
                Metadata cache was outside the table's
                maxStaleness.
            METADATA_CACHING_NOT_ENABLED (3):
                Metadata caching feature is not enabled. [Update BigLake
                tables]
                (/bigquery/docs/create-cloud-storage-table-biglake#update-biglake-tables)
                to enable the metadata caching.
            OTHER_REASON (2):
                Other unknown reason.
        """
        UNUSED_REASON_UNSPECIFIED = 0
        EXCEEDED_MAX_STALENESS = 1
        METADATA_CACHING_NOT_ENABLED = 3
        OTHER_REASON = 2

    table_reference: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=1,
        optional=True,
        message=gcb_table_reference.TableReference,
    )
    unused_reason: UnusedReason = proto.Field(
        proto.ENUM,
        number=2,
        optional=True,
        enum=UnusedReason,
    )
    explanation: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    staleness: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=5,
        message=duration_pb2.Duration,
    )
    table_type: str = proto.Field(
        proto.STRING,
        number=6,
    )


class MetadataCacheStatistics(proto.Message):
    r"""Statistics for metadata caching in queried tables.

    Attributes:
        table_metadata_cache_usage (MutableSequence[google.cloud.bigquery_v2.types.TableMetadataCacheUsage]):
            Set for the Metadata caching eligible tables
            referenced in the query.
    """

    table_metadata_cache_usage: MutableSequence[
        "TableMetadataCacheUsage"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TableMetadataCacheUsage",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
