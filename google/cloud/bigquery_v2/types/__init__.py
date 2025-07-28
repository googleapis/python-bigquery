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
from .biglake_config import (
    BigLakeConfiguration,
)
from .clustering import (
    Clustering,
)
from .data_format_options import (
    DataFormatOptions,
)
from .dataset import (
    Access,
    Dataset,
    DatasetAccessEntry,
    DatasetList,
    DeleteDatasetRequest,
    GcpTag,
    GetDatasetRequest,
    InsertDatasetRequest,
    LinkedDatasetMetadata,
    LinkedDatasetSource,
    ListDatasetsRequest,
    ListFormatDataset,
    UndeleteDatasetRequest,
    UpdateOrPatchDatasetRequest,
)
from .dataset_reference import (
    DatasetReference,
)
from .decimal_target_types import (
    DecimalTargetType,
)
from .encryption_config import (
    EncryptionConfiguration,
)
from .error import (
    ErrorProto,
)
from .external_catalog_dataset_options import (
    ExternalCatalogDatasetOptions,
)
from .external_catalog_table_options import (
    ExternalCatalogTableOptions,
    SerDeInfo,
    StorageDescriptor,
)
from .external_data_config import (
    AvroOptions,
    BigtableColumn,
    BigtableColumnFamily,
    BigtableOptions,
    CsvOptions,
    ExternalDataConfiguration,
    GoogleSheetsOptions,
    JsonOptions,
    ParquetOptions,
)
from .external_dataset_reference import (
    ExternalDatasetReference,
)
from .file_set_specification_type import (
    FileSetSpecType,
)
from .hive_partitioning import (
    HivePartitioningOptions,
)
from .job import (
    CancelJobRequest,
    DeleteJobRequest,
    GetJobRequest,
    GetQueryResultsRequest,
    GetQueryResultsResponse,
    InsertJobRequest,
    Job,
    JobCancelResponse,
    JobList,
    ListFormatJob,
    ListJobsRequest,
    PostQueryRequest,
    QueryRequest,
    QueryResponse,
)
from .job_config import (
    ConnectionProperty,
    DestinationTableProperties,
    JobConfiguration,
    JobConfigurationExtract,
    JobConfigurationLoad,
    JobConfigurationQuery,
    JobConfigurationTableCopy,
    ScriptOptions,
)
from .job_creation_reason import (
    JobCreationReason,
)
from .job_reference import (
    JobReference,
)
from .job_stats import (
    BiEngineReason,
    BiEngineStatistics,
    CopyJobStatistics,
    DataMaskingStatistics,
    DmlStats,
    ExplainQueryStage,
    ExplainQueryStep,
    ExportDataStatistics,
    ExternalServiceCost,
    HighCardinalityJoin,
    IndexUnusedReason,
    InputDataChange,
    JobStatistics,
    JobStatistics2,
    JobStatistics3,
    JobStatistics4,
    LoadQueryStatistics,
    MaterializedView,
    MaterializedViewStatistics,
    MetadataCacheStatistics,
    MlStatistics,
    PartitionSkew,
    PerformanceInsights,
    QueryInfo,
    QueryTimelineSample,
    RowLevelSecurityStatistics,
    ScriptStatistics,
    SearchStatistics,
    SparkStatistics,
    StagePerformanceChangeInsight,
    StagePerformanceStandaloneInsight,
    StoredColumnsUsage,
    TableMetadataCacheUsage,
    VectorSearchStatistics,
    ReservationEdition,
)
from .job_status import (
    JobStatus,
)
from .json_extension import (
    JsonExtension,
)
from .location_metadata import (
    LocationMetadata,
)
from .managed_table_type import (
    ManagedTableType,
)
from .map_target_type import (
    MapTargetType,
)
from .model import (
    DeleteModelRequest,
    GetModelRequest,
    ListModelsRequest,
    ListModelsResponse,
    Model,
    PatchModelRequest,
    RemoteModelInfo,
    TransformColumn,
)
from .model_reference import (
    ModelReference,
)
from .partitioning_definition import (
    PartitionedColumn,
    PartitioningDefinition,
)
from .privacy_policy import (
    AggregationThresholdPolicy,
    DifferentialPrivacyPolicy,
    JoinRestrictionPolicy,
    PrivacyPolicy,
)
from .project import (
    GetServiceAccountRequest,
    GetServiceAccountResponse,
)
from .query_parameter import (
    QueryParameter,
    QueryParameterStructType,
    QueryParameterType,
    QueryParameterValue,
    RangeValue,
)
from .range_partitioning import (
    RangePartitioning,
)
from .restriction_config import (
    RestrictionConfig,
)
from .routine import (
    DeleteRoutineRequest,
    ExternalRuntimeOptions,
    GetRoutineRequest,
    InsertRoutineRequest,
    ListRoutinesRequest,
    ListRoutinesResponse,
    PatchRoutineRequest,
    PythonOptions,
    Routine,
    SparkOptions,
    UpdateRoutineRequest,
)
from .routine_reference import (
    RoutineReference,
)
from .row_access_policy import (
    BatchDeleteRowAccessPoliciesRequest,
    CreateRowAccessPolicyRequest,
    DeleteRowAccessPolicyRequest,
    GetRowAccessPolicyRequest,
    ListRowAccessPoliciesRequest,
    ListRowAccessPoliciesResponse,
    RowAccessPolicy,
    UpdateRowAccessPolicyRequest,
)
from .row_access_policy_reference import (
    RowAccessPolicyReference,
)
from .session_info import (
    SessionInfo,
)
from .standard_sql import (
    StandardSqlDataType,
    StandardSqlField,
    StandardSqlStructType,
    StandardSqlTableType,
)
from .system_variable import (
    SystemVariables,
)
from .table import (
    CloneDefinition,
    DeleteTableRequest,
    ForeignViewDefinition,
    GetTableRequest,
    InsertTableRequest,
    ListFormatTable,
    ListFormatView,
    ListTablesRequest,
    MaterializedViewDefinition,
    MaterializedViewStatus,
    SnapshotDefinition,
    Streamingbuffer,
    Table,
    TableList,
    TableReplicationInfo,
    UpdateOrPatchTableRequest,
    ViewDefinition,
)
from .table_constraints import (
    ColumnReference,
    ForeignKey,
    PrimaryKey,
    TableConstraints,
)
from .table_reference import (
    TableReference,
)
from .table_schema import (
    DataPolicyOption,
    ForeignTypeInfo,
    TableFieldSchema,
    TableSchema,
)
from .time_partitioning import (
    TimePartitioning,
)
from .udf_resource import (
    UserDefinedFunctionResource,
)

__all__ = (
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
