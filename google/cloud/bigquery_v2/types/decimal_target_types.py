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
        "DecimalTargetType",
    },
)


class DecimalTargetType(proto.Enum):
    r"""The data types that could be used as a target type when
    converting decimal values.

    Values:
        DECIMAL_TARGET_TYPE_UNSPECIFIED (0):
            Invalid type.
        NUMERIC (1):
            Decimal values could be converted to NUMERIC
            type.
        BIGNUMERIC (2):
            Decimal values could be converted to
            BIGNUMERIC type.
        STRING (3):
            Decimal values could be converted to STRING
            type.
    """
    DECIMAL_TARGET_TYPE_UNSPECIFIED = 0
    NUMERIC = 1
    BIGNUMERIC = 2
    STRING = 3


__all__ = tuple(sorted(__protobuf__.manifest))
