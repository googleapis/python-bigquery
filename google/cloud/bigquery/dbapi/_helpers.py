# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from collections import abc as collections_abc
import datetime
import decimal
import functools
import numbers
import re

from google.cloud import bigquery
from google.cloud.bigquery import table, enums, query
from google.cloud.bigquery.dbapi import exceptions


_NUMERIC_SERVER_MIN = decimal.Decimal("-9.9999999999999999999999999999999999999E+28")
_NUMERIC_SERVER_MAX = decimal.Decimal("9.9999999999999999999999999999999999999E+28")

type_parameters_re = re.compile(
    r"""
    \(
    \s*[0-9]+\s*
    (,
    \s*[0-9]+\s*
    )*
    \)
    """,
    re.VERBOSE,
)


def _parameter_type(name, value, query_parameter_type=None, value_doc=""):
    if query_parameter_type:
        # Strip type parameters
        query_parameter_type = type_parameters_re.sub("", query_parameter_type)
        try:
            parameter_type = getattr(
                enums.SqlParameterScalarTypes, query_parameter_type.upper()
            )._type
        except AttributeError:
            raise exceptions.ProgrammingError(
                f"The given parameter type, {query_parameter_type},"
                f" for {name} is not a valid BigQuery scalar type."
            )
    else:
        parameter_type = bigquery_scalar_type(value)
        if parameter_type is None:
            raise exceptions.ProgrammingError(
                f"Encountered parameter {name} with "
                f"{value_doc} value {value} of unexpected type."
            )
    return parameter_type


def scalar_to_query_parameter(value, name=None, query_parameter_type=None):
    """Convert a scalar value into a query parameter.

    Args:
        value (Any):
            A scalar value to convert into a query parameter.

        name (str):
            (Optional) Name of the query parameter.
        query_parameter_type (Optional[str]): Given type for the parameter.

    Returns:
        google.cloud.bigquery.ScalarQueryParameter:
            A query parameter corresponding with the type and value of the plain
            Python object.

    Raises:
        google.cloud.bigquery.dbapi.exceptions.ProgrammingError:
            if the type cannot be determined.
    """
    return bigquery.ScalarQueryParameter(
        name, _parameter_type(name, value, query_parameter_type), value
    )


def array_to_query_parameter(value, name=None, query_parameter_type=None):
    """Convert an array-like value into a query parameter.

    Args:
        value (Sequence[Any]): The elements of the array (should not be a
            string-like Sequence).
        name (Optional[str]): Name of the query parameter.
        query_parameter_type (Optional[str]): Given type for the parameter.

    Returns:
        A query parameter corresponding with the type and value of the plain
        Python object.

    Raises:
        google.cloud.bigquery.dbapi.exceptions.ProgrammingError:
            if the type of array elements cannot be determined.
    """
    if not array_like(value):
        raise exceptions.ProgrammingError(
            "The value of parameter {} must be a sequence that is "
            "not string-like.".format(name)
        )

    if query_parameter_type or value:
        array_type = _parameter_type(
            name,
            value[0] if value else None,
            query_parameter_type,
            value_doc="array element ",
        )
    else:
        raise exceptions.ProgrammingError(
            "Encountered an empty array-like value of parameter {}, cannot "
            "determine array elements type.".format(name)
        )

    return bigquery.ArrayQueryParameter(name, array_type, value)


complex_query_parameter_parse = re.compile(
    r"""
    \s*
    (ARRAY|STRUCT|RECORD)  # Type
    \s*
    <([A-Z0-9<> ,()]+)>      # Subtype(s)
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
).match
parse_struct_field = re.compile(
    r"""
    (?:(\w+)\s+)    # field name
    ([A-Z0-9<> ,()]+)  # Field type
    $""",
    re.VERBOSE | re.IGNORECASE,
).match


def split_struct_fields(fields):
    fields = fields.split(",")
    while fields:
        field = fields.pop(0)
        while fields and field.count("<") != field.count(">"):
            field += "," + fields.pop(0)
        yield field


def complex_query_parameter_type(name: str, type_: str, base: str):
    type_ = type_.strip()
    if "<" not in type_:
        # Scalar

        # Strip type parameters
        type_ = type_parameters_re.sub("", type_).strip()
        try:
            type_ = getattr(enums.SqlParameterScalarTypes, type_.upper())
        except AttributeError:
            raise exceptions.ProgrammingError(
                f"Invalid scalar type, {type_}, in {base}"
            )
        if name:
            type_ = type_.with_name(name)
        return type_

    m = complex_query_parameter_parse(type_)
    if not m:
        raise exceptions.ProgrammingError(f"Invalid parameter type, {type_}")
    tname, sub = m.groups()
    tname = tname.upper()
    sub = sub.strip()
    if tname == "ARRAY":
        return query.ArrayQueryParameterType(
            complex_query_parameter_type(None, sub, base), name=name
        )
    else:
        fields = []
        for field_string in split_struct_fields(sub):
            field_string = field_string.strip()
            m = parse_struct_field(field_string)
            if not m:
                raise exceptions.ProgrammingError(
                    f"Invalid struct field, {field_string}, in {base}"
                )
            field_name, field_type = m.groups()
            fields.append(complex_query_parameter_type(field_name, field_type, base))

        return query.StructQueryParameterType(*fields, name=name)


def complex_query_parameter(name, value, type_, base=None):
    """
    Construct a query parameter for a complex type (array or struct record)

    or for a subtype, which may not be complex
    """
    type_ = type_.strip()
    base = base or type_
    if ">" not in type_:
        # Scalar

        # Strip type parameters
        type_ = type_parameters_re.sub("", type_).strip()
        try:
            type_ = getattr(enums.SqlParameterScalarTypes, type_.upper())._type
        except AttributeError:
            raise exceptions.ProgrammingError(
                f"The given parameter type, {type_},"
                f" for {name} is not a valid BigQuery scalar type, in {base}."
            )

        return query.ScalarQueryParameter(name, type_, value)

    m = complex_query_parameter_parse(type_)
    if not m:
        raise exceptions.ProgrammingError(f"Invalid parameter type, {type_}")
    tname, sub = m.groups()
    tname = tname.upper()
    sub = sub.strip()
    if tname == "ARRAY":
        if not array_like(value):
            raise exceptions.ProgrammingError(
                f"Array type with non-array-like value"
                f" with type {type(value).__name__}"
            )
        array_type = complex_query_parameter_type(name, sub, base)
        if isinstance(array_type, query.ArrayQueryParameterType):
            raise exceptions.ProgrammingError(f"Array can't contain an array in {base}")
        return query.ArrayQueryParameter(
            name,
            array_type,
            [complex_query_parameter(None, v, sub, base) for v in value]
            if "<" in sub
            else value,
        )
    else:
        fields = []
        if not isinstance(value, collections_abc.Mapping):
            raise exceptions.ProgrammingError(f"Non-mapping value for type {type_}")
        value_keys = set(value)
        for field_string in split_struct_fields(sub):
            field_string = field_string.strip()
            m = parse_struct_field(field_string)
            if not m:
                raise exceptions.ProgrammingError(
                    f"Invalid struct field, {field_string}, in {base or type_}"
                )
            field_name, field_type = m.groups()
            if field_name not in value:
                raise exceptions.ProgrammingError(
                    f"No field value for {field_name} in {type_}"
                )
            value_keys.remove(field_name)
            fields.append(
                complex_query_parameter(field_name, value[field_name], field_type, base)
            )
        if value_keys:
            raise exceptions.ProgrammingError(f"Extra data keys for {type_}")

        return query.StructQueryParameter(name, *fields)


def to_query_parameters_list(parameters, parameter_types):
    """Converts a sequence of parameter values into query parameters.

    Args:
        parameters (Sequence[Any]): Sequence of query parameter values.
        parameter_types:
            A list of parameter types, one for each parameter.
            Unknown types are provided as None.

    Returns:
        List[google.cloud.bigquery.query._AbstractQueryParameter]:
            A list of query parameters.
    """
    result = []

    for value, type_ in zip(parameters, parameter_types):
        if type_ is not None and "<" in type_:
            param = complex_query_parameter(None, value, type_)
        elif isinstance(value, collections_abc.Mapping):
            raise NotImplementedError("STRUCT-like parameter values are not supported.")
        elif array_like(value):
            param = array_to_query_parameter(value, None, type_)
        else:
            param = scalar_to_query_parameter(value, None, type_)

        result.append(param)

    return result


def to_query_parameters_dict(parameters, query_parameter_types):
    """Converts a dictionary of parameter values into query parameters.

    Args:
        parameters (Mapping[str, Any]): Dictionary of query parameter values.
        parameter_types:
            A dictionary of parameter types. It needn't have a key for each
            parameter.

    Returns:
        List[google.cloud.bigquery.query._AbstractQueryParameter]:
            A list of named query parameters.
    """
    result = []

    for name, value in parameters.items():
        query_parameter_type = query_parameter_types.get(name)
        if query_parameter_type is not None and "<" in query_parameter_type:
            param = complex_query_parameter(name, value, query_parameter_type)
        elif isinstance(value, collections_abc.Mapping):
            raise NotImplementedError(
                "STRUCT-like parameter values are not supported "
                "(parameter {}).".format(name)
            )
        elif array_like(value):
            param = array_to_query_parameter(
                value, name=name, query_parameter_type=query_parameter_type
            )
        else:
            param = scalar_to_query_parameter(
                value, name=name, query_parameter_type=query_parameter_type,
            )

        result.append(param)

    return result


def to_query_parameters(parameters, parameter_types):
    """Converts DB-API parameter values into query parameters.

    Args:
        parameters (Union[Mapping[str, Any], Sequence[Any]]):
            A dictionary or sequence of query parameter values.
        parameter_types (Union[Mapping[str, str], Sequence[str]]):
            A dictionary or list of parameter types.

            If parameters is a mapping, then this must be a dictionary
            of parameter types.  It needn't have a key for each
            parameter.

            If parameters is a sequence, then this must be a list of
            parameter types, one for each paramater.  Unknown types
            are provided as None.

    Returns:
        List[google.cloud.bigquery.query._AbstractQueryParameter]:
            A list of query parameters.
    """
    if parameters is None:
        return []

    if isinstance(parameters, collections_abc.Mapping):
        return to_query_parameters_dict(parameters, parameter_types)
    else:
        return to_query_parameters_list(parameters, parameter_types)


def bigquery_scalar_type(value):
    """Return a BigQuery name of the scalar type that matches the given value.

    If the scalar type name could not be determined (e.g. for non-scalar
    values), ``None`` is returned.

    Args:
        value (Any)

    Returns:
        Optional[str]: The BigQuery scalar type name.
    """
    if isinstance(value, bool):
        return "BOOL"
    elif isinstance(value, numbers.Integral):
        return "INT64"
    elif isinstance(value, numbers.Real):
        return "FLOAT64"
    elif isinstance(value, decimal.Decimal):
        vtuple = value.as_tuple()
        # NUMERIC values have precision of 38 (number of digits) and scale of 9 (number
        # of fractional digits), and their max absolute value must be strictly smaller
        # than 1.0E+29.
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types
        if (
            len(vtuple.digits) <= 38  # max precision: 38
            and vtuple.exponent >= -9  # max scale: 9
            and _NUMERIC_SERVER_MIN <= value <= _NUMERIC_SERVER_MAX
        ):
            return "NUMERIC"
        else:
            return "BIGNUMERIC"

    elif isinstance(value, str):
        return "STRING"
    elif isinstance(value, bytes):
        return "BYTES"
    elif isinstance(value, datetime.datetime):
        return "DATETIME" if value.tzinfo is None else "TIMESTAMP"
    elif isinstance(value, datetime.date):
        return "DATE"
    elif isinstance(value, datetime.time):
        return "TIME"

    return None


def array_like(value):
    """Determine if the given value is array-like.

    Examples of array-like values (as interpreted by this function) are
    sequences such as ``list`` and ``tuple``, but not strings and other
    iterables such as sets.

    Args:
        value (Any)

    Returns:
        bool: ``True`` if the value is considered array-like, ``False`` otherwise.
    """
    return isinstance(value, collections_abc.Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    )


def to_bq_table_rows(rows_iterable):
    """Convert table rows to BigQuery table Row instances.

    Args:
        rows_iterable (Iterable[Mapping]):
            An iterable of row data items to convert to ``Row`` instances.

    Returns:
        Iterable[google.cloud.bigquery.table.Row]
    """

    def to_table_row(row):
        # NOTE: We fetch ARROW values, thus we need to convert them to Python
        # objects with as_py().
        values = tuple(value.as_py() for value in row.values())
        keys_to_index = {key: i for i, key in enumerate(row.keys())}
        return table.Row(values, keys_to_index)

    return (to_table_row(row_data) for row_data in rows_iterable)


def raise_on_closed(
    exc_msg, exc_class=exceptions.ProgrammingError, closed_attr_name="_closed"
):
    """Make public instance methods raise an error if the instance is closed."""

    def _raise_on_closed(method):
        """Make a non-static method raise an error if its containing instance is closed.
        """

        def with_closed_check(self, *args, **kwargs):
            if getattr(self, closed_attr_name):
                raise exc_class(exc_msg)
            return method(self, *args, **kwargs)

        functools.update_wrapper(with_closed_check, method)
        return with_closed_check

    def decorate_public_methods(klass):
        """Apply ``_raise_on_closed()`` decorator to public instance methods.
        """
        for name in dir(klass):
            if name.startswith("_") and name != "__iter__":
                continue

            member = getattr(klass, name)
            if not callable(member):
                continue

            # We need to check for class/static methods directly in the instance
            # __dict__, not via the retrieved attribute (`member`), as the
            # latter is already a callable *produced* by one of these descriptors.
            if isinstance(klass.__dict__[name], (staticmethod, classmethod)):
                continue

            member = _raise_on_closed(member)
            setattr(klass, name, member)

        return klass

    return decorate_public_methods
