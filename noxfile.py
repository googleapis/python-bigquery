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


BLACK_VERSION = "black==19.10b0"
BLACK_PATHS = ("docs", "google", "samples", "tests", "noxfile.py", "setup.py")
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()


def default(session):
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

    session.install("-e", ".[all]", "-c", constraints_path)

    session.install("ipython", "-c", constraints_path)

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=google.cloud.bigquery",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )


@nox.session(python=["3.6", "3.7", "3.8"])
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=["3.8"])
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
    session.install("google-cloud-storage", "-c", constraints_path)

    session.install("-e", ".[all]", "-c", constraints_path)
    session.install("ipython", "-c", constraints_path)

    # Run py.test against the system tests.
    session.run(
        "py.test", "--quiet", os.path.join("tests", "system.py"), *session.posargs
    )


@nox.session(python=["3.8"])
def snippets(session):
    """Run the snippets test suite."""

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Sanity check: Only run snippets tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable.")

    # Install all test dependencies, then install local packages in place.
    session.install("mock", "pytest", "google-cloud-testutils", "-c", constraints_path)
    session.install("google-cloud-storage", "-c", constraints_path)
    session.install("grpcio", "-c", constraints_path)

    session.install("-e", ".[all]", "-c", constraints_path)

    # Run py.test against the snippets tests.
    # Skip tests in samples/snippets, as those are run in a different session
    # using the nox config from that directory.
    session.run("py.test", os.path.join("docs", "snippets.py"), *session.posargs)
    session.run("py.test", "samples", "--ignore=samples/snippets", *session.posargs)


@nox.session(python="3.8")
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")
    session.run("coverage", "erase")


@nox.session(python="3.8")
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


@nox.session(python="3.8")
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""

    session.install("docutils", "Pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python="3.6")
def blacken(session):
    """Run black.
    Format code to uniform standard.

    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
    """
    session.install(BLACK_VERSION)
    session.run("black", *BLACK_PATHS)


@nox.session(python="3.8")
def docs(session):
    """Build the docs."""

    session.install("ipython", "recommonmark", "sphinx", "sphinx_rtd_theme")
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


@nox.session(python="3.8")
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".")
    session.install("sphinx", "alabaster", "recommonmark", "sphinx-docfx-yaml")

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
