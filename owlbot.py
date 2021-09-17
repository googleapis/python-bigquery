# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""
import textwrap

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=100,
    samples=True,
    microgenerator=True,
    split_system_tests=True,
    intersphinx_dependencies={
        "pandas": "http://pandas.pydata.org/pandas-docs/dev",
        "geopandas": "https://geopandas.org/",
    },
)

# BigQuery has a custom multiprocessing note
s.move(
    templated_files,
    excludes=[
        "noxfile.py",
        "docs/multiprocessing.rst",
        ".coveragerc",
        # Include custom SNIPPETS_TESTS job for performance.
        # https://github.com/googleapis/python-bigquery/issues/191
        ".kokoro/presubmit/presubmit.cfg",
        # Group all renovate PRs together. If this works well, remove this and
        # update the shared templates (possibly with configuration option to
        # py_library.)
        "renovate.json",
    ],
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

s.replace(
    "docs/conf.py",
    r'\{"members": True\}',
    '{"members": True, "inherited-members": True}',
)

# ----------------------------------------------------------------------------
# pytype-related changes
# ----------------------------------------------------------------------------

# Add .pytype to .gitignore
s.replace(".gitignore", r"\.pytest_cache", "\\g<0>\n.pytype")

# Add pytype config to setup.cfg
s.replace(
    "setup.cfg",
    r"universal = 1",
    textwrap.dedent(
        """    \\g<0>

    [pytype]
    python_version = 3.8
    inputs =
        google/cloud/
    exclude =
        tests/
    output = .pytype/
    disable =
        # There's some issue with finding some pyi files, thus disabling.
        # The issue https://github.com/google/pytype/issues/150 is closed, but the
        # error still occurs for some reason.
        pyi-error"""
    ),
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
