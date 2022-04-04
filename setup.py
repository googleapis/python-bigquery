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

import io
import os

import setuptools


# Package metadata.

name = "google-cloud-bigquery"
description = "Google BigQuery API client library"
version = "1.28.1"
# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 5 - Production/Stable"
dependencies = [
    'enum34; python_version < "3.4"',
    "google-api-core >= 1.31.5, <3.0.0dev,!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0",
    "google-cloud-core >= 1.4.1, < 3.0dev",
    "google-resumable-media >= 0.6.0, < 2.0dev",
    "six >=1.13.0,< 2.0.0dev",
]
extras = {
    "bqstorage": [
        "google-cloud-bigquery-storage >= 1.0.0, <2.0.0dev",
        # Due to an issue in pip's dependency resolver, the `grpc` extra is not
        # installed, even though `google-cloud-bigquery-storage` specifies it
        # as `google-api-core[grpc]`. We thus need to explicitly specify it here.
        # See: https://github.com/googleapis/python-bigquery/issues/83 The
        # grpc.Channel.close() method isn't added until 1.32.0.
        # https://github.com/grpc/grpc/pull/15254
        "grpcio >= 1.32.0, < 2.0dev",
        "pyarrow >= 1.0.0, < 2.0dev",
    ],
    "pandas": ["pandas>=0.23.0"],
    "pyarrow": [
        # pyarrow 1.0.0 is required for the use of timestamp_as_object keyword.
        "pyarrow >= 1.0.0, < 2.0de ; python_version>='3.5'",
        "pyarrow >= 0.16.0, < 0.17.0dev ; python_version<'3.5'",
    ],
    "tqdm": ["tqdm >= 4.7.4, <5.0.0dev"],
    "fastparquet": [
        "fastparquet",
        "python-snappy",
        # llvmlite >= 0.32.0 cannot be installed on Python 3.5 and below
        # (building the wheel fails), thus needs to be restricted.
        # See: https://github.com/googleapis/python-bigquery/issues/78
        "llvmlite<=0.34.0;python_version>='3.6'",
        "llvmlite<=0.31.0;python_version<'3.6'",
    ],
    "opentelemetry": [
        "opentelemetry-api==0.9b0",
        "opentelemetry-sdk==0.9b0",
        "opentelemetry-instrumentation==0.9b0 ",
    ],
}

all_extras = []

for extra in extras:
    if extra in (
        # Skip fastparquet from "all" because it is redundant with pyarrow and
        # creates a dependency on pre-release versions of numpy. See:
        # https://github.com/googleapis/google-cloud-python/issues/8549
        "fastparquet",
    ):
        continue
    all_extras.extend(extras[extra])

extras["all"] = all_extras

# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

# Only include packages under the 'google' namespace. Do not include tests,
# benchmarks, etc.
packages = [
    package for package in setuptools.find_packages() if package.startswith("google")
]

# Determine which namespaces are needed.
namespaces = ["google"]
if "google.cloud" in packages:
    namespaces.append("google.cloud")


setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    license="Apache 2.0",
    url="https://github.com/googleapis/python-bigquery",
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    platforms="Posix; MacOS X; Windows",
    packages=packages,
    namespace_packages=namespaces,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    include_package_data=True,
    zip_safe=False,
)
