import sys
import pytest

from importlib import reload
import unittest
import mock

from google.cloud.bigquery import opentelemetry_tracing, client

from opentelemetry import trace
from opentelemetry.sdk.trace import export
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
import pdb

TEST_SPAN_NAME = "bar"
TEST_SPAN_ATTRIBUTES = {"foo": "bar"}


# class TestOpentelemetry(unittest.TestCase):
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
    span_creator = opentelemetry_tracing.SpanCreator()
    with span_creator.create('No-op for opentelemetry') as span:
        assert span == None
    sys.modules["opentelemetry"] = temp_module
    reload(opentelemetry_tracing)


def test_opentelemetry_success(setup):
    span_creator = opentelemetry_tracing.SpanCreator()
    expected_attributes = {"foo": "bar",
                           'db.system': 'bigquery'
                           }
    with span_creator.create(
            TEST_SPAN_NAME,
            attributes=TEST_SPAN_ATTRIBUTES,
    ) as span:
        if span is None:
            span_list = setup.get_finished_spans()
            print(span_list)
            assert len(span_list) == 1
        assert span.name == TEST_SPAN_NAME
        assert span.attributes == expected_attributes


def test_default_client_attributes(setup):
    import google.auth.credentials

    mock_credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    test_client = client.Client(project='test_project', credentials=mock_credentials,
                                location='test_location')

    span_creator = opentelemetry_tracing.SpanCreator()
    expected_attributes = {"foo": "bar",
                           'db.system': 'bigquery',
                           'db.name': 'test_project',
                           'location': 'test_location'
                           }
    with span_creator.create(
            TEST_SPAN_NAME,
            attributes=TEST_SPAN_ATTRIBUTES,
            client=test_client
    ) as span:
        if span is None:
            span_list = setup.get_finished_spans()
            print(span_list)
            assert len(span_list) == 1
        assert span.name == TEST_SPAN_NAME
        assert span.attributes == expected_attributes

def test_default_job_attributes(setup):
    from google.cloud.bigquery import job
    import google.auth.credentials

    mock_credentials = mock.Mock(spec=google.auth.credentials.Credentials)

    test_job_reference = job._JobReference(job_id='test_job_id',
                                           project='test_project_id',
                                           location='test_location')
    test_client = client.Client(project='test_project', credentials=mock_credentials,
                                location='test_location')
    test_job = job._AsyncJob(job_id=test_job_reference, client=test_client)

    span_creator = opentelemetry_tracing.SpanCreator()
    # TODO add assertions for attributes being equal
    expected_attributes = {'db.system': 'bigquery',
                           'db.name': 'test_project_id',
                           'location': 'test_location',
                           'num_child_jobs': '0',
                           'job_id': 'test_job_id',
                           'parent_job_id': None,
                           'timeCreated': None,
                           'timeStarted': None,
                           'timeEnded': None,
                           'errors': None,
                           'errorResult': None,
                           'state': None,
                           'foo': 'bar'}

    with span_creator.create(
            TEST_SPAN_NAME,
            attributes=TEST_SPAN_ATTRIBUTES,
            job_ref=test_job
    ) as span:
        if span is None:
            span_list = setup.get_finished_spans()
            print(span_list[0])
            assert len(span_list) == 1
        assert span.name == TEST_SPAN_NAME

