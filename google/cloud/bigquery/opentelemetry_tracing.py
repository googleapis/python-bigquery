# Copyright 2020 Google LLC All rights reserved.
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

import logging
from contextlib import contextmanager
from google.api_core.exceptions import GoogleAPICallError

Logger = logging.getLogger(__name__)
try:
    from opentelemetry import trace
    from opentelemetry.trace.status import Status
    from opentelemetry.instrumentation.utils import http_status_to_canonical_code

    HAS_OPENTELEMETRY = True

except ImportError:
    Logger.info(
        "This service is instrumented using opentelemetry."
        "Opentelemetry could not be imported, please"
        "add opentelemetry-api and opentelemetry-instrumentation"
        "packages, in order to get Big Query Tracing data"
    )

    HAS_OPENTELEMETRY = False


@contextmanager
def create_span(name, attributes=None, client=None, job_ref=None):
    if not HAS_OPENTELEMETRY:
        yield None
        return

    default_attributes = {
        "db.system": "BigQuery",
    }

    tracer = trace.get_tracer(__name__)

    if client:
        client_attributes = _set_client_attributes(client)
        default_attributes.update(client_attributes)
    elif job_ref:
        job_attributes = _set_job_attributes(job_ref)
        default_attributes.update(job_attributes)

    if attributes:
        default_attributes.update(attributes)

    # yield new span value
    with tracer.start_as_current_span(name=name, attributes=default_attributes) as span:
        try:
            yield span
        except GoogleAPICallError as error:
            if error.code is not None:
                span.set_status(Status(http_status_to_canonical_code(error.code)))
            raise


def _set_client_attributes(client):
    return {"db.name": client.project, "location": client.location}


def _set_job_attributes(job_ref):
    return {
        "db.name": job_ref.project,
        "location": job_ref.location,
        "num_child_jobs": str(job_ref.num_child_jobs),
        "job_id": job_ref.job_id,
        "parent_job_id": job_ref.parent_job_id,
        "timeCreated": job_ref.created,
        "timeStarted": job_ref.started,
        "timeEnded": job_ref.ended,
        "errors": job_ref.errors,
        "errorResult": job_ref.error_result,
        "state": job_ref.state,
    }
