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

# import datetime

# import mock
# import pytest

# from google.cloud.bigquery.retry import DEFAULT_TIMEOUT

# # from google.cloud.bigquery.dataset import AccessEntry
# from .helpers import make_connection


# def test_list_jobs_w_timeout(client, PROJECT):
#     from google.cloud.bigquery.dataset import AccessEntry
#     entry = AccessEntry('OWNER', 'userByEmail', 'user@example.com')
#     view = {
#         'projectId': 'my-project',
#         'datasetId': 'my_dataset',
#         # 'tableId': 'my_table'
#       }
#     # entry = AccessEntry(None, 'view', view)
#     entry = AccessEntry(None, 'dataset', view)
#     assert (entry == {})
