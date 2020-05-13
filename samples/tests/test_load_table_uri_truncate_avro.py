# Copyright 2020 Google LLC
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

from .. import load_table_uri_truncate_avro


def test_load_table_uri_truncate_avro(capsys, random_table_id):
    load_table_uri_truncate_avro.load_table_uri_truncate_avro(random_table_id)
    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out
