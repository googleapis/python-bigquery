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
        "ErrorProto",
    },
)


class ErrorProto(proto.Message):
    r"""Error details.

    Attributes:
        reason (str):
            A short error code that summarizes the error.
        location (str):
            Specifies where the error occurred, if
            present.
        debug_info (str):
            Debugging information. This property is
            internal to Google and should not be used.
        message (str):
            A human-readable description of the error.
    """

    reason: str = proto.Field(
        proto.STRING,
        number=1,
    )
    location: str = proto.Field(
        proto.STRING,
        number=2,
    )
    debug_info: str = proto.Field(
        proto.STRING,
        number=3,
    )
    message: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
