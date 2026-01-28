import pytest
from unittest import mock
from google.cloud.bigquery import _pandas_helpers

try:
    from google.cloud import bigquery_storage
except ImportError:
    bigquery_storage = None


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_download_table_bqstorage_passes_timeout_to_create_read_session():
    # Mock dependencies
    project_id = "test-project"
    table = mock.Mock()
    table.table_id = "test_table"
    table.to_bqstorage.return_value = "projects/test/datasets/test/tables/test"

    bqstorage_client = mock.Mock(spec=bigquery_storage.BigQueryReadClient)
    # Mock create_read_session to return a session with no streams so the function returns early
    # (Checking start of loop logic vs empty streams return)
    session = mock.Mock()
    # If streams is empty, _download_table_bqstorage returns early, which is fine for this test
    session.streams = []
    bqstorage_client.create_read_session.return_value = session

    # Call the function
    timeout = 123.456
    # download_arrow_bqstorage yields frames, so we need to iterate to trigger execution
    list(
        _pandas_helpers.download_arrow_bqstorage(
            project_id, table, bqstorage_client, timeout=timeout
        )
    )

    # Verify timeout and retry were passed
    bqstorage_client.create_read_session.assert_called_once()
    _, kwargs = bqstorage_client.create_read_session.call_args
    assert "timeout" in kwargs
    assert kwargs["timeout"] == timeout

    assert "retry" in kwargs
    retry_policy = kwargs["retry"]
    assert retry_policy is not None
    # Check if deadline is set correctly in the retry policy
    assert retry_policy._deadline == timeout
