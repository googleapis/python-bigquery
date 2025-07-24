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


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "AggregationThresholdPolicy",
        "DifferentialPrivacyPolicy",
        "JoinRestrictionPolicy",
        "PrivacyPolicy",
    },
)


class AggregationThresholdPolicy(proto.Message):
    r"""Represents privacy policy associated with "aggregation
    threshold" method.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        threshold (int):
            Optional. The threshold for the "aggregation
            threshold" policy.

            This field is a member of `oneof`_ ``_threshold``.
        privacy_unit_columns (MutableSequence[str]):
            Optional. The privacy unit column(s)
            associated with this policy. For now, only one
            column per data source object (table, view) is
            allowed as a privacy unit column.
            Representing as a repeated field in metadata for
            extensibility to multiple columns in future.
            Duplicates and Repeated struct fields are not
            allowed. For nested fields, use dot notation
            ("outer.inner")
    """

    threshold: int = proto.Field(
        proto.INT64,
        number=1,
        optional=True,
    )
    privacy_unit_columns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class DifferentialPrivacyPolicy(proto.Message):
    r"""Represents privacy policy associated with "differential
    privacy" method.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        max_epsilon_per_query (float):
            Optional. The maximum epsilon value that a
            query can consume. If the subscriber specifies
            epsilon as a parameter in a SELECT query, it
            must be less than or equal to this value. The
            epsilon parameter controls the amount of noise
            that is added to the groups — a higher epsilon
            means less noise.

            This field is a member of `oneof`_ ``_max_epsilon_per_query``.
        delta_per_query (float):
            Optional. The delta value that is used per
            query. Delta represents the probability that any
            row will fail to be epsilon differentially
            private. Indicates the risk associated with
            exposing aggregate rows in the result of a
            query.

            This field is a member of `oneof`_ ``_delta_per_query``.
        max_groups_contributed (int):
            Optional. The maximum groups contributed
            value that is used per query. Represents the
            maximum number of groups to which each protected
            entity can contribute. Changing this value does
            not improve or worsen privacy. The best value
            for accuracy and utility depends on the query
            and data.

            This field is a member of `oneof`_ ``_max_groups_contributed``.
        privacy_unit_column (str):
            Optional. The privacy unit column associated
            with this policy. Differential privacy policies
            can only have one privacy unit column per data
            source object (table, view).

            This field is a member of `oneof`_ ``_privacy_unit_column``.
        epsilon_budget (float):
            Optional. The total epsilon budget for all
            queries against the privacy-protected view. Each
            subscriber query against this view charges the
            amount of epsilon they request in their query.
            If there is sufficient budget, then the
            subscriber query attempts to complete. It might
            still fail due to other reasons, in which case
            the charge is refunded. If there is insufficient
            budget the query is rejected. There might be
            multiple charge attempts if a single query
            references multiple views. In this case there
            must be sufficient budget for all charges or the
            query is rejected and charges are refunded in
            best effort. The budget does not have a refresh
            policy and can only be updated via ALTER VIEW or
            circumvented by creating a new view that can be
            queried with a fresh budget.

            This field is a member of `oneof`_ ``_epsilon_budget``.
        delta_budget (float):
            Optional. The total delta budget for all queries against the
            privacy-protected view. Each subscriber query against this
            view charges the amount of delta that is pre-defined by the
            contributor through the privacy policy delta_per_query
            field. If there is sufficient budget, then the subscriber
            query attempts to complete. It might still fail due to other
            reasons, in which case the charge is refunded. If there is
            insufficient budget the query is rejected. There might be
            multiple charge attempts if a single query references
            multiple views. In this case there must be sufficient budget
            for all charges or the query is rejected and charges are
            refunded in best effort. The budget does not have a refresh
            policy and can only be updated via ALTER VIEW or
            circumvented by creating a new view that can be queried with
            a fresh budget.

            This field is a member of `oneof`_ ``_delta_budget``.
        epsilon_budget_remaining (float):
            Output only. The epsilon budget remaining. If
            budget is exhausted, no more queries are
            allowed. Note that the budget for queries that
            are in progress is deducted before the query
            executes. If the query fails or is cancelled
            then the budget is refunded. In this case the
            amount of budget remaining can increase.

            This field is a member of `oneof`_ ``_epsilon_budget_remaining``.
        delta_budget_remaining (float):
            Output only. The delta budget remaining. If
            budget is exhausted, no more queries are
            allowed. Note that the budget for queries that
            are in progress is deducted before the query
            executes. If the query fails or is cancelled
            then the budget is refunded. In this case the
            amount of budget remaining can increase.

            This field is a member of `oneof`_ ``_delta_budget_remaining``.
    """

    max_epsilon_per_query: float = proto.Field(
        proto.DOUBLE,
        number=1,
        optional=True,
    )
    delta_per_query: float = proto.Field(
        proto.DOUBLE,
        number=2,
        optional=True,
    )
    max_groups_contributed: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    privacy_unit_column: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    epsilon_budget: float = proto.Field(
        proto.DOUBLE,
        number=5,
        optional=True,
    )
    delta_budget: float = proto.Field(
        proto.DOUBLE,
        number=6,
        optional=True,
    )
    epsilon_budget_remaining: float = proto.Field(
        proto.DOUBLE,
        number=7,
        optional=True,
    )
    delta_budget_remaining: float = proto.Field(
        proto.DOUBLE,
        number=8,
        optional=True,
    )


class JoinRestrictionPolicy(proto.Message):
    r"""Represents privacy policy associated with "join restrictions". Join
    restriction gives data providers the ability to enforce joins on the
    'join_allowed_columns' when data is queried from a privacy protected
    view.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        join_condition (google.cloud.bigquery_v2.types.JoinRestrictionPolicy.JoinCondition):
            Optional. Specifies if a join is required or not on queries
            for the view. Default is JOIN_CONDITION_UNSPECIFIED.

            This field is a member of `oneof`_ ``_join_condition``.
        join_allowed_columns (MutableSequence[str]):
            Optional. The only columns that joins are allowed on. This
            field is must be specified for join_conditions JOIN_ANY and
            JOIN_ALL and it cannot be set for JOIN_BLOCKED.
    """

    class JoinCondition(proto.Enum):
        r"""Enum for Join Restrictions policy.

        Values:
            JOIN_CONDITION_UNSPECIFIED (0):
                A join is neither required nor restricted on
                any column. Default value.
            JOIN_ANY (1):
                A join is required on at least one of the
                specified columns.
            JOIN_ALL (2):
                A join is required on all specified columns.
            JOIN_NOT_REQUIRED (3):
                A join is not required, but if present it is only permitted
                on 'join_allowed_columns'
            JOIN_BLOCKED (4):
                Joins are blocked for all queries.
        """
        JOIN_CONDITION_UNSPECIFIED = 0
        JOIN_ANY = 1
        JOIN_ALL = 2
        JOIN_NOT_REQUIRED = 3
        JOIN_BLOCKED = 4

    join_condition: JoinCondition = proto.Field(
        proto.ENUM,
        number=1,
        optional=True,
        enum=JoinCondition,
    )
    join_allowed_columns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class PrivacyPolicy(proto.Message):
    r"""Represents privacy policy that contains the privacy
    requirements specified by the data owner. Currently, this is
    only supported on views.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        aggregation_threshold_policy (google.cloud.bigquery_v2.types.AggregationThresholdPolicy):
            Optional. Policy used for aggregation
            thresholds.

            This field is a member of `oneof`_ ``privacy_policy``.
        differential_privacy_policy (google.cloud.bigquery_v2.types.DifferentialPrivacyPolicy):
            Optional. Policy used for differential
            privacy.

            This field is a member of `oneof`_ ``privacy_policy``.
        join_restriction_policy (google.cloud.bigquery_v2.types.JoinRestrictionPolicy):
            Optional. Join restriction policy is outside of the one of
            policies, since this policy can be set along with other
            policies. This policy gives data providers the ability to
            enforce joins on the 'join_allowed_columns' when data is
            queried from a privacy protected view.

            This field is a member of `oneof`_ ``_join_restriction_policy``.
    """

    aggregation_threshold_policy: "AggregationThresholdPolicy" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="privacy_policy",
        message="AggregationThresholdPolicy",
    )
    differential_privacy_policy: "DifferentialPrivacyPolicy" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="privacy_policy",
        message="DifferentialPrivacyPolicy",
    )
    join_restriction_policy: "JoinRestrictionPolicy" = proto.Field(
        proto.MESSAGE,
        number=1,
        optional=True,
        message="JoinRestrictionPolicy",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
