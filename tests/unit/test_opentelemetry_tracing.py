# Copyright 2020 Google LLC
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


import sys
import pytest

import mock

from google.cloud.bigquery import opentelemetry_tracing

try:
    import opentelemetry
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
except ImportError:
    opentelemetry = None

from six.moves import reload_module

TEST_SPAN_NAME = "bar"
TEST_SPAN_ATTRIBUTES = {"foo": "baz"}


@pytest.mark.skipif(opentelemetry is None, reason="Require `opentelemetry`")
@pytest.fixture
def setup():
    tracer_provider = TracerProvider()
    memory_exporter = InMemorySpanExporter()
    span_processor = SimpleExportSpanProcessor(memory_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)
    yield memory_exporter


@pytest.mark.skipif(opentelemetry is None, reason="Require `opentelemetry`")
def test_opentelemetry_not_installed(setup):
    temp_module = sys.modules["opentelemetry"]
    sys.modules["opentelemetry"] = None
    reload_module(opentelemetry_tracing)
    with opentelemetry_tracing.create_span("No-op for opentelemetry") as span:
        assert span is None
    sys.modules["opentelemetry"] = temp_module
    reload_module(opentelemetry_tracing)


@pytest.mark.skipif(opentelemetry is None, reason="Require `opentelemetry`")
def test_opentelemetry_success(setup):
    expected_attributes = {"foo": "baz", "db.system": "BigQuery"}

    with opentelemetry_tracing.create_span(
        TEST_SPAN_NAME, attributes=TEST_SPAN_ATTRIBUTES, client=None, job_ref=None
    ) as span:
        assert span is not None
        assert span.name == TEST_SPAN_NAME
        assert span.attributes == expected_attributes


@pytest.mark.skipif(opentelemetry is None, reason="Require `opentelemetry`")
def test_default_client_attributes(setup):
    expected_attributes = {
        "foo": "baz",
        "db.system": "BigQuery",
        "db.name": "test_project",
        "location": "test_location",
    }
    with mock.patch("google.cloud.bigquery.client.Client") as test_client:
        test_client.project = "test_project"
        test_client.location = "test_location"
        with opentelemetry_tracing.create_span(
            TEST_SPAN_NAME, attributes=TEST_SPAN_ATTRIBUTES, client=test_client
        ) as span:
            assert span is not None
            assert span.name == TEST_SPAN_NAME
            assert span.attributes == expected_attributes


@pytest.mark.skipif(opentelemetry is None, reason="Require `opentelemetry`")
def test_default_job_attributes(setup):
    expected_attributes = {
        "db.system": "BigQuery",
        "db.name": "test_project_id",
        "location": "test_location",
        "num_child_jobs": "0",
        "job_id": "test_job_id",
        "foo": "baz",
    }
    with mock.patch("google.cloud.bigquery.job._AsyncJob") as test_job_ref:
        test_job_ref.job_id = "test_job_id"
        test_job_ref.location = "test_location"
        test_job_ref.project = "test_project_id"
        test_job_ref.num_child_jobs = "0"

        with opentelemetry_tracing.create_span(
            TEST_SPAN_NAME, attributes=TEST_SPAN_ATTRIBUTES, job_ref=test_job_ref
        ) as span:
            assert span is not None
            assert span.name == TEST_SPAN_NAME
            assert span.attributes == expected_attributes
