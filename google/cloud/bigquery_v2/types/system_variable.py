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

from google.cloud.bigquery_v2.types import standard_sql
from google.protobuf import struct_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "SystemVariables",
    },
)


class SystemVariables(proto.Message):
    r"""System variables given to a query.

    Attributes:
        types (MutableMapping[str, google.cloud.bigquery_v2.types.StandardSqlDataType]):
            Output only. Data type for each system
            variable.
        values (google.protobuf.struct_pb2.Struct):
            Output only. Value for each system variable.
    """

    types: MutableMapping[str, standard_sql.StandardSqlDataType] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=1,
        message=standard_sql.StandardSqlDataType,
    )
    values: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
