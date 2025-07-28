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

from google.cloud.bigquery_v2.types import table_reference


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "PrimaryKey",
        "ColumnReference",
        "ForeignKey",
        "TableConstraints",
    },
)


class PrimaryKey(proto.Message):
    r"""Represents the primary key constraint on a table's columns.

    Attributes:
        columns (MutableSequence[str]):
            Required. The columns that are composed of
            the primary key constraint.
    """

    columns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class ColumnReference(proto.Message):
    r"""The pair of the foreign key column and primary key column.

    Attributes:
        referencing_column (str):
            Required. The column that composes the
            foreign key.
        referenced_column (str):
            Required. The column in the primary key that are referenced
            by the referencing_column.
    """

    referencing_column: str = proto.Field(
        proto.STRING,
        number=1,
    )
    referenced_column: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ForeignKey(proto.Message):
    r"""Represents a foreign key constraint on a table's columns.

    Attributes:
        name (str):
            Optional. Set only if the foreign key
            constraint is named.
        referenced_table (google.cloud.bigquery_v2.types.TableReference):
            Required. The table that holds the primary
            key and is referenced by this foreign key.
        column_references (MutableSequence[google.cloud.bigquery_v2.types.ColumnReference]):
            Required. The columns that compose the
            foreign key.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    referenced_table: table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=2,
        message=table_reference.TableReference,
    )
    column_references: MutableSequence["ColumnReference"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="ColumnReference",
    )


class TableConstraints(proto.Message):
    r"""The TableConstraints defines the primary key and foreign key.

    Attributes:
        primary_key (google.cloud.bigquery_v2.types.PrimaryKey):
            Optional. Represents a primary key constraint
            on a table's columns. Present only if the table
            has a primary key. The primary key is not
            enforced.
        foreign_keys (MutableSequence[google.cloud.bigquery_v2.types.ForeignKey]):
            Optional. Present only if the table has a
            foreign key. The foreign key is not enforced.
    """

    primary_key: "PrimaryKey" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PrimaryKey",
    )
    foreign_keys: MutableSequence["ForeignKey"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="ForeignKey",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
