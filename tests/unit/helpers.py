# Copyright 2018 Google LLC
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

import google.cloud.bigquery.client
import google.cloud.bigquery.dataset
import mock
import pytest


def add_header_assertion_to_kwargs(kwargs):
    timeout = kwargs.get("timeout")
    if timeout is not None:
        headers = kwargs.setdefault("headers", {})
        if headers is None:
            kwargs["headers"] = headers = {}
        headers[google.cloud.bigquery.client.TIMEOUT_HEADER] = str(kwargs["timeout"])

    return kwargs


def add_header_assertion(mock, name):
    """
    Modify assert_called_with-ish assertions to add timeout headers

    if there's a timeout
    """
    orig = getattr(mock, name)

    def repl(*args, **kw):
        return orig(*args, **add_header_assertion_to_kwargs(kw))

    setattr(mock, name, repl)


def api_call(*args, **kw):
    """
    Replacement for mock.call that adds a timeout header, if necessary
    """
    return mock.call(*args, **add_header_assertion_to_kwargs(kw))


def make_connection(*responses):
    import google.cloud.bigquery._http
    import mock
    from google.cloud.exceptions import NotFound

    mock_conn = mock.create_autospec(google.cloud.bigquery._http.Connection)
    mock_conn.user_agent = "testing 1.2.3"
    mock_conn.api_request.side_effect = list(responses) + [NotFound("miss")]
    for name in "assert_called_with", "assert_called_once_with":
        add_header_assertion(mock_conn.api_request, name)

    mock_conn.API_BASE_URL = "https://bigquery.googleapis.com"
    mock_conn.get_api_base_url_for_mtls = mock.Mock(return_value=mock_conn.API_BASE_URL)
    return mock_conn


def _to_pyarrow(value):
    """Convert Python value to pyarrow value."""
    import pyarrow

    return pyarrow.array([value])[0]


def make_client(project="PROJECT", **kw):
    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    return google.cloud.bigquery.client.Client(project, credentials, **kw)


def make_dataset_reference_string(project, ds_id):
    return f"{project}.{ds_id}"


def make_dataset(project, ds_id):
    return google.cloud.bigquery.dataset.Dataset(
        google.cloud.bigquery.dataset.DatasetReference(project, ds_id)
    )


def make_dataset_list_item(project, ds_id):
    return google.cloud.bigquery.dataset.DatasetListItem(
        dict(datasetReference=dict(projectId=project, datasetId=ds_id))
    )


def identity(x):
    return x


def get_reference(x):
    return x.reference


dataset_like = [
    (google.cloud.bigquery.dataset.DatasetReference, identity),
    (make_dataset, identity),
    (make_dataset_list_item, get_reference),
    (
        make_dataset_reference_string,
        google.cloud.bigquery.dataset.DatasetReference.from_string,
    ),
]

dataset_polymorphic = pytest.mark.parametrize(
    "make_dataset,get_reference", dataset_like
)
