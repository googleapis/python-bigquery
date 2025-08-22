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
from google.cloud.bigquery_v2 import gapic_version as package_version

__version__ = package_version.__version__

from .services.dataset_service import DatasetServiceClient
from .services.job_service import JobServiceClient
from .services.model_service import ModelServiceClient
from .services.project_service import ProjectServiceClient
from .services.routine_service import RoutineServiceClient
from .services.row_access_policy_service import RowAccessPolicyServiceClient
from .services.table_service import TableServiceClient

from .types.biglake_config import BigLakeConfiguration
from .types.clustering import Clustering
from .types.data_format_options import DataFormatOptions
from .types.dataset import Access
from .types.dataset import Dataset
from .types.dataset import DatasetAccessEntry
from .types.dataset import DatasetList
from .types.dataset import DeleteDatasetRequest
from .types.dataset import GcpTag
from .types.dataset import GetDatasetRequest
from .types.dataset import InsertDatasetRequest
from .types.dataset import LinkedDatasetMetadata
from .types.dataset import LinkedDatasetSource
from .types.dataset import ListDatasetsRequest
from .types.dataset import ListFormatDataset
from .types.dataset import UndeleteDatasetRequest
from .types.dataset import UpdateOrPatchDatasetRequest
from .types.dataset_reference import DatasetReference
from .types.decimal_target_types import DecimalTargetType
from .types.encryption_config import EncryptionConfiguration
from .types.error import ErrorProto
from .types.external_catalog_dataset_options import ExternalCatalogDatasetOptions
from .types.external_catalog_table_options import ExternalCatalogTableOptions
from .types.external_catalog_table_options import SerDeInfo
from .types.external_catalog_table_options import StorageDescriptor
from .types.external_data_config import AvroOptions
from .types.external_data_config import BigtableColumn
from .types.external_data_config import BigtableColumnFamily
from .types.external_data_config import BigtableOptions
from .types.external_data_config import CsvOptions
from .types.external_data_config import ExternalDataConfiguration
from .types.external_data_config import GoogleSheetsOptions
from .types.external_data_config import JsonOptions
from .types.external_data_config import ParquetOptions
from .types.external_dataset_reference import ExternalDatasetReference
from .types.file_set_specification_type import FileSetSpecType
from .types.hive_partitioning import HivePartitioningOptions
from .types.job import CancelJobRequest
from .types.job import DeleteJobRequest
from .types.job import GetJobRequest
from .types.job import GetQueryResultsRequest
from .types.job import GetQueryResultsResponse
from .types.job import InsertJobRequest
from .types.job import Job
from .types.job import JobCancelResponse
from .types.job import JobList
from .types.job import ListFormatJob
from .types.job import ListJobsRequest
from .types.job import PostQueryRequest
from .types.job import QueryRequest
from .types.job import QueryResponse
from .types.job_config import ConnectionProperty
from .types.job_config import DestinationTableProperties
from .types.job_config import JobConfiguration
from .types.job_config import JobConfigurationExtract
from .types.job_config import JobConfigurationLoad
from .types.job_config import JobConfigurationQuery
from .types.job_config import JobConfigurationTableCopy
from .types.job_config import ScriptOptions
from .types.job_creation_reason import JobCreationReason
from .types.job_reference import JobReference
from .types.job_stats import BiEngineReason
from .types.job_stats import BiEngineStatistics
from .types.job_stats import CopyJobStatistics
from .types.job_stats import DataMaskingStatistics
from .types.job_stats import DmlStats
from .types.job_stats import ExplainQueryStage
from .types.job_stats import ExplainQueryStep
from .types.job_stats import ExportDataStatistics
from .types.job_stats import ExternalServiceCost
from .types.job_stats import HighCardinalityJoin
from .types.job_stats import IndexUnusedReason
from .types.job_stats import InputDataChange
from .types.job_stats import JobStatistics
from .types.job_stats import JobStatistics2
from .types.job_stats import JobStatistics3
from .types.job_stats import JobStatistics4
from .types.job_stats import LoadQueryStatistics
from .types.job_stats import MaterializedView
from .types.job_stats import MaterializedViewStatistics
from .types.job_stats import MetadataCacheStatistics
from .types.job_stats import MlStatistics
from .types.job_stats import PartitionSkew
from .types.job_stats import PerformanceInsights
from .types.job_stats import QueryInfo
from .types.job_stats import QueryTimelineSample
from .types.job_stats import RowLevelSecurityStatistics
from .types.job_stats import ScriptStatistics
from .types.job_stats import SearchStatistics
from .types.job_stats import SparkStatistics
from .types.job_stats import StagePerformanceChangeInsight
from .types.job_stats import StagePerformanceStandaloneInsight
from .types.job_stats import StoredColumnsUsage
from .types.job_stats import TableMetadataCacheUsage
from .types.job_stats import VectorSearchStatistics
from .types.job_stats import ReservationEdition
from .types.job_status import JobStatus
from .types.json_extension import JsonExtension
from .types.location_metadata import LocationMetadata
from .types.managed_table_type import ManagedTableType
from .types.map_target_type import MapTargetType
from .types.model import DeleteModelRequest
from .types.model import GetModelRequest
from .types.model import ListModelsRequest
from .types.model import ListModelsResponse
from .types.model import Model
from .types.model import PatchModelRequest
from .types.model import RemoteModelInfo
from .types.model import TransformColumn
from .types.model_reference import ModelReference
from .types.partitioning_definition import PartitionedColumn
from .types.partitioning_definition import PartitioningDefinition
from .types.privacy_policy import AggregationThresholdPolicy
from .types.privacy_policy import DifferentialPrivacyPolicy
from .types.privacy_policy import JoinRestrictionPolicy
from .types.privacy_policy import PrivacyPolicy
from .types.project import GetServiceAccountRequest
from .types.project import GetServiceAccountResponse
from .types.query_parameter import QueryParameter
from .types.query_parameter import QueryParameterStructType
from .types.query_parameter import QueryParameterType
from .types.query_parameter import QueryParameterValue
from .types.query_parameter import RangeValue
from .types.range_partitioning import RangePartitioning
from .types.restriction_config import RestrictionConfig
from .types.routine import DeleteRoutineRequest
from .types.routine import ExternalRuntimeOptions
from .types.routine import GetRoutineRequest
from .types.routine import InsertRoutineRequest
from .types.routine import ListRoutinesRequest
from .types.routine import ListRoutinesResponse
from .types.routine import PatchRoutineRequest
from .types.routine import PythonOptions
from .types.routine import Routine
from .types.routine import SparkOptions
from .types.routine import UpdateRoutineRequest
from .types.routine_reference import RoutineReference
from .types.row_access_policy import BatchDeleteRowAccessPoliciesRequest
from .types.row_access_policy import CreateRowAccessPolicyRequest
from .types.row_access_policy import DeleteRowAccessPolicyRequest
from .types.row_access_policy import GetRowAccessPolicyRequest
from .types.row_access_policy import ListRowAccessPoliciesRequest
from .types.row_access_policy import ListRowAccessPoliciesResponse
from .types.row_access_policy import RowAccessPolicy
from .types.row_access_policy import UpdateRowAccessPolicyRequest
from .types.row_access_policy_reference import RowAccessPolicyReference
from .types.session_info import SessionInfo
from .types.standard_sql import StandardSqlDataType
from .types.standard_sql import StandardSqlField
from .types.standard_sql import StandardSqlStructType
from .types.standard_sql import StandardSqlTableType
from .types.system_variable import SystemVariables
from .types.table import CloneDefinition
from .types.table import DeleteTableRequest
from .types.table import ForeignViewDefinition
from .types.table import GetTableRequest
from .types.table import InsertTableRequest
from .types.table import ListFormatTable
from .types.table import ListFormatView
from .types.table import ListTablesRequest
from .types.table import MaterializedViewDefinition
from .types.table import MaterializedViewStatus
from .types.table import SnapshotDefinition
from .types.table import Streamingbuffer
from .types.table import Table
from .types.table import TableList
from .types.table import TableReplicationInfo
from .types.table import UpdateOrPatchTableRequest
from .types.table import ViewDefinition
from .types.table_constraints import ColumnReference
from .types.table_constraints import ForeignKey
from .types.table_constraints import PrimaryKey
from .types.table_constraints import TableConstraints
from .types.table_reference import TableReference
from .types.table_schema import DataPolicyOption
from .types.table_schema import ForeignTypeInfo
from .types.table_schema import TableFieldSchema
from .types.table_schema import TableSchema
from .types.time_partitioning import TimePartitioning
from .types.udf_resource import UserDefinedFunctionResource

__all__ = (
    "Access",
    "AggregationThresholdPolicy",
    "AvroOptions",
    "BatchDeleteRowAccessPoliciesRequest",
    "BiEngineReason",
    "BiEngineStatistics",
    "BigLakeConfiguration",
    "BigtableColumn",
    "BigtableColumnFamily",
    "BigtableOptions",
    "CancelJobRequest",
    "CloneDefinition",
    "Clustering",
    "ColumnReference",
    "ConnectionProperty",
    "CopyJobStatistics",
    "CreateRowAccessPolicyRequest",
    "CsvOptions",
    "DataFormatOptions",
    "DataMaskingStatistics",
    "DataPolicyOption",
    "Dataset",
    "DatasetAccessEntry",
    "DatasetList",
    "DatasetReference",
    "DatasetServiceClient",
    "DecimalTargetType",
    "DeleteDatasetRequest",
    "DeleteJobRequest",
    "DeleteModelRequest",
    "DeleteRoutineRequest",
    "DeleteRowAccessPolicyRequest",
    "DeleteTableRequest",
    "DestinationTableProperties",
    "DifferentialPrivacyPolicy",
    "DmlStats",
    "EncryptionConfiguration",
    "ErrorProto",
    "ExplainQueryStage",
    "ExplainQueryStep",
    "ExportDataStatistics",
    "ExternalCatalogDatasetOptions",
    "ExternalCatalogTableOptions",
    "ExternalDataConfiguration",
    "ExternalDatasetReference",
    "ExternalRuntimeOptions",
    "ExternalServiceCost",
    "FileSetSpecType",
    "ForeignKey",
    "ForeignTypeInfo",
    "ForeignViewDefinition",
    "GcpTag",
    "GetDatasetRequest",
    "GetJobRequest",
    "GetModelRequest",
    "GetQueryResultsRequest",
    "GetQueryResultsResponse",
    "GetRoutineRequest",
    "GetRowAccessPolicyRequest",
    "GetServiceAccountRequest",
    "GetServiceAccountResponse",
    "GetTableRequest",
    "GoogleSheetsOptions",
    "HighCardinalityJoin",
    "HivePartitioningOptions",
    "IndexUnusedReason",
    "InputDataChange",
    "InsertDatasetRequest",
    "InsertJobRequest",
    "InsertRoutineRequest",
    "InsertTableRequest",
    "Job",
    "JobCancelResponse",
    "JobConfiguration",
    "JobConfigurationExtract",
    "JobConfigurationLoad",
    "JobConfigurationQuery",
    "JobConfigurationTableCopy",
    "JobCreationReason",
    "JobList",
    "JobReference",
    "JobServiceClient",
    "JobStatistics",
    "JobStatistics2",
    "JobStatistics3",
    "JobStatistics4",
    "JobStatus",
    "JoinRestrictionPolicy",
    "JsonExtension",
    "JsonOptions",
    "LinkedDatasetMetadata",
    "LinkedDatasetSource",
    "ListDatasetsRequest",
    "ListFormatDataset",
    "ListFormatJob",
    "ListFormatTable",
    "ListFormatView",
    "ListJobsRequest",
    "ListModelsRequest",
    "ListModelsResponse",
    "ListRoutinesRequest",
    "ListRoutinesResponse",
    "ListRowAccessPoliciesRequest",
    "ListRowAccessPoliciesResponse",
    "ListTablesRequest",
    "LoadQueryStatistics",
    "LocationMetadata",
    "ManagedTableType",
    "MapTargetType",
    "MaterializedView",
    "MaterializedViewDefinition",
    "MaterializedViewStatistics",
    "MaterializedViewStatus",
    "MetadataCacheStatistics",
    "MlStatistics",
    "Model",
    "ModelReference",
    "ModelServiceClient",
    "ParquetOptions",
    "PartitionSkew",
    "PartitionedColumn",
    "PartitioningDefinition",
    "PatchModelRequest",
    "PatchRoutineRequest",
    "PerformanceInsights",
    "PostQueryRequest",
    "PrimaryKey",
    "PrivacyPolicy",
    "ProjectServiceClient",
    "PythonOptions",
    "QueryInfo",
    "QueryParameter",
    "QueryParameterStructType",
    "QueryParameterType",
    "QueryParameterValue",
    "QueryRequest",
    "QueryResponse",
    "QueryTimelineSample",
    "RangePartitioning",
    "RangeValue",
    "RemoteModelInfo",
    "ReservationEdition",
    "RestrictionConfig",
    "Routine",
    "RoutineReference",
    "RoutineServiceClient",
    "RowAccessPolicy",
    "RowAccessPolicyReference",
    "RowAccessPolicyServiceClient",
    "RowLevelSecurityStatistics",
    "ScriptOptions",
    "ScriptStatistics",
    "SearchStatistics",
    "SerDeInfo",
    "SessionInfo",
    "SnapshotDefinition",
    "SparkOptions",
    "SparkStatistics",
    "StagePerformanceChangeInsight",
    "StagePerformanceStandaloneInsight",
    "StandardSqlDataType",
    "StandardSqlField",
    "StandardSqlStructType",
    "StandardSqlTableType",
    "StorageDescriptor",
    "StoredColumnsUsage",
    "Streamingbuffer",
    "SystemVariables",
    "Table",
    "TableConstraints",
    "TableFieldSchema",
    "TableList",
    "TableMetadataCacheUsage",
    "TableReference",
    "TableReplicationInfo",
    "TableSchema",
    "TableServiceClient",
    "TimePartitioning",
    "TransformColumn",
    "UndeleteDatasetRequest",
    "UpdateOrPatchDatasetRequest",
    "UpdateOrPatchTableRequest",
    "UpdateRoutineRequest",
    "UpdateRowAccessPolicyRequest",
    "UserDefinedFunctionResource",
    "VectorSearchStatistics",
    "ViewDefinition",
)
