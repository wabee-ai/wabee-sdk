from abc import ABC, abstractmethod
from wabee.tools.tool_error import ToolError, ToolErrorType
from wabee.tools.base_model import StructuredToolResponse
from typing import TypeVar, Generic, Optional, Dict, Type, Any
from pydantic import BaseModel, ValidationError

InputType = TypeVar('InputType', Dict, BaseModel)
OutputType = TypeVar('OutputType', bound=StructuredToolResponse)

class BaseTool(ABC, Generic[InputType, OutputType]):
    args_schema: Optional[Type[BaseModel]] = None
    
    def __init__(
        self,
        name: str,
        description: str,
        **kwargs: Any
    ) -> None:
        """
        Initialize the tool with required name and description, plus optional arguments.
        
        Args:
            name: The name of the tool
            description: A description of what the tool does
            **kwargs: Additional tool-specific configuration
        """
        self.name = name
        self.description = description
        
        # Set any additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    @property
    def tool_name(self) -> str:
        """Return the tool's name."""
        return self.name
            
    @abstractmethod
    async def execute(self, input_data: InputType) -> tuple[Optional[OutputType], Optional[ToolError]]:
        """
        Main execution method for the tool.
        Returns either (result, None) or (None, error)
        """
        pass

    async def validate_input(self, input_data: InputType) -> tuple[bool, Optional[str]]:
        """
        Validate input before execution.
        Override this method to add custom validation logic.
        Returns (is_valid, error_message)
        """
        # If args_schema is specified, validate against it
        if self.args_schema is not None:
            try:
                if isinstance(input_data, dict):
                    self.args_schema.model_validate(input_data)
                elif isinstance(input_data, BaseModel):
                    if not isinstance(input_data, self.args_schema):
                        return False, f"Input must be an instance of {self.args_schema.__name__}"
                else:
                    return False, "Input must be either a dict or a BaseModel instance"
            except ValidationError as e:
                return False, str(e)
        
        return True, None

    async def __call__(self, input_data: InputType) -> tuple[Optional[OutputType], Optional[ToolError]]:
        is_valid, error_msg = await self.validate_input(input_data)
        if not is_valid:
            return None, ToolError(
                type=ToolErrorType.INVALID_INPUT,
                message=error_msg or "Invalid input"
            )
        return await self.execute(input_data)
