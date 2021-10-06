# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from google.cloud.bigquery.job.query import QueryJobConfig


@pytest.fixture
def module_under_test():
    from google.cloud.bigquery import _job_helpers

    return _job_helpers


@pytest.mark.parametrize(
    ("job_config", "expected"),
    (
        (None, {"useLegacySql": False}),
        (QueryJobConfig(), {"useLegacySql": False}),
        (QueryJobConfig(dry_run=True), {"useLegacySql": False, "dryRun": True}),
        (
            QueryJobConfig(labels={"abc": "def"}),
            {"useLegacySql": False, "labels": {"abc": "def"}},
        ),
        (
            QueryJobConfig(use_query_cache=False),
            {"useLegacySql": False, "useQueryCache": False},
        ),
    ),
)
def test__to_query_request(module_under_test, job_config, expected):
    result = module_under_test._to_query_request(job_config)
    assert result == expected
