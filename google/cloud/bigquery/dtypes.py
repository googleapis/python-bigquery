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
import operator

import numpy
import packaging.version
from pandas._libs import NaT
import pandas.core.dtypes.base
import pandas.core.dtypes.dtypes
import pandas.core.dtypes.generic

pandas_release = packaging.version.parse(pandas.__version__).release


###########################################################################
# To support old pandas versions, we provide forward ported
# versions. These versions are simpler and, in some cases, less featureful
# than the versions in the later versions of pandas.


def import_default(module_name, force=False, default=None):
    if default is None:
        return lambda func: import_default(module_name, force, func)

    if force:
        return default

    name = default.__name__
    try:
        module = __import__(module_name, {}, {}, [name])
    except ModuleNotFoundError:
        return default

    return getattr(module, name, default)


@import_default("pandas.core.arraylike")
class OpsMixin:
    def __eq__(self, other):
        return self._cmp_method(other, operator.eq)

    def __ne__(self, other):
        return self._cmp_method(other, operator.ne)

    def __lt__(self, other):
        return self._cmp_method(other, operator.lt)

    def __le__(self, other):
        return self._cmp_method(other, operator.le)

    def __gt__(self, other):
        return self._cmp_method(other, operator.gt)

    def __ge__(self, other):
        return self._cmp_method(other, operator.ge)


@import_default("pandas.core.arrays._mixins", pandas_release < (1, 3))
class NDArrayBackedExtensionArray(pandas.core.arrays.base.ExtensionArray):

    ndim = 1

    def __init__(self, values, dtype):
        assert isinstance(values, numpy.ndarray)
        assert values.ndim == 1
        self._ndarray = values
        self._dtype = dtype

    def __getitem__(self, index):
        value = self._ndarray[index]
        if isinstance(index, slice):
            return self.__class__(value, self._dtype)
        else:
            return self._box_func(value)

    def __setitem__(self, index, value):
        self._ndarray[index] = value

    def __len__(self):
        return len(self._ndarray)

    @property
    def shape(self):
        return self._ndarray.shape

    @property
    def ndim(self) -> int:
        return self._ndarray.ndim

    @property
    def size(self) -> int:
        return self._ndarray.size

    @property
    def nbytes(self) -> int:
        return self._ndarray.nbytes

    def copy(self):
        return self[:]

    def repeat(self, n):
        return self.__class__(self._ndarray.repeat(n), self._dtype)


#
###########################################################################


class _BaseDtype(pandas.core.dtypes.base.ExtensionDtype):
    na_value = NaT
    kind = "o"
    names = None
    if pandas_release >= (1, 3):
        # Enables series `dt` special properties :)
        dtype = numpy.datetime64

    @classmethod
    def construct_from_string(cls, name):
        if name != cls.name:
            raise TypeError()

        return cls()


class _BaseArray(OpsMixin, NDArrayBackedExtensionArray):
    def __init__(self, values, dtype=None, copy: bool = False):
        if not (
            isinstance(values, numpy.ndarray) and values.dtype == numpy.dtype("<M8[us]")
        ):
            values = self.__ndarray(values)
        elif copy:
            values = values.copy()

        super().__init__(values=values, dtype=values.dtype)

    @classmethod
    def __ndarray(cls, scalars):
        return numpy.array(
            [None if scalar is None else cls._datetime(scalar) for scalar in scalars],
            "M8[us]",
        )

    @classmethod
    def _from_sequence(cls, scalars, *, dtype=None, copy=False):
        if dtype is not None:
            assert dtype.__class__ is cls.dtype.__class__
        return cls(cls.__ndarray(scalars))

    _from_sequence_of_strings = _from_sequence

    def _cmp_method(self, other, op):
        if type(other) != type(self):
            return NotImplemented
        return op(self._ndarray, other._ndarray)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            _datetime = self._datetime
            value = [_datetime(v) for v in value]
        else:
            value = self._datetime(value)
        return super().__setitem__(key, value)


@pandas.core.dtypes.dtypes.register_extension_dtype
class TimeDtype(_BaseDtype):
    """
    Extension dtype for time data.
    """

    name = "time"
    type = datetime.time

    def construct_array_type(self):
        return TimeArray


class TimeArray(_BaseArray):
    """
    Pandas array type containing time data
    """

    # Data are stored as datetime64 values with a date of Jan 1, 1970

    dtype = TimeDtype()
    _epoch = datetime.datetime(1970, 1, 1)

    @classmethod
    def _datetime(cls, scalar):
        if isinstance(scalar, datetime.time):
            return datetime.datetime.combine(cls._epoch, scalar)
        elif isinstance(scalar, str):
            # iso string
            h, m, s = map(float, scalar.split(":"))
            s, us = divmod(s, 1)
            return datetime.datetime(
                1970, 1, 1, int(h), int(m), int(s), int(us * 1000000)
            )
        else:
            raise TypeError("Invalid value type", scalar)

    def _box_func(self, x):
        if pandas.isnull(x):
            return None
        return x.astype(datetime.datetime).time()


@pandas.core.dtypes.dtypes.register_extension_dtype
class DateDtype(_BaseDtype):
    """
    Extension dtype for time data.
    """

    name = "date"
    type = datetime.date

    def construct_array_type(self):
        return DateArray


class DateArray(_BaseArray):
    """
    Pandas array type containing date data
    """

    # Data are stored as datetime64 values with a date of Jan 1, 1970

    dtype = DateDtype()

    @staticmethod
    def _datetime(scalar):
        if isinstance(scalar, datetime.date):
            return datetime.datetime(scalar.year, scalar.month, scalar.day)
        elif isinstance(scalar, str):
            # iso string
            return datetime.datetime(*map(int, scalar.split("-")))
        else:
            raise TypeError("Invalid value type", scalar)

    def _box_func(self, x):
        if pandas.isnull(x):
            return None
        return x.astype(datetime.datetime).date()
