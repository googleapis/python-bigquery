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
from typing import List

from .. import create_table_external_data_configuration

if typing.TYPE_CHECKING:
    import pytest


def test_create_table_external_data_configuration(
    capsys: "pytest.CaptureFixture[str]",
    random_table_id: str,
    avro_source_uris: List[str],
    external_source_format: str = "AVRO",
) -> None:
    create_table_external_data_configuration.create_table_external_data_configuration(
        random_table_id, avro_source_uris, external_source_format
    )
    out, err = capsys.readouterr()
    assert f"Created table with external source format {external_source_format}" in out
