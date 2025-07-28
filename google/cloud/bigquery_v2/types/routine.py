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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.bigquery_v2.types import routine_reference as gcb_routine_reference
from google.cloud.bigquery_v2.types import standard_sql
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "Routine",
        "PythonOptions",
        "ExternalRuntimeOptions",
        "SparkOptions",
        "GetRoutineRequest",
        "InsertRoutineRequest",
        "UpdateRoutineRequest",
        "PatchRoutineRequest",
        "DeleteRoutineRequest",
        "ListRoutinesRequest",
        "ListRoutinesResponse",
    },
)


class Routine(proto.Message):
    r"""A user-defined function or a stored procedure.

    Attributes:
        etag (str):
            Output only. A hash of this resource.
        routine_reference (google.cloud.bigquery_v2.types.RoutineReference):
            Required. Reference describing the ID of this
            routine.
        routine_type (google.cloud.bigquery_v2.types.Routine.RoutineType):
            Required. The type of routine.
        creation_time (int):
            Output only. The time when this routine was
            created, in milliseconds since the epoch.
        last_modified_time (int):
            Output only. The time when this routine was
            last modified, in milliseconds since the epoch.
        language (google.cloud.bigquery_v2.types.Routine.Language):
            Optional. Defaults to "SQL" if remote_function_options field
            is absent, not set otherwise.
        arguments (MutableSequence[google.cloud.bigquery_v2.types.Routine.Argument]):
            Optional.
        return_type (google.cloud.bigquery_v2.types.StandardSqlDataType):
            Optional if language = "SQL"; required otherwise. Cannot be
            set if routine_type = "TABLE_VALUED_FUNCTION".

            If absent, the return type is inferred from definition_body
            at query time in each query that references this routine. If
            present, then the evaluated result will be cast to the
            specified returned type at query time.

            For example, for the functions created with the following
            statements:

            -  ``CREATE FUNCTION Add(x FLOAT64, y FLOAT64) RETURNS FLOAT64 AS (x + y);``

            -  ``CREATE FUNCTION Increment(x FLOAT64) AS (Add(x, 1));``

            -  ``CREATE FUNCTION Decrement(x FLOAT64) RETURNS FLOAT64 AS (Add(x, -1));``

            The return_type is ``{type_kind: "FLOAT64"}`` for ``Add``
            and ``Decrement``, and is absent for ``Increment`` (inferred
            as FLOAT64 at query time).

            Suppose the function ``Add`` is replaced by
            ``CREATE OR REPLACE FUNCTION Add(x INT64, y INT64) AS (x + y);``

            Then the inferred return type of ``Increment`` is
            automatically changed to INT64 at query time, while the
            return type of ``Decrement`` remains FLOAT64.
        return_table_type (google.cloud.bigquery_v2.types.StandardSqlTableType):
            Optional. Can be set only if routine_type =
            "TABLE_VALUED_FUNCTION".

            If absent, the return table type is inferred from
            definition_body at query time in each query that references
            this routine. If present, then the columns in the evaluated
            table result will be cast to match the column types
            specified in return table type, at query time.
        imported_libraries (MutableSequence[str]):
            Optional. If language = "JAVASCRIPT", this
            field stores the path of the imported JAVASCRIPT
            libraries.
        definition_body (str):
            Required. The body of the routine.

            For functions, this is the expression in the AS clause.

            If language=SQL, it is the substring inside (but excluding)
            the parentheses. For example, for the function created with
            the following statement:

            ``CREATE FUNCTION JoinLines(x string, y string) as (concat(x, "\n", y))``

            The definition_body is ``concat(x, "\n", y)`` (\n is not
            replaced with linebreak).

            If language=JAVASCRIPT, it is the evaluated string in the AS
            clause. For example, for the function created with the
            following statement:

            ``CREATE FUNCTION f() RETURNS STRING LANGUAGE js AS 'return "\n";\n'``

            The definition_body is

            ``return "\n";\n``

            Note that both \\n are replaced with linebreaks.
        description (str):
            Optional. The description of the routine, if
            defined.
        determinism_level (google.cloud.bigquery_v2.types.Routine.DeterminismLevel):
            Optional. The determinism level of the
            JavaScript UDF, if defined.
        security_mode (google.cloud.bigquery_v2.types.Routine.SecurityMode):
            Optional. The security mode of the routine,
            if defined. If not defined, the security mode is
            automatically determined from the routine's
            configuration.
        strict_mode (google.protobuf.wrappers_pb2.BoolValue):
            Optional. Use this option to catch many common errors. Error
            checking is not exhaustive, and successfully creating a
            procedure doesn't guarantee that the procedure will
            successfully execute at runtime. If ``strictMode`` is set to
            ``TRUE``, the procedure body is further checked for errors
            such as non-existent tables or columns. The
            ``CREATE PROCEDURE`` statement fails if the body fails any
            of these checks.

            If ``strictMode`` is set to ``FALSE``, the procedure body is
            checked only for syntax. For procedures that invoke
            themselves recursively, specify ``strictMode=FALSE`` to
            avoid non-existent procedure errors during validation.

            Default value is ``TRUE``.
        remote_function_options (google.cloud.bigquery_v2.types.Routine.RemoteFunctionOptions):
            Optional. Remote function specific options.
        spark_options (google.cloud.bigquery_v2.types.SparkOptions):
            Optional. Spark specific options.
        data_governance_type (google.cloud.bigquery_v2.types.Routine.DataGovernanceType):
            Optional. If set to ``DATA_MASKING``, the function is
            validated and made available as a masking function. For more
            information, see `Create custom masking
            routines <https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask>`__.
        python_options (google.cloud.bigquery_v2.types.PythonOptions):
            Optional. Options for Python UDF.
            `Preview <https://cloud.google.com/products/#product-launch-stages>`__
        external_runtime_options (google.cloud.bigquery_v2.types.ExternalRuntimeOptions):
            Optional. Options for the runtime of the external system
            executing the routine. This field is only applicable for
            Python UDFs.
            `Preview <https://cloud.google.com/products/#product-launch-stages>`__
    """

    class RoutineType(proto.Enum):
        r"""The fine-grained type of the routine.

        Values:
            ROUTINE_TYPE_UNSPECIFIED (0):
                Default value.
            SCALAR_FUNCTION (1):
                Non-built-in persistent scalar function.
            PROCEDURE (2):
                Stored procedure.
            TABLE_VALUED_FUNCTION (3):
                Non-built-in persistent TVF.
            AGGREGATE_FUNCTION (4):
                Non-built-in persistent aggregate function.
        """
        ROUTINE_TYPE_UNSPECIFIED = 0
        SCALAR_FUNCTION = 1
        PROCEDURE = 2
        TABLE_VALUED_FUNCTION = 3
        AGGREGATE_FUNCTION = 4

    class Language(proto.Enum):
        r"""The language of the routine.

        Values:
            LANGUAGE_UNSPECIFIED (0):
                Default value.
            SQL (1):
                SQL language.
            JAVASCRIPT (2):
                JavaScript language.
            PYTHON (3):
                Python language.
            JAVA (4):
                Java language.
            SCALA (5):
                Scala language.
        """
        LANGUAGE_UNSPECIFIED = 0
        SQL = 1
        JAVASCRIPT = 2
        PYTHON = 3
        JAVA = 4
        SCALA = 5

    class DeterminismLevel(proto.Enum):
        r"""JavaScript UDF determinism levels.

        If all JavaScript UDFs are DETERMINISTIC, the query result is
        potentially cacheable (see below). If any JavaScript UDF is
        NOT_DETERMINISTIC, the query result is not cacheable.

        Even if a JavaScript UDF is deterministic, many other factors can
        prevent usage of cached query results. Example factors include but
        not limited to: DDL/DML, non-deterministic SQL function calls,
        update of referenced tables/views/UDFs or imported JavaScript
        libraries.

        SQL UDFs cannot have determinism specified. Their determinism is
        automatically determined.

        Values:
            DETERMINISM_LEVEL_UNSPECIFIED (0):
                The determinism of the UDF is unspecified.
            DETERMINISTIC (1):
                The UDF is deterministic, meaning that 2
                function calls with the same inputs always
                produce the same result, even across 2 query
                runs.
            NOT_DETERMINISTIC (2):
                The UDF is not deterministic.
        """
        DETERMINISM_LEVEL_UNSPECIFIED = 0
        DETERMINISTIC = 1
        NOT_DETERMINISTIC = 2

    class SecurityMode(proto.Enum):
        r"""Security mode.

        Values:
            SECURITY_MODE_UNSPECIFIED (0):
                The security mode of the routine is
                unspecified.
            DEFINER (1):
                The routine is to be executed with the
                privileges of the user who defines it.
            INVOKER (2):
                The routine is to be executed with the
                privileges of the user who invokes it.
        """
        SECURITY_MODE_UNSPECIFIED = 0
        DEFINER = 1
        INVOKER = 2

    class DataGovernanceType(proto.Enum):
        r"""Data governance type values. Only supports ``DATA_MASKING``.

        Values:
            DATA_GOVERNANCE_TYPE_UNSPECIFIED (0):
                The data governance type is unspecified.
            DATA_MASKING (1):
                The data governance type is data masking.
        """
        DATA_GOVERNANCE_TYPE_UNSPECIFIED = 0
        DATA_MASKING = 1

    class Argument(proto.Message):
        r"""Input/output argument of a function or a stored procedure.

        Attributes:
            name (str):
                Optional. The name of this argument. Can be
                absent for function return argument.
            argument_kind (google.cloud.bigquery_v2.types.Routine.Argument.ArgumentKind):
                Optional. Defaults to FIXED_TYPE.
            mode (google.cloud.bigquery_v2.types.Routine.Argument.Mode):
                Optional. Specifies whether the argument is
                input or output. Can be set for procedures only.
            data_type (google.cloud.bigquery_v2.types.StandardSqlDataType):
                Set if argument_kind == FIXED_TYPE.
            is_aggregate (google.protobuf.wrappers_pb2.BoolValue):
                Optional. Whether the argument is an aggregate function
                parameter. Must be Unset for routine types other than
                AGGREGATE_FUNCTION. For AGGREGATE_FUNCTION, if set to false,
                it is equivalent to adding "NOT AGGREGATE" clause in DDL;
                Otherwise, it is equivalent to omitting "NOT AGGREGATE"
                clause in DDL.
        """

        class ArgumentKind(proto.Enum):
            r"""Represents the kind of a given argument.

            Values:
                ARGUMENT_KIND_UNSPECIFIED (0):
                    Default value.
                FIXED_TYPE (1):
                    The argument is a variable with fully
                    specified type, which can be a struct or an
                    array, but not a table.
                ANY_TYPE (2):
                    The argument is any type, including struct or
                    array, but not a table.
            """
            ARGUMENT_KIND_UNSPECIFIED = 0
            FIXED_TYPE = 1
            ANY_TYPE = 2

        class Mode(proto.Enum):
            r"""The input/output mode of the argument.

            Values:
                MODE_UNSPECIFIED (0):
                    Default value.
                IN (1):
                    The argument is input-only.
                OUT (2):
                    The argument is output-only.
                INOUT (3):
                    The argument is both an input and an output.
            """
            MODE_UNSPECIFIED = 0
            IN = 1
            OUT = 2
            INOUT = 3

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        argument_kind: "Routine.Argument.ArgumentKind" = proto.Field(
            proto.ENUM,
            number=2,
            enum="Routine.Argument.ArgumentKind",
        )
        mode: "Routine.Argument.Mode" = proto.Field(
            proto.ENUM,
            number=3,
            enum="Routine.Argument.Mode",
        )
        data_type: standard_sql.StandardSqlDataType = proto.Field(
            proto.MESSAGE,
            number=4,
            message=standard_sql.StandardSqlDataType,
        )
        is_aggregate: wrappers_pb2.BoolValue = proto.Field(
            proto.MESSAGE,
            number=6,
            message=wrappers_pb2.BoolValue,
        )

    class RemoteFunctionOptions(proto.Message):
        r"""Options for a remote user-defined function.

        Attributes:
            endpoint (str):
                Endpoint of the user-provided remote service, e.g.
                ``https://us-east1-my_gcf_project.cloudfunctions.net/remote_add``
            connection (str):
                Fully qualified name of the user-provided connection object
                which holds the authentication information to send requests
                to the remote service. Format:
                ``"projects/{projectId}/locations/{locationId}/connections/{connectionId}"``
            user_defined_context (MutableMapping[str, str]):
                User-defined context as a set of key/value
                pairs, which will be sent as function invocation
                context together with batched arguments in the
                requests to the remote service. The total number
                of bytes of keys and values must be less than
                8KB.
            max_batching_rows (int):
                Max number of rows in each batch sent to the
                remote service. If absent or if 0, BigQuery
                dynamically decides the number of rows in a
                batch.
        """

        endpoint: str = proto.Field(
            proto.STRING,
            number=1,
        )
        connection: str = proto.Field(
            proto.STRING,
            number=2,
        )
        user_defined_context: MutableMapping[str, str] = proto.MapField(
            proto.STRING,
            proto.STRING,
            number=3,
        )
        max_batching_rows: int = proto.Field(
            proto.INT64,
            number=4,
        )

    etag: str = proto.Field(
        proto.STRING,
        number=1,
    )
    routine_reference: gcb_routine_reference.RoutineReference = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcb_routine_reference.RoutineReference,
    )
    routine_type: RoutineType = proto.Field(
        proto.ENUM,
        number=3,
        enum=RoutineType,
    )
    creation_time: int = proto.Field(
        proto.INT64,
        number=4,
    )
    last_modified_time: int = proto.Field(
        proto.INT64,
        number=5,
    )
    language: Language = proto.Field(
        proto.ENUM,
        number=6,
        enum=Language,
    )
    arguments: MutableSequence[Argument] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=Argument,
    )
    return_type: standard_sql.StandardSqlDataType = proto.Field(
        proto.MESSAGE,
        number=10,
        message=standard_sql.StandardSqlDataType,
    )
    return_table_type: standard_sql.StandardSqlTableType = proto.Field(
        proto.MESSAGE,
        number=13,
        message=standard_sql.StandardSqlTableType,
    )
    imported_libraries: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )
    definition_body: str = proto.Field(
        proto.STRING,
        number=9,
    )
    description: str = proto.Field(
        proto.STRING,
        number=11,
    )
    determinism_level: DeterminismLevel = proto.Field(
        proto.ENUM,
        number=12,
        enum=DeterminismLevel,
    )
    security_mode: SecurityMode = proto.Field(
        proto.ENUM,
        number=18,
        enum=SecurityMode,
    )
    strict_mode: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=14,
        message=wrappers_pb2.BoolValue,
    )
    remote_function_options: RemoteFunctionOptions = proto.Field(
        proto.MESSAGE,
        number=15,
        message=RemoteFunctionOptions,
    )
    spark_options: "SparkOptions" = proto.Field(
        proto.MESSAGE,
        number=16,
        message="SparkOptions",
    )
    data_governance_type: DataGovernanceType = proto.Field(
        proto.ENUM,
        number=17,
        enum=DataGovernanceType,
    )
    python_options: "PythonOptions" = proto.Field(
        proto.MESSAGE,
        number=20,
        message="PythonOptions",
    )
    external_runtime_options: "ExternalRuntimeOptions" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="ExternalRuntimeOptions",
    )


class PythonOptions(proto.Message):
    r"""Options for a user-defined Python function.

    Attributes:
        entry_point (str):
            Required. The entry point function in the
            user's Python code.
        packages (MutableSequence[str]):
            Optional. A list of package names along with
            versions to be installed. Follows
            requirements.txt syntax (e.g. numpy==2.0,
            permutation, urllib3<2.2.1)
    """

    entry_point: str = proto.Field(
        proto.STRING,
        number=1,
    )
    packages: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class ExternalRuntimeOptions(proto.Message):
    r"""Options for the runtime of the external system.

    Attributes:
        container_memory (str):
            Optional. Amount of memory provisioned for
            the container instance. Format: {number}{unit}
            where unit is one of "M", "G", "Mi" and "Gi"
            (e.g. 1G, 512Mi). If not specified, the default
            value is 512Mi.
        container_cpu (float):
            Optional. Amount of CPU provisioned for the
            container instance. If not specified, the
            default value is 0.33 vCPUs.
        runtime_connection (str):
            Optional. Fully qualified name of the connection whose
            service account will be used to execute the code in the
            container. Format:
            ``"projects/{project_id}/locations/{location_id}/connections/{connection_id}"``
        max_batching_rows (int):
            Optional. Maximum number of rows in each
            batch sent to the external runtime. If absent or
            if 0, BigQuery dynamically decides the number of
            rows in a batch.
        runtime_version (str):
            Optional. Language runtime version (e.g.
            python-3.11).
    """

    container_memory: str = proto.Field(
        proto.STRING,
        number=1,
    )
    container_cpu: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )
    runtime_connection: str = proto.Field(
        proto.STRING,
        number=3,
    )
    max_batching_rows: int = proto.Field(
        proto.INT64,
        number=4,
    )
    runtime_version: str = proto.Field(
        proto.STRING,
        number=5,
    )


class SparkOptions(proto.Message):
    r"""Options for a user-defined Spark routine.

    Attributes:
        connection (str):
            Fully qualified name of the user-provided Spark connection
            object. Format:
            ``"projects/{project_id}/locations/{location_id}/connections/{connection_id}"``
        runtime_version (str):
            Runtime version. If not specified, the
            default runtime version is used.
        container_image (str):
            Custom container image for the runtime
            environment.
        properties (MutableMapping[str, str]):
            Configuration properties as a set of key/value pairs, which
            will be passed on to the Spark application. For more
            information, see `Apache
            Spark <https://spark.apache.org/docs/latest/index.html>`__
            and the `procedure option
            list <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#procedure_option_list>`__.
        main_file_uri (str):
            The main file/jar URI of the Spark application. Exactly one
            of the definition_body field and the main_file_uri field
            must be set for Python. Exactly one of main_class and
            main_file_uri field should be set for Java/Scala language
            type.
        py_file_uris (MutableSequence[str]):
            Python files to be placed on the PYTHONPATH for PySpark
            application. Supported file types: ``.py``, ``.egg``, and
            ``.zip``. For more information about Apache Spark, see
            `Apache
            Spark <https://spark.apache.org/docs/latest/index.html>`__.
        jar_uris (MutableSequence[str]):
            JARs to include on the driver and executor CLASSPATH. For
            more information about Apache Spark, see `Apache
            Spark <https://spark.apache.org/docs/latest/index.html>`__.
        file_uris (MutableSequence[str]):
            Files to be placed in the working directory of each
            executor. For more information about Apache Spark, see
            `Apache
            Spark <https://spark.apache.org/docs/latest/index.html>`__.
        archive_uris (MutableSequence[str]):
            Archive files to be extracted into the working directory of
            each executor. For more information about Apache Spark, see
            `Apache
            Spark <https://spark.apache.org/docs/latest/index.html>`__.
        main_class (str):
            The fully qualified name of a class in jar_uris, for
            example, com.example.wordcount. Exactly one of main_class
            and main_jar_uri field should be set for Java/Scala language
            type.
    """

    connection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    runtime_version: str = proto.Field(
        proto.STRING,
        number=2,
    )
    container_image: str = proto.Field(
        proto.STRING,
        number=3,
    )
    properties: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    main_file_uri: str = proto.Field(
        proto.STRING,
        number=5,
    )
    py_file_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    jar_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    file_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )
    archive_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    main_class: str = proto.Field(
        proto.STRING,
        number=10,
    )


class GetRoutineRequest(proto.Message):
    r"""Describes the format for getting information about a routine.

    Attributes:
        project_id (str):
            Required. Project ID of the requested routine
        dataset_id (str):
            Required. Dataset ID of the requested routine
        routine_id (str):
            Required. Routine ID of the requested routine
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    routine_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class InsertRoutineRequest(proto.Message):
    r"""Describes the format for inserting a routine.

    Attributes:
        project_id (str):
            Required. Project ID of the new routine
        dataset_id (str):
            Required. Dataset ID of the new routine
        routine (google.cloud.bigquery_v2.types.Routine):
            Required. A routine resource to insert
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    routine: "Routine" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Routine",
    )


class UpdateRoutineRequest(proto.Message):
    r"""Describes the format for updating a routine.

    Attributes:
        project_id (str):
            Required. Project ID of the routine to update
        dataset_id (str):
            Required. Dataset ID of the routine to update
        routine_id (str):
            Required. Routine ID of the routine to update
        routine (google.cloud.bigquery_v2.types.Routine):
            Required. A routine resource which will
            replace the specified routine
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    routine_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    routine: "Routine" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Routine",
    )


class PatchRoutineRequest(proto.Message):
    r"""Describes the format for the partial update (patch) of a
    routine.

    Attributes:
        project_id (str):
            Required. Project ID of the routine to update
        dataset_id (str):
            Required. Dataset ID of the routine to update
        routine_id (str):
            Required. Routine ID of the routine to update
        routine (google.cloud.bigquery_v2.types.Routine):
            Required. A routine resource which will be
            used to partially update the specified routine
        field_mask (google.protobuf.field_mask_pb2.FieldMask):
            Only the Routine fields in the field mask are
            updated by the given routine. Repeated routine
            fields will be fully replaced if contained in
            the field mask.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    routine_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    routine: "Routine" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Routine",
    )
    field_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=5,
        message=field_mask_pb2.FieldMask,
    )


class DeleteRoutineRequest(proto.Message):
    r"""Describes the format for deleting a routine.

    Attributes:
        project_id (str):
            Required. Project ID of the routine to delete
        dataset_id (str):
            Required. Dataset ID of the routine to delete
        routine_id (str):
            Required. Routine ID of the routine to delete
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    routine_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListRoutinesRequest(proto.Message):
    r"""Describes the format for listing routines.

    Attributes:
        project_id (str):
            Required. Project ID of the routines to list
        dataset_id (str):
            Required. Dataset ID of the routines to list
        max_results (google.protobuf.wrappers_pb2.UInt32Value):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results
        filter (str):
            If set, then only the Routines matching this filter are
            returned. The supported format is
            ``routineType:{RoutineType}``, where ``{RoutineType}`` is a
            RoutineType enum. For example:
            ``routineType:SCALAR_FUNCTION``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    max_results: wrappers_pb2.UInt32Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.UInt32Value,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListRoutinesResponse(proto.Message):
    r"""Describes the format of a single result page when listing
    routines.

    Attributes:
        routines (MutableSequence[google.cloud.bigquery_v2.types.Routine]):
            Routines in the requested dataset. Unless read_mask is set
            in the request, only the following fields are populated:
            etag, project_id, dataset_id, routine_id, routine_type,
            creation_time, last_modified_time, language, and
            remote_function_options.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    routines: MutableSequence["Routine"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Routine",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
