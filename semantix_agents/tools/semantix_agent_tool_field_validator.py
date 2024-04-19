from typing import Any

from langchain.pydantic_v1 import validator


def semantix_agent_tool_field_validator(
    *fields: str,
) -> Any:
    return validator(*fields)
