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


def _drop_self_key(kwargs):
    "Drops 'self' key from a given kwargs dict."

    if not isinstance(kwargs, dict):
        raise TypeError("kwargs must be a dict.")
    kwargs.pop("self", None)  # Essentially a no-op if 'self' key does not exist
    return kwargs


def _make_request(
    request_class,
    user_request,
    identifier_value,
    identifier_name: str,
    parser,
    identifier_required: bool = True,
):
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
