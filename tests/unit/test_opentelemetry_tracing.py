import sys
import pytest

from importlib import reload
import mock

from google.cloud.bigquery import opentelemetry_tracing, client

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

TEST_SPAN_NAME = "bar"
TEST_SPAN_ATTRIBUTES = {"foo": "baz"}


@pytest.fixture
def setup():
    tracer_provider = TracerProvider()
    memory_exporter = InMemorySpanExporter()
    span_processor = SimpleExportSpanProcessor(memory_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)
    yield memory_exporter


def test_opentelemetry_not_installed(setup):
    temp_module = sys.modules["opentelemetry"]
    sys.modules["opentelemetry"] = None
    reload(opentelemetry_tracing)
    with opentelemetry_tracing.create_span("No-op for opentelemetry") as span:
        assert span is None
    sys.modules["opentelemetry"] = temp_module
    reload(opentelemetry_tracing)


def test_opentelemetry_success(setup):
    expected_attributes = {"foo": "baz", "db.system": "BigQuery"}
    with opentelemetry_tracing.create_span(
        TEST_SPAN_NAME, attributes=TEST_SPAN_ATTRIBUTES,
    ) as span:
        if span is None:
            span_list = setup.get_finished_spans()
            assert len(span_list) == 1
        assert span.name == TEST_SPAN_NAME
        assert span.attributes == expected_attributes


def test_default_client_attributes(setup):
    import google.auth.credentials

    mock_credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    test_client = client.Client(
        project="test_project", credentials=mock_credentials, location="test_location"
    )

    expected_attributes = {
        "foo": "baz",
        "db.system": "BigQuery",
        "db.name": "test_project",
        "location": "test_location",
    }
    with opentelemetry_tracing.create_span(
        TEST_SPAN_NAME, attributes=TEST_SPAN_ATTRIBUTES, client=test_client
    ) as span:
        if span is None:
            span_list = setup.get_finished_spans()
            assert len(span_list) == 1
        assert span.name == TEST_SPAN_NAME
        assert span.attributes == expected_attributes


def test_default_job_attributes(setup):
    from google.cloud.bigquery import job
    import google.auth.credentials

    mock_credentials = mock.Mock(spec=google.auth.credentials.Credentials)

    test_job_reference = job._JobReference(
        job_id="test_job_id", project="test_project_id", location="test_location"
    )
    test_client = client.Client(
        project="test_project", credentials=mock_credentials, location="test_location"
    )
    test_job = job._AsyncJob(job_id=test_job_reference, client=test_client)

    expected_attributes = {
        "db.system": "BigQuery",
        "db.name": "test_project_id",
        "location": "test_location",
        "num_child_jobs": "0",
        "job_id": "test_job_id",
        "foo": "baz",
    }

    with opentelemetry_tracing.create_span(
        TEST_SPAN_NAME, attributes=TEST_SPAN_ATTRIBUTES, job_ref=test_job
    ) as span:
        if span is None:
            span_list = setup.get_finished_spans()
            assert len(span_list) == 1
        assert span.name == TEST_SPAN_NAME
        assert span.attributes == expected_attributes
