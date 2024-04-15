from typing import Any

from pydantic import field_validator


def semantix_agent_tool_field_validator(
    *fields: str,
) -> Any:
    return field_validator(*fields, mode="after", check_fields=None)
