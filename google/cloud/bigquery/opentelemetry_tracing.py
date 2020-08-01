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
import pdb

Logger = logging.getLogger(__name__)

try:
    from opentelemetry import trace
    from opentelemetry import propagators
    from opentelemetry.trace import SpanContext
    from opentelemetry.trace import get_current_span
    from opentelemetry.trace import set_span_in_context
    from opentelemetry.trace.status import Status
    from opentelemetry.instrumentation.utils import http_status_to_canonical_code

    HAS_OPENTELEMETRY = True

except ImportError:
    Logger.info(
        'This service instrumented using opentelemetry.'
        'Opentelemetry could not be imported please'
        'add opentelemetry-api and opentelemetry-instrumentation'
        'packages in order to get Big Query Tracing data'
    )

    HAS_OPENTELEMETRY = False


class SpanCreator:
    def __init__(self):
        self.opentelemetry_enbled = HAS_OPENTELEMETRY

    @contextmanager
    def create(self, name, attributes=None, parent_context=None):

        print('yerr')

        if not self.opentelemetry_enbled:
            yield None
            return

        tracer = trace.get_tracer(__name__)

        default_attributes = {
            'db.type': 'BigQuery',
        }

        if attributes:
            default_attributes.update(attributes)

        # yield new span value
        with tracer.start_as_current_span(name=name, attributes=attributes, parent=parent_context) as span:
            try:
                yield span
            except GoogleAPICallError as error:
                if error.code is not None:
                    span.set_status(Status(http_status_to_canonical_code(error.code)))
                raise
