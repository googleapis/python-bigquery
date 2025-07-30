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
        "RestrictionConfig",
    },
)


class RestrictionConfig(proto.Message):
    r"""

    Attributes:
        type_ (google.cloud.bigquery_v2.types.RestrictionConfig.RestrictionType):
            Output only. Specifies the type of
            dataset/table restriction.
    """

    class RestrictionType(proto.Enum):
        r"""RestrictionType specifies the type of dataset/table
        restriction.

        Values:
            RESTRICTION_TYPE_UNSPECIFIED (0):
                Should never be used.
            RESTRICTED_DATA_EGRESS (1):
                Restrict data egress. See `Data
                egress <https://cloud.google.com/bigquery/docs/analytics-hub-introduction#data_egress>`__
                for more details.
        """
        RESTRICTION_TYPE_UNSPECIFIED = 0
        RESTRICTED_DATA_EGRESS = 1

    type_: RestrictionType = proto.Field(
        proto.ENUM,
        number=1,
        enum=RestrictionType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
