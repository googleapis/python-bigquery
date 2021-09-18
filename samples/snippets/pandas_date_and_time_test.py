# Copyright 2021 Google Inc. All Rights Reserved.
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

import datetime

from pandas import Timestamp


def test_pandas_date_and_time():
    from pandas_date_and_time import pandas_date_and_time

    dates, _, times, _, combined = pandas_date_and_time()

    assert str(dates.dtype) == "bqdate"
    assert list(dates) == [datetime.date(2021, 9, 17), datetime.date(2021, 9, 18)]

    assert str(times.dtype) == "bqtime"
    assert list(times) == [
        datetime.time(1, 2, 3, 456789),
        datetime.time(12, 0, 0, 600000),
    ]

    assert str(combined.dtype) == "datetime64[ns]"
    assert list(combined) == [
        Timestamp("2021-09-17 01:02:03.456789"),
        Timestamp("2021-09-18 12:00:00.600000"),
    ]
