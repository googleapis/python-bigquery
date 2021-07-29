# Copyright (c) 2021 The PyBigQuery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
        time.sleep(1)
        with contextlib.closing(google.cloud.bigquery.Client()) as client:
            client.query(f"create table {table_name} (id int64)")

    retry_policy = Retry(predicate=if_exception_type(exceptions.NotFound))
    [[count]] = list(job.result(retry=retry_policy))
    assert count == 0

    # The job was retried, and thus got a new job id
    assert job.job_id != job_id

    # Make sure we don't leave a thread behind:
    create_table.join()
