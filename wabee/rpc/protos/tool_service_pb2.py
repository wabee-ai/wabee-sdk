# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: wabee/rpc/protos/tool_service.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'wabee/rpc/protos/tool_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#wabee/rpc/protos/tool_service.proto\x12\x0bwabee.tools\"\x1b\n\nInt64Value\x12\r\n\x05value\x18\x01 \x01(\x03\"\x1c\n\x0bStringValue\x12\r\n\x05value\x18\x01 \x01(\t\"\x1b\n\nFloatValue\x12\r\n\x05value\x18\x01 \x01(\x01\"W\n\x0e\x45xecuteRequest\x12\x11\n\ttool_name\x18\x01 \x01(\t\x12\x13\n\tjson_data\x18\x02 \x01(\tH\x00\x12\x14\n\nproto_data\x18\x03 \x01(\x0cH\x00\x42\x07\n\x05input\"q\n\x0f\x45xecuteResponse\x12\x15\n\x0bjson_result\x18\x01 \x01(\tH\x00\x12\x16\n\x0cproto_result\x18\x02 \x01(\x0cH\x00\x12%\n\x05\x65rror\x18\x03 \x01(\x0b\x32\x16.wabee.tools.ToolErrorB\x08\n\x06result\"*\n\tToolError\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\")\n\x14GetToolSchemaRequest\x12\x11\n\ttool_name\x18\x01 \x01(\t\"I\n\nToolSchema\x12\x11\n\ttool_name\x18\x01 \x01(\t\x12(\n\x06\x66ields\x18\x02 \x03(\x0b\x32\x18.wabee.tools.FieldSchema\"P\n\x0b\x46ieldSchema\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x10\n\x08required\x18\x03 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t2\xa0\x01\n\x0bToolService\x12\x44\n\x07\x45xecute\x12\x1b.wabee.tools.ExecuteRequest\x1a\x1c.wabee.tools.ExecuteResponse\x12K\n\rGetToolSchema\x12!.wabee.tools.GetToolSchemaRequest\x1a\x17.wabee.tools.ToolSchemab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'wabee.rpc.protos.tool_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_INT64VALUE']._serialized_start=52
  _globals['_INT64VALUE']._serialized_end=79
  _globals['_STRINGVALUE']._serialized_start=81
  _globals['_STRINGVALUE']._serialized_end=109
  _globals['_FLOATVALUE']._serialized_start=111
  _globals['_FLOATVALUE']._serialized_end=138
  _globals['_EXECUTEREQUEST']._serialized_start=140
  _globals['_EXECUTEREQUEST']._serialized_end=227
  _globals['_EXECUTERESPONSE']._serialized_start=229
  _globals['_EXECUTERESPONSE']._serialized_end=342
  _globals['_TOOLERROR']._serialized_start=344
  _globals['_TOOLERROR']._serialized_end=386
  _globals['_GETTOOLSCHEMAREQUEST']._serialized_start=388
  _globals['_GETTOOLSCHEMAREQUEST']._serialized_end=429
  _globals['_TOOLSCHEMA']._serialized_start=431
  _globals['_TOOLSCHEMA']._serialized_end=504
  _globals['_FIELDSCHEMA']._serialized_start=506
  _globals['_FIELDSCHEMA']._serialized_end=586
  _globals['_TOOLSERVICE']._serialized_start=589
  _globals['_TOOLSERVICE']._serialized_end=749
# @@protoc_insertion_point(module_scope)