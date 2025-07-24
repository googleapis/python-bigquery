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

from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "TableSchema",
        "ForeignTypeInfo",
        "DataPolicyOption",
        "TableFieldSchema",
    },
)


class TableSchema(proto.Message):
    r"""Schema of a table

    Attributes:
        fields (MutableSequence[google.cloud.bigquery_v2.types.TableFieldSchema]):
            Describes the fields in a table.
        foreign_type_info (google.cloud.bigquery_v2.types.ForeignTypeInfo):
            Optional. Specifies metadata of the foreign data type
            definition in field schema
            ([TableFieldSchema.foreign_type_definition][google.cloud.bigquery.v2.TableFieldSchema.foreign_type_definition]).
    """

    fields: MutableSequence["TableFieldSchema"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TableFieldSchema",
    )
    foreign_type_info: "ForeignTypeInfo" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ForeignTypeInfo",
    )


class ForeignTypeInfo(proto.Message):
    r"""Metadata about the foreign data type definition such as the
    system in which the type is defined.

    Attributes:
        type_system (google.cloud.bigquery_v2.types.ForeignTypeInfo.TypeSystem):
            Required. Specifies the system which defines
            the foreign data type.
    """

    class TypeSystem(proto.Enum):
        r"""External systems, such as query engines or table formats,
        that have their own data types.

        Values:
            TYPE_SYSTEM_UNSPECIFIED (0):
                TypeSystem not specified.
            HIVE (1):
                Represents Hive data types.
        """
        TYPE_SYSTEM_UNSPECIFIED = 0
        HIVE = 1

    type_system: TypeSystem = proto.Field(
        proto.ENUM,
        number=1,
        enum=TypeSystem,
    )


class DataPolicyOption(proto.Message):
    r"""Data policy option proto, it currently supports name only,
    will support precedence later.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Data policy resource name in the form of
            projects/project_id/locations/location_id/dataPolicies/data_policy_id.

            This field is a member of `oneof`_ ``_name``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )


class TableFieldSchema(proto.Message):
    r"""A field in TableSchema

    Attributes:
        name (str):
            Required. The field name. The name must contain only letters
            (a-z, A-Z), numbers (0-9), or underscores (_), and must
            start with a letter or underscore. The maximum length is 300
            characters.
        type_ (str):
            Required. The field data type. Possible values include:

            -  STRING
            -  BYTES
            -  INTEGER (or INT64)
            -  FLOAT (or FLOAT64)
            -  BOOLEAN (or BOOL)
            -  TIMESTAMP
            -  DATE
            -  TIME
            -  DATETIME
            -  GEOGRAPHY
            -  NUMERIC
            -  BIGNUMERIC
            -  JSON
            -  RECORD (or STRUCT)
            -  RANGE

            Use of RECORD/STRUCT indicates that the field contains a
            nested schema.
        mode (str):
            Optional. The field mode. Possible values
            include NULLABLE, REQUIRED and REPEATED. The
            default value is NULLABLE.
        fields (MutableSequence[google.cloud.bigquery_v2.types.TableFieldSchema]):
            Optional. Describes the nested schema fields
            if the type property is set to RECORD.
        description (google.protobuf.wrappers_pb2.StringValue):
            Optional. The field description. The maximum
            length is 1,024 characters.
        policy_tags (google.cloud.bigquery_v2.types.TableFieldSchema.PolicyTagList):
            Optional. The policy tags attached to this field, used for
            field-level access control. If not set, defaults to empty
            policy_tags.
        data_policies (MutableSequence[google.cloud.bigquery_v2.types.DataPolicyOption]):
            Optional. Data policy options, will replace the
            data_policies.
        max_length (int):
            Optional. Maximum length of values of this field for STRINGS
            or BYTES.

            If max_length is not specified, no maximum length constraint
            is imposed on this field.

            If type = "STRING", then max_length represents the maximum
            UTF-8 length of strings in this field.

            If type = "BYTES", then max_length represents the maximum
            number of bytes in this field.

            It is invalid to set this field if type ≠ "STRING" and ≠
            "BYTES".
        precision (int):
            Optional. Precision (maximum number of total digits in base
            10) and scale (maximum number of digits in the fractional
            part in base 10) constraints for values of this field for
            NUMERIC or BIGNUMERIC.

            It is invalid to set precision or scale if type ≠ "NUMERIC"
            and ≠ "BIGNUMERIC".

            If precision and scale are not specified, no value range
            constraint is imposed on this field insofar as values are
            permitted by the type.

            Values of this NUMERIC or BIGNUMERIC field must be in this
            range when:

            -  Precision (P) and scale (S) are specified: [-10P-S +
               10-S, 10P-S - 10-S]
            -  Precision (P) is specified but not scale (and thus scale
               is interpreted to be equal to zero): [-10P + 1, 10P - 1].

            Acceptable values for precision and scale if both are
            specified:

            -  If type = "NUMERIC": 1 ≤ precision - scale ≤ 29 and 0 ≤
               scale ≤ 9.
            -  If type = "BIGNUMERIC": 1 ≤ precision - scale ≤ 38 and 0
               ≤ scale ≤ 38.

            Acceptable values for precision if only precision is
            specified but not scale (and thus scale is interpreted to be
            equal to zero):

            -  If type = "NUMERIC": 1 ≤ precision ≤ 29.
            -  If type = "BIGNUMERIC": 1 ≤ precision ≤ 38.

            If scale is specified but not precision, then it is invalid.
        scale (int):
            Optional. See documentation for precision.
        rounding_mode (google.cloud.bigquery_v2.types.TableFieldSchema.RoundingMode):
            Optional. Specifies the rounding mode to be
            used when storing values of NUMERIC and
            BIGNUMERIC type.
        collation (google.protobuf.wrappers_pb2.StringValue):
            Optional. Field collation can be set only when the type of
            field is STRING. The following values are supported:

            -  'und:ci': undetermined locale, case insensitive.
            -  '': empty string. Default to case-sensitive behavior.
        default_value_expression (google.protobuf.wrappers_pb2.StringValue):
            Optional. A SQL expression to specify the [default value]
            (https://cloud.google.com/bigquery/docs/default-values) for
            this field.
        range_element_type (google.cloud.bigquery_v2.types.TableFieldSchema.FieldElementType):
            Optional. The subtype of the RANGE, if the type of this
            field is RANGE. If the type is RANGE, this field is
            required. Values for the field element type can be the
            following:

            -  DATE
            -  DATETIME
            -  TIMESTAMP
        foreign_type_definition (str):
            Optional. Definition of the foreign data
            type. Only valid for top-level schema fields
            (not nested fields). If the type is FOREIGN,
            this field is required.
    """

    class RoundingMode(proto.Enum):
        r"""Rounding mode options that can be used when storing NUMERIC
        or BIGNUMERIC values.

        Values:
            ROUNDING_MODE_UNSPECIFIED (0):
                Unspecified will default to using ROUND_HALF_AWAY_FROM_ZERO.
            ROUND_HALF_AWAY_FROM_ZERO (1):
                ROUND_HALF_AWAY_FROM_ZERO rounds half values away from zero
                when applying precision and scale upon writing of NUMERIC
                and BIGNUMERIC values. For Scale: 0 1.1, 1.2, 1.3, 1.4 => 1
                1.5, 1.6, 1.7, 1.8, 1.9 => 2
            ROUND_HALF_EVEN (2):
                ROUND_HALF_EVEN rounds half values to the nearest even value
                when applying precision and scale upon writing of NUMERIC
                and BIGNUMERIC values. For Scale: 0 1.1, 1.2, 1.3, 1.4 => 1
                1.5 => 2 1.6, 1.7, 1.8, 1.9 => 2 2.5 => 2
        """
        ROUNDING_MODE_UNSPECIFIED = 0
        ROUND_HALF_AWAY_FROM_ZERO = 1
        ROUND_HALF_EVEN = 2

    class PolicyTagList(proto.Message):
        r"""

        Attributes:
            names (MutableSequence[str]):
                A list of policy tag resource names. For
                example,
                "projects/1/locations/eu/taxonomies/2/policyTags/3".
                At most 1 policy tag is currently allowed.
        """

        names: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class FieldElementType(proto.Message):
        r"""Represents the type of a field element.

        Attributes:
            type_ (str):
                Required. The type of a field element. For more information,
                see
                [TableFieldSchema.type][google.cloud.bigquery.v2.TableFieldSchema.type].
        """

        type_: str = proto.Field(
            proto.STRING,
            number=1,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=2,
    )
    mode: str = proto.Field(
        proto.STRING,
        number=3,
    )
    fields: MutableSequence["TableFieldSchema"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="TableFieldSchema",
    )
    description: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.StringValue,
    )
    policy_tags: PolicyTagList = proto.Field(
        proto.MESSAGE,
        number=9,
        message=PolicyTagList,
    )
    data_policies: MutableSequence["DataPolicyOption"] = proto.RepeatedField(
        proto.MESSAGE,
        number=21,
        message="DataPolicyOption",
    )
    max_length: int = proto.Field(
        proto.INT64,
        number=10,
    )
    precision: int = proto.Field(
        proto.INT64,
        number=11,
    )
    scale: int = proto.Field(
        proto.INT64,
        number=12,
    )
    rounding_mode: RoundingMode = proto.Field(
        proto.ENUM,
        number=15,
        enum=RoundingMode,
    )
    collation: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=13,
        message=wrappers_pb2.StringValue,
    )
    default_value_expression: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=14,
        message=wrappers_pb2.StringValue,
    )
    range_element_type: FieldElementType = proto.Field(
        proto.MESSAGE,
        number=18,
        message=FieldElementType,
    )
    foreign_type_definition: str = proto.Field(
        proto.STRING,
        number=23,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
