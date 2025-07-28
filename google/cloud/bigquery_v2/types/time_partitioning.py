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

from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "TimePartitioning",
    },
)


class TimePartitioning(proto.Message):
    r"""

    Attributes:
        type_ (str):
            Required. The supported types are DAY, HOUR,
            MONTH, and YEAR, which will generate one
            partition per day, hour, month, and year,
            respectively.
        expiration_ms (google.protobuf.wrappers_pb2.Int64Value):
            Optional. Number of milliseconds for which to
            keep the storage for a partition.
            A wrapper is used here because 0 is an invalid
            value.
        field (google.protobuf.wrappers_pb2.StringValue):
            Optional. If not set, the table is partitioned by pseudo
            column '_PARTITIONTIME'; if set, the table is partitioned by
            this field. The field must be a top-level TIMESTAMP or DATE
            field. Its mode must be NULLABLE or REQUIRED. A wrapper is
            used here because an empty string is an invalid value.
    """

    type_: str = proto.Field(
        proto.STRING,
        number=1,
    )
    expiration_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    field: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
