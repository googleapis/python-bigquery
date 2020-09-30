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

# One of the generated tests fails because of an extra newline in string
# representation (a non-essential reason), let's skip it for the time being.
s.replace(
    "tests/unit/gapic/bigquery_v2/test_model_service.py",
    r"def test_list_models_flattened\(\):",
    (
        '@pytest.mark.skip('
        'reason="This test currently fails because of an extra newline in repr()")'
        '\n\g<0>'
    ),
)

# Adjust Model docstring so that Sphinx does not think that "predicted_" is
# a reference to something, issuing a false warning.
s.replace(
    "google/cloud/bigquery_v2/types/model.py",
    r'will have a "predicted_"',
    "will have a `predicted_`",
)

s.replace(
    "docs/conf.py",
    r'\{"members": True\}',
    '{"members": True, "inherited-members": True}'
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
