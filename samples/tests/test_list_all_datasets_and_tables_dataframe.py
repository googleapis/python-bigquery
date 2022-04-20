# Copyright 2022 Cedarwood Insights Limited
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

import pytest

from .. import list_all_datasets_and_tables_dataframe

if typing.TYPE_CHECKING:
    from google.cloud import bigquery

pandas = pytest.importorskip("pandas")


def test_list_all_datasets_and_tables_dataframe(
    capsys: "pytest.CaptureFixture[str]", client: "bigquery.Client"
) -> None:
    dataset_tables_df = (
        list_all_datasets_and_tables_dataframe.list_all_datasets_and_tables_df()
    )
    out, err = capsys.readouterr()
    assert "Datasets and Tables in project {}:".format(client.project) in out
    df = dataset_tables_df
    assert df.columns.values.tolist() == ["project_id", "dataset_id", "table_id"]
    assert df["project_id"].iloc[0] == client.project
