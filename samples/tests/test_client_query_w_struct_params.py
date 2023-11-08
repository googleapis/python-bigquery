# Copyright 2019 Google LLC
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

from .. import client_query_w_struct_params

if typing.TYPE_CHECKING:
    import pytest


def test_client_query_w_struct_params(capsys: "pytest.CaptureFixture[str]") -> None:
    client_query_w_struct_params.client_query_w_struct_params()
    out, err = capsys.readouterr()
    assert "1" in out
    assert "foo" in out
