# Copyright 2023 Google LLC
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

import pytest

from google.cloud import bigquery
import google.cloud.bigquery.table


pyarrow = pytest.importorskip("pyarrow", minversion="3.0.0")


def test_to_arrow_with_jobs_query_response():
    resource = {
        "kind": "bigquery#queryResponse",
        "schema": {
            "fields": [
                {"name": "name", "type": "STRING", "mode": "NULLABLE"},
                {"name": "number", "type": "INTEGER", "mode": "NULLABLE"},
                {"name": "json", "type": "JSON", "mode": "NULLABLE"},
            ]
        },
        "jobReference": {
            "projectId": "test-project",
            "jobId": "job_ocd3cb-N62QIslU7R5qKKa2_427J",
            "location": "US",
        },
        "totalRows": "9",
        "rows": [
            {"f": [{"v": "Tiarra"}, {"v": "6"}, {"v": "123"}]},
            {"f": [{"v": "Timothy"}, {"v": "325"}, {"v": '{"key":"value"}'}]},
            {"f": [{"v": "Tina"}, {"v": "26"}, {"v": "[1,2,3]"}]},
            {
                "f": [
                    {"v": "Tierra"},
                    {"v": "10"},
                    {"v": '{"aKey": {"bKey": {"cKey": -123}}}'},
                ]
            },
            {"f": [{"v": "Tia"}, {"v": "17"}, {"v": None}]},
            {"f": [{"v": "Tiara"}, {"v": "22"}, {"v": '"some-json-string"'}]},
            {"f": [{"v": "Tiana"}, {"v": "6"}, {"v": '{"nullKey":null}'}]},
            {"f": [{"v": "Tiffany"}, {"v": "229"}, {"v": '""'}]},
            {"f": [{"v": "Tiffani"}, {"v": "8"}, {"v": "[]"}]},
        ],
        "totalBytesProcessed": "154775150",
        "jobComplete": True,
        "cacheHit": False,
        "queryId": "job_ocd3cb-N62QIslU7R5qKKa2_427J",
    }

    rows = google.cloud.bigquery.table.RowIterator(
        client=None,
        api_request=None,
        path=None,
        schema=[
            bigquery.SchemaField.from_api_repr(field)
            for field in resource["schema"]["fields"]
        ],
        first_page_response=resource,
    )
    records = rows.to_arrow()

    assert records.column_names == ["name", "number", "json"]
    assert records["name"].to_pylist() == [
        "Tiarra",
        "Timothy",
        "Tina",
        "Tierra",
        "Tia",
        "Tiara",
        "Tiana",
        "Tiffany",
        "Tiffani",
    ]
    assert records["number"].to_pylist() == [6, 325, 26, 10, 17, 22, 6, 229, 8]
    assert records["json"].to_pylist() == [
        "123",
        '{"key":"value"}',
        "[1,2,3]",
        '{"aKey": {"bKey": {"cKey": -123}}}',
        None,
        '"some-json-string"',
        '{"nullKey":null}',
        '""',
        "[]",
    ]


def test_to_arrow_with_json_arrow_type():
    # JSONArrowType added in 1.4.0.
    # https://github.com/googleapis/python-db-dtypes-pandas/pull/312
    db_dtypes = pytest.importorskip("db_dtypes", minversion="1.4.0")

    resource = {
        "kind": "bigquery#queryResponse",
        "schema": {
            "fields": [
                {"name": "json", "type": "JSON", "mode": "NULLABLE"},
                {
                    "name": "reference",
                    "type": "RECORD",
                    "mode": "NULLABLE",
                    "fields": [
                        {"name": "uri", "type": "STRING", "mode": "NULLABLE"},
                        {"name": "authorizer", "type": "STRING", "mode": "NULLABLE"},
                        {"name": "version", "type": "STRING", "mode": "NULLABLE"},
                        {"name": "details", "type": "JSON", "mode": "NULLABLE"},
                    ],
                },
                {"name": "repeated_json", "type": "JSON", "mode": "REPEATED"},
            ]
        },
        "jobReference": {
            "projectId": "test-project",
            "jobId": "job_ocd3cb-N62QIslU7R5qKKa2_427J",
            "location": "US",
        },
        "totalRows": "9",
        "rows": [
            {
                "f": [
                    {"v": '{"key": "value1"}'},
                    {
                        "v": {
                            "f": [
                                {"v": "uri1"},
                                {"v": "auth1"},
                                {"v": "v1"},
                                {"v": '{"detail_key": "detail_value1"}'},
                            ]
                        }
                    },
                    {"v": [{"v": '{"item1": 1}'}, {"v": '{"item2": 2}'}]},
                ]
            },
            {
                "f": [
                    {"v": '{"key": "value2", "num": 2}'},
                    {
                        "v": {
                            "f": [
                                {"v": "uri2"},
                                {"v": "auth2"},
                                {"v": "v2"},
                                {"v": '{"detail_key": "detail_value2", "num": 2}'},
                            ]
                        }
                    },
                    {
                        "v": [
                            {"v": '{"item3": 3}'},
                            {"v": '{"item4": 4}'},
                            {"v": '{"item5": 5}'},
                        ]
                    },
                ]
            },
            {
                "f": [
                    {"v": "null"},
                    {"v": None},
                    {"v": []},
                ]
            },
            {
                "f": [
                    {"v": '{"key": "value4"}'},
                    {
                        "v": {
                            "f": [
                                {"v": "uri4"},
                                {"v": "auth4"},
                                {"v": "v4"},
                                {"v": None},
                            ]
                        }
                    },
                    {"v": [{"v": '{"item6": 6}'}]},
                ]
            },
            {
                "f": [
                    {"v": '{"key": "value5"}'},
                    {
                        "v": {
                            "f": [
                                {"v": None},
                                {"v": None},
                                {"v": None},
                                {"v": None},
                            ]
                        }
                    },
                    {"v": []},
                ]
            },
            {
                "f": [
                    {"v": None},
                    {"v": None},
                    {"v": []},  # Note: None is not supported for REPEATED fields.
                ]
            },
            {
                "f": [
                    {"v": '{"key": "value7"}'},
                    {
                        "v": {
                            "f": [
                                {"v": "uri7"},
                                {"v": "auth7"},
                                {"v": "v7"},
                                {"v": '{"detail_key": "detail_value7"}'},
                            ]
                        }
                    },
                    {"v": []},
                ]
            },
            {
                "f": [
                    {"v": '{"key": "value8"}'},
                    {
                        "v": {
                            "f": [
                                {"v": "uri8"},
                                {"v": "auth8"},
                                {"v": "v8"},
                                {"v": '{"detail_key": "detail_value8"}'},
                            ]
                        }
                    },
                    {"v": [{"v": '{"item9": 9}'}, {"v": '{"item10": 10}'}]},
                ]
            },
            {
                "f": [
                    {"v": '{"key": "value9"}'},
                    {
                        "v": {
                            "f": [
                                {"v": "uri9"},
                                {"v": "auth9"},
                                {"v": "v9"},
                                {"v": '{"detail_key": "detail_value9"}'},
                            ]
                        }
                    },
                    {
                        "v": [
                            {"v": '{"item11": 11}'},
                            {"v": '{"item12": 12}'},
                            {"v": '{"item13": 13}'},
                        ]
                    },
                ]
            },
        ],
        "totalBytesProcessed": "154775150",
        "jobComplete": True,
        "cacheHit": False,
        "queryId": "job_ocd3cb-N62QIslU7R5qKKa2_427J",
    }

    rows = google.cloud.bigquery.table.RowIterator(
        client=None,
        api_request=None,
        path=None,
        schema=[
            bigquery.SchemaField.from_api_repr(field)
            for field in resource["schema"]["fields"]
        ],
        first_page_response=resource,
    )
    records = rows.to_arrow(json_arrow_type=db_dtypes.JSONArrowType())

    assert records.column_names == ["name", "number", "json"]
    assert records["name"].to_pylist() == [
        "Tiarra",
        "Timothy",
        "Tina",
        "Tierra",
        "Tia",
        "Tiara",
        "Tiana",
        "Tiffany",
        "Tiffani",
    ]
    assert records["number"].to_pylist() == [6, 325, 26, 10, 17, 22, 6, 229, 8]
    assert records["json"].to_pylist() == [
        "123",
        '{"key":"value"}',
        "[1,2,3]",
        '{"aKey": {"bKey": {"cKey": -123}}}',
        None,
        '"some-json-string"',
        '{"nullKey":null}',
        '""',
        "[]",
    ]


def test_to_arrow_with_jobs_query_response_and_max_results():
    resource = {
        "kind": "bigquery#queryResponse",
        "schema": {
            "fields": [
                {"name": "name", "type": "STRING", "mode": "NULLABLE"},
                {"name": "number", "type": "INTEGER", "mode": "NULLABLE"},
                {"name": "json", "type": "JSON", "mode": "NULLABLE"},
            ]
        },
        "jobReference": {
            "projectId": "test-project",
            "jobId": "job_ocd3cb-N62QIslU7R5qKKa2_427J",
            "location": "US",
        },
        "totalRows": "9",
        "rows": [
            {"f": [{"v": "Tiarra"}, {"v": "6"}, {"v": "123"}]},
            {"f": [{"v": "Timothy"}, {"v": "325"}, {"v": '{"key":"value"}'}]},
            {"f": [{"v": "Tina"}, {"v": "26"}, {"v": "[1,2,3]"}]},
            {
                "f": [
                    {"v": "Tierra"},
                    {"v": "10"},
                    {"v": '{"aKey": {"bKey": {"cKey": -123}}}'},
                ]
            },
            {"f": [{"v": "Tia"}, {"v": "17"}, {"v": None}]},
            {"f": [{"v": "Tiara"}, {"v": "22"}, {"v": '"some-json-string"'}]},
            {"f": [{"v": "Tiana"}, {"v": "6"}, {"v": '{"nullKey":null}'}]},
            {"f": [{"v": "Tiffany"}, {"v": "229"}, {"v": '""'}]},
            {"f": [{"v": "Tiffani"}, {"v": "8"}, {"v": "[]"}]},
        ],
        "totalBytesProcessed": "154775150",
        "jobComplete": True,
        "cacheHit": False,
        "queryId": "job_ocd3cb-N62QIslU7R5qKKa2_427J",
    }

    rows = google.cloud.bigquery.table.RowIterator(
        client=None,
        api_request=None,
        path=None,
        schema=[
            bigquery.SchemaField.from_api_repr(field)
            for field in resource["schema"]["fields"]
        ],
        first_page_response=resource,
        max_results=3,
    )
    records = rows.to_arrow()

    assert records.column_names == ["name", "number", "json"]
    assert records["name"].to_pylist() == [
        "Tiarra",
        "Timothy",
        "Tina",
    ]
    assert records["number"].to_pylist() == [6, 325, 26]
    assert records["json"].to_pylist() == ["123", '{"key":"value"}', "[1,2,3]"]
