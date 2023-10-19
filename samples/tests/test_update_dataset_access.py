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

from .. import update_dataset_access

if typing.TYPE_CHECKING:
    import pytest


def test_update_dataset_access(
    capsys: "pytest.CaptureFixture[str]", dataset_id: str
) -> None:
    update_dataset_access.update_dataset_access(dataset_id)
    out, err = capsys.readouterr()
    assert (
        "Updated dataset '{}' with modified user permissions.".format(dataset_id) in out
    )
