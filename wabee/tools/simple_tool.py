from functools import wraps
from typing import Callable, Type, Optional, Any, Union, TypeVar, Awaitable
from typing_extensions import ParamSpec
from pydantic import BaseModel, create_model, ConfigDict

from wabee.tools.base_tool import BaseTool
from wabee.tools.tool_error import ToolError, ToolErrorType
from wabee.tools.base_model import StructuredToolResponse

T = TypeVar('T')
P = ParamSpec('P')

def simple_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    schema: Optional[Type[BaseModel]] = None,
    **schema_fields: Any
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[tuple[Optional[StructuredToolResponse], Optional[ToolError]]]]]:
    """
    A decorator that transforms a simple async function into a BaseTool-compatible interface.
    
    Can be used in these ways:
    1. With inline schema fields: @simple_tool(name="Add", description="Adds numbers", x=int, y=int)
    2. With a predefined schema: @simple_tool(name="Add", description="Adds numbers", schema=MySchema)
    3. Without any schema: @simple_tool(name="Add", description="Adds numbers")
    4. With automatic name/description: @simple_tool()
    
    Args:
        name: Optional name for the tool (defaults to function name)
        description: Optional description (defaults to function docstring)
        schema: Optional predefined Pydantic model for input validation
        **schema_fields: Field definitions to create an ad-hoc Pydantic model
        
    Returns:
        A decorator that wraps the function in a BaseTool-compatible interface
        
    Example:
        @simple_tool(x=int, y=int)
        async def add_numbers(input_data):
            return input_data.x + input_data.y
            
        result, error = await add_numbers(x=5, y=3)
    """
    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[tuple[Optional[T], Optional[ToolError]]]]:
        # Create a schema on the fly if fields are provided but no schema
        if schema is None and schema_fields:
            # Convert field definitions to proper Pydantic field annotations
            annotated_fields = {
                field_name: (field_type, ...)  # ... means required
                for field_name, field_type in schema_fields.items()
            }
            model_name = f"{func.__name__.title()}Input"
            dynamic_schema = create_model(
                model_name,
                __config__=ConfigDict(arbitrary_types_allowed=True),
                __module__=func.__module__,
                __base__=None,
                **annotated_fields
            )
        else:
            dynamic_schema = schema

        @wraps(func)
        async def wrapped_tool(*args: P.args, **kwargs: P.kwargs) -> tuple[Union[StructuredToolResponse, None], Optional[ToolError]]:
            # Get tool name and description
            tool_name = name or func.__name__
            tool_description = description or func.__doc__ or ""
            
            # Create an anonymous class inheriting from BaseTool
            class FunctionalTool(BaseTool):
                args_schema = dynamic_schema

                def __init__(self):
                    super().__init__(name=tool_name, description=tool_description)

                async def execute(self, input_data: Any) -> tuple[Union[T, None], Optional[ToolError]]:
                    try:
                        # Validate and convert input to Pydantic model if schema exists
                        if dynamic_schema:
                            if isinstance(input_data, dict):
                                validated_input = dynamic_schema(**input_data)
                            elif isinstance(input_data, dynamic_schema):
                                validated_input = input_data
                            else:
                                raise ValueError(f"Input must be dict or {dynamic_schema.__name__}")
                            result = await func(validated_input)
                        else:
                            # For functions without schema, validate against type hints
                            try:
                                # Create a dynamic model from function annotations
                                hints = func.__annotations__
                                if hints:
                                    fields = {
                                        name: (typ, ...) for name, typ in hints.items()
                                        if name != 'return'
                                    }
                                    model_name = f"{func.__name__}RuntimeSchema"
                                    runtime_schema = create_model(
                                        model_name,
                                        __config__=ConfigDict(arbitrary_types_allowed=True),
                                        __module__=func.__module__,
                                        __base__=None,
                                        **fields
                                    )
                                    # Validate kwargs against the runtime schema
                                    validated_kwargs = runtime_schema(**kwargs).dict()
                                    result = await func(**validated_kwargs)
                                else:
                                    # When no schema and no type hints, pass args/kwargs directly 
                                    if args:
                                        result = await func(*args)
                                    else:
                                        result = await func(**kwargs)
                            except (ValueError, TypeError) as e:
                                return None, ToolError(
                                    type=ToolErrorType.INVALID_INPUT,
                                    message=str(e),
                                    original_error=e
                                )
                        return result, None
                    except ValueError as e:
                        # Business logic errors raised by the function
                        return None, ToolError(
                            type=ToolErrorType.EXECUTION_ERROR,
                            message=str(e),
                            original_error=e
                        )
                    except AttributeError as e:
                        # Schema validation/access errors
                        return None, ToolError(
                            type=ToolErrorType.INVALID_INPUT,
                            message=str(e),
                            original_error=e
                        )
                    except Exception as e:
                        # Unexpected errors
                        return None, ToolError(
                            type=ToolErrorType.INTERNAL_ERROR,
                            message=str(e),
                            original_error=e
                        )

            # Create and call the tool instance
            tool = FunctionalTool()
            return await tool(kwargs if dynamic_schema else args[0] if args else kwargs)

        return wrapped_tool

    return decorator
