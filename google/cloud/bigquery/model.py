# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Define resources for the BigQuery ML Models API."""

import copy
import datetime
from typing import Any, Dict, Optional, Sequence, Union

import google.cloud._helpers
from google.cloud.bigquery import _helpers
from google.cloud.bigquery import standard_sql
from google.cloud.bigquery.encryption_configuration import EncryptionConfiguration


class Model:
    """Model represents a machine learning model resource.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/models

    Args:
        model_ref:
            A pointer to a model. If ``model_ref`` is a string, it must
            included a project ID, dataset ID, and model ID, each separated
            by ``.``.
    """

    _PROPERTY_TO_API_FIELD = {
        "expires": "expirationTime",
        "friendly_name": "friendlyName",
        # Even though it's not necessary for field mapping to map when the
        # property name equals the resource name, we add these here so that we
        # have an exhaustive list of all mutable properties.
        "labels": "labels",
        "description": "description",
        "encryption_configuration": "encryptionConfiguration",
    }

    def __init__(self, model_ref: Union["ModelReference", str, None]):
        # Use _properties on read-write properties to match the REST API
        # semantics. The BigQuery API makes a distinction between an unset
        # value, a null value, and a default value (0 or ""), but the protocol
        # buffer classes do not.
        self._properties = {}

        if isinstance(model_ref, str):
            model_ref = ModelReference.from_string(model_ref)

        if model_ref:
            self._properties["modelReference"] = model_ref.to_api_repr()

    @property
    def reference(self) -> Optional["ModelReference"]:
        """A model reference pointing to this model.

        Read-only.
        """
        resource = self._properties.get("modelReference")
        if resource is not None:
            return ModelReference.from_api_repr(resource)

    @property
    def project(self) -> str:
        """Project bound to the model."""
        return self.reference.project

    @property
    def dataset_id(self) -> str:
        """ID of dataset containing the model."""
        return self.reference.dataset_id

    @property
    def model_id(self) -> str:
        """The model ID."""
        return self.reference.model_id

    @property
    def path(self) -> str:
        """URL path for the model's APIs."""
        return self.reference.path

    @property
    def location(self) -> str:
        """The geographic location where the model resides.

        This value is inherited from the dataset.

        Read-only.
        """
        return self._properties.get("location")

    @property
    def etag(self) -> str:
        """ETag for the model resource (:data:`None` until set from the server).

        Read-only.
        """
        return self._properties.get("etag")

    @property
    def created(self) -> Optional[datetime.datetime]:
        """Datetime at which the model was created (:data:`None` until set from the server).

        Read-only.
        """
        value = self._properties.get("creationTime")
        if value is not None:
            # value will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(value)
            )

    @property
    def modified(self) -> Optional[datetime.datetime]:
        """Datetime at which the model was last modified (:data:`None` until set from the server).

        Read-only.
        """
        value = value = self._properties.get("lastModifiedTime")
        if value is not None:
            # value will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(value)
            )

    @property
    def model_type(self) -> str:
        """Type of the model resource.

        Read-only.
        """
        return self._properties.get("modelType", "MODEL_TYPE_UNSPECIFIED")

    @property
    def training_runs(self) -> Sequence[Dict[str, Any]]:
        """Information for all training runs in increasing order of start time.

        Read-only.
        """
        return self._properties.get("trainingRuns", [])

    @property
    def feature_columns(self) -> Sequence[standard_sql.StandardSqlField]:
        """Input feature columns that were used to train this model.

        Read-only.
        """
        return self._properties.get("featureColumns", [])

    @property
    def label_columns(self) -> Sequence[standard_sql.StandardSqlField]:
        """Label columns that were used to train this model.

        The output of the model will have a ``predicted_`` prefix to these columns.

        Read-only.
        """
        return self._properties.get("labelColumns", [])

    @property
    def expires(self) -> Optional[datetime.datetime]:
        """The datetime when this model expires.

        If not present, the model will persist indefinitely. Expired models will be
        deleted and their storage reclaimed.
        """
        value = self._properties.get("expirationTime")
        if value is not None:
            # value will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(value)
            )

    @expires.setter
    def expires(self, value: Optional[datetime.datetime]):
        if value is not None:
            value = str(google.cloud._helpers._millis_from_datetime(value))
        self._properties["expirationTime"] = value

    @property
    def description(self) -> Optional[str]:
        """Description of the model (defaults to :data:`None`)."""
        return self._properties.get("description")

    @description.setter
    def description(self, value: Optional[str]):
        self._properties["description"] = value

    @property
    def friendly_name(self) -> Optional[str]:
        """Title of the table (defaults to :data:`None`)."""
        return self._properties.get("friendlyName")

    @friendly_name.setter
    def friendly_name(self, value: Optional[str]):
        self._properties["friendlyName"] = value

    @property
    def labels(self) -> Dict[str, str]:
        """Labels for the table.

        This method always returns a dict. To change a model's labels, modify the dict,
        then call ``Client.update_model``. To delete a label, set its value to
        :data:`None` before updating.
        """
        return self._properties.setdefault("labels", {})

    @labels.setter
    def labels(self, value: Optional[Dict[str, str]]):
        if value is None:
            value = {}
        self._properties["labels"] = value

    @property
    def encryption_configuration(self) -> Optional[EncryptionConfiguration]:
        """Custom encryption configuration for the model.

        Custom encryption configuration (e.g., Cloud KMS keys) or :data:`None`
        if using default encryption.

        See `protecting data with Cloud KMS keys
        <https://cloud.google.com/bigquery/docs/customer-managed-encryption>`_
        in the BigQuery documentation.
        """
        prop = self._properties.get("encryptionConfiguration")
        if prop:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @encryption_configuration.setter
    def encryption_configuration(self, value: Optional[EncryptionConfiguration]):
        api_repr = value
        if value:
            api_repr = value.to_api_repr()
        self._properties["encryptionConfiguration"] = api_repr

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]) -> "Model":
        """Factory: construct a model resource given its API representation

        Args:
            resource:
                Model resource representation from the API

        Returns:
            Model parsed from ``resource``.
        """
        this = cls(None)
        resource = copy.deepcopy(resource)
        this._properties = resource
        return this

    def _build_resource(self, filter_fields):
        """Generate a resource for ``update``."""
        return _helpers._build_resource_from_properties(self, filter_fields)

    def __repr__(self):
        return f"Model(reference={self.reference!r})"

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this model.

        Returns:
            Model reference represented as an API resource
        """
        return copy.deepcopy(self._properties)


class ModelReference:
    """ModelReferences are pointers to models.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/models#modelreference
    """

    def __init__(self):
        self._properties = {}

    @property
    def project(self):
        """str: Project bound to the model"""
        return self._properties.get("projectId")

    @property
    def dataset_id(self):
        """str: ID of dataset containing the model."""
        return self._properties.get("datasetId")

    @property
    def model_id(self):
        """str: The model ID."""
        return self._properties.get("modelId")

    @property
    def path(self) -> str:
        """URL path for the model's APIs."""
        return f"/projects/{self.project}/datasets/{self.dataset_id}/models/{self.model_id}"

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]) -> "ModelReference":
        """Factory: construct a model reference given its API representation.

        Args:
            resource:
                Model reference representation returned from the API

        Returns:
            Model reference parsed from ``resource``.
        """
        ref = cls()
        ref._properties = resource
        return ref

    @classmethod
    def from_string(
        cls, model_id: str, default_project: Optional[str] = None
    ) -> "ModelReference":
        """Construct a model reference from model ID string.

        Args:
            model_id:
                A model ID in standard SQL format. If ``default_project``
                is not specified, this must included a project ID, dataset
                ID, and model ID, each separated by ``.``.
            default_project:
                The project ID to use when ``model_id`` does not include
                a project ID.

        Returns:
            Model reference parsed from ``model_id``.

        Raises:
            ValueError:
                If ``model_id`` is not a fully-qualified table ID in
                standard SQL format.
        """
        proj, dset, model = _helpers._parse_3_part_id(
            model_id, default_project=default_project, property_name="model_id"
        )
        return cls.from_api_repr(
            {"projectId": proj, "datasetId": dset, "modelId": model}
        )

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation of this model reference.

        Returns:
            Model reference represented as an API resource.
        """
        return copy.deepcopy(self._properties)

    def _key(self):
        """Unique key for this model.

        This is used for hashing a ModelReference.
        """
        return self.project, self.dataset_id, self.model_id

    def __eq__(self, other):
        if not isinstance(other, ModelReference):
            return NotImplemented
        return self._properties == other._properties

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return "ModelReference(project_id='{}', dataset_id='{}', model_id='{}')".format(
            self.project, self.dataset_id, self.model_id
        )


def _model_arg_to_model_ref(value, default_project=None):
    """Helper to convert a string or Model to ModelReference.

    This function keeps ModelReference and other kinds of objects unchanged.
    """
    if isinstance(value, str):
        return ModelReference.from_string(value, default_project=default_project)
    if isinstance(value, Model):
        return value.reference
    return value
