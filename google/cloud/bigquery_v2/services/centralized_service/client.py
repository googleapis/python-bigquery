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
    job,
    model,
)

from google.api_core import client_options as client_options_lib
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as auth_credentials

# Create a type alias
try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

# TODO: This line is here to simplify prototyping, etc.
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

DEFAULT_RETRY: OptionalRetry = gapic_v1.method.DEFAULT
DEFAULT_TIMEOUT: Union[float, object] = gapic_v1.method.DEFAULT
DEFAULT_METADATA: Sequence[Tuple[str, Union[str, bytes]]] = ()


# Create Centralized Client
class BigQueryClient:
    def __init__(
        self,
        *,
        credentials: Optional[auth_credentials.Credentials] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
    ):
        self._clients = {}
        self._credentials = credentials
        self._client_options = client_options

    @property
    def dataset_service_client(self):
        if "dataset" not in self._clients:
            from google.cloud.bigquery_v2.services import dataset_service
            self._clients["dataset"] = dataset_service.DatasetServiceClient(
                credentials=self._credentials, client_options=self._client_options
            )
        return self._clients["dataset"]

    @dataset_service_client.setter
    def dataset_service_client(self, value):
        # Check for the methods that this class most commonly uses (duck typing)
        required_methods = [
            "get_dataset",
            "insert_dataset",
            "patch_dataset",
            "update_dataset",
            "delete_dataset",
            "list_datasets",
            "undelete_dataset",
        ]
        for method in required_methods:
            if not hasattr(value, method) or not callable(getattr(value, method)):
                raise AttributeError(
                    f"Object assigned to dataset_service_client is missing a callable '{method}' method."
                )
        self._clients["dataset"] = value

    @property
    def job_service_client(self):
        if "job" not in self._clients:
            from google.cloud.bigquery_v2.services import job_service
            self._clients["job"] = job_service.JobServiceClient(
                credentials=self._credentials, client_options=self._client_options
            )
        return self._clients["job"]

    @job_service_client.setter
    def job_service_client(self, value):
        required_methods = [
            "get_job",
            "insert_job",
            "cancel_job",
            "delete_job",
            "list_jobs",
        ]
        for method in required_methods:
            if not hasattr(value, method) or not callable(getattr(value, method)):
                raise AttributeError(
                    f"Object assigned to job_service_client is missing a callable '{method}' method."
                )
        self._clients["job"] = value

    @property
    def model_service_client(self):
        if "model" not in self._clients:
            from google.cloud.bigquery_v2.services import model_service
            self._clients["model"] = model_service.ModelServiceClient(
                credentials=self._credentials, client_options=self._client_options
            )
        return self._clients["model"]

    @model_service_client.setter
    def model_service_client(self, value):
        required_methods = [
            "get_model",
            "delete_model",
            "patch_model",
            "list_models",
        ]
        for method in required_methods:
            if not hasattr(value, method) or not callable(getattr(value, method)):
                raise AttributeError(
                    f"Object assigned to model_service_client is missing a callable '{method}' method."
                )
        self._clients["model"] = value

    def get_dataset(
        self,
        request: Optional[Union[dataset.GetDatasetRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        kwargs = _helpers._drop_self_key(locals())
        return self.dataset_service_client.get_dataset(**kwargs)

    def list_datasets(
        self,
        request: Optional[Union[dataset.ListDatasetsRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Docstring is purposefully blank. microgenerator will add automatically.
        """
        kwargs = _helpers._drop_self_key(locals())
        return self.dataset_service_client.list_datasets(**kwargs)

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
