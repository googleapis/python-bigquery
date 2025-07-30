# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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


from google.cloud.bigquery_v2.services.dataset_service.client import (
    DatasetServiceClient,
)
from google.cloud.bigquery_v2.services.job_service.client import JobServiceClient
from google.cloud.bigquery_v2.services.model_service.client import ModelServiceClient
from google.cloud.bigquery_v2.services.project_service.client import (
    ProjectServiceClient,
)
from google.cloud.bigquery_v2.services.routine_service.client import (
    RoutineServiceClient,
)
from google.cloud.bigquery_v2.services.row_access_policy_service.client import (
    RowAccessPolicyServiceClient,
)
from google.cloud.bigquery_v2.services.table_service.client import TableServiceClient

from google.cloud.bigquery_v2.types.biglake_config import BigLakeConfiguration
from google.cloud.bigquery_v2.types.clustering import Clustering
from google.cloud.bigquery_v2.types.data_format_options import DataFormatOptions
from google.cloud.bigquery_v2.types.dataset import Access
from google.cloud.bigquery_v2.types.dataset import Dataset
from google.cloud.bigquery_v2.types.dataset import DatasetAccessEntry
from google.cloud.bigquery_v2.types.dataset import DatasetList
from google.cloud.bigquery_v2.types.dataset import DeleteDatasetRequest
from google.cloud.bigquery_v2.types.dataset import GcpTag
from google.cloud.bigquery_v2.types.dataset import GetDatasetRequest
from google.cloud.bigquery_v2.types.dataset import InsertDatasetRequest
from google.cloud.bigquery_v2.types.dataset import LinkedDatasetMetadata
from google.cloud.bigquery_v2.types.dataset import LinkedDatasetSource
from google.cloud.bigquery_v2.types.dataset import ListDatasetsRequest
from google.cloud.bigquery_v2.types.dataset import ListFormatDataset
from google.cloud.bigquery_v2.types.dataset import UndeleteDatasetRequest
from google.cloud.bigquery_v2.types.dataset import UpdateOrPatchDatasetRequest
from google.cloud.bigquery_v2.types.dataset_reference import DatasetReference
from google.cloud.bigquery_v2.types.decimal_target_types import DecimalTargetType
from google.cloud.bigquery_v2.types.encryption_config import EncryptionConfiguration
from google.cloud.bigquery_v2.types.error import ErrorProto
from google.cloud.bigquery_v2.types.external_catalog_dataset_options import (
    ExternalCatalogDatasetOptions,
)
from google.cloud.bigquery_v2.types.external_catalog_table_options import (
    ExternalCatalogTableOptions,
)
from google.cloud.bigquery_v2.types.external_catalog_table_options import SerDeInfo
from google.cloud.bigquery_v2.types.external_catalog_table_options import (
    StorageDescriptor,
)
from google.cloud.bigquery_v2.types.external_data_config import AvroOptions
from google.cloud.bigquery_v2.types.external_data_config import BigtableColumn
from google.cloud.bigquery_v2.types.external_data_config import BigtableColumnFamily
from google.cloud.bigquery_v2.types.external_data_config import BigtableOptions
from google.cloud.bigquery_v2.types.external_data_config import CsvOptions
from google.cloud.bigquery_v2.types.external_data_config import (
    ExternalDataConfiguration,
)
from google.cloud.bigquery_v2.types.external_data_config import GoogleSheetsOptions
from google.cloud.bigquery_v2.types.external_data_config import JsonOptions
from google.cloud.bigquery_v2.types.external_data_config import ParquetOptions
from google.cloud.bigquery_v2.types.external_dataset_reference import (
    ExternalDatasetReference,
)
from google.cloud.bigquery_v2.types.file_set_specification_type import FileSetSpecType
from google.cloud.bigquery_v2.types.hive_partitioning import HivePartitioningOptions
from google.cloud.bigquery_v2.types.job import CancelJobRequest
from google.cloud.bigquery_v2.types.job import DeleteJobRequest
from google.cloud.bigquery_v2.types.job import GetJobRequest
from google.cloud.bigquery_v2.types.job import GetQueryResultsRequest
from google.cloud.bigquery_v2.types.job import GetQueryResultsResponse
from google.cloud.bigquery_v2.types.job import InsertJobRequest
from google.cloud.bigquery_v2.types.job import Job
from google.cloud.bigquery_v2.types.job import JobCancelResponse
from google.cloud.bigquery_v2.types.job import JobList
from google.cloud.bigquery_v2.types.job import ListFormatJob
from google.cloud.bigquery_v2.types.job import ListJobsRequest
from google.cloud.bigquery_v2.types.job import PostQueryRequest
from google.cloud.bigquery_v2.types.job import QueryRequest
from google.cloud.bigquery_v2.types.job import QueryResponse
from google.cloud.bigquery_v2.types.job_config import ConnectionProperty
from google.cloud.bigquery_v2.types.job_config import DestinationTableProperties
from google.cloud.bigquery_v2.types.job_config import JobConfiguration
from google.cloud.bigquery_v2.types.job_config import JobConfigurationExtract
from google.cloud.bigquery_v2.types.job_config import JobConfigurationLoad
from google.cloud.bigquery_v2.types.job_config import JobConfigurationQuery
from google.cloud.bigquery_v2.types.job_config import JobConfigurationTableCopy
from google.cloud.bigquery_v2.types.job_config import ScriptOptions
from google.cloud.bigquery_v2.types.job_creation_reason import JobCreationReason
from google.cloud.bigquery_v2.types.job_reference import JobReference
from google.cloud.bigquery_v2.types.job_stats import BiEngineReason
from google.cloud.bigquery_v2.types.job_stats import BiEngineStatistics
from google.cloud.bigquery_v2.types.job_stats import CopyJobStatistics
from google.cloud.bigquery_v2.types.job_stats import DataMaskingStatistics
from google.cloud.bigquery_v2.types.job_stats import DmlStats
from google.cloud.bigquery_v2.types.job_stats import ExplainQueryStage
from google.cloud.bigquery_v2.types.job_stats import ExplainQueryStep
from google.cloud.bigquery_v2.types.job_stats import ExportDataStatistics
from google.cloud.bigquery_v2.types.job_stats import ExternalServiceCost
from google.cloud.bigquery_v2.types.job_stats import HighCardinalityJoin
from google.cloud.bigquery_v2.types.job_stats import IndexUnusedReason
from google.cloud.bigquery_v2.types.job_stats import InputDataChange
from google.cloud.bigquery_v2.types.job_stats import JobStatistics
from google.cloud.bigquery_v2.types.job_stats import JobStatistics2
from google.cloud.bigquery_v2.types.job_stats import JobStatistics3
from google.cloud.bigquery_v2.types.job_stats import JobStatistics4
from google.cloud.bigquery_v2.types.job_stats import LoadQueryStatistics
from google.cloud.bigquery_v2.types.job_stats import MaterializedView
from google.cloud.bigquery_v2.types.job_stats import MaterializedViewStatistics
from google.cloud.bigquery_v2.types.job_stats import MetadataCacheStatistics
from google.cloud.bigquery_v2.types.job_stats import MlStatistics
from google.cloud.bigquery_v2.types.job_stats import PartitionSkew
from google.cloud.bigquery_v2.types.job_stats import PerformanceInsights
from google.cloud.bigquery_v2.types.job_stats import QueryInfo
from google.cloud.bigquery_v2.types.job_stats import QueryTimelineSample
from google.cloud.bigquery_v2.types.job_stats import RowLevelSecurityStatistics
from google.cloud.bigquery_v2.types.job_stats import ScriptStatistics
from google.cloud.bigquery_v2.types.job_stats import SearchStatistics
from google.cloud.bigquery_v2.types.job_stats import SparkStatistics
from google.cloud.bigquery_v2.types.job_stats import StagePerformanceChangeInsight
from google.cloud.bigquery_v2.types.job_stats import StagePerformanceStandaloneInsight
from google.cloud.bigquery_v2.types.job_stats import StoredColumnsUsage
from google.cloud.bigquery_v2.types.job_stats import TableMetadataCacheUsage
from google.cloud.bigquery_v2.types.job_stats import VectorSearchStatistics
from google.cloud.bigquery_v2.types.job_stats import ReservationEdition
from google.cloud.bigquery_v2.types.job_status import JobStatus
from google.cloud.bigquery_v2.types.json_extension import JsonExtension
from google.cloud.bigquery_v2.types.location_metadata import LocationMetadata
from google.cloud.bigquery_v2.types.managed_table_type import ManagedTableType
from google.cloud.bigquery_v2.types.map_target_type import MapTargetType
from google.cloud.bigquery_v2.types.model import DeleteModelRequest
from google.cloud.bigquery_v2.types.model import GetModelRequest
from google.cloud.bigquery_v2.types.model import ListModelsRequest
from google.cloud.bigquery_v2.types.model import ListModelsResponse
from google.cloud.bigquery_v2.types.model import Model
from google.cloud.bigquery_v2.types.model import PatchModelRequest
from google.cloud.bigquery_v2.types.model import RemoteModelInfo
from google.cloud.bigquery_v2.types.model import TransformColumn
from google.cloud.bigquery_v2.types.model_reference import ModelReference
from google.cloud.bigquery_v2.types.partitioning_definition import PartitionedColumn
from google.cloud.bigquery_v2.types.partitioning_definition import (
    PartitioningDefinition,
)
from google.cloud.bigquery_v2.types.privacy_policy import AggregationThresholdPolicy
from google.cloud.bigquery_v2.types.privacy_policy import DifferentialPrivacyPolicy
from google.cloud.bigquery_v2.types.privacy_policy import JoinRestrictionPolicy
from google.cloud.bigquery_v2.types.privacy_policy import PrivacyPolicy
from google.cloud.bigquery_v2.types.project import GetServiceAccountRequest
from google.cloud.bigquery_v2.types.project import GetServiceAccountResponse
from google.cloud.bigquery_v2.types.query_parameter import QueryParameter
from google.cloud.bigquery_v2.types.query_parameter import QueryParameterStructType
from google.cloud.bigquery_v2.types.query_parameter import QueryParameterType
from google.cloud.bigquery_v2.types.query_parameter import QueryParameterValue
from google.cloud.bigquery_v2.types.query_parameter import RangeValue
from google.cloud.bigquery_v2.types.range_partitioning import RangePartitioning
from google.cloud.bigquery_v2.types.restriction_config import RestrictionConfig
from google.cloud.bigquery_v2.types.routine import DeleteRoutineRequest
from google.cloud.bigquery_v2.types.routine import ExternalRuntimeOptions
from google.cloud.bigquery_v2.types.routine import GetRoutineRequest
from google.cloud.bigquery_v2.types.routine import InsertRoutineRequest
from google.cloud.bigquery_v2.types.routine import ListRoutinesRequest
from google.cloud.bigquery_v2.types.routine import ListRoutinesResponse
from google.cloud.bigquery_v2.types.routine import PatchRoutineRequest
from google.cloud.bigquery_v2.types.routine import PythonOptions
from google.cloud.bigquery_v2.types.routine import Routine
from google.cloud.bigquery_v2.types.routine import SparkOptions
from google.cloud.bigquery_v2.types.routine import UpdateRoutineRequest
from google.cloud.bigquery_v2.types.routine_reference import RoutineReference
from google.cloud.bigquery_v2.types.row_access_policy import (
    BatchDeleteRowAccessPoliciesRequest,
)
from google.cloud.bigquery_v2.types.row_access_policy import (
    CreateRowAccessPolicyRequest,
)
from google.cloud.bigquery_v2.types.row_access_policy import (
    DeleteRowAccessPolicyRequest,
)
from google.cloud.bigquery_v2.types.row_access_policy import GetRowAccessPolicyRequest
from google.cloud.bigquery_v2.types.row_access_policy import (
    ListRowAccessPoliciesRequest,
)
from google.cloud.bigquery_v2.types.row_access_policy import (
    ListRowAccessPoliciesResponse,
)
from google.cloud.bigquery_v2.types.row_access_policy import RowAccessPolicy
from google.cloud.bigquery_v2.types.row_access_policy import (
    UpdateRowAccessPolicyRequest,
)
from google.cloud.bigquery_v2.types.row_access_policy_reference import (
    RowAccessPolicyReference,
)
from google.cloud.bigquery_v2.types.session_info import SessionInfo
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlDataType
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlField
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlStructType
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlTableType
from google.cloud.bigquery_v2.types.system_variable import SystemVariables
from google.cloud.bigquery_v2.types.table import CloneDefinition
from google.cloud.bigquery_v2.types.table import DeleteTableRequest
from google.cloud.bigquery_v2.types.table import ForeignViewDefinition
from google.cloud.bigquery_v2.types.table import GetTableRequest
from google.cloud.bigquery_v2.types.table import InsertTableRequest
from google.cloud.bigquery_v2.types.table import ListFormatTable
from google.cloud.bigquery_v2.types.table import ListFormatView
from google.cloud.bigquery_v2.types.table import ListTablesRequest
from google.cloud.bigquery_v2.types.table import MaterializedViewDefinition
from google.cloud.bigquery_v2.types.table import MaterializedViewStatus
from google.cloud.bigquery_v2.types.table import SnapshotDefinition
from google.cloud.bigquery_v2.types.table import Streamingbuffer
from google.cloud.bigquery_v2.types.table import Table
from google.cloud.bigquery_v2.types.table import TableList
from google.cloud.bigquery_v2.types.table import TableReplicationInfo
from google.cloud.bigquery_v2.types.table import UpdateOrPatchTableRequest
from google.cloud.bigquery_v2.types.table import ViewDefinition
from google.cloud.bigquery_v2.types.table_constraints import ColumnReference
from google.cloud.bigquery_v2.types.table_constraints import ForeignKey
from google.cloud.bigquery_v2.types.table_constraints import PrimaryKey
from google.cloud.bigquery_v2.types.table_constraints import TableConstraints
from google.cloud.bigquery_v2.types.table_reference import TableReference
from google.cloud.bigquery_v2.types.table_schema import DataPolicyOption
from google.cloud.bigquery_v2.types.table_schema import ForeignTypeInfo
from google.cloud.bigquery_v2.types.table_schema import TableFieldSchema
from google.cloud.bigquery_v2.types.table_schema import TableSchema
from google.cloud.bigquery_v2.types.time_partitioning import TimePartitioning
from google.cloud.bigquery_v2.types.udf_resource import UserDefinedFunctionResource

__all__ = (
    "DatasetServiceClient",
    "JobServiceClient",
    "ModelServiceClient",
    "ProjectServiceClient",
    "RoutineServiceClient",
    "RowAccessPolicyServiceClient",
    "TableServiceClient",
    "BigLakeConfiguration",
    "Clustering",
    "DataFormatOptions",
    "Access",
    "Dataset",
    "DatasetAccessEntry",
    "DatasetList",
    "DeleteDatasetRequest",
    "GcpTag",
    "GetDatasetRequest",
    "InsertDatasetRequest",
    "LinkedDatasetMetadata",
    "LinkedDatasetSource",
    "ListDatasetsRequest",
    "ListFormatDataset",
    "UndeleteDatasetRequest",
    "UpdateOrPatchDatasetRequest",
    "DatasetReference",
    "DecimalTargetType",
    "EncryptionConfiguration",
    "ErrorProto",
    "ExternalCatalogDatasetOptions",
    "ExternalCatalogTableOptions",
    "SerDeInfo",
    "StorageDescriptor",
    "AvroOptions",
    "BigtableColumn",
    "BigtableColumnFamily",
    "BigtableOptions",
    "CsvOptions",
    "ExternalDataConfiguration",
    "GoogleSheetsOptions",
    "JsonOptions",
    "ParquetOptions",
    "ExternalDatasetReference",
    "FileSetSpecType",
    "HivePartitioningOptions",
    "CancelJobRequest",
    "DeleteJobRequest",
    "GetJobRequest",
    "GetQueryResultsRequest",
    "GetQueryResultsResponse",
    "InsertJobRequest",
    "Job",
    "JobCancelResponse",
    "JobList",
    "ListFormatJob",
    "ListJobsRequest",
    "PostQueryRequest",
    "QueryRequest",
    "QueryResponse",
    "ConnectionProperty",
    "DestinationTableProperties",
    "JobConfiguration",
    "JobConfigurationExtract",
    "JobConfigurationLoad",
    "JobConfigurationQuery",
    "JobConfigurationTableCopy",
    "ScriptOptions",
    "JobCreationReason",
    "JobReference",
    "BiEngineReason",
    "BiEngineStatistics",
    "CopyJobStatistics",
    "DataMaskingStatistics",
    "DmlStats",
    "ExplainQueryStage",
    "ExplainQueryStep",
    "ExportDataStatistics",
    "ExternalServiceCost",
    "HighCardinalityJoin",
    "IndexUnusedReason",
    "InputDataChange",
    "JobStatistics",
    "JobStatistics2",
    "JobStatistics3",
    "JobStatistics4",
    "LoadQueryStatistics",
    "MaterializedView",
    "MaterializedViewStatistics",
    "MetadataCacheStatistics",
    "MlStatistics",
    "PartitionSkew",
    "PerformanceInsights",
    "QueryInfo",
    "QueryTimelineSample",
    "RowLevelSecurityStatistics",
    "ScriptStatistics",
    "SearchStatistics",
    "SparkStatistics",
    "StagePerformanceChangeInsight",
    "StagePerformanceStandaloneInsight",
    "StoredColumnsUsage",
    "TableMetadataCacheUsage",
    "VectorSearchStatistics",
    "ReservationEdition",
    "JobStatus",
    "JsonExtension",
    "LocationMetadata",
    "ManagedTableType",
    "MapTargetType",
    "DeleteModelRequest",
    "GetModelRequest",
    "ListModelsRequest",
    "ListModelsResponse",
    "Model",
    "PatchModelRequest",
    "RemoteModelInfo",
    "TransformColumn",
    "ModelReference",
    "PartitionedColumn",
    "PartitioningDefinition",
    "AggregationThresholdPolicy",
    "DifferentialPrivacyPolicy",
    "JoinRestrictionPolicy",
    "PrivacyPolicy",
    "GetServiceAccountRequest",
    "GetServiceAccountResponse",
    "QueryParameter",
    "QueryParameterStructType",
    "QueryParameterType",
    "QueryParameterValue",
    "RangeValue",
    "RangePartitioning",
    "RestrictionConfig",
    "DeleteRoutineRequest",
    "ExternalRuntimeOptions",
    "GetRoutineRequest",
    "InsertRoutineRequest",
    "ListRoutinesRequest",
    "ListRoutinesResponse",
    "PatchRoutineRequest",
    "PythonOptions",
    "Routine",
    "SparkOptions",
    "UpdateRoutineRequest",
    "RoutineReference",
    "BatchDeleteRowAccessPoliciesRequest",
    "CreateRowAccessPolicyRequest",
    "DeleteRowAccessPolicyRequest",
    "GetRowAccessPolicyRequest",
    "ListRowAccessPoliciesRequest",
    "ListRowAccessPoliciesResponse",
    "RowAccessPolicy",
    "UpdateRowAccessPolicyRequest",
    "RowAccessPolicyReference",
    "SessionInfo",
    "StandardSqlDataType",
    "StandardSqlField",
    "StandardSqlStructType",
    "StandardSqlTableType",
    "SystemVariables",
    "CloneDefinition",
    "DeleteTableRequest",
    "ForeignViewDefinition",
    "GetTableRequest",
    "InsertTableRequest",
    "ListFormatTable",
    "ListFormatView",
    "ListTablesRequest",
    "MaterializedViewDefinition",
    "MaterializedViewStatus",
    "SnapshotDefinition",
    "Streamingbuffer",
    "Table",
    "TableList",
    "TableReplicationInfo",
    "UpdateOrPatchTableRequest",
    "ViewDefinition",
    "ColumnReference",
    "ForeignKey",
    "PrimaryKey",
    "TableConstraints",
    "TableReference",
    "DataPolicyOption",
    "ForeignTypeInfo",
    "TableFieldSchema",
    "TableSchema",
    "TimePartitioning",
    "UserDefinedFunctionResource",
)
