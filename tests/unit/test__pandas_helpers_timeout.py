import concurrent.futures
import time
from unittest import mock
import pytest

# Try to import necessary modules, but don't fail if they are missing
# as the tests will skip themselves if dependencies are missing.
try:
    import pandas
    import pyarrow
except ImportError:
    pandas = None
    pyarrow = None

from google.cloud.bigquery import _pandas_helpers
from google.cloud.bigquery import schema


@pytest.fixture
def module_under_test():
    return _pandas_helpers


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_download_arrow_row_iterator_timeout(module_under_test):
    bq_schema = [schema.SchemaField("name", "STRING")]

    # Mock page with to_arrow method
    mock_page = mock.Mock()
    mock_page.to_arrow.return_value = pyarrow.RecordBatch.from_pydict({"name": ["foo"]})

    def slow_pages():
        # First page yields quickly
        yield mock_page
        # Sleep to exceed timeout
        time.sleep(0.1)
        yield mock_page

    # Timeout of 0.05s
    timeout = 0.05
    iterator = module_under_test.download_arrow_row_iterator(
        slow_pages(), bq_schema, timeout=timeout
    )

    # First item should succeed
    next(iterator)

    # Second item should fail with TimeoutError
    with pytest.raises(concurrent.futures.TimeoutError):
        next(iterator)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_download_dataframe_row_iterator_timeout(module_under_test):
    bq_schema = [schema.SchemaField("name", "STRING")]
    dtypes = {}

    # Mock page
    mock_page = mock.Mock()
    # Mock iterator for _row_iterator_page_to_dataframe checking next(iter(page))
    mock_page.__iter__ = lambda self: iter(["row1"])
    mock_page._columns = [["foo"]]

    def slow_pages():
        yield mock_page
        time.sleep(0.1)
        yield mock_page

    timeout = 0.05
    iterator = module_under_test.download_dataframe_row_iterator(
        slow_pages(), bq_schema, dtypes, timeout=timeout
    )

    next(iterator)

    with pytest.raises(concurrent.futures.TimeoutError):
        next(iterator)
