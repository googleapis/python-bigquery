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

from google.cloud.bigquery_v2.types import dataset_reference as gcb_dataset_reference
from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import (
    external_catalog_dataset_options as gcb_external_catalog_dataset_options,
)
from google.cloud.bigquery_v2.types import (
    external_dataset_reference as gcb_external_dataset_reference,
)
from google.cloud.bigquery_v2.types import restriction_config
from google.cloud.bigquery_v2.types import routine_reference
from google.cloud.bigquery_v2.types import table_reference
from google.cloud.bigquery_v2.types import table_schema
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "DatasetAccessEntry",
        "Access",
        "Dataset",
        "GcpTag",
        "LinkedDatasetSource",
        "LinkedDatasetMetadata",
        "GetDatasetRequest",
        "InsertDatasetRequest",
        "UpdateOrPatchDatasetRequest",
        "DeleteDatasetRequest",
        "ListDatasetsRequest",
        "ListFormatDataset",
        "DatasetList",
        "UndeleteDatasetRequest",
    },
)


class DatasetAccessEntry(proto.Message):
    r"""Grants all resources of particular types in a particular
    dataset read access to the current dataset.

    Similar to how individually authorized views work, updates to
    any resource granted through its dataset (including creation of
    new resources) requires read permission to referenced resources,
    plus write permission to the authorizing dataset.

    Attributes:
        dataset (google.cloud.bigquery_v2.types.DatasetReference):
            The dataset this entry applies to
        target_types (MutableSequence[google.cloud.bigquery_v2.types.DatasetAccessEntry.TargetType]):
            Which resources in the dataset this entry
            applies to. Currently, only views are supported,
            but additional target types may be added in the
            future.
    """

    class TargetType(proto.Enum):
        r"""Indicates the type of resources in a dataset that the entry
        applies to.

        Values:
            TARGET_TYPE_UNSPECIFIED (0):
                Do not use. You must set a target type
                explicitly.
            VIEWS (1):
                This entry applies to views in the dataset.
            ROUTINES (2):
                This entry applies to routines in the
                dataset.
        """
        TARGET_TYPE_UNSPECIFIED = 0
        VIEWS = 1
        ROUTINES = 2

    dataset: gcb_dataset_reference.DatasetReference = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcb_dataset_reference.DatasetReference,
    )
    target_types: MutableSequence[TargetType] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=TargetType,
    )


class Access(proto.Message):
    r"""An object that defines dataset access for an entity.

    Attributes:
        role (str):
            An IAM role ID that should be granted to the user, group, or
            domain specified in this access entry. The following legacy
            mappings will be applied:

            -  ``OWNER``: ``roles/bigquery.dataOwner``
            -  ``WRITER``: ``roles/bigquery.dataEditor``
            -  ``READER``: ``roles/bigquery.dataViewer``

            This field will accept any of the above formats, but will
            return only the legacy format. For example, if you set this
            field to "roles/bigquery.dataOwner", it will be returned
            back as "OWNER".
        user_by_email (str):
            [Pick one] An email address of a user to grant access to.
            For example: fred@example.com. Maps to IAM policy member
            "user:EMAIL" or "serviceAccount:EMAIL".
        group_by_email (str):
            [Pick one] An email address of a Google Group to grant
            access to. Maps to IAM policy member "group:GROUP".
        domain (str):
            [Pick one] A domain to grant access to. Any users signed in
            with the domain specified will be granted the specified
            access. Example: "example.com". Maps to IAM policy member
            "domain:DOMAIN".
        special_group (str):
            [Pick one] A special group to grant access to. Possible
            values include:

            -  projectOwners: Owners of the enclosing project.
            -  projectReaders: Readers of the enclosing project.
            -  projectWriters: Writers of the enclosing project.
            -  allAuthenticatedUsers: All authenticated BigQuery users.

            Maps to similarly-named IAM members.
        iam_member (str):
            [Pick one] Some other type of member that appears in the IAM
            Policy but isn't a user, group, domain, or special group.
        view (google.cloud.bigquery_v2.types.TableReference):
            [Pick one] A view from a different dataset to grant access
            to. Queries executed against that view will have read access
            to views/tables/routines in this dataset. The role field is
            not required when this field is set. If that view is updated
            by any user, access to the view needs to be granted again
            via an update operation.
        routine (google.cloud.bigquery_v2.types.RoutineReference):
            [Pick one] A routine from a different dataset to grant
            access to. Queries executed against that routine will have
            read access to views/tables/routines in this dataset. Only
            UDF is supported for now. The role field is not required
            when this field is set. If that routine is updated by any
            user, access to the routine needs to be granted again via an
            update operation.
        dataset (google.cloud.bigquery_v2.types.DatasetAccessEntry):
            [Pick one] A grant authorizing all resources of a particular
            type in a particular dataset access to this dataset. Only
            views are supported for now. The role field is not required
            when this field is set. If that dataset is deleted and
            re-created, its access needs to be granted again via an
            update operation.
        condition (google.type.expr_pb2.Expr):
            Optional. condition for the binding. If CEL
            expression in this field is true, this access
            binding will be considered
    """

    role: str = proto.Field(
        proto.STRING,
        number=1,
    )
    user_by_email: str = proto.Field(
        proto.STRING,
        number=2,
    )
    group_by_email: str = proto.Field(
        proto.STRING,
        number=3,
    )
    domain: str = proto.Field(
        proto.STRING,
        number=4,
    )
    special_group: str = proto.Field(
        proto.STRING,
        number=5,
    )
    iam_member: str = proto.Field(
        proto.STRING,
        number=7,
    )
    view: table_reference.TableReference = proto.Field(
        proto.MESSAGE,
        number=6,
        message=table_reference.TableReference,
    )
    routine: routine_reference.RoutineReference = proto.Field(
        proto.MESSAGE,
        number=8,
        message=routine_reference.RoutineReference,
    )
    dataset: "DatasetAccessEntry" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="DatasetAccessEntry",
    )
    condition: expr_pb2.Expr = proto.Field(
        proto.MESSAGE,
        number=10,
        message=expr_pb2.Expr,
    )


class Dataset(proto.Message):
    r"""Represents a BigQuery dataset.

    Attributes:
        kind (str):
            Output only. The resource type.
        etag (str):
            Output only. A hash of the resource.
        id (str):
            Output only. The fully-qualified unique name
            of the dataset in the format
            projectId:datasetId. The dataset name without
            the project name is given in the datasetId
            field. When creating a new dataset, leave this
            field blank, and instead specify the datasetId
            field.
        self_link (str):
            Output only. A URL that can be used to access
            the resource again. You can use this URL in Get
            or Update requests to the resource.
        dataset_reference (google.cloud.bigquery_v2.types.DatasetReference):
            Required. A reference that identifies the
            dataset.
        friendly_name (google.protobuf.wrappers_pb2.StringValue):
            Optional. A descriptive name for the dataset.
        description (google.protobuf.wrappers_pb2.StringValue):
            Optional. A user-friendly description of the
            dataset.
        default_table_expiration_ms (google.protobuf.wrappers_pb2.Int64Value):
            Optional. The default lifetime of all tables
            in the dataset, in milliseconds. The minimum
            lifetime value is 3600000 milliseconds (one
            hour). To clear an existing default expiration
            with a PATCH request, set to
            0. Once this property is set, all newly-created
                tables in the dataset will have an
                expirationTime property set to the creation
                time plus the value in this property, and
                changing the value will only affect new
                tables, not existing ones. When the
                expirationTime for a given table is reached,
                that table will be deleted automatically.
            If a table's expirationTime is modified or
            removed before the table expires, or if you
            provide an explicit expirationTime when creating
            a table, that value takes precedence over the
            default expiration time indicated by this
            property.
        default_partition_expiration_ms (google.protobuf.wrappers_pb2.Int64Value):
            This default partition expiration, expressed in
            milliseconds.

            When new time-partitioned tables are created in a dataset
            where this property is set, the table will inherit this
            value, propagated as the ``TimePartitioning.expirationMs``
            property on the new table. If you set
            ``TimePartitioning.expirationMs`` explicitly when creating a
            table, the ``defaultPartitionExpirationMs`` of the
            containing dataset is ignored.

            When creating a partitioned table, if
            ``defaultPartitionExpirationMs`` is set, the
            ``defaultTableExpirationMs`` value is ignored and the table
            will not be inherit a table expiration deadline.
        default_partition_expiration_ms (google.protobuf.wrappers_pb2.Int64Value):
            This default partition expiration, expressed in
            milliseconds.
        labels (MutableMapping[str, str]):
            The labels associated with this dataset. You can use these
            to organize and group your datasets. You can set this
            property when inserting or updating a dataset. See `Creating
            and Updating Dataset
            Labels <https://cloud.google.com/bigquery/docs/creating-managing-labels#creating_and_updating_dataset_labels>`__
            for more information.
        access (MutableSequence[google.cloud.bigquery_v2.types.Access]):
            Optional. An array of objects that define dataset access for
            one or more entities. You can set this property when
            inserting or updating a dataset in order to control who is
            allowed to access the data. If unspecified at dataset
            creation time, BigQuery adds default dataset access for the
            following entities: access.specialGroup: projectReaders;
            access.role: READER; access.specialGroup: projectWriters;
            access.role: WRITER; access.specialGroup: projectOwners;
            access.role: OWNER; access.userByEmail: [dataset creator
            email]; access.role: OWNER; If you patch a dataset, then
            this field is overwritten by the patched dataset's access
            field. To add entities, you must supply the entire existing
            access array in addition to any new entities that you want
            to add.
        creation_time (int):
            Output only. The time when this dataset was
            created, in milliseconds since the epoch.
        last_modified_time (int):
            Output only. The date when this dataset was
            last modified, in milliseconds since the epoch.
        location (str):
            The geographic location where the dataset
            should reside. See
            https://cloud.google.com/bigquery/docs/locations
            for supported locations.
        default_encryption_configuration (google.cloud.bigquery_v2.types.EncryptionConfiguration):
            The default encryption key for all tables in
            the dataset. After this property is set, the
            encryption key of all newly-created tables in
            the dataset is set to this value unless the
            table creation request or query explicitly
            overrides the key.
        satisfies_pzs (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Reserved for future use.
        satisfies_pzi (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Reserved for future use.
        type_ (str):
            Output only. Same as ``type`` in ``ListFormatDataset``. The
            type of the dataset, one of:

            -  DEFAULT - only accessible by owner and authorized
               accounts,
            -  PUBLIC - accessible by everyone,
            -  LINKED - linked dataset,
            -  EXTERNAL - dataset with definition in external metadata
               catalog.
        linked_dataset_source (google.cloud.bigquery_v2.types.LinkedDatasetSource):
            Optional. The source dataset reference when
            the dataset is of type LINKED. For all other
            dataset types it is not set. This field cannot
            be updated once it is set. Any attempt to update
            this field using Update and Patch API Operations
            will be ignored.
        linked_dataset_metadata (google.cloud.bigquery_v2.types.LinkedDatasetMetadata):
            Output only. Metadata about the
            LinkedDataset. Filled out when the dataset type
            is LINKED.
        external_dataset_reference (google.cloud.bigquery_v2.types.ExternalDatasetReference):
            Optional. Reference to a read-only external
            dataset defined in data catalogs outside of
            BigQuery. Filled out when the dataset type is
            EXTERNAL.
        external_catalog_dataset_options (google.cloud.bigquery_v2.types.ExternalCatalogDatasetOptions):
            Optional. Options defining open source
            compatible datasets living in the BigQuery
            catalog. Contains metadata of open source
            database, schema or namespace represented by the
            current dataset.
        is_case_insensitive (google.protobuf.wrappers_pb2.BoolValue):
            Optional. TRUE if the dataset and its table
            names are case-insensitive, otherwise FALSE. By
            default, this is FALSE, which means the dataset
            and its table names are case-sensitive. This
            field does not affect routine references.
        default_collation (google.protobuf.wrappers_pb2.StringValue):
            Optional. Defines the default collation specification of
            future tables created in the dataset. If a table is created
            in this dataset without table-level default collation, then
            the table inherits the dataset default collation, which is
            applied to the string fields that do not have explicit
            collation specified. A change to this field affects only
            tables created afterwards, and does not alter the existing
            tables. The following values are supported:

            -  'und:ci': undetermined locale, case insensitive.
            -  '': empty string. Default to case-sensitive behavior.
        default_rounding_mode (google.cloud.bigquery_v2.types.TableFieldSchema.RoundingMode):
            Optional. Defines the default rounding mode
            specification of new tables created within this
            dataset. During table creation, if this field is
            specified, the table within this dataset will
            inherit the default rounding mode of the
            dataset. Setting the default rounding mode on a
            table overrides this option. Existing tables in
            the dataset are unaffected. If columns are
            defined during that table creation, they will
            immediately inherit the table's default rounding
            mode, unless otherwise specified.
        max_time_travel_hours (google.protobuf.wrappers_pb2.Int64Value):
            Optional. Defines the time travel window in
            hours. The value can be from 48 to 168 hours (2
            to 7 days). The default value is 168 hours if
            this is not set.
        tags (MutableSequence[google.cloud.bigquery_v2.types.GcpTag]):
            Output only. Tags for the dataset. To provide tags as
            inputs, use the ``resourceTags`` field.
        storage_billing_model (google.cloud.bigquery_v2.types.Dataset.StorageBillingModel):
            Optional. Updates storage_billing_model for the dataset.
        restrictions (google.cloud.bigquery_v2.types.RestrictionConfig):
            Optional. Output only. Restriction config for all tables and
            dataset. If set, restrict certain accesses on the dataset
            and all its tables based on the config. See `Data
            egress <https://cloud.google.com/bigquery/docs/analytics-hub-introduction#data_egress>`__
            for more details.
        resource_tags (MutableMapping[str, str]):
            Optional. The
            `tags <https://cloud.google.com/bigquery/docs/tags>`__
            attached to this dataset. Tag keys are globally unique. Tag
            key is expected to be in the namespaced format, for example
            "123456789012/environment" where 123456789012 is the ID of
            the parent organization or project resource for this tag
            key. Tag value is expected to be the short name, for example
            "Production". See `Tag
            definitions <https://cloud.google.com/iam/docs/tags-access-control#definitions>`__
            for more details.
    """

    class StorageBillingModel(proto.Enum):
        r"""Indicates the billing model that will be applied to the
        dataset.

        Values:
            STORAGE_BILLING_MODEL_UNSPECIFIED (0):
                Value not set.
            LOGICAL (1):
                Billing for logical bytes.
            PHYSICAL (2):
                Billing for physical bytes.
        """
        STORAGE_BILLING_MODEL_UNSPECIFIED = 0
        LOGICAL = 1
        PHYSICAL = 2

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )
    id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    self_link: str = proto.Field(
        proto.STRING,
        number=4,
    )
    dataset_reference: gcb_dataset_reference.DatasetReference = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gcb_dataset_reference.DatasetReference,
    )
    friendly_name: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.StringValue,
    )
    description: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.StringValue,
    )
    default_table_expiration_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=8,
        message=wrappers_pb2.Int64Value,
    )
    default_partition_expiration_ms: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=14,
        message=wrappers_pb2.Int64Value,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    access: MutableSequence["Access"] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message="Access",
    )
    creation_time: int = proto.Field(
        proto.INT64,
        number=11,
    )
    last_modified_time: int = proto.Field(
        proto.INT64,
        number=12,
    )
    location: str = proto.Field(
        proto.STRING,
        number=13,
    )
    default_encryption_configuration: encryption_config.EncryptionConfiguration = (
        proto.Field(
            proto.MESSAGE,
            number=16,
            message=encryption_config.EncryptionConfiguration,
        )
    )
    satisfies_pzs: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=17,
        message=wrappers_pb2.BoolValue,
    )
    satisfies_pzi: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=31,
        message=wrappers_pb2.BoolValue,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=18,
    )
    linked_dataset_source: "LinkedDatasetSource" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="LinkedDatasetSource",
    )
    linked_dataset_metadata: "LinkedDatasetMetadata" = proto.Field(
        proto.MESSAGE,
        number=29,
        message="LinkedDatasetMetadata",
    )
    external_dataset_reference: gcb_external_dataset_reference.ExternalDatasetReference = proto.Field(
        proto.MESSAGE,
        number=20,
        message=gcb_external_dataset_reference.ExternalDatasetReference,
    )
    external_catalog_dataset_options: gcb_external_catalog_dataset_options.ExternalCatalogDatasetOptions = proto.Field(
        proto.MESSAGE,
        number=32,
        message=gcb_external_catalog_dataset_options.ExternalCatalogDatasetOptions,
    )
    is_case_insensitive: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=21,
        message=wrappers_pb2.BoolValue,
    )
    default_collation: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=22,
        message=wrappers_pb2.StringValue,
    )
    default_rounding_mode: table_schema.TableFieldSchema.RoundingMode = proto.Field(
        proto.ENUM,
        number=26,
        enum=table_schema.TableFieldSchema.RoundingMode,
    )
    max_time_travel_hours: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=23,
        message=wrappers_pb2.Int64Value,
    )
    tags: MutableSequence["GcpTag"] = proto.RepeatedField(
        proto.MESSAGE,
        number=24,
        message="GcpTag",
    )
    storage_billing_model: StorageBillingModel = proto.Field(
        proto.ENUM,
        number=25,
        enum=StorageBillingModel,
    )
    restrictions: restriction_config.RestrictionConfig = proto.Field(
        proto.MESSAGE,
        number=27,
        message=restriction_config.RestrictionConfig,
    )
    resource_tags: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=30,
    )


class GcpTag(proto.Message):
    r"""A global tag managed by Resource Manager.
    https://cloud.google.com/iam/docs/tags-access-control#definitions

    Attributes:
        tag_key (str):
            Required. The namespaced friendly name of the
            tag key, e.g. "12345/environment" where 12345 is
            org id.
        tag_value (str):
            Required. The friendly short name of the tag
            value, e.g. "production".
    """

    tag_key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tag_value: str = proto.Field(
        proto.STRING,
        number=2,
    )


class LinkedDatasetSource(proto.Message):
    r"""A dataset source type which refers to another BigQuery
    dataset.

    Attributes:
        source_dataset (google.cloud.bigquery_v2.types.DatasetReference):
            The source dataset reference contains project
            numbers and not project ids.
    """

    source_dataset: gcb_dataset_reference.DatasetReference = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcb_dataset_reference.DatasetReference,
    )


class LinkedDatasetMetadata(proto.Message):
    r"""Metadata about the Linked Dataset.

    Attributes:
        link_state (google.cloud.bigquery_v2.types.LinkedDatasetMetadata.LinkState):
            Output only. Specifies whether Linked Dataset
            is currently in a linked state or not.
    """

    class LinkState(proto.Enum):
        r"""Specifies whether Linked Dataset is currently in a linked
        state or not.

        Values:
            LINK_STATE_UNSPECIFIED (0):
                The default value.
                Default to the LINKED state.
            LINKED (1):
                Normal Linked Dataset state. Data is
                queryable via the Linked Dataset.
            UNLINKED (2):
                Data publisher or owner has unlinked this
                Linked Dataset. It means you can no longer query
                or see the data in the Linked Dataset.
        """
        LINK_STATE_UNSPECIFIED = 0
        LINKED = 1
        UNLINKED = 2

    link_state: LinkState = proto.Field(
        proto.ENUM,
        number=1,
        enum=LinkState,
    )


class GetDatasetRequest(proto.Message):
    r"""Request format for getting information about a dataset.

    Attributes:
        project_id (str):
            Required. Project ID of the requested dataset
        dataset_id (str):
            Required. Dataset ID of the requested dataset
        dataset_view (google.cloud.bigquery_v2.types.GetDatasetRequest.DatasetView):
            Optional. Specifies the view that determines
            which dataset information is returned. By
            default, metadata and ACL information are
            returned.
        access_policy_version (int):
            Optional. The version of the access policy schema to fetch.
            Valid values are 0, 1, and 3. Requests specifying an invalid
            value will be rejected.

            Requests for conditional access policy binding in datasets
            must specify version 3. Dataset with no conditional role
            bindings in access policy may specify any valid value or
            leave the field unset.

            This field will be mapped to [IAM Policy version]
            (https://cloud.google.com/iam/docs/policies#versions) and
            will be used to fetch policy from IAM.

            If unset or if 0 or 1 value is used for dataset with
            conditional bindings, access entry with condition will have
            role string appended by 'withcond' string followed by a hash
            value. For example : { "access": [ { "role":
            "roles/bigquery.dataViewer_with_conditionalbinding_7a34awqsda",
            "userByEmail": "user@example.com", } ] } Please refer
            https://cloud.google.com/iam/docs/troubleshooting-withcond
            for more details.
    """

    class DatasetView(proto.Enum):
        r"""DatasetView specifies which dataset information is returned.

        Values:
            DATASET_VIEW_UNSPECIFIED (0):
                The default value.
                Default to the FULL view.
            METADATA (1):
                View metadata information for the dataset,
                such as friendlyName, description, labels, etc.
            ACL (2):
                View ACL information for the dataset, which
                defines dataset access for one or more entities.
            FULL (3):
                View both dataset metadata and ACL
                information.
        """
        DATASET_VIEW_UNSPECIFIED = 0
        METADATA = 1
        ACL = 2
        FULL = 3

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    dataset_view: DatasetView = proto.Field(
        proto.ENUM,
        number=3,
        enum=DatasetView,
    )
    access_policy_version: int = proto.Field(
        proto.INT32,
        number=4,
    )


class InsertDatasetRequest(proto.Message):
    r"""Request format for inserting a dataset.

    Attributes:
        project_id (str):
            Required. Project ID of the new dataset
        dataset (google.cloud.bigquery_v2.types.Dataset):
            Required. Datasets resource to use for the
            new dataset
        access_policy_version (int):
            Optional. The version of the provided access policy schema.
            Valid values are 0, 1, and 3. Requests specifying an invalid
            value will be rejected.

            This version refers to the schema version of the access
            policy and not the version of access policy. This field's
            value can be equal or more than the access policy schema
            provided in the request. For example,

            -  Requests with conditional access policy binding in
               datasets must specify version 3.
            -  But dataset with no conditional role bindings in access
               policy may specify any valid value or leave the field
               unset. If unset or if 0 or 1 value is used for dataset
               with conditional bindings, request will be rejected.

            This field will be mapped to IAM Policy version
            (https://cloud.google.com/iam/docs/policies#versions) and
            will be used to set policy in IAM.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset: "Dataset" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Dataset",
    )
    access_policy_version: int = proto.Field(
        proto.INT32,
        number=4,
    )


class UpdateOrPatchDatasetRequest(proto.Message):
    r"""Message for updating or patching a dataset.

    Attributes:
        project_id (str):
            Required. Project ID of the dataset being
            updated
        dataset_id (str):
            Required. Dataset ID of the dataset being
            updated
        dataset (google.cloud.bigquery_v2.types.Dataset):
            Required. Datasets resource which will
            replace or patch the specified dataset.
        update_mode (google.cloud.bigquery_v2.types.UpdateOrPatchDatasetRequest.UpdateMode):
            Optional. Specifies the fields of dataset
            that update/patch operation is targeting By
            default, both metadata and ACL fields are
            updated.
        access_policy_version (int):
            Optional. The version of the provided access policy schema.
            Valid values are 0, 1, and 3. Requests specifying an invalid
            value will be rejected.

            This version refers to the schema version of the access
            policy and not the version of access policy. This field's
            value can be equal or more than the access policy schema
            provided in the request. For example,

            -  Operations updating conditional access policy binding in
               datasets must specify version 3. Some of the operations
               are :

               -  Adding a new access policy entry with condition.
               -  Removing an access policy entry with condition.
               -  Updating an access policy entry with condition.

            -  But dataset with no conditional role bindings in access
               policy may specify any valid value or leave the field
               unset. If unset or if 0 or 1 value is used for dataset
               with conditional bindings, request will be rejected.

            This field will be mapped to IAM Policy version
            (https://cloud.google.com/iam/docs/policies#versions) and
            will be used to set policy in IAM.
    """

    class UpdateMode(proto.Enum):
        r"""UpdateMode specifies which dataset fields is updated.

        Values:
            UPDATE_MODE_UNSPECIFIED (0):
                The default value. Default to the UPDATE_FULL.
            UPDATE_METADATA (1):
                Includes metadata information for the
                dataset, such as friendlyName, description,
                labels, etc.
            UPDATE_ACL (2):
                Includes ACL information for the dataset,
                which defines dataset access for one or more
                entities.
            UPDATE_FULL (3):
                Includes both dataset metadata and ACL
                information.
        """
        UPDATE_MODE_UNSPECIFIED = 0
        UPDATE_METADATA = 1
        UPDATE_ACL = 2
        UPDATE_FULL = 3

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    dataset: "Dataset" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Dataset",
    )
    update_mode: UpdateMode = proto.Field(
        proto.ENUM,
        number=4,
        enum=UpdateMode,
    )
    access_policy_version: int = proto.Field(
        proto.INT32,
        number=5,
    )


class DeleteDatasetRequest(proto.Message):
    r"""Request format for deleting a dataset.

    Attributes:
        project_id (str):
            Required. Project ID of the dataset being
            deleted
        dataset_id (str):
            Required. Dataset ID of dataset being deleted
        delete_contents (bool):
            If True, delete all the tables in the
            dataset. If False and the dataset contains
            tables, the request will fail. Default is False
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    delete_contents: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class ListDatasetsRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the datasets to be
            listed
        max_results (google.protobuf.wrappers_pb2.UInt32Value):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results
        all_ (bool):
            Whether to list all datasets, including
            hidden ones
        filter (str):
            An expression for filtering the results of the request by
            label. The syntax is ``labels.<name>[:<value>]``. Multiple
            filters can be AND-ed together by connecting with a space.
            Example: ``labels.department:receiving labels.active``. See
            `Filtering datasets using
            labels <https://cloud.google.com/bigquery/docs/filtering-labels#filtering_datasets_using_labels>`__
            for details.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    max_results: wrappers_pb2.UInt32Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.UInt32Value,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    all_: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListFormatDataset(proto.Message):
    r"""A dataset resource with only a subset of fields, to be
    returned in a list of datasets.

    Attributes:
        kind (str):
            The resource type.
            This property always returns the value
            "bigquery#dataset".
        id (str):
            The fully-qualified, unique, opaque ID of the
            dataset.
        dataset_reference (google.cloud.bigquery_v2.types.DatasetReference):
            The dataset reference.
            Use this property to access specific parts of
            the dataset's ID, such as project ID or dataset
            ID.
        labels (MutableMapping[str, str]):
            The labels associated with this dataset.
            You can use these to organize and group your
            datasets.
        friendly_name (google.protobuf.wrappers_pb2.StringValue):
            An alternate name for the dataset.  The
            friendly name is purely decorative in nature.
        location (str):
            The geographic location where the dataset
            resides.
        external_dataset_reference (google.cloud.bigquery_v2.types.ExternalDatasetReference):
            Output only. Reference to a read-only
            external dataset defined in data catalogs
            outside of BigQuery. Filled out when the dataset
            type is EXTERNAL.
    """

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    dataset_reference: gcb_dataset_reference.DatasetReference = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcb_dataset_reference.DatasetReference,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    friendly_name: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.StringValue,
    )
    location: str = proto.Field(
        proto.STRING,
        number=6,
    )
    external_dataset_reference: gcb_external_dataset_reference.ExternalDatasetReference = proto.Field(
        proto.MESSAGE,
        number=11,
        message=gcb_external_dataset_reference.ExternalDatasetReference,
    )


class DatasetList(proto.Message):
    r"""Response format for a page of results when listing datasets.

    Attributes:
        kind (str):
            Output only. The resource type.
            This property always returns the value
            "bigquery#datasetList".
        etag (str):
            Output only. A hash value of the results
            page. You can use this property to determine if
            the page has changed since the last request.
        next_page_token (str):
            A token that can be used to request the next
            results page. This property is omitted on the
            final results page.
        datasets (MutableSequence[google.cloud.bigquery_v2.types.ListFormatDataset]):
            An array of the dataset resources in the
            project. Each resource contains basic
            information. For full information about a
            particular dataset resource, use the Datasets:

            get method. This property is omitted when there
            are no datasets in the project.
        unreachable (MutableSequence[str]):
            A list of skipped locations that were
            unreachable. For more information about BigQuery
            locations, see:

            https://cloud.google.com/bigquery/docs/locations.
            Example: "europe-west5".
    """

    @property
    def raw_page(self):
        return self

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    datasets: MutableSequence["ListFormatDataset"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="ListFormatDataset",
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class UndeleteDatasetRequest(proto.Message):
    r"""Request format for undeleting a dataset.

    Attributes:
        project_id (str):
            Required. Project ID of the dataset to be
            undeleted
        dataset_id (str):
            Required. Dataset ID of dataset being deleted
        deletion_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. The exact time when the dataset was
            deleted. If not specified, the most recently
            deleted version is undeleted. Undeleting a
            dataset using deletion time is not supported.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    deletion_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
