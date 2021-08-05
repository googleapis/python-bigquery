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

import contextlib
import threading
import time

import google.cloud.bigquery


def thread(func):
    thread = threading.Thread(target=func, daemon=True)
    thread.start()
    return thread


def test_query_retry_539(bigquery_client, dataset_id):
    """
    Test semantic retry

    See: https://github.com/googleapis/python-bigquery/issues/539
    """
    from google.api_core import exceptions
    from google.api_core.retry import if_exception_type, Retry

    table_name = f"{dataset_id}.t539"
    job = bigquery_client.query(f"select count(*) from {table_name}")
    job_id = job.job_id

    # We can already know that the job failed, but we're not supposed
    # to find out until we call result, which is where retry happend
    assert job.done()
    assert job.exception() is not None

    @thread
    def create_table():
        time.sleep(1)  # Give the first attempt time to fail.
        with contextlib.closing(google.cloud.bigquery.Client()) as client:
            client.query(f"create table {table_name} (id int64)")

    retry_policy = Retry(predicate=if_exception_type(exceptions.NotFound))
    [[count]] = list(job.result(retry=retry_policy))
    assert count == 0

    # The job was retried, and thus got a new job id
    assert job.job_id != job_id

    # Make sure we don't leave a thread behind:
    create_table.join()
