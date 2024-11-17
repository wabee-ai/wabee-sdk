
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ToolErrorType(Enum):
    RETRYABLE = "retryable"
    PERMANENT = "permanent"
    INVALID_INPUT = "invalid_input"
    INTERNAL_ERROR = "internal_error"
    VALIDATION_ERROR = "validation_error"
    EXECUTION_ERROR = "execution_error"

@dataclass
class ToolError:
    type: ToolErrorType
    message: str
    original_error: Optional[Exception] = None
