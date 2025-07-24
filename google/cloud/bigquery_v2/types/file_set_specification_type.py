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
        "FileSetSpecType",
    },
)


class FileSetSpecType(proto.Enum):
    r"""This enum defines how to interpret source URIs for load jobs
    and external tables.

    Values:
        FILE_SET_SPEC_TYPE_FILE_SYSTEM_MATCH (0):
            This option expands source URIs by listing
            files from the object store. It is the default
            behavior if FileSetSpecType is not set.
        FILE_SET_SPEC_TYPE_NEW_LINE_DELIMITED_MANIFEST (1):
            This option indicates that the provided URIs
            are newline-delimited manifest files, with one
            URI per line. Wildcard URIs are not supported.
    """
    FILE_SET_SPEC_TYPE_FILE_SYSTEM_MATCH = 0
    FILE_SET_SPEC_TYPE_NEW_LINE_DELIMITED_MANIFEST = 1


__all__ = tuple(sorted(__protobuf__.manifest))
