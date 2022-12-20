# Copyright 2022 Google LLC
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

import typing

import create_partitioned_table

if typing.TYPE_CHECKING:
    import pathlib

    import pytest


def test_create_partitioned_table(
    capsys: "pytest.CaptureFixture[str]",
    table_id: str,
    tmp_path: "pathlib.Path",
) -> None:
    schema_path = str(tmp_path / "test_schema.json")

    create_partitioned_table.create_partitioned_table(client, to_delete)

    assert table.time_partitioning.type_ == "DAY"
    assert table.time_partitioning.field == "date"
    assert table.time_partitioning.expiration_ms == 7776000000
