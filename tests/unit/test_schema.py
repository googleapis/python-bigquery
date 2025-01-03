# Copyright 2015 Google LLC
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


import copy
import unittest
from unittest import mock

import pytest

from google.cloud import bigquery
from google.cloud.bigquery.enums import RoundingMode
from google.cloud.bigquery.standard_sql import StandardSqlStructType
from google.cloud.bigquery.schema import (
    PolicyTagList,
    ForeignTypeInfo,
    StorageDescriptor,
    SerDeInfo,
    Schema,
    SchemaField,
    _parse_schema_resource,
    _build_schema_resource,
    _to_schema_fields,
)


class TestSchemaField(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.schema import SchemaField

        return SchemaField

    @staticmethod
    def _get_standard_sql_data_type_class():
        from google.cloud.bigquery import standard_sql

        return standard_sql.StandardSqlDataType

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        field = self._make_one("test", "STRING")
        self.assertEqual(field.name, "test")
        self.assertEqual(field.field_type, "STRING")
        self.assertEqual(field.mode, "NULLABLE")
        self.assertIsNone(field.description)
        self.assertEqual(field.fields, ())
        self.assertIsNone(field.policy_tags)
        self.assertIsNone(field.default_value_expression)
        self.assertEqual(field.rounding_mode, None)
        self.assertEqual(field.foreign_type_definition, None)

    def test_constructor_explicit(self):
        FIELD_DEFAULT_VALUE_EXPRESSION = "This is the default value for this field"
        ROUNDINGMODE = RoundingMode.ROUNDING_MODE_UNSPECIFIED
        field = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(
                names=(
                    "projects/a/locations/b/taxonomies/c/policyTags/e",
                    "projects/f/locations/g/taxonomies/h/policyTags/i",
                )
            ),
            default_value_expression=FIELD_DEFAULT_VALUE_EXPRESSION,
            rounding_mode=ROUNDINGMODE,
            foreign_type_definition="INTEGER",
        )
        self.assertEqual(field.name, "test")
        self.assertEqual(field.field_type, "STRING")
        self.assertEqual(field.mode, "REQUIRED")
        self.assertEqual(field.default_value_expression, FIELD_DEFAULT_VALUE_EXPRESSION)
        self.assertEqual(field.description, "Testing")
        self.assertEqual(field.fields, ())
        self.assertEqual(
            field.policy_tags,
            PolicyTagList(
                names=(
                    "projects/a/locations/b/taxonomies/c/policyTags/e",
                    "projects/f/locations/g/taxonomies/h/policyTags/i",
                )
            ),
        )
        self.assertEqual(field.rounding_mode, ROUNDINGMODE.name)
        self.assertEqual(field.foreign_type_definition, "INTEGER")

    def test_constructor_explicit_none(self):
        field = self._make_one(
            "test",
            "STRING",
            description=None,
            policy_tags=None,
        )
        self.assertIsNone(field.description)
        self.assertIsNone(field.policy_tags)

    def test_constructor_subfields(self):
        sub_field1 = self._make_one("area_code", "STRING")
        sub_field2 = self._make_one("local_number", "STRING")
        field = self._make_one(
            "phone_number", "RECORD", fields=[sub_field1, sub_field2]
        )
        self.assertEqual(field.name, "phone_number")
        self.assertEqual(field.field_type, "RECORD")
        self.assertEqual(field.mode, "NULLABLE")
        self.assertIsNone(field.description)
        self.assertEqual(len(field.fields), 2)
        self.assertEqual(field.fields[0], sub_field1)
        self.assertEqual(field.fields[1], sub_field2)

    def test_constructor_range(self):
        from google.cloud.bigquery.schema import FieldElementType

        field = self._make_one(
            "test",
            "RANGE",
            mode="REQUIRED",
            description="Testing",
            range_element_type=FieldElementType("DATETIME"),
        )
        self.assertEqual(field.name, "test")
        self.assertEqual(field.field_type, "RANGE")
        self.assertEqual(field.mode, "REQUIRED")
        self.assertEqual(field.description, "Testing")
        self.assertEqual(field.range_element_type.element_type, "DATETIME")

    def test_constructor_range_str(self):
        field = self._make_one(
            "test",
            "RANGE",
            mode="REQUIRED",
            description="Testing",
            range_element_type="DATETIME",
        )
        self.assertEqual(field.name, "test")
        self.assertEqual(field.field_type, "RANGE")
        self.assertEqual(field.mode, "REQUIRED")
        self.assertEqual(field.description, "Testing")
        self.assertEqual(field.range_element_type.element_type, "DATETIME")

    def test_to_api_repr(self):
        from google.cloud.bigquery.schema import PolicyTagList

        policy = PolicyTagList(names=("foo", "bar"))
        self.assertEqual(
            policy.to_api_repr(),
            {"names": ["foo", "bar"]},
        )
        ROUNDINGMODE = RoundingMode.ROUNDING_MODE_UNSPECIFIED

        field = self._make_one(
            "foo",
            "INTEGER",
            "NULLABLE",
            description="hello world",
            policy_tags=policy,
            rounding_mode=ROUNDINGMODE,
            foreign_type_definition=None,
        )
        self.assertEqual(
            field.to_api_repr(),
            {
                "mode": "NULLABLE",
                "name": "foo",
                "type": "INTEGER",
                "description": "hello world",
                "policyTags": {"names": ["foo", "bar"]},
                "roundingMode": "ROUNDING_MODE_UNSPECIFIED",
            },
        )

    def test_to_api_repr_omits_unset_properties(self):
        # Prevent accidentally modifying fields that aren't explicitly set.
        # https://github.com/googleapis/python-bigquery/issues/981
        field = self._make_one("foo", "INTEGER")
        resource = field.to_api_repr()
        self.assertNotIn("description", resource)
        self.assertNotIn("policyTags", resource)

    def test_to_api_repr_with_subfield(self):
        for record_type in ("RECORD", "STRUCT"):
            subfield = self._make_one("bar", "INTEGER", "NULLABLE")
            field = self._make_one("foo", record_type, "REQUIRED", fields=(subfield,))
            self.assertEqual(
                field.to_api_repr(),
                {
                    "fields": [{"mode": "NULLABLE", "name": "bar", "type": "INTEGER"}],
                    "mode": "REQUIRED",
                    "name": "foo",
                    "type": record_type,
                },
            )

    def test_from_api_repr(self):
        field = self._get_target_class().from_api_repr(
            {
                "fields": [{"mode": "nullable", "name": "bar", "type": "integer"}],
                "mode": "required",
                "description": "test_description",
                "name": "foo",
                "type": "record",
                "roundingMode": "ROUNDING_MODE_UNSPECIFIED",
            }
        )
        self.assertEqual(field.name, "foo")
        self.assertEqual(field.field_type, "RECORD")
        self.assertEqual(field.mode, "REQUIRED")
        self.assertEqual(field.description, "test_description")
        self.assertEqual(len(field.fields), 1)
        self.assertEqual(field.fields[0].name, "bar")
        self.assertEqual(field.fields[0].field_type, "INTEGER")
        self.assertEqual(field.fields[0].mode, "NULLABLE")
        self.assertEqual(field.range_element_type, None)
        self.assertEqual(field.rounding_mode, "ROUNDING_MODE_UNSPECIFIED")

    def test_from_api_repr_policy(self):
        field = self._get_target_class().from_api_repr(
            {
                "fields": [{"mode": "nullable", "name": "bar", "type": "integer"}],
                "name": "foo",
                "type": "record",
                "policyTags": {"names": ["one", "two"]},
            }
        )
        self.assertEqual(field.name, "foo")
        self.assertEqual(field.field_type, "RECORD")
        self.assertEqual(field.policy_tags.names, ("one", "two"))
        self.assertEqual(len(field.fields), 1)
        self.assertEqual(field.fields[0].name, "bar")
        self.assertEqual(field.fields[0].field_type, "INTEGER")
        self.assertEqual(field.fields[0].mode, "NULLABLE")

    def test_from_api_repr_range(self):
        field = self._get_target_class().from_api_repr(
            {
                "mode": "nullable",
                "description": "test_range",
                "name": "foo",
                "type": "range",
                "rangeElementType": {"type": "DATETIME"},
            }
        )
        self.assertEqual(field.name, "foo")
        self.assertEqual(field.field_type, "RANGE")
        self.assertEqual(field.mode, "NULLABLE")
        self.assertEqual(field.description, "test_range")
        self.assertEqual(len(field.fields), 0)
        self.assertEqual(field.range_element_type.element_type, "DATETIME")

    def test_from_api_repr_defaults(self):
        field = self._get_target_class().from_api_repr(
            {"name": "foo", "type": "record"}
        )
        self.assertEqual(field.name, "foo")
        self.assertEqual(field.field_type, "RECORD")
        self.assertEqual(field.mode, "NULLABLE")
        self.assertEqual(len(field.fields), 0)
        self.assertEqual(field.default_value_expression, None)

        # Keys not present in API representation shouldn't be included in
        # _properties.
        self.assertIsNone(field.description)
        self.assertIsNone(field.policy_tags)
        self.assertIsNone(field.range_element_type)
        self.assertNotIn("description", field._properties)
        self.assertNotIn("policyTags", field._properties)
        self.assertNotIn("rangeElementType", field._properties)

    def test_name_property(self):
        name = "lemon-ness"
        schema_field = self._make_one(name, "INTEGER")
        self.assertEqual(schema_field.name, name)

    def test_field_type_property(self):
        field_type = "BOOLEAN"
        schema_field = self._make_one("whether", field_type)
        self.assertEqual(schema_field.field_type, field_type)

    def test_mode_property(self):
        mode = "REPEATED"
        schema_field = self._make_one("again", "FLOAT", mode=mode)
        self.assertEqual(schema_field.mode, mode)

    def test_is_nullable(self):
        mode = "NULLABLE"
        schema_field = self._make_one("test", "FLOAT", mode=mode)
        self.assertTrue(schema_field.is_nullable)

    def test_is_not_nullable(self):
        mode = "REPEATED"
        schema_field = self._make_one("test", "FLOAT", mode=mode)
        self.assertFalse(schema_field.is_nullable)

    def test_description_property(self):
        description = "It holds some data."
        schema_field = self._make_one("do", "TIMESTAMP", description=description)
        self.assertEqual(schema_field.description, description)

    def test_fields_property(self):
        sub_field1 = self._make_one("one", "STRING")
        sub_field2 = self._make_one("fish", "INTEGER")
        fields = (sub_field1, sub_field2)
        schema_field = self._make_one("boat", "RECORD", fields=fields)
        self.assertEqual(schema_field.fields, fields)

    def test_roundingmode_property_str(self):
        ROUNDINGMODE = "ROUNDING_MODE_UNSPECIFIED"
        schema_field = self._make_one("test", "STRING", rounding_mode=ROUNDINGMODE)
        self.assertEqual(schema_field.rounding_mode, ROUNDINGMODE)

    def test_to_standard_sql_simple_type(self):
        examples = (
            # a few legacy types
            ("INTEGER", bigquery.StandardSqlTypeNames.INT64),
            ("FLOAT", bigquery.StandardSqlTypeNames.FLOAT64),
            ("BOOLEAN", bigquery.StandardSqlTypeNames.BOOL),
            ("DATETIME", bigquery.StandardSqlTypeNames.DATETIME),
            # a few standard types
            ("INT64", bigquery.StandardSqlTypeNames.INT64),
            ("FLOAT64", bigquery.StandardSqlTypeNames.FLOAT64),
            ("BOOL", bigquery.StandardSqlTypeNames.BOOL),
            ("GEOGRAPHY", bigquery.StandardSqlTypeNames.GEOGRAPHY),
        )
        for legacy_type, standard_type in examples:
            field = self._make_one("some_field", legacy_type)
            standard_field = field.to_standard_sql()
            self.assertEqual(standard_field.name, "some_field")
            self.assertEqual(standard_field.type.type_kind, standard_type)

    def test_to_standard_sql_struct_type(self):
        from google.cloud.bigquery import standard_sql

        sql_type = self._get_standard_sql_data_type_class()

        # level 2 fields
        sub_sub_field_date = standard_sql.StandardSqlField(
            name="date_field",
            type=sql_type(type_kind=bigquery.StandardSqlTypeNames.DATE),
        )
        sub_sub_field_time = standard_sql.StandardSqlField(
            name="time_field",
            type=sql_type(type_kind=bigquery.StandardSqlTypeNames.TIME),
        )

        # level 1 fields
        sub_field_struct = standard_sql.StandardSqlField(
            name="last_used",
            type=sql_type(
                type_kind=bigquery.StandardSqlTypeNames.STRUCT,
                struct_type=standard_sql.StandardSqlStructType(
                    fields=[sub_sub_field_date, sub_sub_field_time]
                ),
            ),
        )
        sub_field_bytes = standard_sql.StandardSqlField(
            name="image_content",
            type=sql_type(type_kind=bigquery.StandardSqlTypeNames.BYTES),
        )

        # level 0 (top level)
        expected_result = standard_sql.StandardSqlField(
            name="image_usage",
            type=sql_type(
                type_kind=bigquery.StandardSqlTypeNames.STRUCT,
                struct_type=standard_sql.StandardSqlStructType(
                    fields=[sub_field_bytes, sub_field_struct]
                ),
            ),
        )

        # construct legacy SchemaField object
        sub_sub_field1 = self._make_one("date_field", "DATE")
        sub_sub_field2 = self._make_one("time_field", "TIME")
        sub_field_record = self._make_one(
            "last_used", "RECORD", fields=(sub_sub_field1, sub_sub_field2)
        )
        sub_field_bytes = self._make_one("image_content", "BYTES")

        for type_name in ("RECORD", "STRUCT"):
            schema_field = self._make_one(
                "image_usage", type_name, fields=(sub_field_bytes, sub_field_record)
            )
            standard_field = schema_field.to_standard_sql()
            self.assertEqual(standard_field, expected_result)

    def test_to_standard_sql_array_type_simple(self):
        from google.cloud.bigquery import standard_sql

        sql_type = self._get_standard_sql_data_type_class()

        # construct expected result object
        expected_sql_type = sql_type(
            type_kind=bigquery.StandardSqlTypeNames.ARRAY,
            array_element_type=sql_type(type_kind=bigquery.StandardSqlTypeNames.INT64),
        )
        expected_result = standard_sql.StandardSqlField(
            name="valid_numbers", type=expected_sql_type
        )

        # construct "repeated" SchemaField object and convert to standard SQL
        schema_field = self._make_one("valid_numbers", "INT64", mode="REPEATED")
        standard_field = schema_field.to_standard_sql()

        self.assertEqual(standard_field, expected_result)

    def test_to_standard_sql_array_type_struct(self):
        from google.cloud.bigquery import standard_sql

        sql_type = self._get_standard_sql_data_type_class()

        # define person STRUCT
        name_field = standard_sql.StandardSqlField(
            name="name", type=sql_type(type_kind=bigquery.StandardSqlTypeNames.STRING)
        )
        age_field = standard_sql.StandardSqlField(
            name="age", type=sql_type(type_kind=bigquery.StandardSqlTypeNames.INT64)
        )
        person_struct = standard_sql.StandardSqlField(
            name="person_info",
            type=sql_type(
                type_kind=bigquery.StandardSqlTypeNames.STRUCT,
                struct_type=StandardSqlStructType(fields=[name_field, age_field]),
            ),
        )

        # define expected result - an ARRAY of person structs
        expected_sql_type = sql_type(
            type_kind=bigquery.StandardSqlTypeNames.ARRAY,
            array_element_type=person_struct.type,
        )
        expected_result = standard_sql.StandardSqlField(
            name="known_people", type=expected_sql_type
        )

        # construct legacy repeated SchemaField object
        sub_field1 = self._make_one("name", "STRING")
        sub_field2 = self._make_one("age", "INTEGER")
        schema_field = self._make_one(
            "known_people", "RECORD", fields=(sub_field1, sub_field2), mode="REPEATED"
        )

        standard_field = schema_field.to_standard_sql()
        self.assertEqual(standard_field, expected_result)

    def test_to_standard_sql_unknown_type(self):
        field = self._make_one("weird_field", "TROOLEAN")

        standard_field = field.to_standard_sql()

        self.assertEqual(standard_field.name, "weird_field")
        self.assertEqual(
            standard_field.type.type_kind,
            bigquery.StandardSqlTypeNames.TYPE_KIND_UNSPECIFIED,
        )

    def test_to_standard_sql_foreign_type_valid(self):
        legacy_type = "FOREIGN"
        standard_type = bigquery.StandardSqlTypeNames.FOREIGN
        foreign_type_definition = "INTEGER"

        field = self._make_one(
            "some_field",
            field_type=legacy_type,
            foreign_type_definition=foreign_type_definition,
        )
        standard_field = field.to_standard_sql()
        self.assertEqual(standard_field.name, "some_field")
        self.assertEqual(standard_field.type.type_kind, standard_type)

    def test_to_standard_sql_foreign_type_invalid(self):
        legacy_type = "FOREIGN"
        foreign_type_definition = None

        with self.assertRaises(ValueError) as context:
            self._make_one(
                "some_field",
                field_type=legacy_type,
                foreign_type_definition=foreign_type_definition,
            )
        self.assertTrue("If the 'field_type'" in context.exception.args[0])

    def test___eq___wrong_type(self):
        field = self._make_one("test", "STRING")
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___eq___name_mismatch(self):
        field = self._make_one("test", "STRING")
        other = self._make_one("other", "STRING")
        self.assertNotEqual(field, other)

    def test___eq___field_type_mismatch(self):
        field = self._make_one("test", "STRING")
        other = self._make_one("test", "INTEGER")
        self.assertNotEqual(field, other)

    def test___eq___mode_mismatch(self):
        field = self._make_one("test", "STRING", mode="REQUIRED")
        other = self._make_one("test", "STRING", mode="NULLABLE")
        self.assertNotEqual(field, other)

    def test___eq___description_mismatch(self):
        field = self._make_one("test", "STRING", description="Testing")
        other = self._make_one("test", "STRING", description="Other")
        self.assertNotEqual(field, other)

    def test___eq___fields_mismatch(self):
        sub1 = self._make_one("sub1", "STRING")
        sub2 = self._make_one("sub2", "STRING")
        field = self._make_one("test", "RECORD", fields=[sub1])
        other = self._make_one("test", "RECORD", fields=[sub2])
        self.assertNotEqual(field, other)

    def test___eq___hit(self):
        field = self._make_one("test", "STRING", mode="REQUIRED", description="Testing")
        other = self._make_one("test", "STRING", mode="REQUIRED", description="Testing")
        self.assertEqual(field, other)

    def test___eq___hit_case_diff_on_type(self):
        field = self._make_one("test", "STRING", mode="REQUIRED", description="Testing")
        other = self._make_one("test", "string", mode="REQUIRED", description="Testing")
        self.assertEqual(field, other)

    def test___eq___hit_w_fields(self):
        sub1 = self._make_one("sub1", "STRING")
        sub2 = self._make_one("sub2", "STRING")
        field = self._make_one("test", "RECORD", fields=[sub1, sub2])
        other = self._make_one("test", "RECORD", fields=[sub1, sub2])
        self.assertEqual(field, other)

    def test___eq___hit_w_policy_tags(self):
        field = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(names=["foo", "bar"]),
        )
        other = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(names=["bar", "foo"]),
        )
        self.assertEqual(field, other)  # Policy tags order does not matter.

    def test___ne___wrong_type(self):
        field = self._make_one("toast", "INTEGER")
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___ne___same_value(self):
        field1 = self._make_one("test", "TIMESTAMP", mode="REPEATED")
        field2 = self._make_one("test", "TIMESTAMP", mode="REPEATED")
        # unittest ``assertEqual`` uses ``==`` not ``!=``.
        comparison_val = field1 != field2
        self.assertFalse(comparison_val)

    def test___ne___different_values(self):
        field1 = self._make_one(
            "test1", "FLOAT", mode="REPEATED", description="Not same"
        )
        field2 = self._make_one(
            "test2", "FLOAT", mode="NULLABLE", description="Knot saym"
        )
        self.assertNotEqual(field1, field2)

    def test___ne___different_policy_tags(self):
        field = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(names=["foo", "bar"]),
        )
        other = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(names=["foo", "baz"]),
        )
        self.assertNotEqual(field, other)

    def test___hash__set_equality(self):
        sub1 = self._make_one("sub1", "STRING")
        sub2 = self._make_one("sub2", "STRING")
        field1 = self._make_one("test", "RECORD", fields=[sub1])
        field2 = self._make_one("test", "RECORD", fields=[sub2])
        set_one = {field1, field2}
        set_two = {field1, field2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        sub1 = self._make_one("sub1", "STRING")
        sub2 = self._make_one("sub2", "STRING")
        field1 = self._make_one("test", "RECORD", fields=[sub1])
        field2 = self._make_one("test", "RECORD", fields=[sub2])
        set_one = {field1}
        set_two = {field2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__(self):
        field1 = self._make_one("field1", "STRING")
        expected = "SchemaField('field1', 'STRING', 'NULLABLE', None, None, (), None)"
        self.assertEqual(repr(field1), expected)

    def test___repr__type_not_set(self):
        field1 = self._make_one("field1", field_type=None)
        expected = "SchemaField('field1', None, 'NULLABLE', None, None, (), None)"
        self.assertEqual(repr(field1), expected)

    def test___repr__evaluable_no_policy_tags(self):
        field = self._make_one("field1", "STRING", "REQUIRED", "Description")
        field_repr = repr(field)
        SchemaField = self._get_target_class()  # needed for eval  # noqa

        evaled_field = eval(field_repr)

        assert field == evaled_field

    def test___repr__evaluable_with_policy_tags(self):
        policy_tags = PolicyTagList(names=["foo", "bar"])
        field = self._make_one(
            "field1",
            "STRING",
            "REQUIRED",
            "Description",
            policy_tags=policy_tags,
        )
        field_repr = repr(field)
        SchemaField = self._get_target_class()  # needed for eval  # noqa

        evaled_field = eval(field_repr)

        assert field == evaled_field


class TestFieldElementType(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.schema import FieldElementType

        return FieldElementType

    def _make_one(self, *args):
        return self._get_target_class()(*args)

    def test_constructor(self):
        element_type = self._make_one("DATETIME")
        self.assertEqual(element_type.element_type, "DATETIME")
        self.assertEqual(element_type._properties["type"], "DATETIME")

    def test_to_api_repr(self):
        element_type = self._make_one("DATETIME")
        self.assertEqual(element_type.to_api_repr(), {"type": "DATETIME"})

    def test_from_api_repr(self):
        api_repr = {"type": "DATETIME"}
        expected_element_type = self._make_one("DATETIME")
        self.assertEqual(
            expected_element_type.element_type,
            self._get_target_class().from_api_repr(api_repr).element_type,
        )

    def test_from_api_repr_empty(self):
        self.assertEqual(None, self._get_target_class().from_api_repr({}))

    def test_from_api_repr_none(self):
        self.assertEqual(None, self._get_target_class().from_api_repr(None))


@pytest.fixture
def basic_resource():
    return {
        "schema": {
            "fields": [
                {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                {"name": "age", "type": "INTEGER", "mode": "REQUIRED"},
            ]
        }
    }


@pytest.fixture
def resource_with_subfields(basic_resource):
    basic_resource["schema"]["fields"].append(
        {
            "name": "phone",
            "type": "RECORD",
            "mode": "REPEATED",
            "fields": [
                {"name": "type", "type": "STRING", "mode": "REQUIRED"},
                {"name": "number", "type": "STRING", "mode": "REQUIRED"},
            ],
        }
    )
    return basic_resource


@pytest.fixture
def resource_without_mode(basic_resource):
    basic_resource["schema"]["fields"].append({"name": "phone", "type": "STRING"})
    return basic_resource


class TestParseSchemaResource:
    def verify_field(self, field, r_field):
        assert field.name == r_field["name"]
        assert field.field_type == r_field["type"]
        assert field.mode == r_field.get("mode", "NULLABLE")

    def verify_schema(self, schema, resource):
        r_fields = resource["schema"]["fields"]
        assert len(schema) == len(r_fields)

        for field, r_field in zip(schema, r_fields):
            self.verify_field(field, r_field)

    # Tests focused on exercising the parse_schema_resource() method
    def test_parse_schema_resource_defaults(self, basic_resource):
        schema = _parse_schema_resource(basic_resource["schema"])
        self.verify_schema(schema, basic_resource)

    def test_parse_schema_resource_subfields(self, resource_with_subfields):
        schema = _parse_schema_resource(resource_with_subfields["schema"])
        self.verify_schema(schema, resource_with_subfields)

    def test_parse_schema_resource_fields_without_mode(self, resource_without_mode):
        schema = _parse_schema_resource(resource_without_mode["schema"])
        self.verify_schema(schema, resource_without_mode)


class TestBuildSchemaResource:
    # Tests focused on exercising the build_schema_resource() method
    @pytest.mark.parametrize(
        "fields, expected_resource",
        [
            pytest.param(  # Test case 1: Basic fields
                [
                    SchemaField("full_name", "STRING", mode="REQUIRED"),
                    SchemaField("age", "INTEGER", mode="REQUIRED"),
                ],
                [
                    {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "age", "type": "INTEGER", "mode": "REQUIRED"},
                ],
                id="basic fields",
            ),
            pytest.param(  # Test case 2: Field without mode
                [SchemaField("phone", "STRING")],
                [{"name": "phone", "type": "STRING", "mode": "NULLABLE"}],
                id="field without mode yields NULLABLE mode",
            ),
            pytest.param(  # Test case 3: Field with description
                [
                    SchemaField(
                        "full_name",
                        "STRING",
                        mode="REQUIRED",
                        description="DESCRIPTION",
                    ),
                    SchemaField("age", "INTEGER", mode="REQUIRED", description=None),
                ],
                [
                    {
                        "name": "full_name",
                        "type": "STRING",
                        "mode": "REQUIRED",
                        "description": "DESCRIPTION",
                    },
                    {
                        "name": "age",
                        "type": "INTEGER",
                        "mode": "REQUIRED",
                        "description": None,
                    },
                ],
                id="fields including description",
            ),
            pytest.param(  # Test case 4: Field with subfields
                [
                    SchemaField("full_name", "STRING", mode="REQUIRED"),
                    SchemaField(
                        "phone",
                        "RECORD",
                        mode="REPEATED",
                        fields=[
                            SchemaField("type", "STRING", "REQUIRED"),
                            SchemaField("number", "STRING", "REQUIRED"),
                        ],
                    ),
                ],
                [
                    {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                    {
                        "name": "phone",
                        "type": "RECORD",
                        "mode": "REPEATED",
                        "fields": [
                            {"name": "type", "type": "STRING", "mode": "REQUIRED"},
                            {"name": "number", "type": "STRING", "mode": "REQUIRED"},
                        ],
                    },
                ],
                id="field with subfields",
            ),
        ],
    )
    def test_build_schema_resource(self, fields, expected_resource):
        resource = _build_schema_resource(fields)
        assert resource == expected_resource


class TestToSchemaFields:  # Test class for _to_schema_fields
    @staticmethod
    def _call_fut(schema):
        from google.cloud.bigquery.schema import _to_schema_fields

        return _to_schema_fields(schema)

    def test_invalid_type(self):
        """Invalid list of tuples instead of list of mappings"""
        schema = [
            ("full_name", "STRING", "REQUIRED"),
            ("address", "STRING", "REQUIRED"),
        ]
        with pytest.raises(ValueError):
            _to_schema_fields(schema)

    def test_schema_fields_sequence(self):
        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField(
                "age", "INT64", mode="NULLABLE"
            ),  # Using correct type name INT64
        ]
        result = _to_schema_fields(schema)
        assert result == schema

    def test_unknown_properties(self):
        schema = [
            {
                "name": "full_name",
                "type": "STRING",
                "mode": "REQUIRED",
                "someNewProperty": "test-value",
            },
            {
                "name": "age",
                # Note: This type should be included, too. Avoid client-side
                # validation, as it could prevent backwards-compatible
                # evolution of the server-side behavior.
                "typo": "INTEGER",
                "mode": "REQUIRED",
                "anotherNewProperty": "another-test",
            },
        ]

        # Make sure the setter doesn't mutate schema.
        expected_schema = copy.deepcopy(schema)

        result = self._call_fut(schema)

        for api_repr, field in zip(expected_schema, result):
            assert field.to_api_repr() == api_repr

    @pytest.mark.parametrize(
        "schema, expected_schema",
        [
            pytest.param(
                [
                    {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                    {
                        "name": "residence",
                        "type": "STRUCT",  # Or RECORD, depending on usage
                        "mode": "NULLABLE",
                        "fields": [
                            {"name": "foo", "type": "DATE", "mode": "NULLABLE"},
                            {"name": "bar", "type": "BYTES", "mode": "REQUIRED"},
                        ],
                    },
                ],
                [
                    SchemaField("full_name", "STRING", mode="REQUIRED"),
                    SchemaField(
                        "residence",
                        "STRUCT",  # Or RECORD
                        mode="NULLABLE",
                        fields=[
                            SchemaField("foo", "DATE", mode="NULLABLE"),
                            SchemaField("bar", "BYTES", mode="REQUIRED"),
                        ],
                    ),
                ],
                id="valid mapping representation",
            )
        ],
    )
    def test_valid_mapping_representation(self, schema, expected_schema):
        result = _to_schema_fields(schema)
        assert result == expected_schema

    def test_valid_schema_object(self):
        schema = Schema(
            fields=[SchemaField("name", "STRING", description=None, policy_tags=None)],
            foreign_type_info="TestInfo",
        )
        result = _to_schema_fields(schema)
        expected = Schema(
            [SchemaField("name", "STRING", "NULLABLE", None, None, (), None)],
            "TestInfo",
        )
        assert result.to_api_repr() == expected.to_api_repr()


class TestSchemaObject:  # New test class for Schema object interactions
    def test_schema_object_field_access(self):
        schema = Schema(
            fields=[
                SchemaField("name", "STRING"),
                SchemaField("age", "INTEGER"),
            ]
        )

        assert len(schema) == 2
        assert schema[0]["name"] == "name"  # Access fields using indexing
        assert schema[1]["type"] == "INTEGER"

    def test_schema_object_foreign_type_info(self):
        schema = Schema(foreign_type_info="External")
        assert schema.foreign_type_info == "External"

        schema.foreign_type_info = None
        assert schema.foreign_type_info is None

        with pytest.raises(TypeError):
            schema.foreign_type_info = 123  # Type check

    def test_str(self):
        schema = Schema(
            fields=[SchemaField("name", "STRING")],
            foreign_type_info="TestInfo",
        )
        assert (
            str(schema)
            == "Schema([{'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'}], TestInfo)"
        )

    @pytest.mark.parametrize(
        "schema, expected_repr",
        [
            pytest.param(
                Schema(
                    fields=[SchemaField("name", "STRING")],
                    foreign_type_info="TestInfo",
                ),
                "Schema([{'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'}], 'TestInfo')",
                id="repr with foreign type info",
            ),
            pytest.param(
                Schema(fields=[SchemaField("name", "STRING")]),
                "Schema([{'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'}], None)",
                id="repr without foreign type info",
            ),
        ],
    )
    def test_repr(self, schema, expected_repr):
        assert repr(schema) == expected_repr  # Test __repr__

    def test_schema_iteration(self):
        schema = Schema(
            fields=[SchemaField("name", "STRING"), SchemaField("age", "INTEGER")]
        )
        field_names = [field["name"] for field in schema]
        assert field_names == ["name", "age"]

    def test_schema_object_mutability(self):  # Tests __setitem__ and __delitem__
        schema = Schema(
            fields=[SchemaField("name", "STRING"), SchemaField("age", "INTEGER")]
        )

        schema[0] = SchemaField(
            "updated_name", "STRING"
        )  # Modify a field using setitem
        assert schema[0].name == "updated_name"

        del schema[1]  # Test __delitem__
        assert len(schema) == 1
        assert schema[0].name == "updated_name"

    def test_schema_append(self):
        schema = Schema()  # create an empty schema object
        schema.append(
            SchemaField("name", "STRING")
        )  # use the append method to add a schema field
        assert len(schema) == 1
        assert schema[0].name == "name"

    def test_schema_extend(self):
        schema = Schema()  # create an empty schema object
        schema.extend(
            [SchemaField("name", "STRING"), SchemaField("age", "INTEGER")]
        )  # use the extend method to add multiple schema fields
        assert len(schema) == 2
        assert schema[0].name == "name"
        assert schema[1].name == "age"

    @pytest.mark.parametrize(
        "schema, expected_api_repr",
        [
            pytest.param(
                Schema(
                    fields=[SchemaField("name", "STRING")],
                    foreign_type_info="TestInfo",
                ),
                {
                    "fields": [{"name": "name", "mode": "NULLABLE", "type": "STRING"}],
                    "foreignTypeInfo": "TestInfo",
                },
                id="repr with foreign type info",
            ),
            pytest.param(
                Schema(fields=[SchemaField("name", "STRING")]),
                {
                    "fields": [{"name": "name", "mode": "NULLABLE", "type": "STRING"}],
                    "foreignTypeInfo": None,
                },
                id="repr without foreign type info",
            ),
        ],
    )
    def test_to_api_repr(self, schema, expected_api_repr):
        assert schema.to_api_repr() == expected_api_repr

    @pytest.mark.parametrize(
        "api_repr, expected",
        [
            pytest.param(
                {
                    "fields": [
                        SchemaField("name", "STRING", "NULLABLE", None, None, (), None)
                    ],
                    "foreignTypeInfo": "TestInfo",
                },
                Schema(
                    fields=[
                        SchemaField(
                            "name", "STRING", description=None, policy_tags=None
                        )
                    ],
                    foreign_type_info="TestInfo",
                ),
                id="repr with foreign type info",
            ),
            pytest.param(
                {
                    "fields": [
                        SchemaField("name", "STRING", "NULLABLE", None, None, (), None)
                    ],
                    "foreignTypeInfo": None,
                },
                Schema(
                    fields=[
                        SchemaField(
                            "name", "STRING", description=None, policy_tags=None
                        )
                    ]
                ),
                id="repr without foreign type info",
            ),
        ],
    )
    def test_from_api_repr(self, api_repr, expected):
        """GIVEN an api representation of a Schema object (i.e. resource)
        WHEN converted into a Schema object using from_api_repr() and
        displayed as a dict
        THEN it will have the same representation a Schema object created
        directly and displayed as a dict.
        """

        result = Schema.from_api_repr(api_repr)
        assert result.to_api_repr() == expected.to_api_repr()


class TestPolicyTags(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.schema import PolicyTagList

        return PolicyTagList

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        empty_policy_tags = self._make_one()
        self.assertIsNotNone(empty_policy_tags.names)
        self.assertEqual(len(empty_policy_tags.names), 0)
        policy_tags = self._make_one(["foo", "bar"])
        self.assertEqual(policy_tags.names, ("foo", "bar"))

    def test_from_api_repr(self):
        klass = self._get_target_class()
        api_repr = {"names": ["foo"]}
        policy_tags = klass.from_api_repr(api_repr)
        self.assertEqual(policy_tags.to_api_repr(), api_repr)

        # Ensure the None case correctly returns None, rather
        # than an empty instance.
        policy_tags2 = klass.from_api_repr(None)
        self.assertIsNone(policy_tags2)

    def test_to_api_repr(self):
        taglist = self._make_one(names=["foo", "bar"])
        self.assertEqual(
            taglist.to_api_repr(),
            {"names": ["foo", "bar"]},
        )
        taglist2 = self._make_one(names=("foo", "bar"))
        self.assertEqual(
            taglist2.to_api_repr(),
            {"names": ["foo", "bar"]},
        )

    def test___eq___wrong_type(self):
        policy = self._make_one(names=["foo"])
        other = object()
        self.assertNotEqual(policy, other)
        self.assertEqual(policy, mock.ANY)

    def test___eq___names_mismatch(self):
        policy = self._make_one(names=["foo", "bar"])
        other = self._make_one(names=["bar", "baz"])
        self.assertNotEqual(policy, other)

    def test___hash__set_equality(self):
        policy1 = self._make_one(["foo", "bar"])
        policy2 = self._make_one(["bar", "baz"])
        set_one = {policy1, policy2}
        set_two = {policy1, policy2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        policy1 = self._make_one(["foo", "bar"])
        policy2 = self._make_one(["bar", "baz"])
        set_one = {policy1}
        set_two = {policy2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__no_tags(self):
        policy = self._make_one()
        assert repr(policy) == "PolicyTagList(names=())"

    def test___repr__with_tags(self):
        policy1 = self._make_one(["foo", "bar", "baz"])
        policy2 = self._make_one(["baz", "bar", "foo"])
        expected_repr = "PolicyTagList(names=('bar', 'baz', 'foo'))"  # alphabetical

        assert repr(policy1) == expected_repr
        assert repr(policy2) == expected_repr

    def test___repr__evaluable_no_tags(self):
        policy = self._make_one(names=[])
        policy_repr = repr(policy)

        evaled_policy = eval(policy_repr)

        assert policy == evaled_policy

    def test___repr__evaluable_with_tags(self):
        policy = self._make_one(names=["foo", "bar"])
        policy_repr = repr(policy)

        evaled_policy = eval(policy_repr)

        assert policy == evaled_policy


@pytest.mark.parametrize(
    "api,expect,key2",
    [
        (
            dict(name="n", type="NUMERIC"),
            ("n", "NUMERIC", None, None, None),
            ("n", "NUMERIC"),
        ),
        (
            dict(name="n", type="NUMERIC", precision=9),
            ("n", "NUMERIC", 9, None, None),
            ("n", "NUMERIC(9)"),
        ),
        (
            dict(name="n", type="NUMERIC", precision=9, scale=2),
            ("n", "NUMERIC", 9, 2, None),
            ("n", "NUMERIC(9, 2)"),
        ),
        (
            dict(name="n", type="BIGNUMERIC"),
            ("n", "BIGNUMERIC", None, None, None),
            ("n", "BIGNUMERIC"),
        ),
        (
            dict(name="n", type="BIGNUMERIC", precision=40),
            ("n", "BIGNUMERIC", 40, None, None),
            ("n", "BIGNUMERIC(40)"),
        ),
        (
            dict(name="n", type="BIGNUMERIC", precision=40, scale=2),
            ("n", "BIGNUMERIC", 40, 2, None),
            ("n", "BIGNUMERIC(40, 2)"),
        ),
        (
            dict(name="n", type="STRING"),
            ("n", "STRING", None, None, None),
            ("n", "STRING"),
        ),
        (
            dict(name="n", type="STRING", maxLength=9),
            ("n", "STRING", None, None, 9),
            ("n", "STRING(9)"),
        ),
        (
            dict(name="n", type="BYTES"),
            ("n", "BYTES", None, None, None),
            ("n", "BYTES"),
        ),
        (
            dict(name="n", type="BYTES", maxLength=9),
            ("n", "BYTES", None, None, 9),
            ("n", "BYTES(9)"),
        ),
    ],
)
def test_from_api_repr_parameterized(api, expect, key2):
    from google.cloud.bigquery.schema import SchemaField

    field = SchemaField.from_api_repr(api)

    assert (
        field.name,
        field.field_type,
        field.precision,
        field.scale,
        field.max_length,
    ) == expect

    assert field._key()[:2] == key2


@pytest.mark.parametrize(
    "field,api",
    [
        (
            dict(name="n", field_type="NUMERIC"),
            dict(name="n", type="NUMERIC", mode="NULLABLE"),
        ),
        (
            dict(name="n", field_type="NUMERIC", precision=9),
            dict(
                name="n",
                type="NUMERIC",
                mode="NULLABLE",
                precision=9,
            ),
        ),
        (
            dict(name="n", field_type="NUMERIC", precision=9, scale=2),
            dict(
                name="n",
                type="NUMERIC",
                mode="NULLABLE",
                precision=9,
                scale=2,
            ),
        ),
        (
            dict(name="n", field_type="BIGNUMERIC"),
            dict(name="n", type="BIGNUMERIC", mode="NULLABLE"),
        ),
        (
            dict(name="n", field_type="BIGNUMERIC", precision=40),
            dict(
                name="n",
                type="BIGNUMERIC",
                mode="NULLABLE",
                precision=40,
            ),
        ),
        (
            dict(name="n", field_type="BIGNUMERIC", precision=40, scale=2),
            dict(
                name="n",
                type="BIGNUMERIC",
                mode="NULLABLE",
                precision=40,
                scale=2,
            ),
        ),
        (
            dict(name="n", field_type="STRING"),
            dict(name="n", type="STRING", mode="NULLABLE"),
        ),
        (
            dict(name="n", field_type="STRING", max_length=9),
            dict(
                name="n",
                type="STRING",
                mode="NULLABLE",
                maxLength=9,
            ),
        ),
        (
            dict(name="n", field_type="BYTES"),
            dict(name="n", type="BYTES", mode="NULLABLE"),
        ),
        (
            dict(name="n", field_type="BYTES", max_length=9),
            dict(
                name="n",
                type="BYTES",
                mode="NULLABLE",
                maxLength=9,
            ),
        ),
    ],
)
def test_to_api_repr_parameterized(field, api):
    from google.cloud.bigquery.schema import SchemaField

    assert SchemaField(**field).to_api_repr() == api


class TestForeignTypeInfo:
    """Tests metadata re: the foreign data type definition in field schema.

    Specifies the system which defines the foreign data type.

    TypeSystems are external systems, such as query engines or table formats,
    that have their own data types.

    TypeSystem may be:
        TypeSystem not specified: TYPE_SYSTEM_UNSPECIFIED
        Represents Hive data types: HIVE
    """

    @staticmethod
    def _get_target_class():
        return ForeignTypeInfo

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    @pytest.mark.parametrize(
        "type_system,expected",
        [
            (None, None),
            ("TYPE_SYSTEM_UNSPECIFIED", "TYPE_SYSTEM_UNSPECIFIED"),
            ("HIVE", "HIVE"),
        ],
    )
    def test_ctor_valid_input(self, type_system, expected):
        result = self._make_one(type_system=type_system)

        assert result.type_system == expected

    def test_ctor_invalid_input(self):
        with pytest.raises(TypeError) as e:
            self._make_one(type_system=123)

        # Looking for the first word from the string "Pass <variable> as..."
        assert "Pass " in str(e.value)

    @pytest.mark.parametrize(
        "type_system,expected",
        [
            ("TYPE_SYSTEM_UNSPECIFIED", {"typeSystem": "TYPE_SYSTEM_UNSPECIFIED"}),
            ("HIVE", {"typeSystem": "HIVE"}),
            (None, {"typeSystem": None}),
        ],
    )
    def test_to_api_repr(self, type_system, expected):
        result = self._make_one(type_system=type_system)
        assert result.to_api_repr() == expected

    def test_from_api_repr(self):
        """GIVEN an api representation of a ForeignTypeInfo object (i.e. resource)
        WHEN converted into a ForeignTypeInfo object using from_api_repr() and
        displayed as a dict
        THEN it will have the same representation a ForeignTypeInfo object created
        directly (via _make_one()) and displayed as a dict.
        """
        resource = {"typeSystem": "TYPE_SYSTEM_UNSPECIFIED"}

        expected = self._make_one(type_system="TYPE_SYSTEM_UNSPECIFIED")

        klass = self._get_target_class()
        result = klass.from_api_repr(resource)

        assert result.to_api_repr() == expected.to_api_repr()


@pytest.fixture
def _make_storage_descriptor():
    serdeinfo = SerDeInfo(
        serialization_library="testpath.to.LazySimpleSerDe",
        name="serde_lib_name",
        parameters={"key": "value"},
    )

    obj = StorageDescriptor(
        input_format="testpath.to.OrcInputFormat",
        location_uri="gs://test/path/",
        output_format="testpath.to.OrcOutputFormat",
        serde_info=serdeinfo,
    )
    return obj


class TestStorageDescriptor:
    """Tests for the StorageDescriptor class."""

    @staticmethod
    def _get_target_class():
        return StorageDescriptor

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    SERDEINFO = SerDeInfo(
        serialization_library="testpath.to.LazySimpleSerDe",
        name="serde_lib_name",
        parameters={"key": "value"},
    )

    @pytest.mark.parametrize(
        "input_format,location_uri,output_format,serde_info",
        [
            (None, None, None, None),
            ("testpath.to.OrcInputFormat", None, None, None),
            (None, "gs://test/path/", None, None),
            (None, None, "testpath.to.OrcOutputFormat", None),
            (None, None, None, SERDEINFO),
            (
                "testpath.to.OrcInputFormat",
                "gs://test/path/",
                "testpath.to.OrcOutputFormat",
                SERDEINFO,
            ),
        ],
    )
    def test_ctor_valid_input(
        self, input_format, location_uri, output_format, serde_info
    ):
        storage_descriptor = self._make_one(
            input_format=input_format,
            location_uri=location_uri,
            output_format=output_format,
            serde_info=serde_info,
        )
        assert storage_descriptor.input_format == input_format
        assert storage_descriptor.location_uri == location_uri
        assert storage_descriptor.output_format == output_format
        if serde_info is not None:
            assert (
                storage_descriptor.serde_info.to_api_repr() == serde_info.to_api_repr()
            )
        else:
            assert storage_descriptor.serde_info is None

    @pytest.mark.parametrize(
        "input_format,location_uri,output_format,serde_info",
        [
            (123, None, None, None),
            (None, 123, None, None),
            (None, None, 123, None),
            (None, None, None, 123),
        ],
    )
    def test_ctor_invalid_input(
        self, input_format, location_uri, output_format, serde_info
    ):
        with pytest.raises(TypeError) as e:
            self._make_one(
                input_format=input_format,
                location_uri=location_uri,
                output_format=output_format,
                serde_info=serde_info,
            )

        # Looking for the first word from the string "Pass <variable> as..."
        assert "Pass " in str(e.value)

    def test_to_api_repr(self):
        storage_descriptor = self._make_one(
            input_format="input_format",
            location_uri="location_uri",
            output_format="output_format",
            serde_info=self.SERDEINFO,
        )
        expected_repr = {
            "inputFormat": "input_format",
            "locationUri": "location_uri",
            "outputFormat": "output_format",
            "serDeInfo": self.SERDEINFO.to_api_repr(),
        }

        assert storage_descriptor.to_api_repr() == expected_repr

    SERDEINFO = SerDeInfo(
        serialization_library="testpath.to.LazySimpleSerDe",
        name="serde_lib_name",
        parameters={"key": "value"},
    )

    API_REPR = {
        "inputFormat": "testpath.to.OrcInputFormat",
        "locationUri": "gs://test/path/",
        "outputFormat": "testpath.to.OrcOutputFormat",
        "serDeInfo": SERDEINFO.to_api_repr(),
    }

    def test_from_api_repr(self, _make_storage_descriptor):
        """GIVEN an api representation of a StorageDescriptor (i.e. API_REPR)
        WHEN converted into a StorageDescriptor using from_api_repr() and
        displayed as a dict
        THEN it will have the same representation a StorageDescriptor created
        directly (via the fixture) and displayed as a dict.
        """
        # generate via fixture
        expected = _make_storage_descriptor
        resource = self.API_REPR
        klass = self._get_target_class()
        # generate via API_REPR
        result = klass.from_api_repr(resource)

        assert result.to_api_repr() == expected.to_api_repr()


class TestSerDeInfo:
    """Tests for the SerDeInfo class."""

    @staticmethod
    def _get_target_class():
        return SerDeInfo

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @pytest.mark.parametrize(
        "serialization_library,name,parameters",
        [
            ("testpath.to.LazySimpleSerDe", None, None),
            ("testpath.to.LazySimpleSerDe", "serde_name", None),
            ("testpath.to.LazySimpleSerDe", None, {"key": "value"}),
            ("testpath.to.LazySimpleSerDe", "serde_name", {"key": "value"}),
        ],
    )
    def test_ctor_valid_input(self, serialization_library, name, parameters):
        serde_info = self._make_one(
            serialization_library=serialization_library,
            name=name,
            parameters=parameters,
        )
        assert serde_info.serialization_library == serialization_library
        assert serde_info.name == name
        assert serde_info.parameters == parameters

    @pytest.mark.parametrize(
        "serialization_library,name,parameters",
        [
            (123, None, None),
            ("testpath.to.LazySimpleSerDe", 123, None),
            ("testpath.to.LazySimpleSerDe", None, ["test", "list"]),
            ("testpath.to.LazySimpleSerDe", None, 123),
        ],
    )
    def test_ctor_invalid_input(self, serialization_library, name, parameters):
        with pytest.raises(TypeError) as e:
            self._make_one(
                serialization_library=serialization_library,
                name=name,
                parameters=parameters,
            )
        # Looking for the first word from the string "Pass <variable> as..."
        assert "Pass " in str(e.value)

    def test_to_api_repr(self):
        serde_info = self._make_one(
            serialization_library="testpath.to.LazySimpleSerDe",
            name="serde_name",
            parameters={"key": "value"},
        )
        expected_repr = {
            "serializationLibrary": "testpath.to.LazySimpleSerDe",
            "name": "serde_name",
            "parameters": {"key": "value"},
        }
        assert serde_info.to_api_repr() == expected_repr

    def test_from_api_repr(self, _make_storage_descriptor):
        """GIVEN an api representation of a SerDeInfo object (i.e. resource)
        WHEN converted into a SerDeInfo using from_api_repr() and
        displayed as a dict
        THEN it will have the same representation a SerDeInfo object created
        directly (via _make_one()) and displayed as a dict.
        """
        resource = {
            "serializationLibrary": "testpath.to.LazySimpleSerDe",
            "name": "serde_name",
            "parameters": {"key": "value"},
        }

        expected = self._make_one(
            serialization_library="testpath.to.LazySimpleSerDe",
            name="serde_name",
            parameters={"key": "value"},
        )

        klass = self._get_target_class()
        result = klass.from_api_repr(resource)

        assert result.to_api_repr() == expected.to_api_repr()
