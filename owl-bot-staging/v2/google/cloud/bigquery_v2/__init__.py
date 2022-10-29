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


from .services.model_service import ModelServiceClient
from .services.model_service import ModelServiceAsyncClient

from .types.encryption_config import EncryptionConfiguration
from .types.model import DeleteModelRequest
from .types.model import GetModelRequest
from .types.model import ListModelsRequest
from .types.model import ListModelsResponse
from .types.model import Model
from .types.model import PatchModelRequest
from .types.model_reference import ModelReference
from .types.standard_sql import StandardSqlDataType
from .types.standard_sql import StandardSqlField
from .types.standard_sql import StandardSqlStructType
from .types.standard_sql import StandardSqlTableType
from .types.table_reference import TableReference

__all__ = (
    'ModelServiceAsyncClient',
'DeleteModelRequest',
'EncryptionConfiguration',
'GetModelRequest',
'ListModelsRequest',
'ListModelsResponse',
'Model',
'ModelReference',
'ModelServiceClient',
'PatchModelRequest',
'StandardSqlDataType',
'StandardSqlField',
'StandardSqlStructType',
'StandardSqlTableType',
'TableReference',
)
