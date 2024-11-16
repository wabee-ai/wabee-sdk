from abc import ABC, abstractmethod
from wabee.tools.tool_error import ToolError, ToolErrorType
from typing import TypeVar, Generic, Optional, Union, Dict
from pydantic import BaseModel

# Input type remains generic, output is constrained to str or BaseModel
I = TypeVar('I', Dict, BaseModel)
O = TypeVar('O', str, Dict, BaseModel)

class BaseTool(ABC, Generic[I, O]):
    @abstractmethod
    async def execute(self, input_data: I) -> tuple[O | None, ToolError | None]:
        """
        Main execution method for the tool.
        Returns either (result, None) or (None, error)
        """
        pass

    @abstractmethod
    async def validate_input(self, input_data: I) -> tuple[bool, Optional[str]]:
        """
        Validate input before execution
        Returns (is_valid, error_message)
        """
        pass

    async def __call__(self, input_data: I) -> tuple[O | None, ToolError | None]:
        is_valid, error_msg = await self.validate_input(input_data)
        if not is_valid:
            return None, ToolError(
                type=ToolErrorType.INVALID_INPUT,
                message=error_msg or "Invalid input"
            )
        return await self.execute(input_data)

# Example usage:
class APIResponse(BaseModel):
    status: int
    data: str

class APITool(BaseTool[dict, Union[str, APIResponse]]):
    async def validate_input(self, input_data: dict) -> tuple[bool, Optional[str]]:
        if "url" not in input_data:
            return False, "URL is required"
        return True, None

    async def execute(self, input_data: dict) -> tuple[Union[str, APIResponse] | None, ToolError | None]:
        try:
            # Return either a string
            return "success", None
            # Or a Pydantic model
            # return APIResponse(status=200, data="success"), None
        except TimeoutError as e:
            return None, ToolError(
                type=ToolErrorType.RETRYABLE,
                message="API timeout",
                original_error=e
            )