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
        "JobCreationReason",
    },
)


class JobCreationReason(proto.Message):
    r"""Reason about why a Job was created from a
    ```jobs.query`` <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query>`__
    method when used with ``JOB_CREATION_OPTIONAL`` Job creation mode.

    For
    ```jobs.insert`` <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert>`__
    method calls it will always be ``REQUESTED``.

    Attributes:
        code (google.cloud.bigquery_v2.types.JobCreationReason.Code):
            Output only. Specifies the high level reason
            why a Job was created.
    """

    class Code(proto.Enum):
        r"""Indicates the high level reason why a job was created.

        Values:
            CODE_UNSPECIFIED (0):
                Reason is not specified.
            REQUESTED (1):
                Job creation was requested.
            LONG_RUNNING (2):
                The query request ran beyond a system defined timeout
                specified by the `timeoutMs field in the
                QueryRequest <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#queryrequest>`__.
                As a result it was considered a long running operation for
                which a job was created.
            LARGE_RESULTS (3):
                The results from the query cannot fit in the
                response.
            OTHER (4):
                BigQuery has determined that the query needs
                to be executed as a Job.
        """
        CODE_UNSPECIFIED = 0
        REQUESTED = 1
        LONG_RUNNING = 2
        LARGE_RESULTS = 3
        OTHER = 4

    code: Code = proto.Field(
        proto.ENUM,
        number=1,
        enum=Code,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
