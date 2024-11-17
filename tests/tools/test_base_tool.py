import pytest
from pydantic import BaseModel
from typing import Optional, Dict, Any
from wabee.tools.base_tool import BaseTool
from wabee.tools.tool_error import ToolError, ToolErrorType

# Test schemas
class TestInputSchema(BaseModel):
    value: int
    text: str

class TestOutputSchema(BaseModel):
    result: str

# Test implementation of BaseTool
class TestTool(BaseTool[Dict, str]):
    args_schema = TestInputSchema

    async def execute(self, input_data: Dict) -> tuple[Optional[str], Optional[ToolError]]:
        return f"Processed: {input_data['value']}", None

class CustomValidationTool(BaseTool[Dict, str]):
    args_schema = TestInputSchema

    async def validate_input(self, input_data: Dict) -> tuple[bool, Optional[str]]:
        if input_data.get('value', 0) <= 0:
            return False, "Value must be positive"
        return True, None

    async def execute(self, input_data: Dict) -> tuple[Optional[str], Optional[ToolError]]:
        return f"Valid input: {input_data['value']}", None

@pytest.fixture
def basic_tool():
    return TestTool()

@pytest.fixture
def custom_validation_tool():
    return CustomValidationTool()

@pytest.mark.asyncio
async def test_tool_initialization():
    tool = TestTool(custom_param="test")
    assert hasattr(tool, "custom_param")
    assert tool.custom_param == "test"

@pytest.mark.asyncio
async def test_valid_input_validation(basic_tool):
    valid_input = {"value": 42, "text": "test"}
    is_valid, error = await basic_tool.validate_input(valid_input)
    assert is_valid
    assert error is None

@pytest.mark.asyncio
async def test_invalid_input_validation(basic_tool):
    invalid_input = {"value": "not an int", "text": "test"}
    is_valid, error = await basic_tool.validate_input(invalid_input)
    assert not is_valid
    assert error is not None

@pytest.mark.asyncio
async def test_missing_field_validation(basic_tool):
    invalid_input = {"value": 42}  # missing 'text' field
    is_valid, error = await basic_tool.validate_input(invalid_input)
    assert not is_valid
    assert error is not None

@pytest.mark.asyncio
async def test_custom_validation(custom_validation_tool):
    invalid_input = {"value": -1, "text": "test"}
    is_valid, error = await custom_validation_tool.validate_input(invalid_input)
    assert not is_valid
    assert error == "Value must be positive"

@pytest.mark.asyncio
async def test_successful_execution(basic_tool):
    valid_input = {"value": 42, "text": "test"}
    result, error = await basic_tool(valid_input)
    assert result == "Processed: 42"
    assert error is None

@pytest.mark.asyncio
async def test_execution_with_invalid_input(basic_tool):
    invalid_input = {"value": "not an int", "text": "test"}
    result, error = await basic_tool(invalid_input)
    assert result is None
    assert isinstance(error, ToolError)
    assert error.type == ToolErrorType.INVALID_INPUT

@pytest.mark.asyncio
async def test_basemodel_input_validation(basic_tool):
    valid_input = TestInputSchema(value=42, text="test")
    is_valid, error = await basic_tool.validate_input(valid_input)
    assert is_valid
    assert error is None

@pytest.mark.asyncio
async def test_invalid_input_type(basic_tool):
    invalid_input = "not a dict or BaseModel"
    is_valid, error = await basic_tool.validate_input(invalid_input)
    assert not is_valid
    assert error == "Input must be either a dict or a BaseModel instance"
