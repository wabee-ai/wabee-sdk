
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ToolErrorType(Enum):
    RETRYABLE = "retryable"
    PERMANENT = "permanent"
    INVALID_INPUT = "invalid_input"

@dataclass
class ToolError:
    type: ToolErrorType
    message: str
    original_error: Optional[Exception] = None