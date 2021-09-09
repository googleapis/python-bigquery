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


def _make_one():
    from google.cloud.bigquery.dtypes import TimeArray

    return TimeArray._from_sequence((datetime.time(15, 39, 42), "1:2:3.5"))


@pytest.fixture
def TimeArray():
    from google.cloud.bigquery.dtypes import TimeArray

    return TimeArray


def test_timearray_construction():
    a = _make_one()
    assert len(a) == 2
    assert a[0] == datetime.time(15, 39, 42)
    assert a[1] == datetime.time(1, 2, 3, 500000)

    # implementation details:
    assert a.nbytes == 16
    assert np.array_equal(
        a._ndarray,
        np.array(
            ["1970-01-01T15:39:42.000000", "1970-01-01T01:02:03.500000"],
            dtype="datetime64[us]",
        ),
    )


def test_time_series_construction(TimeArray):
    s = pd.Series([datetime.time(15, 39, 42), "1:2:3.5"], dtype="time")
    assert len(s) == 2
    assert s[0] == datetime.time(15, 39, 42)
    assert s[1] == datetime.time(1, 2, 3, 500000)
    assert s.nbytes == 16
    assert isinstance(s.array, TimeArray)


@pytest.mark.parametrize(
    "left,op,right,expected",
    [
        (["1:2:3.5", "15:39:42"], "==", ["1:2:3.5", "15:39:42"], [True, True]),
        (["1:2:3.5", "15:39:43"], "==", ["1:2:3.5", "15:39:42"], [True, False]),
        (["1:2:3.5", "15:39:43"], "<=", ["1:2:3.5", "15:39:42"], [True, False]),
        (["1:2:3.5", "15:39:41"], "<=", ["1:2:3.5", "15:39:42"], [True, True]),
        (["1:2:3.5", "15:39:43"], ">=", ["1:2:3.5", "15:39:42"], [True, True]),
        (["1:2:3.5", "15:39:41"], ">=", ["1:2:3.5", "15:39:42"], [True, False]),
    ],
)
def test_timearray_comparisons(
    TimeArray,
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
    left = TimeArray._from_sequence(left)
    right = TimeArray._from_sequence(right)
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


def test_timearray_slicing(TimeArray):
    a = _make_one()
    b = a[:]
    assert b is not a
    assert b.__class__ == a.__class__
    assert np.array_equal(b, a)

    assert np.array_equal(a[:1], TimeArray._from_sequence(["15:39:42"]))

    # Assignment works:
    a[:1] = TimeArray._from_sequence(["0:0:0"])
    assert np.array_equal(a, TimeArray._from_sequence(["0:0:0", "1:2:3.5"]))

    # Series also work:
    s = pd.Series(["1:2:3.5", "15:39:42"], dtype="time")
    assert np.array_equal(s[:1].array, TimeArray._from_sequence(["1:2:3.5"]))


def test_item_assignment(TimeArray):
    a = _make_one()
    a[0] = datetime.time(0, 0, 0)
    assert np.array_equal(a, TimeArray._from_sequence(["0:0:0", "1:2:3.5"]))
