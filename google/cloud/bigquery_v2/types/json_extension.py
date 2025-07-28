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
        "JsonExtension",
    },
)


class JsonExtension(proto.Enum):
    r"""Used to indicate that a JSON variant, rather than normal JSON, is
    being used as the source_format. This should only be used in
    combination with the JSON source format.

    Values:
        JSON_EXTENSION_UNSPECIFIED (0):
            The default if provided value is not one
            included in the enum, or the value is not
            specified. The source format is parsed without
            any modification.
        GEOJSON (1):
            Use GeoJSON variant of JSON. See
            https://tools.ietf.org/html/rfc7946.
    """
    JSON_EXTENSION_UNSPECIFIED = 0
    GEOJSON = 1


__all__ = tuple(sorted(__protobuf__.manifest))
