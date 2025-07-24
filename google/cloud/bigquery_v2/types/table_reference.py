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
        "TableReference",
    },
)


class TableReference(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. The ID of the project containing
            this table.
        dataset_id (str):
            Required. The ID of the dataset containing
            this table.
        table_id (str):
            Required. The ID of the table. The ID can contain Unicode
            characters in category L (letter), M (mark), N (number), Pc
            (connector, including underscore), Pd (dash), and Zs
            (space). For more information, see `General
            Category <https://wikipedia.org/wiki/Unicode_character_property#General_Category>`__.
            The maximum length is 1,024 characters. Certain operations
            allow suffixing of the table ID with a partition decorator,
            such as ``sample_table$20190123``.
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


__all__ = tuple(sorted(__protobuf__.manifest))
