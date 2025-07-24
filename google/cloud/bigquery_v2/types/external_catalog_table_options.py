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
        "ExternalCatalogTableOptions",
        "StorageDescriptor",
        "SerDeInfo",
    },
)


class ExternalCatalogTableOptions(proto.Message):
    r"""Metadata about open source compatible table. The fields
    contained in these options correspond to Hive metastore's
    table-level properties.

    Attributes:
        parameters (MutableMapping[str, str]):
            Optional. A map of the key-value pairs
            defining the parameters and properties of the
            open source table. Corresponds with Hive
            metastore table parameters. Maximum size of
            4MiB.
        storage_descriptor (google.cloud.bigquery_v2.types.StorageDescriptor):
            Optional. A storage descriptor containing
            information about the physical storage of this
            table.
        connection_id (str):
            Optional. A connection ID that specifies the credentials to
            be used to read external storage, such as Azure Blob, Cloud
            Storage, or Amazon S3. This connection is needed to read the
            open source table from BigQuery. The connection_id format
            must be either
            ``<project_id>.<location_id>.<connection_id>`` or
            ``projects/<project_id>/locations/<location_id>/connections/<connection_id>``.
    """

    parameters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )
    storage_descriptor: "StorageDescriptor" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="StorageDescriptor",
    )
    connection_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class StorageDescriptor(proto.Message):
    r"""Contains information about how a table's data is stored and
    accessed by open source query engines.

    Attributes:
        location_uri (str):
            Optional. The physical location of the table (e.g.
            ``gs://spark-dataproc-data/pangea-data/case_sensitive/`` or
            ``gs://spark-dataproc-data/pangea-data/*``). The maximum
            length is 2056 bytes.
        input_format (str):
            Optional. Specifies the fully qualified class
            name of the InputFormat (e.g.
            "org.apache.hadoop.hive.ql.io.orc.OrcInputFormat").
            The maximum length is 128 characters.
        output_format (str):
            Optional. Specifies the fully qualified class
            name of the OutputFormat (e.g.
            "org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat").
            The maximum length is 128 characters.
        serde_info (google.cloud.bigquery_v2.types.SerDeInfo):
            Optional. Serializer and deserializer
            information.
    """

    location_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    input_format: str = proto.Field(
        proto.STRING,
        number=2,
    )
    output_format: str = proto.Field(
        proto.STRING,
        number=3,
    )
    serde_info: "SerDeInfo" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="SerDeInfo",
    )


class SerDeInfo(proto.Message):
    r"""Serializer and deserializer information.

    Attributes:
        name (str):
            Optional. Name of the SerDe.
            The maximum length is 256 characters.
        serialization_library (str):
            Required. Specifies a fully-qualified class
            name of the serialization library that is
            responsible for the translation of data between
            table representation and the underlying
            low-level input and output format structures.
            The maximum length is 256 characters.
        parameters (MutableMapping[str, str]):
            Optional. Key-value pairs that define the
            initialization parameters for the serialization
            library. Maximum size 10 Kib.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    serialization_library: str = proto.Field(
        proto.STRING,
        number=2,
    )
    parameters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
