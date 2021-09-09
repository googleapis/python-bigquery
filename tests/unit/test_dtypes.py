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

import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")


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
def test_array_construction2(dtype):
    a = _make_one(dtype)
    sample_values = SAMPLE_VALUES[dtype]
    assert len(a) == 3
    assert a[0], a[1] == sample_values[:2]
    assert a[2] is None

    # implementation details:
    assert a.nbytes == 24
    assert np.array_equal(
        a._ndarray == np.array(SAMPLE_DT_VALUES[dtype][:2] + ('NaT', ),
                               dtype="datetime64[us]"),
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
        a[:2], cls._from_sequence([sample_values[2], sample_values[1]]))

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
