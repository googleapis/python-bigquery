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

"""Define resources for the BigQuery Routines API."""

from google.protobuf import json_format

import google.cloud._helpers
from google.cloud.bigquery import _helpers
import google.cloud.bigquery_v2.types
from google.cloud.bigquery_v2.types import StandardSqlTableType


class RoutineType:
    """The fine-grained type of the routine.

    https://cloud.google.com/bigquery/docs/reference/rest/v2/routines#routinetype

    .. versionadded:: 2.22.0
    """

    ROUTINE_TYPE_UNSPECIFIED = "ROUTINE_TYPE_UNSPECIFIED"
    SCALAR_FUNCTION = "SCALAR_FUNCTION"
    PROCEDURE = "PROCEDURE"
    TABLE_VALUED_FUNCTION = "TABLE_VALUED_FUNCTION"


class Routine(object):
    """Resource representing a user-defined routine.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/routines

    Args:
        routine_ref (Union[str, google.cloud.bigquery.routine.RoutineReference]):
            A pointer to a routine. If ``routine_ref`` is a string, it must
            included a project ID, dataset ID, and routine ID, each separated
            by ``.``.
        ``**kwargs`` (Dict):
            Initial property values.
    """

    _PROPERTY_TO_API_FIELD = {
        "arguments": "arguments",
        "body": "definitionBody",
        "created": "creationTime",
        "etag": "etag",
        "imported_libraries": "importedLibraries",
        "language": "language",
        "modified": "lastModifiedTime",
        "reference": "routineReference",
        "return_type": "returnType",
        "return_table_type": "returnTableType",
        "type_": "routineType",
        "description": "description",
        "determinism_level": "determinismLevel",
    }

    def __init__(self, routine_ref, **kwargs):
        if isinstance(routine_ref, str):
            routine_ref = RoutineReference.from_string(routine_ref)

        self._properties = {"routineReference": routine_ref.to_api_repr()}
        for property_name in kwargs:
            setattr(self, property_name, kwargs[property_name])

    @property
    def reference(self):
        """google.cloud.bigquery.routine.RoutineReference: Reference
        describing the ID of this routine.
        """
        return RoutineReference.from_api_repr(
            self._properties[self._PROPERTY_TO_API_FIELD["reference"]]
        )

    @property
    def path(self):
        """str: URL path for the routine's APIs."""
        return self.reference.path

    @property
    def project(self):
        """str: ID of the project containing the routine."""
        return self.reference.project

    @property
    def dataset_id(self):
        """str: ID of dataset containing the routine."""
        return self.reference.dataset_id

    @property
    def routine_id(self):
        """str: The routine ID."""
        return self.reference.routine_id

    @property
    def etag(self):
        """str: ETag for the resource (:data:`None` until set from the
        server).

        Read-only.
        """
        return self._properties.get(self._PROPERTY_TO_API_FIELD["etag"])

    @property
    def type_(self):
        """str: The fine-grained type of the routine.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/routines#RoutineType
        """
        return self._properties.get(self._PROPERTY_TO_API_FIELD["type_"])

    @type_.setter
    def type_(self, value):
        self._properties[self._PROPERTY_TO_API_FIELD["type_"]] = value

    @property
    def created(self):
        """Optional[datetime.datetime]: Datetime at which the routine was
        created (:data:`None` until set from the server).

        Read-only.
        """
        value = self._properties.get(self._PROPERTY_TO_API_FIELD["created"])
        if value is not None and value != 0:
            # value will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(value)
            )

    @property
    def modified(self):
        """Optional[datetime.datetime]: Datetime at which the routine was
        last modified (:data:`None` until set from the server).

        Read-only.
        """
        value = self._properties.get(self._PROPERTY_TO_API_FIELD["modified"])
        if value is not None and value != 0:
            # value will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(value)
            )

    @property
    def language(self):
        """Optional[str]: The language of the routine.

        Defaults to ``SQL``.
        """
        return self._properties.get(self._PROPERTY_TO_API_FIELD["language"])

    @language.setter
    def language(self, value):
        self._properties[self._PROPERTY_TO_API_FIELD["language"]] = value

    @property
    def arguments(self):
        """List[google.cloud.bigquery.routine.RoutineArgument]: Input/output
        argument of a function or a stored procedure.

        In-place modification is not supported. To set, replace the entire
        property value with the modified list of
        :class:`~google.cloud.bigquery.routine.RoutineArgument` objects.
        """
        resources = self._properties.get(self._PROPERTY_TO_API_FIELD["arguments"], [])
        return [RoutineArgument.from_api_repr(resource) for resource in resources]

    @arguments.setter
    def arguments(self, value):
        if not value:
            resource = []
        else:
            resource = [argument.to_api_repr() for argument in value]
        self._properties[self._PROPERTY_TO_API_FIELD["arguments"]] = resource

    @property
    def return_type(self):
        """google.cloud.bigquery_v2.types.StandardSqlDataType: Return type of
        the routine.

        If absent, the return type is inferred from
        :attr:`~google.cloud.bigquery.routine.Routine.body` at query time in
        each query that references this routine. If present, then the
        evaluated result will be cast to the specified returned type at query
        time.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/routines#Routine.FIELDS.return_type
        """
        resource = self._properties.get(self._PROPERTY_TO_API_FIELD["return_type"])
        if not resource:
            return resource

        output = google.cloud.bigquery_v2.types.StandardSqlDataType()
        raw_protobuf = json_format.ParseDict(
            resource, output._pb, ignore_unknown_fields=True
        )
        return type(output).wrap(raw_protobuf)

    @return_type.setter
    def return_type(self, value):
        if value:
            resource = json_format.MessageToDict(value._pb)
        else:
            resource = None
        self._properties[self._PROPERTY_TO_API_FIELD["return_type"]] = resource

    @property
    def return_table_type(self) -> StandardSqlTableType:
        """The return type of a Table Valued Function (TVF) routine.

        .. versionadded:: 2.22.0
        """
        resource = self._properties.get(
            self._PROPERTY_TO_API_FIELD["return_table_type"]
        )
        if not resource:
            return resource

        output = google.cloud.bigquery_v2.types.StandardSqlTableType()
        raw_protobuf = json_format.ParseDict(
            resource, output._pb, ignore_unknown_fields=True
        )
        return type(output).wrap(raw_protobuf)

    @return_table_type.setter
    def return_table_type(self, value):
        if not value:
            resource = None
        else:
            resource = {
                "columns": [json_format.MessageToDict(col._pb) for col in value.columns]
            }

        self._properties[self._PROPERTY_TO_API_FIELD["return_table_type"]] = resource

    @property
    def imported_libraries(self):
        """List[str]: The path of the imported JavaScript libraries.

        The :attr:`~google.cloud.bigquery.routine.Routine.language` must
        equal ``JAVACRIPT``.

        Examples:
            Set the ``imported_libraries`` to a list of Google Cloud Storage
            URIs.

            .. code-block:: python

               routine = bigquery.Routine("proj.dataset.routine_id")
               routine.imported_libraries = [
                   "gs://cloud-samples-data/bigquery/udfs/max-value.js",
               ]
        """
        return self._properties.get(
            self._PROPERTY_TO_API_FIELD["imported_libraries"], []
        )

    @imported_libraries.setter
    def imported_libraries(self, value):
        if not value:
            resource = []
        else:
            resource = value
        self._properties[self._PROPERTY_TO_API_FIELD["imported_libraries"]] = resource

    @property
    def body(self):
        """str: The body of the routine."""
        return self._properties.get(self._PROPERTY_TO_API_FIELD["body"])

    @body.setter
    def body(self, value):
        self._properties[self._PROPERTY_TO_API_FIELD["body"]] = value

    @property
    def description(self):
        """Optional[str]: Description of the routine (defaults to
        :data:`None`).
        """
        return self._properties.get(self._PROPERTY_TO_API_FIELD["description"])

    @description.setter
    def description(self, value):
        self._properties[self._PROPERTY_TO_API_FIELD["description"]] = value

    @property
    def determinism_level(self):
        """Optional[str]: (experimental) The determinism level of the JavaScript UDF
        if defined.
        """
        return self._properties.get(self._PROPERTY_TO_API_FIELD["determinism_level"])

    @determinism_level.setter
    def determinism_level(self, value):
        self._properties[self._PROPERTY_TO_API_FIELD["determinism_level"]] = value

    @classmethod
    def from_api_repr(cls, resource: dict) -> "Routine":
        """Factory: construct a routine given its API representation.

        Args:
            resource (Dict[str, object]):
                Resource, as returned from the API.

        Returns:
            google.cloud.bigquery.routine.Routine:
                Python object, as parsed from ``resource``.
        """
        ref = cls(RoutineReference.from_api_repr(resource["routineReference"]))
        ref._properties = resource
        return ref

    def to_api_repr(self) -> dict:
        """Construct the API resource representation of this routine.

        Returns:
            Dict[str, object]: Routine represented as an API resource.
        """
        return self._properties

    def _build_resource(self, filter_fields):
        """Generate a resource for ``update``."""
        return _helpers._build_resource_from_properties(self, filter_fields)

    def __repr__(self):
        return "Routine('{}.{}.{}')".format(
            self.project, self.dataset_id, self.routine_id
        )


class RoutineArgument(object):
    """Input/output argument of a function or a stored procedure.

    See:
    https://cloud.google.com/bigquery/docs/reference/rest/v2/routines#argument

    Args:
        ``**kwargs`` (Dict):
            Initial property values.
    """

    _PROPERTY_TO_API_FIELD = {
        "data_type": "dataType",
        "kind": "argumentKind",
        # Even though it's not necessary for field mapping to map when the
        # property name equals the resource name, we add these here so that we
        # have an exhaustive list of all properties.
        "name": "name",
        "mode": "mode",
    }

    def __init__(self, **kwargs):
        self._properties = {}
        for property_name in kwargs:
            setattr(self, property_name, kwargs[property_name])

    @property
    def name(self):
        """Optional[str]: Name of this argument.

        Can be absent for function return argument.
        """
        return self._properties.get(self._PROPERTY_TO_API_FIELD["name"])

    @name.setter
    def name(self, value):
        self._properties[self._PROPERTY_TO_API_FIELD["name"]] = value

    @property
    def kind(self):
        """Optional[str]: The kind of argument, for example ``FIXED_TYPE`` or
        ``ANY_TYPE``.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/routines#Argument.FIELDS.argument_kind
        """
        return self._properties.get(self._PROPERTY_TO_API_FIELD["kind"])

    @kind.setter
    def kind(self, value):
        self._properties[self._PROPERTY_TO_API_FIELD["kind"]] = value

    @property
    def mode(self):
        """Optional[str]: The input/output mode of the argument."""
        return self._properties.get(self._PROPERTY_TO_API_FIELD["mode"])

    @mode.setter
    def mode(self, value):
        self._properties[self._PROPERTY_TO_API_FIELD["mode"]] = value

    @property
    def data_type(self):
        """Optional[google.cloud.bigquery_v2.types.StandardSqlDataType]: Type
        of a variable, e.g., a function argument.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/routines#Argument.FIELDS.data_type
        """
        resource = self._properties.get(self._PROPERTY_TO_API_FIELD["data_type"])
        if not resource:
            return resource

        output = google.cloud.bigquery_v2.types.StandardSqlDataType()
        raw_protobuf = json_format.ParseDict(
            resource, output._pb, ignore_unknown_fields=True
        )
        return type(output).wrap(raw_protobuf)

    @data_type.setter
    def data_type(self, value):
        if value:
            resource = json_format.MessageToDict(value._pb)
        else:
            resource = None
        self._properties[self._PROPERTY_TO_API_FIELD["data_type"]] = resource

    @classmethod
    def from_api_repr(cls, resource: dict) -> "RoutineArgument":
        """Factory: construct a routine argument given its API representation.

        Args:
            resource (Dict[str, object]): Resource, as returned from the API.

        Returns:
            google.cloud.bigquery.routine.RoutineArgument:
                Python object, as parsed from ``resource``.
        """
        ref = cls()
        ref._properties = resource
        return ref

    def to_api_repr(self) -> dict:
        """Construct the API resource representation of this routine argument.

        Returns:
            Dict[str, object]: Routine argument represented as an API resource.
        """
        return self._properties

    def __eq__(self, other):
        if not isinstance(other, RoutineArgument):
            return NotImplemented
        return self._properties == other._properties

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        all_properties = [
            "{}={}".format(property_name, repr(getattr(self, property_name)))
            for property_name in sorted(self._PROPERTY_TO_API_FIELD)
        ]
        return "RoutineArgument({})".format(", ".join(all_properties))


class RoutineReference(object):
    """A pointer to a routine.

    See:
    https://cloud.google.com/bigquery/docs/reference/rest/v2/routines#routinereference
    """

    def __init__(self):
        self._properties = {}

    @property
    def project(self):
        """str: ID of the project containing the routine."""
        return self._properties["projectId"]  # pytype: disable=key-error

    @property
    def dataset_id(self):
        """str: ID of dataset containing the routine."""
        return self._properties["datasetId"]  # pytype: disable=key-error

    @property
    def routine_id(self):
        """str: The routine ID."""
        return self._properties["routineId"]  # pytype: disable=key-error

    @property
    def path(self):
        """str: URL path for the routine's APIs."""
        return "/projects/%s/datasets/%s/routines/%s" % (
            self.project,
            self.dataset_id,
            self.routine_id,
        )

    @classmethod
    def from_api_repr(cls, resource: dict) -> "RoutineReference":
        """Factory: construct a routine reference given its API representation.

        Args:
            resource (Dict[str, object]):
                Routine reference representation returned from the API.

        Returns:
            google.cloud.bigquery.routine.RoutineReference:
                Routine reference parsed from ``resource``.
        """
        ref = cls()
        ref._properties = resource
        return ref

    @classmethod
    def from_string(
        cls, routine_id: str, default_project: str = None
    ) -> "RoutineReference":
        """Factory: construct a routine reference from routine ID string.

        Args:
            routine_id (str):
                A routine ID in standard SQL format. If ``default_project``
                is not specified, this must included a project ID, dataset
                ID, and routine ID, each separated by ``.``.
            default_project (Optional[str]):
                The project ID to use when ``routine_id`` does not
                include a project ID.

        Returns:
            google.cloud.bigquery.routine.RoutineReference:
                Routine reference parsed from ``routine_id``.

        Raises:
            ValueError:
                If ``routine_id`` is not a fully-qualified routine ID in
                standard SQL format.
        """
        proj, dset, routine = _helpers._parse_3_part_id(
            routine_id, default_project=default_project, property_name="routine_id"
        )
        return cls.from_api_repr(
            {"projectId": proj, "datasetId": dset, "routineId": routine}
        )

    def to_api_repr(self) -> dict:
        """Construct the API resource representation of this routine reference.

        Returns:
            Dict[str, object]: Routine reference represented as an API resource.
        """
        return self._properties

    def __eq__(self, other):
        """Two RoutineReferences are equal if they point to the same routine."""
        if not isinstance(other, RoutineReference):
            return NotImplemented
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "RoutineReference.from_string('{}')".format(str(self))

    def __str__(self):
        """String representation of the reference.

        This is a fully-qualified ID, including the project ID and dataset ID.
        """
        return "{}.{}.{}".format(self.project, self.dataset_id, self.routine_id)
