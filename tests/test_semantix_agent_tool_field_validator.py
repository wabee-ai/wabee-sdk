import json
from typing import Any

from pydantic import field_validator
import pytest

from semantix_agent_tools.semantix_agent_tool_config import SemantixAgentToolConfig
from semantix_agent_tools.semantix_agent_tool_input import SemantixAgentToolInput


def semantix_agent_tool_field_validator(
    __field: str,
    *fields: str,
) -> Any:
    return field_validator(__field, *fields, mode="after", check_fields=None)


class TestSemantixAgentToolFieldValidator:
    def test_should_validate_agent_tool_fields_on_config(self) -> None:
        class SemantixAgentToolConfigChild(SemantixAgentToolConfig):
            x: int
            y: int

            @semantix_agent_tool_field_validator("x", "y")
            def check_fields(cls, value: int) -> int:
                if value <= 0:
                    raise ValueError("Field cannot be smaller than zero!")
                return value


        with pytest.raises(Exception):
            SemantixAgentToolConfigChild(x=-1, y=0, name="any_name", description="any_description")

    def test_should_validate_agent_tool_fields_on_input(self) -> None:
        class SemantixAgentToolInputChild(SemantixAgentToolInput):
            x: int

            @semantix_agent_tool_field_validator("x")
            def check_fields(cls, value: int) -> int:
                if value <= 0:
                    raise ValueError("Field cannot be smaller than zero!")
                return value


        with pytest.raises(Exception):
            SemantixAgentToolInputChild.query_to_tool_input(json.dumps({"x": -1}))
