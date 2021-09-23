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

from google.cloud import bigquery


class TestStandardSqlDataType:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.standard_sql import StandardSqlDataType

        return StandardSqlDataType

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_default_type_kind(self):
        instance = self._make_one()
        assert instance.type_kind == bigquery.StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED

    def test_to_api_repr_no_type_set(self):
        instance = self._make_one()
        instance.type_kind = None

        result = instance.to_api_repr()

        assert result == {"typeKind": "TYPE_KIND_UNSPECIFIED"}

    def test_to_api_repr_scalar_type(self):
        instance = self._make_one(bigquery.StandardSqlTypeNames.FLOAT64)

        result = instance.to_api_repr()

        assert result == {"typeKind": "FLOAT64"}

    def test_to_api_repr_array_type_element_type_missing(self):
        instance = self._make_one(
            bigquery.StandardSqlTypeNames.ARRAY, array_element_type=None
        )

        result = instance.to_api_repr()

        expected = {"typeKind": "ARRAY"}
        assert result == expected

    def test_to_api_repr_array_type_w_element_type(self):
        array_element_type = self._make_one(
            type_kind=bigquery.StandardSqlTypeNames.BOOL
        )
        instance = self._make_one(
            bigquery.StandardSqlTypeNames.ARRAY, array_element_type=array_element_type
        )

        result = instance.to_api_repr()

        expected = {"typeKind": "ARRAY", "arrayElementType": {"typeKind": "BOOL"}}
        assert result == expected

    def test_to_api_repr_struct_type_field_types_missing(self):
        instance = self._make_one(
            bigquery.StandardSqlTypeNames.STRUCT, struct_type=None
        )

        result = instance.to_api_repr()

        assert result == {"typeKind": "STRUCT"}

    def test_to_api_repr_struct_type_w_field_types(self):
        from google.cloud.bigquery.standard_sql import StandardSqlField
        from google.cloud.bigquery.standard_sql import StandardSqlStructType

        StandardSqlDataType = self._get_target_class()
        TypeNames = bigquery.StandardSqlTypeNames

        person_type = StandardSqlStructType(
            fields=[
                StandardSqlField("name", StandardSqlDataType(TypeNames.STRING)),
                StandardSqlField("age", StandardSqlDataType(TypeNames.INT64)),
            ]
        )
        employee_type = StandardSqlStructType(
            fields=[
                StandardSqlField("job_title", StandardSqlDataType(TypeNames.STRING)),
                StandardSqlField("salary", StandardSqlDataType(TypeNames.FLOAT64)),
                StandardSqlField(
                    "employee_info",
                    StandardSqlDataType(
                        type_kind=TypeNames.STRUCT, struct_type=person_type,
                    ),
                ),
            ]
        )

        instance = self._make_one(TypeNames.STRUCT, struct_type=employee_type)
        result = instance.to_api_repr()

        expected = {
            "typeKind": "STRUCT",
            "structType": {
                "fields": [
                    {"name": "job_title", "type": {"typeKind": "STRING"}},
                    {"name": "salary", "type": {"typeKind": "FLOAT64"}},
                    {
                        "name": "employee_info",
                        "type": {
                            "typeKind": "STRUCT",
                            "structType": {
                                "fields": [
                                    {"name": "name", "type": {"typeKind": "STRING"}},
                                    {"name": "age", "type": {"typeKind": "INT64"}},
                                ],
                            },
                        },
                    },
                ],
            },
        }
        assert result == expected

    def test_from_api_repr_empty_resource(self):
        klass = self._get_target_class()
        result = klass.from_api_repr(resource={})

        expected = klass(
            type_kind=bigquery.StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED,
            array_element_type=None,
            struct_type=None,
        )
        assert result == expected

    def test_from_api_repr_scalar_type(self):
        klass = self._get_target_class()
        resource = {"typeKind": "DATE"}

        result = klass.from_api_repr(resource=resource)

        expected = klass(
            type_kind=bigquery.StandardSqlTypeNames.DATE,
            array_element_type=None,
            struct_type=None,
        )
        assert result == expected

    def test_from_api_repr_array_type_full(self):
        klass = self._get_target_class()
        resource = {"typeKind": "ARRAY", "arrayElementType": {"typeKind": "BYTES"}}

        result = klass.from_api_repr(resource=resource)

        expected = klass(
            type_kind=bigquery.StandardSqlTypeNames.ARRAY,
            array_element_type=klass(type_kind=bigquery.StandardSqlTypeNames.BYTES),
            struct_type=None,
        )
        assert result == expected

    def test_from_api_repr_array_type_missing_element_type(self):
        klass = self._get_target_class()
        resource = {"typeKind": "ARRAY"}

        result = klass.from_api_repr(resource=resource)

        expected = klass(
            type_kind=bigquery.StandardSqlTypeNames.ARRAY,
            array_element_type=None,
            struct_type=None,
        )
        assert result == expected

    def test_from_api_repr_struct_type_nested(self):
        from google.cloud.bigquery.standard_sql import StandardSqlField
        from google.cloud.bigquery.standard_sql import StandardSqlStructType

        klass = self._get_target_class()
        TypeNames = bigquery.StandardSqlTypeNames

        resource = {
            "typeKind": "STRUCT",
            "structType": {
                "fields": [
                    {"name": "job_title", "type": {"typeKind": "STRING"}},
                    {"name": "salary", "type": {"typeKind": "FLOAT64"}},
                    {
                        "name": "employee_info",
                        "type": {
                            "typeKind": "STRUCT",
                            "structType": {
                                "fields": [
                                    {"name": "name", "type": {"typeKind": "STRING"}},
                                    {"name": "age", "type": {"typeKind": "INT64"}},
                                ],
                            },
                        },
                    },
                ],
            },
        }

        result = klass.from_api_repr(resource=resource)

        expected = klass(
            type_kind=TypeNames.STRUCT,
            struct_type=StandardSqlStructType(
                fields=[
                    StandardSqlField("job_title", klass(TypeNames.STRING)),
                    StandardSqlField("salary", klass(TypeNames.FLOAT64)),
                    StandardSqlField(
                        "employee_info",
                        klass(
                            type_kind=TypeNames.STRUCT,
                            struct_type=StandardSqlStructType(
                                fields=[
                                    StandardSqlField("name", klass(TypeNames.STRING)),
                                    StandardSqlField("age", klass(TypeNames.INT64)),
                                ]
                            ),
                        ),
                    ),
                ]
            ),
        )
        assert result == expected

    def test_from_api_repr_struct_type_missing_struct_info(self):
        klass = self._get_target_class()
        resource = {"typeKind": "STRUCT"}

        result = klass.from_api_repr(resource=resource)

        expected = klass(
            type_kind=bigquery.StandardSqlTypeNames.STRUCT,
            array_element_type=None,
            struct_type=None,
        )
        assert result == expected

    def test_from_api_repr_struct_type_incomplete_field_info(self):
        from google.cloud.bigquery.standard_sql import StandardSqlField
        from google.cloud.bigquery.standard_sql import StandardSqlStructType

        klass = self._get_target_class()
        TypeNames = bigquery.StandardSqlTypeNames

        resource = {
            "typeKind": "STRUCT",
            "structType": {
                "fields": [
                    {"type": {"typeKind": "STRING"}},  # missing name
                    {"name": "salary"},  # missing type
                ],
            },
        }

        result = klass.from_api_repr(resource=resource)

        expected = klass(
            type_kind=TypeNames.STRUCT,
            struct_type=StandardSqlStructType(
                fields=[
                    StandardSqlField(None, klass(TypeNames.STRING)),
                    StandardSqlField("salary", klass(TypeNames.TYPE_KIND_UNSPECIFIED)),
                ]
            ),
        )
        assert result == expected

    def test_str(self):
        instance = self._make_one(type_kind=bigquery.StandardSqlTypeNames.BOOL)
        bool_type_repr = repr(bigquery.StandardSqlTypeNames.BOOL)
        assert str(instance) == f"StandardSqlDataType(type_kind={bool_type_repr}, ...)"


class TestStandardSqlTableType:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.standard_sql import StandardSqlTableType

        return StandardSqlTableType

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_columns_shallow_copy(self):
        from google.cloud.bigquery.standard_sql import StandardSqlField

        columns = [
            StandardSqlField("foo"),
            StandardSqlField("bar"),
            StandardSqlField("baz"),
        ]

        instance = self._make_one(columns=columns)

        assert len(instance.columns) == 3
        columns.pop()
        assert len(instance.columns) == 3  # Still the same.

    def test_to_api_repr_no_columns(self):
        instance = self._make_one(columns=[])
        result = instance.to_api_repr()
        assert result == {"columns": []}

    def test_to_api_repr_with_columns(self):
        from google.cloud.bigquery.standard_sql import StandardSqlField

        columns = [StandardSqlField("foo"), StandardSqlField("bar")]
        instance = self._make_one(columns=columns)

        result = instance.to_api_repr()

        expected = {
            "columns": [{"name": "foo", "type": None}, {"name": "bar", "type": None}]
        }
        assert result == expected

    def test_from_api_repr_missing_columns(self):
        resource = {}
        result = self._get_target_class().from_api_repr(resource)
        assert result.columns == []

    def test_from_api_repr_with_incomplete_columns(self):
        from google.cloud.bigquery.standard_sql import StandardSqlDataType
        from google.cloud.bigquery.standard_sql import StandardSqlField

        resource = {
            "columns": [
                {"type": {"typeKind": "BOOL"}},  # missing name
                {"name": "bar"},  # missing type
            ]
        }

        result = self._get_target_class().from_api_repr(resource)

        assert len(result.columns) == 2

        expected = StandardSqlField(
            name=None,
            type=StandardSqlDataType(type_kind=bigquery.StandardSqlTypeNames.BOOL),
        )
        assert result.columns[0] == expected

        expected = StandardSqlField(
            name="bar",
            type=StandardSqlDataType(
                type_kind=bigquery.StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED
            ),
        )
        assert result.columns[1] == expected
