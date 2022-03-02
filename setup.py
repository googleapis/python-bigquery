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

# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 5 - Production/Stable"
pyarrow_dep = ["pyarrow >=3.0.0, <8.0dev"]
dependencies = [
    "grpcio >= 1.38.1, < 2.0dev",  # https://github.com/googleapis/python-bigquery/issues/695
    # NOTE: Maintainers, please do not require google-api-core>=2.x.x
    # Until this issue is closed
    # https://github.com/googleapis/google-cloud-python/issues/10566
    "google-api-core[grpc] >= 1.29.0, <3.0.0dev",
    "proto-plus >= 1.10.0",
    # NOTE: Maintainers, please do not require google-cloud-core>=2.x.x
    # Until this issue is closed
    # https://github.com/googleapis/google-cloud-python/issues/10566
    "google-cloud-core >= 1.4.1, <3.0.0dev",
    "google-resumable-media >= 0.6.0, < 3.0dev",
    "packaging >= 14.3",
    "protobuf >= 3.12.0",
    "python-dateutil >= 2.7.2, <3.0dev",
    "requests >= 2.18.0, < 3.0.0dev",
]
extras = {
    "bqstorage": [
        "google-cloud-bigquery-storage >= 2.0.0, <3.0.0dev",
        # Due to an issue in pip's dependency resolver, the `grpc` extra is not
        # installed, even though `google-cloud-bigquery-storage` specifies it
        # as `google-api-core[grpc]`. We thus need to explicitly specify it here.
        # See: https://github.com/googleapis/python-bigquery/issues/83 The
        # grpc.Channel.close() method isn't added until 1.32.0.
        # https://github.com/grpc/grpc/pull/15254
        "grpcio >= 1.38.1, < 2.0dev",
    ]
    + pyarrow_dep,
    "geopandas": ["geopandas>=0.9.0, <1.0dev", "Shapely>=1.6.0, <2.0dev"],
    "pandas": ["pandas>=0.24.2"] + pyarrow_dep,
    "bignumeric_type": pyarrow_dep,
    "ipython": ["ipython>=7.0.1,!=8.1.0"],
    "tqdm": ["tqdm >= 4.7.4, <5.0.0dev"],
    "opentelemetry": [
        "opentelemetry-api >= 1.1.0",
        "opentelemetry-sdk >= 1.1.0",
        "opentelemetry-instrumentation >= 0.20b0",
    ],
}

all_extras = []

for extra in extras:
    # Exclude this extra from all to avoid overly strict dependencies on core
    # libraries such as pyarrow.
    # https://github.com/googleapis/python-bigquery/issues/563
    if extra in {"bignumeric_type"}:
        continue
    all_extras.extend(extras[extra])

extras["all"] = all_extras

# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

version = {}
with open(os.path.join(package_root, "google/cloud/bigquery/version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

# Only include packages under the 'google' namespace. Do not include tests,
# benchmarks, etc.
packages = [
    package
    for package in setuptools.PEP420PackageFinder.find()
    if package.startswith("google")
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    platforms="Posix; MacOS X; Windows",
    packages=packages,
    namespace_packages=namespaces,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=3.6, <3.11",
    include_package_data=True,
    zip_safe=False,
)
