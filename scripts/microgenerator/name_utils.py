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
    """Converts a PascalCase name to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

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
