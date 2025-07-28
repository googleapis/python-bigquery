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
        "RowAccessPolicyReference",
    },
)


class RowAccessPolicyReference(proto.Message):
    r"""Id path of a row access policy.

    Attributes:
        project_id (str):
            Required. The ID of the project containing
            this row access policy.
        dataset_id (str):
            Required. The ID of the dataset containing
            this row access policy.
        table_id (str):
            Required. The ID of the table containing this
            row access policy.
        policy_id (str):
            Required. The ID of the row access policy. The ID must
            contain only letters (a-z, A-Z), numbers (0-9), or
            underscores (_). The maximum length is 256 characters.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    policy_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
