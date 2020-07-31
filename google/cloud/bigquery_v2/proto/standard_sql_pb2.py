# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/bigquery_v2/proto/standard_sql.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/cloud/bigquery_v2/proto/standard_sql.proto",
    package="google.cloud.bigquery.v2",
    syntax="proto3",
    serialized_options=b"\n\034com.google.cloud.bigquery.v2B\020StandardSqlProtoZ@google.golang.org/genproto/googleapis/cloud/bigquery/v2;bigquery",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n1google/cloud/bigquery_v2/proto/standard_sql.proto\x12\x18google.cloud.bigquery.v2\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1cgoogle/api/annotations.proto"\xcb\x03\n\x13StandardSqlDataType\x12N\n\ttype_kind\x18\x01 \x01(\x0e\x32\x36.google.cloud.bigquery.v2.StandardSqlDataType.TypeKindB\x03\xe0\x41\x02\x12K\n\x12\x61rray_element_type\x18\x02 \x01(\x0b\x32-.google.cloud.bigquery.v2.StandardSqlDataTypeH\x00\x12\x46\n\x0bstruct_type\x18\x03 \x01(\x0b\x32/.google.cloud.bigquery.v2.StandardSqlStructTypeH\x00"\xc2\x01\n\x08TypeKind\x12\x19\n\x15TYPE_KIND_UNSPECIFIED\x10\x00\x12\t\n\x05INT64\x10\x02\x12\x08\n\x04\x42OOL\x10\x05\x12\x0b\n\x07\x46LOAT64\x10\x07\x12\n\n\x06STRING\x10\x08\x12\t\n\x05\x42YTES\x10\t\x12\r\n\tTIMESTAMP\x10\x13\x12\x08\n\x04\x44\x41TE\x10\n\x12\x08\n\x04TIME\x10\x14\x12\x0c\n\x08\x44\x41TETIME\x10\x15\x12\r\n\tGEOGRAPHY\x10\x16\x12\x0b\n\x07NUMERIC\x10\x17\x12\t\n\x05\x41RRAY\x10\x10\x12\n\n\x06STRUCT\x10\x11\x42\n\n\x08sub_type"g\n\x10StandardSqlField\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0\x41\x01\x12@\n\x04type\x18\x02 \x01(\x0b\x32-.google.cloud.bigquery.v2.StandardSqlDataTypeB\x03\xe0\x41\x01"S\n\x15StandardSqlStructType\x12:\n\x06\x66ields\x18\x01 \x03(\x0b\x32*.google.cloud.bigquery.v2.StandardSqlFieldBr\n\x1c\x63om.google.cloud.bigquery.v2B\x10StandardSqlProtoZ@google.golang.org/genproto/googleapis/cloud/bigquery/v2;bigqueryb\x06proto3',
    dependencies=[
        google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,
        google_dot_api_dot_annotations__pb2.DESCRIPTOR,
    ],
)


_STANDARDSQLDATATYPE_TYPEKIND = _descriptor.EnumDescriptor(
    name="TypeKind",
    full_name="google.cloud.bigquery.v2.StandardSqlDataType.TypeKind",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name="TYPE_KIND_UNSPECIFIED",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="INT64",
            index=1,
            number=2,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="BOOL",
            index=2,
            number=5,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="FLOAT64",
            index=3,
            number=7,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="STRING",
            index=4,
            number=8,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="BYTES",
            index=5,
            number=9,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="TIMESTAMP",
            index=6,
            number=19,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="DATE",
            index=7,
            number=10,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="TIME",
            index=8,
            number=20,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="DATETIME",
            index=9,
            number=21,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="GEOGRAPHY",
            index=10,
            number=22,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="NUMERIC",
            index=11,
            number=23,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="ARRAY",
            index=12,
            number=16,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="STRUCT",
            index=13,
            number=17,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=396,
    serialized_end=590,
)
_sym_db.RegisterEnumDescriptor(_STANDARDSQLDATATYPE_TYPEKIND)


_STANDARDSQLDATATYPE = _descriptor.Descriptor(
    name="StandardSqlDataType",
    full_name="google.cloud.bigquery.v2.StandardSqlDataType",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="type_kind",
            full_name="google.cloud.bigquery.v2.StandardSqlDataType.type_kind",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\002",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="array_element_type",
            full_name="google.cloud.bigquery.v2.StandardSqlDataType.array_element_type",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="struct_type",
            full_name="google.cloud.bigquery.v2.StandardSqlDataType.struct_type",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[_STANDARDSQLDATATYPE_TYPEKIND,],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="sub_type",
            full_name="google.cloud.bigquery.v2.StandardSqlDataType.sub_type",
            index=0,
            containing_type=None,
            create_key=_descriptor._internal_create_key,
            fields=[],
        ),
    ],
    serialized_start=143,
    serialized_end=602,
)


_STANDARDSQLFIELD = _descriptor.Descriptor(
    name="StandardSqlField",
    full_name="google.cloud.bigquery.v2.StandardSqlField",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="google.cloud.bigquery.v2.StandardSqlField.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="type",
            full_name="google.cloud.bigquery.v2.StandardSqlField.type",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=604,
    serialized_end=707,
)


_STANDARDSQLSTRUCTTYPE = _descriptor.Descriptor(
    name="StandardSqlStructType",
    full_name="google.cloud.bigquery.v2.StandardSqlStructType",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="fields",
            full_name="google.cloud.bigquery.v2.StandardSqlStructType.fields",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=709,
    serialized_end=792,
)

_STANDARDSQLDATATYPE.fields_by_name[
    "type_kind"
].enum_type = _STANDARDSQLDATATYPE_TYPEKIND
_STANDARDSQLDATATYPE.fields_by_name[
    "array_element_type"
].message_type = _STANDARDSQLDATATYPE
_STANDARDSQLDATATYPE.fields_by_name["struct_type"].message_type = _STANDARDSQLSTRUCTTYPE
_STANDARDSQLDATATYPE_TYPEKIND.containing_type = _STANDARDSQLDATATYPE
_STANDARDSQLDATATYPE.oneofs_by_name["sub_type"].fields.append(
    _STANDARDSQLDATATYPE.fields_by_name["array_element_type"]
)
_STANDARDSQLDATATYPE.fields_by_name[
    "array_element_type"
].containing_oneof = _STANDARDSQLDATATYPE.oneofs_by_name["sub_type"]
_STANDARDSQLDATATYPE.oneofs_by_name["sub_type"].fields.append(
    _STANDARDSQLDATATYPE.fields_by_name["struct_type"]
)
_STANDARDSQLDATATYPE.fields_by_name[
    "struct_type"
].containing_oneof = _STANDARDSQLDATATYPE.oneofs_by_name["sub_type"]
_STANDARDSQLFIELD.fields_by_name["type"].message_type = _STANDARDSQLDATATYPE
_STANDARDSQLSTRUCTTYPE.fields_by_name["fields"].message_type = _STANDARDSQLFIELD
DESCRIPTOR.message_types_by_name["StandardSqlDataType"] = _STANDARDSQLDATATYPE
DESCRIPTOR.message_types_by_name["StandardSqlField"] = _STANDARDSQLFIELD
DESCRIPTOR.message_types_by_name["StandardSqlStructType"] = _STANDARDSQLSTRUCTTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StandardSqlDataType = _reflection.GeneratedProtocolMessageType(
    "StandardSqlDataType",
    (_message.Message,),
    {
        "DESCRIPTOR": _STANDARDSQLDATATYPE,
        "__module__": "google.cloud.bigquery_v2.proto.standard_sql_pb2",
        "__doc__": """The type of a variable, e.g., a function argument. Examples: INT64:
  {type_kind=``INT64``} ARRAY: {type_kind=``ARRAY``,
  array_element_type=``STRING``} STRUCT<x STRING, y ARRAY>:
  {type_kind=``STRUCT``, struct_type={fields=[ {name=``x``,
  type={type_kind=``STRING``}}, {name=``y``, type={type_kind=``ARRAY``,
  array_element_type=``DATE``}} ]}}
  
  Attributes:
      type_kind:
          Required. The top level type of this field. Can be any
          standard SQL data type (e.g., ``INT64``, ``DATE``, ``ARRAY``).
      array_element_type:
          The type of the array’s elements, if type_kind = ``ARRAY``.
      struct_type:
          The fields of this struct, in order, if type_kind = ``STRUCT``.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.v2.StandardSqlDataType)
    },
)
_sym_db.RegisterMessage(StandardSqlDataType)

StandardSqlField = _reflection.GeneratedProtocolMessageType(
    "StandardSqlField",
    (_message.Message,),
    {
        "DESCRIPTOR": _STANDARDSQLFIELD,
        "__module__": "google.cloud.bigquery_v2.proto.standard_sql_pb2",
        "__doc__": """A field or a column.
  
  Attributes:
      name:
          Optional. The name of this field. Can be absent for struct
          fields.
      type:
          Optional. The type of this parameter. Absent if not explicitly
          specified (e.g., CREATE FUNCTION statement can omit the return
          type; in this case the output parameter does not have this
          ``type`` field).
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.v2.StandardSqlField)
    },
)
_sym_db.RegisterMessage(StandardSqlField)

StandardSqlStructType = _reflection.GeneratedProtocolMessageType(
    "StandardSqlStructType",
    (_message.Message,),
    {
        "DESCRIPTOR": _STANDARDSQLSTRUCTTYPE,
        "__module__": "google.cloud.bigquery_v2.proto.standard_sql_pb2"
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.v2.StandardSqlStructType)
    },
)
_sym_db.RegisterMessage(StandardSqlStructType)


DESCRIPTOR._options = None
_STANDARDSQLDATATYPE.fields_by_name["type_kind"]._options = None
_STANDARDSQLFIELD.fields_by_name["name"]._options = None
_STANDARDSQLFIELD.fields_by_name["type"]._options = None
# @@protoc_insertion_point(module_scope)
