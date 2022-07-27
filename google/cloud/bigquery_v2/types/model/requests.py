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

__manifest__ = (
    "GetModelRequest",
    "PatchModelRequest",
    "DeleteModelRequest",
    "ListModelsRequest",
)


class GetModelRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the requested model.
        dataset_id (str):
            Required. Dataset ID of the requested model.
        model_id (str):
            Required. Model ID of the requested model.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    project_id = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id = proto.Field(
        proto.STRING,
        number=2,
    )
    model_id = proto.Field(
        proto.STRING,
        number=3,
    )


class PatchModelRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the model to patch.
        dataset_id (str):
            Required. Dataset ID of the model to patch.
        model_id (str):
            Required. Model ID of the model to patch.
        model (google.cloud.bigquery_v2.types.Model):
            Required. Patched model.
            Follows RFC5789 patch semantics. Missing fields
            are not updated. To clear a field, explicitly
            set to default value.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    project_id = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id = proto.Field(
        proto.STRING,
        number=2,
    )
    model_id = proto.Field(
        proto.STRING,
        number=3,
    )
    model = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Model",
    )


class DeleteModelRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the model to delete.
        dataset_id (str):
            Required. Dataset ID of the model to delete.
        model_id (str):
            Required. Model ID of the model to delete.
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    project_id = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id = proto.Field(
        proto.STRING,
        number=2,
    )
    model_id = proto.Field(
        proto.STRING,
        number=3,
    )


class ListModelsRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the models to list.
        dataset_id (str):
            Required. Dataset ID of the models to list.
        max_results (google.protobuf.wrappers_pb2.UInt32Value):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call to
            request the next page of results
    """
    __module__ = __module__.rsplit(".", maxsplit=1)[0]  # type: ignore

    project_id = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id = proto.Field(
        proto.STRING,
        number=2,
    )
    max_results = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.UInt32Value,
    )
    page_token = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__manifest__))
