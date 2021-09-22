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

import copy
from typing import Any, Dict, Generator, Iterable, List, Optional

from google.cloud.bigquery.enums import StandardSqlTypeNames


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

    Args:
        type_kind:
            The top level type of this field. Can be any standard SQL data type,
            e.g. INT64, DATE, ARRAY.
        array_element_type:
            The type of the array's elements, if type_kind is ARRAY.
        struct_type:
            The fields of this struct, in order, if type_kind is STRUCT.
    """

    def __init__(
        self,
        type_kind: Optional[
            StandardSqlTypeNames
        ] = StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED,
        array_element_type: Optional["StandardSqlDataType"] = None,
        struct_type: Optional["StandardSqlStructType"] = None,
    ):
        if array_element_type is not None and struct_type is not None:
            raise ValueError(
                "array_element_type and struct_type are mutally exclusive."
            )

        self._properties = {}

        self.type_kind = type_kind
        self.array_element_type = array_element_type
        self.struct_type = struct_type

    @property
    def type_kind(self) -> StandardSqlTypeNames:
        """The top level type of this field.

        Can be any standard SQL data type, e.g. INT64, DATE, ARRAY.
        """
        kind = self._properties["typeKind"]
        return StandardSqlTypeNames[kind]  # pytype: disable=missing-parameter

    @type_kind.setter
    def type_kind(self, value: Optional[StandardSqlTypeNames]):
        new_instance = "typeKind" not in self._properties

        if not new_instance:
            current = self._properties.get("typeKind")

            if value == current:
                return  # Nothing to change.

            if (
                current == StandardSqlTypeNames.ARRAY
                and self.array_element_type.type_kind
                is not StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED
            ):
                raise ValueError(
                    "Cannot change {StandardSqlTypeNames.ARRAY} type_kind, first set "
                    "array_element_type attribute to None."
                )

            if current == StandardSqlTypeNames.STRUCT and self.struct_type.fields:
                raise ValueError(
                    "Cannot change {StandardSqlTypeNames.STRUCT} type_kind, first set "
                    "struct_type attribute to None."
                )

        if not value:
            kind = StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED.value
        else:
            kind = value.value
        self._properties["typeKind"] = kind

    @property
    def array_element_type(self) -> Optional["StandardSqlDataType"]:
        """The type of the array's elements, if type_kind is ARRAY."""
        result = None
        if self.type_kind == StandardSqlTypeNames.ARRAY:
            element_type = self._properties.get("arrayElementType")
            if element_type is not None:
                result = StandardSqlDataType.from_api_repr(element_type)
            else:
                result = StandardSqlDataType()

        return result

    @array_element_type.setter
    def array_element_type(self, value: Optional["StandardSqlDataType"]):
        if self.type_kind != StandardSqlTypeNames.ARRAY and value is not None:
            raise ValueError(
                "Cannot set to a non-None value if type_kind is not "
                f"{StandardSqlTypeNames.ARRAY.value}."
            )

        element_type = None if value is None else value.to_api_repr()

        if element_type is None:
            self._properties.pop("arrayElementType", None)
        else:
            self._properties["arrayElementType"] = element_type

    @property
    def struct_type(self) -> Optional["StandardSqlStructType"]:
        """The fields of this struct, in order, if type_kind is STRUCT."""
        result = None
        if self.type_kind == StandardSqlTypeNames.STRUCT:
            struct_info = self._properties.get("structType")
            if struct_info is not None:
                result = StandardSqlStructType.from_api_repr(struct_info)
            else:
                result = StandardSqlStructType()

        return result

    @struct_type.setter
    def struct_type(self, value: Optional["StandardSqlStructType"]):
        if self.type_kind != StandardSqlTypeNames.STRUCT and value is not None:
            raise ValueError(
                "Cannot set to a non-None value if type_kind is not "
                f"{StandardSqlTypeNames.STRUCT.value}."
            )

        struct_type = None if value is None else value.to_api_repr()

        if struct_type is None:
            self._properties.pop("structType", None)
        else:
            self._properties["structType"] = struct_type

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this SQL data type."""
        return copy.deepcopy(self._properties)

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
        if type_kind == StandardSqlTypeNames.ARRAY:
            element_type = resource.get("arrayElementType")
            if element_type:
                array_element_type = cls.from_api_repr(element_type)

        struct_type = None
        if type_kind == StandardSqlTypeNames.STRUCT:
            struct_info = resource.get("structType")
            if struct_info:
                struct_type = StandardSqlStructType.from_api_repr(struct_info)

        return cls(type_kind, array_element_type, struct_type)

    def __eq__(self, other):
        if not isinstance(other, StandardSqlDataType):
            return NotImplemented
        else:
            return (
                self.type_kind == other.type_kind
                and self.array_element_type == other.array_element_type
                and self.struct_type == other.struct_type
            )

    __hash__ = None


class StandardSqlField:
    """A field or a column.

    See:
    https://cloud.google.com/bigquery/docs/reference/rest/v2/StandardSqlField

    Args:
        name:
            The name of this field. Can be absent for struct fields.
        type:
            The type of this parameter. Absent if not explicitly specified.

            For example, CREATE FUNCTION statement can omit the return type; in this
            case the output parameter does not have this "type" field).
    """

    def __init__(
        self, name: Optional[str] = None, type: Optional[StandardSqlDataType] = None
    ):
        if type is not None:
            type = type.to_api_repr()

        self._properties = {"name": name, "type": type}

    @property
    def name(self):
        """The name of this field. Can be absent for struct fields."""
        return self._properties["name"]

    @name.setter
    def name(self, value: Optional[str]):
        self._properties["name"] = value

    @property
    def type(self):
        """The type of this parameter. Absent if not explicitly specified.

        For example, CREATE FUNCTION statement can omit the return type; in this
        case the output parameter does not have this "type" field).
        """
        result = self._properties["type"]
        if result is not None:
            result = StandardSqlDataType.from_api_repr(result)
        return result

    @type.setter
    def type(self, value: Optional[StandardSqlDataType]):
        if value is not None:
            value = value.to_api_repr()
        self._properties["type"] = value

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this SQL field."""
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]):
        """Construct an SQL field instance given its API representation."""
        result = cls(
            name=resource.get("name"),
            type=StandardSqlDataType.from_api_repr(resource.get("type", {})),
        )
        return result

    def __eq__(self, other):
        if not isinstance(other, StandardSqlField):
            return NotImplemented
        else:
            return self.name == other.name and self.type == other.type

    __hash__ = None


class StandardSqlStructType:
    """Type of a struct field.

    See:
    https://cloud.google.com/bigquery/docs/reference/rest/v2/StandardSqlDataType#StandardSqlStructType

    Args:
        fields: The fields in this struct.
    """

    def __init__(self, fields: Optional[Iterable[StandardSqlField]] = None):
        if fields is None:
            fields = []
        self._properties = {"fields": [field.to_api_repr() for field in fields]}

    @property
    def fields(self) -> List[StandardSqlField]:
        """The fields in this struct."""
        result = self._fields_from_resource(self._properties)
        return list(result)

    @fields.setter
    def fields(self, value: Iterable[StandardSqlField]):
        self._properties["fields"] = [field.to_api_repr() for field in value]

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this SQL struct type."""
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]) -> "StandardSqlStructType":
        """Construct an SQL struct type instance given its API representation."""
        fields = cls._fields_from_resource(resource)
        return cls(fields=fields)

    @staticmethod
    def _fields_from_resource(
        resource: Dict[str, Any]
    ) -> Generator[StandardSqlField, None, None]:
        """Yield field instancess based on the resource info."""
        for field_resource in resource.get("fields", []):
            yield StandardSqlField.from_api_repr(field_resource)

    def __eq__(self, other):
        if not isinstance(other, StandardSqlStructType):
            return NotImplemented
        else:
            return self.fields == other.fields

    __hash__ = None


class StandardSqlTableType:
    """A table type.

    See:
    https://cloud.google.com/workflows/docs/reference/googleapis/bigquery/v2/Overview#StandardSqlTableType

    Args:
        columns: The columns in this table type.
    """

    def __init__(self, columns: Iterable[StandardSqlField]):
        self._properties = {"columns": [col.to_api_repr() for col in columns]}

    @property
    def columns(self) -> List[StandardSqlField]:
        """The columns in this table type."""
        return list(self._columns_from_resource(self._properties))

    @columns.setter
    def columns(self, value: Iterable[StandardSqlField]):
        self._properties["columns"] = [col.to_api_repr() for col in value]

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this SQL table type."""
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]) -> "StandardSqlTableType":
        """Construct an SQL table type instance given its API representation."""
        columns = cls._columns_from_resource(resource)
        return cls(columns=columns)

    @staticmethod
    def _columns_from_resource(
        resource: Dict[str, Any]
    ) -> Generator[StandardSqlField, None, None]:
        """Yield column instances based on the resource info."""
        for column in resource.get("columns", []):
            type_ = column.get("type")
            if type_ is None:
                type_ = {}

            yield StandardSqlField(
                name=column.get("name"), type=StandardSqlDataType.from_api_repr(type_),
            )

    def __eq__(self, other):
        if not isinstance(other, StandardSqlTableType):
            return NotImplemented
        else:
            return self.columns == other.columns

    __hash__ = None
