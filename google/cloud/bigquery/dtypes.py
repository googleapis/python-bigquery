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
from typing import Any, Optional, Sequence

import numpy
import packaging.version
import pandas
from pandas._libs import NaT
from pandas._libs.lib import is_integer
from pandas._typing import Scalar
import pandas.compat.numpy.function
import pandas.core.algorithms
import pandas.core.arrays
import pandas.core.dtypes.base
from pandas.core.dtypes.common import is_dtype_equal, is_list_like, pandas_dtype
import pandas.core.dtypes.dtypes
import pandas.core.dtypes.generic
import pandas.core.nanops

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
    def _cmp_method(self, other, op):  # pragma: NO COVER
        return NotImplemented

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

    @classmethod
    def _from_backing_data(cls, data):
        return cls(data, data.dtype)

    def __getitem__(self, index):
        value = self._ndarray[index]
        if is_integer(index):
            return self._box_func(value)
        return self.__class__(value, self._dtype)

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

    @classmethod
    def _concat_same_type(cls, to_concat, axis=0):
        dtypes = {str(x.dtype) for x in to_concat}
        if len(dtypes) != 1:
            raise ValueError("to_concat must have the same dtype (tz)", dtypes)

        new_values = [x._ndarray for x in to_concat]
        new_values = numpy.concatenate(new_values, axis=axis)
        return to_concat[0]._from_backing_data(new_values)  # type: ignore[arg-type]


#
###########################################################################


class _BaseDtype(pandas.core.dtypes.base.ExtensionDtype):
    na_value = NaT
    kind = "o"
    names = None

    @classmethod
    def construct_from_string(cls, name):
        if name != cls.name:
            raise TypeError()

        return cls()


class _BaseArray(OpsMixin, NDArrayBackedExtensionArray):
    def __init__(self, values, dtype=None, copy: bool = False):
        if not (
            isinstance(values, numpy.ndarray) and values.dtype == numpy.dtype("<M8[ns]")
        ):
            values = self.__ndarray(values)
        elif copy:
            values = values.copy()

        super().__init__(values=values, dtype=values.dtype)

    @classmethod
    def __ndarray(cls, scalars):
        return numpy.array(
            [None if scalar is None else cls._datetime(scalar) for scalar in scalars],
            "M8[ns]",
        )

    @classmethod
    def _from_sequence(cls, scalars, *, dtype=None, copy=False):
        if dtype is not None:
            assert dtype.__class__ is cls.dtype.__class__
        return cls(cls.__ndarray(scalars))

    _from_sequence_of_strings = _from_sequence

    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if is_dtype_equal(dtype, self.dtype):
            if not copy:
                return self
            else:
                return self.copy()

        return super().astype(dtype, copy=copy)

    def _cmp_method(self, other, op):
        if type(other) != type(self):
            return NotImplemented
        return op(self._ndarray, other._ndarray)

    def __setitem__(self, key, value):
        if is_list_like(value):
            _datetime = self._datetime
            value = [_datetime(v) for v in value]
        elif not pandas.isna(value):
            value = self._datetime(value)
        return super().__setitem__(key, value)

    def _from_factorized(self, unique, original):
        return self.__class__(unique)

    def isna(self):
        return pandas.isna(self._ndarray)

    def _validate_scalar(self, value):
        if pandas.isna(value):
            return None

        if not isinstance(value, self.dtype.type):
            raise ValueError(value)

        return value

    def take(
        self,
        indices: Sequence[int],
        *,
        allow_fill: bool = False,
        fill_value: Any = None,
    ):
        indices = numpy.asarray(indices, dtype=numpy.intp)
        data = self._ndarray
        if allow_fill:
            fill_value = self._validate_scalar(fill_value)
            fill_value = (
                numpy.datetime64()
                if fill_value is None
                else numpy.datetime64(self._datetime(fill_value))
            )
            if (indices < -1).any():
                raise ValueError(
                    "take called with negative indexes other than -1,"
                    " when a fill value is provided."
                )
        out = data.take(indices)
        if allow_fill:
            out[indices == -1] = fill_value

        return self.__class__(out)

    # TODO: provide implementations of dropna, fillna, unique,
    # factorize, argsort, searchsoeted for better performance over
    # abstract implementations.

    def any(
        self,
        *,
        axis: Optional[int] = None,
        out=None,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        pandas.compat.numpy.function.validate_any(
            (), {"out": out, "keepdims": keepdims}
        )
        result = pandas.core.nanops.nanany(self._ndarray, axis=axis, skipna=skipna)
        return result

    def all(
        self,
        *,
        axis: Optional[int] = None,
        out=None,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        pandas.compat.numpy.function.validate_all(
            (), {"out": out, "keepdims": keepdims}
        )
        result = pandas.core.nanops.nanall(self._ndarray, axis=axis, skipna=skipna)
        return result

    def min(
        self, *, axis: Optional[int] = None, skipna: bool = True, **kwargs
    ) -> Scalar:
        pandas.compat.numpy.function.validate_min((), kwargs)
        result = pandas.core.nanops.nanmin(
            values=self._ndarray, axis=axis, mask=self.isna(), skipna=skipna
        )
        return self._box_func(result)

    def max(
        self, *, axis: Optional[int] = None, skipna: bool = True, **kwargs
    ) -> Scalar:
        pandas.compat.numpy.function.validate_max((), kwargs)
        result = pandas.core.nanops.nanmax(
            values=self._ndarray, axis=axis, mask=self.isna(), skipna=skipna
        )
        return self._box_func(result)

    if pandas_release >= (1, 2):

        def median(
            self,
            *,
            axis: Optional[int] = None,
            out=None,
            overwrite_input: bool = False,
            keepdims: bool = False,
            skipna: bool = True,
        ):
            pandas.compat.numpy.function.validate_median(
                (),
                {"out": out, "overwrite_input": overwrite_input, "keepdims": keepdims},
            )
            result = pandas.core.nanops.nanmedian(
                self._ndarray, axis=axis, skipna=skipna
            )
            return self._box_func(result)


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
    _npepoch = numpy.datetime64(_epoch)

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

        try:
            return x.astype("<M8[us]").astype(datetime.datetime).time()
        except AttributeError:
            x = numpy.datetime64(x)
            return x.astype("<M8[us]").astype(datetime.datetime).time()

    __return_deltas = {"timedelta", "timedelta64", "timedelta64[ns]", "<m8", "<m8[ns]"}

    def astype(self, dtype, copy=True):
        deltas = self._ndarray - self._npepoch
        stype = str(dtype)
        if stype in self.__return_deltas:
            return deltas
        elif stype.startswith("timedelta64[") or stype.startswith("<m8["):
            return deltas.astype(dtype, copy=False)
        else:
            return super().astype(dtype, copy=copy)


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
        try:
            return x.astype("<M8[us]").astype(datetime.datetime).date()
        except AttributeError:
            x = numpy.datetime64(x)
            return x.astype("<M8[us]").astype(datetime.datetime).date()

    def astype(self, dtype, copy=True):
        stype = str(dtype)
        if stype.startswith("datetime"):
            if stype == "datetime" or stype == "datetime64":
                dtype = self._ndarray.dtype
            return self._ndarray.astype(dtype, copy=copy)
        elif stype.startswith("<M8"):
            if stype == "<M8":
                dtype = self._ndarray.dtype
            return self._ndarray.astype(dtype, copy=copy)

        return super().astype(dtype, copy=copy)
