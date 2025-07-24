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

from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "QueryParameterStructType",
        "QueryParameterType",
        "RangeValue",
        "QueryParameterValue",
        "QueryParameter",
    },
)


class QueryParameterStructType(proto.Message):
    r"""The type of a struct parameter.

    Attributes:
        name (str):
            Optional. The name of this field.
        type_ (google.cloud.bigquery_v2.types.QueryParameterType):
            Required. The type of this field.
        description (str):
            Optional. Human-oriented description of the
            field.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: "QueryParameterType" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="QueryParameterType",
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )


class QueryParameterType(proto.Message):
    r"""The type of a query parameter.

    Attributes:
        type_ (str):
            Required. The top level type of this field.
        array_type (google.cloud.bigquery_v2.types.QueryParameterType):
            Optional. The type of the array's elements,
            if this is an array.
        struct_types (MutableSequence[google.cloud.bigquery_v2.types.QueryParameterStructType]):
            Optional. The types of the fields of this
            struct, in order, if this is a struct.
        range_element_type (google.cloud.bigquery_v2.types.QueryParameterType):
            Optional. The element type of the range, if
            this is a range.
    """

    type_: str = proto.Field(
        proto.STRING,
        number=1,
    )
    array_type: "QueryParameterType" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="QueryParameterType",
    )
    struct_types: MutableSequence["QueryParameterStructType"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="QueryParameterStructType",
    )
    range_element_type: "QueryParameterType" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="QueryParameterType",
    )


class RangeValue(proto.Message):
    r"""Represents the value of a range.

    Attributes:
        start (google.cloud.bigquery_v2.types.QueryParameterValue):
            Optional. The start value of the range. A
            missing value represents an unbounded start.
        end (google.cloud.bigquery_v2.types.QueryParameterValue):
            Optional. The end value of the range. A
            missing value represents an unbounded end.
    """

    start: "QueryParameterValue" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="QueryParameterValue",
    )
    end: "QueryParameterValue" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="QueryParameterValue",
    )


class QueryParameterValue(proto.Message):
    r"""The value of a query parameter.

    Attributes:
        value (google.protobuf.wrappers_pb2.StringValue):
            Optional. The value of this value, if a
            simple scalar type.
        array_values (MutableSequence[google.cloud.bigquery_v2.types.QueryParameterValue]):
            Optional. The array values, if this is an
            array type.
        struct_values (MutableMapping[str, google.cloud.bigquery_v2.types.QueryParameterValue]):
            The struct field values.
        range_value (google.cloud.bigquery_v2.types.RangeValue):
            Optional. The range value, if this is a range
            type.
        alt_struct_values (MutableSequence[google.protobuf.struct_pb2.Value]):
            This field should not be used.
    """

    value: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.StringValue,
    )
    array_values: MutableSequence["QueryParameterValue"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="QueryParameterValue",
    )
    struct_values: MutableMapping[str, "QueryParameterValue"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=3,
        message="QueryParameterValue",
    )
    range_value: "RangeValue" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="RangeValue",
    )
    alt_struct_values: MutableSequence[struct_pb2.Value] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Value,
    )


class QueryParameter(proto.Message):
    r"""A parameter given to a query.

    Attributes:
        name (str):
            Optional. If unset, this is a positional
            parameter. Otherwise, should be unique within a
            query.
        parameter_type (google.cloud.bigquery_v2.types.QueryParameterType):
            Required. The type of this parameter.
        parameter_value (google.cloud.bigquery_v2.types.QueryParameterValue):
            Required. The value of this parameter.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    parameter_type: "QueryParameterType" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="QueryParameterType",
    )
    parameter_value: "QueryParameterValue" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="QueryParameterValue",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
