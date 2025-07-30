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
        "StandardSqlDataType",
        "StandardSqlField",
        "StandardSqlStructType",
        "StandardSqlTableType",
    },
)


class StandardSqlDataType(proto.Message):
    r"""The data type of a variable such as a function argument. Examples
    include:

    -  INT64: ``{"typeKind": "INT64"}``

    -  ARRAY:

       { "typeKind": "ARRAY", "arrayElementType": {"typeKind": "STRING"}
       }

    -  STRUCT<x STRING, y ARRAY>:

       { "typeKind": "STRUCT", "structType": { "fields": [ { "name":
       "x", "type": {"typeKind": "STRING"} }, { "name": "y", "type": {
       "typeKind": "ARRAY", "arrayElementType": {"typeKind": "DATE"} } }
       ] } }

    -  RANGE:

       { "typeKind": "RANGE", "rangeElementType": {"typeKind": "DATE"} }

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        type_kind (google.cloud.bigquery_v2.types.StandardSqlDataType.TypeKind):
            Required. The top level type of this field.
            Can be any GoogleSQL data type (e.g., "INT64",
            "DATE", "ARRAY").
        array_element_type (google.cloud.bigquery_v2.types.StandardSqlDataType):
            The type of the array's elements, if type_kind = "ARRAY".

            This field is a member of `oneof`_ ``sub_type``.
        struct_type (google.cloud.bigquery_v2.types.StandardSqlStructType):
            The fields of this struct, in order, if type_kind =
            "STRUCT".

            This field is a member of `oneof`_ ``sub_type``.
        range_element_type (google.cloud.bigquery_v2.types.StandardSqlDataType):
            The type of the range's elements, if type_kind = "RANGE".

            This field is a member of `oneof`_ ``sub_type``.
    """

    class TypeKind(proto.Enum):
        r"""The kind of the datatype.

        Values:
            TYPE_KIND_UNSPECIFIED (0):
                Invalid type.
            INT64 (2):
                Encoded as a string in decimal format.
            BOOL (5):
                Encoded as a boolean "false" or "true".
            FLOAT64 (7):
                Encoded as a number, or string "NaN",
                "Infinity" or "-Infinity".
            STRING (8):
                Encoded as a string value.
            BYTES (9):
                Encoded as a base64 string per RFC 4648,
                section 4.
            TIMESTAMP (19):
                Encoded as an RFC 3339 timestamp with
                mandatory "Z" time zone string:
                1985-04-12T23:20:50.52Z
            DATE (10):
                Encoded as RFC 3339 full-date format string:
                1985-04-12
            TIME (20):
                Encoded as RFC 3339 partial-time format
                string: 23:20:50.52
            DATETIME (21):
                Encoded as RFC 3339 full-date "T"
                partial-time: 1985-04-12T23:20:50.52
            INTERVAL (26):
                Encoded as fully qualified 3 part: 0-5 15
                2:30:45.6
            GEOGRAPHY (22):
                Encoded as WKT
            NUMERIC (23):
                Encoded as a decimal string.
            BIGNUMERIC (24):
                Encoded as a decimal string.
            JSON (25):
                Encoded as a string.
            ARRAY (16):
                Encoded as a list with types matching Type.array_type.
            STRUCT (17):
                Encoded as a list with fields of type Type.struct_type[i].
                List is used because a JSON object cannot have duplicate
                field names.
            RANGE (29):
                Encoded as a pair with types matching range_element_type.
                Pairs must begin with "[", end with ")", and be separated by
                ", ".
        """
        TYPE_KIND_UNSPECIFIED = 0
        INT64 = 2
        BOOL = 5
        FLOAT64 = 7
        STRING = 8
        BYTES = 9
        TIMESTAMP = 19
        DATE = 10
        TIME = 20
        DATETIME = 21
        INTERVAL = 26
        GEOGRAPHY = 22
        NUMERIC = 23
        BIGNUMERIC = 24
        JSON = 25
        ARRAY = 16
        STRUCT = 17
        RANGE = 29

    type_kind: TypeKind = proto.Field(
        proto.ENUM,
        number=1,
        enum=TypeKind,
    )
    array_element_type: "StandardSqlDataType" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="sub_type",
        message="StandardSqlDataType",
    )
    struct_type: "StandardSqlStructType" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="sub_type",
        message="StandardSqlStructType",
    )
    range_element_type: "StandardSqlDataType" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="sub_type",
        message="StandardSqlDataType",
    )


class StandardSqlField(proto.Message):
    r"""A field or a column.

    Attributes:
        name (str):
            Optional. The name of this field. Can be
            absent for struct fields.
        type_ (google.cloud.bigquery_v2.types.StandardSqlDataType):
            Optional. The type of this parameter. Absent
            if not explicitly specified (e.g., CREATE
            FUNCTION statement can omit the return type; in
            this case the output parameter does not have
            this "type" field).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: "StandardSqlDataType" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="StandardSqlDataType",
    )


class StandardSqlStructType(proto.Message):
    r"""The representation of a SQL STRUCT type.

    Attributes:
        fields (MutableSequence[google.cloud.bigquery_v2.types.StandardSqlField]):
            Fields within the struct.
    """

    fields: MutableSequence["StandardSqlField"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="StandardSqlField",
    )


class StandardSqlTableType(proto.Message):
    r"""A table type

    Attributes:
        columns (MutableSequence[google.cloud.bigquery_v2.types.StandardSqlField]):
            The columns in this table type
    """

    columns: MutableSequence["StandardSqlField"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="StandardSqlField",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
