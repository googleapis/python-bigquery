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

import os
from typing import (
    Dict,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from google.cloud.bigquery_v2.services.centralized_service import _helpers

# Import service client modules
from google.cloud.bigquery_v2.services import (
    dataset_service,
    job_service,
    model_service,
)

# Import types modules (to access *Requests classes)
from google.cloud.bigquery_v2.types import (
    dataset,
    dataset_reference,
    job,
    model,
)

from google.api_core import client_options as client_options_lib
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as auth_credentials

# Create type aliases
try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

DatasetIdentifier = Union[str, dataset_reference.DatasetReference]

# TODO: This variable is here to simplify prototyping, etc.
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DEFAULT_RETRY: OptionalRetry = gapic_v1.method.DEFAULT
DEFAULT_TIMEOUT: Union[float, object] = gapic_v1.method.DEFAULT
DEFAULT_METADATA: Sequence[Tuple[str, Union[str, bytes]]] = ()

# Create Centralized Client
class BigQueryClient:
    """A centralized client for BigQuery API."""

    def __init__(
        self,
        *,
        credentials: Optional[auth_credentials.Credentials] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
    ):
        """
        Initializes the BigQueryClient.

        Args:
            credentials:
                The credentials to use for authentication. If not provided, the
                client will attempt to use the default credentials.
            client_options:
                A dictionary of client options to pass to the underlying
                service clients.
        """

        self._clients: Dict[str, object] = {}
        self._credentials = credentials
        self._client_options = client_options
        self.project = PROJECT_ID

    # --- HELPER METHODS ---
    def _parse_dataset_path(self, dataset_path: str) -> Tuple[Optional[str], str]:
        """
        Helper to parse project and dataset from a string identifier.

        Args:
            dataset_path: A string in the format 'project_id.dataset_id' or
                'dataset_id'.

        Returns:
            A tuple of (project_id, dataset_id).
        """
        if "." in dataset_path:
            project_id, dataset_id = dataset_path.split(".", 1)
            return project_id, dataset_id
        return self.project, dataset_path

    def _parse_dataset_id_to_dict(self, dataset_id: DatasetIdentifier) -> dict:
        if isinstance(dataset_id, str):
            project_id, dataset_id_str = self._parse_dataset_path(dataset_id)
            return {"project_id": project_id, "dataset_id": dataset_id_str}
        elif isinstance(dataset_id, dataset_reference.DatasetReference):
            return {
                "project_id": dataset_id.project_id,
                "dataset_id": dataset_id.dataset_id,
            }
        else:
            raise TypeError(f"Invalid type for dataset_id: {type(dataset_id)}")

    def _parse_project_id_to_dict(self, project_id: Optional[str] = None) -> dict:
        """Helper to create a request dictionary from a project_id."""
        final_project_id = project_id or self.project
        return {"project_id": final_project_id}

    # --- *SERVICECLIENT ATTRIBUTES ---
    @property
    def dataset_service_client(self):
        if "dataset" not in self._clients:
            self._clients["dataset"] = dataset_service.DatasetServiceClient(
                credentials=self._credentials, client_options=self._client_options
            )
        return self._clients["dataset"]

    @dataset_service_client.setter
    def dataset_service_client(self, value):
        if not isinstance(value, dataset_service.DatasetServiceClient):
            raise TypeError(
                "Expected an instance of dataset_service.DatasetServiceClient."
            )
        self._clients["dataset"] = value

    @property
    def job_service_client(self):
        if "job" not in self._clients:
            self._clients["job"] = job_service.JobServiceClient(
                credentials=self._credentials, client_options=self._client_options
            )
        return self._clients["job"]

    @job_service_client.setter
    def job_service_client(self, value):
        if not isinstance(value, job_service.JobServiceClient):
            raise TypeError("Expected an instance of job_service.JobServiceClient.")
        self._clients["job"] = value

    @property
    def model_service_client(self):
        if "model" not in self._clients:
            self._clients["model"] = model_service.ModelServiceClient(
                credentials=self._credentials, client_options=self._client_options
            )
        return self._clients["model"]

    @model_service_client.setter
    def model_service_client(self, value):
        if not isinstance(value, model_service.ModelServiceClient):
            raise TypeError("Expected an instance of model_service.ModelServiceClient.")
        self._clients["model"] = value

    # --- *SERVICECLIENT METHODS ---
    def get_dataset(
        self,
        dataset_id: Optional[DatasetIdentifier] = None,
        *,
        request: Optional["dataset.GetDatasetRequest"] = None,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ) -> "dataset.Dataset":
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        final_request = _helpers._make_request(
            request_class=dataset.GetDatasetRequest,
            user_request=request,
            identifier_value=dataset_id,
            identifier_name="dataset_id",
            parser=self._parse_dataset_id_to_dict,
            identifier_required=True,
        )

        return self.dataset_service_client.get_dataset(
            request=final_request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_datasets(
        self,
        project_id: Optional[str] = None,
        *,
        request: Optional["dataset.ListDatasetsRequest"] = None,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        final_request = _helpers._make_request(
            request_class=dataset.ListDatasetsRequest,
            user_request=request,
            identifier_value=project_id,
            identifier_name="project_id",
            parser=self._parse_project_id_to_dict,
            identifier_required=False,
        )

        return self.dataset_service_client.list_datasets(
            request=final_request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_jobs(
        self,
        request: Optional[Union[job.ListJobsRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        kwargs = _helpers._drop_self_key(locals())
        return self.job_service_client.list_jobs(**kwargs)

    def get_model(
        self,
        request: Optional[Union[model.GetModelRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        kwargs = _helpers._drop_self_key(locals())
        return self.model_service_client.get_model(**kwargs)

    def delete_model(
        self,
        request: Optional[Union[model.DeleteModelRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        kwargs = _helpers._drop_self_key(locals())
        # The underlying GAPIC client returns None on success.
        return self.model_service_client.delete_model(**kwargs)

    def patch_model(
        self,
        request: Optional[Union[model.PatchModelRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        kwargs = _helpers._drop_self_key(locals())
        return self.model_service_client.patch_model(**kwargs)

    def list_models(
        self,
        request: Optional[Union[model.ListModelsRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        kwargs = _helpers._drop_self_key(locals())
        return self.model_service_client.list_models(**kwargs)
