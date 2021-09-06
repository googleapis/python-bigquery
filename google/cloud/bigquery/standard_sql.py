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
from typing import Any, Dict, Iterable, Optional

from google.cloud.bigquery.enums import StandardSqlTypeNames


@dataclass
class StandardSqlDataType:
    """The type of a variable, e.g., a function argument.

    See:
    https://cloud.google.com/bigquery/docs/reference/rest/v2/StandardSqlDataType

    Examples:

    .. code-block:: text

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

    type_kind: Optional[
        StandardSqlTypeNames
    ] = StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED
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

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this SQL data type."""

        if not self.type_kind:
            type_kind = StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED.value
        else:
            type_kind = self.type_kind.value

        result = {"typeKind": type_kind}

        if self.type_kind == StandardSqlTypeNames.ARRAY:
            if not self.array_element_type:
                array_type = None
            else:
                array_type = self.array_element_type.to_api_repr()
            result["arrayElementType"] = array_type
        elif self.type_kind == StandardSqlTypeNames.STRUCT:
            if not self.struct_type:
                struct_type = None
            else:
                struct_type = self.struct_type.to_api_repr()
            result["structType"] = struct_type

        return result

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]):
        """Construct an SQL data type instance given its API representation."""
        type_kind = resource.get("typeKind")
        if type_kind not in StandardSqlTypeNames.__members__:
            type_kind = StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED
        else:
            # Convert string to an enum member.
            type_kind = StandardSqlTypeNames[  # pytype: disable=missing-parameter
                type_kind
            ]

        array_element_type = None
        if type_kind == cls.type_kind.ARRAY:
            element_type = resource.get("arrayElementType", {})
            array_element_type = cls.from_api_repr(element_type)

        struct_type = None
        if type_kind == StandardSqlTypeNames.STRUCT:
            struct_info = resource.get("structType", {})
            struct_type = StandardSqlStructType.from_api_repr(struct_info)

        return cls(type_kind, array_element_type, struct_type)


@dataclass
class StandardSqlField:
    """A field or a column.

    See:
    https://cloud.google.com/bigquery/docs/reference/rest/v2/StandardSqlField
    """

    name: Optional[str] = None
    """The name of this field. Can be absent for struct fields."""

    type: Optional["StandardSqlDataType"] = None
    """The type of this parameter. Absent if not explicitly specified.

    For example, CREATE FUNCTION statement can omit the return type; in this case the
    output parameter does not have this "type" field).
    """

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this SQL field."""
        type_repr = None if self.type is None else self.type.to_api_repr()
        return {"name": self.name, "type": type_repr}

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]):
        """Construct an SQL field instance given its API representation."""
        result = cls(
            name=resource.get("name"),
            type=StandardSqlDataType.from_api_repr(resource.get("type", {})),
        )
        return result


@dataclass(init=False)
class StandardSqlStructType:
    """Type of a struct field.

    See:
    https://cloud.google.com/bigquery/docs/reference/rest/v2/StandardSqlDataType#StandardSqlStructType
    """

    fields: Optional[Iterable["StandardSqlField"]]

    def __init__(self, fields=None):
        self.fields = [] if fields is None else [field for field in fields]

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this SQL struct type."""
        fields = [field.to_api_repr() for field in self.fields]
        result = {"fields": fields}
        return result

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]) -> "StandardSqlStructType":
        """Construct an SQL struct type instance given its API representation."""
        fields = (
            StandardSqlField.from_api_repr(field)
            for field in resource.get("fields", [])
        )
        return cls(fields=fields)


@dataclass(init=False)
class StandardSqlTableType:
    """A table type.

    https://cloud.google.com/workflows/docs/reference/googleapis/bigquery/v2/Overview#StandardSqlTableType
    """

    columns: Iterable[StandardSqlField]
    """The columns in this table type"""

    def __init__(self, columns: Iterable[StandardSqlField]):
        self.columns = [col for col in columns]

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this SQL table type."""
        columns = [col.to_api_repr() for col in self.columns]
        return {"columns": columns}

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]) -> "StandardSqlTableType":
        """Construct an SQL table type instance given its API representation."""
        columns = (
            StandardSqlField(
                name=column.get("name"),
                type=StandardSqlDataType.from_api_repr(column.get("type", {})),
            )
            for column in resource.get("columns", [])
        )
        return cls(columns=columns)
