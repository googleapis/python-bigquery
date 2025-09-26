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

"""A utility module for handling name transformations."""

import re
from typing import Dict


def to_snake_case(name: str) -> str:
    """Converts a PascalCase name to snake_case, handling acronyms."""
    if not name:
        return ""
    # Add underscore between lower and upper case
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    # Add underscore between multiple upper case and a following lower case
    name = re.sub(r"([A-Z])([A-Z][a-z])", r"\1_\2", name)
    return name.lower()


def generate_service_names(class_name: str) -> Dict[str, str]:
    """
    Generates various name formats for a service based on its client class name.

    Args:
        class_name: The PascalCase name of the service client class
                    (e.g., 'DatasetServiceClient').

    Returns:
        A dictionary containing different name variations.
    """
    snake_case_name = to_snake_case(class_name)
    module_name = snake_case_name.replace("_client", "")
    service_name = module_name.replace("_service", "")

    return {
        "service_name": service_name,
        "service_module_name": module_name,
        "service_client_class": class_name,
        "property_name": snake_case_name,  # Direct use of snake_case_name
    }


def method_to_request_class_name(method_name: str) -> str:
    """
    Converts a snake_case method name to a PascalCase Request class name.

    This follows the convention where a method like `get_dataset` corresponds
    to a `GetDatasetRequest` class.

    Args:
        method_name: The snake_case name of the API method.

    Returns:
        The inferred PascalCase name for the corresponding request class.

    Raises:
        ValueError: If method_name is empty.

    Example:
        >>> method_to_request_class_name('get_dataset')
        'GetDatasetRequest'
        >>> method_to_request_class_name('list_jobs')
        'ListJobsRequest'
    """
    if not method_name:
        raise ValueError("method_name cannot be empty")

    # e.g., "get_dataset" -> ["get", "dataset"]
    parts = method_name.split("_")
    # e.g., ["get", "dataset"] -> "GetDataset"
    pascal_case_base = "".join(part.capitalize() for part in parts)
    return f"{pascal_case_base}Request"
