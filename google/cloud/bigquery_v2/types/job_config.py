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

from google.cloud.bigquery_v2.types import clustering as gcb_clustering
from google.cloud.bigquery_v2.types import dataset_reference
from google.cloud.bigquery_v2.types import (
    decimal_target_types as gcb_decimal_target_types,
)
from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import external_data_config
from google.cloud.bigquery_v2.types import file_set_specification_type
from google.cloud.bigquery_v2.types import hive_partitioning
from google.cloud.bigquery_v2.types import json_extension as gcb_json_extension
from google.cloud.bigquery_v2.types import model_reference
from google.cloud.bigquery_v2.types import query_parameter
from google.cloud.bigquery_v2.types import range_partitioning as gcb_range_partitioning
from google.cloud.bigquery_v2.types import system_variable
from google.cloud.bigquery_v2.types import table_reference
from google.cloud.bigquery_v2.types import table_schema
from google.cloud.bigquery_v2.types import time_partitioning as gcb_time_partitioning
from google.cloud.bigquery_v2.types import udf_resource
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "DestinationTableProperties",
        "ConnectionProperty",
        "JobConfigurationQuery",
        "ScriptOptions",
        "JobConfigurationLoad",
        "JobConfigurationTableCopy",
        "JobConfigurationExtract",
        "JobConfiguration",
    },
)


class DestinationTableProperties(proto.Message):
    r"""Properties for the destination table.

    Attributes:
        friendly_name (google.protobuf.wrappers_pb2.StringValue):
            Optional. Friendly name for the destination
            table. If the table already exists, it should be
            same as the existing friendly name.
        description (google.protobuf.wrappers_pb2.StringValue):
            Optional. The description for the destination
            table. This will only be used if the destination
            table is newly created. If the table already
            exists and a value different than the current
            description is provided, the job will fail.
        labels (MutableMapping[str, str]):
            Optional. The labels associated with this
            table. You can use these to organize and group
            your tables. This will only be used if the
            destination table is newly created. If the table
            already exists and labels are different than the
            current labels are provided, the job will fail.
    """

    friendly_name: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.StringValue,
    )
    description: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.StringValue,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


class ConnectionProperty(proto.Message):
    r"""A connection-level property to customize query behavior. Under JDBC,
    these correspond directly to connection properties passed to the
    DriverManager. Under ODBC, these correspond to properties in the
    connection string.

    Currently supported connection properties:

    -  **dataset_project_id**: represents the default project for
       datasets that are used in the query. Setting the system variable
       ``@@dataset_project_id`` achieves the same behavior. For more
       information about system variables, see:
       https://cloud.google.com/bigquery/docs/reference/system-variables

    -  **time_zone**: represents the default timezone used to run the
       query.

    -  **session_id**: associates the query with a given session.

    -  **query_label**: associates the query with a given job label. If
       set, all subsequent queries in a script or session will have this
       label. For the format in which a you can specify a query label,
       see labels in the JobConfiguration resource type:
       https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfiguration

    -  **service_account**: indicates the service account to use to run
       a continuous query. If set, the query job uses the service
       account to access Google Cloud resources. Service account access
       is bounded by the IAM permissions that you have granted to the
       service account.

    Additional properties are allowed, but ignored. Specifying multiple
    connection properties with the same key returns an error.

    Attributes:
        key (str):
            The key of the property to set.
        value (str):
            The value of the property to set.
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )


class JobConfigurationQuery(proto.Message):
    r"""JobConfigurationQuery configures a BigQuery query job.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        query (str):
            [Required] SQL query text to execute. The useLegacySql field
            can be used to indicate whether the query uses legacy SQL or
            GoogleSQL.
        destination_table (google.cloud.bigquery_v2.types.TableReference):
            Optional. Describes the table where the query
            results should be stored. This property must be
            set for large results that exceed the maximum
            response size.  For queries that produce
            anonymous (cached) results, this field will be
            populated by BigQuery.
        external_table_definitions (MutableMapping[str, google.cloud.bigquery_v2.types.ExternalDataConfiguration]):
            Optional. You can specify external table
            definitions, which operate as ephemeral tables
            that can be queried.  These definitions are
            configured using a JSON map, where the string
            key represents the table identifier, and the
            value is the corresponding external data
            configuration object.
        user_defined_function_resources (MutableSequence[google.cloud.bigquery_v2.types.UserDefinedFunctionResource]):
            Describes user-defined function resources
            used in the query.
        create_disposition (str):
            Optional. Specifies whether the job is allowed to create new
            tables. The following values are supported:

            -  CREATE_IF_NEEDED: If the table does not exist, BigQuery
               creates the table.
            -  CREATE_NEVER: The table must already exist. If it does
               not, a 'notFound' error is returned in the job result.

            The default value is CREATE_IF_NEEDED. Creation, truncation
            and append actions occur as one atomic update upon job
            completion.
        write_disposition (str):
            Optional. Specifies the action that occurs if the
            destination table already exists. The following values are
            supported:

            -  WRITE_TRUNCATE: If the table already exists, BigQuery
               overwrites the data, removes the constraints, and uses
               the schema from the query result.
            -  WRITE_TRUNCATE_DATA: If the table already exists,
               BigQuery overwrites the data, but keeps the constraints
               and schema of the existing table.
            -  WRITE_APPEND: If the table already exists, BigQuery
               appends the data to the table.
            -  WRITE_EMPTY: If the table already exists and contains
               data, a 'duplicate' error is returned in the job result.

            The default value is WRITE_EMPTY. Each action is atomic and
            only occurs if BigQuery is able to complete the job
            successfully. Creation, truncation and append actions occur
            as one atomic update upon job completion.
        default_dataset (google.cloud.bigquery_v2.types.DatasetReference):
            Optional. Specifies the default dataset to use for
            unqualified table names in the query. This setting does not
            alter behavior of unqualified dataset names. Setting the
            system variable ``@@dataset_id`` achieves the same behavior.
            See
            https://cloud.google.com/bigquery/docs/reference/system-variables
            for more information on system variables.
        priority (str):
            Optional. Specifies a priority for the query.
            Possible values include INTERACTIVE and BATCH.
            The default value is INTERACTIVE.
        allow_large_results (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If true and query uses legacy SQL
            dialect, allows the query to produce arbitrarily
            large result tables at a slight cost in
            performance. Requires destinationTable to be
            set.
            For GoogleSQL queries, this flag is ignored and
            large results are always allowed.  However, you
            must still set destinationTable when result size
            exceeds the allowed maximum response size.
        use_query_cache (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Whether to look for the result in
            the query cache. The query cache is a
            best-effort cache that will be flushed whenever
            tables in the query are modified. Moreover, the
            query cache is only available when a query does
            not have a destination table specified. The
            default value is true.
        flatten_results (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If true and query uses legacy SQL
            dialect, flattens all nested and repeated fields
            in the query results. allowLargeResults must be
            true if this is set to false. For GoogleSQL
            queries, this flag is ignored and results are
            never flattened.
        maximum_bytes_billed (google.protobuf.wrappers_pb2.Int64Value):
            Limits the bytes billed for this job. Queries
            that will have bytes billed beyond this limit
            will fail (without incurring a charge). If
            unspecified, this will be set to your project
            default.
        use_legacy_sql (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Specifies whether to use BigQuery's
            legacy SQL dialect for this query. The default
            value is true. If set to false, the query will
            use BigQuery's GoogleSQL:

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
        system_variables (google.cloud.bigquery_v2.types.SystemVariables):
            Output only. System variables for GoogleSQL
            queries. A system variable is output if the
            variable is settable and its value differs from
            the system default.
            "@@" prefix is not included in the name of the
            System variables.

            This field is a member of `oneof`_ ``_system_variables``.
        schema_update_options (MutableSequence[str]):
            Allows the schema of the destination table to be updated as
            a side effect of the query job. Schema update options are
            supported in two cases: when writeDisposition is
            WRITE_APPEND; when writeDisposition is WRITE_TRUNCATE and
            the destination table is a partition of a table, specified
            by partition decorators. For normal tables, WRITE_TRUNCATE
            will always overwrite the schema. One or more of the
            following values are specified:

            -  ALLOW_FIELD_ADDITION: allow adding a nullable field to
               the schema.
            -  ALLOW_FIELD_RELAXATION: allow relaxing a required field
               in the original schema to nullable.
        time_partitioning (google.cloud.bigquery_v2.types.TimePartitioning):
            Time-based partitioning specification for the
            destination table. Only one of timePartitioning
            and rangePartitioning should be specified.
        range_partitioning (google.cloud.bigquery_v2.types.RangePartitioning):
            Range partitioning specification for the
            destination table. Only one of timePartitioning
            and rangePartitioning should be specified.
        clustering (google.cloud.bigquery_v2.types.Clustering):
            Clustering specification for the destination
            table.
        destination_encryption_configuration (google.cloud.bigquery_v2.types.EncryptionConfiguration):
            Custom encryption configuration (e.g., Cloud
            KMS keys)
        script_options (google.cloud.bigquery_v2.types.ScriptOptions):
            Options controlling the execution of scripts.
        connection_properties (MutableSequence[google.cloud.bigquery_v2.types.ConnectionProperty]):
            Connection properties which can modify the
            query behavior.
        create_session (google.protobuf.wrappers_pb2.BoolValue):
            If this property is true, the job creates a new session
            using a randomly generated session_id. To continue using a
            created session with subsequent queries, pass the existing
            session identifier as a ``ConnectionProperty`` value. The
            session identifier is returned as part of the
            ``SessionInfo`` message within the query statistics.

            The new session's location will be set to
            ``Job.JobReference.location`` if it is present, otherwise
            it's set to the default location based on existing routing
            logic.
        continuous (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Whether to run the query as
            continuous or a regular query. Continuous query
            is currently in experimental stage and not ready
            for general usage.
        write_incremental_results (bool):
            Optional. This is only supported for a SELECT
            query using a temporary table. If set, the query
            is allowed to write results incrementally to the
            temporary result table. This may incur a
            performance penalty. This option cannot be used
            with Legacy SQL. This feature is not yet
            available.
    """

    query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    destination_table: table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=2,
        message=table_reference.TableReference,
    )
    external_table_definitions: MutableMapping[
        str, external_data_config.ExternalDataConfiguration
    ] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=23,
        message=external_data_config.ExternalDataConfiguration,
    )
    user_defined_function_resources: MutableSequence[
        udf_resource.UserDefinedFunctionResource
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=udf_resource.UserDefinedFunctionResource,
    )
    create_disposition: str = proto.Field(
        proto.STRING,
        number=5,
    )
    write_disposition: str = proto.Field(
        proto.STRING,
        number=6,
    )
    default_dataset: dataset_reference.DatasetReference = proto.Field(
        proto.MESSAGE,
        number=7,
        message=dataset_reference.DatasetReference,
    )
    priority: str = proto.Field(
        proto.STRING,
        number=8,
    )
    allow_large_results: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=10,
        message=wrappers_pb2.BoolValue,
    )
    use_query_cache: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=11,
        message=wrappers_pb2.BoolValue,
    )
    flatten_results: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=12,
        message=wrappers_pb2.BoolValue,
    )
    maximum_bytes_billed: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=14,
        message=wrappers_pb2.Int64Value,
    )
    use_legacy_sql: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=15,
        message=wrappers_pb2.BoolValue,
    )
    parameter_mode: str = proto.Field(
        proto.STRING,
        number=16,
    )
    query_parameters: MutableSequence[
        query_parameter.QueryParameter
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=17,
        message=query_parameter.QueryParameter,
    )
    system_variables: system_variable.SystemVariables = proto.Field(
        proto.MESSAGE,
        number=35,
        optional=True,
        message=system_variable.SystemVariables,
    )
    schema_update_options: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=18,
    )
    time_partitioning: gcb_time_partitioning.TimePartitioning = proto.Field(
        proto.MESSAGE,
        number=19,
        message=gcb_time_partitioning.TimePartitioning,
    )
    range_partitioning: gcb_range_partitioning.RangePartitioning = proto.Field(
        proto.MESSAGE,
        number=22,
        message=gcb_range_partitioning.RangePartitioning,
    )
    clustering: gcb_clustering.Clustering = proto.Field(
        proto.MESSAGE,
        number=20,
        message=gcb_clustering.Clustering,
    )
    destination_encryption_configuration: encryption_config.EncryptionConfiguration = (
        proto.Field(
            proto.MESSAGE,
            number=21,
            message=encryption_config.EncryptionConfiguration,
        )
    )
    script_options: "ScriptOptions" = proto.Field(
        proto.MESSAGE,
        number=24,
        message="ScriptOptions",
    )
    connection_properties: MutableSequence["ConnectionProperty"] = proto.RepeatedField(
        proto.MESSAGE,
        number=33,
        message="ConnectionProperty",
    )
    create_session: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=34,
        message=wrappers_pb2.BoolValue,
    )
    continuous: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=36,
        message=wrappers_pb2.BoolValue,
    )
    write_incremental_results: bool = proto.Field(
        proto.BOOL,
        number=37,
    )


class ScriptOptions(proto.Message):
    r"""Options related to script execution.

    Attributes:
        statement_timeout_ms (google.protobuf.wrappers_pb2.Int64Value):
            Timeout period for each statement in a
            script.
        statement_byte_budget (google.protobuf.wrappers_pb2.Int64Value):
            Limit on the number of bytes billed per
            statement. Exceeding this budget results in an
            error.
        key_result_statement (google.cloud.bigquery_v2.types.ScriptOptions.KeyResultStatementKind):
            Determines which statement in the script
            represents the "key result", used to populate
            the schema and query results of the script job.
            Default is LAST.
    """

    class KeyResultStatementKind(proto.Enum):
        r"""KeyResultStatementKind controls how the key result is
        determined.

        Values:
            KEY_RESULT_STATEMENT_KIND_UNSPECIFIED (0):
                Default value.
            LAST (1):
                The last result determines the key result.
            FIRST_SELECT (2):
                The first SELECT statement determines the key
                result.
        """
        KEY_RESULT_STATEMENT_KIND_UNSPECIFIED = 0
        LAST = 1
        FIRST_SELECT = 2

    statement_timeout_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.Int64Value,
    )
    statement_byte_budget: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    key_result_statement: KeyResultStatementKind = proto.Field(
        proto.ENUM,
        number=4,
        enum=KeyResultStatementKind,
    )


class JobConfigurationLoad(proto.Message):
    r"""JobConfigurationLoad contains the configuration properties
    for loading data into a destination table.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        source_uris (MutableSequence[str]):
            [Required] The fully-qualified URIs that point to your data
            in Google Cloud. For Google Cloud Storage URIs: Each URI can
            contain one '*' wildcard character and it must come after
            the 'bucket' name. Size limits related to load jobs apply to
            external data sources. For Google Cloud Bigtable URIs:
            Exactly one URI can be specified and it has be a fully
            specified and valid HTTPS URL for a Google Cloud Bigtable
            table. For Google Cloud Datastore backups: Exactly one URI
            can be specified. Also, the '*' wildcard character is not
            allowed.
        file_set_spec_type (google.cloud.bigquery_v2.types.FileSetSpecType):
            Optional. Specifies how source URIs are
            interpreted for constructing the file set to
            load. By default, source URIs are expanded
            against the underlying storage. You can also
            specify manifest files to control how the file
            set is constructed. This option is only
            applicable to object storage systems.
        schema (google.cloud.bigquery_v2.types.TableSchema):
            Optional. The schema for the destination
            table. The schema can be omitted if the
            destination table already exists, or if you're
            loading data from Google Cloud Datastore.
        destination_table (google.cloud.bigquery_v2.types.TableReference):
            [Required] The destination table to load the data into.
        destination_table_properties (google.cloud.bigquery_v2.types.DestinationTableProperties):
            Optional. [Experimental] Properties with which to create the
            destination table if it is new.
        create_disposition (str):
            Optional. Specifies whether the job is allowed to create new
            tables. The following values are supported:

            -  CREATE_IF_NEEDED: If the table does not exist, BigQuery
               creates the table.
            -  CREATE_NEVER: The table must already exist. If it does
               not, a 'notFound' error is returned in the job result.
               The default value is CREATE_IF_NEEDED. Creation,
               truncation and append actions occur as one atomic update
               upon job completion.
        write_disposition (str):
            Optional. Specifies the action that occurs if the
            destination table already exists. The following values are
            supported:

            -  WRITE_TRUNCATE: If the table already exists, BigQuery
               overwrites the data, removes the constraints and uses the
               schema from the load job.
            -  WRITE_TRUNCATE_DATA: If the table already exists,
               BigQuery overwrites the data, but keeps the constraints
               and schema of the existing table.
            -  WRITE_APPEND: If the table already exists, BigQuery
               appends the data to the table.
            -  WRITE_EMPTY: If the table already exists and contains
               data, a 'duplicate' error is returned in the job result.

            The default value is WRITE_APPEND. Each action is atomic and
            only occurs if BigQuery is able to complete the job
            successfully. Creation, truncation and append actions occur
            as one atomic update upon job completion.
        null_marker (google.protobuf.wrappers_pb2.StringValue):
            Optional. Specifies a string that represents
            a null value in a CSV file. For example, if you
            specify "\N", BigQuery interprets "\N" as a null
            value when loading a CSV file.
            The default value is the empty string. If you
            set this property to a custom value, BigQuery
            throws an error if an empty string is present
            for all data types except for STRING and BYTE.
            For STRING and BYTE columns, BigQuery interprets
            the empty string as an empty value.
        field_delimiter (str):
            Optional. The separator character for fields
            in a CSV file. The separator is interpreted as a
            single byte. For files encoded in ISO-8859-1,
            any single character can be used as a separator.
            For files encoded in UTF-8, characters
            represented in decimal range 1-127
            (U+0001-U+007F) can be used without any
            modification. UTF-8 characters encoded with
            multiple bytes (i.e. U+0080 and above) will have
            only the first byte used for separating fields.
            The remaining bytes will be treated as a part of
            the field. BigQuery also supports the escape
            sequence "\t" (U+0009) to specify a tab
            separator. The default value is comma (",",
            U+002C).
        skip_leading_rows (google.protobuf.wrappers_pb2.Int32Value):
            Optional. The number of rows at the top of a CSV file that
            BigQuery will skip when loading the data. The default value
            is 0. This property is useful if you have header rows in the
            file that should be skipped. When autodetect is on, the
            behavior is the following:

            -  skipLeadingRows unspecified - Autodetect tries to detect
               headers in the first row. If they are not detected, the
               row is read as data. Otherwise data is read starting from
               the second row.
            -  skipLeadingRows is 0 - Instructs autodetect that there
               are no headers and data should be read starting from the
               first row.
            -  skipLeadingRows = N > 0 - Autodetect skips N-1 rows and
               tries to detect headers in row N. If headers are not
               detected, row N is just skipped. Otherwise row N is used
               to extract column names for the detected schema.
        encoding (str):
            Optional. The character encoding of the data. The supported
            values are UTF-8, ISO-8859-1, UTF-16BE, UTF-16LE, UTF-32BE,
            and UTF-32LE. The default value is UTF-8. BigQuery decodes
            the data after the raw, binary data has been split using the
            values of the ``quote`` and ``fieldDelimiter`` properties.

            If you don't specify an encoding, or if you specify a UTF-8
            encoding when the CSV file is not UTF-8 encoded, BigQuery
            attempts to convert the data to UTF-8. Generally, your data
            loads successfully, but it may not match byte-for-byte what
            you expect. To avoid this, specify the correct encoding by
            using the ``--encoding`` flag.

            If BigQuery can't convert a character other than the ASCII
            ``0`` character, BigQuery converts the character to the
            standard Unicode replacement character: �.
        quote (google.protobuf.wrappers_pb2.StringValue):
            Optional. The value that is used to quote
            data sections in a CSV file. BigQuery converts
            the string to ISO-8859-1 encoding, and then uses
            the first byte of the encoded string to split
            the data in its raw, binary state.
            The default value is a double-quote ('"').
            If your data does not contain quoted sections,
            set the property value to an empty string.
            If your data contains quoted newline characters,
            you must also set the allowQuotedNewlines
            property to true.
            To include the specific quote character within a
            quoted value, precede it with an additional
            matching quote character. For example, if you
            want to escape the default character  ' " ', use
            ' "" '. @default ".
        max_bad_records (google.protobuf.wrappers_pb2.Int32Value):
            Optional. The maximum number of bad records that BigQuery
            can ignore when running the job. If the number of bad
            records exceeds this value, an invalid error is returned in
            the job result. The default value is 0, which requires that
            all records are valid. This is only supported for CSV and
            NEWLINE_DELIMITED_JSON file formats.
        allow_quoted_newlines (google.protobuf.wrappers_pb2.BoolValue):
            Indicates if BigQuery should allow quoted
            data sections that contain newline characters in
            a CSV file. The default value is false.
        source_format (str):
            Optional. The format of the data files. For CSV files,
            specify "CSV". For datastore backups, specify
            "DATASTORE_BACKUP". For newline-delimited JSON, specify
            "NEWLINE_DELIMITED_JSON". For Avro, specify "AVRO". For
            parquet, specify "PARQUET". For orc, specify "ORC". The
            default value is CSV.
        allow_jagged_rows (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Accept rows that are missing
            trailing optional columns. The missing values
            are treated as nulls. If false, records with
            missing trailing columns are treated as bad
            records, and if there are too many bad records,
            an invalid error is returned in the job result.
            The default value is false.
            Only applicable to CSV, ignored for other
            formats.
        ignore_unknown_values (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Indicates if BigQuery should allow
            extra values that are not represented in the
            table schema. If true, the extra values are
            ignored.
            If false, records with extra columns are treated
            as bad records, and if there are too many bad
            records, an invalid error is returned in the job
            result. The default value is false.
            The sourceFormat property determines what
            BigQuery treats as an extra value:

              CSV: Trailing columns
              JSON: Named values that don't match any column
            names in the table schema   Avro, Parquet, ORC:
            Fields in the file schema that don't exist in
            the   table schema.
            BigQuery treats as an extra value.
        projection_fields (MutableSequence[str]):
            If sourceFormat is set to "DATASTORE_BACKUP", indicates
            which entity properties to load into BigQuery from a Cloud
            Datastore backup. Property names are case sensitive and must
            be top-level properties. If no properties are specified,
            BigQuery loads all properties. If any named property isn't
            found in the Cloud Datastore backup, an invalid error is
            returned in the job result.
        autodetect (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Indicates if we should
            automatically infer the options and schema for
            CSV and JSON sources.
        schema_update_options (MutableSequence[str]):
            Allows the schema of the destination table to be updated as
            a side effect of the load job if a schema is autodetected or
            supplied in the job configuration. Schema update options are
            supported in two cases: when writeDisposition is
            WRITE_APPEND; when writeDisposition is WRITE_TRUNCATE and
            the destination table is a partition of a table, specified
            by partition decorators. For normal tables, WRITE_TRUNCATE
            will always overwrite the schema. One or more of the
            following values are specified:

            -  ALLOW_FIELD_ADDITION: allow adding a nullable field to
               the schema.
            -  ALLOW_FIELD_RELAXATION: allow relaxing a required field
               in the original schema to nullable.
            will always overwrite the schema. One or more of the.

        time_partitioning (google.cloud.bigquery_v2.types.TimePartitioning):
            Time-based partitioning specification for the
            destination table. Only one of timePartitioning
            and rangePartitioning should be specified.
        range_partitioning (google.cloud.bigquery_v2.types.RangePartitioning):
            Range partitioning specification for the
            destination table. Only one of timePartitioning
            and rangePartitioning should be specified.
        clustering (google.cloud.bigquery_v2.types.Clustering):
            Clustering specification for the destination
            table.
        destination_encryption_configuration (google.cloud.bigquery_v2.types.EncryptionConfiguration):
            Custom encryption configuration (e.g., Cloud
            KMS keys)
        use_avro_logical_types (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If sourceFormat is set to "AVRO",
            indicates whether to interpret logical types as
            the corresponding BigQuery data type (for
            example, TIMESTAMP), instead of using the raw
            type (for example, INTEGER).
        reference_file_schema_uri (google.protobuf.wrappers_pb2.StringValue):
            Optional. The user can provide a reference
            file with the reader schema. This file is only
            loaded if it is part of source URIs, but is not
            loaded otherwise. It is enabled for the
            following formats: AVRO, PARQUET, ORC.
        hive_partitioning_options (google.cloud.bigquery_v2.types.HivePartitioningOptions):
            Optional. When set, configures hive
            partitioning support. Not all storage formats
            support hive partitioning -- requesting hive
            partitioning on an unsupported format will lead
            to an error, as will providing an invalid
            specification.
        decimal_target_types (MutableSequence[google.cloud.bigquery_v2.types.DecimalTargetType]):
            Defines the list of possible SQL data types to which the
            source decimal values are converted. This list and the
            precision and the scale parameters of the decimal field
            determine the target type. In the order of NUMERIC,
            BIGNUMERIC, and STRING, a type is picked if it is in the
            specified list and if it supports the precision and the
            scale. STRING supports all precision and scale values. If
            none of the listed types supports the precision and the
            scale, the type supporting the widest range in the specified
            list is picked, and if a value exceeds the supported range
            when reading the data, an error will be thrown.

            Example: Suppose the value of this field is ["NUMERIC",
            "BIGNUMERIC"]. If (precision,scale) is:

            -  (38,9) -> NUMERIC;
            -  (39,9) -> BIGNUMERIC (NUMERIC cannot hold 30 integer
               digits);
            -  (38,10) -> BIGNUMERIC (NUMERIC cannot hold 10 fractional
               digits);
            -  (76,38) -> BIGNUMERIC;
            -  (77,38) -> BIGNUMERIC (error if value exceeds supported
               range).

            This field cannot contain duplicate types. The order of the
            types in this field is ignored. For example, ["BIGNUMERIC",
            "NUMERIC"] is the same as ["NUMERIC", "BIGNUMERIC"] and
            NUMERIC always takes precedence over BIGNUMERIC.

            Defaults to ["NUMERIC", "STRING"] for ORC and ["NUMERIC"]
            for the other file formats.
        json_extension (google.cloud.bigquery_v2.types.JsonExtension):
            Optional. Load option to be used together with source_format
            newline-delimited JSON to indicate that a variant of JSON is
            being loaded. To load newline-delimited GeoJSON, specify
            GEOJSON (and source_format must be set to
            NEWLINE_DELIMITED_JSON).
        parquet_options (google.cloud.bigquery_v2.types.ParquetOptions):
            Optional. Additional properties to set if
            sourceFormat is set to PARQUET.
        preserve_ascii_control_characters (google.protobuf.wrappers_pb2.BoolValue):
            Optional. When sourceFormat is set to "CSV",
            this indicates whether the embedded ASCII
            control characters (the first 32 characters in
            the ASCII-table, from
            '\x00' to '\x1F') are preserved.
        connection_properties (MutableSequence[google.cloud.bigquery_v2.types.ConnectionProperty]):
            Optional. Connection properties which can modify the load
            job behavior. Currently, only the 'session_id' connection
            property is supported, and is used to resolve \_SESSION
            appearing as the dataset id.
        create_session (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If this property is true, the job creates a new
            session using a randomly generated session_id. To continue
            using a created session with subsequent queries, pass the
            existing session identifier as a ``ConnectionProperty``
            value. The session identifier is returned as part of the
            ``SessionInfo`` message within the query statistics.

            The new session's location will be set to
            ``Job.JobReference.location`` if it is present, otherwise
            it's set to the default location based on existing routing
            logic.
        column_name_character_map (google.cloud.bigquery_v2.types.JobConfigurationLoad.ColumnNameCharacterMap):
            Optional. Character map supported for column
            names in CSV/Parquet loads. Defaults to STRICT
            and can be overridden by Project Config Service.
            Using this option with unsupporting load formats
            will result in an error.
        copy_files_only (google.protobuf.wrappers_pb2.BoolValue):
            Optional. [Experimental] Configures the load job to copy
            files directly to the destination BigLake managed table,
            bypassing file content reading and rewriting.

            Copying files only is supported when all the following are
            true:

            -  ``source_uris`` are located in the same Cloud Storage
               location as the destination table's ``storage_uri``
               location.
            -  ``source_format`` is ``PARQUET``.
            -  ``destination_table`` is an existing BigLake managed
               table. The table's schema does not have flexible column
               names. The table's columns do not have type parameters
               other than precision and scale.
            -  No options other than the above are specified.
        time_zone (google.protobuf.wrappers_pb2.StringValue):
            Optional. Default time zone that will apply
            when parsing timestamp values that have no
            specific time zone.
        null_markers (MutableSequence[str]):
            Optional. A list of strings represented as SQL NULL value in
            a CSV file.

            null_marker and null_markers can't be set at the same time.
            If null_marker is set, null_markers has to be not set. If
            null_markers is set, null_marker has to be not set. If both
            null_marker and null_markers are set at the same time, a
            user error would be thrown. Any strings listed in
            null_markers, including empty string would be interpreted as
            SQL NULL. This applies to all column types.
        date_format (str):
            Optional. Date format used for parsing DATE
            values.

            This field is a member of `oneof`_ ``_date_format``.
        datetime_format (str):
            Optional. Date format used for parsing
            DATETIME values.

            This field is a member of `oneof`_ ``_datetime_format``.
        time_format (str):
            Optional. Date format used for parsing TIME
            values.

            This field is a member of `oneof`_ ``_time_format``.
        timestamp_format (str):
            Optional. Date format used for parsing
            TIMESTAMP values.

            This field is a member of `oneof`_ ``_timestamp_format``.
        source_column_match (google.cloud.bigquery_v2.types.JobConfigurationLoad.SourceColumnMatch):
            Optional. Controls the strategy used to match
            loaded columns to the schema. If not set, a
            sensible default is chosen based on how the
            schema is provided. If autodetect is used, then
            columns are matched by name. Otherwise, columns
            are matched by position. This is done to keep
            the behavior backward-compatible.
    """

    class ColumnNameCharacterMap(proto.Enum):
        r"""Indicates the character map used for column names.

        Values:
            COLUMN_NAME_CHARACTER_MAP_UNSPECIFIED (0):
                Unspecified column name character map.
            STRICT (1):
                Support flexible column name and reject
                invalid column names.
            V1 (2):
                Support alphanumeric + underscore characters
                and names must start with a letter or
                underscore. Invalid column names will be
                normalized.
            V2 (3):
                Support flexible column name. Invalid column
                names will be normalized.
        """
        COLUMN_NAME_CHARACTER_MAP_UNSPECIFIED = 0
        STRICT = 1
        V1 = 2
        V2 = 3

    class SourceColumnMatch(proto.Enum):
        r"""Indicates the strategy used to match loaded columns to the
        schema.

        Values:
            SOURCE_COLUMN_MATCH_UNSPECIFIED (0):
                Uses sensible defaults based on how the
                schema is provided. If autodetect is used, then
                columns are matched by name. Otherwise, columns
                are matched by position. This is done to keep
                the behavior backward-compatible.
            POSITION (1):
                Matches by position. This assumes that the
                columns are ordered the same way as the schema.
            NAME (2):
                Matches by name. This reads the header row as
                column names and reorders columns to match the
                field names in the schema.
        """
        SOURCE_COLUMN_MATCH_UNSPECIFIED = 0
        POSITION = 1
        NAME = 2

    source_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    file_set_spec_type: file_set_specification_type.FileSetSpecType = proto.Field(
        proto.ENUM,
        number=49,
        enum=file_set_specification_type.FileSetSpecType,
    )
    schema: table_schema.TableSchema = proto.Field(
        proto.MESSAGE,
        number=2,
        message=table_schema.TableSchema,
    )
    destination_table: table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=3,
        message=table_reference.TableReference,
    )
    destination_table_properties: "DestinationTableProperties" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="DestinationTableProperties",
    )
    create_disposition: str = proto.Field(
        proto.STRING,
        number=5,
    )
    write_disposition: str = proto.Field(
        proto.STRING,
        number=6,
    )
    null_marker: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.StringValue,
    )
    field_delimiter: str = proto.Field(
        proto.STRING,
        number=8,
    )
    skip_leading_rows: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=9,
        message=wrappers_pb2.Int32Value,
    )
    encoding: str = proto.Field(
        proto.STRING,
        number=10,
    )
    quote: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=11,
        message=wrappers_pb2.StringValue,
    )
    max_bad_records: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=12,
        message=wrappers_pb2.Int32Value,
    )
    allow_quoted_newlines: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=15,
        message=wrappers_pb2.BoolValue,
    )
    source_format: str = proto.Field(
        proto.STRING,
        number=16,
    )
    allow_jagged_rows: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=17,
        message=wrappers_pb2.BoolValue,
    )
    ignore_unknown_values: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=18,
        message=wrappers_pb2.BoolValue,
    )
    projection_fields: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=19,
    )
    autodetect: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=20,
        message=wrappers_pb2.BoolValue,
    )
    schema_update_options: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=21,
    )
    time_partitioning: gcb_time_partitioning.TimePartitioning = proto.Field(
        proto.MESSAGE,
        number=22,
        message=gcb_time_partitioning.TimePartitioning,
    )
    range_partitioning: gcb_range_partitioning.RangePartitioning = proto.Field(
        proto.MESSAGE,
        number=26,
        message=gcb_range_partitioning.RangePartitioning,
    )
    clustering: gcb_clustering.Clustering = proto.Field(
        proto.MESSAGE,
        number=23,
        message=gcb_clustering.Clustering,
    )
    destination_encryption_configuration: encryption_config.EncryptionConfiguration = (
        proto.Field(
            proto.MESSAGE,
            number=24,
            message=encryption_config.EncryptionConfiguration,
        )
    )
    use_avro_logical_types: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=25,
        message=wrappers_pb2.BoolValue,
    )
    reference_file_schema_uri: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=45,
        message=wrappers_pb2.StringValue,
    )
    hive_partitioning_options: hive_partitioning.HivePartitioningOptions = proto.Field(
        proto.MESSAGE,
        number=37,
        message=hive_partitioning.HivePartitioningOptions,
    )
    decimal_target_types: MutableSequence[
        gcb_decimal_target_types.DecimalTargetType
    ] = proto.RepeatedField(
        proto.ENUM,
        number=39,
        enum=gcb_decimal_target_types.DecimalTargetType,
    )
    json_extension: gcb_json_extension.JsonExtension = proto.Field(
        proto.ENUM,
        number=41,
        enum=gcb_json_extension.JsonExtension,
    )
    parquet_options: external_data_config.ParquetOptions = proto.Field(
        proto.MESSAGE,
        number=42,
        message=external_data_config.ParquetOptions,
    )
    preserve_ascii_control_characters: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=44,
        message=wrappers_pb2.BoolValue,
    )
    connection_properties: MutableSequence["ConnectionProperty"] = proto.RepeatedField(
        proto.MESSAGE,
        number=46,
        message="ConnectionProperty",
    )
    create_session: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=47,
        message=wrappers_pb2.BoolValue,
    )
    column_name_character_map: ColumnNameCharacterMap = proto.Field(
        proto.ENUM,
        number=50,
        enum=ColumnNameCharacterMap,
    )
    copy_files_only: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=51,
        message=wrappers_pb2.BoolValue,
    )
    time_zone: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=52,
        message=wrappers_pb2.StringValue,
    )
    null_markers: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=53,
    )
    date_format: str = proto.Field(
        proto.STRING,
        number=54,
        optional=True,
    )
    datetime_format: str = proto.Field(
        proto.STRING,
        number=55,
        optional=True,
    )
    time_format: str = proto.Field(
        proto.STRING,
        number=56,
        optional=True,
    )
    timestamp_format: str = proto.Field(
        proto.STRING,
        number=57,
        optional=True,
    )
    source_column_match: SourceColumnMatch = proto.Field(
        proto.ENUM,
        number=58,
        enum=SourceColumnMatch,
    )


class JobConfigurationTableCopy(proto.Message):
    r"""JobConfigurationTableCopy configures a job that copies data from one
    table to another. For more information on copying tables, see `Copy
    a
    table <https://cloud.google.com/bigquery/docs/managing-tables#copy-table>`__.

    Attributes:
        source_table (google.cloud.bigquery_v2.types.TableReference):
            [Pick one] Source table to copy.
        source_tables (MutableSequence[google.cloud.bigquery_v2.types.TableReference]):
            [Pick one] Source tables to copy.
        destination_table (google.cloud.bigquery_v2.types.TableReference):
            [Required] The destination table.
        create_disposition (str):
            Optional. Specifies whether the job is allowed to create new
            tables. The following values are supported:

            -  CREATE_IF_NEEDED: If the table does not exist, BigQuery
               creates the table.
            -  CREATE_NEVER: The table must already exist. If it does
               not, a 'notFound' error is returned in the job result.

            The default value is CREATE_IF_NEEDED. Creation, truncation
            and append actions occur as one atomic update upon job
            completion.
        write_disposition (str):
            Optional. Specifies the action that occurs if the
            destination table already exists. The following values are
            supported:

            -  WRITE_TRUNCATE: If the table already exists, BigQuery
               overwrites the table data and uses the schema and table
               constraints from the source table.
            -  WRITE_APPEND: If the table already exists, BigQuery
               appends the data to the table.
            -  WRITE_EMPTY: If the table already exists and contains
               data, a 'duplicate' error is returned in the job result.

            The default value is WRITE_EMPTY. Each action is atomic and
            only occurs if BigQuery is able to complete the job
            successfully. Creation, truncation and append actions occur
            as one atomic update upon job completion.
        destination_encryption_configuration (google.cloud.bigquery_v2.types.EncryptionConfiguration):
            Custom encryption configuration (e.g., Cloud
            KMS keys).
        operation_type (google.cloud.bigquery_v2.types.JobConfigurationTableCopy.OperationType):
            Optional. Supported operation types in table
            copy job.
        destination_expiration_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. The time when the destination table
            expires. Expired tables will be deleted and
            their storage reclaimed.
    """

    class OperationType(proto.Enum):
        r"""Indicates different operation types supported in table copy
        job.

        Values:
            OPERATION_TYPE_UNSPECIFIED (0):
                Unspecified operation type.
            COPY (1):
                The source and destination table have the
                same table type.
            SNAPSHOT (2):
                The source table type is TABLE and
                the destination table type is SNAPSHOT.
            RESTORE (3):
                The source table type is SNAPSHOT and
                the destination table type is TABLE.
            CLONE (4):
                The source and destination table have the
                same table type, but only bill for unique data.
        """
        OPERATION_TYPE_UNSPECIFIED = 0
        COPY = 1
        SNAPSHOT = 2
        RESTORE = 3
        CLONE = 4

    source_table: table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=1,
        message=table_reference.TableReference,
    )
    source_tables: MutableSequence[
        table_reference.TableReference
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=table_reference.TableReference,
    )
    destination_table: table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=3,
        message=table_reference.TableReference,
    )
    create_disposition: str = proto.Field(
        proto.STRING,
        number=4,
    )
    write_disposition: str = proto.Field(
        proto.STRING,
        number=5,
    )
    destination_encryption_configuration: encryption_config.EncryptionConfiguration = (
        proto.Field(
            proto.MESSAGE,
            number=6,
            message=encryption_config.EncryptionConfiguration,
        )
    )
    operation_type: OperationType = proto.Field(
        proto.ENUM,
        number=8,
        enum=OperationType,
    )
    destination_expiration_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )


class JobConfigurationExtract(proto.Message):
    r"""JobConfigurationExtract configures a job that exports data
    from a BigQuery table into Google Cloud Storage.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        source_table (google.cloud.bigquery_v2.types.TableReference):
            A reference to the table being exported.

            This field is a member of `oneof`_ ``source``.
        source_model (google.cloud.bigquery_v2.types.ModelReference):
            A reference to the model being exported.

            This field is a member of `oneof`_ ``source``.
        destination_uris (MutableSequence[str]):
            [Pick one] A list of fully-qualified Google Cloud Storage
            URIs where the extracted table should be written.
        print_header (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Whether to print out a header row
            in the results. Default is true. Not applicable
            when extracting models.
        field_delimiter (str):
            Optional. When extracting data in CSV format,
            this defines the delimiter to use between fields
            in the exported data. Default is ','. Not
            applicable when extracting models.
        destination_format (str):
            Optional. The exported file format. Possible values include
            CSV, NEWLINE_DELIMITED_JSON, PARQUET, or AVRO for tables and
            ML_TF_SAVED_MODEL or ML_XGBOOST_BOOSTER for models. The
            default value for tables is CSV. Tables with nested or
            repeated fields cannot be exported as CSV. The default value
            for models is ML_TF_SAVED_MODEL.
        compression (str):
            Optional. The compression type to use for
            exported files. Possible values include DEFLATE,
            GZIP, NONE, SNAPPY, and ZSTD. The default value
            is NONE. Not all compression formats are support
            for all file formats. DEFLATE is only supported
            for Avro. ZSTD is only supported for Parquet.
            Not applicable when extracting models.
        use_avro_logical_types (google.protobuf.wrappers_pb2.BoolValue):
            Whether to use logical types when extracting
            to AVRO format. Not applicable when extracting
            models.
        model_extract_options (google.cloud.bigquery_v2.types.JobConfigurationExtract.ModelExtractOptions):
            Optional. Model extract options only
            applicable when extracting models.
    """

    class ModelExtractOptions(proto.Message):
        r"""Options related to model extraction.

        Attributes:
            trial_id (google.protobuf.wrappers_pb2.Int64Value):
                The 1-based ID of the trial to be exported from a
                hyperparameter tuning model. If not specified, the trial
                with id =
                `Model <https://cloud.google.com/bigquery/docs/reference/rest/v2/models#resource:-model>`__.defaultTrialId
                is exported. This field is ignored for models not trained
                with hyperparameter tuning.
        """

        trial_id: wrappers_pb2.Int64Value = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.Int64Value,
        )

    source_table: table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="source",
        message=table_reference.TableReference,
    )
    source_model: model_reference.ModelReference = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="source",
        message=model_reference.ModelReference,
    )
    destination_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    print_header: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.BoolValue,
    )
    field_delimiter: str = proto.Field(
        proto.STRING,
        number=5,
    )
    destination_format: str = proto.Field(
        proto.STRING,
        number=6,
    )
    compression: str = proto.Field(
        proto.STRING,
        number=7,
    )
    use_avro_logical_types: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=13,
        message=wrappers_pb2.BoolValue,
    )
    model_extract_options: ModelExtractOptions = proto.Field(
        proto.MESSAGE,
        number=14,
        message=ModelExtractOptions,
    )


class JobConfiguration(proto.Message):
    r"""

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        job_type (str):
            Output only. The type of the job. Can be
            QUERY, LOAD, EXTRACT, COPY or UNKNOWN.
        query (google.cloud.bigquery_v2.types.JobConfigurationQuery):
            [Pick one] Configures a query job.
        load (google.cloud.bigquery_v2.types.JobConfigurationLoad):
            [Pick one] Configures a load job.
        copy (google.cloud.bigquery_v2.types.JobConfigurationTableCopy):
            [Pick one] Copies a table.
        extract (google.cloud.bigquery_v2.types.JobConfigurationExtract):
            [Pick one] Configures an extract job.
        dry_run (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If set, don't actually run this
            job. A valid query will return a mostly empty
            response with some processing statistics, while
            an invalid query will return the same error it
            would if it wasn't a dry run. Behavior of
            non-query jobs is undefined.
        job_timeout_ms (google.protobuf.wrappers_pb2.Int64Value):
            Optional. Job timeout in milliseconds. If
            this time limit is exceeded, BigQuery will
            attempt to stop a longer job, but may not always
            succeed in canceling it before the job
            completes. For example, a job that takes more
            than 60 seconds to complete has a better chance
            of being stopped than a job that takes 10
            seconds to complete.
        labels (MutableMapping[str, str]):
            The labels associated with this job. You can
            use these to organize and group your jobs.
            Label keys and values can be no longer than 63
            characters, can only contain lowercase letters,
            numeric characters, underscores and dashes.
            International characters are allowed. Label
            values are optional.  Label keys must start with
            a letter and each label in the list must have a
            different key.
        reservation (str):
            Optional. The reservation that job would use. User can
            specify a reservation to execute the job. If reservation is
            not set, reservation is determined based on the rules
            defined by the reservation assignments. The expected format
            is
            ``projects/{project}/locations/{location}/reservations/{reservation}``.

            This field is a member of `oneof`_ ``_reservation``.
    """

    job_type: str = proto.Field(
        proto.STRING,
        number=8,
    )
    query: "JobConfigurationQuery" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="JobConfigurationQuery",
    )
    load: "JobConfigurationLoad" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="JobConfigurationLoad",
    )
    copy: "JobConfigurationTableCopy" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="JobConfigurationTableCopy",
    )
    extract: "JobConfigurationExtract" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="JobConfigurationExtract",
    )
    dry_run: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.BoolValue,
    )
    job_timeout_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.Int64Value,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    reservation: str = proto.Field(
        proto.STRING,
        number=11,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
