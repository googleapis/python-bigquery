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
        "RangePartitioning",
    },
)


class RangePartitioning(proto.Message):
    r"""

    Attributes:
        field (str):
            Required. The name of the column to partition
            the table on. It must be a top-level, INT64
            column whose mode is NULLABLE or REQUIRED.
        range_ (google.cloud.bigquery_v2.types.RangePartitioning.Range):
            Defines the ranges for range partitioning.
    """

    class Range(proto.Message):
        r"""Defines the ranges for range partitioning.

        Attributes:
            start (str):
                Required. The start of range partitioning,
                inclusive. This field is an INT64 value
                represented as a string.
            end (str):
                Required. The end of range partitioning,
                exclusive. This field is an INT64 value
                represented as a string.
            interval (str):
                Required. The width of each interval. This
                field is an INT64 value represented as a string.
        """

        start: str = proto.Field(
            proto.STRING,
            number=1,
        )
        end: str = proto.Field(
            proto.STRING,
            number=2,
        )
        interval: str = proto.Field(
            proto.STRING,
            number=3,
        )

    field: str = proto.Field(
        proto.STRING,
        number=1,
    )
    range_: Range = proto.Field(
        proto.MESSAGE,
        number=2,
        message=Range,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
