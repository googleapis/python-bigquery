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

# Import service clients
from google.cloud.bigquery_v2.services.dataset_service import DatasetServiceClient
from google.cloud.bigquery_v2.services.job_service import JobServiceClient
from google.cloud.bigquery_v2.services.model_service import ModelServiceClient

# Import Request classes
from google.cloud.bigquery_v2.types import (
    # DatasetService Request classes
    GetDatasetRequest,
    # JobService Request classes
    ListJobsRequest,
    # ModelService Request classes
    DeleteModelRequest,
    GetModelRequest,
    PatchModelRequest,
    ListModelsRequest,
)

from google.api_core import gapic_v1
from google.api_core import retry as retries

# Create a type alias
try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

# TODO: revise this universally.
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

DEFAULT_RETRY: OptionalRetry = gapic_v1.method.DEFAULT
DEFAULT_TIMEOUT: Union[float, object] = gapic_v1.method.DEFAULT
DEFAULT_METADATA: Sequence[Tuple[str, Union[str, bytes]]] = ()


def _drop_self_key(kwargs):
    "Drops 'self' key from a given kwargs dict."

    if not isinstance(kwargs, dict):
        raise TypeError("kwargs must be a dict.")
    kwargs.pop("self", None)  # Essentially a no-op if 'self' key does not exist
    return kwargs


# Create Centralized Client
class BigQueryClient:
    def __init__(self):
        # Dataset service related init attributes
        self.dataset_service_client = DatasetServiceClient()
        self.job_service_client = JobServiceClient()
        self.model_service_client = ModelServiceClient()

    def get_dataset(
        self,
        request: Optional[Union[GetDatasetRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Add docstring.
        """
        kwargs = _drop_self_key(locals())
        return self.dataset_service_client.get_dataset(**kwargs)

    def list_jobs(
        self,
        request: Optional[Union[ListJobsRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Add docstring.
        """
        kwargs = _drop_self_key(locals())
        return self.job_service_client.list_jobs(**kwargs)

    def get_model(
        self,
        request: Optional[Union[GetModelRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Add docstring.
        """
        kwargs = _drop_self_key(locals())
        return self.model_service_client.get_model(**kwargs)

    def delete_model(
        self,
        request: Optional[Union[DeleteModelRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Add docstring.
        """
        kwargs = _drop_self_key(locals())
        # The underlying GAPIC client returns None on success.
        return self.model_service_client.delete_model(**kwargs)

    def patch_model(
        self,
        request: Optional[Union[PatchModelRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Add docstring.
        """
        kwargs = _drop_self_key(locals())
        return self.model_service_client.patch_model(**kwargs)

    def list_models(
        self,
        request: Optional[Union[ListModelsRequest, dict]] = None,
        *,
        retry: OptionalRetry = DEFAULT_RETRY,
        timeout: Union[float, object] = DEFAULT_TIMEOUT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = DEFAULT_METADATA,
    ):
        """
        TODO: Add docstring.
        """
        kwargs = _drop_self_key(locals())
        return self.model_service_client.list_models(**kwargs)


# ===============================================
# Sample TODO: Relocate this to a samples file
# ===============================================

# Instantiate BQClient class
bqclient = BigQueryClient()

# Instantiate Request class
get_dataset_request = GetDatasetRequest(
    project_id=PROJECT_ID,
    dataset_id="experimental",
)

# Generate response
dataset = bqclient.get_dataset(request=get_dataset_request)

# Display response
print(f"GET DATASET:\n\t{dataset.id=}\n")
