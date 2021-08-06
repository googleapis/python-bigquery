# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
import enum
from typing import Iterable, Optional


@dataclass
class StandardSqlDataType:
    """The type of a variable, e.g., a function argument.

    Examples:

    INT64: {type_kind="INT64"}
    ARRAY: {type_kind="ARRAY", array_element_type="STRING"}
    STRUCT<x STRING, y ARRAY>: {
        type_kind="STRUCT",
        struct_type={
            fields=[
                {name="x", type={type_kind="STRING"}},
                {
                    name="y",
                    type={type_kind="ARRAY", array_element_type="DATE"}
                }
            ]
        }
    }
    """

    class TypeKind(str, enum.Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name

        TYPE_KIND_UNSPECIFIED = enum.auto()
        INT64 = enum.auto()
        BOOL = enum.auto()
        FLOAT64 = enum.auto()
        STRING = enum.auto()
        BYTES = enum.auto()
        TIMESTAMP = enum.auto()
        DATE = enum.auto()
        TIME = enum.auto()
        DATETIME = enum.auto()
        INTERVAL = enum.auto()
        GEOGRAPHY = enum.auto()
        NUMERIC = enum.auto()
        BIGNUMERIC = enum.auto()
        JSON = enum.auto()
        ARRAY = enum.auto()
        STRUCT = enum.auto()

    type_kind: Optional[TypeKind] = TypeKind.TYPE_KIND_UNSPECIFIED
    """The top level type of this field. Can be any standard SQL data type,
        e.g. INT64, DATE, ARRAY.
    """

    array_element_type: Optional["StandardSqlDataType"] = None
    """The type of the array's elements, if type_kind is ARRAY."""

    struct_type: Optional["StandardSqlStructType"] = None
    """The fields of this struct, in order, if type_kind is STRUCT."""

    def __post_init__(self):
        if self.array_element_type is not None and self.struct_type is not None:
            raise ValueError(
                "array_element_type and struct_type are mutally exclusive."
            )


@dataclass
class StandardSqlField:
    """A field or a column."""

    name: Optional[str] = None
    """The name of this field. Can be absent for struct fields."""

    type: Optional["StandardSqlDataType"] = None
    """The type of this parameter. Absent if not explicitly specified.

    For example, CREATE FUNCTION statement can omit the return type; in this case the
    output parameter does not have this "type" field).
    """


@dataclass(init=False)
class StandardSqlStructType:
    """Type of a struct field."""

    fields: Optional[Iterable["StandardSqlField"]]

    def __init__(self, fields=None):
        self.fields = [] if fields is None else [field for field in fields]


@dataclass(init=False)
class StandardSqlTableType:
    """A table type"""

    columns: Iterable[StandardSqlField]
    """The columns in this table type"""

    def __init__(self, columns):
        self.columns = [col for col in columns]
