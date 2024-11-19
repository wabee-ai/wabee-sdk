from typing import Type, get_type_hints, Any, Dict, List
from pydantic import BaseModel
import inspect
from dataclasses import dataclass

@dataclass
class ProtoField:
    name: str
    type: str
    number: int
    required: bool = True
    description: str = ""

@dataclass
class ProtoMessage:
    name: str
    fields: List[ProtoField]
    package: str = "wabee.tools"
    
class ProtoSchemaGenerator:
    TYPE_MAPPING = {
        int: "int64",
        str: "string",
        float: "double",
        bool: "bool",
        dict: "bytes",  # For complex nested structures
        list: "repeated bytes",  # For arrays
    }
    
    @classmethod
    def generate_from_pydantic(
        cls,
        model: Type[BaseModel],
        message_name: str
    ) -> ProtoMessage:
        fields = []
        for i, (name, field) in enumerate(model.model_fields.items(), start=1):
            proto_type = cls.TYPE_MAPPING.get(field.annotation.__class__, "bytes")
            fields.append(ProtoField(
                name=name,
                type=proto_type,
                number=i,
                required=field.is_required(),
                description=field.description or ""
            ))
        return ProtoMessage(message_name, fields)

    @classmethod
    def generate_from_function(
        cls,
        func: Any,
        message_name: str
    ) -> ProtoMessage:
        hints = get_type_hints(func)
        sig = inspect.signature(func)
        
        fields = []
        for i, (name, param) in enumerate(sig.parameters.items(), start=1):
            if name == 'self' or name == 'cls':
                continue
                
            param_type = hints.get(name, Any)
            proto_type = cls.TYPE_MAPPING.get(param_type, "bytes")
            required = param.default == inspect.Parameter.empty
            
            fields.append(ProtoField(
                name=name,
                type=proto_type,
                number=i,
                required=required
            ))
            
        return ProtoMessage(message_name, fields)

    @classmethod
    def get_tool_schema(cls, tool: Any) -> Dict[str, Any]:
        """Get schema information for a tool"""
        if hasattr(tool, 'args_schema'):
            schema = tool.args_schema.model_json_schema()
        else:
            hints = get_type_hints(tool)
            sig = inspect.signature(tool)
            schema = {
                "properties": {
                    name: {"type": str(typ)}
                    for name, typ in hints.items()
                    if name != "return"
                },
                "required": [
                    name for name, param in sig.parameters.items()
                    if param.default == inspect.Parameter.empty
                ]
            }
        return schema
