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

from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "UserDefinedFunctionResource",
    },
)


class UserDefinedFunctionResource(proto.Message):
    r"""This is used for defining User Defined Function (UDF) resources only
    when using legacy SQL. Users of GoogleSQL should leverage either DDL
    (e.g. CREATE [TEMPORARY] FUNCTION ... ) or the Routines API to
    define UDF resources.

    For additional information on migrating, see:
    https://cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql#differences_in_user-defined_javascript_functions

    Attributes:
        resource_uri (google.protobuf.wrappers_pb2.StringValue):
            [Pick one] A code resource to load from a Google Cloud
            Storage URI (gs://bucket/path).
        inline_code (google.protobuf.wrappers_pb2.StringValue):
            [Pick one] An inline resource that contains code for a
            user-defined function (UDF). Providing a inline code
            resource is equivalent to providing a URI for a file
            containing the same code.
    """

    resource_uri: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.StringValue,
    )
    inline_code: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
