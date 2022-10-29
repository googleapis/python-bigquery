# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
from google.cloud.bigquery import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bigquery_v2.services.model_service.client import ModelServiceClient
from google.cloud.bigquery_v2.services.model_service.async_client import ModelServiceAsyncClient

from google.cloud.bigquery_v2.types.encryption_config import EncryptionConfiguration
from google.cloud.bigquery_v2.types.model import DeleteModelRequest
from google.cloud.bigquery_v2.types.model import GetModelRequest
from google.cloud.bigquery_v2.types.model import ListModelsRequest
from google.cloud.bigquery_v2.types.model import ListModelsResponse
from google.cloud.bigquery_v2.types.model import Model
from google.cloud.bigquery_v2.types.model import PatchModelRequest
from google.cloud.bigquery_v2.types.model_reference import ModelReference
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlDataType
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlField
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlStructType
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlTableType
from google.cloud.bigquery_v2.types.table_reference import TableReference

__all__ = ('ModelServiceClient',
    'ModelServiceAsyncClient',
    'EncryptionConfiguration',
    'DeleteModelRequest',
    'GetModelRequest',
    'ListModelsRequest',
    'ListModelsResponse',
    'Model',
    'PatchModelRequest',
    'ModelReference',
    'StandardSqlDataType',
    'StandardSqlField',
    'StandardSqlStructType',
    'StandardSqlTableType',
    'TableReference',
)
