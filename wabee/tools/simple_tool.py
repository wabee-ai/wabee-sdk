from functools import wraps
from typing import Callable, Type, Optional, Any, Union, TypeVar
from pydantic import BaseModel, create_model

from wabee.tools.base_tool import BaseTool
from wabee.tools.tool_error import ToolError, ToolErrorType

T = TypeVar('T')

def simple_tool(
    schema: Optional[Type[BaseModel]] = None,
    **schema_fields: Any
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    A decorator that transforms a simple async function into a BaseTool-compatible interface.
    
    Can be used in three ways:
    1. With inline schema fields: @simple_tool(x=int, y=int)
    2. With a predefined schema: @simple_tool(schema=MySchema)
    3. Without any schema: @simple_tool()
    
    Args:
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
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Create a schema on the fly if fields are provided but no schema
        if schema is None and schema_fields:
            # Convert field definitions to proper Pydantic field annotations
            annotated_fields = {
                field_name: (field_type, ...)  # ... means required
                for field_name, field_type in schema_fields.items()
            }
            dynamic_schema = create_model(
                f"{func.__name__.title()}Input",
                **annotated_fields
            )
        else:
            dynamic_schema = schema

        @wraps(func)
        async def wrapped_tool(*args: Any, **kwargs: Any) -> tuple[Union[T, None], Optional[ToolError]]:
            # Create an anonymous class inheriting from BaseTool
            class FunctionalTool(BaseTool):
                args_schema = dynamic_schema

                async def execute(self, input_data: Any) -> tuple[Union[T, None], Optional[ToolError]]:
                    try:
                        # Validate and convert input to Pydantic model if schema exists
                        if dynamic_schema:
                            if isinstance(input_data, dict):
                                validated_input = dynamic_schema(**input_data)
                            else:
                                validated_input = input_data
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
                                    runtime_schema = create_model(
                                        f"{func.__name__}RuntimeSchema",
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
