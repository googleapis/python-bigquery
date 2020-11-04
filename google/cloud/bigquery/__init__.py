# Copyright 2015 Google LLC
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

"""Google BigQuery API wrapper.

The main concepts with this API are:

- :class:`~google.cloud.bigquery.client.Client` manages connections to the
  BigQuery API. Use the client methods to run jobs (such as a
  :class:`~google.cloud.bigquery.job.QueryJob` via
  :meth:`~google.cloud.bigquery.client.Client.query`) and manage resources.

- :class:`~google.cloud.bigquery.dataset.Dataset` represents a
  collection of tables.

- :class:`~google.cloud.bigquery.table.Table` represents a single "relation".
"""


from google.cloud.bigquery import version as bigquery_version

__version__ = bigquery_version.__version__

from google.cloud.bigquery.client import Client
from google.cloud.bigquery.dataset import AccessEntry
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery import enums
from google.cloud.bigquery.enums import SqlTypeNames
from google.cloud.bigquery.enums import StandardSqlDataTypes
from google.cloud.bigquery.external_config import ExternalConfig
from google.cloud.bigquery.external_config import BigtableOptions
from google.cloud.bigquery.external_config import BigtableColumnFamily
from google.cloud.bigquery.external_config import BigtableColumn
from google.cloud.bigquery.external_config import CSVOptions
from google.cloud.bigquery.external_config import GoogleSheetsOptions
from google.cloud.bigquery.external_config import ExternalSourceFormat
from google.cloud.bigquery.job import Compression
from google.cloud.bigquery.job import CopyJob
from google.cloud.bigquery.job import CopyJobConfig
from google.cloud.bigquery.job import CreateDisposition
from google.cloud.bigquery.job import DestinationFormat
from google.cloud.bigquery.job import Encoding
from google.cloud.bigquery.job import ExtractJob
from google.cloud.bigquery.job import ExtractJobConfig
from google.cloud.bigquery.job import LoadJob
from google.cloud.bigquery.job import LoadJobConfig
from google.cloud.bigquery.job import QueryJob
from google.cloud.bigquery.job import QueryJobConfig
from google.cloud.bigquery.job import QueryPriority
from google.cloud.bigquery.job import SchemaUpdateOption
from google.cloud.bigquery.job import SourceFormat
from google.cloud.bigquery.job import UnknownJob
from google.cloud.bigquery.job import WriteDisposition
from google.cloud.bigquery.model import Model
from google.cloud.bigquery.model import ModelReference
from google.cloud.bigquery.query import ArrayQueryParameter
from google.cloud.bigquery.query import ScalarQueryParameter
from google.cloud.bigquery.query import StructQueryParameter
from google.cloud.bigquery.query import UDFResource
from google.cloud.bigquery.retry import DEFAULT_RETRY
from google.cloud.bigquery.routine import Routine
from google.cloud.bigquery.routine import RoutineArgument
from google.cloud.bigquery.routine import RoutineReference
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import PartitionRange
from google.cloud.bigquery.table import RangePartitioning
from google.cloud.bigquery.table import Row
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.table import TableReference
from google.cloud.bigquery.table import TimePartitioningType
from google.cloud.bigquery.table import TimePartitioning
from google.cloud.bigquery.encryption_configuration import EncryptionConfiguration

__all__ = [
    "__version__",
    "Client",
    # Queries
    "QueryJob",
    "QueryJobConfig",
    "ArrayQueryParameter",
    "ScalarQueryParameter",
    "StructQueryParameter",
    # Datasets
    "Dataset",
    "DatasetReference",
    "AccessEntry",
    # Tables
    "Table",
    "TableReference",
    "PartitionRange",
    "RangePartitioning",
    "Row",
    "TimePartitioning",
    "TimePartitioningType",
    # Jobs
    "CopyJob",
    "CopyJobConfig",
    "ExtractJob",
    "ExtractJobConfig",
    "LoadJob",
    "LoadJobConfig",
    "UnknownJob",
    # Models
    "Model",
    "ModelReference",
    # Routines
    "Routine",
    "RoutineArgument",
    "RoutineReference",
    # Shared helpers
    "SchemaField",
    "UDFResource",
    "ExternalConfig",
    "BigtableOptions",
    "BigtableColumnFamily",
    "BigtableColumn",
    "CSVOptions",
    "GoogleSheetsOptions",
    "DEFAULT_RETRY",
    # Enum Constants
    "enums",
    "Compression",
    "CreateDisposition",
    "DestinationFormat",
    "ExternalSourceFormat",
    "Encoding",
    "QueryPriority",
    "SchemaUpdateOption",
    "SourceFormat",
    "SqlTypeNames",
    "StandardSqlDataTypes",
    "WriteDisposition",
    # EncryptionConfiguration
    "EncryptionConfiguration",
]


def load_ipython_extension(ipython):
    """Called by IPython when this module is loaded as an IPython extension."""
    from google.cloud.bigquery.magics.magics import _cell_magic

    ipython.register_magic_function(
        _cell_magic, magic_kind="cell", magic_name="bigquery"
    )
