# -*- coding: utf-8 -*-
#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from google.cloud.bigquery_v2.types import StandardSqlDataType
from google.cloud.bigquery_v2.types import StandardSqlField


@pytest.fixture
def target_class():
    from google.cloud.bigquery.routine import StandardSQLTableType

    return StandardSQLTableType


@pytest.fixture
def table_type_columns():
    columns = [
        StandardSqlField(
            name="int_col",
            type=StandardSqlDataType(type_kind=StandardSqlDataType.TypeKind.INT64),
        ),
        StandardSqlField(
            name="str_col",
            type=StandardSqlDataType(type_kind=StandardSqlDataType.TypeKind.STRING),
        ),
    ]
    return columns


def test_ctor(target_class, table_type_columns):
    result = target_class(columns=table_type_columns)

    assert result.columns == table_type_columns
    del table_type_columns[0]
    assert len(result.columns) == 2, "Instance should store a shallow copy of columns."


def test_eq_hit(target_class, table_type_columns):
    table_type = target_class(columns=table_type_columns)
    table_type_2 = target_class(columns=table_type_columns)
    assert table_type == table_type_2


def test_eq_miss_different_columns(target_class, table_type_columns):
    table_type = target_class(columns=table_type_columns[:1])
    table_type_2 = target_class(columns=table_type_columns[1:])
    assert table_type != table_type_2


def test_eq_miss_different_type(target_class, table_type_columns):
    table_type = target_class(columns=table_type_columns)
    assert table_type != object()
