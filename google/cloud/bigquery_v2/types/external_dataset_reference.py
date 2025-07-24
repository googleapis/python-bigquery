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
        "ExternalDatasetReference",
    },
)


class ExternalDatasetReference(proto.Message):
    r"""Configures the access a dataset defined in an external
    metadata storage.

    Attributes:
        external_source (str):
            Required. External source that backs this
            dataset.
        connection (str):
            Required. The connection id that is used to access the
            external_source.

            Format:
            projects/{project_id}/locations/{location_id}/connections/{connection_id}
    """

    external_source: str = proto.Field(
        proto.STRING,
        number=2,
    )
    connection: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
