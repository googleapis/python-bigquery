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

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
version = "v2"

library = gapic.py_library(
    service="bigquery",
    version=version,
    bazel_target=f"//google/cloud/bigquery/{version}:bigquery-{version}-py",
    include_protos=True,
)

s.move(
    library,
    excludes=[
        "docs/index.rst",
        "README.rst",
        "noxfile.py",
        "setup.py",
        library / f"google/cloud/bigquery/__init__.py",
        library / f"google/cloud/bigquery/py.typed",
    ],
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=100,
    samples=True,
    microgenerator=True,
    split_system_tests=True,
)

# BigQuery has a custom multiprocessing note
s.move(
    templated_files,
    excludes=["noxfile.py", "docs/multiprocessing.rst", ".coveragerc"]
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

# python.py_samples()  # TODO: why doesn't this work here with Bazel?


s.replace(
    "docs/conf.py",
    r'\{"members": True\}',
    '{"members": True, "inherited-members": True}'
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
