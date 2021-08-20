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

default_version = "v2"

for library in s.get_staging_dirs(default_version):
    # Do not expose ModelServiceClient and ModelServiceAsyncClient, as there
    # is no public API endpoint for the models service.
    s.replace(
        library / f"google/cloud/bigquery_{library.name}/__init__.py",
        r"from \.services\.model_service import ModelServiceClient",
        "",
    )

    s.replace(
        library / f"google/cloud/bigquery_{library.name}/__init__.py",
        r"from \.services\.model_service import ModelServiceAsyncClient",
        "",
    )

    s.replace(
        library / f"google/cloud/bigquery_{library.name}/__init__.py",
        r"""["']ModelServiceClient["'],""",
        "",
    )

    s.replace(
        library / f"google/cloud/bigquery_{library.name}/__init__.py",
        r"""["']ModelServiceAsyncClient["'],""",
        "",
    )

    # Adjust Model docstring so that Sphinx does not think that "predicted_" is
    # a reference to something, issuing a false warning.
    s.replace(
        library / f"google/cloud/bigquery_{library.name}/types/model.py",
        r'will have a "predicted_"',
        "will have a `predicted_`",
    )

    # Avoid breaking change due to change in field renames.
    # https://github.com/googleapis/python-bigquery/issues/319
    s.replace(
        library / f"google/cloud/bigquery_{library.name}/types/standard_sql.py",
        r"type_ ",
        "type ",
    )

    s.move(
        library,
        excludes=[
            "*.tar.gz",
            ".coveragerc",
            "docs/index.rst",
            f"docs/bigquery_{library.name}/*_service.rst",
            f"docs/bigquery_{library.name}/services.rst",
            "README.rst",
            "noxfile.py",
            "setup.py",
            f"scripts/fixup_bigquery_{library.name}_keywords.py",
            "google/cloud/bigquery/__init__.py",
            "google/cloud/bigquery/py.typed",
            # There are no public API endpoints for the generated ModelServiceClient,
            # thus there's no point in generating it and its tests.
            f"google/cloud/bigquery_{library.name}/services/**",
            f"tests/unit/gapic/bigquery_{library.name}/**",
        ],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=100, samples=True, microgenerator=True, split_system_tests=True,
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
