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

from google.cloud.bigquery_v2.types import error


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "JobStatus",
    },
)


class JobStatus(proto.Message):
    r"""

    Attributes:
        error_result (google.cloud.bigquery_v2.types.ErrorProto):
            Output only. Final error result of the job.
            If present, indicates that the job has completed
            and was unsuccessful.
        errors (MutableSequence[google.cloud.bigquery_v2.types.ErrorProto]):
            Output only. The first errors encountered
            during the running of the job. The final message
            includes the number of errors that caused the
            process to stop. Errors here do not necessarily
            mean that the job has not completed or was
            unsuccessful.
        state (str):
            Output only. Running state of the job.  Valid
            states include 'PENDING', 'RUNNING', and 'DONE'.
    """

    error_result: error.ErrorProto = proto.Field(
        proto.MESSAGE,
        number=1,
        message=error.ErrorProto,
    )
    errors: MutableSequence[error.ErrorProto] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=error.ErrorProto,
    )
    state: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
