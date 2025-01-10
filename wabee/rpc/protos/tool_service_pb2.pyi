from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Int64Value(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class StringValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class FloatValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...

class ExecuteRequest(_message.Message):
    __slots__ = ("tool_name", "json_data", "proto_data")
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    JSON_DATA_FIELD_NUMBER: _ClassVar[int]
    PROTO_DATA_FIELD_NUMBER: _ClassVar[int]
    tool_name: str
    json_data: str
    proto_data: bytes
    def __init__(self, tool_name: _Optional[str] = ..., json_data: _Optional[str] = ..., proto_data: _Optional[bytes] = ...) -> None: ...

class ImageToolResponse(_message.Message):
    __slots__ = ("mime_type", "data")
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    mime_type: str
    data: str
    def __init__(self, mime_type: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class StructuredToolResponse(_message.Message):
    __slots__ = ("variable_name", "content", "local_file_path", "metadata", "memory_push", "images", "error")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    VARIABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    LOCAL_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    MEMORY_PUSH_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    variable_name: str
    content: str
    local_file_path: str
    metadata: _containers.ScalarMap[str, str]
    memory_push: bool
    images: _containers.RepeatedCompositeFieldContainer[ImageToolResponse]
    error: str
    def __init__(self, variable_name: _Optional[str] = ..., content: _Optional[str] = ..., local_file_path: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., memory_push: bool = ..., images: _Optional[_Iterable[_Union[ImageToolResponse, _Mapping]]] = ..., error: _Optional[str] = ...) -> None: ...

class ExecuteResponse(_message.Message):
    __slots__ = ("json_result", "proto_result", "structured_result", "error")
    JSON_RESULT_FIELD_NUMBER: _ClassVar[int]
    PROTO_RESULT_FIELD_NUMBER: _ClassVar[int]
    STRUCTURED_RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    json_result: str
    proto_result: bytes
    structured_result: StructuredToolResponse
    error: ToolError
    def __init__(self, json_result: _Optional[str] = ..., proto_result: _Optional[bytes] = ..., structured_result: _Optional[_Union[StructuredToolResponse, _Mapping]] = ..., error: _Optional[_Union[ToolError, _Mapping]] = ...) -> None: ...

class ToolError(_message.Message):
    __slots__ = ("type", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    message: str
    def __init__(self, type: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class GetToolSchemaRequest(_message.Message):
    __slots__ = ("tool_name",)
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    tool_name: str
    def __init__(self, tool_name: _Optional[str] = ...) -> None: ...

class ToolSchema(_message.Message):
    __slots__ = ("tool_name", "description", "fields")
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    tool_name: str
    description: str
    fields: _containers.RepeatedCompositeFieldContainer[FieldSchema]
    def __init__(self, tool_name: _Optional[str] = ..., description: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[FieldSchema, _Mapping]]] = ...) -> None: ...

class FieldSchema(_message.Message):
    __slots__ = ("name", "type", "required", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    required: bool
    description: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., required: bool = ..., description: _Optional[str] = ...) -> None: ...
