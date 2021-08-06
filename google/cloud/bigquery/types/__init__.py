# Copyright 2021 Google LLC
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

# NOTE: This subpackage define type classes that were previously generated from protobuf
# definitions in library versions before 3.0.

from .standard_sql import (
    StandardSqlDataType,
    StandardSqlField,
    StandardSqlStructType,
    StandardSqlTableType,
)

__all__ = (
    "StandardSqlDataType",
    "StandardSqlField",
    "StandardSqlStructType",
    "StandardSqlTableType",
)
