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

from functools import wraps
import pathlib
import os
import nox
import time


MYPY_VERSION = "mypy==1.6.1"
PYTYPE_VERSION = "pytype==2024.9.13"
BLACK_VERSION = "black==23.7.0"
BLACK_PATHS = (".",)

DEFAULT_PYTHON_VERSION = "3.9"
UNIT_TEST_PYTHON_VERSIONS = ["3.9", "3.11", "3.12", "3.13"]
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()


def _calculate_duration(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        total_seconds = round(end - start)
        hours = total_seconds // 3600  # Integer division to get hours
        remaining_seconds = total_seconds % 3600  # Modulo to find remaining seconds
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        human_time = f"{hours:}:{minutes:0>2}:{seconds:0>2}"
        print(f"Session ran in {total_seconds} seconds ({human_time})")
        return result

    return wrapper


# 'docfx' is excluded since it only needs to run in 'docs-presubmit'
nox.options.sessions = [
    "unit",
    "cover",
    "lint",
    "lint_setup_py",
    "blacken",
    "mypy",
    "pytype",
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
        "pytest",
        "google-cloud-testutils",
        "pytest-cov",
        "pytest-xdist",
        "freezegun",
        "-c",
        constraints_path,
    )
    # We have logic in the magics.py file that checks for whether 'bigquery_magics'
    # is imported OR not. If yes, we use a context object from that library.
    # If no, we use our own context object from magics.py. In order to exercise
    # that logic (and the associated tests) we avoid installing the [ipython] extra
    # which has a downstream effect of then avoiding installing bigquery_magics.
    if install_extras:  # run against all other UNIT_TEST_PYTHON_VERSIONS
        install_target = "."
    else:
        install_target = "."
    session.install("-e", install_target, "-c", constraints_path)

    # Test with some broken "extras" in case the user didn't install the extra
    # directly. For example, pandas-gbq is recommended for pandas features, but
    # we want to test that we fallback to the previous behavior. For context,
    # see internal document go/pandas-gbq-and-bigframes-redundancy.
    session.run("python", "-m", "pip", "freeze")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "-n=8",
        "--quiet",
        "-W default::PendingDeprecationWarning",
        "--cov=scripts.microgenerator",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        "tests/unit",
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
@_calculate_duration
def unit(session):
    """Run the unit test suite."""

    default(session)


@nox.session(python=DEFAULT_PYTHON_VERSION)
@_calculate_duration
def mypy(session):
    """Run type checks with mypy."""

    session.install("-e", ".")
    session.install(MYPY_VERSION)

    # Just install the dependencies' type info directly, since "mypy --install-types"
    # might require an additional pass.
    session.install(
        "types-protobuf",
        "types-python-dateutil",
        "types-requests",
        "types-setuptools",
    )
    session.run("python", "-m", "pip", "freeze")
    session.run("mypy", "-p", "google", "--show-traceback")


@nox.session(python=DEFAULT_PYTHON_VERSION)
@_calculate_duration
def pytype(session):
    """Run type checks with pytype."""
    # An indirect dependecy attrs==21.1.0 breaks the check, and installing a less
    # recent version avoids the error until a possibly better fix is found.
    # https://github.com/googleapis/python-bigquery/issues/655

    session.install("attrs==20.3.0")
    session.install("-e", ".")
    session.install(PYTYPE_VERSION)
    session.run("python", "-m", "pip", "freeze")
    # See https://github.com/google/pytype/issues/464
    session.run("pytype", "-P", ".", "scripts")


@nox.session(python=DEFAULT_PYTHON_VERSION)
@_calculate_duration
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """

    session.install("coverage", "pytest-cov")
    session.run("python", "-m", "pip", "freeze")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")
    session.run("coverage", "erase")


@nox.session(python=DEFAULT_PYTHON_VERSION)
@_calculate_duration
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """

    session.install("flake8", BLACK_VERSION)
    session.install("-e", ".")
    session.run("python", "-m", "pip", "freeze")
    session.run("flake8", os.path.join("scripts"))
    session.run("flake8", "tests")
    session.run("flake8", "benchmark")
    session.run("black", "--check", *BLACK_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
@_calculate_duration
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""

    session.install("docutils", "Pygments")
    session.run("python", "-m", "pip", "freeze")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
@_calculate_duration
def blacken(session):
    """Run black.
    Format code to uniform standard.
    """

    session.install(BLACK_VERSION)
    session.run("python", "-m", "pip", "freeze")
    session.run("black", *BLACK_PATHS)
