# Copyright 2020 Google LLC
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

from .. import load_table_dataframe_array_contains


pandas = pytest.importorskip("pandas")
pyarrow = pytest.importorskip("pyarrow", minversion="2.0.0")


def test_load_table_dataframe_array_contains(capsys, random_table_id):

    table = load_table_dataframe_array_contains.load_table_dataframe_array_contains(
        random_table_id
    )
    out, _ = capsys.readouterr()
    expected_column_names = ["A"]
    assert "Loaded 3 rows and {} columns".format(len(expected_column_names)) in out

    column_names = [field.name for field in table.schema]
    assert column_names == expected_column_names
