# Copyright 2023 Google LLC
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

"""Shared helper functions for connecting BigQuery and pyarrow."""

from typing import Any

from google.cloud.bigquery.exceptions import LegacyPyarrowError

import packaging.version

_MIN_PYARROW_VERSION = packaging.version.Version("3.0.0")

try:
    import pyarrow
except ImportError as exc:  # pragma: NO COVER
    raise LegacyPyarrowError(
        f"pyarrow package not found. Install pyarrow version >= {_MIN_PYARROW_VERSION}."
    ) from exc

# Use 0.0.0, since it is earlier than any released version.
# Legacy versions also have the same property, but
# creating a LegacyVersion has been deprecated.
# https://github.com/pypa/packaging/issues/321
_pyarrow_version = packaging.version.parse(getattr(pyarrow, "__version__", "0.0.0"))

if _pyarrow_version < _MIN_PYARROW_VERSION:
    msg = (
        "Dependency pyarrow is outdated, please upgrade "
        f"it to version >= {_MIN_PYARROW_VERSION} (version found: {_pyarrow_version})."
    )
    raise LegacyPyarrowError(msg)


def pyarrow_datetime():
    return pyarrow.timestamp("us", tz=None)


def pyarrow_numeric():
    return pyarrow.decimal128(38, 9)


def pyarrow_bignumeric():
    # 77th digit is partial.
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types
    return pyarrow.decimal256(76, 38)


def pyarrow_time():
    return pyarrow.time64("us")


def pyarrow_timestamp():
    return pyarrow.timestamp("us", tz="UTC")


# This dictionary is duplicated in bigquery_storage/test/unite/test_reader.py
# When modifying it be sure to update it there as well.
# Note(todo!!): type "BIGNUMERIC"'s matching pyarrow type is added in _pandas_helpers.py
_BQ_TO_ARROW_SCALARS = {
    "BOOL": pyarrow.bool_,
    "BOOLEAN": pyarrow.bool_,
    "BYTES": pyarrow.binary,
    "DATE": pyarrow.date32,
    "DATETIME": pyarrow_datetime,
    "FLOAT": pyarrow.float64,
    "FLOAT64": pyarrow.float64,
    "GEOGRAPHY": pyarrow.string,
    "INT64": pyarrow.int64,
    "INTEGER": pyarrow.int64,
    "NUMERIC": pyarrow_numeric,
    "STRING": pyarrow.string,
    "TIME": pyarrow_time,
    "TIMESTAMP": pyarrow_timestamp,
    "BIGNUMERIC": pyarrow_bignumeric,
}

_ARROW_SCALAR_IDS_TO_BQ = {
    # https://arrow.apache.org/docs/python/api/datatypes.html#type-classes
    pyarrow.bool_().id: "BOOL",
    pyarrow.int8().id: "INT64",
    pyarrow.int16().id: "INT64",
    pyarrow.int32().id: "INT64",
    pyarrow.int64().id: "INT64",
    pyarrow.uint8().id: "INT64",
    pyarrow.uint16().id: "INT64",
    pyarrow.uint32().id: "INT64",
    pyarrow.uint64().id: "INT64",
    pyarrow.float16().id: "FLOAT64",
    pyarrow.float32().id: "FLOAT64",
    pyarrow.float64().id: "FLOAT64",
    pyarrow.time32("ms").id: "TIME",
    pyarrow.time64("ns").id: "TIME",
    pyarrow.timestamp("ns").id: "TIMESTAMP",
    pyarrow.date32().id: "DATE",
    pyarrow.date64().id: "DATETIME",  # because millisecond resolution
    pyarrow.binary().id: "BYTES",
    pyarrow.string().id: "STRING",  # also alias for pyarrow.utf8()
    # The exact scale and precision don't matter, see below.
    pyarrow.decimal128(38, scale=9).id: "NUMERIC",
    pyarrow.decimal256(76, scale=38).id: "BIGNUMERIC",
}


class PyarrowVersions:
    """Version comparisons for pyarrow package."""

    def __init__(self):
        self._installed_version = None

    @property
    def installed_version(self) -> packaging.version.Version:
        """Return the parsed version of pyarrow."""
        if self._installed_version is None:
            import pyarrow  # type: ignore

            self._installed_version = packaging.version.parse(
                # Use 0.0.0, since it is earlier than any released version.
                # Legacy versions also have the same property, but
                # creating a LegacyVersion has been deprecated.
                # https://github.com/pypa/packaging/issues/321
                getattr(pyarrow, "__version__", "0.0.0")
            )

        return self._installed_version

    @staticmethod
    def bq_to_arrow_scalars(bq_scalar: str):
        """
        Returns:
            The Arrow scalar type that the input BigQuery scalar type maps to.
            If cannot find the BigQuery scalar, return None.
        """
        return _BQ_TO_ARROW_SCALARS.get(bq_scalar)

    @staticmethod
    def arrow_scalar_ids_to_bq(arrow_scalar: any) -> str:
        """
        Returns:
            The BigQuery scalar type that the input arrow scalar type maps to.
            If cannot find the arrow scalar, return None.
        """
        return _ARROW_SCALAR_IDS_TO_BQ.get(arrow_scalar)

    @property
    def use_compliant_nested_type(self) -> bool:
        return self.installed_version.major >= 4

    def try_import(self, raise_if_error: bool = False) -> Any:
        """Verify that a recent enough version of pyarrow extra is
        installed.

        The function assumes that pyarrow extra is installed, and should thus
        be used in places where this assumption holds.

        Because `pip` can install an outdated version of this extra despite the
        constraints in `setup.py`, the calling code can use this helper to
        verify the version compatibility at runtime.

        Returns:
            The ``pyarrow`` module or ``None``.

        Raises:
            LegacyPyarrowError:
                If the pyarrow package is outdated and ``raise_if_error`` is ``True``.
        """
        try:
            import pyarrow
        except ImportError as exc:  # pragma: NO COVER
            if raise_if_error:
                raise LegacyPyarrowError(
                    f"pyarrow package not found. Install pyarrow version >= {_MIN_PYARROW_VERSION}."
                ) from exc
            return None

        if self.installed_version < _MIN_PYARROW_VERSION:
            if raise_if_error:
                msg = (
                    "Dependency pyarrow is outdated, please upgrade "
                    f"it to version >= {_MIN_PYARROW_VERSION} (version found: {self.installed_version})."
                )
                raise LegacyPyarrowError(msg)
            return None

        return pyarrow

PYARROW_VERSIONS = PyarrowVersions()
