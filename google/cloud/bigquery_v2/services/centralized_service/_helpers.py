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

from typing import Any, Callable, Optional, Type, TypeVar


T = TypeVar("T")


def _drop_self_key(kwargs):
    """Drops 'self' key from a given kwargs dict."""

    if not isinstance(kwargs, dict):
        raise TypeError("kwargs must be a dict.")
    kwargs.pop("self", None)  # Essentially a no-op if 'self' key does not exist
    return kwargs


def _make_request(
    request_class: Type[T],
    user_request: Optional[T],
    identifier_value: Optional[Any],
    identifier_name: str,
    parser: Callable[..., Any],
    identifier_required: bool = True,
) -> T:
    """A factory for creating *Request objects.

    This function simplifies the creation of request objects by extracting identifier
    values from strings (e.g., 'project_id.dataset_id') and using them to instantiate
    the appropriate request object. It allows users to continue using identifier
    strings with BigQueryClient methods, even though the underlying *ServiceClient
    methods do not directly support this convenience.

    For example, this helper is used in methods like:
    - BigQueryClient.get_dataset()
    - BigQueryClient.delete_dataset()

    Args:
        request_class: The class of the request object to create (e.g.,
            GetDatasetRequest, ListModelsRequest).
        user_request: A user-provided *Request object. If not None, this
            object is returned directly.
        identifier_value: The value to be parsed to create the request object
            (e.g., a dataset_id for GetDatasetRequest).
        identifier_name: The name of the identifier field (e.g., 'dataset_id',
            'job_id').
        parser: A callable that takes the identifier_value and returns a dict
            of fields for the request object. For example, a parser could
            separate a 'project_id.dataset_id' string into its components.
        identifier_required: Whether the identifier is required. Defaults to True.

    Returns:
        A *Request object.

    Raises:
        ValueError: If both user_request and identifier_value are provided, or
            if identifier_required is True and both are None.

    Example:
        request = _make_request(
            request_class=dataset.GetDatasetRequest,
            user_request=request,
            identifier_value=dataset_id,
            identifier_name="dataset_id",
            parser=self._parse_dataset_id_to_dict,
            identifier_required=True,
        )
    """
    if user_request is not None and identifier_value is not None:
        raise ValueError(
            f"Provide either a request object or '{identifier_name}', not both."
        )

    if user_request is not None:
        return user_request

    if identifier_required and identifier_value is None:
        raise ValueError(
            f"Either a request object or '{identifier_name}' must be provided."
        )

    if identifier_value is None:
        request_fields = parser()
    else:
        request_fields = parser(identifier_value)
    return request_class(**request_fields)
