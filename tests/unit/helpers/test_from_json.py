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

from dateutil.relativedelta import relativedelta
import pytest

from google.cloud.bigquery.schema import SchemaField


def create_field(mode="NULLABLE", type_="IGNORED"):
    return SchemaField("test_field", type_, mode=mode)


@pytest.fixture
def mut():
    from google.cloud.bigquery import _helpers

    return _helpers


def test_interval_from_json_w_none_nullable(mut):
    got = mut._interval_from_json(None, create_field())
    assert got is None


def test_interval_from_json_w_none_required(mut):
    with pytest.raises(TypeError):
        mut._interval_from_json(None, create_field(mode="REQUIRED"))


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        # SELECT INTERVAL -1 YEAR
        ("-1-0 0 0:0:0", relativedelta(years=-1)),
        # SELECT INTERVAL -1 MONTH
        ("-0-1 0 0:0:0", relativedelta(months=-1)),
        # SELECT INTERVAL -1 DAY
        ("0-0 -1 0:0:0", relativedelta(days=-1)),
        # SELECT INTERVAL -1 HOUR
        ("0-0 0 -1:0:0", relativedelta(hours=-1)),
        # SELECT INTERVAL -1 MINUTE
        ("0-0 0 -0:1:0", relativedelta(minutes=-1)),
        # SELECT INTERVAL -1 SECOND
        ("0-0 0 -0:0:1", relativedelta(seconds=-1)),
        # SELECT (INTERVAL -1 SECOND) / 1000000
        ("0-0 0 -0:0:0.000001", relativedelta(microseconds=-1)),
        # Test with multiple digits in each section.
        (
            "32-11 45 67:16:23.987654",
            relativedelta(
                years=32,
                months=11,
                days=45,
                hours=67,
                minutes=16,
                seconds=23,
                microseconds=987654,
            ),
        ),
        (
            "-32-11 -45 -67:16:23.987654",
            relativedelta(
                years=-32,
                months=-11,
                days=-45,
                hours=-67,
                minutes=-16,
                seconds=-23,
                microseconds=-987654,
            ),
        ),
        # Test with mixed +/- sections.
        (
            "9999-9 -999999 9999999:59:59.999999",
            relativedelta(
                years=9999,
                months=9,
                days=-999999,
                hours=9999999,
                minutes=59,
                seconds=59,
                microseconds=999999,
            ),
        ),
        # Test with fraction that is not microseconds.
        ("0-0 0 0:0:0.1", relativedelta(microseconds=100000)),
        ("0-0 0 0:0:0.12", relativedelta(microseconds=120000)),
        ("0-0 0 0:0:0.123", relativedelta(microseconds=123000)),
        ("0-0 0 0:0:0.1234", relativedelta(microseconds=123400)),
    ),
)
def test_w_string_values(mut, value, expected):
    got = mut._interval_from_json(value, create_field())
    assert got == expected
