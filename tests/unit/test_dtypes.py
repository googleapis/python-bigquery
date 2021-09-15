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

for_date_and_time = pytest.mark.parametrize("dtype", ["date", "time"])


@pytest.fixture(autouse=True)
def register_dtype():
    import google.cloud.bigquery.dtypes  # noqa


def _cls(dtype):
    from google.cloud.bigquery import dtypes

    return getattr(dtypes, dtype.capitalize() + "Array")


def _make_one(dtype):
    return _cls(dtype)._from_sequence(SAMPLE_RAW_VALUES[dtype])


@for_date_and_time
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


@for_date_and_time
def test_array_construction_bad_vaue_type(dtype):
    with pytest.raises(TypeError, match="Invalid value type"):
        _cls(dtype)._from_sequence([42])


@for_date_and_time
def test_time_series_construction(dtype):
    sample_values = SAMPLE_VALUES[dtype]
    s = pd.Series(SAMPLE_RAW_VALUES[dtype], dtype=dtype)
    assert len(s) == 3
    assert s[0], s[1] == sample_values[:2]
    assert s[2] is None
    assert s.nbytes == 24
    assert isinstance(s.array, _cls(dtype))


@for_date_and_time
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


@for_date_and_time
def test___getitem___arrayindex(dtype):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    assert np.array_equal(
        cls(sample_values)[[1, 3]], cls([sample_values[1], sample_values[3]]),
    )


@for_date_and_time
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


@for_date_and_time
def test_item_assignment(dtype):
    a = _make_one(dtype)[:2]
    sample_values = SAMPLE_VALUES[dtype]
    cls = _cls(dtype)
    a[0] = sample_values[2]
    assert np.array_equal(a, cls._from_sequence([sample_values[2], sample_values[1]]))
    a[1] = None
    assert np.array_equal(a, cls._from_sequence([sample_values[2], None]))


@for_date_and_time
def test_array_assignment(dtype):
    a = _make_one(dtype)
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    a[a.isna()] = sample_values[3]
    assert np.array_equal(a, cls([sample_values[i] for i in (0, 1, 3)]))
    a[[0, 2]] = sample_values[2]
    assert np.array_equal(a, cls([sample_values[i] for i in (2, 1, 2)]))


@for_date_and_time
def test_repeat(dtype):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    a = cls._from_sequence(sample_values).repeat(3)
    assert list(a) == sorted(sample_values * 3)


@for_date_and_time
def test_copy(dtype):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    a = cls._from_sequence(sample_values)
    b = a.copy()
    assert b is not a
    assert b._ndarray is not a._ndarray
    assert np.array_equal(b, a)


@for_date_and_time
def test_from_ndarray_copy(dtype):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    a = cls._from_sequence(sample_values)
    b = cls(a._ndarray, copy=True)
    assert b._ndarray is not a._ndarray
    assert np.array_equal(b, a)


@pytest.mark.skipif(
    # TODO: Can we make this work for Pandas 1.1 and later?
    pandas_release < (1, 3),
    reason="The .dt attribute was added in Pandas 1.1",
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


@for_date_and_time
def test__from_factorized(dtype):
    sample_values = SAMPLE_VALUES[dtype]
    a = _cls(dtype)(sample_values * 2)
    codes, b = a.factorize()
    assert b.__class__ is a.__class__
    assert [b[code] for code in codes] == list(a)


@for_date_and_time
def test_isna(dtype):
    a = _make_one(dtype)
    assert list(a.isna()) == [False, False, True]


@for_date_and_time
def test__validate_scalar_invalid(dtype):
    with pytest.raises(ValueError):
        _make_one(dtype)._validate_scalar("bad")


@for_date_and_time
@pytest.mark.parametrize(
    "allow_fill, fill_value",
    [
        (False, None),
        (True, None),
        (True, pd._libs.NaT if pd else None),
        (True, np.NaN if pd else None),
        (True, 42),
    ],
)
def test_take(dtype, allow_fill, fill_value):
    sample_values = SAMPLE_VALUES[dtype]
    a = _cls(dtype)(sample_values)
    if allow_fill:
        if fill_value == 42:
            fill_value = expected_fill = (
                datetime.date(1971, 4, 2)
                if dtype == "date"
                else datetime.time(0, 42, 42, 424242)
            )
        else:
            expected_fill = None
        b = a.take([1, -1, 3], allow_fill=True, fill_value=fill_value)
        expect = [sample_values[1], expected_fill, sample_values[3]]
    else:
        b = a.take([1, -4, 3])
        expect = [sample_values[1], sample_values[-4], sample_values[3]]

    assert list(b) == expect


@for_date_and_time
def test_take_bad_index(dtype):
    # When allow_fill is set, negative indexes < -1 raise ValueError.
    # This is based on testing with an integer series/array.
    # The documentation isn't clear on this at all.
    sample_values = SAMPLE_VALUES[dtype]
    a = _cls(dtype)(sample_values)
    with pytest.raises(ValueError):
        a.take([1, -2, 3], allow_fill=True, fill_value=None)


@for_date_and_time
def test__concat_same_type_via_concat(dtype):
    sample_values = SAMPLE_VALUES[dtype]
    s1 = pd.Series(sample_values[:2], dtype=dtype)
    s2 = pd.Series(sample_values[2:], dtype=dtype)
    assert tuple(pd.concat((s1, s2))) == sample_values


@for_date_and_time
def test__concat_same_type_not_same_type(dtype):
    # Test a dtype-compatibility in _concat_same_type.
    # This seems not to be needed in practice, because higher-level
    # convatenation code detects multiple dtypes and casts to a common
    # type, however, having the check seems hygienic. :)
    sample_values = SAMPLE_VALUES[dtype]
    s1 = pd.Series(sample_values[:2], dtype=dtype)
    s2 = pd.Series(sample_values[2:])
    with pytest.raises(ValueError):
        s1.array._concat_same_type((s1.array, s2.array))


@for_date_and_time
def test_dropna(dtype):
    assert np.array_equal(_make_one(dtype).dropna(), _make_one(dtype)[:2])


@pytest.mark.parametrize(
    "value, meth, limit, expect",
    [
        (1, None, None, [0, 1, 1, 3]),
        ([0, 2, 1, 0], None, None, [0, 2, 1, 3]),
        (None, "backfill", None, [0, 3, 3, 3]),
        (None, "bfill", None, [0, 3, 3, 3]),
        (None, "pad", None, [0, 0, 0, 3]),
        (None, "ffill", None, [0, 0, 0, 3]),
        (None, "backfill", 1, [0, None, 3, 3]),
        (None, "bfill", 1, [0, None, 3, 3]),
        (None, "pad", 1, [0, 0, None, 3]),
        (None, "ffill", 1, [0, 0, None, 3]),
    ],
)
@for_date_and_time
def test_fillna(dtype, value, meth, limit, expect):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    a = cls([sample_values[0], None, None, sample_values[3]])
    if isinstance(value, list):
        value = cls([sample_values[i] for i in value])
    elif value is not None:
        value = sample_values[value]
    expect = cls([None if i is None else sample_values[i] for i in expect])
    assert np.array_equal(a.fillna(value, meth, limit), expect)


@for_date_and_time
def test_unique(dtype):
    cls = _cls(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    assert np.array_equal(cls(sample_values * 3).unique(), cls(sample_values),)


@for_date_and_time
def test_argsort(dtype):
    sample_values = SAMPLE_VALUES[dtype]
    s = pd.Series(sample_values * 2, dtype=dtype).argsort()
    assert list(s) == [0, 4, 1, 5, 2, 6, 3, 7]


@for_date_and_time
def test_astype_copy(dtype):
    a = _make_one(dtype)
    b = a.astype(a.dtype, copy=True)
    assert b is not a
    assert b.__class__ is a.__class__
    assert np.array_equal(b, a)


@pytest.mark.parametrize(
    "dtype, same",
    [
        ("<M8[ns]", True),
        ("<M8", True),
        ("datetime64[ns]", True),
        ("datetime64", True),
        ("datetime", True),
        ("<M8[us]", False),
        ("<M8[ms]", False),
        ("<M8[s]", False),
        ("datetime64[us]", False),
        ("datetime64[ms]", False),
        ("datetime64[s]", False),
    ],
)
def test_asdatetime(dtype, same):
    a = _make_one("date")
    for dt in dtype, np.dtype(dtype) if dtype != "datetime" else dtype:
        if same:
            b = a.astype(dt, copy=False)
            assert b is a._ndarray
            copy = True
        else:
            copy = False

        b = a.astype(dt, copy=copy)
        assert b is not a._ndarray
        assert np.array_equal(b[:2], a._ndarray[:2])
        assert pd.isna(b[2]) and str(b[2]) == "NaT"


@pytest.mark.parametrize(
    "dtype",
    [
        "<m8",
        "<m8[s]",
        "<m8[ms]",
        "<m8[us]",
        "<m8[ns]",
        "timedelta",
        "timedelta64",
        "timedelta64[s]",
        "timedelta64[ms]",
        "timedelta64[us]",
        "timedelta64[ns]",
    ],
)
def test_astimedelta(dtype):
    t = "01:02:03.123456"
    expect = pd.to_timedelta([t]).array.astype(
        "timedelta64[ns]" if dtype == "timedelta" else dtype
    )

    a = _cls("time")([t, None])
    b = a.astype(dtype)
    np.array_equal(b[:1], expect)
    assert pd.isna(b[1]) and str(b[1]) == "NaT"
