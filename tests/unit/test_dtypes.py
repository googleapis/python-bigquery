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

import datetime

import packaging.version
import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")

pandas_release = packaging.version.parse(pd.__version__).release

SAMPLE_RAW_VALUES = dict(
    date=(datetime.date(2021, 2, 2), "2021-2-3", None),
    time=(datetime.time(1, 2, 2), "1:2:3.5", None),
)
SAMPLE_VALUES = dict(
    date=(
        datetime.date(2021, 2, 2),
        datetime.date(2021, 2, 3),
        datetime.date(2021, 2, 4),
        datetime.date(2021, 2, 5),
    ),
    time=(
        datetime.time(1, 2, 2),
        datetime.time(1, 2, 3, 500000),
        datetime.time(1, 2, 4, 500000),
        datetime.time(1, 2, 5, 500000),
    ),
)
SAMPLE_DT_VALUES = dict(
    date=(
        "2021-02-02T00:00:00.000000",
        "2021-02-03T00:00:00.000000",
        "2021-02-04T00:00:00.000000",
        "2021-02-05T00:00:00.000000",
    ),
    time=(
        "1970-01-01T01:02:02.000000",
        "1970-01-01T01:02:03.500000",
        "1970-01-01T01:02:04.500000",
        "1970-01-01T01:02:05.500000",
    ),
)


def _cls(dtype):
    from google.cloud.bigquery import dtypes

    return getattr(dtypes, dtype.capitalize() + "Array")


def _make_one(dtype):
    return _cls(dtype)._from_sequence(SAMPLE_RAW_VALUES[dtype])


@pytest.mark.parametrize("dtype", ["date", "time"])
@pytest.mark.parametrize(
    "factory_method", [None, "_from_sequence", "_from_sequence_of_strings"]
)
def test_array_construction(dtype, factory_method):
    sample_raw_values = SAMPLE_RAW_VALUES[dtype]
    factory = _cls(dtype)
    if factory_method:
        factory = getattr(factory, factory_method)
        if factory_method == "_from_sequence_of_strings":
            sample_raw_values = [
                str(v) if v is not None else v for v in sample_raw_values
            ]
    a = factory(sample_raw_values)
    assert len(a) == 3
    assert a.size == 3
    assert a.shape == (3,)
    sample_values = SAMPLE_VALUES[dtype]
    assert a[0], a[1] == sample_values[:2]
    assert a[2] is None

    # implementation details:
    assert a.nbytes == 24
    assert np.array_equal(
        a._ndarray
        == np.array(SAMPLE_DT_VALUES[dtype][:2] + ("NaT",), dtype="datetime64[us]"),
        [True, True, False],
    )


@pytest.mark.parametrize("dtype", ["date", "time"])
def test_array_construction_bad_vaue_type(dtype):
    with pytest.raises(TypeError, match="Invalid value type"):
        _cls(dtype)._from_sequence([42])


@pytest.mark.parametrize("dtype", ["date", "time"])
def test_time_series_construction(dtype):
    sample_values = SAMPLE_VALUES[dtype]
    s = pd.Series(SAMPLE_RAW_VALUES[dtype], dtype=dtype)
    assert len(s) == 3
    assert s[0], s[1] == sample_values[:2]
    assert s[2] is None
    assert s.nbytes == 24
    assert isinstance(s.array, _cls(dtype))


@pytest.mark.parametrize("dtype", ["date", "time"])
@pytest.mark.parametrize(
    "left,op,right,expected",
    [
        ([1, 2], "==", [1, 2], [True, True]),
        ([1, 2], "==", [1, 3], [True, False]),
        ([1, 3], "<=", [1, 2], [True, False]),
        ([1, 2], "<=", [1, 3], [True, True]),
        ([1, 3], ">=", [1, 2], [True, True]),
        ([1, 2], ">=", [1, 3], [True, False]),
    ],
)
def test_timearray_comparisons(
    dtype,
    left,
    op,
    right,
    expected,
    comparisons={
        "==": (lambda a, b: a == b),
        ">=": (lambda a, b: a >= b),
        "<=": (lambda a, b: a <= b),
    },
    complements={
        "==": (lambda a, b: a != b),
        ">=": (lambda a, b: a < b),
        "<=": (lambda a, b: a > b),
    },
):
    sample_values = SAMPLE_VALUES[dtype]
    left = [sample_values[index] for index in left]
    right = [sample_values[index] for index in right]
    left = _cls(dtype)._from_sequence(left)
    right = _cls(dtype)._from_sequence(right)
    right_obs = np.array(list(right))
    expected = np.array(expected)
    for r in right, right_obs:
        # Note that the right_obs comparisons work because
        # they're called on right_obs rather then left, because
        # TimeArrays only support comparisons with TimeArrays.
        assert np.array_equal(comparisons[op](left, r), expected)
        assert np.array_equal(complements[op](left, r), ~expected)

    # Bad shape
    for bad_shape in ([], [1, 2, 3]):
        if op == "==":
            assert not comparisons[op](left, np.array(bad_shape))
            assert complements[op](left, np.array(bad_shape))
        else:
            with pytest.raises(
                ValueError, match="operands could not be broadcast together",
            ):
                comparisons[op](left, np.array(bad_shape))
            with pytest.raises(
                ValueError, match="operands could not be broadcast together",
            ):
                complements[op](left, np.array(bad_shape))

    # Bad items
    for bad_items in (
        [1, 2],
        [1],  # a single-element array gets broadcast
    ):
        if op == "==":
            assert np.array_equal(
                comparisons[op](left, np.array(bad_items)), np.array([False, False])
            )
            assert np.array_equal(
                complements[op](left, np.array(bad_items)), np.array([True, True])
            )
        else:
            # Can't compare orderings times and ints:
            with pytest.raises(TypeError, match="not supported"):
                comparisons[op](left, np.array(bad_items))
            with pytest.raises(TypeError, match="not supported"):
                complements[op](left, np.array(bad_items))


@pytest.mark.parametrize("dtype", ["date", "time"])
def test_timearray_slicing(dtype):
    a = _make_one(dtype)
    b = a[:]
    assert b is not a
    assert b.__class__ == a.__class__
    assert np.array_equal(b, a)

    sample_values = SAMPLE_VALUES[dtype]
    cls = _cls(dtype)
    assert np.array_equal(a[:1], cls._from_sequence(sample_values[:1]))

    # Assignment works:
    a[:1] = cls._from_sequence([sample_values[2]])
    assert np.array_equal(
        a[:2], cls._from_sequence([sample_values[2], sample_values[1]])
    )

    # Series also work:
    s = pd.Series(SAMPLE_RAW_VALUES[dtype], dtype=dtype)
    assert np.array_equal(s[:1].array, cls._from_sequence([sample_values[0]]))


@pytest.mark.parametrize("dtype", ["date", "time"])
def test_item_assignment(dtype):
    a = _make_one(dtype)[:2]
    sample_values = SAMPLE_VALUES[dtype]
    cls = _cls(dtype)
    a[0] = sample_values[2]
    assert np.array_equal(a, cls._from_sequence([sample_values[2], sample_values[1]]))


@pytest.mark.parametrize("dtype", ["date", "time"])
def test_repeat(dtype):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    a = cls._from_sequence(sample_values).repeat(3)
    assert list(a) == sorted(sample_values * 3)


@pytest.mark.parametrize("dtype", ["date", "time"])
def test_copy(dtype):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    a = cls._from_sequence(sample_values)
    b = a.copy()
    assert b is not a
    assert b._ndarray is not a._ndarray
    assert np.array_equal(b, a)


@pytest.mark.parametrize("dtype", ["date", "time"])
def test_from_ndarray_copy(dtype):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    a = cls._from_sequence(sample_values)
    b = cls(a._ndarray, copy=True)
    assert b._ndarray is not a._ndarray
    assert np.array_equal(b, a)


@pytest.mark.skipif(
    # TODO: Can we make this work for Pandas 1.1 and later?
    pandas_release < (1, 3), reason="The .dt attribute was added in Pandas 1.1",
)
def test_dt_date_and_time_functions():
    dates = [datetime.date(2020, 1, 1), datetime.date(2021, 3, 31)]
    s = pd.Series(dates, dtype="date")
    assert list(s.dt.year) == [2020, 2021]
    assert list(s.dt.month) == [1, 3]
    assert list(s.dt.day) == [1, 31]
    assert list(s.dt.date) == dates
    assert list(s.dt.dayofyear) == [1, 90]
    assert list(s.dt.day_of_year) == [1, 90]
    assert list(s.dt.weekofyear) == [1, 13]
    assert list(s.dt.week) == [1, 13]
    assert list(s.dt.day_of_week) == [2, 2]
    assert list(s.dt.dayofweek) == [2, 2]
    assert list(s.dt.weekday) == [2, 2]
    assert list(s.dt.quarter) == [1, 1]
    assert list(s.dt.days_in_month) == [31, 31]
    assert list(s.dt.is_month_start) == [True, False]
    assert list(s.dt.is_month_end) == [False, True]
    assert list(s.dt.is_quarter_start) == [True, False]
    assert list(s.dt.is_quarter_end) == [False, True]
    assert list(s.dt.is_year_start) == [True, False]
    assert list(s.dt.is_year_end) == [False, False]
    assert list(s.dt.is_leap_year) == [True, False]

    times = [datetime.time(1, 2, 3), datetime.time(4, 5, 6, 500000)]
    s = pd.Series(times, dtype="time")
    assert list(s.dt.hour) == [1, 4]
    assert list(s.dt.minute) == [2, 5]
    assert list(s.dt.second) == [3, 6]
    assert list(s.dt.microsecond) == [0, 500000]
    # nanoseconds are distinct and BQ and Python time are only microsecond
    assert list(s.dt.nanosecond) == [0, 0]
    assert list(s.dt.time) == times
