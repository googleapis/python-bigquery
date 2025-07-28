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


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "BigLakeConfiguration",
    },
)


class BigLakeConfiguration(proto.Message):
    r"""Configuration for BigQuery tables for Apache Iceberg
    (formerly BigLake managed tables.)

    Attributes:
        connection_id (str):
            Optional. The connection specifying the credentials to be
            used to read and write to external storage, such as Cloud
            Storage. The connection_id can have the form
            ``{project}.{location}.{connection_id}`` or
            \`projects/{project}/locations/{location}/connections/{connection_id}".
        storage_uri (str):
            Optional. The fully qualified location prefix of the
            external folder where table data is stored. The '*' wildcard
            character is not allowed. The URI should be in the format
            ``gs://bucket/path_to_table/``
        file_format (google.cloud.bigquery_v2.types.BigLakeConfiguration.FileFormat):
            Optional. The file format the table data is
            stored in.
        table_format (google.cloud.bigquery_v2.types.BigLakeConfiguration.TableFormat):
            Optional. The table format the metadata only
            snapshots are stored in.
    """

    class FileFormat(proto.Enum):
        r"""Supported file formats for BigQuery tables for Apache
        Iceberg.

        Values:
            FILE_FORMAT_UNSPECIFIED (0):
                Default Value.
            PARQUET (1):
                Apache Parquet format.
        """
        FILE_FORMAT_UNSPECIFIED = 0
        PARQUET = 1

    class TableFormat(proto.Enum):
        r"""Supported table formats for BigQuery tables for Apache
        Iceberg.

        Values:
            TABLE_FORMAT_UNSPECIFIED (0):
                Default Value.
            ICEBERG (1):
                Apache Iceberg format.
        """
        TABLE_FORMAT_UNSPECIFIED = 0
        ICEBERG = 1

    connection_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    storage_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    file_format: FileFormat = proto.Field(
        proto.ENUM,
        number=3,
        enum=FileFormat,
    )
    table_format: TableFormat = proto.Field(
        proto.ENUM,
        number=4,
        enum=TableFormat,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
