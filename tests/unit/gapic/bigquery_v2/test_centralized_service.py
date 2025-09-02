# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
#

import pytest
from typing import (
    Optional,
    Sequence,
    Tuple,
    Union,
)
from unittest import mock

from google.api_core import client_options as client_options_lib
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as auth_credentials

# --- IMPORT SERVICECLIENT MODULES ---
from google.cloud.bigquery_v2.services import (
    centralized_service,
    dataset_service,
    job_service,
    model_service,
)

# --- IMPORT TYPES MODULES (to access *Requests classes) ---
from google.cloud.bigquery_v2.types import (
    dataset,
    job,
    model,
)

# --- TYPE ALIASES ---
try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

AnyRequest = Union[
    dataset.GetDatasetRequest,
    model.GetModelRequest,
    model.DeleteModelRequest,
    model.PatchModelRequest,
    job.ListJobsRequest,
    model.ListModelsRequest,
]

# --- CONSTANTS ---
PROJECT_ID = "test-project"
DATASET_ID = "test_dataset"
JOB_ID = "test_job"
MODEL_ID = "test_model"
DEFAULT_ETAG = "test_etag"

DEFAULT_RETRY: OptionalRetry = gapic_v1.method.DEFAULT
DEFAULT_TIMEOUT: Union[float, object] = gapic_v1.method.DEFAULT
DEFAULT_METADATA: Sequence[Tuple[str, Union[str, bytes]]] = ()

# --- HELPERS ---
def assert_client_called_once_with(
    mock_method: mock.Mock,
    request: AnyRequest,
    retry: OptionalRetry = DEFAULT_RETRY,
    timeout: Union[float, object] = DEFAULT_TIMEOUT,
    metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
):
    """Helper to assert a client method was called with default args."""
    mock_method.assert_called_once_with(
        request=request,
        retry=retry,
        timeout=timeout,
        metadata=metadata,
    )


# --- FIXTURES ---


@pytest.fixture
def mock_dataset_service_client_class():
    with mock.patch(
        "google.cloud.bigquery_v2.services.dataset_service.DatasetServiceClient",
        autospec=True,
    ) as mock_class:
        yield mock_class


@pytest.fixture
def mock_job_service_client_class():
    with mock.patch(
        "google.cloud.bigquery_v2.services.job_service.JobServiceClient",
        autospec=True,
    ) as mock_class:
        yield mock_class


@pytest.fixture
def mock_model_service_client_class():
    with mock.patch(
        "google.cloud.bigquery_v2.services.model_service.ModelServiceClient",
        autospec=True,
    ) as mock_class:
        yield mock_class


# --- TEST CLASSES ---


class TestCentralizedClientInitialization:
    @pytest.mark.parametrize(
        "credentials, client_options",
        [
            (None, None),
            (mock.MagicMock(spec=auth_credentials.Credentials), None),
            (
                None,
                client_options_lib.ClientOptions(api_endpoint="test.googleapis.com"),
            ),
            (
                mock.MagicMock(spec=auth_credentials.Credentials),
                client_options_lib.ClientOptions(api_endpoint="test.googleapis.com"),
            ),
        ],
    )
    def test_client_initialization_arguments(
        self,
        credentials,
        client_options,
        mock_dataset_service_client_class,
        mock_job_service_client_class,
        mock_model_service_client_class,
    ):
        # Act
        client = centralized_service.BigQueryClient(
            credentials=credentials, client_options=client_options
        )

        # Assert
        _ = client.dataset_service_client
        mock_dataset_service_client_class.assert_called_once_with(
            credentials=credentials, client_options=client_options
        )

        _ = client.job_service_client
        mock_job_service_client_class.assert_called_once_with(
            credentials=credentials, client_options=client_options
        )

        _ = client.model_service_client
        mock_model_service_client_class.assert_called_once_with(
            credentials=credentials, client_options=client_options
        )


class TestCentralizedClientDatasetService:
    def test_get_dataset(self, mock_dataset_service_client_class):
        # Arrange
        mock_instance = mock_dataset_service_client_class.return_value
        expected_dataset = dataset.Dataset(
            kind="bigquery#dataset", id=f"{PROJECT_ID}:{DATASET_ID}"
        )
        mock_instance.get_dataset.return_value = expected_dataset
        get_dataset_request = dataset.GetDatasetRequest(
            project_id=PROJECT_ID, dataset_id=DATASET_ID
        )
        client = centralized_service.BigQueryClient()

        # Act
        dataset_response = client.get_dataset(request=get_dataset_request)

        # Assert
        assert dataset_response == expected_dataset
        assert_client_called_once_with(mock_instance.get_dataset, get_dataset_request)

    @pytest.mark.parametrize(
        "call_args, expected_request",
        [
            (
                {"project_id": PROJECT_ID},
                dataset.ListDatasetsRequest(project_id=PROJECT_ID),
            ),
            (
                {"request": dataset.ListDatasetsRequest(project_id=PROJECT_ID)},
                dataset.ListDatasetsRequest(project_id=PROJECT_ID),
            ),
            ({}, dataset.ListDatasetsRequest(project_id=PROJECT_ID)),
        ],
    )
    def test_list_datasets(
        self, mock_dataset_service_client_class, call_args, expected_request
    ):
        # Arrange
        mock_instance = mock_dataset_service_client_class.return_value
        expected_datasets = [
            dataset.Dataset(kind="bigquery#dataset", id=f"{PROJECT_ID}:{DATASET_ID}")
        ]
        mock_instance.list_datasets.return_value = expected_datasets
        client = centralized_service.BigQueryClient()
        client.project = PROJECT_ID

        # Act
        datasets_response = client.list_datasets(**call_args)

        # Assert
        assert datasets_response == expected_datasets
        assert_client_called_once_with(mock_instance.list_datasets, expected_request)

    def test_list_datasets_conflicting_args(self, mock_dataset_service_client_class):
        # Arrange
        client = centralized_service.BigQueryClient()
        list_datasets_request = dataset.ListDatasetsRequest(project_id=PROJECT_ID)

        # Act & Assert
        with pytest.raises(ValueError):
            client.list_datasets(project_id=PROJECT_ID, request=list_datasets_request)


class TestCentralizedClientJobService:
    def test_list_jobs(self, mock_job_service_client_class):
        # Arrange
        mock_instance = mock_job_service_client_class.return_value
        expected_jobs = [job.Job(kind="bigquery#job", id=f"{PROJECT_ID}:{JOB_ID}")]
        mock_instance.list_jobs.return_value = expected_jobs
        list_jobs_request = job.ListJobsRequest(project_id=PROJECT_ID)
        client = centralized_service.BigQueryClient()

        # Act
        jobs_response = client.list_jobs(request=list_jobs_request)

        # Assert
        assert jobs_response == expected_jobs
        assert_client_called_once_with(mock_instance.list_jobs, list_jobs_request)


class TestCentralizedClientModelService:
    def test_get_model(self, mock_model_service_client_class):
        # Arrange
        mock_instance = mock_model_service_client_class.return_value
        expected_model = model.Model(
            etag=DEFAULT_ETAG,
            model_reference={
                "project_id": PROJECT_ID,
                "dataset_id": DATASET_ID,
                "model_id": MODEL_ID,
            },
        )
        mock_instance.get_model.return_value = expected_model
        get_model_request = model.GetModelRequest(
            project_id=PROJECT_ID, dataset_id=DATASET_ID, model_id=MODEL_ID
        )
        client = centralized_service.BigQueryClient()

        # Act
        model_response = client.get_model(request=get_model_request)

        # Assert
        assert model_response == expected_model
        assert_client_called_once_with(mock_instance.get_model, get_model_request)

    def test_delete_model(self, mock_model_service_client_class):
        # Arrange
        mock_instance = mock_model_service_client_class.return_value
        mock_instance.delete_model.return_value = None
        delete_model_request = model.DeleteModelRequest(
            project_id=PROJECT_ID, dataset_id=DATASET_ID, model_id=MODEL_ID
        )
        client = centralized_service.BigQueryClient()

        # Act
        result = client.delete_model(request=delete_model_request)

        # Assert
        assert result is None
        assert_client_called_once_with(mock_instance.delete_model, delete_model_request)

    def test_patch_model(self, mock_model_service_client_class):
        # Arrange
        mock_instance = mock_model_service_client_class.return_value
        expected_model = model.Model(
            etag="new_etag",
            model_reference={
                "project_id": PROJECT_ID,
                "dataset_id": DATASET_ID,
                "model_id": MODEL_ID,
            },
            description="A newly patched description.",
        )
        mock_instance.patch_model.return_value = expected_model

        model_patch = model.Model(description="A newly patched description.")
        patch_model_request = model.PatchModelRequest(
            project_id=PROJECT_ID,
            dataset_id=DATASET_ID,
            model_id=MODEL_ID,
            model=model_patch,
        )
        client = centralized_service.BigQueryClient()

        # Act
        patched_model = client.patch_model(request=patch_model_request)

        # Assert
        assert patched_model == expected_model
        assert_client_called_once_with(mock_instance.patch_model, patch_model_request)

    def test_list_models(self, mock_model_service_client_class):
        # Arrange
        mock_instance = mock_model_service_client_class.return_value
        expected_models = [
            model.Model(
                etag=DEFAULT_ETAG,
                model_reference={
                    "project_id": PROJECT_ID,
                    "dataset_id": DATASET_ID,
                    "model_id": MODEL_ID,
                },
            )
        ]
        mock_instance.list_models.return_value = expected_models
        list_models_request = model.ListModelsRequest(
            project_id=PROJECT_ID, dataset_id=DATASET_ID
        )
        client = centralized_service.BigQueryClient()

        # Act
        models_response = client.list_models(request=list_models_request)

        # Assert
        assert models_response == expected_models
        assert_client_called_once_with(mock_instance.list_models, list_models_request)
