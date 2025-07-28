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
        "MapTargetType",
    },
)


class MapTargetType(proto.Enum):
    r"""Indicates the map target type. Only applies to parquet maps.

    Values:
        MAP_TARGET_TYPE_UNSPECIFIED (0):
            In this mode, the map will have the following schema: struct
            map_field_name { repeated struct key_value { key value } }.
        ARRAY_OF_STRUCT (1):
            In this mode, the map will have the following schema:
            repeated struct map_field_name { key value }.
    """
    MAP_TARGET_TYPE_UNSPECIFIED = 0
    ARRAY_OF_STRUCT = 1


__all__ = tuple(sorted(__protobuf__.manifest))
