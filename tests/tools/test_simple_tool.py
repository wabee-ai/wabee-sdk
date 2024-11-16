import pytest
from pydantic import BaseModel
from typing import Optional
from wabee.tools.simple_tool import simple_tool
from wabee.tools.tool_error import ToolError, ToolErrorType

# Test schemas
class AdditionSchema(BaseModel):
    x: int
    y: int

class PersonSchema(BaseModel):
    name: str
    age: int
    email: Optional[str] = None

# Test functions with different decorator patterns
@simple_tool(schema=AdditionSchema)
async def add_with_schema(input_data):
    return input_data.x + input_data.y

@simple_tool()  # Test without predefined schema
async def add_with_fields(x: int, y: int):
    return x + y

@simple_tool()
async def greet(name: str):
    return f"Hello, {name}!"

@simple_tool(schema=PersonSchema)
async def process_person(input_data):
    if input_data.age < 0:
        raise ValueError("Age cannot be negative")
    return f"Processed {input_data.name}, age {input_data.age}"

# Tests
@pytest.mark.asyncio
async def test_tool_with_predefined_schema():
    result, error = await add_with_schema(x=5, y=3)
    assert result == 8
    assert error is None

@pytest.mark.asyncio
async def test_tool_with_inline_schema():
    result, error = await add_with_fields(x=10, y=20)
    assert result == 30
    assert error is None

@pytest.mark.asyncio
async def test_tool_without_schema():
    result, error = await greet(name="Alice")
    print(f"error: {error}")
    assert result == "Hello, Alice!"
    assert error is None

@pytest.mark.asyncio
async def test_invalid_input_for_schema():
    result, error = await add_with_schema(x="not a number", y=3)
    assert result is None
    assert isinstance(error, ToolError)
    assert error.type == ToolErrorType.INVALID_INPUT

@pytest.mark.asyncio
async def test_missing_required_field():
    result, error = await add_with_schema(x=5)  # missing y
    assert result is None
    assert isinstance(error, ToolError)
    assert error.type == ToolErrorType.INVALID_INPUT

@pytest.mark.asyncio
async def test_optional_field():
    result, error = await process_person(name="Bob", age=30)
    assert result == "Processed Bob, age 30"
    assert error is None

    result, error = await process_person(name="Alice", age=25, email="alice@example.com")
    assert result == "Processed Alice, age 25"
    assert error is None

@pytest.mark.asyncio
async def test_business_logic_error():
    result, error = await process_person(name="Charlie", age=-5)
    assert result is None
    assert isinstance(error, ToolError)
    assert error.type == ToolErrorType.EXECUTION_ERROR
    assert "Age cannot be negative" in error.message

@pytest.mark.asyncio
async def test_type_validation():
    result, error = await add_with_fields(x="invalid", y="invalid")
    assert result is None
    assert isinstance(error, ToolError)
    assert error.type == ToolErrorType.INVALID_INPUT

@pytest.mark.asyncio
async def test_complex_schema_validation():
    result, error = await process_person(
        name="Dave",
        age=40,
        email="invalid-email"  # Invalid email format
    )
    assert result == "Processed Dave, age 40"  # Should pass as email is optional
    assert error is None
