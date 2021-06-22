# Copyright 2016 Google LLC
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

from __future__ import absolute_import

import pathlib
import os
import shutil

import nox


PYTYPE_VERSION = "pytype==2021.4.9"
BLACK_VERSION = "black==19.10b0"
BLACK_PATHS = ("docs", "google", "samples", "tests", "noxfile.py", "setup.py")

DEFAULT_PYTHON_VERSION = "3.8"
SYSTEM_TEST_PYTHON_VERSIONS = ["3.8"]
UNIT_TEST_PYTHON_VERSIONS = ["3.6", "3.7", "3.8", "3.9"]
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

# 'docfx' is excluded since it only needs to run in 'docs-presubmit'
nox.options.sessions = [
    "unit_noextras",
    "unit",
    "system",
    "snippets",
    "cover",
    "lint",
    "lint_setup_py",
    "blacken",
    "pytype",
    "docs",
]


def default(session, install_extras=True):
    """Default unit test session.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary the ``PATH`` can
    run the tests.
    """
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Install all test dependencies, then install local packages in-place.
    session.install(
        "mock",
        "pytest",
        "google-cloud-testutils",
        "pytest-cov",
        "freezegun",
        "-c",
        constraints_path,
    )

    install_target = ".[all]" if install_extras else "."
    session.install("-e", install_target, "-c", constraints_path)

    session.install("ipython", "-c", constraints_path)

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=google/cloud/bigquery",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS[-1])
def unit_noextras(session):
    """Run the unit test suite."""
    default(session, install_extras=False)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def pytype(session):
    """Run type checks."""
    # An indirect dependecy attrs==21.1.0 breaks the check, and installing a less
    # recent version avoids the error until a possibly better fix is found.
    # https://github.com/googleapis/python-bigquery/issues/655
    session.install("attrs==20.3.0")
    session.install("-e", ".[all]")
    session.install("ipython")
    session.install(PYTYPE_VERSION)
    session.run("pytype")


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system(session):
    """Run the system test suite."""

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Check the value of `RUN_SYSTEM_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_SYSTEM_TESTS", "true") == "false":
        session.skip("RUN_SYSTEM_TESTS is set to false, skipping")

    # Sanity check: Only run system tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable.")

    # Use pre-release gRPC for system tests.
    session.install("--pre", "grpcio", "-c", constraints_path)

    # Install all test dependencies, then install local packages in place.
    session.install(
        "mock", "pytest", "psutil", "google-cloud-testutils", "-c", constraints_path
    )
    if os.environ.get("GOOGLE_API_USE_CLIENT_CERTIFICATE", "") == "true":
        # mTLS test requires pyopenssl and latest google-cloud-storage
        session.install("google-cloud-storage", "pyopenssl")
    else:
        session.install("google-cloud-storage", "-c", constraints_path)

    # Data Catalog needed for the column ACL test with a real Policy Tag.
    session.install("google-cloud-datacatalog", "-c", constraints_path)

    session.install("-e", ".[all]", "-c", constraints_path)
    session.install("ipython", "-c", constraints_path)

    # Run py.test against the system tests.
    session.run("py.test", "--quiet", os.path.join("tests", "system"), *session.posargs)


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def snippets(session):
    """Run the snippets test suite."""

    # Check the value of `RUN_SNIPPETS_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_SNIPPETS_TESTS", "true") == "false":
        session.skip("RUN_SNIPPETS_TESTS is set to false, skipping")

    # Sanity check: Only run snippets tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable.")

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Install all test dependencies, then install local packages in place.
    session.install("mock", "pytest", "google-cloud-testutils", "-c", constraints_path)
    session.install("google-cloud-storage", "-c", constraints_path)
    session.install("grpcio", "-c", constraints_path)

    session.install("-e", ".[all]", "-c", constraints_path)

    # Run py.test against the snippets tests.
    # Skip tests in samples/snippets, as those are run in a different session
    # using the nox config from that directory.
    session.run("py.test", os.path.join("docs", "snippets.py"), *session.posargs)
    session.run(
        "py.test",
        "samples",
        "--ignore=samples/snippets",
        "--ignore=samples/geography",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")
    session.run("coverage", "erase")


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def prerelease_deps(session):
    """Run all tests with prerelease versions of dependencies installed.

    https://github.com/googleapis/python-bigquery/issues/95
    """
    # PyArrow prerelease packages are published to an alternative PyPI host.
    # https://arrow.apache.org/docs/python/install.html#installing-nightly-packages
    session.install(
        "--extra-index-url", "https://pypi.fury.io/arrow-nightlies/", "--pre", "pyarrow"
    )
    session.install("--pre", "grpcio", "pandas")
    session.install(
        "freezegun",
        "google-cloud-datacatalog",
        "google-cloud-storage",
        "google-cloud-testutils",
        "IPython",
        "mock",
        "psutil",
        "pytest",
        "pytest-cov",
    )
    session.install("-e", ".[all]")

    # Print out prerelease package versions.
    session.run("python", "-c", "import grpc; print(grpc.__version__)")
    session.run("python", "-c", "import pandas; print(pandas.__version__)")
    session.run("python", "-c", "import pyarrow; print(pyarrow.__version__)")

    # Run all tests, except a few samples tests which require extra dependencies.
    session.run("py.test", "tests/unit")
    session.run("py.test", "tests/system")
    session.run("py.test", "samples/tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """

    session.install("flake8", BLACK_VERSION)
    session.install("-e", ".")
    session.run("flake8", os.path.join("google", "cloud", "bigquery"))
    session.run("flake8", "tests")
    session.run("flake8", os.path.join("docs", "samples"))
    session.run("flake8", os.path.join("docs", "snippets.py"))
    session.run("black", "--check", *BLACK_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""

    session.install("docutils", "Pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black.
    Format code to uniform standard.
    """

    session.install(BLACK_VERSION)
    session.run("black", *BLACK_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    """Build the docs."""

    session.install("ipython", "recommonmark", "sphinx==4.0.1", "sphinx_rtd_theme")
    session.install("google-cloud-storage")
    session.install("-e", ".[all]")

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-W",  # warnings as errors
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".")
    session.install(
        "sphinx==4.0.1", "alabaster", "recommonmark", "gcp-sphinx-docfx-yaml"
    )

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-D",
        (
            "extensions=sphinx.ext.autodoc,"
            "sphinx.ext.autosummary,"
            "docfx_yaml.extension,"
            "sphinx.ext.intersphinx,"
            "sphinx.ext.coverage,"
            "sphinx.ext.napoleon,"
            "sphinx.ext.todo,"
            "sphinx.ext.viewcode,"
            "recommonmark"
        ),
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )
