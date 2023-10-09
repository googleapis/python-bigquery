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

import unittest

import mock

try:
    import pyarrow
except ImportError:  # pragma: NO COVER
    pyarrow = None


@unittest.skipIf(pyarrow is None, "Requires `pyarrow`")
class TestPyarrowVersions(unittest.TestCase):
    def tearDown(self):
        from google.cloud.bigquery import _pyarrow_helpers

        # Reset any cached versions since it may not match reality.
        _pyarrow_helpers.PYARROW_VERSIONS._installed_version = None

    def _object_under_test(self):
        from google.cloud.bigquery import _pyarrow_helpers

        return _pyarrow_helpers.PyarrowVersions()

    def _call_try_import(self, **kwargs):
        from google.cloud.bigquery import _pyarrow_helpers

        _pyarrow_helpers.PYARROW_VERSIONS._installed_version = None
        return _pyarrow_helpers.PYARROW_VERSIONS.try_import(**kwargs)

    def test_try_import_raises_no_error_w_recent_pyarrow(self):
        from google.cloud.bigquery.exceptions import LegacyPyarrowError

        with mock.patch("pyarrow.__version__", new="5.0.0"):
            try:
                pyarrow = self._call_try_import(raise_if_error=True)
                self.assertIsNotNone(pyarrow)
            except LegacyPyarrowError:  # pragma: NO COVER
                self.fail("Legacy error raised with a non-legacy dependency version.")

    def test_try_import_returns_none_w_legacy_pyarrow(self):
        with mock.patch("pyarrow.__version__", new="2.0.0"):
            pyarrow = self._call_try_import()
            self.assertIsNone(pyarrow)

    def test_try_import_raises_error_w_legacy_pyarrow(self):
        from google.cloud.bigquery.exceptions import LegacyPyarrowError

        with mock.patch("pyarrow.__version__", new="2.0.0"):
            with self.assertRaises(LegacyPyarrowError):
                self._call_try_import(raise_if_error=True)

    def test_installed_version_returns_cached(self):
        versions = self._object_under_test()
        versions._installed_version = object()
        assert versions.installed_version is versions._installed_version

    def test_installed_version_returns_parsed_version(self):
        versions = self._object_under_test()

        with mock.patch("pyarrow.__version__", new="1.2.3"):
            version = versions.installed_version

        assert version.major == 1
        assert version.minor == 2
        assert version.micro == 3
