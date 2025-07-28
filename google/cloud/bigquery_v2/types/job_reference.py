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
        "JobReference",
    },
)


class JobReference(proto.Message):
    r"""A job reference is a fully qualified identifier for referring
    to a job.

    Attributes:
        project_id (str):
            Required. The ID of the project containing
            this job.
        job_id (str):
            Required. The ID of the job. The ID must contain only
            letters (a-z, A-Z), numbers (0-9), underscores (_), or
            dashes (-). The maximum length is 1,024 characters.
        location (google.protobuf.wrappers_pb2.StringValue):
            Optional. The geographic location of the job.
            The default value is US.
            For more information about BigQuery locations,
            see:

            https://cloud.google.com/bigquery/docs/locations
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    location: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
