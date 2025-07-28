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
        "ExternalCatalogDatasetOptions",
    },
)


class ExternalCatalogDatasetOptions(proto.Message):
    r"""Options defining open source compatible datasets living in
    the BigQuery catalog. Contains metadata of open source database,
    schema, or namespace represented by the current dataset.

    Attributes:
        parameters (MutableMapping[str, str]):
            Optional. A map of key value pairs defining
            the parameters and properties of the open source
            schema. Maximum size of 2MiB.
        default_storage_location_uri (str):
            Optional. The storage location URI for all
            tables in the dataset. Equivalent to hive
            metastore's database locationUri. Maximum length
            of 1024 characters.
    """

    parameters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )
    default_storage_location_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
