import pytest
from typing import (
    Optional,
    Sequence,
    Tuple,
    Union,
)
from unittest import mock

from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.cloud.bigquery_v2 import BigQueryClient
from google.cloud.bigquery_v2.types import Dataset, Job, Model
from google.cloud.bigquery_v2 import DatasetServiceClient
from google.cloud.bigquery_v2 import JobServiceClient
from google.cloud.bigquery_v2 import ModelServiceClient

from google.cloud.bigquery_v2 import GetDatasetRequest

from google.cloud.bigquery_v2 import ListJobsRequest

from google.cloud.bigquery_v2 import DeleteModelRequest
from google.cloud.bigquery_v2 import GetModelRequest
from google.cloud.bigquery_v2 import PatchModelRequest
from google.cloud.bigquery_v2 import ListModelsRequest


try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


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
    request: Union[
        GetDatasetRequest,
        GetModelRequest,
        DeleteModelRequest,
        PatchModelRequest,
        ListJobsRequest,
        ListModelsRequest,
    ],  # TODO this needs to be simplified.
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
def mock_dataset_service_client():
    """Mocks the DatasetServiceClient."""
    with mock.patch(
        "google.cloud.bigquery_v2.services.centralized_services.client.DatasetServiceClient",
        autospec=True,
    ) as mock_client:
        yield mock_client


@pytest.fixture
def mock_job_service_client():
    """Mocks the JobServiceClient."""
    with mock.patch(
        "google.cloud.bigquery_v2.services.centralized_services.client.JobServiceClient",
        autospec=True,
    ) as mock_client:
        yield mock_client


@pytest.fixture
def mock_model_service_client():
    """Mocks the ModelServiceClient."""
    with mock.patch(
        "google.cloud.bigquery_v2.services.centralized_services.client.ModelServiceClient",
        autospec=True,
    ) as mock_client:
        yield mock_client


# TODO: figure out a solution for this... is there an easier way to feed in clients?
# TODO: is there an easier way to make mock_x_service_clients?
@pytest.fixture
def bq_client(
    mock_dataset_service_client, mock_job_service_client, mock_model_service_client
):
    """Provides a BigQueryClient with mocked underlying services."""
    client = BigQueryClient()
    client.dataset_service_client = mock_dataset_service_client
    client.job_service_client = mock_job_service_client
    client.model_service_client = mock_model_service_client
    ...
    return client


# --- TEST CLASSES ---


class TestCentralizedClientDatasetService:
    def test_get_dataset(self, bq_client, mock_dataset_service_client):
        # Arrange
        expected_dataset = Dataset(
            kind="bigquery#dataset", id=f"{PROJECT_ID}:{DATASET_ID}"
        )
        mock_dataset_service_client.get_dataset.return_value = expected_dataset
        get_dataset_request = GetDatasetRequest(
            project_id=PROJECT_ID, dataset_id=DATASET_ID
        )

        # Act
        dataset = bq_client.get_dataset(request=get_dataset_request)

        # Assert
        assert dataset == expected_dataset
        assert_client_called_once_with(
            mock_dataset_service_client.get_dataset, get_dataset_request
        )


class TestCentralizedClientJobService:
    def test_list_jobs(self, bq_client, mock_job_service_client):
        # Arrange
        expected_jobs = [Job(kind="bigquery#job", id=f"{PROJECT_ID}:{JOB_ID}")]
        mock_job_service_client.list_jobs.return_value = expected_jobs
        list_jobs_request = ListJobsRequest(project_id=PROJECT_ID)

        # Act
        jobs = bq_client.list_jobs(request=list_jobs_request)

        # Assert
        assert jobs == expected_jobs
        assert_client_called_once_with(
            mock_job_service_client.list_jobs, list_jobs_request
        )


class TestCentralizedClientModelService:
    def test_get_model(self, bq_client, mock_model_service_client):
        # Arrange
        expected_model = Model(
            etag=DEFAULT_ETAG,
            model_reference={
                "project_id": PROJECT_ID,
                "dataset_id": DATASET_ID,
                "model_id": MODEL_ID,
            },
        )
        mock_model_service_client.get_model.return_value = expected_model
        get_model_request = GetModelRequest(
            project_id=PROJECT_ID, dataset_id=DATASET_ID, model_id=MODEL_ID
        )

        # Act
        model = bq_client.get_model(request=get_model_request)

        # Assert
        assert model == expected_model
        assert_client_called_once_with(
            mock_model_service_client.get_model, get_model_request
        )

    def test_delete_model(self, bq_client, mock_model_service_client):
        # Arrange
        # The underlying service call returns nothing on success.
        mock_model_service_client.delete_model.return_value = None
        delete_model_request = DeleteModelRequest(
            project_id=PROJECT_ID, dataset_id=DATASET_ID, model_id=MODEL_ID
        )

        # Act
        # The wrapper method should also return nothing.
        result = bq_client.delete_model(request=delete_model_request)

        # Assert
        # 1. Assert the return value is None. This fails if the method doesn't exist.
        assert result is None
        # 2. Assert the underlying service was called correctly.
        assert_client_called_once_with(
            mock_model_service_client.delete_model,
            delete_model_request,
        )

    def test_patch_model(self, bq_client, mock_model_service_client):
        # Arrange
        expected_model = Model(
            etag="new_etag",
            model_reference={
                "project_id": PROJECT_ID,
                "dataset_id": DATASET_ID,
                "model_id": MODEL_ID,
            },
            description="A newly patched description.",
        )
        mock_model_service_client.patch_model.return_value = expected_model

        model_patch = Model(description="A newly patched description.")
        patch_model_request = PatchModelRequest(
            project_id=PROJECT_ID,
            dataset_id=DATASET_ID,
            model_id=MODEL_ID,
            model=model_patch,
        )

        # Act
        patched_model = bq_client.patch_model(request=patch_model_request)

        # Assert
        assert patched_model == expected_model
        assert_client_called_once_with(
            mock_model_service_client.patch_model, patch_model_request
        )

    def test_list_models(self, bq_client, mock_model_service_client):
        # Arrange
        expected_models = [
            Model(
                etag=DEFAULT_ETAG,
                model_reference={
                    "project_id": PROJECT_ID,
                    "dataset_id": DATASET_ID,
                    "model_id": MODEL_ID,
                },
            )
        ]
        mock_model_service_client.list_models.return_value = expected_models
        list_models_request = ListModelsRequest(
            project_id=PROJECT_ID, dataset_id=DATASET_ID
        )
        # Act
        models = bq_client.list_models(request=list_models_request)

        # Assert
        assert models == expected_models
        assert_client_called_once_with(
            mock_model_service_client.list_models, list_models_request
        )
