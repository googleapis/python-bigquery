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

from google.cloud.bigquery_v2.types import (
    row_access_policy_reference as gcb_row_access_policy_reference,
)
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "ListRowAccessPoliciesRequest",
        "ListRowAccessPoliciesResponse",
        "GetRowAccessPolicyRequest",
        "CreateRowAccessPolicyRequest",
        "UpdateRowAccessPolicyRequest",
        "DeleteRowAccessPolicyRequest",
        "BatchDeleteRowAccessPoliciesRequest",
        "RowAccessPolicy",
    },
)


class ListRowAccessPoliciesRequest(proto.Message):
    r"""Request message for the ListRowAccessPolicies method.

    Attributes:
        project_id (str):
            Required. Project ID of the row access
            policies to list.
        dataset_id (str):
            Required. Dataset ID of row access policies
            to list.
        table_id (str):
            Required. Table ID of the table to list row
            access policies.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results.
        page_size (int):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=5,
    )


class ListRowAccessPoliciesResponse(proto.Message):
    r"""Response message for the ListRowAccessPolicies method.

    Attributes:
        row_access_policies (MutableSequence[google.cloud.bigquery_v2.types.RowAccessPolicy]):
            Row access policies on the requested table.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    row_access_policies: MutableSequence["RowAccessPolicy"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RowAccessPolicy",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetRowAccessPolicyRequest(proto.Message):
    r"""Request message for the GetRowAccessPolicy method.

    Attributes:
        project_id (str):
            Required. Project ID of the table to get the
            row access policy.
        dataset_id (str):
            Required. Dataset ID of the table to get the
            row access policy.
        table_id (str):
            Required. Table ID of the table to get the
            row access policy.
        policy_id (str):
            Required. Policy ID of the row access policy.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    policy_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class CreateRowAccessPolicyRequest(proto.Message):
    r"""Request message for the CreateRowAccessPolicy method.

    Attributes:
        project_id (str):
            Required. Project ID of the table to get the
            row access policy.
        dataset_id (str):
            Required. Dataset ID of the table to get the
            row access policy.
        table_id (str):
            Required. Table ID of the table to get the
            row access policy.
        row_access_policy (google.cloud.bigquery_v2.types.RowAccessPolicy):
            Required. The row access policy to create.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    row_access_policy: "RowAccessPolicy" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="RowAccessPolicy",
    )


class UpdateRowAccessPolicyRequest(proto.Message):
    r"""Request message for the UpdateRowAccessPolicy method.

    Attributes:
        project_id (str):
            Required. Project ID of the table to get the
            row access policy.
        dataset_id (str):
            Required. Dataset ID of the table to get the
            row access policy.
        table_id (str):
            Required. Table ID of the table to get the
            row access policy.
        policy_id (str):
            Required. Policy ID of the row access policy.
        row_access_policy (google.cloud.bigquery_v2.types.RowAccessPolicy):
            Required. The row access policy to update.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    policy_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    row_access_policy: "RowAccessPolicy" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="RowAccessPolicy",
    )


class DeleteRowAccessPolicyRequest(proto.Message):
    r"""Request message for the DeleteRowAccessPolicy method.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. Project ID of the table to delete
            the row access policy.
        dataset_id (str):
            Required. Dataset ID of the table to delete
            the row access policy.
        table_id (str):
            Required. Table ID of the table to delete the
            row access policy.
        policy_id (str):
            Required. Policy ID of the row access policy.
        force (bool):
            If set to true, it deletes the row access
            policy even if it's the last row access policy
            on the table and the deletion will widen the
            access rather narrowing it.

            This field is a member of `oneof`_ ``_force``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    policy_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=5,
        optional=True,
    )


class BatchDeleteRowAccessPoliciesRequest(proto.Message):
    r"""Request message for the BatchDeleteRowAccessPoliciesRequest
    method.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. Project ID of the table to delete
            the row access policies.
        dataset_id (str):
            Required. Dataset ID of the table to delete
            the row access policies.
        table_id (str):
            Required. Table ID of the table to delete the
            row access policies.
        policy_ids (MutableSequence[str]):
            Required. Policy IDs of the row access
            policies.
        force (bool):
            If set to true, it deletes the row access
            policy even if it's the last row access policy
            on the table and the deletion will widen the
            access rather narrowing it.

            This field is a member of `oneof`_ ``_force``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    policy_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=5,
        optional=True,
    )


class RowAccessPolicy(proto.Message):
    r"""Represents access on a subset of rows on the specified table,
    defined by its filter predicate. Access to the subset of rows is
    controlled by its IAM policy.

    Attributes:
        etag (str):
            Output only. A hash of this resource.
        row_access_policy_reference (google.cloud.bigquery_v2.types.RowAccessPolicyReference):
            Required. Reference describing the ID of this
            row access policy.
        filter_predicate (str):
            Required. A SQL boolean expression that represents the rows
            defined by this row access policy, similar to the boolean
            expression in a WHERE clause of a SELECT query on a table.
            References to other tables, routines, and temporary
            functions are not supported.

            Examples: region="EU" date_field = CAST('2019-9-27' as DATE)
            nullable_field is not NULL numeric_field BETWEEN 1.0 AND 5.0
        creation_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when this row access
            policy was created, in milliseconds since the
            epoch.
        last_modified_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when this row access
            policy was last modified, in milliseconds since
            the epoch.
        grantees (MutableSequence[str]):
            Optional. Input only. The optional list of iam_member users
            or groups that specifies the initial members that the
            row-level access policy should be created with.

            grantees types:

            -  "user:alice@example.com": An email address that
               represents a specific Google account.
            -  "serviceAccount:my-other-app@appspot.gserviceaccount.com":
               An email address that represents a service account.
            -  "group:admins@example.com": An email address that
               represents a Google group.
            -  "domain:example.com":The Google Workspace domain
               (primary) that represents all the users of that domain.
            -  "allAuthenticatedUsers": A special identifier that
               represents all service accounts and all users on the
               internet who have authenticated with a Google Account.
               This identifier includes accounts that aren't connected
               to a Google Workspace or Cloud Identity domain, such as
               personal Gmail accounts. Users who aren't authenticated,
               such as anonymous visitors, aren't included.
            -  "allUsers":A special identifier that represents anyone
               who is on the internet, including authenticated and
               unauthenticated users. Because BigQuery requires
               authentication before a user can access the service,
               allUsers includes only authenticated users.
    """

    etag: str = proto.Field(
        proto.STRING,
        number=1,
    )
    row_access_policy_reference: gcb_row_access_policy_reference.RowAccessPolicyReference = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcb_row_access_policy_reference.RowAccessPolicyReference,
    )
    filter_predicate: str = proto.Field(
        proto.STRING,
        number=3,
    )
    creation_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    last_modified_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    grantees: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
