# Copyright 2017 Google LLC
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

import base64
import copy
import unittest

from google.cloud.bigquery import external_config
from google.cloud.bigquery import schema


class TestExternalConfig(unittest.TestCase):

    SOURCE_URIS = ["gs://foo", "gs://bar"]

    BASE_RESOURCE = {
        "sourceFormat": "",
        "sourceUris": SOURCE_URIS,
        "maxBadRecords": 17,
        "autodetect": True,
        "ignoreUnknownValues": False,
        "compression": "compression",
    }

    def test_from_api_repr_base(self):
        resource = copy.deepcopy(self.BASE_RESOURCE)
        ec = external_config.ExternalConfig.from_api_repr(resource)
        self._verify_base(ec)
        self.assertEqual(ec.schema, [])
        self.assertIsNone(ec.options)

        got_resource = ec.to_api_repr()
        self.assertEqual(got_resource, self.BASE_RESOURCE)

        resource = _copy_and_update(
            self.BASE_RESOURCE,
            {
                "schema": {
                    "fields": [
                        {
                            "name": "full_name",
                            "type": "STRING",
                            "mode": "REQUIRED",
                            "description": None,
                        }
                    ]
                }
            },
        )
        ec = external_config.ExternalConfig.from_api_repr(resource)
        self._verify_base(ec)
        exp_schema = [schema.SchemaField("full_name", "STRING", mode="REQUIRED")]
        self.assertEqual(ec.schema, exp_schema)
        self.assertIsNone(ec.options)

        got_resource = ec.to_api_repr()
        self.assertEqual(got_resource, resource)

    def test_to_api_repr_base(self):
        ec = external_config.ExternalConfig("")
        ec.source_uris = self.SOURCE_URIS
        ec.max_bad_records = 17
        ec.autodetect = True
        ec.ignore_unknown_values = False
        ec.compression = "compression"
        ec.connection_id = "path/to/connection"
        ec.schema = [schema.SchemaField("full_name", "STRING", mode="REQUIRED")]

        exp_schema = {
            "fields": [{"name": "full_name", "type": "STRING", "mode": "REQUIRED"}]
        }
        got_resource = ec.to_api_repr()
        exp_resource = {
            "sourceFormat": "",
            "sourceUris": self.SOURCE_URIS,
            "maxBadRecords": 17,
            "autodetect": True,
            "ignoreUnknownValues": False,
            "compression": "compression",
            "connectionId": "path/to/connection",
            "schema": exp_schema,
        }
        self.assertEqual(got_resource, exp_resource)

    def test_connection_id(self):
        ec = external_config.ExternalConfig("")
        self.assertIsNone(ec.connection_id)
        ec.connection_id = "path/to/connection"
        self.assertEqual(ec.connection_id, "path/to/connection")

    def test_schema_None(self):
        ec = external_config.ExternalConfig("")
        ec.schema = None
        got = ec.to_api_repr()
        want = {"sourceFormat": "", "schema": None}
        self.assertEqual(got, want)

    def test_schema_empty(self):
        ec = external_config.ExternalConfig("")
        ec.schema = []
        got = ec.to_api_repr()
        want = {"sourceFormat": "", "schema": {"fields": []}}
        self.assertEqual(got, want)

    def _verify_base(self, ec):
        self.assertEqual(ec.autodetect, True)
        self.assertEqual(ec.compression, "compression")
        self.assertEqual(ec.ignore_unknown_values, False)
        self.assertEqual(ec.max_bad_records, 17)
        self.assertEqual(ec.source_uris, self.SOURCE_URIS)

    def test_to_api_repr_source_format(self):
        ec = external_config.ExternalConfig("CSV")
        got = ec.to_api_repr()
        want = {"sourceFormat": "CSV"}
        self.assertEqual(got, want)

    def test_from_api_repr_sheets(self):
        resource = _copy_and_update(
            self.BASE_RESOURCE,
            {
                "sourceFormat": "GOOGLE_SHEETS",
                "googleSheetsOptions": {
                    "skipLeadingRows": "123",
                    "range": "Sheet1!A5:B10",
                },
            },
        )

        ec = external_config.ExternalConfig.from_api_repr(resource)

        self._verify_base(ec)
        self.assertEqual(ec.source_format, "GOOGLE_SHEETS")
        self.assertIsInstance(ec.options, external_config.GoogleSheetsOptions)
        self.assertEqual(ec.options.skip_leading_rows, 123)
        self.assertEqual(ec.options.range, "Sheet1!A5:B10")

        got_resource = ec.to_api_repr()

        self.assertEqual(got_resource, resource)

        del resource["googleSheetsOptions"]["skipLeadingRows"]
        del resource["googleSheetsOptions"]["range"]
        ec = external_config.ExternalConfig.from_api_repr(resource)
        self.assertIsNone(ec.options.skip_leading_rows)
        self.assertIsNone(ec.options.range)
        got_resource = ec.to_api_repr()
        self.assertEqual(got_resource, resource)

    def test_to_api_repr_sheets(self):
        ec = external_config.ExternalConfig("GOOGLE_SHEETS")
        options = external_config.GoogleSheetsOptions()
        options.skip_leading_rows = 123
        options.range = "Sheet1!A5:B10"
        ec._options = options

        exp_resource = {
            "sourceFormat": "GOOGLE_SHEETS",
            "googleSheetsOptions": {"skipLeadingRows": "123", "range": "Sheet1!A5:B10"},
        }

        got_resource = ec.to_api_repr()

        self.assertEqual(got_resource, exp_resource)

    def test_from_api_repr_hive_partitioning(self):
        resource = _copy_and_update(
            self.BASE_RESOURCE,
            {
                "sourceFormat": "FORMAT_FOO",
                "hivePartitioningOptions": {
                    "sourceUriPrefix": "http://foo/bar",
                    "mode": "STRINGS",
                    "requirePartitionFilter": True,
                },
            },
        )

        ec = external_config.ExternalConfig.from_api_repr(resource)

        self._verify_base(ec)
        self.assertEqual(ec.source_format, "FORMAT_FOO")
        self.assertIsInstance(
            ec.hive_partitioning, external_config.HivePartitioningOptions
        )
        self.assertEqual(ec.hive_partitioning.source_uri_prefix, "http://foo/bar")
        self.assertEqual(ec.hive_partitioning.mode, "STRINGS")
        self.assertEqual(ec.hive_partitioning.require_partition_filter, True)

        # converting back to API representation should yield the same result
        got_resource = ec.to_api_repr()
        self.assertEqual(got_resource, resource)

        del resource["hivePartitioningOptions"]
        ec = external_config.ExternalConfig.from_api_repr(resource)
        self.assertIsNone(ec.hive_partitioning)

        got_resource = ec.to_api_repr()
        self.assertEqual(got_resource, resource)

    def test_to_api_repr_hive_partitioning(self):
        hive_partitioning = external_config.HivePartitioningOptions()
        hive_partitioning.source_uri_prefix = "http://foo/bar"
        hive_partitioning.mode = "STRINGS"
        hive_partitioning.require_partition_filter = False

        ec = external_config.ExternalConfig("FORMAT_FOO")
        ec.hive_partitioning = hive_partitioning

        got_resource = ec.to_api_repr()

        expected_resource = {
            "sourceFormat": "FORMAT_FOO",
            "hivePartitioningOptions": {
                "sourceUriPrefix": "http://foo/bar",
                "mode": "STRINGS",
                "requirePartitionFilter": False,
            },
        }
        self.assertEqual(got_resource, expected_resource)

    def test_from_api_repr_csv(self):
        resource = _copy_and_update(
            self.BASE_RESOURCE,
            {
                "sourceFormat": "CSV",
                "csvOptions": {
                    "fieldDelimiter": "fieldDelimiter",
                    "skipLeadingRows": "123",
                    "quote": "quote",
                    "allowQuotedNewlines": True,
                    "allowJaggedRows": False,
                    "encoding": "encoding",
                },
            },
        )

        ec = external_config.ExternalConfig.from_api_repr(resource)

        self._verify_base(ec)
        self.assertEqual(ec.source_format, "CSV")
        self.assertIsInstance(ec.options, external_config.CSVOptions)
        self.assertEqual(ec.options.field_delimiter, "fieldDelimiter")
        self.assertEqual(ec.options.skip_leading_rows, 123)
        self.assertEqual(ec.options.quote_character, "quote")
        self.assertEqual(ec.options.allow_quoted_newlines, True)
        self.assertEqual(ec.options.allow_jagged_rows, False)
        self.assertEqual(ec.options.encoding, "encoding")

        got_resource = ec.to_api_repr()

        self.assertEqual(got_resource, resource)

        del resource["csvOptions"]["skipLeadingRows"]
        ec = external_config.ExternalConfig.from_api_repr(resource)
        self.assertIsNone(ec.options.skip_leading_rows)
        got_resource = ec.to_api_repr()
        self.assertEqual(got_resource, resource)

    def test_to_api_repr_csv(self):
        ec = external_config.ExternalConfig("CSV")
        options = external_config.CSVOptions()
        options.allow_quoted_newlines = True
        options.encoding = "encoding"
        options.field_delimiter = "fieldDelimiter"
        options.quote_character = "quote"
        options.skip_leading_rows = 123
        options.allow_jagged_rows = False
        ec._options = options

        exp_resource = {
            "sourceFormat": "CSV",
            "csvOptions": {
                "fieldDelimiter": "fieldDelimiter",
                "skipLeadingRows": "123",
                "quote": "quote",
                "allowQuotedNewlines": True,
                "allowJaggedRows": False,
                "encoding": "encoding",
            },
        }

        got_resource = ec.to_api_repr()

        self.assertEqual(got_resource, exp_resource)

    def test_from_api_repr_bigtable(self):
        qualifier_encoded = base64.standard_b64encode(b"q").decode("ascii")
        resource = _copy_and_update(
            self.BASE_RESOURCE,
            {
                "sourceFormat": "BIGTABLE",
                "bigtableOptions": {
                    "ignoreUnspecifiedColumnFamilies": True,
                    "readRowkeyAsString": False,
                    "columnFamilies": [
                        {
                            "familyId": "familyId",
                            "type": "type",
                            "encoding": "encoding",
                            "columns": [
                                {
                                    "qualifierString": "q",
                                    "fieldName": "fieldName1",
                                    "type": "type1",
                                    "encoding": "encoding1",
                                    "onlyReadLatest": True,
                                },
                                {
                                    "qualifierEncoded": qualifier_encoded,
                                    "fieldName": "fieldName2",
                                    "type": "type2",
                                    "encoding": "encoding2",
                                },
                            ],
                            "onlyReadLatest": False,
                        }
                    ],
                },
            },
        )

        ec = external_config.ExternalConfig.from_api_repr(resource)

        self._verify_base(ec)
        self.assertEqual(ec.source_format, "BIGTABLE")
        self.assertIsInstance(ec.options, external_config.BigtableOptions)
        self.assertEqual(ec.options.ignore_unspecified_column_families, True)
        self.assertEqual(ec.options.read_rowkey_as_string, False)
        self.assertEqual(len(ec.options.column_families), 1)
        fam1 = ec.options.column_families[0]
        self.assertIsInstance(fam1, external_config.BigtableColumnFamily)
        self.assertEqual(fam1.family_id, "familyId")
        self.assertEqual(fam1.type_, "type")
        self.assertEqual(fam1.encoding, "encoding")
        self.assertEqual(len(fam1.columns), 2)
        self.assertFalse(fam1.only_read_latest)
        col1 = fam1.columns[0]
        self.assertEqual(col1.qualifier_string, "q")
        self.assertEqual(col1.field_name, "fieldName1")
        self.assertEqual(col1.type_, "type1")
        self.assertEqual(col1.encoding, "encoding1")
        self.assertTrue(col1.only_read_latest)
        self.assertIsNone(col1.qualifier_encoded)
        col2 = ec.options.column_families[0].columns[1]
        self.assertEqual(col2.qualifier_encoded, b"q")
        self.assertEqual(col2.field_name, "fieldName2")
        self.assertEqual(col2.type_, "type2")
        self.assertEqual(col2.encoding, "encoding2")

        got_resource = ec.to_api_repr()

        self.assertEqual(got_resource, resource)

    def test_to_api_repr_bigtable(self):
        ec = external_config.ExternalConfig("BIGTABLE")
        options = external_config.BigtableOptions()
        options.ignore_unspecified_column_families = True
        options.read_rowkey_as_string = False
        ec._options = options

        fam1 = external_config.BigtableColumnFamily()
        fam1.family_id = "familyId"
        fam1.type_ = "type"
        fam1.encoding = "encoding"
        fam1.only_read_latest = False
        col1 = external_config.BigtableColumn()
        col1.qualifier_string = "q"
        col1.field_name = "fieldName1"
        col1.type_ = "type1"
        col1.encoding = "encoding1"
        col1.only_read_latest = True
        col2 = external_config.BigtableColumn()
        col2.qualifier_encoded = b"q"
        col2.field_name = "fieldName2"
        col2.type_ = "type2"
        col2.encoding = "encoding2"
        fam1.columns = [col1, col2]
        options.column_families = [fam1]

        qualifier_encoded = base64.standard_b64encode(b"q").decode("ascii")
        exp_resource = {
            "sourceFormat": "BIGTABLE",
            "bigtableOptions": {
                "ignoreUnspecifiedColumnFamilies": True,
                "readRowkeyAsString": False,
                "columnFamilies": [
                    {
                        "familyId": "familyId",
                        "type": "type",
                        "encoding": "encoding",
                        "columns": [
                            {
                                "qualifierString": "q",
                                "fieldName": "fieldName1",
                                "type": "type1",
                                "encoding": "encoding1",
                                "onlyReadLatest": True,
                            },
                            {
                                "qualifierEncoded": qualifier_encoded,
                                "fieldName": "fieldName2",
                                "type": "type2",
                                "encoding": "encoding2",
                            },
                        ],
                        "onlyReadLatest": False,
                    }
                ],
            },
        }

        got_resource = ec.to_api_repr()

        self.assertEqual(got_resource, exp_resource)

    def test_parquet_options_getter(self):
        from google.cloud.bigquery.format_options import ParquetOptions

        parquet_options = ParquetOptions.from_api_repr(
            {"enumAsString": True, "enableListInference": False}
        )
        ec = external_config.ExternalConfig(
            external_config.ExternalSourceFormat.PARQUET
        )

        self.assertIsNone(ec.parquet_options.enum_as_string)
        self.assertIsNone(ec.parquet_options.enable_list_inference)

        ec._options = parquet_options

        self.assertTrue(ec.parquet_options.enum_as_string)
        self.assertFalse(ec.parquet_options.enable_list_inference)

        self.assertIs(ec.parquet_options, ec.options)

    def test_parquet_options_getter_non_parquet_format(self):
        ec = external_config.ExternalConfig(external_config.ExternalSourceFormat.CSV)
        self.assertIsNone(ec.parquet_options)

    def test_parquet_options_setter(self):
        from google.cloud.bigquery.format_options import ParquetOptions

        parquet_options = ParquetOptions.from_api_repr(
            {"enumAsString": False, "enableListInference": True}
        )
        ec = external_config.ExternalConfig(
            external_config.ExternalSourceFormat.PARQUET
        )

        ec.parquet_options = parquet_options

        # Setting Parquet options should be reflected in the generic options attribute.
        self.assertFalse(ec.options.enum_as_string)
        self.assertTrue(ec.options.enable_list_inference)

    def test_parquet_options_setter_non_parquet_format(self):
        from google.cloud.bigquery.format_options import ParquetOptions

        parquet_options = ParquetOptions.from_api_repr(
            {"enumAsString": False, "enableListInference": True}
        )
        ec = external_config.ExternalConfig(external_config.ExternalSourceFormat.CSV)

        with self.assertRaisesRegex(TypeError, "Cannot set.*source format is CSV"):
            ec.parquet_options = parquet_options

    def test_from_api_repr_parquet(self):
        from google.cloud.bigquery.format_options import ParquetOptions

        resource = _copy_and_update(
            self.BASE_RESOURCE,
            {
                "sourceFormat": "PARQUET",
                "parquetOptions": {"enumAsString": True, "enableListInference": False},
            },
        )

        ec = external_config.ExternalConfig.from_api_repr(resource)

        self._verify_base(ec)
        self.assertEqual(ec.source_format, external_config.ExternalSourceFormat.PARQUET)
        self.assertIsInstance(ec.options, ParquetOptions)
        self.assertTrue(ec.parquet_options.enum_as_string)
        self.assertFalse(ec.parquet_options.enable_list_inference)

        got_resource = ec.to_api_repr()

        self.assertEqual(got_resource, resource)

        del resource["parquetOptions"]["enableListInference"]
        ec = external_config.ExternalConfig.from_api_repr(resource)
        self.assertIsNone(ec.options.enable_list_inference)
        got_resource = ec.to_api_repr()
        self.assertEqual(got_resource, resource)

    def test_to_api_repr_parquet(self):
        from google.cloud.bigquery.format_options import ParquetOptions

        ec = external_config.ExternalConfig(
            external_config.ExternalSourceFormat.PARQUET
        )
        options = ParquetOptions.from_api_repr(
            dict(enumAsString=False, enableListInference=True)
        )
        ec._options = options

        exp_resource = {
            "sourceFormat": external_config.ExternalSourceFormat.PARQUET,
            "parquetOptions": {"enumAsString": False, "enableListInference": True},
        }

        got_resource = ec.to_api_repr()

        self.assertEqual(got_resource, exp_resource)


def _copy_and_update(d, u):
    d = copy.deepcopy(d)
    d.update(u)
    return d
