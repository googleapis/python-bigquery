import contextlib
import google.cloud.bigquery.opentelemetry_tracing
import mock
import pytest

from .helpers import make_client


@pytest.fixture
def client():
    yield make_client()


@pytest.fixture
def PROJECT():
    yield "PROJECT"


@pytest.fixture
def DS_ID():
    yield "DATASET_ID"


@pytest.fixture(autouse=True, scope="session")
def bypass_opentelemetry_tracing():
    @contextlib.contextmanager
    def create_span(name, attributes=None, client=None, job_ref=None):
        # Make existing test code that checks _get_final_span_attributes work:
        google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes(
            attributes, client, job_ref
        )
        yield

    # Note that we have to mock in client, because it uses a from import. :/
    with mock.patch("google.cloud.bigquery.client.create_span", create_span):
        yield
