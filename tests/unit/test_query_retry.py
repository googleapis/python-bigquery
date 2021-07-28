import mock

from .helpers import make_connection


@mock.patch('time.sleep')
def test_retry_failed_jobs(sleep, client):
    """
    Test retry of job failures, as opposed to API-invocation failures.
    """
    err = dict(reason='rateLimitExceeded')
    responses = [
        dict(status=dict(state='DONE', errors=[err], errorResult=err)),
        dict(status=dict(state='DONE', errors=[err], errorResult=err)),
        dict(status=dict(state='DONE', errors=[err], errorResult=err)),
        dict(status=dict(state='DONE')),
        dict(rows=[{'f': [{'v': '1'}]}], totalRows='1'),
        ]

    def api_request(method, path, query_params=None, data=None, **kw):
        response = responses.pop(0)
        if data:
            response['jobReference'] = data['jobReference']
        else:
            response['jobReference'] = dict(jobId=path.split('/')[-1],
                                            projectId='PROJECT')
        print(response)
        return response

    conn = client._connection = make_connection()
    conn.api_request.side_effect = api_request

    job = client.query("select 1")
    orig_job_id = job.job_id
    result = job.result()
    assert result.total_rows == 1
    assert not responses  # We made all the calls we expected to.

    # The job adjusts it's job id based on the id of the last attempt.
    assert job.job_id != orig_job_id
    assert job.job_id == conn.mock_calls[3][2]['data']['jobReference']['jobId']

    # each of the first four calls was for a different job.
    assert len(set(call[2]['data']['jobReference']['jobId']
                   for call in conn.mock_calls[:4])) == 4

    # We had to sleep three times
    assert len(sleep.mock_calls) == 3

    # Sleeps are random, however they're more than 0
    assert min(c[1][0] for c in sleep.mock_calls) > 0

    # They're at most 2 * (multiplier**(number of sleeps - 1)) * initial
    # The default multiplier is 2
    assert max(c[1][0] for c in sleep.mock_calls) <= 8
