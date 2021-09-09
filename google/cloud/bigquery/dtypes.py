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
from typing import Optional

import numpy
import pandas.core.arrays.datetimelike
import pandas.core.construction
import pandas.core.dtypes.base
import pandas.core.arraylike
import pandas.core.arrays._mixins
from pandas._libs.arrays import NDArrayBacked

_epoch = datetime.datetime(1970, 1, 1)


@pandas.core.dtypes.base.register_extension_dtype
class TimeDtype(pandas.core.dtypes.base.ExtensionDtype):
    """
    Extension dtype for time data.
    """

    name = "time"
    na_value = pandas.core.arrays.datetimelike.NaT
    kind = "o"
    names = None
    type = datetime.time

    def construct_array_type(self):
        return TimeArray

    @staticmethod
    def _datetime(scalar):
        if isinstance(scalar, datetime.time):
            return datetime.datetime.combine(_epoch, scalar)
        elif isinstance(scalar, str):
            # iso string
            h, m, s = map(float, scalar.split(":"))
            s, us = divmod(s, 1)
            return datetime.datetime(
                1970, 1, 1, int(h), int(m), int(s), int(us * 1000000)
            )


class TimeArray(
    pandas.core.arraylike.OpsMixin,
    pandas.core.arrays._mixins.NDArrayBackedExtensionArray,
):
    """
    Pandas array type containing time data
    """

    # Data stre stored as datetime64 values with a date of Jan 1, 1970

    dtype = TimeDtype()

    def __init__(self, values, copy: bool = False):
        values = pandas.core.construction.extract_array(values, extract_numpy=True)
        if copy:
            values = values.copy()
        super().__init__(values=values, dtype=values.dtype)

    @classmethod
    def _from_sequence(
        cls,
        scalars,
        *,
        dtype: Optional[pandas.core.arrays.datetimelike.Dtype] = None,
        copy=False
    ):
        if dtype is not None:
            assert isinstance(dtype, TimeDtype)
        array = numpy.array(
            [TimeDtype._datetime(scalar) for scalar in scalars], "M8[us]"
        )
        return TimeArray(array)

    def _box_func(self, x):
        return x.astype(datetime.datetime).time()

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            value = [datetime.datetime.combine(_epoch, v) for v in value]
        else:
            value = datetime.datetime.combine(_epoch, value)
        return super().__setitem__(key, value)

    def _cmp_method(self, other, op):
        if type(other) != type(self):
            return NotImplemented
        return op(self._ndarray, other._ndarray)
