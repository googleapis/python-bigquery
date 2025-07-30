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

from google.cloud.bigquery_v2.types import (
    decimal_target_types as gcb_decimal_target_types,
)
from google.cloud.bigquery_v2.types import file_set_specification_type
from google.cloud.bigquery_v2.types import hive_partitioning
from google.cloud.bigquery_v2.types import json_extension as gcb_json_extension
from google.cloud.bigquery_v2.types import map_target_type as gcb_map_target_type
from google.cloud.bigquery_v2.types import table_schema
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "AvroOptions",
        "ParquetOptions",
        "CsvOptions",
        "JsonOptions",
        "BigtableColumn",
        "BigtableColumnFamily",
        "BigtableOptions",
        "GoogleSheetsOptions",
        "ExternalDataConfiguration",
    },
)


class AvroOptions(proto.Message):
    r"""Options for external data sources.

    Attributes:
        use_avro_logical_types (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If sourceFormat is set to "AVRO",
            indicates whether to interpret logical types as
            the corresponding BigQuery data type (for
            example, TIMESTAMP), instead of using the raw
            type (for example, INTEGER).
    """

    use_avro_logical_types: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.BoolValue,
    )


class ParquetOptions(proto.Message):
    r"""Parquet Options for load and make external tables.

    Attributes:
        enum_as_string (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Indicates whether to infer Parquet
            ENUM logical type as STRING instead of BYTES by
            default.
        enable_list_inference (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Indicates whether to use schema
            inference specifically for Parquet LIST logical
            type.
        map_target_type (google.cloud.bigquery_v2.types.MapTargetType):
            Optional. Indicates how to represent a
            Parquet map if present.
    """

    enum_as_string: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.BoolValue,
    )
    enable_list_inference: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.BoolValue,
    )
    map_target_type: gcb_map_target_type.MapTargetType = proto.Field(
        proto.ENUM,
        number=3,
        enum=gcb_map_target_type.MapTargetType,
    )


class CsvOptions(proto.Message):
    r"""Information related to a CSV data source.

    Attributes:
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
        skip_leading_rows (google.protobuf.wrappers_pb2.Int64Value):
            Optional. The number of rows at the top of a CSV file that
            BigQuery will skip when reading the data. The default value
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
        quote (google.protobuf.wrappers_pb2.StringValue):
            Optional. The value that is used to quote
            data sections in a CSV file. BigQuery converts
            the string to ISO-8859-1 encoding, and then uses
            the first byte of the encoded string to split
            the data in its raw, binary state.
            The default value is a double-quote (").
            If your data does not contain quoted sections,
            set the property value to an empty string.
            If your data contains quoted newline characters,
            you must also set the allowQuotedNewlines
            property to true.
            To include the specific quote character within a
            quoted value, precede it with an additional
            matching quote character. For example, if you
            want to escape the default character  ' " ', use
            ' "" '.
        allow_quoted_newlines (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Indicates if BigQuery should allow
            quoted data sections that contain newline
            characters in a CSV file. The default value is
            false.
        allow_jagged_rows (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Indicates if BigQuery should accept
            rows that are missing trailing optional columns.
            If true, BigQuery treats missing trailing
            columns as null values.
            If false, records with missing trailing columns
            are treated as bad records, and if there are too
            many bad records, an invalid error is returned
            in the job result. The default value is false.
        encoding (str):
            Optional. The character encoding of the data.
            The supported values are UTF-8, ISO-8859-1,
            UTF-16BE, UTF-16LE, UTF-32BE, and UTF-32LE.  The
            default value is UTF-8.
            BigQuery decodes the data after the raw, binary
            data has been split using the values of the
            quote and fieldDelimiter properties.
        preserve_ascii_control_characters (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Indicates if the embedded ASCII
            control characters (the first 32 characters in
            the ASCII-table, from '\x00' to '\x1F') are
            preserved.
        null_marker (google.protobuf.wrappers_pb2.StringValue):
            Optional. Specifies a string that represents
            a null value in a CSV file. For example, if you
            specify "\N", BigQuery interprets "\N" as a null
            value when querying a CSV file.
            The default value is the empty string. If you
            set this property to a custom value, BigQuery
            throws an error if an empty string is present
            for all data types except for STRING and BYTE.
            For STRING and BYTE columns, BigQuery interprets
            the empty string as an empty value.
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
        source_column_match (str):
            Optional. Controls the strategy used to match
            loaded columns to the schema. If not set, a
            sensible default is chosen based on how the
            schema is provided. If autodetect is used, then
            columns are matched by name. Otherwise, columns
            are matched by position. This is done to keep
            the behavior backward-compatible. Acceptable
            values are:

              POSITION - matches by position. This assumes
            that the columns are ordered              the
            same way as the schema.
              NAME - matches by name. This reads the header
            row as column names and          reorders
            columns to match the field names in the schema.
    """

    field_delimiter: str = proto.Field(
        proto.STRING,
        number=1,
    )
    skip_leading_rows: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    quote: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.StringValue,
    )
    allow_quoted_newlines: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.BoolValue,
    )
    allow_jagged_rows: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.BoolValue,
    )
    encoding: str = proto.Field(
        proto.STRING,
        number=6,
    )
    preserve_ascii_control_characters: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.BoolValue,
    )
    null_marker: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=8,
        message=wrappers_pb2.StringValue,
    )
    null_markers: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    source_column_match: str = proto.Field(
        proto.STRING,
        number=10,
    )


class JsonOptions(proto.Message):
    r"""Json Options for load and make external tables.

    Attributes:
        encoding (str):
            Optional. The character encoding of the data.
            The supported values are UTF-8, UTF-16BE,
            UTF-16LE, UTF-32BE, and UTF-32LE.  The default
            value is UTF-8.
    """

    encoding: str = proto.Field(
        proto.STRING,
        number=1,
    )


class BigtableColumn(proto.Message):
    r"""Information related to a Bigtable column.

    Attributes:
        qualifier_encoded (google.protobuf.wrappers_pb2.BytesValue):
            [Required] Qualifier of the column. Columns in the parent
            column family that has this exact qualifier are exposed as
            ``<family field name>.<column field name>`` field. If the
            qualifier is valid UTF-8 string, it can be specified in the
            qualifier_string field. Otherwise, a base-64 encoded value
            must be set to qualifier_encoded. The column field name is
            the same as the column qualifier. However, if the qualifier
            is not a valid BigQuery field identifier i.e. does not match
            [a-zA-Z][a-zA-Z0-9_]*, a valid identifier must be provided
            as field_name.
        qualifier_string (google.protobuf.wrappers_pb2.StringValue):
            Qualifier string.
        field_name (str):
            Optional. If the qualifier is not a valid BigQuery field
            identifier i.e. does not match [a-zA-Z][a-zA-Z0-9_]*, a
            valid identifier must be provided as the column field name
            and is used as field name in queries.
        type_ (str):
            Optional. The type to convert the value in cells of this
            column. The values are expected to be encoded using HBase
            Bytes.toBytes function when using the BINARY encoding value.
            Following BigQuery types are allowed (case-sensitive):

            -  BYTES
            -  STRING
            -  INTEGER
            -  FLOAT
            -  BOOLEAN
            -  JSON

            Default type is BYTES. 'type' can also be set at the column
            family level. However, the setting at this level takes
            precedence if 'type' is set at both levels.
        encoding (str):
            Optional. The encoding of the values when the
            type is not STRING. Acceptable encoding values
            are:

              TEXT - indicates values are alphanumeric text
            strings.   BINARY - indicates values are encoded
            using HBase Bytes.toBytes family of
            functions.
            'encoding' can also be set at the column family
            level. However, the setting at this level takes
            precedence if 'encoding' is set at both levels.
        only_read_latest (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If this is set, only the latest
            version of value in this column             are
            exposed. 'onlyReadLatest' can also be set at the
            column family level. However, the setting at
            this level takes precedence if 'onlyReadLatest'
            is set at both levels.
    """

    qualifier_encoded: wrappers_pb2.BytesValue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.BytesValue,
    )
    qualifier_string: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.StringValue,
    )
    field_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=4,
    )
    encoding: str = proto.Field(
        proto.STRING,
        number=5,
    )
    only_read_latest: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.BoolValue,
    )


class BigtableColumnFamily(proto.Message):
    r"""Information related to a Bigtable column family.

    Attributes:
        family_id (str):
            Identifier of the column family.
        type_ (str):
            Optional. The type to convert the value in cells of this
            column family. The values are expected to be encoded using
            HBase Bytes.toBytes function when using the BINARY encoding
            value. Following BigQuery types are allowed
            (case-sensitive):

            -  BYTES
            -  STRING
            -  INTEGER
            -  FLOAT
            -  BOOLEAN
            -  JSON

            Default type is BYTES. This can be overridden for a specific
            column by listing that column in 'columns' and specifying a
            type for it.
        encoding (str):
            Optional. The encoding of the values when the
            type is not STRING. Acceptable encoding values
            are:

              TEXT - indicates values are alphanumeric text
            strings.   BINARY - indicates values are encoded
            using HBase Bytes.toBytes family of
            functions.
            This can be overridden for a specific column by
            listing that column in 'columns' and specifying
            an encoding for it.
        columns (MutableSequence[google.cloud.bigquery_v2.types.BigtableColumn]):
            Optional. Lists of columns that should be exposed as
            individual fields as opposed to a list of (column name,
            value) pairs. All columns whose qualifier matches a
            qualifier in this list can be accessed as
            ``<family field name>.<column field name>``. Other columns
            can be accessed as a list through the
            ``<family field name>.Column`` field.
        only_read_latest (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If this is set only the latest
            version of value are exposed for all columns in
            this column family. This can be overridden for a
            specific column by listing that column in
            'columns' and specifying a different setting
            for that column.
    """

    family_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=2,
    )
    encoding: str = proto.Field(
        proto.STRING,
        number=3,
    )
    columns: MutableSequence["BigtableColumn"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="BigtableColumn",
    )
    only_read_latest: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.BoolValue,
    )


class BigtableOptions(proto.Message):
    r"""Options specific to Google Cloud Bigtable data sources.

    Attributes:
        column_families (MutableSequence[google.cloud.bigquery_v2.types.BigtableColumnFamily]):
            Optional. List of column families to expose
            in the table schema along with their types.
            This list restricts the column families that can
            be referenced in queries and specifies their
            value types.
            You can use this list to do type conversions -
            see the 'type' field for more details.
            If you leave this list empty, all column
            families are present in the table schema and
            their values are read as BYTES.
            During a query only the column families
            referenced in that query are read from Bigtable.
        ignore_unspecified_column_families (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If field is true, then the column
            families that are not specified in
            columnFamilies list are not exposed in the table
            schema. Otherwise, they are read with BYTES type
            values. The default value is false.
        read_rowkey_as_string (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If field is true, then the rowkey
            column families will be read and converted to
            string. Otherwise they are read with BYTES type
            values and users need to manually cast them with
            CAST if necessary. The default value is false.
        output_column_families_as_json (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If field is true, then each column
            family will be read as a single JSON column.
            Otherwise they are read as a repeated cell
            structure containing timestamp/value tuples. The
            default value is false.
    """

    column_families: MutableSequence["BigtableColumnFamily"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BigtableColumnFamily",
    )
    ignore_unspecified_column_families: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.BoolValue,
    )
    read_rowkey_as_string: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.BoolValue,
    )
    output_column_families_as_json: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.BoolValue,
    )


class GoogleSheetsOptions(proto.Message):
    r"""Options specific to Google Sheets data sources.

    Attributes:
        skip_leading_rows (google.protobuf.wrappers_pb2.Int64Value):
            Optional. The number of rows at the top of a sheet that
            BigQuery will skip when reading the data. The default value
            is 0. This property is useful if you have header rows that
            should be skipped. When autodetect is on, the behavior is
            the following:

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
        range_ (str):
            Optional. Range of a sheet to query from. Only used when
            non-empty. Typical format:
            sheet_name!top_left_cell_id:bottom_right_cell_id For
            example: sheet1!A1:B20
    """

    skip_leading_rows: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.Int64Value,
    )
    range_: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ExternalDataConfiguration(proto.Message):
    r"""

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
            table. For Google Cloud Datastore backups, exactly one URI
            can be specified. Also, the '*' wildcard character is not
            allowed.
        file_set_spec_type (google.cloud.bigquery_v2.types.FileSetSpecType):
            Optional. Specifies how source URIs are
            interpreted for constructing the file set to
            load.  By default source URIs are expanded
            against the underlying storage.  Other options
            include specifying manifest files. Only
            applicable to object storage systems.
        schema (google.cloud.bigquery_v2.types.TableSchema):
            Optional. The schema for the data.
            Schema is required for CSV and JSON formats if
            autodetect is not on. Schema is disallowed for
            Google Cloud Bigtable, Cloud Datastore backups,
            Avro, ORC and Parquet formats.
        source_format (str):
            [Required] The data format. For CSV files, specify "CSV".
            For Google sheets, specify "GOOGLE_SHEETS". For
            newline-delimited JSON, specify "NEWLINE_DELIMITED_JSON".
            For Avro files, specify "AVRO". For Google Cloud Datastore
            backups, specify "DATASTORE_BACKUP". For Apache Iceberg
            tables, specify "ICEBERG". For ORC files, specify "ORC". For
            Parquet files, specify "PARQUET". [Beta] For Google Cloud
            Bigtable, specify "BIGTABLE".
        max_bad_records (google.protobuf.wrappers_pb2.Int32Value):
            Optional. The maximum number of bad records
            that BigQuery can ignore when reading data. If
            the number of bad records exceeds this value, an
            invalid error is returned in the job result. The
            default value is 0, which requires that all
            records are valid. This setting is ignored for
            Google Cloud Bigtable, Google Cloud Datastore
            backups, Avro, ORC and Parquet formats.
        autodetect (google.protobuf.wrappers_pb2.BoolValue):
            Try to detect schema and format options
            automatically. Any option specified explicitly
            will be honored.
        ignore_unknown_values (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Indicates if BigQuery should allow
            extra values that are not represented in the
            table schema. If true, the extra values are
            ignored.
            If false, records with extra columns are treated
            as bad records, and if there are too many bad
            records, an invalid error is returned in the job
            result.
            The default value is false.
            The sourceFormat property determines what
            BigQuery treats as an extra value:

              CSV: Trailing columns
              JSON: Named values that don't match any column
            names   Google Cloud Bigtable: This setting is
            ignored.   Google Cloud Datastore backups: This
            setting is ignored.   Avro: This setting is
            ignored.
              ORC: This setting is ignored.
              Parquet: This setting is ignored.
        compression (str):
            Optional. The compression type of the data
            source. Possible values include GZIP and NONE.
            The default value is NONE. This setting is
            ignored for Google Cloud Bigtable, Google Cloud
            Datastore backups, Avro, ORC and Parquet
            formats. An empty string is an invalid value.
        csv_options (google.cloud.bigquery_v2.types.CsvOptions):
            Optional. Additional properties to set if
            sourceFormat is set to CSV.
        json_options (google.cloud.bigquery_v2.types.JsonOptions):
            Optional. Additional properties to set if
            sourceFormat is set to JSON.
        bigtable_options (google.cloud.bigquery_v2.types.BigtableOptions):
            Optional. Additional options if sourceFormat
            is set to BIGTABLE.
        google_sheets_options (google.cloud.bigquery_v2.types.GoogleSheetsOptions):
            Optional. Additional options if sourceFormat is set to
            GOOGLE_SHEETS.
        hive_partitioning_options (google.cloud.bigquery_v2.types.HivePartitioningOptions):
            Optional. When set, configures hive
            partitioning support. Not all storage formats
            support hive partitioning -- requesting hive
            partitioning on an unsupported format will lead
            to an error, as will providing an invalid
            specification.
        connection_id (str):
            Optional. The connection specifying the credentials to be
            used to read external storage, such as Azure Blob, Cloud
            Storage, or S3. The connection_id can have the form
            ``{project_id}.{location_id};{connection_id}`` or
            ``projects/{project_id}/locations/{location_id}/connections/{connection_id}``.
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
        avro_options (google.cloud.bigquery_v2.types.AvroOptions):
            Optional. Additional properties to set if
            sourceFormat is set to AVRO.
        json_extension (google.cloud.bigquery_v2.types.JsonExtension):
            Optional. Load option to be used together with source_format
            newline-delimited JSON to indicate that a variant of JSON is
            being loaded. To load newline-delimited GeoJSON, specify
            GEOJSON (and source_format must be set to
            NEWLINE_DELIMITED_JSON).
        parquet_options (google.cloud.bigquery_v2.types.ParquetOptions):
            Optional. Additional properties to set if
            sourceFormat is set to PARQUET.
        object_metadata (google.cloud.bigquery_v2.types.ExternalDataConfiguration.ObjectMetadata):
            Optional. ObjectMetadata is used to create Object Tables.
            Object Tables contain a listing of objects (with their
            metadata) found at the source_uris. If ObjectMetadata is
            set, source_format should be omitted.

            Currently SIMPLE is the only supported Object Metadata type.

            This field is a member of `oneof`_ ``_object_metadata``.
        reference_file_schema_uri (google.protobuf.wrappers_pb2.StringValue):
            Optional. When creating an external table,
            the user can provide a reference file with the
            table schema. This is enabled for the following
            formats:
            AVRO, PARQUET, ORC.
        metadata_cache_mode (google.cloud.bigquery_v2.types.ExternalDataConfiguration.MetadataCacheMode):
            Optional. Metadata Cache Mode for the table.
            Set this to enable caching of metadata from
            external data source.
        time_zone (str):
            Optional. Time zone used when parsing timestamp values that
            do not have specific time zone information (e.g. 2024-04-20
            12:34:56). The expected format is a IANA timezone string
            (e.g. America/Los_Angeles).

            This field is a member of `oneof`_ ``_time_zone``.
        date_format (str):
            Optional. Format used to parse DATE values.
            Supports C-style and SQL-style values.

            This field is a member of `oneof`_ ``_date_format``.
        datetime_format (str):
            Optional. Format used to parse DATETIME
            values. Supports C-style and SQL-style values.

            This field is a member of `oneof`_ ``_datetime_format``.
        time_format (str):
            Optional. Format used to parse TIME values.
            Supports C-style and SQL-style values.

            This field is a member of `oneof`_ ``_time_format``.
        timestamp_format (str):
            Optional. Format used to parse TIMESTAMP
            values. Supports C-style and SQL-style values.

            This field is a member of `oneof`_ ``_timestamp_format``.
    """

    class ObjectMetadata(proto.Enum):
        r"""Supported Object Metadata Types.

        Values:
            OBJECT_METADATA_UNSPECIFIED (0):
                Unspecified by default.
            DIRECTORY (1):
                A synonym for ``SIMPLE``.
            SIMPLE (2):
                Directory listing of objects.
        """
        OBJECT_METADATA_UNSPECIFIED = 0
        DIRECTORY = 1
        SIMPLE = 2

    class MetadataCacheMode(proto.Enum):
        r"""MetadataCacheMode identifies if the table should use metadata
        caching for files from external source (eg Google Cloud
        Storage).

        Values:
            METADATA_CACHE_MODE_UNSPECIFIED (0):
                Unspecified metadata cache mode.
            AUTOMATIC (1):
                Set this mode to trigger automatic background
                refresh of metadata cache from the external
                source. Queries will use the latest available
                cache version within the table's maxStaleness
                interval.
            MANUAL (2):
                Set this mode to enable triggering manual
                refresh of the metadata cache from external
                source. Queries will use the latest manually
                triggered cache version within the table's
                maxStaleness interval.
        """
        METADATA_CACHE_MODE_UNSPECIFIED = 0
        AUTOMATIC = 1
        MANUAL = 2

    source_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    file_set_spec_type: file_set_specification_type.FileSetSpecType = proto.Field(
        proto.ENUM,
        number=25,
        enum=file_set_specification_type.FileSetSpecType,
    )
    schema: table_schema.TableSchema = proto.Field(
        proto.MESSAGE,
        number=2,
        message=table_schema.TableSchema,
    )
    source_format: str = proto.Field(
        proto.STRING,
        number=3,
    )
    max_bad_records: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.Int32Value,
    )
    autodetect: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.BoolValue,
    )
    ignore_unknown_values: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.BoolValue,
    )
    compression: str = proto.Field(
        proto.STRING,
        number=7,
    )
    csv_options: "CsvOptions" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="CsvOptions",
    )
    json_options: "JsonOptions" = proto.Field(
        proto.MESSAGE,
        number=26,
        message="JsonOptions",
    )
    bigtable_options: "BigtableOptions" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="BigtableOptions",
    )
    google_sheets_options: "GoogleSheetsOptions" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="GoogleSheetsOptions",
    )
    hive_partitioning_options: hive_partitioning.HivePartitioningOptions = proto.Field(
        proto.MESSAGE,
        number=13,
        message=hive_partitioning.HivePartitioningOptions,
    )
    connection_id: str = proto.Field(
        proto.STRING,
        number=14,
    )
    decimal_target_types: MutableSequence[
        gcb_decimal_target_types.DecimalTargetType
    ] = proto.RepeatedField(
        proto.ENUM,
        number=16,
        enum=gcb_decimal_target_types.DecimalTargetType,
    )
    avro_options: "AvroOptions" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="AvroOptions",
    )
    json_extension: gcb_json_extension.JsonExtension = proto.Field(
        proto.ENUM,
        number=18,
        enum=gcb_json_extension.JsonExtension,
    )
    parquet_options: "ParquetOptions" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="ParquetOptions",
    )
    object_metadata: ObjectMetadata = proto.Field(
        proto.ENUM,
        number=22,
        optional=True,
        enum=ObjectMetadata,
    )
    reference_file_schema_uri: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=23,
        message=wrappers_pb2.StringValue,
    )
    metadata_cache_mode: MetadataCacheMode = proto.Field(
        proto.ENUM,
        number=24,
        enum=MetadataCacheMode,
    )
    time_zone: str = proto.Field(
        proto.STRING,
        number=27,
        optional=True,
    )
    date_format: str = proto.Field(
        proto.STRING,
        number=28,
        optional=True,
    )
    datetime_format: str = proto.Field(
        proto.STRING,
        number=29,
        optional=True,
    )
    time_format: str = proto.Field(
        proto.STRING,
        number=30,
        optional=True,
    )
    timestamp_format: str = proto.Field(
        proto.STRING,
        number=31,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
