# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import proto  # type: ignore

from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import model_reference as gcb_model_reference
from google.cloud.bigquery_v2.types import standard_sql
from google.cloud.bigquery_v2.types import table_reference
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore

__manifest__ = ("ListModelsResponse",)


class ListModelsResponse(proto.Message):
    r"""

    Attributes:
        models (Sequence[google.cloud.bigquery_v2.types.Model]):
            Models in the requested dataset. Only the following fields
            are populated: model_reference, model_type, creation_time,
            last_modified_time and labels.
        next_page_token (str):
            A token to request the next page of results.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    @property
    def raw_page(self):
        return self

    models = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Model",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__manifest__))
