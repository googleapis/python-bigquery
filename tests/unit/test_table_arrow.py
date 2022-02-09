# Copyright 2021 Google LLC
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

import pytest


TEST_PATH = "/v1/project/test-proj/dataset/test-dset/table/test-tbl/data"


@pytest.fixture
def class_under_test():
    from google.cloud.bigquery.table import RowIterator

    return RowIterator


def test_to_arrow_rest_extreme_bignumeric(monkeypatch, class_under_test):
    assert False


def test_to_arrow_rest_extreme_bignumeric_multipage(monkeypatch, class_under_test):
    assert False
