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

import typing

import load_table_uri_firestore  # type: ignore

if typing.TYPE_CHECKING:
    import pytest


def test_load_table_uri_firestore(
    capsys: "pytest.CaptureFixture[str]", random_table_id: str
) -> None:
    load_table_uri_firestore.load_table_uri_firestore(random_table_id)
    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out
