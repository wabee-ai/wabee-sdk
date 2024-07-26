from typing import Any

from langchain.pydantic_v1 import validator


def wabee_agent_tool_field_validator(
    *fields: str,
    **kwargs,
) -> Any:
    return validator(*fields, **kwargs)
