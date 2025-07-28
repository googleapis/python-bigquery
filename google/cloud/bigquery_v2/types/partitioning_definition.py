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
        "PartitioningDefinition",
        "PartitionedColumn",
    },
)


class PartitioningDefinition(proto.Message):
    r"""The partitioning information, which includes managed table,
    external table and metastore partitioned table partition
    information.

    Attributes:
        partitioned_column (MutableSequence[google.cloud.bigquery_v2.types.PartitionedColumn]):
            Optional. Details about each partitioning column. This field
            is output only for all partitioning types other than
            metastore partitioned tables. BigQuery native tables only
            support 1 partitioning column. Other table types may support
            0, 1 or more partitioning columns. For metastore partitioned
            tables, the order must match the definition order in the
            Hive Metastore, where it must match the physical layout of
            the table. For example,

            CREATE TABLE a_table(id BIGINT, name STRING) PARTITIONED BY
            (city STRING, state STRING).

            In this case the values must be ['city', 'state'] in that
            order.
    """

    partitioned_column: MutableSequence["PartitionedColumn"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="PartitionedColumn",
    )


class PartitionedColumn(proto.Message):
    r"""The partitioning column information.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        field (str):
            Required. The name of the partition column.

            This field is a member of `oneof`_ ``_field``.
    """

    field: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
