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
        "ManagedTableType",
    },
)


class ManagedTableType(proto.Enum):
    r"""The classification of managed table types that can be
    created.

    Values:
        MANAGED_TABLE_TYPE_UNSPECIFIED (0):
            No managed table type specified.
        NATIVE (1):
            The managed table is a native BigQuery table.
        BIGLAKE (2):
            The managed table is a BigLake table for
            Apache Iceberg in BigQuery.
    """
    MANAGED_TABLE_TYPE_UNSPECIFIED = 0
    NATIVE = 1
    BIGLAKE = 2


__all__ = tuple(sorted(__protobuf__.manifest))
