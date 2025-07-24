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

from google.cloud.bigquery_v2.types import biglake_config
from google.cloud.bigquery_v2.types import clustering as gcb_clustering
from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import error
from google.cloud.bigquery_v2.types import (
    external_catalog_table_options as gcb_external_catalog_table_options,
)
from google.cloud.bigquery_v2.types import external_data_config
from google.cloud.bigquery_v2.types import managed_table_type as gcb_managed_table_type
from google.cloud.bigquery_v2.types import partitioning_definition
from google.cloud.bigquery_v2.types import privacy_policy as gcb_privacy_policy
from google.cloud.bigquery_v2.types import range_partitioning as gcb_range_partitioning
from google.cloud.bigquery_v2.types import restriction_config
from google.cloud.bigquery_v2.types import table_constraints as gcb_table_constraints
from google.cloud.bigquery_v2.types import table_reference as gcb_table_reference
from google.cloud.bigquery_v2.types import table_schema
from google.cloud.bigquery_v2.types import time_partitioning as gcb_time_partitioning
from google.cloud.bigquery_v2.types import udf_resource
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "TableReplicationInfo",
        "ViewDefinition",
        "ForeignViewDefinition",
        "MaterializedViewDefinition",
        "MaterializedViewStatus",
        "SnapshotDefinition",
        "CloneDefinition",
        "Streamingbuffer",
        "Table",
        "GetTableRequest",
        "InsertTableRequest",
        "UpdateOrPatchTableRequest",
        "DeleteTableRequest",
        "ListTablesRequest",
        "ListFormatView",
        "ListFormatTable",
        "TableList",
    },
)


class TableReplicationInfo(proto.Message):
    r"""Replication info of a table created using ``AS REPLICA`` DDL like:
    ``CREATE MATERIALIZED VIEW mv1 AS REPLICA OF src_mv``

    Attributes:
        source_table (google.cloud.bigquery_v2.types.TableReference):
            Required. Source table reference that is
            replicated.
        replication_interval_ms (int):
            Optional. Specifies the interval at which the
            source table is polled for updates.
            It's Optional. If not specified, default
            replication interval would be applied.
        replicated_source_last_refresh_time (int):
            Optional. Output only. If source is a
            materialized view, this field signifies the last
            refresh time of the source.
        replication_status (google.cloud.bigquery_v2.types.TableReplicationInfo.ReplicationStatus):
            Optional. Output only. Replication status of
            configured replication.
        replication_error (google.cloud.bigquery_v2.types.ErrorProto):
            Optional. Output only. Replication error that
            will permanently stopped table replication.
    """

    class ReplicationStatus(proto.Enum):
        r"""Replication status of the table created using ``AS REPLICA`` like:
        ``CREATE MATERIALIZED VIEW mv1 AS REPLICA OF src_mv``

        Values:
            REPLICATION_STATUS_UNSPECIFIED (0):
                Default value.
            ACTIVE (1):
                Replication is Active with no errors.
            SOURCE_DELETED (2):
                Source object is deleted.
            PERMISSION_DENIED (3):
                Source revoked replication permissions.
            UNSUPPORTED_CONFIGURATION (4):
                Source configuration doesn’t allow
                replication.
        """
        REPLICATION_STATUS_UNSPECIFIED = 0
        ACTIVE = 1
        SOURCE_DELETED = 2
        PERMISSION_DENIED = 3
        UNSUPPORTED_CONFIGURATION = 4

    source_table: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcb_table_reference.TableReference,
    )
    replication_interval_ms: int = proto.Field(
        proto.INT64,
        number=2,
    )
    replicated_source_last_refresh_time: int = proto.Field(
        proto.INT64,
        number=3,
    )
    replication_status: ReplicationStatus = proto.Field(
        proto.ENUM,
        number=4,
        enum=ReplicationStatus,
    )
    replication_error: error.ErrorProto = proto.Field(
        proto.MESSAGE,
        number=5,
        message=error.ErrorProto,
    )


class ViewDefinition(proto.Message):
    r"""Describes the definition of a logical view.

    Attributes:
        query (str):
            Required. A query that BigQuery executes when
            the view is referenced.
        user_defined_function_resources (MutableSequence[google.cloud.bigquery_v2.types.UserDefinedFunctionResource]):
            Describes user-defined function resources
            used in the query.
        use_legacy_sql (google.protobuf.wrappers_pb2.BoolValue):
            Specifies whether to use BigQuery's legacy
            SQL for this view. The default value is true. If
            set to false, the view will use BigQuery's
            GoogleSQL:

            https://cloud.google.com/bigquery/sql-reference/

            Queries and views that reference this view must
            use the same flag value. A wrapper is used here
            because the default value is True.
        use_explicit_column_names (bool):
            True if the column names are explicitly
            specified. For example by using the 'CREATE VIEW
            v(c1, c2) AS ...' syntax. Can only be set for
            GoogleSQL views.
        privacy_policy (google.cloud.bigquery_v2.types.PrivacyPolicy):
            Optional. Specifies the privacy policy for
            the view.
        foreign_definitions (MutableSequence[google.cloud.bigquery_v2.types.ForeignViewDefinition]):
            Optional. Foreign view representations.
    """

    query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    user_defined_function_resources: MutableSequence[
        udf_resource.UserDefinedFunctionResource
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=udf_resource.UserDefinedFunctionResource,
    )
    use_legacy_sql: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.BoolValue,
    )
    use_explicit_column_names: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    privacy_policy: gcb_privacy_policy.PrivacyPolicy = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gcb_privacy_policy.PrivacyPolicy,
    )
    foreign_definitions: MutableSequence["ForeignViewDefinition"] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="ForeignViewDefinition",
    )


class ForeignViewDefinition(proto.Message):
    r"""A view can be represented in multiple ways. Each
    representation has its own dialect. This message stores the
    metadata required for these representations.

    Attributes:
        query (str):
            Required. The query that defines the view.
        dialect (str):
            Optional. Represents the dialect of the
            query.
    """

    query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dialect: str = proto.Field(
        proto.STRING,
        number=7,
    )


class MaterializedViewDefinition(proto.Message):
    r"""Definition and configuration of a materialized view.

    Attributes:
        query (str):
            Required. A query whose results are
            persisted.
        last_refresh_time (int):
            Output only. The time when this materialized
            view was last refreshed, in milliseconds since
            the epoch.
        enable_refresh (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Enable automatic refresh of the
            materialized view when the base table is
            updated. The default value is "true".
        refresh_interval_ms (google.protobuf.wrappers_pb2.UInt64Value):
            Optional. The maximum frequency at which this
            materialized view will be refreshed. The default
            value is "1800000" (30 minutes).
        allow_non_incremental_definition (google.protobuf.wrappers_pb2.BoolValue):
            Optional. This option declares the intention to construct a
            materialized view that isn't refreshed incrementally.
            Non-incremental materialized views support an expanded range
            of SQL queries. The ``allow_non_incremental_definition``
            option can't be changed after the materialized view is
            created.
    """

    query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    last_refresh_time: int = proto.Field(
        proto.INT64,
        number=2,
    )
    enable_refresh: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.BoolValue,
    )
    refresh_interval_ms: wrappers_pb2.UInt64Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.UInt64Value,
    )
    allow_non_incremental_definition: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.BoolValue,
    )


class MaterializedViewStatus(proto.Message):
    r"""Status of a materialized view.
    The last refresh timestamp status is omitted here, but is
    present in the MaterializedViewDefinition message.

    Attributes:
        refresh_watermark (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Refresh watermark of
            materialized view. The base tables' data were
            collected into the materialized view cache until
            this time.
        last_refresh_status (google.cloud.bigquery_v2.types.ErrorProto):
            Output only. Error result of the last
            automatic refresh. If present, indicates that
            the last automatic refresh was unsuccessful.
    """

    refresh_watermark: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    last_refresh_status: error.ErrorProto = proto.Field(
        proto.MESSAGE,
        number=2,
        message=error.ErrorProto,
    )


class SnapshotDefinition(proto.Message):
    r"""Information about base table and snapshot time of the
    snapshot.

    Attributes:
        base_table_reference (google.cloud.bigquery_v2.types.TableReference):
            Required. Reference describing the ID of the
            table that was snapshot.
        snapshot_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. The time at which the base table
            was snapshot. This value is reported in the JSON
            response using RFC3339 format.
    """

    base_table_reference: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcb_table_reference.TableReference,
    )
    snapshot_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class CloneDefinition(proto.Message):
    r"""Information about base table and clone time of a table clone.

    Attributes:
        base_table_reference (google.cloud.bigquery_v2.types.TableReference):
            Required. Reference describing the ID of the
            table that was cloned.
        clone_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. The time at which the base table
            was cloned. This value is reported in the JSON
            response using RFC3339 format.
    """

    base_table_reference: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcb_table_reference.TableReference,
    )
    clone_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class Streamingbuffer(proto.Message):
    r"""

    Attributes:
        estimated_bytes (int):
            Output only. A lower-bound estimate of the
            number of bytes currently in the streaming
            buffer.
        estimated_rows (int):
            Output only. A lower-bound estimate of the
            number of rows currently in the streaming
            buffer.
        oldest_entry_time (int):
            Output only. Contains the timestamp of the
            oldest entry in the streaming buffer, in
            milliseconds since the epoch, if the streaming
            buffer is available.
    """

    estimated_bytes: int = proto.Field(
        proto.UINT64,
        number=1,
    )
    estimated_rows: int = proto.Field(
        proto.UINT64,
        number=2,
    )
    oldest_entry_time: int = proto.Field(
        proto.FIXED64,
        number=3,
    )


class Table(proto.Message):
    r"""

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        kind (str):
            The type of resource ID.
        etag (str):
            Output only. A hash of this resource.
        id (str):
            Output only. An opaque ID uniquely
            identifying the table.
        self_link (str):
            Output only. A URL that can be used to access
            this resource again.
        table_reference (google.cloud.bigquery_v2.types.TableReference):
            Required. Reference describing the ID of this
            table.
        friendly_name (google.protobuf.wrappers_pb2.StringValue):
            Optional. A descriptive name for this table.
        description (google.protobuf.wrappers_pb2.StringValue):
            Optional. A user-friendly description of this
            table.
        labels (MutableMapping[str, str]):
            The labels associated with this table. You
            can use these to organize and group your tables.
            Label keys and values can be no longer than 63
            characters, can only contain lowercase letters,
            numeric characters, underscores and dashes.
            International characters are allowed. Label
            values are optional. Label keys must start with
            a letter and each label in the list must have a
            different key.
        schema (google.cloud.bigquery_v2.types.TableSchema):
            Optional. Describes the schema of this table.
        time_partitioning (google.cloud.bigquery_v2.types.TimePartitioning):
            If specified, configures time-based
            partitioning for this table.
        range_partitioning (google.cloud.bigquery_v2.types.RangePartitioning):
            If specified, configures range partitioning
            for this table.
        clustering (google.cloud.bigquery_v2.types.Clustering):
            Clustering specification for the table. Must
            be specified with time-based partitioning, data
            in the table will be first partitioned and
            subsequently clustered.
        require_partition_filter (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If set to true, queries over this
            table require a partition filter that can be
            used for partition elimination to be specified.
        partition_definition (google.cloud.bigquery_v2.types.PartitioningDefinition):
            Optional. The partition information for all
            table formats, including managed partitioned
            tables, hive partitioned tables, iceberg
            partitioned, and metastore partitioned tables.
            This field is only populated for metastore
            partitioned tables. For other table formats,
            this is an output only field.

            This field is a member of `oneof`_ ``_partition_definition``.
        num_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The size of this table in
            logical bytes, excluding any data in the
            streaming buffer.
        num_physical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The physical size of this table
            in bytes. This includes storage used for time
            travel.
        num_long_term_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of logical bytes in
            the table that are considered "long-term
            storage".
        num_rows (google.protobuf.wrappers_pb2.UInt64Value):
            Output only. The number of rows of data in
            this table, excluding any data in the streaming
            buffer.
        creation_time (int):
            Output only. The time when this table was
            created, in milliseconds since the epoch.
        expiration_time (google.protobuf.wrappers_pb2.Int64Value):
            Optional. The time when this table expires,
            in milliseconds since the epoch. If not present,
            the table will persist indefinitely. Expired
            tables will be deleted and their storage
            reclaimed.  The defaultTableExpirationMs
            property of the encapsulating dataset can be
            used to set a default expirationTime on newly
            created tables.
        last_modified_time (int):
            Output only. The time when this table was
            last modified, in milliseconds since the epoch.
        type_ (str):
            Output only. Describes the table type. The following values
            are supported:

            -  ``TABLE``: A normal BigQuery table.
            -  ``VIEW``: A virtual table defined by a SQL query.
            -  ``EXTERNAL``: A table that references data stored in an
               external storage system, such as Google Cloud Storage.
            -  ``MATERIALIZED_VIEW``: A precomputed view defined by a
               SQL query.
            -  ``SNAPSHOT``: An immutable BigQuery table that preserves
               the contents of a base table at a particular time. See
               additional information on `table
               snapshots <https://cloud.google.com/bigquery/docs/table-snapshots-intro>`__.

            The default value is ``TABLE``.
        view (google.cloud.bigquery_v2.types.ViewDefinition):
            Optional. The view definition.
        materialized_view (google.cloud.bigquery_v2.types.MaterializedViewDefinition):
            Optional. The materialized view definition.
        materialized_view_status (google.cloud.bigquery_v2.types.MaterializedViewStatus):
            Output only. The materialized view status.
        external_data_configuration (google.cloud.bigquery_v2.types.ExternalDataConfiguration):
            Optional. Describes the data format,
            location, and other properties of a table stored
            outside of BigQuery. By defining these
            properties, the data source can then be queried
            as if it were a standard BigQuery table.
        biglake_configuration (google.cloud.bigquery_v2.types.BigLakeConfiguration):
            Optional. Specifies the configuration of a
            BigQuery table for Apache Iceberg.
        managed_table_type (google.cloud.bigquery_v2.types.ManagedTableType):
            Optional. If set, overrides the default
            managed table type configured in the dataset.
        location (str):
            Output only. The geographic location where
            the table resides. This value is inherited from
            the dataset.
        streaming_buffer (google.cloud.bigquery_v2.types.Streamingbuffer):
            Output only. Contains information regarding
            this table's streaming buffer, if one is
            present. This field will be absent if the table
            is not being streamed to or if there is no data
            in the streaming buffer.
        encryption_configuration (google.cloud.bigquery_v2.types.EncryptionConfiguration):
            Custom encryption configuration (e.g., Cloud
            KMS keys).
        snapshot_definition (google.cloud.bigquery_v2.types.SnapshotDefinition):
            Output only. Contains information about the
            snapshot. This value is set via snapshot
            creation.
        default_collation (google.protobuf.wrappers_pb2.StringValue):
            Optional. Defines the default collation specification of new
            STRING fields in the table. During table creation or update,
            if a STRING field is added to this table without explicit
            collation specified, then the table inherits the table
            default collation. A change to this field affects only
            fields added afterwards, and does not alter the existing
            fields. The following values are supported:

            -  'und:ci': undetermined locale, case insensitive.
            -  '': empty string. Default to case-sensitive behavior.
        default_rounding_mode (google.cloud.bigquery_v2.types.TableFieldSchema.RoundingMode):
            Optional. Defines the default rounding mode
            specification of new decimal fields (NUMERIC OR
            BIGNUMERIC) in the table. During table creation
            or update, if a decimal field is added to this
            table without an explicit rounding mode
            specified, then the field inherits the table
            default rounding mode. Changing this field
            doesn't affect existing fields.
        clone_definition (google.cloud.bigquery_v2.types.CloneDefinition):
            Output only. Contains information about the
            clone. This value is set via the clone
            operation.
        num_time_travel_physical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of physical bytes used by
            time travel storage (deleted or changed data).
            This data is not kept in real time, and might be
            delayed by a few seconds to a few minutes.
        num_total_logical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Total number of logical bytes in
            the table or materialized view.
        num_active_logical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of logical bytes that are
            less than 90 days old.
        num_long_term_logical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of logical bytes that are
            more than 90 days old.
        num_current_physical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of physical bytes used by
            current live data storage. This data is not kept
            in real time, and might be delayed by a few
            seconds to a few minutes.
        num_total_physical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The physical size of this table
            in bytes. This also includes storage used for
            time travel. This data is not kept in real time,
            and might be delayed by a few seconds to a few
            minutes.
        num_active_physical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of physical bytes less
            than 90 days old. This data is not kept in real
            time, and might be delayed by a few seconds to a
            few minutes.
        num_long_term_physical_bytes (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Number of physical bytes more
            than 90 days old. This data is not kept in real
            time, and might be delayed by a few seconds to a
            few minutes.
        num_partitions (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of partitions present
            in the table or materialized view. This data is
            not kept in real time, and might be delayed by a
            few seconds to a few minutes.
        max_staleness (str):
            Optional. The maximum staleness of data that
            could be returned when the table (or stale MV)
            is queried. Staleness encoded as a string
            encoding of sql IntervalValue type.
        restrictions (google.cloud.bigquery_v2.types.RestrictionConfig):
            Optional. Output only. Restriction config for table. If set,
            restrict certain accesses on the table based on the config.
            See `Data
            egress <https://cloud.google.com/bigquery/docs/analytics-hub-introduction#data_egress>`__
            for more details.
        table_constraints (google.cloud.bigquery_v2.types.TableConstraints):
            Optional. Tables Primary Key and Foreign Key
            information
        resource_tags (MutableMapping[str, str]):
            Optional. The
            `tags <https://cloud.google.com/bigquery/docs/tags>`__
            attached to this table. Tag keys are globally unique. Tag
            key is expected to be in the namespaced format, for example
            "123456789012/environment" where 123456789012 is the ID of
            the parent organization or project resource for this tag
            key. Tag value is expected to be the short name, for example
            "Production". See `Tag
            definitions <https://cloud.google.com/iam/docs/tags-access-control#definitions>`__
            for more details.
        table_replication_info (google.cloud.bigquery_v2.types.TableReplicationInfo):
            Optional. Table replication info for table created
            ``AS REPLICA`` DDL like:
            ``CREATE MATERIALIZED VIEW mv1 AS REPLICA OF src_mv``
        replicas (MutableSequence[google.cloud.bigquery_v2.types.TableReference]):
            Optional. Output only. Table references of
            all replicas currently active on the table.
        external_catalog_table_options (google.cloud.bigquery_v2.types.ExternalCatalogTableOptions):
            Optional. Options defining open source
            compatible table.
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
    table_reference: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gcb_table_reference.TableReference,
    )
    friendly_name: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.StringValue,
    )
    description: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.StringValue,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
    )
    schema: table_schema.TableSchema = proto.Field(
        proto.MESSAGE,
        number=9,
        message=table_schema.TableSchema,
    )
    time_partitioning: gcb_time_partitioning.TimePartitioning = proto.Field(
        proto.MESSAGE,
        number=10,
        message=gcb_time_partitioning.TimePartitioning,
    )
    range_partitioning: gcb_range_partitioning.RangePartitioning = proto.Field(
        proto.MESSAGE,
        number=27,
        message=gcb_range_partitioning.RangePartitioning,
    )
    clustering: gcb_clustering.Clustering = proto.Field(
        proto.MESSAGE,
        number=23,
        message=gcb_clustering.Clustering,
    )
    require_partition_filter: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=28,
        message=wrappers_pb2.BoolValue,
    )
    partition_definition: partitioning_definition.PartitioningDefinition = proto.Field(
        proto.MESSAGE,
        number=51,
        optional=True,
        message=partitioning_definition.PartitioningDefinition,
    )
    num_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=11,
        message=wrappers_pb2.Int64Value,
    )
    num_physical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=26,
        message=wrappers_pb2.Int64Value,
    )
    num_long_term_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=12,
        message=wrappers_pb2.Int64Value,
    )
    num_rows: wrappers_pb2.UInt64Value = proto.Field(
        proto.MESSAGE,
        number=13,
        message=wrappers_pb2.UInt64Value,
    )
    creation_time: int = proto.Field(
        proto.INT64,
        number=14,
    )
    expiration_time: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=15,
        message=wrappers_pb2.Int64Value,
    )
    last_modified_time: int = proto.Field(
        proto.FIXED64,
        number=16,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=17,
    )
    view: "ViewDefinition" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="ViewDefinition",
    )
    materialized_view: "MaterializedViewDefinition" = proto.Field(
        proto.MESSAGE,
        number=25,
        message="MaterializedViewDefinition",
    )
    materialized_view_status: "MaterializedViewStatus" = proto.Field(
        proto.MESSAGE,
        number=42,
        message="MaterializedViewStatus",
    )
    external_data_configuration: external_data_config.ExternalDataConfiguration = (
        proto.Field(
            proto.MESSAGE,
            number=19,
            message=external_data_config.ExternalDataConfiguration,
        )
    )
    biglake_configuration: biglake_config.BigLakeConfiguration = proto.Field(
        proto.MESSAGE,
        number=45,
        message=biglake_config.BigLakeConfiguration,
    )
    managed_table_type: gcb_managed_table_type.ManagedTableType = proto.Field(
        proto.ENUM,
        number=55,
        enum=gcb_managed_table_type.ManagedTableType,
    )
    location: str = proto.Field(
        proto.STRING,
        number=20,
    )
    streaming_buffer: "Streamingbuffer" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="Streamingbuffer",
    )
    encryption_configuration: encryption_config.EncryptionConfiguration = proto.Field(
        proto.MESSAGE,
        number=22,
        message=encryption_config.EncryptionConfiguration,
    )
    snapshot_definition: "SnapshotDefinition" = proto.Field(
        proto.MESSAGE,
        number=29,
        message="SnapshotDefinition",
    )
    default_collation: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=30,
        message=wrappers_pb2.StringValue,
    )
    default_rounding_mode: table_schema.TableFieldSchema.RoundingMode = proto.Field(
        proto.ENUM,
        number=44,
        enum=table_schema.TableFieldSchema.RoundingMode,
    )
    clone_definition: "CloneDefinition" = proto.Field(
        proto.MESSAGE,
        number=31,
        message="CloneDefinition",
    )
    num_time_travel_physical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=33,
        message=wrappers_pb2.Int64Value,
    )
    num_total_logical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=34,
        message=wrappers_pb2.Int64Value,
    )
    num_active_logical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=35,
        message=wrappers_pb2.Int64Value,
    )
    num_long_term_logical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=36,
        message=wrappers_pb2.Int64Value,
    )
    num_current_physical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=53,
        message=wrappers_pb2.Int64Value,
    )
    num_total_physical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=37,
        message=wrappers_pb2.Int64Value,
    )
    num_active_physical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=38,
        message=wrappers_pb2.Int64Value,
    )
    num_long_term_physical_bytes: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=39,
        message=wrappers_pb2.Int64Value,
    )
    num_partitions: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=40,
        message=wrappers_pb2.Int64Value,
    )
    max_staleness: str = proto.Field(
        proto.STRING,
        number=41,
    )
    restrictions: restriction_config.RestrictionConfig = proto.Field(
        proto.MESSAGE,
        number=46,
        message=restriction_config.RestrictionConfig,
    )
    table_constraints: gcb_table_constraints.TableConstraints = proto.Field(
        proto.MESSAGE,
        number=47,
        message=gcb_table_constraints.TableConstraints,
    )
    resource_tags: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=48,
    )
    table_replication_info: "TableReplicationInfo" = proto.Field(
        proto.MESSAGE,
        number=49,
        message="TableReplicationInfo",
    )
    replicas: MutableSequence[gcb_table_reference.TableReference] = proto.RepeatedField(
        proto.MESSAGE,
        number=50,
        message=gcb_table_reference.TableReference,
    )
    external_catalog_table_options: gcb_external_catalog_table_options.ExternalCatalogTableOptions = proto.Field(
        proto.MESSAGE,
        number=54,
        message=gcb_external_catalog_table_options.ExternalCatalogTableOptions,
    )


class GetTableRequest(proto.Message):
    r"""Request format for getting table metadata.

    Attributes:
        project_id (str):
            Required. Project ID of the requested table
        dataset_id (str):
            Required. Dataset ID of the requested table
        table_id (str):
            Required. Table ID of the requested table
        selected_fields (str):
            List of table schema fields to return (comma-separated). If
            unspecified, all fields are returned. A fieldMask cannot be
            used here because the fields will automatically be converted
            from camelCase to snake_case and the conversion will fail if
            there are underscores. Since these are fields in BigQuery
            table schemas, underscores are allowed.
        view (google.cloud.bigquery_v2.types.GetTableRequest.TableMetadataView):
            Optional. Specifies the view that determines which table
            information is returned. By default, basic table information
            and storage statistics (STORAGE_STATS) are returned.
    """

    class TableMetadataView(proto.Enum):
        r"""TableMetadataView specifies which table information is
        returned.

        Values:
            TABLE_METADATA_VIEW_UNSPECIFIED (0):
                The default value. Default to the STORAGE_STATS view.
            BASIC (1):
                Includes basic table information including
                schema and partitioning specification. This view
                does not include storage statistics such as
                numRows or numBytes. This view is significantly
                more efficient and should be used to support
                high query rates.
            STORAGE_STATS (2):
                Includes all information in the BASIC view as
                well as storage statistics (numBytes,
                numLongTermBytes, numRows and lastModifiedTime).
            FULL (3):
                Includes all table information, including storage
                statistics. It returns same information as STORAGE_STATS
                view, but may contain additional information in the future.
        """
        TABLE_METADATA_VIEW_UNSPECIFIED = 0
        BASIC = 1
        STORAGE_STATS = 2
        FULL = 3

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    selected_fields: str = proto.Field(
        proto.STRING,
        number=4,
    )
    view: TableMetadataView = proto.Field(
        proto.ENUM,
        number=5,
        enum=TableMetadataView,
    )


class InsertTableRequest(proto.Message):
    r"""Request format for inserting table metadata.

    Attributes:
        project_id (str):
            Required. Project ID of the new table
        dataset_id (str):
            Required. Dataset ID of the new table
        table (google.cloud.bigquery_v2.types.Table):
            Required. A tables resource to insert
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table: "Table" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Table",
    )


class UpdateOrPatchTableRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the table to update
        dataset_id (str):
            Required. Dataset ID of the table to update
        table_id (str):
            Required. Table ID of the table to update
        table (google.cloud.bigquery_v2.types.Table):
            Required. A tables resource which will
            replace or patch the specified table
        autodetect_schema (bool):
            Optional. When true will autodetect schema,
            else will keep original schema.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    table: "Table" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Table",
    )
    autodetect_schema: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class DeleteTableRequest(proto.Message):
    r"""Request format for deleting a table.

    Attributes:
        project_id (str):
            Required. Project ID of the table to delete
        dataset_id (str):
            Required. Dataset ID of the table to delete
        table_id (str):
            Required. Table ID of the table to delete
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListTablesRequest(proto.Message):
    r"""Request format for enumerating tables.

    Attributes:
        project_id (str):
            Required. Project ID of the tables to list
        dataset_id (str):
            Required. Dataset ID of the tables to list
        max_results (google.protobuf.wrappers_pb2.UInt32Value):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    max_results: wrappers_pb2.UInt32Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.UInt32Value,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListFormatView(proto.Message):
    r"""Information about a logical view.

    Attributes:
        use_legacy_sql (google.protobuf.wrappers_pb2.BoolValue):
            True if view is defined in legacy SQL
            dialect, false if in GoogleSQL.
        privacy_policy (google.cloud.bigquery_v2.types.PrivacyPolicy):
            Specifies the privacy policy for the view.
    """

    use_legacy_sql: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.BoolValue,
    )
    privacy_policy: gcb_privacy_policy.PrivacyPolicy = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcb_privacy_policy.PrivacyPolicy,
    )


class ListFormatTable(proto.Message):
    r"""

    Attributes:
        kind (str):
            The resource type.
        id (str):
            An opaque ID of the table.
        table_reference (google.cloud.bigquery_v2.types.TableReference):
            A reference uniquely identifying table.
        friendly_name (google.protobuf.wrappers_pb2.StringValue):
            The user-friendly name for this table.
        type_ (str):
            The type of table.
        time_partitioning (google.cloud.bigquery_v2.types.TimePartitioning):
            The time-based partitioning for this table.
        range_partitioning (google.cloud.bigquery_v2.types.RangePartitioning):
            The range partitioning for this table.
        clustering (google.cloud.bigquery_v2.types.Clustering):
            Clustering specification for this table, if
            configured.
        labels (MutableMapping[str, str]):
            The labels associated with this table. You
            can use these to organize and group your tables.
        view (google.cloud.bigquery_v2.types.ListFormatView):
            Additional details for a view.
        creation_time (int):
            Output only. The time when this table was
            created, in milliseconds since the epoch.
        expiration_time (int):
            The time when this table expires, in
            milliseconds since the epoch. If not present,
            the table will persist indefinitely. Expired
            tables will be deleted and their storage
            reclaimed.
        require_partition_filter (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If set to true, queries including
            this table must specify a partition filter. This
            filter is used for partition elimination.
    """

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_reference: gcb_table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcb_table_reference.TableReference,
    )
    friendly_name: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.StringValue,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=5,
    )
    time_partitioning: gcb_time_partitioning.TimePartitioning = proto.Field(
        proto.MESSAGE,
        number=6,
        message=gcb_time_partitioning.TimePartitioning,
    )
    range_partitioning: gcb_range_partitioning.RangePartitioning = proto.Field(
        proto.MESSAGE,
        number=12,
        message=gcb_range_partitioning.RangePartitioning,
    )
    clustering: gcb_clustering.Clustering = proto.Field(
        proto.MESSAGE,
        number=11,
        message=gcb_clustering.Clustering,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    view: "ListFormatView" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="ListFormatView",
    )
    creation_time: int = proto.Field(
        proto.INT64,
        number=9,
    )
    expiration_time: int = proto.Field(
        proto.INT64,
        number=10,
    )
    require_partition_filter: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=14,
        message=wrappers_pb2.BoolValue,
    )


class TableList(proto.Message):
    r"""Partial projection of the metadata for a given table in a
    list response.

    Attributes:
        kind (str):
            The type of list.
        etag (str):
            A hash of this page of results.
        next_page_token (str):
            A token to request the next page of results.
        tables (MutableSequence[google.cloud.bigquery_v2.types.ListFormatTable]):
            Tables in the requested dataset.
        total_items (google.protobuf.wrappers_pb2.Int32Value):
            The total number of tables in the dataset.
    """

    @property
    def raw_page(self):
        return self

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    tables: MutableSequence["ListFormatTable"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="ListFormatTable",
    )
    total_items: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.Int32Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
